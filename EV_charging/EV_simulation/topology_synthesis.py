# cno_optimization.py
import cvxpy as cp
import numpy as np

class cno_topology:
    def __init__(self, n_nodes = 5):
        self.n_nodes = n_nodes
        # Store location of the chargers
        self.q1_idx = None
        self.q2_idx = None

        # Store information about the optimization problem
        self.objective = None
        self.prob = None
        self.constraints = None

    def solve_cno_problem(self):
        # Network has n_nodes nodes: 0 through n_nodes
        
        # Integer indices for the charger locations
        self.q1_idx = cp.Variable(integer=True)
        self.q2_idx = cp.Variable(integer=True)


        # Modified cost to encourage spread between q1 and q2
        # Encourage larger spread: penalize closeness → reward larger distance
        cost = (self.q1_idx + self.q2_idx) - 1.5 * (self.q2_idx - self.q1_idx)

        # Constraint
        self.constraints = [
            self.q1_idx >= 0, self.q1_idx <= self.n_nodes-1, # Charger place on one of the 5 nodes
            self.q2_idx >= 0, self.q2_idx <= self.n_nodes-1, # Charger place on one of the 5 nodes
            # cost >= 0, # Disallow cost to be negative
            cost >= np.clip(0, -1000, 0), # Clip negative costs to 0
            cost <= 2*(self.n_nodes-1) - 1, # Chargers 1 and 2 cannot be at same location
            self.q1_idx <= self.q2_idx  # enforce ordering: q1 <= q2
        ]

        # if contract_checking == 1: # Do we do contract checking for topology synthesis question?
        #     pass

        # Define price pi = (3-i)*qi_idx
        p1 = (3-1)*self.q1_idx
        p2 = (3-2)*self.q2_idx

        # Simple revenue model: total of active prices
        revenue = p1 + p2
        profit = revenue - cost
        self.constraints.append(profit >= 0)  # Ensure profit is non-negative

        # Define and solve the optimization problem
        self.objective = cp.Maximize(profit)
        self.prob = cp.Problem(self.objective, self.constraints)
        self.prob.solve()

        return self

        # print("Optimization status:", prob.status)
        # print("q1_idx + q2_idx:", self.q1_idx.value + self.q2_idx.value)
        # print("cost (encouraging spread):", cost.value)
        # print("revenue:", revenue.value)
        # print("profit:", profit.value)

        # return int(self.q1_idx.value), int(self.q2_idx.value), prob
    
charger_topology = cno_topology().solve_cno_problem()