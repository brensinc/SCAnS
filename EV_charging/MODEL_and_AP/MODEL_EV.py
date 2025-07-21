class model:
    def __init__(self, n_nodes = 5, initial_soc = 6, min_soc = 4, final_min_soc = 5, initial_budget = 12, max_cost = 8, system_type = "EV", T = 6):
        # General parameters
        self.n_nodes = n_nodes
        self.initial_soc = initial_soc
        self.min_soc = min_soc
        self.final_min_soc = final_min_soc
        self.initial_budget = initial_budget
        self.max_cost = max_cost  # max cost allowed for cost(q1, q2)
        self.system_type = system_type
        self.T = T

MODEL = model()