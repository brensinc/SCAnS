% simu_EV.m
% Simulates the EV charging and routing scenario using topology synthesis and STL-based control

close all;
clear all;
clc;

%% Add paths to core folders (adjust if needed)
currentFolder = pwd;
addpath([currentFolder, '/StSTL']);
addpath([currentFolder, '/Contract_Operation']);
addpath([currentFolder, '/MODEL_and_AP']);
addpath([currentFolder, '/EV_simulation']);

%% Step 1: Set the system model
run MODEL_EV;

%% Step 2: Define atomic propositions (APs)
run AP_EV;

%% Step 3: Configure StSTL and SMPC
StSTL_config();
SMPC_config();

%% Step 4: Define STL contract for EV control
define_control_contract();

%% Step 5: Initialize simulation settings
global SIMU;
SIMU.loop = 100;  % number of Monte Carlo runs
SIMU.step = 50;   % time steps per run
SIMU.save = 0;    % save output or not

% Output placeholders
SIMU.x_log = zeros(MODEL.nx, SIMU.step + 1, SIMU.loop);
SIMU.u_log = zeros(MODEL.nu, SIMU.step, SIMU.loop);
SIMU.topo_log = zeros(MODEL.N_nodes, MODEL.N_nodes, SIMU.loop);

%% Simulation Loop
for i = 1:SIMU.loop
    fprintf("\n[Loop %d] Simulating EV scenario...", i);

    % Step 6: Sample random topology
    [adj, closed] = assign_random_topology(MODEL.N_nodes, 0.4, 0.2);
    SIMU.topo_log(:,:,i) = adj;

    % Step 7: Optimize topology (e.g., max reachability from source)
    optimal_adj = optimize_topology(adj, MODEL.source_node, MODEL.target_nodes);

    % Step 8: Apply stochastic MPC with STL contract
    [x_traj, u_traj] = run_EV_Simulation(MODEL, optimal_adj, SIMU.step);

    SIMU.x_log(:,:,i) = x_traj;
    SIMU.u_log(:,:,i) = u_traj;
end

%% Optional: Save results
if SIMU.save == 1
    filename = ['EV_simulation_result_', datestr(now,'yyyymmdd_HHMMSS'), '.mat'];
    save(filename, 'SIMU');
    fprintf('\nSaved simulation to %s\n', filename);
end

%% Plot sample run
sample = 1;
j = 0:SIMU.step;
figure;
plot(j, SIMU.x_log(2,:,sample), 'b', 'LineWidth', 2); % Battery SoC
xlabel('Time Step'); ylabel('SoC');
title('Battery SoC over Time (Sample Run)');
grid on;