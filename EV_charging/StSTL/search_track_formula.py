from StSTL_class import StSTL

def search_track_formula(str_formula, sat_time_hint, neg_prefix, StSTL):
    """
    Search a formula in the tracked set and determine if it's already present.
    If it's new, track it and assign a binary variable.

    Args:
        str_formula (str): The formula string.
        sat_time_hint (list): Satisfaction time hints.
        neg_prefix (int): Number of negations before the formula.
        StSTL (dict): Global tracking structure.

    Returns:
        is_found (bool): True if already tracked.
        formu_index (int): Index in the tracked list.
    """
    is_found = False
    formu_index = 0

    if StSTL.total_formu > 0 and StSTL.repeat_check:
        indices = [i for i, f in enumerate(StSTL.formu_str[:StSTL.total_formu]) if f == str_formula]
        valid_indices = []

        for idx in indices:
            same_time = (StSTL.formu_time[idx] == sat_time_hint)
            same_neg = (StSTL.formu_neg[idx] == neg_prefix)
            if same_time and same_neg:
                valid_indices.append(idx)

        if len(valid_indices) >= 2:
            raise ValueError("Same formula assigned multiple times!")
        elif len(valid_indices) == 1:
            formu_index = valid_indices[0]
            is_found = True
    
    if not is_found:
        StSTL.total_formu += 1
        formu_index = StSTL.total_formu - 1
        StSTL.formu_str.append(str_formula)
        StSTL.formu_time.append(sat_time_hint)
        StSTL.formu_neg.append(neg_prefix)
        StSTL.formu_bin.append('binvar')  # placeholder for binary variable

        if StSTL.display:
            if StSTL.repeat_check:
                print(f"Tracked new formula '{str_formula}' with time {sat_time_hint}, neg_prefix {neg_prefix}. Index = {formu_index}")
            else:
                print(f"Tracked without checking repetition. Index = {formu_index}")

    return is_found, formu_index