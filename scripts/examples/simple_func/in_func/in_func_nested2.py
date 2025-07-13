"""Tests behaviour of in-functions with complex nested substring conditions using elif-statements."""
def in_func_nested2(param: str) -> bool:
    if "hello " in param:
        if "world!" in param:
            if "hello world!" not in param:
                   return True
    elif "goodbye " in param:
        if "world!" in param:
            return True
    elif "hello again" in param:
        return True
    else:
        if "goodbye again" in param:
            if "123456" in param:
                return True
    return False
