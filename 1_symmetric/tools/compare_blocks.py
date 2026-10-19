#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — helper tool: compare ciphertext blocks.

Used in Step S3 (ECB mode leaks patterns). It cuts a ciphertext into 16-byte blocks,
prints their hex, and marks blocks that repeat — both within one file and across files.

The evidence you must collect: the SAME block in two different files means two identical
plaintext parts produced identical ciphertext. With AES-GCM that does not happen.

Usage (run from the BAB2_Kripto folder):
    python3 1_symmetric/tools/compare_blocks.py                          # the two built-in ECB artifacts
    python3 1_symmetric/tools/compare_blocks.py file1.enc file2.enc
"""

from __future__ import annotations

import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS = os.path.join(DIR, "..", "artifacts")
BLOCK_SIZE = 16


def blocks(path: str) -> list[str]:
    with open(path, "rb") as f:
        data = f.read()
    return [data[i : i + BLOCK_SIZE].hex() for i in range(0, len(data), BLOCK_SIZE)]


def show(name: str, block_list: list[str]) -> None:
    print(f"{name}  ({len(block_list)} blocks)")
    for i, b in enumerate(block_list):
        mark = "  <-- repeated in this file" if block_list.count(b) > 1 else ""
        print(f"  block {i:02d}  {b}{mark}")
    print()


def main(argv: list[str]) -> int:
    if len(argv) >= 3:
        a, b = argv[1], argv[2]
    else:
        a = os.path.join(ARTIFACTS, "order_ecb_a.enc")
        b = os.path.join(ARTIFACTS, "order_ecb_b.enc")

    for p in (a, b):
        if not os.path.exists(p):
            print(f"file not found: {p}")
            print("ask the instructor to provide the artifact files first.")
            return 2

    ba, bb = blocks(a), blocks(b)
    show(os.path.basename(a), ba)
    show(os.path.basename(b), bb)

    same = [i for i, x in enumerate(ba) if i < len(bb) and x == bb[i]]
    print("=" * 68)
    print(f"identical blocks at the same position: {same if same else 'none'}")
    if same:
        print()
        print("Evidence for your report:")
        print(f"  - {len(same)} of {len(ba)} ciphertext blocks are identical across the two files.")
        print("  - So identical plaintext parts stay visible from the outside,")
        print("    without knowing the key.")
        print()
        print("Repeat this for a file produced by AES-GCM. The identical blocks")
        print("disappear because GCM uses a nonce and spreads the randomness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
