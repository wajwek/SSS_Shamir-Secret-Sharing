from secrets import randbelow

def generate_coefficients(secret: int, degree: int, q: int) -> list[int]:
    if not 0 <= secret < q:
        raise ValueError("Secret must be in the range [0, q).")
    if degree < 1:
        raise ValueError("Degree must be at least 1.")

    if q < 2:
        raise ValueError("Field modulus must be at least 2.")

    leading_coefficient = randbelow(q - 1) + 1
    random_coefficients = [leading_coefficient] + [
        randbelow(q) for _ in range(degree - 1)
    ]
    return [*random_coefficients, secret]

def evaluate_polynomial(coefficients: list[int], x: int, q: int) -> int:
    """Evaluate descending coefficients [a_n, ..., a_0] using Horner's method."""
    result = 0
    for coefficient in coefficients:
        result = (result * x + coefficient) % q
    return result
