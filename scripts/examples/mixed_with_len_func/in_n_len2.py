"""Tests behaviour of substring matching with different length conditions on both inputs."""
def strComp_n_len3(param1: str, param2: str) -> bool:
    if ("Hello world and universe!" in param1 and "Goodbye everyone." in param2) and (len(param1) < len(param2)):
        return True
    return False
