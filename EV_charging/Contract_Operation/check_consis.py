def check_consis(contract, encoding_style):
    """
    Check the consistency of a given contract: is the guarantee feasible?

    Parameters:
    - contract: object with attributes A, G, orig_G
    - encoding_style: str, either 'equivalent' or 'suffi_and_neces'

    Returns:
    - out: int
        1 if consistent
        0 if inconsistent
       -1 if no conclusion
    """
    from global_state import StSTL, SMPC, contract_checking
    from helpers import StSTL_reset, SMPC_reset, add_formula, enforce_formula, solve_mip_problem

    if encoding_style == 'equivalent':
        StSTL_reset(encoding_style)
        SMPC_reset()
    else:
        StSTL_reset('sufficient')
        SMPC_reset()

    contract_checking['flag'] = 1
    verbose = 0
    disp_feas = 0

    i1 = add_formula(contract.G)
    enforce_formula(i1)

    diagnostic1 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], solver='gurobi', verbose=verbose)

    if diagnostic1['problem'] == 0:
        print(f"({contract.A}, {contract.orig_G}) is consistent")
        if disp_feas:
            print("\tA feasible x_0 is given by:", SMPC['x0'].value)
            print("\tA feasible trajectory of u is:")
            for t in range(StSTL['unrolled'] + 1):
                print(SMPC['u'][t].value)
        print(f"\tcheck_consis() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking['flag'] = 0
        return 1

    if diagnostic1['problem'] == 1 and encoding_style == 'equivalent':
        print(f"({contract.A}, {contract.orig_G}) is inconsistent")
        print(f"\tcheck_consis() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic1['info']}")
        contract_checking['flag'] = 0
        return 0

    if encoding_style == 'equivalent':
        print(f"no conclusion on whether ({contract.A}, {contract.orig_G}) is consistent")
        print(f"\tcheck_consis() solvertime: {diagnostic1['solvertime']:.3f}")
        print(f"\tcheck_consis() optimization information: {diagnostic1['info']}")
        print(f"\tencoding style: {encoding_style}")
        contract_checking['flag'] = 0
        return -1

    # Try necessary encoding
    StSTL_reset('necessary')
    i2 = add_formula(contract.G)
    enforce_formula(i2)

    diagnostic2 = solve_mip_problem(StSTL['MIP_cons'], SMPC['perf_func'], solver='gurobi', verbose=verbose)

    if diagnostic2['problem'] == 1:
        print(f"({contract.A}, {contract.orig_G}) is inconsistent")
        print(f"\tcheck_consis() solvertime: {diagnostic2['solvertime']:.3f}")
        print(f"\tencoding style: {encoding_style}, {diagnostic2['info']}")
        contract_checking['flag'] = 0
        return 0
    else:
        print(f"no conclusion on whether ({contract.A}, {contract.orig_G}) is consistent")
        total_time = diagnostic1['solvertime'] + diagnostic2['solvertime']
        print(f"\tcheck_consis() solvertime: {total_time:.3f}")
        print(f"\tcheck_consis() optimization information: {diagnostic1['info']}, {diagnostic2['info']}")
        print(f"\tencoding style: {encoding_style}")
        contract_checking['flag'] = 0
        return -1
