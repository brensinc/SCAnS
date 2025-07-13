# ststl_config.py

def StSTL_config():
    """
    Configure the encoding of StSTL (Signal Temporal Logic) formulas.
    This function initializes a global dictionary to hold encoding preferences,
    tracked formulas, and constraints.
    """
    global StSTL
    StSTL = {}

    # Encoding style: 'equivalent', 'sufficient', or 'necessary'
    StSTL["style"] = "equivalent"

    # Display debug info, check for duplicates, constants
    StSTL["display"] = 0
    StSTL["repeat_check"] = 1
    StSTL["large_num"] = 1e5
    StSTL["small_num"] = 0.001

    # Quadruple (formu_str, formu_time, formu_neg, formu_bin)
    StSTL["formu_str"] = []
    StSTL["formu_time"] = []
    StSTL["formu_neg"] = []
    StSTL["formu_bin"] = []

    # Tracking counters and constraints
    StSTL["total_formu"] = 0
    StSTL["MIP_cons"] = []
    StSTL["total_MIP_cons"] = 0
    StSTL["unrolled"] = -1

    return StSTL
