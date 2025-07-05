"""Tests behaviour of in-functions with multiple nested substring checks and 'or' logic."""
def in_func_or2(param: str) -> bool:
    if "foobar" in param or "test123" in param:
        if "666666" in param:
            return True
    return False
