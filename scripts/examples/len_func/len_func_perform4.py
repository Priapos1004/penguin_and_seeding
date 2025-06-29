"""Tests behaviour of len-functions with three parameters in three nested if statements."""
def len_func_perform4(param1: str, param2: str, param3: str) -> bool:
    avg = (len(param1) + len(param2) + len(param3)) / 3
    if len(param2) > avg:
        if len(param1) % 2 == 1:
            if len(param1) < len(param3) < len(param2):
                return True
    return False
