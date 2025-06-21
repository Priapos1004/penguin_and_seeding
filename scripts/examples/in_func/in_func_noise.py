"""Tests behaviour of in-functions with noise functions."""
def in_func_noise(param: str) -> bool:
    if "test123" in param.lower():
        return True
    return False
