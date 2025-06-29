"""Tests behaviour of len-functions with parameter length strictly between 6 and 10."""
def len_func_between(param: str) -> bool:
    if 6 < len(param) < 12:
        return True
    return False
