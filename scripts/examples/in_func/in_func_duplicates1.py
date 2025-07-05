"""Tests behaviour of in-functions with one parameter and duplicated tests."""
def in_func_duplicates1(param: str) -> bool:
    if "test123" in param:
        pass

    if "test123" in param:
        pass

    return True
