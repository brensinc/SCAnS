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
    from global_vars import StSTL, SMPC, contract_checking
    from utils import StSTL_reset, SMPC_reset, add_formula, enforce_formula
    from optimization import solve_mip_problem

    verbose = 0
    disp_feas = 0

    contract_checking[0] = 1

    if encoding_style == 'equivalent':
        StSTL_reset('equivalent')
        SMPC_reset()
    else:
        StSTL_reset('sufficient')
        SMPC_reset()

    i1 = add_formula(contract['A'])
    enforce_formula(i1)

    diagnostic1 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], verbose=verbose)

    if diagnostic1['problem'] == 0:
        print(f"({contract['A']},{contract['orig_G']}) is compatible")
        if disp_feas:
            print("\ta feasible x_0 is given by:")
            print(SMPC['x0'].value())
            print("\ta feasible trajectory of u is given by:")
            for t in range(StSTL['unrolled'] + 1):
                print(SMPC['u'][t].value())
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking[0] = 0
        return 1
    elif diagnostic1['problem'] == 1 and encoding_style == 'equivalent':
        print(f"({contract['A']},{contract['orig_G']}) is incompatible")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking[0] = 0
        return 0
    elif encoding_style == 'equivalent':
        print(f"no conclusion on whether ({contract['A']},{contract['orig_G']}) is compatible or not")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tcheck_compat() optimization information: {diagnostic1['info']}")
        print(f"\tencoding style: {encoding_style}")
        contract_checking[0] = 0
        return -1

    # Now try necessary encoding if sufficient is inconclusive
    StSTL_reset('necessary')
    i2 = add_formula(contract['A'])
    enforce_formula(i2)
    diagnostic2 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], verbose=verbose)

    if diagnostic2['problem'] == 1:
        print(f"({contract['A']},{contract['orig_G']}) is incompatible")
        print(f"\tcheck_compat() solvertime: {diagnostic2['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic2['info']}")
        contract_checking[0] = 0
        return 0
    else:
        print(f"no conclusion on whether ({contract['A']},{contract['orig_G']}) is compatible or not")
        print(f"\tcheck_compat() solvertime: {diagnostic1['solvertime'] + diagnostic2['solvertime']:.3f}")
        print(f"\tcheck_compat() optimization information: {diagnostic1['info']}, {diagnostic2['info']}")
        print(f"\tencoding style: {encoding_style}")
        contract_checking[0] = 0
        return -1