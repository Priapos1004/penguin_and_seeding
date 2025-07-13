"""Tests behaviour when the first parameter equals one of two values using or,
has length modulo 3 equal to 2, and the second parameter is different from a forbidden value
and has length greater than 8."""
def str_comp_n_len(param1: str, param2: str) -> bool:    
    if ((param1 == "Software Engineering 1" or param1 == "Software Engineering 2")
        and len(param1) % 3 == 2) and (param2 != "forbidden" and len(param2) > 8):
        return True
    return False
