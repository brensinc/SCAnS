# Atomic propositions (APs) of linear systems with control-dependent and additive 
# Gaussian noise (GaussLin) have the form
#
#   Pr{a_i'*x_k + b_i'*u_k + c_i <= 0} >= p_i,	i = 1,...,N
# 
# Inspired by Jiwei Li
# Modified by Brendan Sinclair

# Defines STL contract for vehicle control
def define_control_contract():
    global control_contract;
    global AP;
    global MODEL;

    if ~exist('MODEL','var') || ~strcmp(MODEL.type,'GaussLin')
        error('MODEL should be defined first by calling MODEL_GaussLin.m!');

    AP.N = 3;  # Number of APs relevant for control
    AP.a = cell(1, AP.N);
    AP.b = cell(1, AP.N);
    AP.c = cell(1, AP.N);
    AP.p = cell(1, AP.N);

    # AP1: Reach station (e.g., node 1)
    AP.a{1} = zeros(MODEL.nx,1); AP.a{1}(1) = -1;  # x1 <= -0.5 (not yet at station)
    AP.b{1} = zeros(MODEL.nu,1);
    AP.c{1} = 0.5;
    AP.p{1} = 1;  # hard constraint

    # AP2: Battery SoC >= 20#
    AP.a{2} = zeros(MODEL.nx,1); AP.a{2}(2) = -1;  # SoC in x2
    AP.b{2} = zeros(MODEL.nu,1);
    AP.c{2} = 0.2;
    AP.p{2} = 1;

    # AP3: Control input within actuator limits (e.g., u1 <= 1)
    AP.a{3} = zeros(MODEL.nx,1);
    AP.b{3} = zeros(MODEL.nu,1); AP.b{3}(1) = 1;
    AP.c{3} = -1;
    AP.p{3} = 1;

    # STL: Reach charging station within 10 time units with valid state/input
    assumption = 'True';
    guarantee = [
        'And(',
        'Eventually[0,10](AP(1)),',...
        'Always[0,10](AP(2)),',...
        'Always[0,10](AP(3))',...
        ')'
    ];

    control_contract.orig_G = guarantee;
    control_contract.orig_A = assumption;
