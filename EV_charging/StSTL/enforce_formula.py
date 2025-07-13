def enforce_formula(formu_index):
    """
    Assign the binary variable for a formula indexed by formu_index to 1.

    Args:
        formu_index: A list or array of formula indices.
    
    Raises:
        ValueError: If formu_index is not a 1D row vector.
    """
    global StSTL

    if not isinstance(formu_index, (list, tuple)):
        raise ValueError("Input of enforce_formula should be a row vector.")

    for k in formu_index:
        if k > 0:
            StSTL['MIP_cons'].append(StSTL['formu_bin'][k] == 1)
            StSTL['total_MIP_cons'] += 1