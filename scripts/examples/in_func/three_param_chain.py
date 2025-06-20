"""Tests behaviour a chained 'in'-relationship between three parameters, starting with a fixed substring."""
def three_param_chain(param1, param2, param3: str) -> bool:
    if "test123" in param1:
        if param1 in param2:
            if param2 in param3:
                return True        
    return False
