# 14. always true condition
def test_taut(param: str) -> bool:    
    if param == "xyz" or not param == "xyz":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_taut: {test_taut(inp)}")
        print("-" * 40)