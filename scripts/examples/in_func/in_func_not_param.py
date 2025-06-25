"""Tests behaviour of in-functions with negation of substring in parameter."""
def in_func_not_param(param: str) -> bool:
    if not "forbidden" in param: # noqa: E713
        return True
    return False
