import pytest

from shamir.polynomial import evaluate_polynomial, generate_coefficients


def test_generate_coefficients_keeps_secret_as_constant_term(monkeypatch):
    generated_values = iter([3, 7])
    monkeypatch.setattr(
        "shamir.polynomial.randbelow",
        lambda q: next(generated_values),
    )

    assert generate_coefficients(secret=5, degree=2, q=17) == [3, 7, 5]


def test_generate_coefficients_rejects_secret_outside_field():
    with pytest.raises(ValueError, match=r"Secret must be in the range \[0, q\)"):
        generate_coefficients(secret=17, degree=2, q=17)


def test_generate_coefficients_rejects_non_positive_degree():
    with pytest.raises(ValueError, match="Degree must be at least 1"):
        generate_coefficients(secret=5, degree=0, q=17)


def test_evaluate_polynomial_returns_value_modulo_q():
    coefficients = [3, 7, 5]

    assert evaluate_polynomial(coefficients, x=2, q=17) == 14


def test_evaluate_polynomial_returns_secret_for_x_zero():
    assert evaluate_polynomial([3, 7, 5], x=0, q=17) == 5
