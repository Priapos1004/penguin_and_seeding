"""Tests behaviour of in-functions with special characters in substring."""
def in_func_sp_chars(param: str) -> bool:
    if "@#$%()!" in param:
        return True
    return False