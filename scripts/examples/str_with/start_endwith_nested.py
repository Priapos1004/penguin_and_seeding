"""Tests behaviour when string starts with prefix, and if so, performs further end-check based on suffix."""
def start_endwith_nested(param: str) -> bool:
    if param.startswith("user_id"):
        if param.endswith("_admin"):
            return True
        if param.endswith("_guest"):
            return True
    return False
