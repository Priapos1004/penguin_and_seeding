def palindrome(text: str) -> bool:
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = ''
    for char in text:
        if char.isalnum():
            cleaned += char.lower()

    # Use two-pointer technique to check for palindrome
    left = 0
    right = len(cleaned) - 1

    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1

    return True

if __name__ == "__main__":
    # Example usage
    test_strings = [
        "",
        "Racecar",
        "Was it a car or a cat I saw?",
        "No 'x' in Nixon",
        "Hello, World!",
    ]
    for s in test_strings:
        result = palindrome(s)
        print(f'"{s}" is a palindrome: {result}')
