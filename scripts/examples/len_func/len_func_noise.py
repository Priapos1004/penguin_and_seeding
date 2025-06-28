"""Tests behaviour of len-functions with parameter length divisible by 6 and starts with uppercase letter."""
def len_func_noise(param: str) -> bool:
    if len(param) % 6 == 0 and param[:1].isupper():
        return True
    return False
