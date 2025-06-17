# 5. contradiction
def test_contradiction(param: str) -> bool:
    if param == "arbok" and param == "kobra":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_contradiction: {test_contradiction(inp)}")
        print("-" * 40)