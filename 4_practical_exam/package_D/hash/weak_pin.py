#!/usr/bin/env python3
"""
PRACTICAL EXAM — Hash station. 4-digit PIN storage in a legacy cashier application.
Provided by the instructor. pin_dump.csv lists the users and their PIN hashes (dummy data).
"""

from __future__ import annotations

import hashlib
import sys


def store_pin(pin: str) -> str:
    return hashlib.sha1(pin.encode()).hexdigest()


def check_pin(pin: str, stored: str) -> bool:
    return store_pin(pin) == stored


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[1].isdigit():
        pin = argv[1]
        print(f"PIN: {pin} -> SHA-1 Hash: {store_pin(pin)}")
        return 0
    if len(argv) == 3 and argv[1].isdigit():
        pin, expected = argv[1], argv[2]
        match = check_pin(pin, expected)
        print(f"PIN: {pin} vs Hash: {expected} -> Match: {match}")
        return 0 if match else 1
    print("Hash Station — Cashier PIN Storage (Unsalted SHA-1)")
    print("Usage:")
    print("  python3 weak_pin.py <4-digit-pin>")
    print("  python3 weak_pin.py <4-digit-pin> <expected_hash>")
    print("Example:")
    print("  python3 weak_pin.py 1234")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
