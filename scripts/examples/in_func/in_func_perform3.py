"""Tests behaviour of in-functions with ten nested if statements for performance."""
def in_func_perform3(param: str) -> bool:
    if "simple" in param:
        if "waffle" in param:
            if "recipe:" in param:      
                if "flour 2cup" in param:       
                    if "baking powder 2tsp" in param:
                        if "salt 0.5tsp" in param:
                            if "sugar 1tsp" in param:
                                if "egg 1" in param:
                                    if "milk 1cup" in param:
                                        if "vanilla 1tsp" in param:                                            
                                            return True                      
    return False
