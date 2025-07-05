"""Tests behaviour based on disjunctive and nested conditions involving string equality and length constraints."""
def strComp_n_len4(param1: str, param2: str, param3: str) -> bool:    
    if param1 == "Prime number" or len(param2) == 17:
        if param3 == "Fibonacci" or len(param3) != 11:
            if param2 == "Euler's number" or len(param1) > 23:                        
                return True
    return False
