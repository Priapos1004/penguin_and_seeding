# 7. nested if-statements
def test_nested_if(param: str) -> bool:
    if param == "test123":
        if param == "abrakadabra":
            return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_nested_if: {test_nested_if(inp)}")
        print("-" * 40)