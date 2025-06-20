"""Tests behaviour of string comparison functions with two if-statements."""
def two_ifs(param: str) -> bool:
    if param == "test123":
        return True
    if param == "test123.2.0":            
        return True
    return False