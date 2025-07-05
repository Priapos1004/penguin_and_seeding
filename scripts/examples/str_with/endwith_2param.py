"""Tests behaviour when first parameter ends with '.json' or second parameter ends with '.html'."""
def endwith_2param(param1: str, param2: str) -> bool:
    if param1.endswith(".json"):
        return True
    elif param2.endswith(".html"):
        return True
    return False
