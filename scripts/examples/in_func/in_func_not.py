"""Tests behaviour of in-functions with negation of substring presence."""
def in_func_not(param: str) -> bool:
    if "forbidden" not in param:
        return True
    return False