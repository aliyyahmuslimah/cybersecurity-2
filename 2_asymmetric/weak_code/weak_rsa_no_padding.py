#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — WEAK CODE EXAMPLE: RSA without padding is deterministic.

Provided by the instructor. Do NOT treat this as a correct example.

Context: a "session key exchange" module between the ordering service and the payment
service. The developer wrote "bare" RSA (textbook RSA) because it looked simpler than OAEP.

Deliberate weaknesses:
  R-1  RSA without padding is deterministic: the same plaintext always gives the same
       ciphertext. An attacker can recognise repeated messages without breaking the key,
       and can mount a dictionary attack (guess a plaintext, encrypt it, compare).
  R-2  Without padding RSA is also open to classic mathematical attacks
       (e.g. Hastad's cube root, Bleichenbacher on PKCS#1 v1.5).

Compare with RSA-OAEP, which inserts randomness so two encryptions of the same message
always differ.

Technical note: the `cryptography` library no longer offers RSA encryption without
padding, so this example uses the raw maths (c = m^e mod n) to make the weakness visible.

Usage (run from the BAB2_Kripto folder):
    python3 2_asymmetric/weak_code/weak_rsa_no_padding.py
"""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

MESSAGE = b"session key: 0123456789abcdef"


def encrypt_no_padding(message: bytes, n: int, e: int) -> bytes:
    """Textbook RSA: c = m^e mod n. R-1: there is no randomness at all."""
    k = (n.bit_length() + 7) // 8
    if len(message) > k:
        raise ValueError("message is longer than the modulus")
    m = int.from_bytes(message.rjust(k, b"\x00"), "big")
    c = pow(m, e, n)
    return c.to_bytes(k, "big")


def decrypt_no_padding(ciphertext: bytes, n: int, d: int) -> bytes:
    c = int.from_bytes(ciphertext, "big")
    m = pow(c, d, n)
    k = (n.bit_length() + 7) // 8
    return m.to_bytes(k, "big").lstrip(b"\x00")


def main() -> int:
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = priv.public_key()
    pub_numbers = pub.public_numbers()
    priv_numbers = priv.private_numbers()

    print("Message being encrypted (exactly the same):", MESSAGE.decode())
    print()

    # --- R-1: no padding -> deterministic -------------------------------------
    c1 = encrypt_no_padding(MESSAGE, pub_numbers.n, pub_numbers.e)
    c2 = encrypt_no_padding(MESSAGE, pub_numbers.n, pub_numbers.e)
    print("RSA WITHOUT PADDING")
    print("  ciphertext #1:", c1.hex()[:64], "...")
    print("  ciphertext #2:", c2.hex()[:64], "...")
    print("  identical?      ", c1 == c2, " <-- weakness R-1")
    print("  decrypts right? ", decrypt_no_padding(c1, pub_numbers.n, priv_numbers.d) == MESSAGE)
    print()

    # --- The comparison: OAEP --------------------------------------------------
    oaep = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
    o1 = pub.encrypt(MESSAGE, oaep)
    o2 = pub.encrypt(MESSAGE, oaep)
    print("RSA-OAEP (correct)")
    print("  ciphertext #1:", o1.hex()[:64], "...")
    print("  ciphertext #2:", o2.hex()[:64], "...")
    print("  identical?      ", o1 == o2, " <-- the randomness works")
    print("  decrypts right? ", priv.decrypt(o1, oaep) == MESSAGE)
    print()

    print("Conclusion: without padding, two encryptions of the same message give the same")
    print("ciphertext. An attacker can use a ciphertext dictionary, and can tell that two")
    print("transmissions carried the same message — without the key.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
