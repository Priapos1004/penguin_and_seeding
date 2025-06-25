"""Tests behaviour of len-functions with parameter length being a prime number (up to 20)."""
def len_func_is_prime(param: str) -> bool:
    prime_list = {2, 3, 5, 7, 11, 13, 17, 19}
    if len(param) in prime_list:
        return True
    return False
