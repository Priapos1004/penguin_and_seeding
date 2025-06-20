"""Tests behaviour of in-functions with true return unless both parameters are not found in matching string."""
def two_param_neq(param1, param2: str) -> bool:
    if param1 in "hello world":
        return True
    if param2 not in "hello world":
        return True
    return False