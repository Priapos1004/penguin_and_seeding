"""Tests behaviour of in-functions with different substrings in 'and' not in the parameter."""
def in_func_in_and_notin(param: str) -> bool:
    if "foobar" in param and "test123" not in param:
        return True
    return False
