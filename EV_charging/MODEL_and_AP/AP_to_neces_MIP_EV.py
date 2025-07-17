# ap_to_neces_mip_ev.py
# Converts APs with temporal logic into deterministic MIP constraints for EVs

import numpy as np
import cvxpy as cp
from scipy.stats import norm
from StSTL.StSTL_class import StSTL
from AP_EV import AP



# Assume global StSTL and AP structures

def ap_to_neces_mip_ev(AP_tag, k, formu_index, neg_prefix, x_vars, u_vars):
    """
    Convert atomic proposition AP[AP_tag] at time step k into MIP constraints.

    Parameters:
    - AP_tag: int, index into AP list
    - k: int, time index
    - formu_index: int, index for logic tracking in StSTL
    - neg_prefix: bool, whether this is negated
    - x_vars: list of cp.Variable vectors [SOC[k], budget[k], pos[k], q1, q2]
    - u_vars: list of cp.Variable vectors [move[k], charge[k], idle[k]]
    - StSTL: dict to hold logic constraints and metadata
    - AP: list of atomic proposition dictionaries

    Returns:
    - index of the formula in formu_bin
    """

    M = StSTL.large_num
    epsl = StSTL.small_num

    ap = AP[AP_tag]

    # Negation logic
    if neg_prefix:
        if ap['p'] == 0:
            StSTL.formu_bin[formu_index] = 0
            return formu_index
        elif ap['p'] == 1:
            a0 = -np.array(ap['a'])
            b0 = -np.array(ap.get('b', np.zeros(3)))
            c0 = -ap['c'] + epsl
            p0 = 1
        else:
            a0 = -np.array(ap['a'])
            b0 = -np.array(ap.get('b', np.zeros(3)))
            c0 = -ap['c'] + epsl
            p0 = 1 - ap['p'] + epsl
    else:
        a0 = np.array(ap['a'])
        b0 = np.array(ap.get('b', np.zeros(3)))
        c0 = ap['c']
        p0 = ap['p']

    if p0 <= 0:
        StSTL.formu_bin[formu_index] = 1
        return formu_index

    if p0 == 1:
        F_inv = 0
    elif 0 < p0 < 1:
        F_inv = norm.ppf(p0)
    else:
        raise ValueError("Invalid p value in AP")

    # Assemble linear expression
    x_vec = x_vars[k] if isinstance(x_vars, list) else x_vars
    u_vec = u_vars[k] if isinstance(u_vars, list) else u_vars

    lam1 = a0 @ x_vec + b0 @ u_vec + c0

    # For deterministic constraints (p=1), lam2 = 0
    lam2 = 0  # Can be replaced by model uncertainty if added later

    # Add MILP constraints for indicator variable formu_bin
    z = cp.Variable(boolean=True)
    StSTL.formu_bin[formu_index] = z
    StSTL.MIP_cons += [lam1 + F_inv * lam2 + (z - 1) * M <= 0]
    StSTL.MIP_cons += [lam1 + F_inv * lam2 + z * M >= epsl]

    StSTL.total_MIP_cons += 2

    return formu_index