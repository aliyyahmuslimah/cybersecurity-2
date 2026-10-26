#!/usr/bin/env python3
"""
PRACTICAL EXAM — Symmetric station. The warehouse unit's "daily report" script.
Provided by the instructor. Find its weakness, prove it, then fix it.
"""

from __future__ import annotations

import sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_PART_1 = bytes.fromhex("705077bdb3f172435b62e4fd8a2e266e8b08da1642a6568a701ffc44537dc7b7")
_PART_2 = bytes.fromhex("06d063277e930ab72bf97e76cc4d909336a69a418438ad68814b0cc10568c3d0")
_NONCE = bytes.fromhex("d5ba4d098a93f620572bc54e")


def _key() -> bytes:
    return bytes(a ^ b for a, b in zip(_PART_1, _PART_2))


def encrypt(plaintext: bytes) -> bytes:
    return AESGCM(_key()).encrypt(_NONCE, plaintext, None)


def decrypt(ciphertext: bytes) -> bytes:
    return AESGCM(_key()).decrypt(_NONCE, ciphertext, None)


def main(argv: list[str]) -> int:
    if len(argv) == 3 and argv[1] == "decrypt":
        with open(argv[2], "rb") as f:
            data = f.read()
        try:
            pt = decrypt(data)
            print(pt.decode("utf-8", errors="replace"))
            return 0
        except Exception as err:
            print(f"Decryption failed: {err}")
            return 1
    elif len(argv) == 3 and argv[1] == "encrypt":
        with open(argv[2], "rb") as f:
            data = f.read()
        ct = encrypt(data)
        sys.stdout.buffer.write(ct)
        return 0
    elif len(argv) == 4 and argv[1] == "encrypt":
        with open(argv[2], "rb") as f:
            data = f.read()
        ct = encrypt(data)
        with open(argv[3], "wb") as f:
            f.write(ct)
        print(f"Encrypted {len(data)} bytes -> {argv[3]}")
        return 0
    print("Symmetric Station — Warehouse Daily Report Encryptor")
    print("Usage:")
    print("  python3 daily_report.py decrypt report_monday.enc")
    print("  python3 daily_report.py decrypt report_tuesday.enc")
    print("  python3 daily_report.py encrypt <input_file> <output_file>")
    print("  python3 daily_report.py encrypt <input_file> > <output_file>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
