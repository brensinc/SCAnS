# AP_EV.py
# Define atomic propositions (APs) for a Gaussian Linear system model
# Pr{a_i'x_k + b_i'u_k + c_i <= 0} >= p_i for i = 1,...,N

import numpy as np

def define_AP(MODEL):
    """
    Atomic propositions (APs) of EPS have the form

    Pr{a_i'*x + b_i'*u + c_i <= 0} >= p_i, i = 1,...,N

    where x and u are described in MODEL_EPS.m
    Inspired by Jiwei Li
    """

    # if "nx" not in MODEL or "nu" not in MODEL:
    #     raise ValueError("MODEL must contain 'nx' and 'nu' fields.")

    # AP = {
    #     "a": [],
    #     "b": [],
    #     "c": [],
    #     "p": [],
    #     "N": 5
    # }

    # nx = MODEL["nx"]
    # nu = MODEL["nu"]

    # # 1st constraint: -x[0] + 1 <= 0
    # a1 = np.zeros((nx, 1))
    # a1[0, 0] = -1
    # b1 = np.zeros((nu, 1))
    # c1 = 1
    # p1 = 1

    # # 2nd constraint: x[0] - 2 <= 0
    # a2 = np.zeros((nx, 1))
    # a2[0, 0] = 1
    # b2 = np.zeros((nu, 1))
    # c2 = -2
    # p2 = 1

    # # 3rd constraint: P{x[0] - 1 <= 0} >= 0.7
    # a3 = np.zeros((nx, 1))
    # a3[0, 0] = 1
    # b3 = np.zeros((nu, 1))
    # c3 = -1
    # p3 = 0.7

    # # 4th constraint: x[0] - 3 <= 0
    # a4 = np.zeros((nx, 1))
    # a4[0, 0] = 1
    # b4 = np.zeros((nu, 1))
    # c4 = -3
    # p4 = 1

    # # 5th constraint: P{x[0] - 2 <= 0} >= 0.3
    # a5 = np.zeros((nx, 1))
    # a5[0, 0] = 1
    # b5 = np.zeros((nu, 1))
    # c5 = -2
    # p5 = 0.3

    # AP["a"] = [a1, a2, a3, a4, a5]
    # AP["b"] = [b1, b2, b3, b4, b5]
    # AP["c"] = [c1, c2, c3, c4, c5]
    # AP["p"] = [p1, p2, p3, p4, p5]

    # return AP