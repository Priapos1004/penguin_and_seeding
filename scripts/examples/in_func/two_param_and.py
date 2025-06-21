"""Tests behaviour of in-functions with two parameters checks with 'and' logic."""
def two_param_and(param1, param2: str) -> bool:
    if "foobar" in param1 and "test123" in param2:
        return True
    return False
