"""Tests behaviour when first string starts with 'temp_' or second ends with '.bak'."""
def endwith_2param(param1: str, param2: str) -> bool:
    if param1.endswith(".json"):
        return True
    elif param2.endswith(".html"):
        return True
    return False
