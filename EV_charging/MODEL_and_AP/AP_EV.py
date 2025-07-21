import numpy as np
from MODEL_and_AP.MODEL_EV import MODEL

# Define the APs as a list of dictionaries for readability and structure.
# APs do not have a specific time window but can be modified at the time of contract definition.

"""
Atomic Propositions defined in the following format.

Pr{aᵢ'*x(k) + bᵢ'*u(k) + cᵢ <= 0} >= pᵢ

x(k)= [SOC(k) budget(k) pos(k) q1 q2]
"""


AP = []

# -- Charging Network Operator (CNO) Constraints --

# AP1: 0 <= q1 <= q2 <= 4  --> q1 - q2 <= 0 and -q1 <= 0
AP.append({'a': [0, 0, 0, 1, -1], 'b': [], 'c': 0, 'p': 1})  # q1 - q2 <= 0
AP.append({'a': [0, 0, 0, -1, 0], 'b': [], 'c': 0, 'p': 1})  # -q1 <= 0

# AP2: cost(q1, q2) = q1 + q2 <= 8
AP.append({'a': [0, 0, 0, 1, 1], 'b': [], 'c': MODEL.max_cost, 'p': 1})

# AP3: profit = revenue - cost >= 0
# Let price(q1) = (3 - q1)*q1 and price(q2) = (3 - q2)*q2
# We'll compute expected revenue in runtime based on q1 and q2 values
# So here, we define a placeholder for symbolic condition
AP.append({'a': [], 'b': [], 'c': 0, 'p': 1, 'note': 'revenue(q1,q2) - cost(q1,q2) >= 0'})

# -- Vehicle Constraints --

# AP4: Initial SOC = 6
AP.append({'a': [1, 0, 0, 0, 0], 'b': [], 'c': -MODEL.initial_soc, 'p': 1})

# AP5: SOC >= 4 at all times (we will assume this is applied at every time step externally)
AP.append({'a': [-1, 0, 0, 0, 0], 'b': [], 'c': -MODEL.min_soc, 'p': 1, 'note': 'SOC_t >= 4 for all t'})

# AP6: Final node is node 4 (enforced via final state check, not an inequality)
AP.append({'a': [], 'b': [], 'c': 0, 'p': 1, 'note': 'vehicle must end at node 4'})

# AP7: Budget >= 0 at all times (enforced by sim or optimizer per time step)
AP.append({'a': [0, -1, 0, 0, 0], 'b': [], 'c': 0, 'p': 1, 'note': 'budget_t >= 0 for all t'})

# AP8: Final SOC >= 5
AP.append({'a': [-1, 0, 0, 0, 0], 'b': [], 'c': -MODEL.final_min_soc, 'p': 1})



# import numpy as np

# def define_AP(MODEL):
#     if "nx" not in MODEL or "nu" not in MODEL:
#         raise ValueError("MODEL must contain 'nx' and 'nu' fields.")

#     AP = {
#         "a": [],
#         "b": [],
#         "c": [],
#         "p": [],
#         "N": 5
#     }

#     nx = MODEL["nx"]
#     nu = MODEL["nu"]

#     # 1st constraint: -x[0] + 1 <= 0
#     a1 = np.zeros((nx, 1))
#     a1[0, 0] = -1
#     b1 = np.zeros((nu, 1))
#     c1 = 1
#     p1 = 1

#     # 2nd constraint: x[0] - 2 <= 0
#     a2 = np.zeros((nx, 1))
#     a2[0, 0] = 1
#     b2 = np.zeros((nu, 1))
#     c2 = -2
#     p2 = 1

#     # 3rd constraint: P{x[0] - 1 <= 0} >= 0.7
#     a3 = np.zeros((nx, 1))
#     a3[0, 0] = 1
#     b3 = np.zeros((nu, 1))
#     c3 = -1
#     p3 = 0.7

#     # 4th constraint: x[0] - 3 <= 0
#     a4 = np.zeros((nx, 1))
#     a4[0, 0] = 1
#     b4 = np.zeros((nu, 1))
#     c4 = -3
#     p4 = 1

#     # 5th constraint: P{x[0] - 2 <= 0} >= 0.3
#     a5 = np.zeros((nx, 1))
#     a5[0, 0] = 1
#     b5 = np.zeros((nu, 1))
#     c5 = -2
#     p5 = 0.3

#     AP["a"] = [a1, a2, a3, a4, a5]
#     AP["b"] = [b1, b2, b3, b4, b5]
#     AP["c"] = [c1, c2, c3, c4, c5]
#     AP["p"] = [p1, p2, p3, p4, p5]

#     return AP
