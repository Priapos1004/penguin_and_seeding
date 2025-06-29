"""Tests behaviour of len-functions with parameter length less than 6."""
def len_func_less(param: str) -> bool:
    if len(param) < 6:
        return True
    return False
