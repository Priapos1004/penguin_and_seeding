# 13. if not <param> != "test123"
def test_not_neq(param: str) -> bool:
    if not param != "test123":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_not_neq: {test_not_neq(inp)}")
        print("-" * 40)