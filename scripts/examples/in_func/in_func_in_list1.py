"""Tests behaviour of in-functions with parameter in a list of two strings."""
def in_func_in_list1(param: str) -> bool:
    if param in ["Fuzzingbook", "Pynguin"]:
        return True
    return False
