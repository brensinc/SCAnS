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