# 8. two if-statements
def test_two_ifs(param: str) -> bool:
    if param == "test123":
        return True
    if param == "test123.2.0":            
        return False
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_two_ifs: {test_two_ifs(inp)}")        
        print("-" * 40)