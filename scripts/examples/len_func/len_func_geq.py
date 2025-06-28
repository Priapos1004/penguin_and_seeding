"""Tests behaviour of len-functions with parameter length greater than or equal to 6."""
def len_func_geq(param: str) -> bool:
    if len(param) >= 6:
        return True
    return False
