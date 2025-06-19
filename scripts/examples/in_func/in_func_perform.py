"""Tests behaviour of in-functions with multi nested if statements for performance."""
def in_func_perform(param: str) -> bool:
    if "a" in param:
        if "b" in param:
            if "c" in param:
                if "123" in param:
                    return True
    return False