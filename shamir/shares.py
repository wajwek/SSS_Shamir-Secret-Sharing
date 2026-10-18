from secrets import randbelow

from shamir.polynomial import evaluate_polynomial

def generate_shares(number_of_shares: int, q: int) -> list[int]:
    if number_of_shares <= 0:
        raise ValueError("Number of shares must be bigger than 0.")

    random_coefficients = [randbelow(q) for _ in range(number_of_shares)]
    return [*random_coefficients]

def calculate_points(arr_of_x, coefficients, q):
    result_arr = []
    for x in arr_of_x:
        y = evaluate_polynomial(coefficients, x, q)
        result_arr.append((x, y))
    return result_arr
