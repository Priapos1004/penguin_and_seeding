"""Tests behaviour of in-functions with two parameters and complex duplicated tests."""
def in_func_duplicates3(param1: str, param2: str) -> bool:
    if "test123" in param1:
        pass

    if "test" in param2:
        if "test123" in param1:
            pass

    if "test123" in param1:
        if "" in param2:
            pass

    return True
