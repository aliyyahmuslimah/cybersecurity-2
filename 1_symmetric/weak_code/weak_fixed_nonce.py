#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — WEAK CODE EXAMPLE: an AES-GCM nonce that is reused.

Provided by the instructor. Do NOT treat this as a correct example.

Context: a "daily report" script that encrypts every report with the same key AND the
same nonce. The key is not in this file (the instructor keeps it) — and it is not
needed for the attack.

Deliberate weakness:
  S-5  A fixed nonce (FIXED_NONCE). In a stream-style mode such as GCM (CTR inside),
       two messages under the same key+nonce use the same keystream:
           C1 xor C2 = P1 xor P2
       If one plaintext is known, the other is readable WITHOUT the key.

TASK (Step S5): for artifacts/reused_nonce_1.enc and reused_nonce_2.enc, recover the
plaintext of the second message using the first plaintext (artifacts/reused_nonce_1.txt).
Then fix it: a random nonce per message, stored as nonce + ciphertext.

Usage (run from the BAB2_Kripto folder):
    python3 1_symmetric/weak_code/weak_fixed_nonce.py encrypt <key_base64> <input_file> <output_file>
    python3 1_symmetric/weak_code/weak_fixed_nonce.py decrypt <key_base64> <input_file> <output_file>
"""

from __future__ import annotations

import base64
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

FIXED_NONCE = bytes(range(12, 24))  # S-5: used for EVERY message


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    return AESGCM(key).encrypt(FIXED_NONCE, plaintext, None)


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    return AESGCM(key).decrypt(FIXED_NONCE, ciphertext, None)


def main(argv: list[str]) -> int:
    if len(argv) != 5 or argv[1] not in ("encrypt", "decrypt"):
        print(__doc__)
        return 2
    mode, key_b64, src, dst = argv[1:]
    key = base64.b64decode(key_b64)
    with open(src, "rb") as f:
        data = f.read()
    result = encrypt(data, key) if mode == "encrypt" else decrypt(data, key)
    with open(dst, "wb") as f:
        f.write(result)
    print(f"{mode}: {src} -> {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
