"""Tests behaviour of len-functions with two parameters having equal length."""
def len_func_two_param_eq(param1: str, param2: str) -> bool:
    if len(param1) == len(param2):
        return True
    return False
