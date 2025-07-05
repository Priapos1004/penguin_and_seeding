"""Tests behaviour based on multiple disjunctive conditions involving string equality and length checks."""
def strComp_n_len4(param1: str, param2: str, param3: str) -> bool:    
    if (param1 == "Prime number" or len(param2) == 13) or param3 != "Fibonacci" or len(param3) != 7:        
        return True
    return False
