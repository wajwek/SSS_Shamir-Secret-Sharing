from secrets import randbelow

def generate_coefficients(secret: int, degree: int, q: int) -> list[int]:
    if not 0 <= secret < q:
        raise ValueError("Secret must be in the range [0, q).")
    if degree < 1:
        raise ValueError("Degree must be at least 1.")

    random_coefficients = [randbelow(q) for _ in range(degree)]
    return [*random_coefficients, secret]

# coefficients are in order from a_n (next to the x with the highest power) to a_0

def evaluate_polynomial(coefficients, x, q):
    result = 0
    for coefficient in coefficients:
        result = (result * x + coefficient) % q
    return result


        