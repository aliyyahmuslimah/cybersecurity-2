#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — Step A1: RSA-OAEP (STARTER).

Fill in the TODO parts. Use the `cryptography` library; OAEP with SHA-256 (MGF1 SHA-256).
Expected output once finished:
    round-trip: True
    two encryptions identical? False
"""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes  # noqa: F401
from cryptography.hazmat.primitives.asymmetric import padding, rsa  # noqa: F401


def generate_key():
    """TODO A1: an RSA private key, 2048 bits, public exponent 65537."""
    raise NotImplementedError("A1: generate_key")


def encrypt_oaep(pub, message: bytes) -> bytes:
    """TODO A1: encrypt with padding.OAEP(...)."""
    raise NotImplementedError("A1: encrypt_oaep")


def decrypt_oaep(priv, ciphertext: bytes) -> bytes:
    """TODO A1: decrypt with the same OAEP."""
    raise NotImplementedError("A1: decrypt_oaep")


def main() -> int:
    priv = generate_key()
    pub = priv.public_key()
    message = b"session key: 0123456789abcdef"
    c1, c2 = encrypt_oaep(pub, message), encrypt_oaep(pub, message)
    print("round-trip:", decrypt_oaep(priv, c1) == message)
    print("two encryptions identical?", c1 == c2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
