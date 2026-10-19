#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — Step H1: salted password hashing (STARTER).

Stored format (one string):
    pbkdf2_sha256$<iterations>$<salt_base64>$<hash_base64>

Rules: hashlib.pbkdf2_hmac('sha256', ...), a random 16-byte salt per password, a default of
>= 600000 iterations, and comparison with hmac.compare_digest.
Behaviour you must handle:
  - wrong password                                       -> check() returns False
  - a corrupt stored string / another algorithm /
    iterations <= 0 or absurdly large                    -> ValueError
Expected output once finished:
    two hashes differ? True
    correct password verifies? True
    wrong password verifies? False
"""

from __future__ import annotations

import base64  # noqa: F401
import hashlib  # noqa: F401
import hmac  # noqa: F401
import os  # noqa: F401

ITERATIONS = 600_000


def make_hash(password: str, iterations: int = ITERATIONS) -> str:
    """TODO H1: build the stored string with a fresh random salt."""
    raise NotImplementedError("H1: make_hash")


def check(password: str, stored: str) -> bool:
    """TODO H1: parse the string, recompute with the stored salt/iterations, compare in constant time."""
    raise NotImplementedError("H1: check")


def main() -> int:
    a, b = make_hash("SecretPass123", 100_000), make_hash("SecretPass123", 100_000)
    print("two hashes differ?", a != b)
    print("correct password verifies?", check("SecretPass123", a))
    print("wrong password verifies?", check("wrong", a))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
