"""Tests behaviour of len-functions with three parameters in six nested if statements."""
def len_func_perform5(param1: str, param2: str, param3: str) -> bool:
    if (len(param1) + len(param2) + len(param3)) % 3 == 0:
        if (len(param1) + len(param2))  > (len(param2) + len(param3)):
            if (len(param1) + len(param2))  > (len(param3) + len(param1)):                
                if len(param2) % 2 == 0:
                    if len(param3) % 2 == 1:          
                        return True
    return False
    