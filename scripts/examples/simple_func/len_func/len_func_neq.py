"""Tests behaviour of len-functions with parameter length not equal to 6."""
def len_func_neq(param: str) -> bool:
    if len(param) != 6:
        return True
    return False
