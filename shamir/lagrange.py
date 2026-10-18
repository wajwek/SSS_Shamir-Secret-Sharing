from shamir.field_operations import inverse

Point = tuple[int, int]

def interpolate(points: list[Point], x: int, q: int) -> int:
    
    if not points:
        raise ValueError("At least one point is required.")

    x_values = [point[0] for point in points]
    if len(set(x_values)) != len(x_values):
        raise ValueError("Points must have distinct x coordinates.")

    result = 0
    for index, (x_i, y_i) in enumerate(points):
        basis = y_i
        for other_index, (x_j, _) in enumerate(points):
            if index == other_index:
                continue
            numerator = (x - x_j) % q
            denominator = (x_i - x_j) % q
            basis = basis * numerator * inverse(denominator, q) % q
        result = (result + basis) % q

    return result

def reconstruct_secret(points: list[Point], degree: int, q: int) -> int:
    if degree < 0:
        raise ValueError("Degree must be non-negative.")
    if len(points) < degree + 1:
        raise ValueError(
            f"At least {degree + 1} shares are required for degree {degree}."
        )

    return interpolate(points, x=0, q=q)
