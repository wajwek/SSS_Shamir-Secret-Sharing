
# Shamir Secret Sharing (SSS)

Educational Python implementation of Shamir's Secret Sharing over a finite
field. The configured scheme is **3-of-5**: a secret is the constant term of a
random polynomial of degree two, five shares are generated, and any three shares
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

## How it works

For a threshold `t`, the polynomial has degree `t - 1`:

```text
f(x) = a_(t-1) * x^(t-1) + ... + a_1 * x + secret (mod q)
```

The modulus `q` must be prime, the secret must satisfy `0 <= secret < q`,
and at most `q - 1` shares can be generated. The caller supplies the prime
modulus; the implementation does not test primality. The demos use `q = 17`
and the order of the P-256 base point, respectively. The latter is different
from the modulus used for the curve's point coordinates.

`generate_shares` generates only the unique, non-zero `x` coordinates;
`calculate_points` turns them into `(x, f(x))` shares. Reconstruction uses
Lagrange interpolation at `x = 0`. The degree passed to `reconstruct_secret`
sets the minimum number of shares accepted; it does not authenticate shares
or detect corrupted input. Use shares from the same polynomial and canonical
field coordinates (`1 <= x < q`).

## Encountered problems

### Keeping the highest-degree coefficient non-zero

A zero leading coefficient lowers the polynomial's degree. For example,
`0*x^2 + a_1*x + secret` is linear, so two points can recover its constant
term even when the intended scheme is 3-of-5. The generator therefore samples
the leading coefficient from `1..q-1`; other random coefficients can be zero.

This enforces an exact degree, but conditioning the leading coefficient to be
non-zero changes the usual Shamir distribution: standard perfect-secrecy
proofs use independent uniform coefficients from the entire field. This
educational variant should not be treated as a production cryptographic scheme.

### Avoiding shares with x = 0

The constant term is the secret, so `f(0) = secret`. In the ECDSA demo this
secret is the private scalar. Giving someone the share `(0, f(0))` would
therefore disclose the complete secret. Share coordinates are sampled from
`1..q-1` without duplicates. Distinct coordinates are also necessary for
Lagrange interpolation.

### Evaluating polynomials efficiently: Horner's method

Computing each power separately is unnecessary. Horner's method rewrites
`a_2*x^2 + a_1*x + a_0` as `(a_2*x + a_1)*x + a_0`. The implementation
walks through coefficients in descending order and updates
`result = (result * x + coefficient) % q`. This takes linear time in the
polynomial's degree and keeps intermediate values reduced modulo `q`.

### Finding a multiplicative inverse modulo q

Division in a finite field means multiplication by an inverse:
`a / b = a * b^(-1) (mod q)`. The inverse satisfies
`b * b^(-1) = 1 (mod q)`. For example, the inverse of `3` modulo `17` is
`6`, because `3 * 6 = 18 = 1 (mod 17)`.

The implementation uses Python's `pow(b, -1, q)`, which computes a modular
inverse. For a prime modulus every non-zero field element has an inverse;
zero does not. In Lagrange interpolation the denominators contain
`x_i - x_j`, which explains why repeated coordinates modulo `q` are invalid.

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

The tests cover modular arithmetic,
polynomial evaluation, share generation, interpolation, reconstruction, and
validation helpers.

## Security notice

This is an educational implementation and has not been independently audited.
Do not use it to protect production secrets. In particular, the ECDSA example
temporarily reconstructs the complete private key in one process.
