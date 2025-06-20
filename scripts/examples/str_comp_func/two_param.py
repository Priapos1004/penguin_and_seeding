"""Tests behaviour of string comparison functions with two parameters."""
def two_param(param1, param2: str) -> bool:
    if param1 == "test123":
        return True
    if param2 == "abc456":            
        return True
    return False