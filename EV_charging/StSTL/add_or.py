def add_or(formula_str, formu_index, sat_time_hint, neg_prefix):
    """
    Encode an OR formula by assigning binary variables to its subformulas
    and adding MIP constraints to the encoding constraint set.
    """
    from utils import find_comma, search_track_formula, add_formula
    global StSTL

    if len(sat_time_hint.shape) != 1:
        raise ValueError("In add_or(), sat_time_hint must be a 1D array.")

    comma_index, comma_num = find_comma(formula_str)
    given_sub_num = comma_num + 1
    given_satis_num = len(sat_time_hint)

    if given_sub_num > 1 and given_satis_num > 1 and given_sub_num != given_satis_num:
        raise ValueError("Mismatch between number of subformulas and satisfaction times.")

    sub_num = max(given_sub_num, given_satis_num)
    sub_index = [0] * sub_num
    sub_str = [''] * sub_num

    if given_sub_num == 1:
        sub_str = [formula_str] * sub_num
    else:
        sub_str[0] = formula_str[:comma_index[0]]
        for i in range(1, comma_num):
            sub_str[i] = formula_str[comma_index[i-1]+1:comma_index[i]]
        sub_str[-1] = formula_str[comma_index[-1]+1:]

    if given_satis_num == 1:
        sat_time_hint = [sat_time_hint[0]] * sub_num

    for i in range(sub_num):
        is_found, index = search_track_formula(sub_str[i], sat_time_hint[i], neg_prefix)
        if is_found and StSTL.display:
            print(f"In add_or(), formula {StSTL.formu_str[index]} with sat_time_hint {StSTL.formu_time[index]}" \
                  f", neg_prefix {StSTL.formu_neg[index]} is revoked by {sub_str[i]} with sat_time_hint {sat_time_hint[i]}")
        sub_index[i] = index

    for i in range(sub_num):
        add_result = add_formula(sub_str[i], sub_index[i], sat_time_hint[i], neg_prefix)
        if add_result == 0:
            return 0

    sum_vars = sum(StSTL.formu_bin[idx] for idx in sub_index)
    StSTL.total_MIP_cons += 2

    if neg_prefix == 0:  # logical OR
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] >= sum_vars / sub_num)
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] <= sum_vars)
    else:  # logical AND
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] >= sum_vars - sub_num + 1)
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] <= sum_vars / sub_num)

    return formu_index
