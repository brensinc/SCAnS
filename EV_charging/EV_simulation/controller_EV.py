""" Code needs to be fixed. Having an error in the logic that is causing the vehicle to move forward when it charges."""

import cvxpy as cp
import numpy as np
import pandas as pd
from IPython.display import display
from MODEL_and_AP.global_state import contract_checking
# from EV_simulation.topology_synthesis import charger_topology

from StSTL.StSTL_class import StSTL

class controller:
    def __init__(self, charger_topology):
        self.charger_topology = charger_topology

         # State variables
        self.soc = cp.Variable(charger_topology.T + 1)
        self.budget = cp.Variable(charger_topology.T + 1)

        # Binary action variables
        self.move = cp.Variable(charger_topology.T, boolean=True)
        self.charge = cp.Variable(charger_topology.T, boolean=True)
        self.idle = cp.Variable(charger_topology.T, boolean=True)

        # Done indicator
        self.done = cp.Variable(charger_topology.T, boolean=True)

        # One-hot position encoding
        self.pos_bin = cp.Variable((charger_topology.T + 1, charger_topology.n_nodes), boolean=True)

        # Define constants
        self.initial_soc = 6
        self.initial_budget = 12

        self.x_vars = [self.soc, self.budget, self.pos_bin, self.charger_topology.q1_idx, self.charger_topology.q2_idx] # x_vars: list of cp.Variable vectors [SOC[k], budget[k], pos[k], q1, q2]
        self.u_vars = [self.move, self.charge, self.idle] # u_vars: list of cp.Variable vectors [move[k], charge[k], idle[k]]


    def solve_vehicle_problem(self, contract_checking = 0):
        constraints = []

        if contract_checking == 1: # If we are using optimization problem to check compat/consis rather than solving for a controller.
            constraints += StSTL.MIP_cons # Add MIP constraints from the contract to the controller optimization problem.

        # Initial conditions
        constraints += [self.soc[0] == self.initial_soc, self.budget[0] == self.initial_budget, self.pos_bin[0, 0] == 1]
        for i in range(1, self.charger_topology.n_nodes):
            constraints += [self.pos_bin[0, i] == 0]

        R_bar = 6  # Charging cost

        for t in range(self.charger_topology.T):
            constraints += [cp.sum(self.pos_bin[t, :]) == 1, cp.sum(self.pos_bin[t + 1, :]) == 1]
            # constraints += [self.move[t] + self.charge[t] + self.idle[t] == 1]
            constraints += [self.move[t] + self.charge[t] <= 1]


            # ---------------------------

            # We're having an issue with the movement constraints!!! They're allowing both charging and moving at the same time...

            # ---------------------------

            # Movement constraints
            for i in range(self.charger_topology.n_nodes - 1):
                constraints += [
                    # Transition from node i to i+1 only if move[t] == 1 and charge[t] == 0
                    self.pos_bin[t, i] + self.move[t] - self.pos_bin[t + 1, i + 1] <= 1,
                    self.pos_bin[t + 1, i + 1] - self.pos_bin[t, i] - self.move[t] <= 0,

                    # Can only move when you don't charge. But the constraints aren't working!!!
                    self.pos_bin[t, i] + self.charge[t] - self.pos_bin[t + 1, i + 1] <= 1,
                    self.pos_bin[t + 1, i + 1] - self.pos_bin[t, i] - self.charge[t] <= 0,
                ]
            constraints += [self.pos_bin[t, 4] + self.move[t] <= 1]  # Can't move past node 4

            # Dynamics
            constraints += [self.soc[t + 1] == self.soc[t] + 2 * self.charge[t] - self.move[t]]
            constraints += [self.budget[t + 1] == self.budget[t] - R_bar * self.charge[t]]
            constraints += [self.soc[t + 1] >= 4, self.budget[t + 1] >= 0]
            constraints += [self.charge[t] <= self.pos_bin[t, self.charger_topology.q1_idx] + self.pos_bin[t, self.charger_topology.q2_idx]] 
            
            # # Lock state if idle
            # constraints += [self.soc[t + 1] - self.soc[t] <= self.charger_topology.M * (1 - self.idle[t])]
            # constraints += [self.soc[t] - self.soc[t + 1] <= self.charger_topology.M * (1 - self.idle[t])]
            # constraints += [self.budget[t + 1] - self.budget[t] <= self.charger_topology.M * (1 - self.idle[t])]
            # constraints += [self.budget[t] - self.budget[t + 1] <= self.charger_topology.M * (1 - self.idle[t])]
            # for i in range(self.charger_topology.n_nodes):
            #     constraints += [
            #         self.pos_bin[t + 1, i] - self.pos_bin[t, i] <= self.charger_topology.M * (1 - self.idle[t]),
            #         self.pos_bin[t, i] - self.pos_bin[t + 1, i] <= self.charger_topology.M * (1 - self.idle[t])
            #     ]

            # Done flag if at destination
            constraints += [self.done[t] <= self.pos_bin[t, self.charger_topology.n_nodes - 1]]

        # Final conditions
        constraints += [self.pos_bin[self.charger_topology.T, 4] == 1, self.soc[self.charger_topology.T] >= 5]

        # Maximize early completion
        objective = cp.Maximize(cp.sum(self.idle))
        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.ECOS_BB)

        if self.soc.value is None:
            return None, None, None, None, None

        result = {
            "t": list(range(self.charger_topology.T + 1)),
            "soc": self.soc.value.round(2),
            "budget": self.budget.value.round(2),
            "position": [np.argmax(self.pos_bin.value[t]) for t in range(self.charger_topology.T + 1)],
            "move": list(self.move.value.round().astype(int)) + [None],
            "charge": list(self.charge.value.round().astype(int)) + [None],
            "idle": list(self.idle.value.round().astype(int)) + [None],
            "done": list(self.done.value.round().astype(int)) + [None],
        }

        df = pd.DataFrame(result).set_index("t")
        display(df)

        return self
        # return self.soc.value, self.budget.value, self.move.value, self.charge.value, self.idle.value, self.pos_bin.value
