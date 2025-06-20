"""Tests behaviour of string comparison functions with concatenation of two parameters."""
def three_param(param1, param2, param3: str) -> bool:
    if param1 == "test123":
        if param2 == "abc456":
            if param3 == "xyz789":
                return True
    return False