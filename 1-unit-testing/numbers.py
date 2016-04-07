"""Basic numerical operations.
"""


def is_odd(n):
    """Returns True if n is odd, else False.
    """
    return n % 2 == 1


def is_prime(n):
    """Returns True if n is prime, else False.
    """
    if n < 2 or n % 2 == 0:
        return False
    if n == 2:
        return True
    max_ = n**0.5
    i = 3
    while i <= max_:
        if n % i == 0:
            return False
        i += 2
    return True
