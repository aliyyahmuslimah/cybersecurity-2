#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — WEAK CODE EXAMPLE: ECB mode leaks patterns.

Provided by the instructor. Do NOT treat this as a correct example.

Context: the operations unit has an "order vault" — a fixed-width export from the B2B
ordering system. Every line is exactly 16 bytes so the blocks line up. Most slots are
still empty.

Deliberate weaknesses:
  E-1  ECB encrypts every 16-byte block independently. Two identical plaintext blocks
       give two identical ciphertext blocks, so the structure and repetition of the
       original data stay visible.
  E-2  The key is stored as a literal in the script (a lab key).
  E-3  No authentication (ECB has no tag) — the ciphertext can be modified without
       detection.

Usage (run from the BAB2_Kripto folder):
    python3 1_symmetric/weak_code/weak_ecb.py                          # encrypt the two sample files
    python3 1_symmetric/weak_code/weak_ecb.py <input_file> <output_file>
"""

from __future__ import annotations

import base64
import os
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ---------------------------------------------------------------------------
# E-2: the key as a literal in the code (a lab key, not a real secret — still
# wrong in practice because the key gets committed along with the code).
# ---------------------------------------------------------------------------
_KEY_LITERAL = "TGFiS2V5RUNCMTZieXRlcw=="  # base64 -> 16 bytes (AES-128)

KEY = base64.b64decode(_KEY_LITERAL)
ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "artifacts")


def _pad_pkcs7(data: bytes) -> bytes:
    n = 16 - (len(data) % 16)
    return data + bytes([n]) * n


def encrypt_ecb(plaintext: bytes) -> bytes:
    """Encrypt with AES-128-ECB. E-1: identical blocks -> identical ciphertext."""
    encryptor = Cipher(algorithms.AES(KEY), modes.ECB()).encryptor()
    return encryptor.update(_pad_pkcs7(plaintext)) + encryptor.finalize()


def decrypt_ecb(ciphertext: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(KEY), modes.ECB()).decryptor()
    result = decryptor.update(ciphertext) + decryptor.finalize()
    return result[: -result[-1]]  # strip the PKCS7 padding


# ---------------------------------------------------------------------------
# Two fixed-width exports that partly share content. Look at the "EMPTY" blocks.
# ---------------------------------------------------------------------------
BLOCK_HEADER = b"ORDER-VAULT-----"
BLOCK_EMPTY = b"EMPTY-----------"


def order_block(n: int) -> bytes:
    """One order line, exactly 16 bytes: ORDER-0000001---"""
    return ("ORDER-%07d---" % n).encode()


def sample_a() -> bytes:
    """Export A: three empty slots, then one order."""
    return BLOCK_HEADER + BLOCK_EMPTY * 3 + order_block(1)


def sample_b() -> bytes:
    """Export B: two empty slots, then two orders."""
    return BLOCK_HEADER + BLOCK_EMPTY * 2 + order_block(2) + order_block(3)


def main(argv: list[str]) -> int:
    if len(argv) == 3:
        src, dst = argv[1], argv[2]
        with open(src, "rb") as f:
            data = f.read()
        with open(dst, "wb") as f:
            f.write(encrypt_ecb(data))
        print(f"encrypted: {src} -> {dst} ({len(data)} bytes)")
        return 0

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    for name, data in (("order_ecb_a", sample_a()), ("order_ecb_b", sample_b())):
        out = os.path.join(ARTIFACTS_DIR, name + ".enc")
        with open(out, "wb") as f:
            f.write(encrypt_ecb(data))
        print(f"{out}  ({len(data)} plaintext bytes)")

    print()
    print("Ciphertext blocks (16 bytes each) — look for the repeated blocks:")
    for name in ("order_ecb_a", "order_ecb_b"):
        with open(os.path.join(ARTIFACTS_DIR, name + ".enc"), "rb") as f:
            ct = f.read()
        blocks = [ct[i : i + 16].hex() for i in range(0, len(ct), 16)]
        print(f"  {name}: " + "  ".join(blocks))
    print()
    print("Run `python3 1_symmetric/tools/compare_blocks.py` (from the BAB2_Kripto folder) for automatic analysis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
