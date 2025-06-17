# tests based on string comparisons with boolean return values
# one input parameter <param> of type str

# 1. if <param> == "test123"
def test_eq(param: str) -> bool:    
    if param == "test123":
        return True
    return False

# 2. if "test123" == <param>
def test_eq_rev(param: str) -> bool:    
    if "test123" == param:
        return True
    return False

# 3. if "test123"       == <param>  (extra spaces)
def test_eq_spaces(param: str) -> bool:    
    if "test123"       == param:
        return True
    return False

# 4. if "test123"==<param>  (no spaces)
def test_eq_no_spaces(param: str) -> bool:    
    if "test123"==param:
        return True
    return False

# 5. contradiction
def test_contradiction(param: str) -> bool:
    if param == "arbok" and param == "kobra":
        return True
    return False

# 6. if <param> == "hello" or <param> == "world"
def test_eq_or(param: str) -> bool:    
    if param == "hello" or param == "world":
        return True
    return False

# 7. nested if-statements
def test_nested_if(param: str) -> bool:
    if param == "test123":
        if param == "abrakadabra":
            return True
    return False

# 8. two if-statements
def test_two_ifs(param: str) -> bool:
    if param == "test123":
        return True
    if param == "test123.2.0":            
        return False
    return False

# 9. added noise with random methods e.g. split
def test_noise(param: str) -> bool: 
    if param == "test123" and param.split("s")[0] == "te":
        return True
    return False

# 10. if <param> != "forbidden"
def test_neq(param: str) -> bool:
    if param != "forbidden":
        return True
    return False

# 11. if "forbidden" != <param>
def test_neq_rev(param: str) -> bool:
    if "forbidden" != param:
        return True
    return False

# 12. if not <param> == "test123"
def test_not_eq(param: str) -> bool:
    if not param == "test123":
        return True
    return False

# 13. if not <param> != "test123"
def test_not_neq(param: str) -> bool:
    if not param != "test123":
        return True
    return False

# 14. always true condition
def test_taut(param: str) -> bool:    
    if param == "xyz" or not param == "xyz":
        return True
    return False

# 15. non SATisfiable condition
def test_oxy(param: str) -> bool:    
    if param == "xyz" and not param == "xyz":
        return True
    return False

# main function to run tests 
if __name__ == "__main__":
    test_inputs = ["test123", "xyz", "arbok", "forbidden", "test123.2.0", "abrakadabra", "te.st123", "", "$%$&!*()", "hello", "world"]

    for inp in test_inputs:
        print(f"Testing input: {inp}")
        print(f"test_eq: {test_eq(inp)}")
        print(f"test_eq_rev: {test_eq_rev(inp)}")
        print(f"test_eq_spaces: {test_eq_spaces(inp)}")
        print(f"test_eq_no_spaces: {test_eq_no_spaces(inp)}")
        print(f"test_contradiction: {test_contradiction(inp)}")
        print(f"test_eq_or: {test_eq_or(inp)}")
        print(f"test_nested_if: {test_nested_if(inp)}")
        print(f"test_two_ifs: {test_two_ifs(inp)}")        
        print(f"test_noise: {test_noise(inp)}")
        print(f"test_neq: {test_neq(inp)}")
        print(f"test_neq_rev: {test_neq_rev(inp)}")
        print(f"test_not_eq: {test_not_eq(inp)}")
        print(f"test_not_neq: {test_not_neq(inp)}")
        print(f"test_taut: {test_taut(inp)}")
        print(f"test_oxy: {test_oxy(inp)}")
        print("-" * 40)
