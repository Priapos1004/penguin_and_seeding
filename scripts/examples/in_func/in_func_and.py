"""Tests behaviour of in-functions with multiple substring checks with 'and' logic."""
def in_func_and(param: str) -> bool:
    if "foo" in param and "bar" in param:
        return True
    return False