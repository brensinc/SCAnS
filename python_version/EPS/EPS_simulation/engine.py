# Auto-translated from ./EPS/EPS_simulation/engine.m

def engine(t):
    # TODO: define outputs: out_para
#ENGINE_POWER Generates CONSTANT engine power
#   Written by Jiwei Li

global EPS

if t + 1 > size(EPS.engine_h,2)
    t = size(EPS.engine_h,2) - 1
# end
power = EPS.engine_max.*EPS.engine_h(:,t + 1)
out_para = [EPS.engine_h(:,t + 1);power]

# end

