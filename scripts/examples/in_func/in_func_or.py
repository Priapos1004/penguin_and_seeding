"""Tests behaviour of in-functions with multiple substring checks with 'or' logic."""
def in_func_or(param: str) -> bool:
    if "foo" in param or "bar" in param:
        return True
    return False