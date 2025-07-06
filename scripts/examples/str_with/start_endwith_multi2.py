"""Tests behaviour with mixed start/end checks across with one parameters using both or and nested if-statements."""
def start_endwith_multi2(param: str) -> bool:
    if param.startswith("www.") or param.endswith("./login"):
        if param.endswith(".com") or param.startswith("https://"):
            return True
    return False
