"""Tests behaviour of in-functions with substring at the end."""
def in_func_endswith(param: str) -> bool:
    if param.endswith("127.0.0.1"):
        return True
    return False
