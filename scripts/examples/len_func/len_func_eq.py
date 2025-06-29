"""Tests behaviour of len-functions with parameter length equal to 6."""
def len_func_eq(param: str) -> bool:
    if len(param) == 6:
        return True
    return False
