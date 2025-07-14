"""Tests behaviour of in-functions with lower() method."""
def in_func_lower(param: str) -> bool:
    if "TEST123".lower() in param:
        return True
    if "test123" in param.lower():
        return True
    return False
