def contains_pattern(s: str) -> bool:
    if "#" in s:
        if s.count("$") == 2:
            return True
    return False
