"""Tests behaviour of in-functions with nested substring conditions."""
def in_func_nested(param: str) -> bool:
    if "test_xzy" in param:
        if "abc123" in param:
            return True
    return False
