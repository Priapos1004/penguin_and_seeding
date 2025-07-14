"""Tests behaviour when a substring matches a specific value and its length exceeds 10."""
def in_n_len(param: str) -> bool:
    if (not param in "Software Engineering 1" and param in "Software Engineering 123") and len(param) > 10:  # noqa: E713
        return True
    return False
