#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — WEAK CODE EXAMPLE: passwords stored as unsalted MD5.

Provided by the instructor. Do NOT treat this as a correct example.

Context: the "login" module of the legacy ordering service. Its user database has leaked
(artifacts/user_dump.csv, dummy data). The real passwords are NOT in any file — you have to
recover them from the hashes.

Deliberate weaknesses:
  H-1  MD5 is fast (millions of guesses per second) and was not designed for passwords.
  H-2  No salt: the same password gives the same hash (visible straight away in the dump),
       and one table of hashes works against every user at once.
  H-3  Comparison with `==` is not constant-time.

TASK:
  H2  Write wordlist_attack.py yourself: read the dump + artifacts/small_wordlist.txt and
      recover the passwords that are in the wordlist. Record how many users fall and why the
      rest do not.
  H3  Replace this with a salted KDF (PBKDF2-HMAC-SHA256 >= 600,000 iterations, or scrypt)
      and hmac.compare_digest; measure the difference in time per guess.

Usage (run from the BAB2_Kripto folder):
    python3 3_hash/weak_code/weak_hash_no_salt.py
"""

from __future__ import annotations

import hashlib


def store_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()  # H-1, H-2


def check_password(password: str, stored: str) -> bool:
    return store_password(password) == stored  # H-3


def main() -> int:
    print("md5('password123') =", store_password("password123"))
    print("md5('password123') =", store_password("password123"), " <-- always the same (no salt)")
    print()
    print("Task: recover the passwords from artifacts/user_dump.csv with a wordlist (H2),")
    print("then fix it with a salted KDF (H3).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
