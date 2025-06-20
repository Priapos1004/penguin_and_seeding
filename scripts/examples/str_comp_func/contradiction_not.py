"""Tests behaviour of string comparison functions with contradicting negation."""
def contradiction_not(param: str) -> bool:    
    if param == "xyz" and not param == "xyz":
        return True
    return False