"""Tests behaviour of string comparison functions with negation and reversed order of parameter and value."""
def neq_rev(param: str) -> bool:
    if "forbidden" != param:
        return True
    return False