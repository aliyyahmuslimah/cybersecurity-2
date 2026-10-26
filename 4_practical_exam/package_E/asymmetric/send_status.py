#!/usr/bin/env python3
"""
PRACTICAL EXAM — Asymmetric station. The sender of order statuses to a partner.
Provided by the instructor. An order status is always one of VALID_STATUSES.
order_status.csv holds the order number and the ciphertext (hex).
"""

from __future__ import annotations

import os
import pathlib
import sys

from cryptography.hazmat.primitives import serialization

VALID_STATUSES = (b"PROCESSING", b"PENDING", b"SHIPPED")
_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_DIR, "public_key.pem"), "rb") as _f:
    _PUB = serialization.load_pem_public_key(_f.read()).public_numbers()


def encrypt_status(status: bytes) -> bytes:
    """'Bare' RSA: c = m^e mod n."""
    k = (_PUB.n.bit_length() + 7) // 8
    m = int.from_bytes(status.rjust(k, b"\x00"), "big")
    return pow(m, _PUB.e, _PUB.n).to_bytes(k, "big")


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1].encode() in VALID_STATUSES:
        status = argv[1].encode()
        ct = encrypt_status(status)
        print(f"Status: {argv[1]}")
        print(f"Ciphertext (hex):\n{ct.hex()}")
        return 0
    print("Asymmetric Station — Order Status Sender (Bare RSA)")
    print(f"Valid statuses: {[s.decode() for s in VALID_STATUSES]}")
    print("Usage:")
    print("  python3 send_status.py <STATUS>")
    print("Example:")
    print("  python3 send_status.py PENDING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
