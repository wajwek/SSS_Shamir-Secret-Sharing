from random import SystemRandom
from secrets import randbelow

from shamir.lagrange import reconstruct_secret
from shamir.parameters import NUMBER_OF_SHARES, POLYNOMIAL_DEGREE, Q
from shamir.polynomial import generate_coefficients
from shamir.shares import calculate_points, generate_shares

secure_random = SystemRandom()


def main() -> None:
    secret = randbelow(Q)
    coefficients = generate_coefficients(
        secret=secret,
        degree=POLYNOMIAL_DEGREE,
        q=Q,
    )
    x_values = generate_shares(NUMBER_OF_SHARES, Q)
    shares = calculate_points(x_values, coefficients, Q)
    selected_shares = secure_random.sample(
        shares,
        POLYNOMIAL_DEGREE + 1,
    )
    reconstructed_secret = reconstruct_secret(
        selected_shares,
        degree=POLYNOMIAL_DEGREE,
        q=Q,
    )

    print("=== Shamir Secret Sharing: 3-of-5 demonstration ===")
    print(f"Q = {Q}")
    print(f"Number of shares = {NUMBER_OF_SHARES}")
    print(f"Polynomial degree = {POLYNOMIAL_DEGREE}")
    print(f"Randomly generated secret = {secret}")
    print(f"Coefficients [a2, a1, a0] = {coefficients}")
    print()
    print("Calculated random shares:")
    for x, y in shares:
        print(f"  x = {x}: y = f({x}) = {y} (mod {Q}) -> ({x}, {y})")
    print()
    print(f"Randomly selected shares for reconstruction: {selected_shares}")
    print(f"Original secret: {secret}")
    print(f"Reconstructed secret: {reconstructed_secret}")
    print(f"Result is correct: {reconstructed_secret == secret}")

    if reconstructed_secret != secret:
        raise RuntimeError("Secret reconstruction failed.")


if __name__ == "__main__":
    main()
