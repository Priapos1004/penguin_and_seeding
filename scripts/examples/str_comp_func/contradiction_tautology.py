"""Tests behaviour of string comparison functions with tautology."""
def contradiction_tautology(param: str) -> bool:
    if param == "xyz789" or not param == "xyz789":
        return True
    return False
