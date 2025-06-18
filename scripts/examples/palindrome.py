def palindrome(text: str) -> bool:
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Remove non-alphanumeric characters and convert to lowercase
    cleaned = ''
    for char in text:
        if char.isalnum():
            cleaned += char

    # At least length of 3 chars
    if len(cleaned) < 3:
        return False

    # Use two-pointer technique to check for palindrome
    left = 0
    right = len(cleaned) - 1

    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1

    return True
