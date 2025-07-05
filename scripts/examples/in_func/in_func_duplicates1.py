"""Tests behaviour of in-functions with one parameter and duplicated tests."""
def in_func_duplicates1(param1: str, param2: str) -> bool:
    if "test123" in param1:
        pass

    if "test123" in param1:
        pass

    return True
