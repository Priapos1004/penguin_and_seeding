"""Tests behaviour of in-functions with space in substring."""
def in_func_space(param: str) -> bool:
    if "hello world" in param:
        return True
    return False