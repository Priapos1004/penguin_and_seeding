"""Tests behaviour of string comparison functions with concatenation of two parameters and dependency."""
def three_param_concat(param1, param2, param3: str) -> bool:
    if param1 == "test123":
        if param2 == "abc456":
            if param3 == param2 + param1:
                return True
    return False