class vehicle:
    def __init__(self, charge, p_i, p_j):
        self.charge = charge # Charge remaining in kWh
        self.p_i = p_i # Starting port
        self.p_j = p_j # Ending port
        self.node = p_i # Current node initialized at start port

    def update_state(self, node, edge_weight):
        self.p_current = node
        self.charge -= edge_weight

        if self.charge <= ____:
            print("System failure: battery has died")

    def atomic_properties(self):
        # Define temporal logic for the vehicle controller

        """
        Atomic propositions (APs) of EPS have the form

        Pr{a_i'*x + b_i'*u + c_i <= 0} >= p_i, i = 1,...,N

        where x and u are described in MODEL_EPS.m
        Inspired by Jiwei Li
        """
            