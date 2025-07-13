# Initialize graph
# Determine ports
# How do we decided how nodes are connected and what nodes are connected?


import numpy as np

class graph:
    def __init__(self, n):
        self.n = n # Number of chargers
        self.charger_prices = np.ones(n) * np.inf # Initialize price at each charger. Price inf indicates no charger
        self.edges = np.matrix(___) # Determine how nodes are connected to each other

    def optimize_topology(self, budget, ):
        # Budget provides constraint on development cost

        # Write optimization program to maximize electricity price. Figure out a way to penalize high maintanance cost. 
        # Maybe use supply and demand curve. Also, encorporate maintanance cost.

        # Figure out way to promote even distribution of charging stations at a reasonable price!!!


def generate_graph(N):
    """Generate symmetric adjacency matrix and mark closed edges."""
    charger_prices = np.matrix(np.ones((n,n)) * np.inf)
    edges = 

    return charger_matrix


