# 11. if "forbidden" != <param>
def test_neq_rev(param: str) -> bool:
    if "forbidden" != param:
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_neq_rev: {test_neq_rev(inp)}")
        print("-" * 40)