"""Tests behaviour of string comparison functions with two parameters in reverse order."""
def two_param_rev(param1, param2: str) -> bool:
    if "abc456" == param2:
        return True
    if "test123" == param1:            
        return True
    return False