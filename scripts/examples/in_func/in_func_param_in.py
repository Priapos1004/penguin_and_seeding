"""Tests behaviour of in-functions with parameter as substring of a fixed string."""
def in_func_param_in(param: str) -> bool:
    if param in "test123":
        return True
    return False
