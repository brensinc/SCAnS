# from MODEL_and_AP.MODEL_EV import MODEL

def make_contract(A, G):
    """
    Construct a contract using the assumption and guarantee.

    Parameters:
        A (str): Assumption formula string in StSTL.
        G (str): Guarantee formula string in StSTL.

    Returns:
        dict: Contract with keys 'sys', 'A', 'orig_G', and 'G'
    """
    global MODEL

    return {
        # 'sys': MODEL.system_type,  # record the system type
        'A': A,
        'orig_G': G,
        'G': f"Or(Not({A}),{G})"  # logical implication: A -> G
    }