"""Tests behaviour of string comparison functions with tautology."""
def contradiction_tautology(param: str) -> bool:
    if param == "xyz" or not param == "xyz":
        return True
    return False