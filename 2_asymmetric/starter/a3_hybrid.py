#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — Step A3: hybrid encryption (STARTER).

Design: a random AES-256 key -> encrypt the data with AES-GCM (random 12-byte nonce); wrap that
AES key with RSA-OAEP. Package format:

    wrapped_key_length (2 bytes, big-endian) | wrapped_key | nonce | ct+tag

Behaviour you must handle:
  - empty / truncated package / a lying length header  -> ValueError
  - wrong private key                                  -> ValueError
  - data was modified                                  -> InvalidTag
Expected output once finished:
    10000 bytes: round-trip True
"""

from __future__ import annotations

import os

from cryptography.hazmat.primitives import hashes  # noqa: F401
from cryptography.hazmat.primitives.asymmetric import padding, rsa  # noqa: F401
from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # noqa: F401


def hybrid_encrypt(data: bytes, pub) -> bytes:
    """TODO A3: build the package in the format above."""
    raise NotImplementedError("A3: hybrid_encrypt")


def hybrid_decrypt(package: bytes, priv) -> bytes:
    """TODO A3: parse the package, checking lengths BEFORE slicing."""
    raise NotImplementedError("A3: hybrid_decrypt")


def main() -> int:
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    data = os.urandom(10_000)
    package = hybrid_encrypt(data, priv.public_key())
    print(f"{len(data)} bytes: round-trip", hybrid_decrypt(package, priv) == data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
