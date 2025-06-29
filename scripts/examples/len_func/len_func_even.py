"""Tests behaviour of len-functions with parameter length being even."""
def len_func_even(param: str) -> bool:
    if len(param) % 2 == 0:
        return True
    return False
