# 9. added noise with random methods e.g. split
def test_noise(param: str) -> bool: 
    if param == "test123" and param.split("s")[0] == "te":
        return True
    return False

if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")    
        print(f"test_noise: {test_noise(inp)}")
        print("-" * 40)