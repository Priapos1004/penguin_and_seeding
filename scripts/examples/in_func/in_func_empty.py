"""Tests behaviour of in-functions with empty substring."""
def in_func_empty(param: str) -> bool:
    if "" in param:
        return True
    return False