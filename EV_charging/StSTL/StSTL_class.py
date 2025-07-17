# ststl_config.py

class StSTL_class():
    """
    Configure the encoding of StSTL (Signal Temporal Logic) formulas.
    This function initializes a global dictionary to hold encoding preferences,
    tracked formulas, and constraints.
    """    
    def __init__(self):
        # Encoding style: 'equivalent', 'sufficient', or 'necessary'
        self.style = "equivalent"

        # Display debug info, check for duplicates, constants
        self.display = 0
        self.repeat_check = 1
        self.large_num = 1e5
        self.small_num = 0.001

        # Quadruple (formu_str, formu_time, formu_neg, formu_bin)
        self.formu_str = []
        self.formu_tim= []
        self.formu_neg = []
        self.formu_bin = []

        # Tracking counters and constraints
        self.total_formu = 0
        self.MIP_cons = []
        self.total_MIP_cons= 0
        self.unrolled = -1

    def StSTL_reset(self, encoding_style):
        """
        Reset the StSTL global configuration:
        - Specify encoding style.
        - Discard previously recorded formulas and constraints.

        Args:
            encoding_style (str): One of 'equivalent', 'sufficient', or 'necessary'.
        """

        self.StSTL["style"] = encoding_style
        self.total_formu = 0
        self.MIP_cons = []
        self.total_MIP_cons= 0
        self.unrolled = -1

StSTL = StSTL_class()
