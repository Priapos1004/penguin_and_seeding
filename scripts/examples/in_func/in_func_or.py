"""Tests behaviour of in-functions with multiple substring checks with 'or' logic."""
def in_func_or(param: str) -> bool:
    if "foobar" in param or "test123" in param:
        return True
    return False
