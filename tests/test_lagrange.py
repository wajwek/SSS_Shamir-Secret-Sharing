import pytest

from shamir.lagrange import interpolate, reconstruct_secret


POINTS = [(1, 15), (2, 14), (3, 2)]


def test_interpolate_evaluates_polynomial_at_requested_x():
    assert interpolate(POINTS, x=4, q=17) == 13


def test_reconstruct_secret_returns_constant_term():
    assert reconstruct_secret(POINTS, degree=2, q=17) == 5


def test_reconstruct_secret_accepts_more_than_three_shares():
    points = [(1, 15), (2, 14), (3, 2), (4, 13), (5, 13)]

    assert reconstruct_secret(points, degree=2, q=17) == 5


def test_reconstruct_secret_requires_three_shares():
    with pytest.raises(ValueError, match="At least 3 shares are required"):
        reconstruct_secret(POINTS[:2], degree=2, q=17)


def test_reconstruct_secret_requires_degree_plus_one_shares():
    points = [(1, 6), (2, 9), (3, 14), (4, 4)]

    with pytest.raises(ValueError, match="At least 4 shares are required"):
        reconstruct_secret(points[:3], degree=3, q=17)


def test_reconstruct_secret_accepts_degree_plus_one_shares():
    points = [(1, 6), (2, 9), (3, 14), (4, 4)]

    assert reconstruct_secret(points, degree=3, q=17) == 5


def test_interpolate_rejects_duplicate_x_coordinates():
    with pytest.raises(ValueError, match="distinct x coordinates"):
        interpolate([(1, 15), (1, 14), (3, 2)], x=0, q=17)
