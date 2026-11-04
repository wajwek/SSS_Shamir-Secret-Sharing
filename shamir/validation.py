from itertools import combinations
from random import sample

from shamir.lagrange import Point, reconstruct_secret
from shamir.parameters import NUMBER_OF_SHARES, POLYNOMIAL_DEGREE, Q

POLYNOMIAL_COEFFICIENTS: list[int] = [3, 7, 5]
SECRET = POLYNOMIAL_COEFFICIENTS[-1]
SHARES: list[Point] = [
    (1, 15),
    (2, 14),
    (3, 2),
    (4, 13),
    (5, 13),
]


def can_reconstruct_secret(
    points: list[Point],
    secret: int,
    degree: int = POLYNOMIAL_DEGREE,
    q: int = Q,
) -> bool:
    """Return whether the supplied shares reconstruct the expected secret."""
    if len(points) < degree + 1:
        return False

    return reconstruct_secret(points, degree=degree, q=q) == secret


def validate_example() -> int:
    """Reconstruct the secret from three randomly selected shares."""
    selected_shares = sample(SHARES, POLYNOMIAL_DEGREE + 1)
    reconstructed_secret = reconstruct_secret(
        selected_shares,
        degree=POLYNOMIAL_DEGREE,
        q=Q,
    )
    print(f"Secret = {SECRET}")
    print(f"Reconstructed secret = {reconstructed_secret}")
    return reconstructed_secret


def all_share_combinations() -> list[tuple[Point, ...]]:
    """Return every valid combination of shares for the configured scheme."""
    return [
        combination
        for number_of_shares in range(
            POLYNOMIAL_DEGREE + 1,
            NUMBER_OF_SHARES + 1,
        )
        for combination in combinations(SHARES, number_of_shares)
    ]
