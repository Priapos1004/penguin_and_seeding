"""Tests behaviour of seeding strategies with contradicting string comparisons."""
def contradiction(param: str) -> bool:
    if param == "rettan" and param == "natter":
        return True
    return False
