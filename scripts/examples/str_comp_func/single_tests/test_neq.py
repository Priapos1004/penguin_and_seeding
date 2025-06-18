# 10. if <param> != "forbidden"
def test_neq(param: str) -> bool:
    if param != "forbidden":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_neq: {test_neq(inp)}")
        print("-" * 40)