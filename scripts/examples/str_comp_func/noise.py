"""Tests behaviour of string comparison functions with functions not supported by the custom seeding as noise."""
def noise(param: str) -> bool: 
    if param.split("s")[0] == "te" and param == "test123":
        return True
    return False