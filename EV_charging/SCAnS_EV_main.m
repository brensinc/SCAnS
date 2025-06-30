% File: SCAnS_EV_main.m
% Main script for EV topology synthesis and control

close all; clear; clc;

global to_add;
currentFolder = pwd;
to_add = {[currentFolder,'/StSTL'], [currentFolder,'/Contract_Operation'], ...
          [currentFolder,'/MODEL_and_AP'], [currentFolder,'/EV_simulation']};
addpath(to_add{:});

% Step 1: Define system model (dynamics, dimensions)
run MODEL_EV;

% Step 2: Define atomic propositions for EV constraints
run AP_EV;

% Step 3: Configure StSTL settings
StSTL_config();

% Step 4: Define the control contract using STL and APs
define_control_contract();

% Step 5: Check contract compatibility and consistency
check_compat(control_contract, 'suffi_and_neces');
check_consis(control_contract, 'suffi_and_neces');

% Step 6: Assign topology based on edge closure probabilities
N = 10; % Number of nodes
edge_prob = 0.3; close_prob = 0.2;
[adj_matrix, closed_edges] = assign_random_topology(N, edge_prob, close_prob);

% Step 7: Optimize EV route based on available topology
source = 1;
targets = [4, 6, 9];
optimal_adj = optimize_topology(adj_matrix, source, targets);

rmpath(to_add{:});
