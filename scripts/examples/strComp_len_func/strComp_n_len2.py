"""Tests behaviour of string matching with different length conditions on both inputs."""
def strComp_n_len_even(param1: str, param2: str) -> bool:
    if (param1 == "Hello world!" and param2 == "Goodbye everyone.") and (len(param1) < len(param2)):
        return True
    return False
