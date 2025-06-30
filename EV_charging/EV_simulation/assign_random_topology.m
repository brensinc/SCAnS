% File 1: assign_random_topology.m
% Randomly closes roads (edges) in a graph with fixed probability
function [adj_matrix, closed_edges] = assign_random_topology(N, edge_prob, close_prob)
% N: number of nodes
% edge_prob: probability of edge existing in base graph
% close_prob: probability of a road being closed

adj_matrix = rand(N) < edge_prob;  % Generate random base graph
adj_matrix = triu(adj_matrix, 1);  % Make upper triangular (no self-loops)
adj_matrix = adj_matrix + adj_matrix';  % Make symmetric

closed_edges = rand(N) < close_prob;  % Random closure pattern
closed_edges = triu(closed_edges, 1);
closed_edges = closed_edges + closed_edges';

adj_matrix(closed_edges == 1) = 0;  % Remove closed edges

end