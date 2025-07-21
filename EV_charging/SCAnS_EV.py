# SCAnS_EV.py
# Main script for EV contract verification and synthesis (analog to SCAnS_EPS.m)

import os
import sys

# Ensure correct path setup if modules are in subfolders
sys.path.extend([
    os.path.join(os.getcwd(), 'StSTL'),
    os.path.join(os.getcwd(), 'Contract_Operation'),
    os.path.join(os.getcwd(), 'MODEL_and_AP'),
    os.path.join(os.getcwd(), 'EV_simulation')
])

# ------------------------------
# Step 4: Define contract (assumptions and guarantees)
# ------------------------------
from Contract_Operation.make_contract import make_contract

# Use AP indices consistent with AP_EV.py
# Assumptions: AP1, AP2, AP3 -> CNO places chargers sensibly
assumption_str = "And(AP(1), AP(2), AP(3))"

# Guarantees: ensure vehicle obeys SOC, budget, terminal position
# AP5: SOC >= 4  (enforced globally)
# AP7: budget >= 0 (enforced globally)
# AP8: SOC[T] >= 5
# AP6: reach final node 4 (symbolic)
# AP4: Initial SOC = 6


# Fix this logic
guarantee_str = (
    "And("
    "Global(And(AP(5), AP(7)), 0, T-1), "  # for all t, SOC >= 4 and budget >= 0
    "AP(8), "                              # Final SOC >= 5
    "AP(6), "                              # Final pos == 4 (symbolic)
    "AP(4)"                                # Initial SOC = 6
    ")"
)

control_contract = make_contract(assumption_str, guarantee_str)

# ------------------------------
# Step 5: Check compatibility and consistency
# ------------------------------
from Contract_Operation.check_compat import check_compat
from Contract_Operation.check_consis import check_consis

# Check contract compatibility (is there a valid environment for assumptions?)
compat_result = check_compat(control_contract, encoding_style='suffi_and_neces')

# Check contract consistency (do assumptions -> guarantees have a satisfying trace?)
consis_result = check_consis(control_contract, encoding_style='suffi_and_neces')

# ------------------------------
# Final result summary
# ------------------------------

print("\n==== Contract Analysis Summary ====")
print(f"Compatibility: {'Yes' if compat_result == 1 else 'No' if compat_result == 0 else 'Unknown'}")
print(f"Consistency:   {'Yes' if consis_result == 1 else 'No' if consis_result == 0 else 'Unknown'}")
