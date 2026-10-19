#!/usr/bin/env python3
"""
Practical 2 (BAB 2) — WEAK CODE EXAMPLE: RSA used directly on large data.

Provided by the instructor. Do NOT treat this as a correct example.

Context: a developer wants to send an order export (1 KB) to a partner and calls RSA-OAEP
directly on the whole file.

Weakness / limitation:
  R-3  RSA can only encrypt messages that are MUCH shorter than the modulus. With a 2048-bit
       key and OAEP-SHA256 the limit is 256 - 2*32 - 2 = 190 bytes. Cutting the file into
       190-byte pieces and encrypting them one by one is slow and the wrong approach. The fix
       is HYBRID ENCRYPTION — a random AES key for the data (GCM), RSA-OAEP only to wrap that
       AES key.

TASK (Step A3): run this script, look at the failure, then write hybrid encryption in
starter/a3_hybrid.py.

Usage (run from the BAB2_Kripto folder):
    python3 2_asymmetric/weak_code/weak_rsa_large_data.py
"""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

OAEP = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)


def try_direct_encrypt(data: bytes) -> dict:
    """Try RSA-OAEP directly. Returns {'success', 'limit_bytes', 'data_size'}."""
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = priv.public_key()
    limit = (pub.key_size // 8) - 2 * hashes.SHA256.digest_size - 2
    try:
        pub.encrypt(data, OAEP)
        success = True
    except ValueError:
        success = False
    return {"success": success, "limit_bytes": limit, "data_size": len(data)}


def main() -> int:
    data = b"ORDER-0000001|PT Contoh Niaga|PROCESSING|12500000\n" * 20  # ~1 KB
    result = try_direct_encrypt(data)
    print(f"data size     : {result['data_size']} bytes")
    print(f"RSA-OAEP limit: {result['limit_bytes']} bytes (2048-bit key, SHA-256)")
    print(f"succeeded?    : {result['success']}  <-- limitation R-3")
    print()
    print("Task: write hybrid encryption (AES-GCM for the data, RSA-OAEP for the AES key).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
