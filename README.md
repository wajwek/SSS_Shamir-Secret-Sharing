
# Shamir Secret Sharing (SSS)

Educational Python implementation of Shamir's Secret Sharing over a finite
field. The configured scheme is **3-of-5**: a secret is the constant term of a
random quadratic polynomial, five shares are generated, and any three shares
recover the secret with Lagrange interpolation.

The repository also contains an ECDSA demonstration using the NIST P-256
curve. It reconstructs the private scalar before signing; it is **not** a
distributed threshold-signature implementation.

## Requirements

- Python 3.11 or newer
- `cryptography` for the ECDSA demonstration
- `pytest` for the test suite

## Setup

Create and activate a virtual environment, then install the project with its
development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows PowerShell, activate the environment with
`.venv\Scripts\Activate.ps1`.

## Usage

Run the basic secret-sharing demonstration from the repository root:

```bash
python -m demos.basic_sss
```

Run the ECDSA demonstration:

```bash
python -m demos.ecdsa_demo
```

The basic demo uses the constants from `shamir.parameters`:

```python
from shamir.lagrange import reconstruct_secret
from shamir.parameters import Q
from shamir.polynomial import generate_coefficients
from shamir.shares import calculate_points, generate_shares

secret = 12
coefficients = generate_coefficients(secret, degree=2, q=Q)
shares = calculate_points(
    generate_shares(number_of_shares=5, q=Q),
    coefficients,
    q=Q,
)
recovered = reconstruct_secret(shares[:3], degree=2, q=Q)
assert recovered == secret
```

Shares are `(x, y)` pairs. Their `x` coordinates must be distinct and
non-zero. `generate_coefficients` returns coefficients in descending order,
`[a_n, ..., a_1, a_0]`, with the secret as `a_0`.

## Project layout

```text
.
├── shamir/
│   ├── field_operations.py  # Modular inverse and division
│   ├── lagrange.py          # Interpolation and reconstruction
│   ├── parameters.py        # Demo and P-256 field parameters
│   ├── polynomial.py        # Coefficient generation and evaluation
│   ├── shares.py            # Share coordinates and point calculation
│   └── validation.py        # Example validation helpers
├── demos/
│   ├── basic_sss.py         # 3-of-5 finite-field example
│   └── ecdsa_demo.py        # P-256 signing example
├── tests/
├── pyproject.toml
└── README.md
```

## Verification

Run all automated tests:

```bash
python -m pytest
```

The repository currently contains 35 tests covering modular arithmetic,
polynomial evaluation, share generation, interpolation, reconstruction, and
validation helpers.

## Security notice

This is an educational implementation and has not been independently audited.
Do not use it to protect production secrets. In particular, the ECDSA example
temporarily reconstructs the complete private key in one process.
