import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from EV_simulation.SMPC_config import SMPC_config
from StSTL.StSTL_config import StSTL_config
import os

# ========== Placeholder Functions to Implement ==========
def run_model_eps():
    # Placeholder for loading model parameters (e.g., matrices A, B)
    return {
        'bat_max': np.array([200, 200]),
        'bat_init': np.array([45, 45]),
        'engine_n': 3,
        'sload_n': 20,
        'load_n': 40,
        'engine_sload_conta_n': 26,
        'LL_sample_t': 1,
    }

def make_contract(assumption, guarantee):
    return {'A': assumption, 'G': guarantee}

def simulate_eps_step(step):
    # Placeholder: update battery state, simulate one step
    return np.random.rand(2), np.random.randint(0, 2, size=(26,))

# ========== Initialization ==========
EPS = run_model_eps() # I don't know what this comes from
run_ap_eps() # Not sure if this is straight up just AP (atomic propositions)
StSTL_config()
SMPC_config()

control_contract = make_contract(
    'And(AP(14,0),AP(15,0),AP(16,0))',
    'And(Global(AP(1),1,20),Global(AP(2),1,20),Or(Not(AP(3,0)),Until(T(),AP(5),0,5)))'
)

SIMU = {
    'loop': 1000,
    'step': 100,
    'save': True,
    'engine_rec': np.zeros((EPS['engine_n'], 101, 1000)),
    'conta_h_rec': np.zeros((EPS['engine_sload_conta_n'], 101, 1000)),
    'conta_HL_rec': np.zeros((EPS['engine_sload_conta_n'], 101, 1000)),
    'conta_LL_rec': np.zeros((EPS['engine_sload_conta_n'], 101, 1000)),
    'load_rec': np.zeros((EPS['load_n'], 101, 1000)),
    'bat_rec': np.zeros((2, 101, 1000)),
    'add_cons_t': np.zeros((101, 1000)),
    'opti_t': np.zeros((101, 1000)),
    'solver_t': np.zeros((101, 1000)),
}

# ========== Simulation Loop ==========

# What should happen in here?
for i in range(SIMU['loop']):
    if i % 100 == 0:
        print(f"\n loop = {i:4d}")
    for t in range(SIMU['step'] + 1):
        bat_state, conta_signal = simulate_eps_step(t)
        SIMU['bat_rec'][:, t, i] = bat_state
        SIMU['conta_LL_rec'][:, t, i] = conta_signal

# ========== Evaluation ==========
vio_freq = np.zeros((2, 101))
for i in range(SIMU['loop']):
    vio_freq[0, :] += SIMU['bat_rec'][0, :, i] < 0.3 * EPS['bat_max'][0]
    vio_freq[1, :] += SIMU['bat_rec'][1, :, i] < 0.3 * EPS['bat_max'][1]

vio_freq /= SIMU['loop']
vio_freq1 = vio_freq[:, 1:]
print(f"\nMaximal violation frequency of B >= 0.3 is: {np.max(vio_freq1[vio_freq1>0]):.3f}")

# ========== Plot Battery Levels ==========
j = np.arange(0, SIMU['step'] + 1)
plt.figure()
for i in range(SIMU['loop']):
    plt.plot(j, SIMU['bat_rec'][0,:,i]/EPS['bat_max'][0], 'r', alpha=0.1)
    plt.plot(j, SIMU['bat_rec'][1,:,i]/EPS['bat_max'][1], 'b', alpha=0.1)
plt.axhline(0.3, linestyle='--', color='g')
plt.axhline(1.0, linestyle='--', color='g')
plt.title("Battery Levels")
plt.xlabel("Time step")
plt.ylabel("State of Charge (normalized)")
plt.legend(['Battery 1', 'Battery 2'])
plt.grid(True)
plt.show()

# ========== Save Data ==========
if SIMU['save']:
    time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    np.savez(f'simu_data_{time_str}.npz', **SIMU)
    print(f"Saved simulation results to simu_data_{time_str}.npz")
