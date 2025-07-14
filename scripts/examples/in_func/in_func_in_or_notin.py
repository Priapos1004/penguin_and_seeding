"""Tests behaviour of in-functions with different substrings in 'or' not in the parameter."""
def in_func_in_or_notin(param: str) -> bool:
    if "foobar" in param or "test123" not in param:
        return True
    return False
