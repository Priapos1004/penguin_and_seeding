"""Tests behaviour with mixed start/end checks across two parameters using both or and nested if-statements."""
def start_endwith_multi(param1: str, param2: str) -> bool:
    if param1.startswith("wwww.") or param2.endswith("./login"):
        if param1.endswith(".com") and param2.startswith("https://"):
            return True
    return False
