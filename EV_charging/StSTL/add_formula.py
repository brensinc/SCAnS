from StSTL.StSTL_class import StSTL

from search_track_formula import search_track_formula

from add_neg import add_neg
from add_until import add_until
from add_weak import add_weak
from add_and import add_and
from add_always import add_always
from add_or import add_or
from add_AP import add_AP


def add_formula(formula, *args):
    """
    Encode a formula by assigning binary variables to its sub-formulas and adding MIP constraints.
    """
    add_result = 1
    if not isinstance(formula, str):
        print("Formula must be a string.")
        return 0
    if not formula.endswith(')'):
        print("Formula must end with )")
        return 0

    var_num = len(args)
    if var_num == 3:
        formu_index, sat_time_hint, neg_prefix = args
    elif var_num == 2:
        formu_index, sat_time_hint = args
        neg_prefix = 0
    elif var_num == 1:
        formu_index = args[0]
        sat_time_hint = -1
        neg_prefix = 0
    elif var_num == 0:
        formu_index = 0
        sat_time_hint = -1
        neg_prefix = 0
    else:
        print("Too many input arguments!")
        return 0

    if formu_index > 0:
        if StSTL.display == 1:
            print(f"In add_formula(): {StSTL.formu_str[formu_index]}, formu_index = {formu_index}, "
                  f"sat_time_hint = {sat_time_hint}, neg_prefix = {neg_prefix}")
        if (formula != StSTL.formu_str[formu_index] or
            StSTL.formu_time[formu_index] != sat_time_hint or
            StSTL.formu_neg[formu_index] != neg_prefix):
            raise ValueError("formu_index is inconsistent with the formula it points to.")
    else:
        if StSTL.display == 1:
            print(f"In add_formula(): {formula} given by user with sat_time_hint = {sat_time_hint}")
        is_found, formu_index = search_track_formula(formula, sat_time_hint, neg_prefix)
        if is_found:
            print(f"Formula {formula} already translated with sat_time_hint {sat_time_hint}. Returning 0.")
            return 0

    MIP_cons_num_prev = StSTL.total_MIP_cons
    formulas_track_num_prev = StSTL.total_formu
    left_par = formula.find('(')

    if left_par == -1:
        raise ValueError("No ( found in the formula.")
    if left_par == 0:
        raise ValueError("( found at the very beginning of the formula.")

    neg_prefix = neg_prefix % 2
    op = formula[:left_par]
    args_str = formula[left_par + 1:-1]

    dispatch = {
        'Not': lambda: add_neg(args_str, formu_index, sat_time_hint, neg_prefix + 1),
        'Until': lambda: add_until(args_str, formu_index, sat_time_hint, neg_prefix),
        'Weak': lambda: add_weak(args_str, formu_index, sat_time_hint, neg_prefix),
        'And': lambda: add_and(args_str, formu_index, sat_time_hint, neg_prefix),
        'Global': lambda: add_always(args_str, formu_index, sat_time_hint, neg_prefix),
        'Or': lambda: add_or(args_str, formu_index, sat_time_hint, neg_prefix),
        'T': lambda: 1 if neg_prefix == 0 else 0,
        'F': lambda: 0 if neg_prefix == 0 else 1,
        'AP': lambda: add_AP(args_str, formu_index, sat_time_hint, neg_prefix)
    }

    if op in dispatch:
        add_result = dispatch[op]()
    else:
        print(f"Invalid sub formula '{op}' detected. Quit.")
        return 0

    if add_result:
        return formu_index
    else:
        for i in range(formulas_track_num_prev + 1, StSTL.total_formu):
            StSTL.formu_bin[i] = None
        StSTL.total_formu = formulas_track_num_prev
        StSTL.MIP_cons = StSTL.MIP_cons[:MIP_cons_num_prev]
        StSTL.total_MIP_cons = MIP_cons_num_prev
        return 0
