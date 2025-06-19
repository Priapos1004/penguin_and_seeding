"""Tests behaviour of in-functions with multiple substring conditions."""
def in_func_multi(param: str) -> bool:
    if "test" in param:
        return True
    if "123" in param:
        return True
    return False