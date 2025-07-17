""" Code needs to be fixed. Having an error in the logic that is causing the vehicle to move forward when it charges."""

import cvxpy as cp
import numpy as np
import pandas as pd
from IPython.display import display
from MODEL_and_AP.global_state import contract_checking

from StSTL.StSTL_class import StSTL


def solve_vehicle_problem(q1_idx, q2_idx, contract_checking = 0):
    T = 6  # Total time steps
    n_nodes = 5
    M = 1000  # Big-M constant

    # State variables
    soc = cp.Variable(T + 1)
    budget = cp.Variable(T + 1)

    # Binary action variables
    move = cp.Variable(T, boolean=True)
    charge = cp.Variable(T, boolean=True)
    idle = cp.Variable(T, boolean=True)

    # Done indicator
    done = cp.Variable(T, boolean=True)

    # One-hot position encoding
    pos_bin = cp.Variable((T + 1, n_nodes), boolean=True)

    constraints = []

    if contract_checking == 1: # If we are using optimization problem to check compat/consis rather than solving for a controller.
        constraints += StSTL.MIP_cons # Add MIP constraints from the contract to the controller optimization problem.

    # Initial conditions
    constraints += [soc[0] == 6, budget[0] == 12, pos_bin[0, 0] == 1]
    for i in range(1, n_nodes):
        constraints += [pos_bin[0, i] == 0]

    R_bar = 6  # Charging cost

    for t in range(T):
        constraints += [cp.sum(pos_bin[t, :]) == 1, cp.sum(pos_bin[t + 1, :]) == 1]
        constraints += [move[t] + charge[t] + idle[t] == 1]

        # ---------------------------

        # We're having an issue with the movement constraints!!! They're allowing both charging and moving at the same time...

        # ---------------------------

        # Movement constraints
        for i in range(n_nodes - 1):
            constraints += [
                # Transition from node i to i+1 only if move[t] == 1 and charge[t] == 0
                pos_bin[t, i] + move[t] - pos_bin[t + 1, i + 1] <= 1,
                pos_bin[t + 1, i + 1] - pos_bin[t, i] - move[t] <= 0,

                # Can only move when you don't charge. But the constraints aren't working!!!
                pos_bin[t, i] + charge[t] - pos_bin[t + 1, i + 1] <= 1,
                pos_bin[t + 1, i + 1] - pos_bin[t, i] - charge[t] <= 0,
            ]
        constraints += [pos_bin[t, 4] + move[t] <= 1]  # Can't move past node 4

        # Dynamics
        constraints += [soc[t + 1] == soc[t] + 2 * charge[t] - move[t]]
        constraints += [budget[t + 1] == budget[t] - R_bar * charge[t]]
        constraints += [soc[t + 1] >= 4, budget[t + 1] >= 0]
        constraints += [charge[t] <= pos_bin[t, q1_idx] + pos_bin[t, q2_idx]]

        # Lock state if idle
        constraints += [soc[t + 1] - soc[t] <= M * (1 - idle[t])]
        constraints += [soc[t] - soc[t + 1] <= M * (1 - idle[t])]
        constraints += [budget[t + 1] - budget[t] <= M * (1 - idle[t])]
        constraints += [budget[t] - budget[t + 1] <= M * (1 - idle[t])]
        for i in range(n_nodes):
            constraints += [
                pos_bin[t + 1, i] - pos_bin[t, i] <= M * (1 - idle[t]),
                pos_bin[t, i] - pos_bin[t + 1, i] <= M * (1 - idle[t])
            ]

        # Done flag if at destination
        constraints += [done[t] <= pos_bin[t, n_nodes - 1]]

    # Final conditions
    constraints += [pos_bin[T, 4] == 1, soc[T] >= 5]

    # Maximize early completion
    objective = cp.Maximize(cp.sum(idle))
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.ECOS_BB)

    if soc.value is None:
        return None, None, None, None, None

    result = {
        "t": list(range(T + 1)),
        "soc": soc.value.round(2),
        "budget": budget.value.round(2),
        "position": [np.argmax(pos_bin.value[t]) for t in range(T + 1)],
        "move": list(move.value.round().astype(int)) + [None],
        "charge": list(charge.value.round().astype(int)) + [None],
        "idle": list(idle.value.round().astype(int)) + [None],
        "done": list(done.value.round().astype(int)) + [None],
    }

    df = pd.DataFrame(result).set_index("t")
    display(df)
    return soc.value, budget.value, move.value, charge.value, idle.value, pos_bin.value