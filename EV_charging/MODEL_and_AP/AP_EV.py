# AP_EV.py
# Define atomic propositions (APs) for a Gaussian Linear system model
# Pr{a_i'x_k + b_i'u_k + c_i <= 0} >= p_i for i = 1,...,N

import numpy as np

def define_AP(MODEL):
    if "nx" not in MODEL or "nu" not in MODEL:
        raise ValueError("MODEL must contain 'nx' and 'nu' fields.")

    AP = {
        "a": [],
        "b": [],
        "c": [],
        "p": [],
        "N": 5
    }

    nx = MODEL["nx"]
    nu = MODEL["nu"]

    # 1st constraint: -x[0] + 1 <= 0
    a1 = np.zeros((nx, 1))
    a1[0, 0] = -1
    b1 = np.zeros((nu, 1))
    c1 = 1
    p1 = 1

    # 2nd constraint: x[0] - 2 <= 0
    a2 = np.zeros((nx, 1))
    a2[0, 0] = 1
    b2 = np.zeros((nu, 1))
    c2 = -2
    p2 = 1

    # 3rd constraint: P{x[0] - 1 <= 0} >= 0.7
    a3 = np.zeros((nx, 1))
    a3[0, 0] = 1
    b3 = np.zeros((nu, 1))
    c3 = -1
    p3 = 0.7

    # 4th constraint: x[0] - 3 <= 0
    a4 = np.zeros((nx, 1))
    a4[0, 0] = 1
    b4 = np.zeros((nu, 1))
    c4 = -3
    p4 = 1

    # 5th constraint: P{x[0] - 2 <= 0} >= 0.3
    a5 = np.zeros((nx, 1))
    a5[0, 0] = 1
    b5 = np.zeros((nu, 1))
    c5 = -2
    p5 = 0.3

    AP["a"] = [a1, a2, a3, a4, a5]
    AP["b"] = [b1, b2, b3, b4, b5]
    AP["c"] = [c1, c2, c3, c4, c5]
    AP["p"] = [p1, p2, p3, p4, p5]

    return AP


# AP_EV.py
# Import MODEL_EV defined elsewhere

"""
Atomic propositions (APs) of EPS have the form

Pr{a_i'*x + b_i'*u + c_i <= 0} >= p_i, i = 1,...,N

where x and u are described in MODEL_EPS.m
Inspired by Jiwei Li
"""

# # Define global AP dictionary
# AP = {
#     'a': [],  # coefficients on state x
#     'b': [],  # coefficients on input u
#     'c': [],  # constant offset
#     'p': []   # probability thresholds
# }

# # Constraint 1: Battery level >= 20% of max
# AP['a'].append([-1, 0, 0])  # -b <= -0.2*bat_max  =>  b >= 0.2*bat_max
# AP['b'].append([0])         # no input dependency
# AP['c'].append(-0.2 * model.bat_max)
# AP['p'].append(1.0)

# # Constraint 2: Battery level <= max
# AP['a'].append([1, 0, 0])
# AP['b'].append([0])
# AP['c'].append(model.bat_max)
# AP['p'].append(1.0)

# # Constraint 3: Speed <= speed limit
# AP['a'].append([0, 1, 0])
# AP['b'].append([0])
# AP['c'].append(model.v_max)
# AP['p'].append(1.0)

# # Constraint 4: Speed >= 0
# AP['a'].append([0, -1, 0])
# AP['b'].append([0])
# AP['c'].append(0)
# AP['p'].append(1.0)

# # Constraint 5: Reach goal by time T (example at final timestep)
# # Assume p(t_final) >= destination_position
# AP['a'].append([-1, 0, 0])  # -p <= -destination_position
# AP['b'].append([0])
# AP['c'].append(-model.destination_position)
# AP['p'].append(1.0)

# # Constraint 6 (optional): control acceleration is within bounds
# # a <= a_max
# AP['a'].append([0, 0, 0])
# AP['b'].append([1])
# AP['c'].append(model.a_max)
# AP['p'].append(1.0)

# # -a <= -a_min  => a >= a_min
# AP['a'].append([0, 0, 0])
# AP['b'].append([-1])
# AP['c'].append(-model.a_min)
# AP['p'].append(1.0)
