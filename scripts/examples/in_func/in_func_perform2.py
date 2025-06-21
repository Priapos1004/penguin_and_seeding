"""Tests behaviour of in-functions with five nested if statements for performance."""
def in_func_perform2(param: str) -> bool:
    if "Hey pynguin," in param:
        if "can you" in param:
            if "find the" in param:      
                if "full coverage" in param:       
                    if "for this test?" in param:
                        return True                      
    return False
