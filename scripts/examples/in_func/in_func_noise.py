"""Tests behaviour of in-functions with noise functions."""
def in_func_noise(param: str) -> bool:
    if "test" in param.strip().lower() and "123" in param.split("-")[-1]:
        return True
    return False