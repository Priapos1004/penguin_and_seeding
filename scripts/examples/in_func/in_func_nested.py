"""Tests behaviour of in-functions with nested substring conditions."""
def in_func_nested(param: str) -> bool:
    if "test" in param:
        if "123" in param:
            return True
    return False