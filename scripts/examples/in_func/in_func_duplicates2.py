"""Tests behaviour of in-functions with two parameters and duplicated tests."""
def in_func_duplicates2(param1: str, param2: str) -> bool:
    if "test123" in param1:
        pass

    if "test" in param2:
        if "test123" in param1:
            pass

    return True
