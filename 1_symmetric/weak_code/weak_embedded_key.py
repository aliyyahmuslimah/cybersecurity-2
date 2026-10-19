#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — WEAK CODE EXAMPLE: a key embedded in the code.

Provided by the instructor. Do NOT treat this as a correct example.

Context: the "order vault" script the operations unit uses to protect order exports
before sending them to a partner. The encryption key lives in the same script, and the
script is committed to Git.

Deliberate weaknesses:
  K-1  The encryption key is stored as a (base64) literal inside the script.
       Whoever holds the script holds the key.
  K-2  A fixed nonce (reused for every encryption).
  K-3  The encryption adds no security at all: the file and its key travel together.

TASK (Step S6): find the key in this code, decode it, then decrypt
../artifacts/order_vault.enc WITHOUT being handed the key directly. Keep the decrypted
output as evidence.

Usage (run from the BAB2_Kripto folder):
    python3 1_symmetric/weak_code/weak_embedded_key.py encrypt <input_file> <output_file>
    python3 1_symmetric/weak_code/weak_embedded_key.py decrypt <input_file> <output_file>
"""

from __future__ import annotations

import base64
import json
import os
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------------------------------------------------------------------------
# K-1: the variable name is made inconspicuous, but this IS the key.
# ---------------------------------------------------------------------------
_TEMPLATE_CACHE_B64 = "TGFiS2V5Rm9yQkFCMlZhdWx0Q3liZXJTZWN1cmUhISE="
_IV_DEFAULT = "AAECAwQFBgcICQoL"  # K-2: fixed nonce, 12 bytes


def key() -> bytes:
    return base64.b64decode(_TEMPLATE_CACHE_B64)


def nonce() -> bytes:
    return base64.b64decode(_IV_DEFAULT)


def encrypt(plaintext: bytes) -> bytes:
    return AESGCM(key()).encrypt(nonce(), plaintext, None)


def decrypt(ciphertext: bytes) -> bytes:
    return AESGCM(key()).decrypt(nonce(), ciphertext, None)


# ---------------------------------------------------------------------------
# Sample vault content (dummy data, nothing real).
# ---------------------------------------------------------------------------
VAULT_CONTENT = {
    "unit": "B2B Order Operations",
    "note": "Dummy data for Practical 2 — not real customer data.",
    "orders": [
        {"no": "ORDER-0000001", "customer": "PT Contoh Niaga", "status": "PROCESSING", "amount": 12500000},
        {"no": "ORDER-0000002", "customer": "CV Mitra Contoh", "status": "PENDING", "amount": 4300000},
        {"no": "ORDER-0000003", "customer": "Koperasi Contoh", "status": "SHIPPED", "amount": 7850000},
    ],
}


def _read(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _write(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)


def main(argv: list[str]) -> int:
    if len(argv) == 4 and argv[1] in ("encrypt", "decrypt"):
        mode, src, dst = argv[1], argv[2], argv[3]
        data = _read(src)
        result = encrypt(data) if mode == "encrypt" else decrypt(data)
        _write(dst, result)
        print(f"{mode}: {src} -> {dst} ({len(data)} bytes)")
        return 0

    # No arguments: rebuild the sample vault.
    target = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "artifacts", "order_vault.enc"
    )
    os.makedirs(os.path.dirname(target), exist_ok=True)
    data = json.dumps(VAULT_CONTENT, indent=2, ensure_ascii=False).encode("utf-8")
    _write(target, encrypt(data))
    print(f"vault written: {target} ({len(data)} plaintext bytes)")
    print("Task: recover the key from this code, then decrypt that file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
