"""Tests behaviour of string comparison functions with negation."""
def neq(param: str) -> bool:
    if param != "forbidden":
        return True
    return False