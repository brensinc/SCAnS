def add_until(formula_str, formu_index, sat_time_hint, neg_prefix):
    """
    Encode an UNTIL formula by assigning binary variables to its sub-formulas
    and adding MIP constraints into the encoding constraint set.
    
    Args:
        formula_str (str): Formula string of the form 'f1,f2,t_start,t_end'
        formu_index (int): Index in StSTL formula structure
        sat_time_hint (int): Starting time offset
        neg_prefix (int): Number of negations preceding formula

    Returns:
        int: formu_index if successful, 0 otherwise
    """
    global StSTL

    comma_index = [i for i, c in enumerate(formula_str) if c == ',']
    if len(comma_index) != 3:
        raise ValueError("Parameter number should be 3 in add_until()!")

    f1 = formula_str[:comma_index[0]]
    f2 = formula_str[comma_index[0]+1:comma_index[1]]
    t_start = int(formula_str[comma_index[1]+1:comma_index[2]])
    t_end = int(formula_str[comma_index[2]+1:])

    if t_start < 0 or t_end < 0 or t_start > t_end:
        raise ValueError("In add_until(), invalid t_start or t_end!")

    if not isinstance(sat_time_hint, int):
        raise ValueError("Invalid sat_time_hint!")

    T0 = 0 if sat_time_hint == -1 else sat_time_hint

    sub_num = t_end - t_start + 1
    sub_index = [0] * sub_num
    sub_t_vector = [None] * sub_num
    sub_str = ["" for _ in range(sub_num)]

    # First subformula (just f2)
    sub_str[0] = f2
    sub_t_vector[0] = t_start + T0
    is_found, index_1 = search_track_formula(sub_str[0], sub_t_vector[0], neg_prefix)
    if is_found and StSTL["display"]:
        print(f"In add_until(), formula {StSTL['formu_str'][index_1]} with sat_time_hint {StSTL['formu_time'][index_1]}" +
              f", neg_prefix {StSTL['formu_neg'][index_1]} is revoked by {sub_str[0]} at {sub_t_vector[0]}")
    sub_index[0] = index_1

    # Construct rest of subformulas
    for i in range(1, sub_num):
        conj = 'And' if neg_prefix == 0 else 'Or'
        sub_str[i] = f"{conj}({f2}" + ",".join([f1] * i) + ")"
        sub_t_vector[i] = list(range(t_start + T0 + i, t_start + T0 - 1, -1))

        is_found, index_i = search_track_formula(sub_str[i], sub_t_vector[i], neg_prefix)
        if is_found and StSTL["display"]:
            print(f"In add_until(), formula {StSTL['formu_str'][index_i]} with sat_time_hint {StSTL['formu_time'][index_i]}" +
                  f", neg_prefix {StSTL['formu_neg'][index_i]} is revoked by {sub_str[i]} at {sub_t_vector[i]}")
        sub_index[i] = index_i

    # Add subformulas
    for i in range(sub_num):
        result = add_formula(sub_str[i], sub_index[i], sub_t_vector[i], neg_prefix)
        if result == 0:
            return 0

    # Add final binary logic constraints
    sum_vars = sum(StSTL["formu_bin"][sub_index[i]] for i in range(sub_num))
    if neg_prefix == 0:
        StSTL["MIP_cons"].append(1 / sub_num * sum_vars <= StSTL["formu_bin"][formu_index])
        StSTL["MIP_cons"].append(StSTL["formu_bin"][formu_index] <= sum_vars)
    else:
        StSTL["MIP_cons"].append(sum_vars - sub_num + 1 <= StSTL["formu_bin"][formu_index])
        StSTL["MIP_cons"].append(StSTL["formu_bin"][formu_index] <= 1 / sub_num * sum_vars)

    StSTL["total_MIP_cons"] += 2
    return formu_index
