"""Tests behaviour of in-functions with noise functions."""
def in_func_noise(param: str) -> bool:
    if "123456" in param.split("-")[-1] and "test123" in param:
        return True
    return False
