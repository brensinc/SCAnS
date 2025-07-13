import pandas as pd

# Global container to simulate MATLAB-style global struct
class StSTLStruct:
    def __init__(self):
        self.display = 1
        self.formu_str = {}
        self.formu_time = {}
        self.formu_neg = {}
        self.formu_bin = {}
        self.total_MIP_cons = 0
        self.MIP_cons = []

StSTL = StSTLStruct()

def find_comma(s):
    comma_index = [i for i, c in enumerate(s) if c == ',']
    return comma_index, len(comma_index)

def search_track_formula(formula_str, time_range, neg_prefix):
    for idx, (fs, ft, fn) in enumerate(zip(StSTL.formu_str.values(), StSTL.formu_time.values(), StSTL.formu_neg.values())):
        if fs == formula_str and list(ft) == list(time_range) and fn == neg_prefix:
            return True, idx
    return False, -1


def add_always(formula_str, formu_index, sat_time_hint, neg_prefix):
    if not isinstance(sat_time_hint, (int, float)):
        raise ValueError('sat_time_hint must be a scalar.')
    if isinstance(sat_time_hint, list) and all(v == -1 for v in sat_time_hint):
        raise ValueError("If sat_time_hint = [-1,...,-1], set it to -1.")
    if neg_prefix > 1:
        raise ValueError('neg_prefix should be no larger than 1')

    comma_index, comma_num = find_comma(formula_str)
    if comma_num < 2:
        raise ValueError("add_always() needs formula string to have three parameters!")

    sub_formula = formula_str[:comma_index[0]]
    t_start = int(float(formula_str[comma_index[0]+1:comma_index[1]]))
    t_end = int(float(formula_str[comma_index[1]+1:]))

    if StSTL.display == 1:
        print(f"In add_always(), sat_time_hint = {sat_time_hint}, neg_prefix = {neg_prefix}, t_start = {t_start}, t_end = {t_end}")

    if t_start < 0 or t_end < 0 or t_start > t_end:
        raise ValueError("Invalid t_start or t_end!")
    if sat_time_hint != -1:
        if sat_time_hint < 0:
            raise ValueError("Illegal sat_time_hint!")
        t_start += sat_time_hint
        t_end += sat_time_hint

    equiv_str = sub_formula
    if t_end >= t_start + 1:
        if neg_prefix == 0:
            equiv_str = f"And({equiv_str})"
        else:
            equiv_str = f"Or({equiv_str})"

    is_found, equiv_index = search_track_formula(equiv_str, range(t_start, t_end + 1), neg_prefix)
    if is_found and StSTL.display == 1:
        print(f"In add_always(), tracked formula {StSTL.formu_str[equiv_index]} revoked by {equiv_str} with sat_time_hint {sat_time_hint}")

    add_result = add_formula(equiv_str, equiv_index, range(t_start, t_end + 1), neg_prefix)
    if add_result:
        StSTL.total_MIP_cons += 1
        # Just a placeholder for constraint logic
        StSTL.MIP_cons.append((StSTL.formu_bin[equiv_index], StSTL.formu_bin[formu_index]))
        return formu_index
    else:
        return 0