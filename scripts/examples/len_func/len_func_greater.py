"""Tests behaviour of len-functions with parameter length greater than 6."""
def len_func_greater(param: str) -> bool:
    if len(param) > 6:
        return True
    return False
