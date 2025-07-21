import numpy as np
from EV_simulation.controller_EV import controller
from EV_simulation.topology_synthesis import cno_topology

# Enforce system level contract constraints and return whether a solution is feasible that satisfies system requirements.
def solve_ev_feasibility(contract_checking, veh_controller):
        veh_controller = veh_controller.solve_vehicle_problem(contract_checking)
        all_vars = [veh_controller.soc, veh_controller.budget, veh_controller.pos_bin, veh_controller.move, veh_controller.charge, veh_controller.idle]
        feasible = all(x is not None for x in all_vars)
        return {
            'problem': 0 if feasible else 1,
            'solvertime': 0.0,
            'info': 'EV deterministic MILP feasibility'
            }

def check_compat(contract, encoding_style):
    """
    Check the compatibility of a given contract.

    Parameters:
    - contract: dict with keys 'A' and 'orig_G'
    - encoding_style: 'suffi_and_neces' or 'equivalent'

    Returns:
    - 1 if contract is compatible
    - 0 if contract is incompatible
    - -1 if no conclusion can be drawn
    """
    from MODEL_and_AP.global_state import contract_checking
    from StSTL.add_formula import add_formula
    from StSTL.enforce_formula import enforce_formula
    from StSTL.StSTL_class import StSTL

    verbose = 0
    disp_feas = 0

    # contract_checking[0] = 1

    # Initialize charging topology. Or should I just do this in topology_synthesis.py?
    charger_topology = cno_topology().solve_cno_problem()

    # Initialize vehicle controller
    veh_controller = controller(charger_topology)

    # Step 1: Try sufficient encoding
    if encoding_style == 'equivalent':
        StSTL.StSTL_reset('equivalent')
        # SMPC_reset() # Do we have any control parameters that we need to reset?
    else:
        StSTL.StSTL_reset('sufficient')
        # SMPC_reset()

    StSTL.display = 1

    i1 = add_formula(contract['A'], veh_controller.x_vars, veh_controller.u_vars)
    # i1 = np.atleast_1d(i1) # Make sure the output is a vector
    enforce_formula(i1)

    # Try sufficient condition for compatibility.
    diagnostic1 = solve_ev_feasibility(contract_checking = 1, veh_controller = veh_controller)
    # diagnostic1 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], verbose=verbose)

    if diagnostic1["problem"] == 0: # Feasible solution found
        print(f"({contract['A']},{contract['orig_G']}) is compatible")
        if disp_feas:
            print("\ta feasible x_0 is given by:")
            print("\ta feasible trajectory of u is given by:")
            print(veh_controller.move, veh_controller.charge, veh_controller.idle)
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking[0] = 0
        return 1
    elif diagnostic1["problem"] == 1 and encoding_style == 'equivalent': # No feasible solution found
        print(f"({contract['A']},{contract['orig_G']}) is incompatible")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking[0] = 0
        return 0
    elif encoding_style == 'equivalent': # No conclusion drawn
        print(f"no conclusion on whether ({contract['A']},{contract['orig_G']}) is compatible or not")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tcheck_compat() optimization information: {diagnostic1['info']}")
        print(f"\tencoding style: {encoding_style}")
        contract_checking[0] = 0
        return -1

    # Now try necessary encoding if sufficient is inconclusive
    StSTL.StSTL_reset('necessary') # Where does necessary come in? Do we specify necessary when we 
    i2 = add_formula(contract['A'], veh_controller.x_vars, veh_controller.u_vars)
    enforce_formula(i2)

    diagnostic2 = solve_ev_feasibility(contract_checking)

    # StSTL.StSTL_reset('necessary')
    # ap_to_neces_mip_ev() # Encode necessary conditions for compatibility
    # diagnostic2 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], verbose=verbose)

    if diagnostic2 == 1: # Feasible solution found
        print(f"({contract['A']},{contract['orig_G']}) is incompatible")
        print(f"\tcheck_compat() solvertime: {diagnostic2['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic2['info']}")
        contract_checking[0] = 0
        return 0
    else: # No feasible solution found
        print(f"no conclusion on whether ({contract['A']},{contract['orig_G']}) is compatible or not")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime'] + diagnostic2['solvertime']:.3f}")
        print(f"\tcheck_compat() optimization information: {diagnostic1['info']}, {diagnostic2['info']}")
        print(f"\tencoding style: {encoding_style}")
        contract_checking[0] = 0
        return -1

# def check_compat(contract, encoding_style):
#     """
#     Check the compatibility of a given contract.

#     Parameters:
#     - contract: dict with keys 'A' and 'orig_G'
#     - encoding_style: 'suffi_and_neces' or 'equivalent'

#     Returns:
#     - 1 if contract is compatible
#     - 0 if contract is incompatible
#     - -1 if no conclusion can be drawn
#     """
#     from MODEL_and_AP.global_state import contract_checking
#     from StSTL import add_formula, enforce_formula
#     from StSTL.StSTL_class import StSTL

#     verbose = 0
#     disp_feas = 0

#     contract_checking[0] = 1

#     # Step 1: Try sufficient encoding
#     StSTL.StSTL_reset('sufficient') # Removes all current constraints and sets style to sufficient
#     # ap_to_suffi_mip_ev(...)  # add constraints

#     # Add atomic propositions to the set of constraints. This will parse through the contract specifications, 
#     #then calls AP_to_{neces/suffi}_MIP_EV.py which add constraints to StSTL.MIP_cons. 
#     add_AP(str_formula = contract["A"], formu_index, sat_time_hint, neg_prefix, x_vars, u_vars)
#     diagnostic1 = solve_ev_feasibility(charger_topology.q1_idx, charger_topology.q2_idx, contract_checking)

#     if diagnostic1 == 0:
#         return 1  # Contract is compatible
#     else:
#         # Step 2: Try necessary encoding
#         StSTL.StSTL_reset('necessary') # Removes all current constraints and sets style to necessary
#         # ap_to_neces_mip_ev(...)  # add constraints
#         add_AP(str_formula = contract["A"], formu_index, sat_time_hint, neg_prefix, x_vars, u_vars)
#         diagnostic2 = solve_ev_feasibility(charger_topology.q1_idx, charger_topology.q2_idx, contract_checking)
        
#         if diagnostic2.problem == 1:
#             return 0  # Contract is incompatible
#         else:
#             return -1  # Inconclusive
