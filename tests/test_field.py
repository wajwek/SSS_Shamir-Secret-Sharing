import pytest

from shamir.field_operations import division, inverse, multiply


@pytest.mark.parametrize(
    ("a", "q", "expected"),
    [
        (3, 7, 5),
        (5, 7, 3),
        (-3, 7, 2),
    ],
)
def test_inverse_returns_multiplicative_inverse(a, q, expected):
    assert inverse(a, q) == expected
    assert (a * inverse(a, q)) % q == 1


def test_inverse_of_zero_raises_value_error():
    with pytest.raises(ValueError, match="no multiplicative inverse"):
        inverse(0, 7)


def test_inverse_of_zero_residue_raises_value_error():
    with pytest.raises(ValueError, match="no multiplicative inverse"):
        inverse(7, 7)


def test_division_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="no multiplicative inverse"):
        division(4, 0, 7)


def test_division_uses_modular_inverse():
    assert division(4, 3, 7) == 6
    assert multiply(3, division(4, 3, 7), 7) == 4


def test_builtin_pow_raises_for_inverse_of_zero():
    with pytest.raises(ValueError):
        pow(0, -1, 7)


@pytest.mark.parametrize("a", [1, 2, 3, 4, 5, 6])
def test_builtin_pow_inverse_is_correct(a):
    q = 7
    result = pow(a, -1, q)

    assert (a * result) % q == 1
