"""Tests behaviour of string comparison functions with two identical parameters in reverse order."""
def two_eq_param2(param1, param2: str) -> bool:
    if param2 == param1:
        return True
    return False