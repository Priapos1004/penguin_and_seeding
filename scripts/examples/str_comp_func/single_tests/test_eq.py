# 1. if <param> == "test123"
def test_eq(param: str) -> bool:    
    if param == "test123":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_eq: {test_eq(inp)}")
        print("-" * 40)