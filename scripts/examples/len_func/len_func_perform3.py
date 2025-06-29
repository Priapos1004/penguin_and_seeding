"""Tests behaviour of len-functions with two parameters with a while loop."""
def len_func_perform3(param1: str, param2: str) -> bool:
    len1 = len(param1)
    len2 = len(param2)  
    while (len1 + len2) % 2 == 0:        
        if len2 % 3 == 0 and len1 % 5 == 0:
            return True
        len1 -= 1
    return False
