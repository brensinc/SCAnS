from EV_charging.MODEL_and_AP import AP_to_neces_MIP_EV
from EV_simulation.controller_EV import solve_vehicle_problem
from MODEL_and_AP.AP_to_suffi_MIP_EV import ap_to_suffi_mip_ev
from MODEL_and_AP.AP_to_neces_MIP_EV import ap_to_neces_mip_ev
from EV_simulation.topology_synthesis import charger_topology

# Enforce system level contract constraints and return whether a solution is feasible that satisfies system requirements.
def solve_ev_feasibility(q1_idx, q2_idx, contract_checking):
        soc, budget, move, charge, idle, pos_bin = solve_vehicle_problem(q1_idx, q2_idx, contract_checking) # Fix this so that we can input mip_constraints into optimization problem
        all_vars = [soc, budget, pos_bin, move, charge, idle]
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
    from StSTL import add_formula, enforce_formula
    from StSTL.StSTL_class import StSTL

    verbose = 0
    disp_feas = 0

    contract_checking[0] = 1

    # if encoding_style == 'equivalent':
    #     StSTL.StSTL_reset('equivalent')
    #     SMPC_reset()
    # elif encoding_style == 'sufficient':
    #     StSTL.StSTL_reset('sufficient')
    #     SMPC_reset()
    # else:
    #     raise Exception(f"encoding style {encoding_style} not valid")

    # These commands allows for more generalizable and abstract code implementations.
    # Look to implement them in the future. Could be used to replace the following lines.
    # i1 = add_formula(contract['A'])
    # enforce_formula(i1)

    # Add MIP Constraints using AP_to_{suffi/neces}_MIP_EV.py. The constraints will be assigned to StSTL.MIP_cons. 
    # They will then be enforced when we pass contract_checking = 1 into controller optimizaiton
    if encoding_style == 'equivalent':
        StSTL.StSTL_reset('equivalent')
        ap_to_neces_mip_ev() # Add inputs
    else:
        StSTL.StSTL_reset('sufficient')
        ap_to_suffi_mip_ev()
    
    ap_to_suffi_mip_ev() # Encode sufficient conditions for compatibility

    # Try sufficient condition for compatibility.
    diagnostic1 = solve_ev_feasibility(charger_topology.q1_idx, charger_topology.q2_idx, contract_checking) # Where are q1_idx and q2_idx derived from?

    # diagnostic1 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], verbose=verbose)
    # diagnostic1 = 

    if diagnostic1['problem'] == 0: # Feasible solution found
        print(f"({contract['A']},{contract['orig_G']}) is compatible")
        # if disp_feas:
            # print("\ta feasible x_0 is given by:")
            # print(SMPC['x0'].value())
            # print("\ta feasible trajectory of u is given by:")
            # for t in range(StSTL['unrolled'] + 1):
                # print(SMPC['u'][t].value())
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking[0] = 0
        return 1
    # elif diagnostic1['problem'] == 1 and encoding_style == 'equivalent': # No feasible solution found
    #     print(f"({contract['A']},{contract['orig_G']}) is incompatible")
    #     print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
    #     print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        # contract_checking[0] = 0
        # return 0
    elif encoding_style == 'equivalent': # No conclusion drawn
        print(f"no conclusion on whether ({contract['A']},{contract['orig_G']}) is compatible or not")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tcheck_compat() optimization information: {diagnostic1['info']}")
        print(f"\tencoding style: {encoding_style}")
        # contract_checking[0] = 0
        # return -1

    # # Now try necessary encoding if sufficient is inconclusive
    # StSTL.StSTL_reset('necessary') # Where does necessary come in? Do we specify necessary when we 
    # i2 = add_formula(contract['A'])
    # enforce_formula(i2)
    

    StSTL.StSTL_reset('necessary')
    ap_to_neces_mip_ev() # Encode necessary conditions for compatibility
    diagnostic2 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], verbose=verbose)

    if diagnostic2['problem'] == 1: # Feasible solution found
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