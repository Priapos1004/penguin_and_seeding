"""Tests behaviour of in-functions with noise functions out of scope."""
def in_func_noise_outscope(param: str) -> bool:
    if "ABCtest" in param.strip().lower() and "123456" in param.split("-")[-1]:
        return True
    return False
