# 6. if <param> == "hello" or <param> == "world"
def test_eq_or(param: str) -> bool:    
    if param == "hello" or param == "world":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_eq_or: {test_eq_or(inp)}")
        print("-" * 40)