# ststl_reset.py

def StSTL_reset(encoding_style):
    """
    Reset the StSTL global configuration:
    - Specify encoding style.
    - Discard previously recorded formulas and constraints.

    Args:
        encoding_style (str): One of 'equivalent', 'sufficient', or 'necessary'.
    """
    global StSTL

    StSTL["style"] = encoding_style
    StSTL["total_formu"] = 0
    StSTL["MIP_cons"] = []
    StSTL["total_MIP_cons"] = 0
    StSTL["unrolled"] = -1
