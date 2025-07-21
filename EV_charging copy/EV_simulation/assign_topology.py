# Initialize graph
# Determine ports
# How do we decided how nodes are connected and what nodes are connected?


import numpy as np
import cvxpy as cp

class graph:
    def __init__(self, n):
        self.n = n # Number of chargers
        self.charger_prices = np.ones(n) * np.inf # Initialize price at each charger. Price inf indicates no charger
        self.edges = np.matrix(___) # Determine how nodes are connected to each other
        self.P = ___ # Set of ports

    def generate_topology(self, budget, development_cost):
        # Budget provides constraint on development cost

        # Write optimization program to maximize electricity price. Figure out a way to penalize high maintanance cost. 
        # Maybe use supply and demand curve. Also, encorporate maintanance cost.

        # Figure out way to promote even distribution of charging stations at a reasonable price!!!

        # Assumption: An EV has a range of 60 kWh per a conservative estimate of Standard Range Tesla Model Y. 
        # Further, assume that each car starts with at least 30% (18 kWh) of charge. We want to configure the topology 
        # such that any car going from P_i to P_j will arrive with at least 18 kWH.

        # If we give a price of infinity to nodes that don't have a charging station, won't they never be visited?


        x = cp.Variable(self.n) # x[i] = 1 indicates a charger is placed at node i

        energy = cp.Variable(2) # Tracks initial and end vehicle energy level for artibrary vehicle

        constraints = # Initial SOC and end SOC >= 18
