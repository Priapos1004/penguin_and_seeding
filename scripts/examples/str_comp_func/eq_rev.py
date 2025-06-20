"""Tests behaviour of string comparison functions with reversed order of parameter and value."""
def eq_rev(param: str) -> bool:    
    if "test123" == param:
        return True
    return False