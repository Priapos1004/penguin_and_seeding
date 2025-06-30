"""Tests behaviour of len-functions with two parameters with a for loop."""
def len_func_perform2(param1: str, param2: str) -> bool:
    for i in range(len(param1)):        
        if len(param2)  - i > 6 and len(param1) > 6:
            return True
    return False
