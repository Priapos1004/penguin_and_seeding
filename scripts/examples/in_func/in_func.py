"""Tests behaviour of in-functions in its standard form."""
def in_func(param: str) -> bool:
    if "test123" in param:
        return True
    return False