# MANIFEST — encrypted files (from the instructor)

The files in this folder are **provided by the instructor**. Do not change them. If they are
changed, the instructor can rebuild them.

Everything here is **dummy data**. There is no real customer data, no real credential and no
real key.

| File | Size | Made by | For step |
|---|---|---|---|
| `order_ecb_a.enc` | 96 bytes | `weak_code/weak_ecb.py` | S3, S4 |
| `order_ecb_b.enc` | 96 bytes | `weak_code/weak_ecb.py` | S3 |
| `order_vault.enc` | 532 bytes | `weak_code/weak_embedded_key.py` | S6 |
| `reused_nonce_1.enc`, `reused_nonce_2.enc` | 79 bytes | `weak_code/weak_fixed_nonce.py` | S5 |
| `reused_nonce_1.txt` | 63 bytes | — (the leaked plaintext of message 1) | S5 |
| `caesar_message.txt` | text | — | C2 |

## `order_ecb_a.enc` and `order_ecb_b.enc`

Two exports of the "order vault", encrypted with **AES-128-ECB**. They are fixed-width exports
(every line is exactly 16 bytes) and part of their content is the same. Both use the same lab key.

What you must find: ciphertext blocks that **repeat**, both within one file and across the two
files. Use `python3 tools/compare_blocks.py`.

The plaintext of both files is **not** included — reconstruct it from the pattern.

## `order_vault.enc`

An export of order data encrypted by `weak_code/weak_embedded_key.py`. Its encryption key is
**embedded in that script**, and its nonce is fixed.

What you must do (Step S6): find the key in the code, recover it, then decrypt this file
**without ever being handed the key**. Keep the decrypted output as evidence.

## Artifacts C2, S4 and S5

| File | Used for |
|---|---|
| `caesar_message.txt` | **C2**: a sentence encrypted with the Caesar cipher using an undisclosed shift; break it by trying all 25 possibilities |
| `order_ecb_a.enc` | **S4**: copy one ciphertext block over another, then decrypt — no error is raised |
| `reused_nonce_1.enc`, `reused_nonce_2.enc` | **S5**: two reports encrypted with AES-GCM under the same key **and the same nonce** |
| `reused_nonce_1.txt` | **S5**: the plaintext of report 1 (leaked). The key is **not** provided |

What you must do (S5): recover the plaintext of report 2 **without the key**
(`C1 xor C2 xor P1`). Ignore the 16-byte tag at the end of each ciphertext.

## Where the keys are

> Read this section only if you have already tried it yourself and are stuck.

- The key for `order_ecb_*` is embedded in `weak_code/weak_ecb.py`.
- The key for `order_vault.enc` is embedded in `weak_code/weak_embedded_key.py` — that is the
  whole point of Step S6.
- The key for `reused_nonce_*` is deliberately **not** provided; the attack does not need it.
- The RSA private key is not included: `2_asymmetric/weak_code/weak_rsa_no_padding.py` generates a
  temporary key every time it runs.
