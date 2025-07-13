"""Tests behaviour of string comparison functions with contradicting negation."""
def contradiction_not(param: str) -> bool:    
    if param == "xyz789" and not param == "xyz789":
        return True
    return False
