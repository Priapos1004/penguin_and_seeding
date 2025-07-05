"""Tests behaviour when string starts with 'log_file', ends with '.txt', and contains 'name' in between."""
def str_with_in(param: str) -> bool:
    if param.startswith("log_file"):
        if param.endswith(".txt"):
            if "name" in param[5:-5]:  
                return True
    return False
