"""Tests behaviour of in-functions with parameter in a list of five strings."""
def in_func_in_list2(param: str) -> bool:
    if param in ["Python", "Kotlin", "MatLab", "JavaScript", "Visual Basic"]:
        return True
    return False
