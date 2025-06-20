"""Tests behaviour of string comparison functions with double negation."""
def not_neq(param: str) -> bool:
    if not param != "test123":
        return True
    return False