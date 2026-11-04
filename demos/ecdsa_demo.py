"""Demonstration of SSS with ECDSA on the NIST P-256 curve."""

from random import SystemRandom

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from shamir.lagrange import reconstruct_secret
from shamir.parameters import NUMBER_OF_SHARES, P256_ORDER, POLYNOMIAL_DEGREE
from shamir.polynomial import generate_coefficients
from shamir.shares import calculate_points, generate_shares

secure_random = SystemRandom()
MESSAGE = b"Shamir Secret Sharing with ECDSA"


def main() -> None:
    original_private_key = ec.generate_private_key(ec.SECP256R1())
    original_private_value = original_private_key.private_numbers().private_value
    coefficients = generate_coefficients(
        secret=original_private_value,
        degree=POLYNOMIAL_DEGREE,
        q=P256_ORDER,
    )
    x_values = generate_shares(NUMBER_OF_SHARES, P256_ORDER)
    shares = calculate_points(x_values, coefficients, P256_ORDER)
    selected_shares = secure_random.sample(
        shares,
        POLYNOMIAL_DEGREE + 1,
    )
    reconstructed_private_value = reconstruct_secret(
        selected_shares,
        degree=POLYNOMIAL_DEGREE,
        q=P256_ORDER,
    )
    reconstructed_private_key = ec.derive_private_key(
        reconstructed_private_value,
        ec.SECP256R1(),
    )
    signature = reconstructed_private_key.sign(
        MESSAGE,
        ec.ECDSA(hashes.SHA256()),
    )

    try:
        original_private_key.public_key().verify(
            signature,
            MESSAGE,
            ec.ECDSA(hashes.SHA256()),
        )
    except InvalidSignature as error:
        raise RuntimeError("ECDSA signature verification failed.") from error

    print("=== Shamir Secret Sharing with ECDSA: 3-of-5 demonstration ===")
    print("Curve = NIST P-256 (secp256r1)")
    print(f"Field modulus Q = {P256_ORDER}")
    print(f"Number of shares = {NUMBER_OF_SHARES}")
    print(f"Polynomial degree = {POLYNOMIAL_DEGREE}")
    print(f"Original private scalar = {original_private_value}")
    print(f"Polynomial coefficients [a2, a1, a0] = {coefficients}")
    print()
    print("Calculated shares:")
    for x, y in shares:
        print(f"  x = {x}: y = f(x) = {y} -> ({x}, {y})")
    print()
    print(f"Selected shares for reconstruction: {selected_shares}")
    print(f"Reconstructed private scalar = {reconstructed_private_value}")
    print(
        "Private scalar recovered correctly: "
        f"{reconstructed_private_value == original_private_value}"
    )
    print(f"Message signed: {MESSAGE!r}")
    print("Signature verified with the original public key: True")


if __name__ == "__main__":
    main()
