"""Tests behaviour of string comparison functions with 'or' operator."""
def eq_or(param: str) -> bool:    
    if param == "hello" or param == "world":
        return True
    return False