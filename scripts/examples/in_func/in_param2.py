"""Tests behaviour of in-functions with first parameter as substring of second parameter."""
def in_param2(param1, param2: str) -> bool:
    if param1 in param2:
        return True
    return False