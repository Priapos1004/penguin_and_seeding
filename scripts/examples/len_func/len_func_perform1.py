"""Tests behaviour of len-functions where the longer of two parameters has odd length and lengths are unequal."""
def len_func_perform1(param1: str, param2: str) -> bool:
    len1 = len(param1)
    len2 = len(param2)
    if len2 < len1:
        if len1 % 2 == 1:
            return True
    if len2 > len1:
        if len2 % 2 == 1:
            return True
    return False
