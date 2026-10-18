"""Działania w ciele skończonym modulo liczby pierwszej."""

# TODO: Zaimplementować działania modularne, w szczególności odwrotność.

def add(a, b, q):
    return (a + b) % q

def minus(a, b, q):
    return wrap(a - b) % q

def wrap(a, q):
    while a < 0:
        a += q
    return a

def multiply(a, b, q):
    return (a * b) % q

def inverse(a, q):
    if a % q == 0:
        raise ValueError("Zero has no multiplicative inverse")
    return pow(a, -1, q)

def division(a, b, q):
    return (a * inverse(b, q)) % q
