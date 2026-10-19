# Track 2 — Asymmetric Cryptography

**Session 2 · Week 4 · about 40 of the 75 practice minutes (the rest is Track 3) · individual work**

Part of Practical 2 (BAB 2) and of Assignment 2 — Cryptography: build, misuse, fix (*Tugas 2*,
rubric C2). Same pattern as Track 1: **build it correctly → break the weak version → fix it and prove it**.

## What you will do in this track

1. **Build** RSA encryption the right way (RSA-OAEP).
2. **See** why "bare" RSA without padding is broken: the same message always gives the same ciphertext.
3. **Hit RSA's size limit** on a 1 KB file, then **build hybrid encryption** (a random AES key for the
   data, RSA only to protect that AES key) — the way real systems do it.
4. **Write down evidence** for each one in your evidence sheet. After the session you also do A4 (RSA signatures); it is
   described in `5_homework/README.md`.

You never design your own cipher. You use the `cryptography` library and attack code that was written badly on purpose.

## Before you start (once, about 5 minutes)

**Every command in this guide is run from the `BAB2_Kripto/` folder.** Open a terminal there first.

If you already did the setup in Track 1, only re-activate the environment and skip to step 3. Otherwise:

1. You need Python 3.10 or newer: `python3 --version`.
2. Create and activate an environment, then install the library:

   macOS / Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   Windows (PowerShell; use `py` wherever this guide says `python3`):
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Check that it works. It must print a version number (42 or higher) and no error:
   ```bash
   python3 -c "import cryptography; print(cryptography.__version__)"
   ```
4. Create the folder for the scripts you write yourself: `2_asymmetric/my_work/` (it does not exist yet — make it).
5. Keep `2_asymmetric/evidence_sheet.md` open. You fill one row per step as you go.

**Where you may write — Never edit anything in `weak_code/`.**

| Folder | What it holds | You may edit it? |
|---|---|---|
| `starter/` | the two files you complete (`a1_rsa_oaep.py`, `a3_hybrid.py`) | **yes** — edit them in place |
| `my_work/` | scripts you write yourself (the checks in A1 and A3) | **yes** — you create this folder |
| `weak_code/` | the instructor's deliberately weak code | no — read it, run it, never change it |

**Start every script you write in `my_work/` with these lines:**

```python
import pathlib, sys

TRACK = pathlib.Path(__file__).resolve().parents[1]   # the 2_asymmetric/ folder
sys.path.insert(0, str(TRACK / "starter"))            # lets you `import a1_rsa_oaep`
sys.path.insert(0, str(TRACK / "weak_code"))
```

## The rules

- **Dummy data only.** Never use real data.
- **Do not design your own algorithms.** Use `cryptography`.
- **Private keys must not end up in the repository or in your evidence sheet.** The keys in this track are
  generated in memory each time you run; if you ever save one, save it outside the repository.
- Encryption does not replace access control.

## Session timeline (about 40 of the 75 practice minutes of Session 2)

| Min | Step | Files | Evidence for the sheet |
|---|---|---|---|
| 10 | **A1** Build RSA-OAEP | `starter/a1_rsa_oaep.py` | `round-trip: True`, two different encryptions |
| 10 | **A2** RSA without padding is deterministic | `weak_code/weak_rsa_no_padding.py` | `identical? True` vs OAEP `False` |
| 20 | **A3** Large data: hybrid encryption | `weak_code/weak_rsa_large_data.py`, `starter/a3_hybrid.py` | the 190-byte limit; a 10,000-byte round-trip |
| after | **A4** RSA-PSS signature | `5_homework/starter/a4_signature.py` | original valid; tampered `InvalidSignature` |

## Step-by-step guide

### Step A1 — Build RSA-OAEP (10 min)

**Goal.** Encrypt and decrypt a small message with RSA the correct way. OAEP adds randomness, so encrypting the same
message twice gives two different ciphertexts.

**Do**
1. Open `2_asymmetric/starter/a1_rsa_oaep.py`. Replace `raise NotImplementedError(...)` in the three functions:

   | Function | What it must do |
   |---|---|
   | `generate_key()` | return an RSA **private key** with `key_size=2048` and `public_exponent=65537` |
   | `encrypt_oaep(pub, message)` | encrypt with `padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)` |
   | `decrypt_oaep(priv, ciphertext)` | decrypt with exactly the same OAEP settings |

2. Run the built-in check:

**Run**
```bash
python3 2_asymmetric/starter/a1_rsa_oaep.py
```

**Expected** — exactly these two lines:
```
round-trip: True
two encryptions identical? False
```

3. Now find RSA's size limit. Create `2_asymmetric/my_work/a1_limit.py` (boilerplate lines first, then `import a1_rsa_oaep as tools`).
   It must generate a key and try to encrypt `b"x" * 190` and then `b"x" * 191` with `encrypt_oaep`, catching `ValueError`,
   and print one line for each.

**Run**
```bash
python3 2_asymmetric/my_work/a1_limit.py
```

**Expected** — your script prints:
```
190 bytes: ok
191 bytes: ValueError
```

**Record** (row `A1`): payload = "ran the starter check and `a1_limit.py`"; evidence = the two expected lines of each; fix = "this is the
correct design (OAEP padding, 2048-bit key)"; re-test = the same lines. Note the limit: **190 bytes**.

**Done when** both programs print what is expected and you know why a 191-byte message is rejected.

**If stuck:** `ValueError: Decryption failed` means you decrypted with different OAEP settings than you encrypted with, or with a key
that does not belong to the public key.

### Step A2 — RSA without padding is deterministic (10 min)

**Goal.** See why "bare" (textbook) RSA is broken: the same message always produces the same ciphertext. That lets an attacker
recognise repeated messages and test guesses without ever having the key.

**Do**
1. Read `2_asymmetric/weak_code/weak_rsa_no_padding.py`. Find `encrypt_no_padding` — it is only `pow(m, e, n)`. Do not edit it.
2. Run it:

**Run**
```bash
python3 2_asymmetric/weak_code/weak_rsa_no_padding.py
```

**Expected** — the ciphertext hex values differ on each run, but these two lines are always there (the first in the "WITHOUT PADDING"
block, the second in the "OAEP" block):
```
  identical?       True  <-- weakness R-1
  identical?       False  <-- the randomness works
```

3. Answer in your evidence sheet (2–3 sentences each):
   - Why is "the same message gives the same ciphertext" dangerous? Describe an attacker who knows an order status is
     one of only three words and only has the public key.
   - What does OAEP add that fixes it?

**Record** (row `A2`): vulnerable code = `weak_rsa_no_padding.py`, `encrypt_no_padding`; payload = "encrypted the same message twice
and compared the ciphertexts"; evidence = the two `identical?` lines; fix = "RSA-OAEP (Step A1)"; re-test = "two OAEP encryptions
of the same message differ (`identical? False`)".

**Done when** you can explain the dictionary attack in your own words.

### Step A3 — RSA cannot encrypt a large file: build hybrid encryption (20 min)

**Goal.** RSA can only encrypt a few hundred bytes. Real systems encrypt the **data** with a random AES key (GCM) and use RSA only to
wrap that small AES key. You build that, and make it fail safely on bad input.

**Do**
1. See the problem first:

**Run**
```bash
python3 2_asymmetric/weak_code/weak_rsa_large_data.py
```

**Expected**
```
data size     : 1000 bytes
RSA-OAEP limit: 190 bytes (2048-bit key, SHA-256)
succeeded?    : False  <-- limitation R-3
```

2. Open `2_asymmetric/starter/a3_hybrid.py` and implement the two functions. The package you produce has this exact layout:

   | Part | Size | Content |
   |---|---|---|
   | length header | 2 bytes, big-endian | the length of the wrapped key (256 for a 2048-bit key) |
   | wrapped key | that many bytes | the random AES-256 key, encrypted with RSA-OAEP |
   | nonce | 12 bytes | a new random nonce |
   | body | the rest | AES-GCM ciphertext + 16-byte tag |

   - `hybrid_encrypt(data, pub)`: make a random 256-bit AES key; encrypt `data` with AES-GCM and a new random nonce; wrap the AES key with
     RSA-OAEP; return `length_header + wrapped_key + nonce + body`. (Hint: `len(wrapped).to_bytes(2, "big")`.)
   - `hybrid_decrypt(package, priv)`: **check lengths before slicing** — a package shorter than 2 bytes, a header of 0, or a package too short
     for header + wrapped key + 12-byte nonce + 16-byte tag must raise `ValueError`. Then unwrap the key with `priv.decrypt` and decrypt the body.
     (Hint: `int.from_bytes(package[:2], "big")`.)

3. Run the built-in check:

**Run**
```bash
python3 2_asymmetric/starter/a3_hybrid.py
```

**Expected**
```
10000 bytes: round-trip True
```

4. Prove it handles bad input. Create `2_asymmetric/my_work/a3_checks.py` (boilerplate first, then `import a3_hybrid as hybrid`) that generates two
   different RSA keys and prints exactly the five lines below. How to get each one: (a) round-trip 10,000 random bytes (`os.urandom`) through
   key 1; (b) decrypt a valid package with **key 2**; (c) keep only the **first 100 bytes** of a valid package (shorter than header + wrapped key + nonce + tag); (d) pass `b""`;
   (e) flip the **last byte** of a valid package (`ValueError` for b, c, d; `InvalidTag` from `cryptography.exceptions` for e).
   Good to know: a package cut somewhere *inside* the body is long enough to parse, so it is GCM's authentication that rejects it
   (`InvalidTag`) — that is also correct behaviour.

**Run**
```bash
python3 2_asymmetric/my_work/a3_checks.py
```

**Expected** — your script prints:
```
round-trip 10000 bytes: True
wrong key: ValueError
truncated package: ValueError
empty package: ValueError
tampered data: InvalidTag
```

**Record** (row `A3`): vulnerable code = `weak_rsa_large_data.py`; payload = "encrypted a 1 KB export directly with RSA-OAEP, then through my hybrid
function"; evidence = the 190-byte limit lines and the five lines of `a3_checks.py`; fix = "hybrid encryption: AES-GCM for data, RSA-OAEP to
wrap the AES key"; re-test = the `a3_checks.py` output.

**Done when** all five lines match and you can say why RSA alone is the wrong tool for files.

**If stuck:** `IndexError` or a hang on a truncated package means you sliced before checking the length. `ValueError: Ciphertext length must be equal to key size`
means the wrapped-key slice has the wrong length — check the 2-byte header arithmetic.

## How to fill in an evidence-sheet row

Open `2_asymmetric/evidence_sheet.md`. One row per step, five columns. Example (for a step you will not do — write your own):

| Case | Vulnerable code (file/line) | Your payload / test step | Output evidence | Fix | Re-test result |
|---|---|---|---|---|---|
| A1 RSA-OAEP done right | — (correct design) | ran the starter check and tried 190 vs 191 bytes | `round-trip: True`; `191 bytes: ValueError` | not needed | same output on a second run |

Rules for the sheet: short and checkable; paste real output; **never paste a private key**.

## When you are stuck

| What you see | Most likely cause | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'cryptography'` | the environment is not active | activate it again and re-run `pip install -r requirements.txt` |
| `command not found: python3` (Windows) | Windows uses another launcher | use `py` instead of `python3` |
| `NotImplementedError: A1: generate_key` | a starter function is still empty | fill it in, as described in the step |
| `ValueError: Decryption failed` | wrong key, or different OAEP settings on each side | use the same `OAEP(...)` object settings and the matching key |
| `ModuleNotFoundError: No module named 'a1_rsa_oaep'` | the boilerplate lines are missing from your script | paste the `sys.path.insert` lines from "Before you start" |
| key generation feels slow | 2048-bit RSA takes a moment | normal — wait a second |

If you are still blocked after 5 minutes on one step, move on to the next one and ask the instructor.

## What you hand in from this track

- Your completed `starter/a1_rsa_oaep.py` and `starter/a3_hybrid.py` and the scripts in `my_work/`, in your repository — **without any key**.
- `2_asymmetric/evidence_sheet.md`, filled in.
- After the session: A4 (RSA-PSS signatures) and the automated tests for this track (`test_asymmetric.py`: 2 base + 2 optional).
  See **`5_homework/README.md`**.
