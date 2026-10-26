# BAB 2 — Cryptography Practical Kit

Companion to **Practical 2 — Symmetric, Asymmetric Encryption and Hashing (Python)** in
`Modul_Ajar_Cyber_Security.docx` (Weeks 3–4) and to **Assignment 2 — Cryptography: build,
misuse, fix** (*Tugas 2*, rubric **C2**, 10%). The instructor provides weak code examples and
encrypted files; you build the correct version, break the weak one, fix it, and prove it with
automated tests.

## Folders

| Folder | When | Contents |
|---|---|---|
| [`1_symmetric/`](1_symmetric/README.md) | Session 1 (Week 3, 150 min) | a Caesar warm-up (C1–C2), AES-GCM, ECB, a reused nonce, an embedded key |
| [`2_asymmetric/`](2_asymmetric/README.md) | Session 2 (Week 4) | RSA-OAEP, RSA without padding, hybrid encryption |
| [`3_hash/`](3_hash/README.md) | Session 2 (Week 4) | salted hashing, a dictionary attack, a KDF |
| [`4_practical_exam/`](4_practical_exam/exam_instructions.md) | end of Session 2 | three stations, Packages A–E — **handed out by the instructor at exam time, not before** |
| [`5_homework/`](5_homework/README.md) | after the sessions (Assignment 2) | A4, H4, all the automated-test skeletons, the take-home evidence sheet |

## Timetable

| Session | Minutes | Activity |
|---|---|---|
| 1 | 150 | C1–C2 (a 15-minute warm-up) and S1–S6 in `1_symmetric/` |
| 2 | 75 | A1–A3 in `2_asymmetric/`, H1–H3 in `3_hash/` |
| 2 | 75 | Practical exam (`4_practical_exam/`) |
| After | — | `5_homework/`: A4, H4, automated tests (at least 6 passing), the four evidence sheets, README + flow diagram, commit history |

## Setup

```bash
cd BAB2_Kripto
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -c "import cryptography; print(cryptography.__version__)"
```

Run your tests with `pytest -q 5_homework/starter_tests` from this folder
(**7 base tests + 7 optional; at least 6 must pass**).

## Limits you must not cross

- **Dummy data** only. There is no real customer data anywhere in this folder.
- Do **not** design your own crypto algorithms.
- Encryption is **not** a substitute for access control.
- Private keys and your own keys **must not** be written into a report or committed to Git
  (`.gitignore` in this folder already ignores `*.key` and `*_private.pem`).
- The keys in this folder are single-use lab keys. Never reuse them outside the practical.
