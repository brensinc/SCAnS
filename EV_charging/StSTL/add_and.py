import numpy as np
from StSTL.find_comma import find_comma
from StSTL.search_track_formula import search_track_formula
from StSTL.StSTL_class import StSTL
from StSTL.add_formula import add_formula
import cvxpy as cp

def add_and(str_expr, formu_index, sat_time_hint, neg_prefix):
    """
    Encode an AND formula by assigning binary variables to its sub-formulas and adding
    MIP constraints into the encoding constraint set.

    Parameters:
    - str_expr: string, formula in the form 'f1,f2,...,fm'
    - formu_index: index of this formula in StSTL
    - sat_time_hint: list or np.array of satisfaction times
    - neg_prefix: int, number of negations

    Returns:
    - add_result: int, formu_index if successful, else 0
    """
    
    # # NOT SURE ABOUT THIS!
    # if formu_index == 0:
    #     is_found, formu_index = search_track_formula(f"And({str_expr})", sat_time_hint.tolist(), neg_prefix)
    # if is_found:
    #     print(f"In add_and(): formula already encoded, skipping.")
    #     return formu_index
    # # NOT SURE ABOUT THIS!

    sat_time_hint = np.array(sat_time_hint)
    sat_time_hint = np.atleast_1d(sat_time_hint) # Convert sat_time_hint to a row vector
    if sat_time_hint.ndim != 1:
        raise ValueError("In add_and(), sat_time_hint has to be a row vector.")

    if neg_prefix > 1:
        raise ValueError("neg_prefix should be no larger than 1")

    comma_index, comma_num = find_comma(str_expr)
    given_sub_num = comma_num + 1
    given_sat_num = sat_time_hint.size

    if given_sub_num > 1 and given_sat_num > 1 and given_sub_num != given_sat_num:
        raise ValueError("In add_and(), #sat_time_hint != #subformulas, but both > 1!")

    sub_num = max(given_sub_num, given_sat_num)
    sub_index = [0] * sub_num
    sub_str = [''] * sub_num

    if given_sub_num == 1:
        sub_str = [str_expr] * sub_num
    else:
        sub_str[0] = str_expr[:comma_index[0]]
        for i in range(comma_num - 1):
            sub_str[i + 1] = str_expr[comma_index[i] + 1:comma_index[i + 1]]
        sub_str[sub_num - 1] = str_expr[comma_index[comma_num - 1] + 1:]

    # Test
    sub_str = [s.strip() for s in sub_str]


    if given_sat_num == 1:
        sat_time_hint = np.full(sub_num, sat_time_hint[0])

    for i in range(sub_num):
        is_found, index = search_track_formula(sub_str[i], sat_time_hint[i], neg_prefix) # Adds variables such as formu_bin (?) to the StSTL object
        if is_found and StSTL.display == 1:
            print(f"In add_and(), formula {StSTL.formu_str[index]} with sat_time_hint {StSTL.formu_time[index]}, "
                  f"neg_prefix {StSTL.formu_neg[index]} that has already tracked is revoked by "
                  f"{sub_str[i]} with sat_time_hint {sat_time_hint[i]}")
        sub_index[i] = index

    add_result = 1
    for i in range(sub_num):
        add_result = add_formula(sub_str[i], sub_index[i], sat_time_hint[i], neg_prefix)
        if add_result == 0:
            break

     # Create the binary variable for the overall formula (this is the fix). Should we put this in search_track_formula?
    # StSTL.formu_bin.append(cp.Variable(boolean=True))

    # Ensure subformulas are defined
    for idx in sub_index:
        if StSTL.formu_bin[idx] is None:
            raise ValueError(f"StSTL.formu_bin[{idx}] is None — subformula not encoded properly.")

    if add_result:
        sum_vars = sum(StSTL.formu_bin[idx] for idx in sub_index) # Define AFFINE cvxpy constraint
        if neg_prefix == 0:  # logical AND
            StSTL.MIP_cons.append(sum_vars - sub_num + 1 <= StSTL.formu_bin[formu_index])
            StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] <= (1 / sub_num) * sum_vars)
        else:  # logical OR
            StSTL.MIP_cons.append((1 / sub_num) * sum_vars <= StSTL.formu_bin[formu_index])
            StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] <= sum_vars)

        StSTL.total_MIP_cons += 2
        # return formu_index
        return add_result

    # return -1
    return 0
