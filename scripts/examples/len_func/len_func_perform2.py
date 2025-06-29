"""Tests behaviour of len-functions with two parameters with a for loop."""
def len_func_perform2(param1: str, param2: str) -> bool:
    len1 = len(param1)
    len2 = len(param2)  
    for i in range(len1):        
        if len2 - i > 6 and len1 > 6:
            return True
    return False
