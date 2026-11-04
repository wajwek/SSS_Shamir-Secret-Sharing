from secrets import randbelow

from shamir.polynomial import evaluate_polynomial

def generate_shares(number_of_shares: int, q: int) -> list[int]:
    if number_of_shares <= 0:
        raise ValueError("Number of shares must be bigger than 0.")
    if number_of_shares > q - 1:
        raise ValueError("Number of shares must be smaller than q.")

    x_values: set[int] = set()
    while len(x_values) < number_of_shares:
        x_values.add(randbelow(q - 1) + 1)
    return list(x_values)

def calculate_points(
    x_values: list[int], coefficients: list[int], q: int
) -> list[tuple[int, int]]:
    return [(x, evaluate_polynomial(coefficients, x, q)) for x in x_values]
