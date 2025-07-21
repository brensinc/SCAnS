from StSTL.find_comma import find_comma

def add_neg(str_formula, formu_index, sat_time_hint, neg_prefix):
    """
    Encode a NOT formula by assigning binary variables to its sub-formulas
    and adding MIP constraints into the encoding constraint set.
    """
    global StSTL

    comma_index = find_comma(str_formula)
    comma_num = len(comma_index)

    if comma_num == 0:
        sub_formula = str_formula
    elif comma_num == 1:
        sub_formula = str_formula[:comma_index[0]].strip()
        time_point_1 = int(float(str_formula[comma_index[0] + 1:].strip()))
        if sat_time_hint != -1 and sat_time_hint != time_point_1:
            raise ValueError("Inconsistency between formula string and sat_time_hint")
        elif sat_time_hint == -1:
            sat_time_hint = time_point_1
    else:
        raise ValueError("Maximal parameter number is 2 in add_negation!")

    if neg_prefix == 2:
        neg_prefix = 0
    elif neg_prefix > 2:
        raise ValueError("neg_prefix should be less than 3")

    is_found, sub_formula_index = search_track_formula(sub_formula, sat_time_hint, neg_prefix)

    if is_found and StSTL.display == 1:
        print(f"formula {StSTL.formu_str[sub_formula_index]} with sat_time_hint {StSTL.formu_time[sub_formula_index]}, "
              f"neg_prefix {StSTL.formu_neg[sub_formula_index]} already tracked is revoked by {sub_formula} "
              f"with sat_time_hint {sat_time_hint}")

    add_result = add_formula(sub_formula, sub_formula_index, sat_time_hint, neg_prefix)

    if add_result:
        StSTL.total_MIP_cons += 1
        StSTL.MIP_cons.append(StSTL.formu_bin[formu_index] == StSTL.formu_bin[sub_formula_index])
        add_result = formu_index

    return add_result
