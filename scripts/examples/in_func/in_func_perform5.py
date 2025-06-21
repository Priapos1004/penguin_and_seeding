"""Tests behaviour of in-functions with multiple nested if statements with three depend parameters and some negation in substring for performance."""
def in_func_perform5(param1, param2, param3: str) -> bool:
    if "Hey pynguin," in param1:
        if "can you" in param2:
            if "find the" in param3:      
                if "full coverage" not in param1:       
                    if "for this test?" not in param2:
                        if "fuzzing book" in param3:
                            return True                                           
    return False
