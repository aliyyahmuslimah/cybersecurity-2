#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — Steps S1–S2: an AES-GCM file vault (STARTER).

Fill in every function marked TODO (remove the `raise NotImplementedError`).
Rules: use the `cryptography` library (AESGCM). Do not design your own algorithm.
Keep the key OUTSIDE the repository and the report (e.g. ~/.lab_keys/vault.key).

Encrypted file format:  nonce (12 bytes) + ciphertext + tag (16 bytes)

When finished, run:
    python3 1_symmetric/starter/s1_vault_gcm.py
Expected output:
    round-trip: True
    tampered ciphertext rejected: InvalidTag
"""

from __future__ import annotations

import os
import tempfile

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # noqa: F401  (you will use it)

NONCE_SIZE = 12
TAG_SIZE = 16


def create_key() -> bytes:
    """TODO S1: a random AES-256 key (32 bytes). Hint: AESGCM.generate_key."""
    raise NotImplementedError("S1: create_key")


def save_key(key: bytes, path: str) -> None:
    """TODO S1: write the key to `path` with permissions 0600 (os.open with a mode)."""
    raise NotImplementedError("S1: save_key")


def load_key(path: str) -> bytes:
    """TODO S1: read the key; reject (ValueError) if its length is not 32 bytes."""
    raise NotImplementedError("S1: load_key")


def encrypt_data(key: bytes, data: bytes) -> bytes:
    """TODO S1: a NEW random 12-byte nonce for every message; return nonce + ct."""
    raise NotImplementedError("S1: encrypt_data")


def decrypt_data(key: bytes, package: bytes) -> bytes:
    """TODO S1/S2: split nonce and ct; ValueError if the package is < 28 bytes;
    let InvalidTag surface if the data was changed or the key is wrong."""
    raise NotImplementedError("S2: decrypt_data")


def encrypt_file(key: bytes, src: str, dst: str) -> None:
    """TODO S1: read `src`, write the encrypted result to `dst`."""
    raise NotImplementedError("S1: encrypt_file")


def decrypt_file(key: bytes, src: str, dst: str) -> None:
    """TODO S1: write `dst` ONLY if decryption succeeds."""
    raise NotImplementedError("S1: decrypt_file")


def main() -> int:
    key = create_key()
    with tempfile.TemporaryDirectory() as d:
        orig, enc, dec = (os.path.join(d, n) for n in ("a.txt", "a.enc", "a.out"))
        with open(orig, "wb") as f:
            f.write(b"ORDER-0000001 | dummy data")
        encrypt_file(key, orig, enc)
        decrypt_file(key, enc, dec)
        with open(orig, "rb") as a, open(dec, "rb") as b:
            print("round-trip:", a.read() == b.read())
        with open(enc, "rb") as f:
            broken = bytearray(f.read())
        broken[NONCE_SIZE] ^= 1  # S2: flip one bit
        with open(enc, "wb") as f:
            f.write(broken)
        try:
            decrypt_file(key, enc, dec)
            print("tampered ciphertext rejected: NO  <-- something is wrong")
        except InvalidTag:
            print("tampered ciphertext rejected: InvalidTag")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
