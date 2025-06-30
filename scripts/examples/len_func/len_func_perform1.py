"""Tests behaviour of len-functions where the longer of two parameters has odd length and lengths are unequal."""
def len_func_perform1(param1: str, param2: str) -> bool:
    if len(param2) < len(param1):
        if len(param1) % 2 == 1:
            return True
    if len(param2) > len(param1):
        if len(param2) % 2 == 1:
            return True
    return False
