"""Tests behaviour of in-functions with three nested if statements for performance."""
def in_func_perform1(param: str) -> bool:
    if "atest123" in param:
        if "beste456" in param:
            if "coolste789" in param:               
                    return True
    return False
