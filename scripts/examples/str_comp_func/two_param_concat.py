"""Tests behaviour of string comparison functions with concatenation of two parameters."""
def two_param_concat(param1: str, param2: str, param3: str) -> bool:
    if "hello world" == param2 + param1:
        return True
    return False
