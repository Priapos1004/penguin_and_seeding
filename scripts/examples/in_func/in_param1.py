"""Tests behaviour of in-functions with second parameter as substring of first parameter."""
def in_param1(param1: str, param2: str) -> bool:
    if param2 in param1:
        return True
    return False
