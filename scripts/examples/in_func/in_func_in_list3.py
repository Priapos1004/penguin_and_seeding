"""Tests behaviour of in-functions nested if-statements, list membership and substring checks."""
def in_func_in_list3(param: str) -> bool:
    if param in ["Bumblebee", "Optimus Prime", "Megatron"]:
        if "Mega" not in param or "Prime" in param:
            return True
    if param in ["Autobots", "Decepticons"]:
        if "bot" in param:
            if param in ["Autobots"]:
                return True
    return False
