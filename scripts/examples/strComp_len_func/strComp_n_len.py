"""Tests behaviour when a string matches one a specific value and its length does not exceed length of 30."""
def strComp_n_len(param: str) -> bool:
    if (not param == "Software Engineering 1" and param == "Software Engineering 2") and len(param) < 30:
        return True
    return False
