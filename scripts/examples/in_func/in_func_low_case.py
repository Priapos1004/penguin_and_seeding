"""Tests behaviour of in-functions with lower case characters in substring."""
def in_func_low_case(param: str) -> bool:
    if "TEST123".lower() in param.lower():
        return True
    return False