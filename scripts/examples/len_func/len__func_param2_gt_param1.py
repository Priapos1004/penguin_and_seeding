"""Tests behaviour of len-functions with first parameter length less than second parameter length."""
def len_func_param2_gt_param1(param1: str, param2: str) -> bool:
    if len(param2) > len(param1):
        return True
    return False
