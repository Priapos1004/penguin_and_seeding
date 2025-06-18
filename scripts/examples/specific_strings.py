def check_login(token: str) -> bool:
    if "admin" in token:
        if token.startswith("auth_"):
            if token.endswith("_secure"):
                return True
    return False
