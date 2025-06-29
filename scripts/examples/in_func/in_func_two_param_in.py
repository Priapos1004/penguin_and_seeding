"""Tests behaviour of in-functions with two parameter as substring of one fixed string."""
def in_func_two_param_in(param1: str, param2: str) -> bool:
    if param1 in "The fuzzingbook":
        return True
    if param2 in "The fuzzingbook":
        return True
    return False
