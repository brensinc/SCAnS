import numpy as np

def enforce_formula(add_result):
    """
    Assign the binary variable for a formula indexed by formu_index to 1.

    Args:
        add_result: Index of last MIP_cons. add_result + 1 gives number of MIP_cons we should encode.
    
    Raises:
        ValueError: If formu_index is not a 1D row vector.
    """
    from StSTL.StSTL_class import StSTL

    # if not isinstance(formu_index, (list, tuple)):
    #     raise ValueError("Input of enforce_formula should be a row vector.")

    for k in np.arange(0, add_result + 1):
        # if k > 0:
        StSTL.MIP_cons.append(StSTL.formu_bin[k] == 1) # Indicate that each MIP_cons must be true
        StSTL.total_MIP_cons += 1