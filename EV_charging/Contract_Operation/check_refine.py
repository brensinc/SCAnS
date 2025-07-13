def check_refine(contract1, contract2, encoding_style):
    """
    Check whether contract2 refines contract1.

    Parameters:
        contract1: dict with 'A', 'G', 'orig_G'
        contract2: dict with 'A', 'G', 'orig_G'
        encoding_style: str, either 'equivalent' or 'suffi_and_neces'

    Returns:
        int: 1 (refines), 0 (does not refine), -1 (inconclusive)
    """
    global StSTL, SMPC, contract_checking

    def try_optimization(formula_str):
        idx = add_formula(formula_str)
        enforce_formula(idx)
        return solve_mip_problem(SMPC.perf_func)

    contract_checking = 1

    # Step 1.1: check if for all u, A1 -> A2
    reset_style = encoding_style if encoding_style == 'equivalent' else 'necessary'
    StSTL_reset(reset_style)
    SMPC_reset()
    diag1 = try_optimization(f"And({contract1['A']},Not({contract2['A']}))")
    
    if diag1['status'] == 'infeasible':
        any_u_A1_imply_A2 = True
    elif diag1['status'] == 'feasible' and encoding_style == 'equivalent':
        print(f"({contract2['A']},{contract2['orig_G']}) does not refine ({contract1['A']},{contract1['orig_G']})")
        contract_checking = 0
        return 0
    else:
        any_u_A1_imply_A2 = False

    # Step 1.2: check if for all u, G2 -> G1
    StSTL_reset(reset_style)
    diag2 = try_optimization(f"Not(Or(Not({contract2['G']}),{contract1['G']}))")

    if diag2['status'] == 'infeasible':
        any_u_G2_imply_G1 = True
    elif diag2['status'] == 'feasible' and encoding_style == 'equivalent':
        print(f"({contract2['A']},{contract2['orig_G']}) does not refine ({contract1['A']},{contract1['orig_G']})")
        contract_checking = 0
        return 0
    else:
        any_u_G2_imply_G1 = False

    if any_u_A1_imply_A2 and any_u_G2_imply_G1:
        print(f"({contract2['A']},{contract2['orig_G']}) refines ({contract1['A']},{contract1['orig_G']})")
        contract_checking = 0
        return 1

    # Step 2.1: check if for some u, Not(A1 -> A2)
    StSTL_reset('sufficient' if encoding_style != 'equivalent' else 'equivalent')
    diag3 = try_optimization(f"Not(Or(Not({contract1['A']}),{contract2['A']}))")

    if diag3['status'] == 'feasible':
        print(f"({contract2['A']},{contract2['orig_G']}) does not refine ({contract1['A']},{contract1['orig_G']})")
        contract_checking = 0
        return 0

    # Step 2.2: check if for some u, Not(G2 -> G1)
    StSTL_reset('sufficient' if encoding_style != 'equivalent' else 'equivalent')
    diag4 = try_optimization(f"Not(Or(Not({contract2['G']}),{contract1['G']}))")

    if diag4['status'] == 'feasible':
        print(f"({contract2['A']},{contract2['orig_G']}) does not refine ({contract1['A']},{contract1['orig_G']})")
        contract_checking = 0
        return 0

    print(f"no conclusion on whether ({contract2['A']},{contract2['orig_G']}) refines ({contract1['A']},{contract1['orig_G']})")
    contract_checking = 0
    return -1