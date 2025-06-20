"""Tests behaviour of seeding strategies with contradicting string comparisons."""
def contradiction(param: str) -> bool:
    if param == "arbok" and param == "kobra":
        return True
    return False