
# Shamir Secret Sharing (SSS)

A Python implementation of **Shamir's Secret Sharing (SSS)**, focusing on polynomial-based secret splitting and reconstruction over finite fields.

The project explores the mathematical foundations of threshold cryptography, with a practical demonstration of splitting and recovering an ECDSA private key.

## Overview

Shamir's Secret Sharing is a cryptographic algorithm that divides a secret into multiple shares. A predefined minimum number of shares is required to reconstruct the original secret.

This project focuses on a **(3, 5) threshold scheme**:

- A secret is used as the constant term of a randomly generated polynomial of degree at most 2.
- Five shares are created by evaluating the polynomial at distinct, non-zero points.
- Any three shares can reconstruct the original secret using Lagrange interpolation.
- Two or fewer shares are insufficient to uniquely determine the secret.

All polynomial operations are performed over a finite field to ensure mathematically exact computations.

## Project Goals

The implementation is developed from scratch to explore the underlying mathematics rather than relying on an existing SSS library.

The main goals are:

1. Implement modular arithmetic, including modular inverses.
2. Generate random polynomials over finite fields.
3. Generate secret shares using polynomial evaluation.
4. Implement Lagrange interpolation using basis polynomials.
5. Reconstruct the secret from a minimum number of shares.
6. Verify the implementation through unit tests.
7. Integrate the algorithm with ECDSA using the NIST P-256 curve.
8. Demonstrate signing and verifying a message with a reconstructed private key.

## Project Structure

```text
.
├── shamir/
│   ├── __init__.py
│   ├── parameters.py
│   ├── field.py
│   ├── polynomial.py
│   ├── shares.py
│   ├── lagrange.py
│   ├── validation.py
│   └── models.py
├── tests/
│   ├── test_field.py
│   ├── test_polynomial.py
│   ├── test_shares.py
│   ├── test_lagrange.py
│   └── test_validation.py
├── demos/
│   ├── basic_sss.py
│   └── ecdsa_demo.py
├── README.md
├── pyproject.toml
└── .gitignore
```

### Core Modules

| Module | Purpose |
|--------|---------|
| `parameters.py` | Finite field parameters and elliptic curve constants |
| `field.py` | Modular arithmetic and modular inverses |
| `polynomial.py` | Polynomial generation and evaluation |
| `shares.py` | Secret splitting and share generation |
| `lagrange.py` | Lagrange interpolation and secret reconstruction |
| `validation.py` | Input and share validation |
| `models.py` | Data structures for representing shares |

## Mathematical Background

For a threshold scheme requiring three shares, the secret is embedded in a polynomial:

\[
f(x) = s + a_1x + a_2x^2 \pmod q
\]

where:

- \(s\) is the original secret.
- \(a_1, a_2\) are randomly generated coefficients.
- \(q\) is a prime defining the finite field.

Each share consists of a point:

\[
(x_i, f(x_i))
\]

The original secret is recovered by evaluating the interpolated polynomial at \(x = 0\):

\[
s = f(0) = \sum_{i=1}^{3} y_i
\prod_{\substack{j=1 \\ j \ne i}}^{3}
\frac{-x_j}{x_i-x_j} \pmod q
\]

Division in the finite field is performed using modular inverses.

## ECDSA Integration

The final demonstration will use the reconstructed secret as an ECDSA private key.

The workflow will include:

1. Generating an ECDSA private key using the P-256 curve.
2. Splitting the private scalar into five shares.
3. Selecting three shares to reconstruct the scalar.
4. Recreating the corresponding ECDSA private key.
5. Signing a test message.
6. Verifying the signature using the original public key.

The secret sharing operations will use the prime order of the P-256 base point as their finite field modulus.

**Note:** This implementation reconstructs the private key before signing. It is not a distributed threshold ECDSA signing protocol.

## Development

The project is being implemented incrementally, with each mathematical component developed and tested separately.

**Current status:** Educational development and experimentation.

The code is intended for learning, testing, and demonstrating cryptographic concepts. It has not been independently audited and should not be used to protect production secrets.

## Technologies

- Python 3.11+
- pytest
- cryptography (ECDSA integration)
