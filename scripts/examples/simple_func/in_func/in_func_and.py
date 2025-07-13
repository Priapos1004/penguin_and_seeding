"""Tests behaviour of in-functions with multiple substring checks with 'and' logic."""
def in_func_and(param: str) -> bool:
    if "foobar" in param and "test123" in param:
        return True
    return False
