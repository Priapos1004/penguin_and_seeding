"""Tests behaviour of len-functions with two parameters with a while loop."""
def len_func_perform3(param1: str, param2: str) -> bool:
    i = 0
    while ((len(param1) - i) + len(param2)) % 2 == 0:        
        if len(param2) % 3 == 0 and (len(param1) - i) % 5 == 0:
            return True
        i += 1
    return False
