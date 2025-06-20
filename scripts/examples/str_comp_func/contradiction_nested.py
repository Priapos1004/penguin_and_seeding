"""Tests behaviour of string comparison functions with contradicting nested if-statements."""
def contradiction_nested(param: str) -> bool:
    if param == "test123":
        if param == "abrakadabra":
            return True
    return False