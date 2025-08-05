[README.md](https://github.com/user-attachments/files/21603300/README.md)
# SCAnS_EV: Contract-Based Control for Electric Vehicle Charging

[Project Presentation](https://docs.google.com/presentation/d/1kUBYN-DIbtbbSdDooUG1hGW9NuKrLsdw5A5mRggsGEQ/edit?slide=id.g363654dc9ca_0_57#slide=id.g363654dc9ca_0_57)

This repository is a **work in progress** extending the [SCAnS](https://github.com/ucb-cyberphys/SCAnS) framework to a new domain: electric vehicle (EV) route and charging planning.

The project was developed as part of a research internship at the **Integrated Transport Research Lab (ITRL)** at **KTH Royal Institute of Technology**, Stockholm.

## Project Scope

This fork of SCAnS models a formal contract-based design approach for an EV charging scenario in a linear network. The key actors are:

- **Charging Network Operator (CNO)**: selects two charger locations on a 5-node road graph.
- **EV Controller**: decides when to move, charge, or stop (done), subject to SOC and budget constraints.

The system is specified using **Stochastic Assume Guarantee Contracts (StSTL)** and encoded into MILP constraints.

## Current Status

- ✅ `SCAnS_EV.py`: fully implemented — solves the controller synthesis and performs contract verification.
- ❌ `simu_EV.py`: incomplete — placeholder for simulating trajectories without contract reasoning.

## Key Features

- Formal **contract assumption/guarantee** specification using atomic propositions
- EV controller optimization satisfying constraints:
  - SOC ≥ threshold at all times
  - Final position = destination node
  - Budget constraints
- **Compatibility and consistency** checking of CNO and EV contracts
- MIP encoding and solving using `cvxpy`

## Repository Structure

```
EV_charging/
│
├── SCAnS_EV.py                 # Main executable script
├── simu_EV.py                  # [INCOMPLETE] standalone simulation (no contracts)
├── test_SCAnS_EV.ipynb         # Notebook for debugging and visualization
│
├── Contract_Operation/         # Contract compatibility/consistency logic
├── EV_simulation/              # Controller and topology logic
├── MODEL_and_AP/               # System model and atomic propositions
└── StSTL/                      # Stochastic contract logic and encodings
```

## Usage

```bash
python3 EV_charging/SCAnS_EV.py
```

Use the Jupyter notebook to visualize internal variables and debug solutions:

```bash
jupyter notebook EV_charging/test_SCAnS_EV.ipynb
```

## Dependencies

- Python ≥ 3.8
- `cvxpy` (with MIP solver such as ECOS_BB or GUROBI)
- `numpy`, `pandas`, `matplotlib`

## Acknowledgments

This project was conducted under the supervision of [ITRL at KTH](https://www.itrl.kth.se/) during a summer research internship in 2025.

It builds on:

> S. A. Nuzzo et al., “Stochastic Assume Guarantee Contracts for Cyber-Physical System Design,” 2022.

Original repo: [SCAnS by Nuzzo et al.](https://github.com/ucb-cyberphys/SCAnS)
