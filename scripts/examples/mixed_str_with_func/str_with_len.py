"""Tests behaviour when the string starts with a specific prefix, has minimum length, and ends with one of several suffixes."""
def str_with_len(param: str) -> bool:
    if param.startswith(("Config_", "Configuration_")) and len(param) > 32:
        if param.endswith((".py", ".csv", ".txt", ".json", ".java")):
            return True
    return False
