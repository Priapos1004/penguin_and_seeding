"""Tests behaviour of in-functions with nested substring conditions."""
def in_func_nested(param: str) -> bool:
    if "hello " in param:
        if "world!" in param:
            if "hello world!" not in param:
                   return True
    return False
