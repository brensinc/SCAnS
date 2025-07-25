from StSTL.StSTL_class import StSTL
from MODEL_and_AP.AP_to_neces_MIP_EV import ap_to_neces_mip_ev
from MODEL_and_AP.AP_to_suffi_MIP_EV import ap_to_suffi_mip_ev
# from MODEL_and_AP.AP_to_equiv_MIP_EV import ap_to_equiv_mip_ev  # If implemented

def add_AP(str_formula, formu_index, sat_time_hint, neg_prefix, x_vars, u_vars):
    """
    Translates an atomic proposition (AP) string into MIP constraints by invoking the
    appropriate function based on the encoding style.
    
    Args:
        str_formula: e.g. '3,2' or '3'
        formu_index: index of the formula in StSTL data structure
        sat_time_hint: time index (integer)
        neg_prefix: number of negations before the AP string
        x_vars: list of cp.Variable vectors (state variables per time)
        u_vars: list of cp.Variable vectors (input variables per time)
        
    Returns:
        add_result: formu_index if successful, 0 otherwise
    """
    if not isinstance(sat_time_hint, int):
        raise ValueError("sat_time_hint must be an integer.")

    parts = str_formula.split(',')
    if len(parts) > 2:
        print(f"Too many commas in atomic string {str_formula}! Omit this AP.")
        return 0

    try:
        AP_tag = int(parts[0])
    except ValueError:
        raise ValueError(f"Invalid AP index in {str_formula}")

    if len(parts) == 2:
        try:
            t = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid time index in AP({str_formula})")
        if t != sat_time_hint and sat_time_hint != -1:
            raise ValueError("Inconsistency between time parameter and sat_time_hint!")
    else:
        if sat_time_hint == -1:
            raise ValueError("No satisfaction time provided.")
        t = sat_time_hint

    # Dispatch to appropriate AP translation function
    style = StSTL.style.lower()

    

    if style == 'sufficient':
        return ap_to_suffi_mip_ev(AP_tag, t, formu_index, neg_prefix, x_vars, u_vars)
    elif style in ['necessary', 'equivalent']:
        return ap_to_neces_mip_ev(AP_tag, t, formu_index, neg_prefix, x_vars, u_vars)
    else:
        raise ValueError(f"Unknown encoding style: {style}")



# def add_AP(str_formula, formu_index, sat_time_hint, neg_prefix):
#     """
#     Translates an atomic proposition (AP) string into MIP constraints by invoking the
#     appropriate function based on the encoding style.
    
#     Args:
#         str_formula: e.g. '3,2' or '3'
#         formu_index: index of the formula in StSTL data structure
#         sat_time_hint: time index (integer)
#         neg_prefix: number of negations before the AP string
#     Returns:
#         add_result: formu_index if successful, 0 otherwise
#     """
#     global_vars = globals()
#     StSTL = global_vars.get('StSTL', {})
#     MODEL = global_vars.get('MODEL', {})

#     if not isinstance(sat_time_hint, int):
#         raise ValueError("sat_time_hint must be an integer.")

#     parts = str_formula.split(',')
#     comma_num = len(parts) - 1

#     if comma_num > 1:
#         print('Too many commas in atomic string! Omit this AP.')
#         return 0

#     if comma_num == 1:
#         AP_tag, t_str = parts
#         try:
#             t = int(float(t_str))
#         except ValueError:
#             print("Illegal time index! Omit this AP.")
#             return 0
#         if t < 0:
#             print("Illegal time index! Omit this AP.")
#             return 0
#         if t != sat_time_hint and sat_time_hint != -1:
#             raise ValueError("Inconsistency between the time parameter and sat_time_hint!")
#     else:  # comma_num == 0
#         if sat_time_hint == -1:
#             raise ValueError("No satisfaction time is specified for AP!")
#         t = sat_time_hint
#         AP_tag = str_formula

#     style = StSTL.get('style', '')
#     model_type = MODEL.get('type', '')

#     func_name = None
#     if style == 'sufficient':
#         func_name = f"AP_to_suffi_MIP_{model_type}"
#     elif style == 'necessary':
#         func_name = f"AP_to_neces_MIP_{model_type}"
#     elif style == 'equivalent':
#         func_name = f"AP_to_equiv_MIP_{model_type}"
#     else:
#         raise ValueError("Unrecognized encoding style.")

#     if func_name not in global_vars:
#         raise NameError(f"Function {func_name} is not defined.")

#     add_func = global_vars[func_name]
#     add_result = add_func(AP_tag, t, formu_index, neg_prefix)

#     return add_result