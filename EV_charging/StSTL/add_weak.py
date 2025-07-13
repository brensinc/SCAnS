def add_weak(string, formu_index, sat_time_hint, neg_prefix):
    """
    Encode a WEAK UNTIL formula by assigning binary variables to its sub-formulas
    and adding MIP constraints into the encoding constraint set.
    
    Args:
        string (str): the formula string, must have the form 'f1,f2,t_start,t_end'.
        formu_index (int): the index of this formula stored in the StSTL encoding structure.
        sat_time_hint (int): starting time after which the formula is satisfied.
        neg_prefix (int): number of negations before the formula.

    Returns:
        int: formu_index if successful, 0 otherwise.
    """
    from .utils import find_comma, search_track_formula, add_formula
    from .globals import StSTL

    comma_index, comma_num = find_comma(string)
    if comma_num == 3:
        f1 = string[:comma_index[0]]
        t_start = int(float(string[comma_index[1] + 1:comma_index[2]]))
        t_end = int(float(string[comma_index[2] + 1:]))
        if t_start < 0 or t_end < 0 or t_start > t_end:
            raise ValueError("In add_weak(), invalid t_start or t_end!")
    else:
        raise ValueError("Parameter number should be 3 in add_weak()!")

    if not isinstance(sat_time_hint, (int, float)):
        raise TypeError("Invalid sat_time_hint!")

    sub_str = [f"Until({string})", f"Global({f1},{t_start},{t_end})"]
    sub_index = [0, 0]

    for i in range(2):
        is_found, index = search_track_formula(sub_str[i], sat_time_hint, neg_prefix)
        if is_found and StSTL.display == 1:
            print(f"In add_weak(), formula {StSTL.formu_str[index]} with sat_time_hint "
                  f"{StSTL.formu_time[index]}, neg_prefix {StSTL.formu_neg[index]} that has already tracked "
                  f"is revoked by {sub_str[i]} with sat_time_hint {sat_time_hint}")
        sub_index[i] = index

    for i in range(2):
        add_result = add_formula(sub_str[i], sub_index[i], sat_time_hint, neg_prefix)
        if add_result == 0:
            return 0

    sum_vars = sum(StSTL.formu_bin[i] for i in sub_index)
    if neg_prefix == 0:
        StSTL.MIP_cons.append((1/2) * sum_vars <= StSTL.formu_bin[formu_index])
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] <= sum_vars)
    else:
        StSTL.MIP_cons.append(sum_vars - 1 <= StSTL.formu_bin[formu_index])
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] <= (1/2) * sum_vars)

    StSTL.total_MIP_cons += 2
    return formu_index
