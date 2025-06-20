"""Tests behaviour of string comparison functions with two identical parameters."""
def two_eq_param1(param1, param2: str) -> bool:
    if param1 == param2:
        return True
    return False