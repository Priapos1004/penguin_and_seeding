"""Tests behaviour of in-functions with substring at the start."""
def startswith(param: str) -> bool:
    if param.startswith("ABCtest"):
        return True
    return False