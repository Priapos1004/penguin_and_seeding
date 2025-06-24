"""Tests behaviour of in-functions with multiple nested if statements with two parameters for performance."""
def in_func_perform4(param1, param2: str) -> bool:
    if "Hey pynguin," in param1:
        if "can you" in param2:
            if "find the" in param1:      
                if "full coverage" in param2:       
                    if "for this test?" in param1:
                        return True                      
    return False
