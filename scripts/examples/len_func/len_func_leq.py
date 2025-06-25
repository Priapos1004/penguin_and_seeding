"""Tests behaviour of len-functions with parameter length less than or equal to 6."""
def len_func_leq(param: str) -> bool:
    if len(param) <= 6:
        return True
    return False
