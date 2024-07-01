def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(p):
    """Return the next prime number after the given prime p."""
    if not is_prime(p):
        raise ValueError(f"The input number {p} is not a prime number.")
    
    next_candidate = p + 1
    while not is_prime(next_candidate):
        next_candidate += 1
    return next_candidate

# Example usage
r = 23
next_p = next_prime(r)
print(next_p)  # Output: 7
