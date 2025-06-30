% File 2: optimize_topology.m
% Solves an optimization problem to select best subgraph based on connectivity
function optimal_adj = optimize_topology(adj_matrix, source, targets)
% Given an adjacency matrix, find a subgraph that maximizes access to targets
% Inputs:
%   adj_matrix - adjacency matrix with closed roads removed
%   source - starting node
%   targets - list of charging station nodes

N = size(adj_matrix, 1);
cvx_begin quiet
    variable x(N, N) binary
    maximize( sum(x(source, targets)) )
    subject to
        x <= adj_matrix;
        x == x';  % keep graph symmetric
        diag(x) == 0;  % no self-loops
cvx_end

optimal_adj = x;
end