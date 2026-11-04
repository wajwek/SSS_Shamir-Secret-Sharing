import pytest

from shamir.shares import calculate_points, generate_shares


def test_generate_shares_returns_requested_number_of_unique_nonzero_x_values(
    monkeypatch,
):
    generated_values = iter([0, 2, 2, 4, 7])
    monkeypatch.setattr(
        "shamir.shares.randbelow",
        lambda q: next(generated_values),
    )

    assert generate_shares(number_of_shares=3, q=17) == [1, 3, 5]


def test_generate_shares_rejects_non_positive_number():
    with pytest.raises(ValueError, match="Number of shares must be bigger than 0"):
        generate_shares(number_of_shares=0, q=17)


def test_generate_shares_rejects_more_values_than_nonzero_field_elements():
    with pytest.raises(ValueError, match="smaller than q"):
        generate_shares(number_of_shares=17, q=17)


def test_calculate_points_returns_x_and_y_pairs():
    coefficients = [3, 7, 5]

    assert calculate_points([1, 2, 3, 4, 5], coefficients, q=17) == [
        (1, 15),
        (2, 14),
        (3, 2),
        (4, 13),
        (5, 13),
    ]
