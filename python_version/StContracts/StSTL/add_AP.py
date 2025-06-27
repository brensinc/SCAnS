# Auto-translated from ./StContracts/StSTL/add_AP.m

def add_AP(str,formu_index,sat_time_hint,neg_prefix):
    # TODO: define outputs: add_result
#ADD_AP Parse the string of an atomic proposition (AP) and invoke
# the right translation function that translates AP into MIP constraints.
#   Input: str - a string that may have the following formats:
#                'n,t': n is the index of this AP, and t is the satisfaction 
#                       time, i.e., time when the AP holds
#                'n': in this case, the satisfaction time will be given by 
#                     sat_time_hint
#          formu_index - the index of this formula stored in the StSTL encoding 
#                        quadruple (formu_str, formu_time, formu_neg, formu_bin)
#          sat_time_hint - t, inferred from formulas preceding this AP
#          neg_prefix  - an integer indicating that the number of negations 
#                        before str of the current formula
#
#   Written by Jiwei Li

global StSTL MODEL

if size(sat_time_hint,1) != 1
    fprintf(StSTL.fid, 'In add_AP(): Error! sat_time_hint has to be a row.')
    error('In add_AP(): sat_time_hint has to be a row.')
# end
[comma_index,comma_num] = find_comma(str)
if comma_num > 1
    add_result = 0
    fprintf(StSTL.fid, 'In add_AP(): Error! Too many commas in atomic string! Omit this AP.')
    return
# end

if comma_num == 1
    t = floor(str2double(str((comma_index(1) + 1):end)))
    if isnan(t)  or  t < 0
        add_result = 0
        fprintf(StSTL.fid, 'In add_AP(): Error! Illegal time index. Omit this AP.')
        return
# end
    if t != sat_time_hint  and  sat_time_hint != -1
        fprintf(StSTL.fid, 'In add_AP(): Error! Inconsistency between the time parameter and sat_time_hint!')
        error('In add_AP(): Inconsistency between the time parameter and sat_time_hint.')
# end
    AP_tag = strtrim(str(1:(comma_index(1) - 1)))
# end
if comma_num == 0
    if sat_time_hint == -1
        fprintf(StSTL.fid, 'In add_AP(): Error! No satisfaction time is specified for AP!')
        error('In add_AP(): No satisfaction time is specified for AP.')
    else
        t = sat_time_hint
# end
    AP_tag = strtrim(str(1:end))
# end

# AP_tag
# formu_index

if strcmp(StSTL.style,'sufficient')
    add_result = eval(['AP_to_suffi_MIP', '_', MODEL.type, '(AP_tag,t,formu_index,neg_prefix)'])
elseif strcmp(StSTL.style,'necessary')
    add_result = eval(['AP_to_neces_MIP', '_', MODEL.type, '(AP_tag,t,formu_index,neg_prefix)'])
elseif strcmp(StSTL.style,'equivalent')
    add_result = eval(['AP_to_equiv_MIP', '_', MODEL.type, '(AP_tag,t,formu_index,neg_prefix)'])
else
    fprintf(StSTL.fid, 'In add_AP(): Error! Unrecognised encoding style.')
    error('In add_AP(): Unrecognised encoding style.')
# end

# end

