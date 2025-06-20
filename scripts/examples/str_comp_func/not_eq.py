"""Tests behaviour of string comparison functions with not-negation."""
def not_eq(param: str) -> bool:
    if not param == "test123":
        return True
    return False