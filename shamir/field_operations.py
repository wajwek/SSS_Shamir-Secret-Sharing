def add(a, b, q):
    return (a + b) % q

def multiply(a, b, q):
    return (a * b) % q

def inverse(a, q):
    if a % q == 0:
        raise ValueError("Zero has no multiplicative inverse")
    return pow(a, -1, q)

def division(a, b, q):
    return (a * inverse(b, q)) % q
