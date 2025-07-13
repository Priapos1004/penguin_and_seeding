"""Tests behaviour of in-functions with multiple substring conditions."""
def in_func_multi(param: str) -> bool:
    if "test_xzy" in param:
        return True
    if "abc123" in param:
        return True
    return False
