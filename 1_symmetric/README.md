# Track 1 — Symmetric Cryptography

**Session 1 · Week 3 · 150 minutes · individual work**

Part of Practical 2 (BAB 2) and of Assignment 2 — Cryptography: build, misuse, fix (*Tugas 2*,
rubric C2). Every exercise follows the same pattern: **build it correctly → break the weak
version → fix it and prove it**.

## What you will do in this session

1. **Warm up** by breaking a toy cipher (Caesar) in a few lines of code.
2. **Build** a correct encrypted file vault with AES-GCM (the standard way to do symmetric encryption).
3. **Break four weak examples** the instructor prepared: ECB mode, an edited ECB ciphertext, a reused
   nonce, and a key hidden inside code.
4. **Write down evidence** for each one in your evidence sheet.

You never design your own cipher. You use the `cryptography` library, and you attack code that was
written badly on purpose.

## Before you start (once, about 5 minutes)

**Every command in this guide is run from the `BAB2_Kripto/` folder.** Open a terminal there first.

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
4. Create the folder for the scripts you write yourself: `1_symmetric/my_work/`
   (it does not exist yet — make it).
5. Open `1_symmetric/evidence_sheet.md` next to your editor. You fill one row per step as you go.

**Where you may write — Never edit anything in `weak_code/` or `artifacts/`.**

| Folder | What it holds | You may edit it? |
|---|---|---|
| `starter/` | the two files you complete (`c1_caesar.py`, `s1_vault_gcm.py`) | **yes** — edit them in place |
| `my_work/` | scripts you write yourself (S2–S6) | **yes** — you create this folder |
| `weak_code/` | the instructor's deliberately weak code | no — read it, run it, never change it |
| `artifacts/` | the encrypted files you attack | no — read them, never change them |
| `tools/` | a helper for Step S3 | no |

**Start every script you write in `my_work/` with these lines.** They let you import the starter and
weak files:

```python
import pathlib, sys

TRACK = pathlib.Path(__file__).resolve().parents[1]   # the 1_symmetric/ folder
sys.path.insert(0, str(TRACK / "starter"))            # lets you `import s1_vault_gcm`
sys.path.insert(0, str(TRACK / "weak_code"))          # lets you `import weak_ecb`
```

## The rules

- **Dummy data only.** Everything in this folder is fake. Never use real data.
- **Do not design your own algorithms.** Use `AESGCM` from the `cryptography` library.
- **Keys must not end up in the repository or in your evidence sheet.** Write *how you got a key*,
  never its value. Read keys from files or from the code at runtime; do not paste them into your scripts.
- Encryption does not replace access control.

## Session timeline (150 minutes)

| Min | Step | Files | Evidence for the sheet |
|---|---|---|---|
| 5 | Introduction | — | — |
| 15 | **C1–C2** Warm-up: build the Caesar cipher, then break it | `starter/c1_caesar.py`, `artifacts/caesar_message.txt` | readable message; keyspace 25 (not graded) |
| 25 | **S1** An AES-GCM file vault | `starter/s1_vault_gcm.py` | `round-trip: True` |
| 10 | **S2** Detect modification | `my_work/s2_checks.py` | `InvalidTag` |
| 25 | **S3** ECB leaks patterns | `weak_code/weak_ecb.py`, `tools/compare_blocks.py` | identical blocks |
| 15 | **S4** ECB: a moved block goes undetected | `artifacts/order_ecb_a.enc` | decryption succeeds with no error; GCM → `InvalidTag` |
| 25 | **S5** A reused GCM nonce | `weak_code/weak_fixed_nonce.py`, `artifacts/reused_nonce_*` | second plaintext recovered **without the key** |
| 20 | **S6** An embedded key | `weak_code/weak_embedded_key.py`, `artifacts/order_vault.enc` | the decrypted JSON |
| 10 | Wrap-up | `1_symmetric/evidence_sheet.md` | every row filled in |

## Step-by-step guide

### Step C1–C2 — Warm-up: build and break the Caesar cipher (15 min, not graded)

**Goal.** Caesar shifts every letter by a fixed number. You build it, then break it by trying every
possible key. It shows why a small keyspace is fatal. Caesar is a toy: never use it for real data.

**Do**
1. Open `1_symmetric/starter/c1_caesar.py`.
2. Replace `raise NotImplementedError(...)` in the three functions with working code:

   | Function | What it must do |
   |---|---|
   | `caesar_encrypt(text, shift)` | shift each letter `A–Z` and `a–z` forward by `shift`, wrapping around after `z`; **keep upper/lower case**; leave digits, spaces and punctuation unchanged; accept negative shifts and shifts of 26 or more |
   | `caesar_decrypt(text, shift)` | the exact inverse |
   | `brute_force(ciphertext)` | return a list of 25 pairs `(shift, decrypted_text)` for shifts 1 to 25 |

3. Run it. It reads `artifacts/caesar_message.txt` for you and prints every candidate.

**Run**
```bash
python3 1_symmetric/starter/c1_caesar.py
```

**Expected** — the first two lines below, then 25 candidate lines like `  shift  4: ...`. **Exactly one** candidate is readable
English and starts with `ORDER-`; finding it (and its shift number) is the point of the step:
```
round-trip: True
keyspace: 25
```

**Record** (row `C1–C2`): payload = "ran `brute_force` on `caesar_message.txt`"; evidence = the readable line and its
shift; fix = "use AES-GCM instead (Step S1)"; re-test = "not applicable, it is a toy cipher".

**Done when** you see `round-trip: True`, you know which shift made the message readable, and you can say in
one sentence why 25 possible keys is nothing compared with the 2²⁵⁶ keys of AES-256.

**If stuck:** `round-trip: False` usually means upper/lower case was not preserved, or letters wrapped wrongly
after `z`/`Z`. Test `caesar_encrypt("xyz", 3)` — it must give `abc`.

### Step S1 — Build an AES-GCM file vault (25 min)

**Goal.** Encrypt and decrypt data correctly with AES-GCM. GCM both hides the data **and** detects any change.

**Do**
1. Open `1_symmetric/starter/s1_vault_gcm.py`. Fill in the seven functions:

   | Function | What it must do |
   |---|---|
   | `create_key()` | return 32 random bytes (an AES-256 key) — use `AESGCM.generate_key(bit_length=256)` |
   | `save_key(key, path)` | create the folder if needed, write the key to `path`, and make the file readable by you only (permissions `0600`) |
   | `load_key(path)` | read the file and return the key; raise `ValueError` if it is not exactly 32 bytes |
   | `encrypt_data(key, data)` | make a **new random 12-byte nonce for every message** (`os.urandom(12)`); return `nonce + ciphertext` (the 16-byte tag is already part of the ciphertext) |
   | `decrypt_data(key, package)` | if `len(package) < 28` raise `ValueError`; split off the first 12 bytes as the nonce; decrypt the rest; let `InvalidTag` propagate if the data was changed or the key is wrong |
   | `encrypt_file(key, src, dst)` | read `src`, write `encrypt_data(...)` to `dst` |
   | `decrypt_file(key, src, dst)` | read `src`, decrypt, and write `dst` **only if decryption succeeded** |

2. Run the built-in check:

**Run**
```bash
python3 1_symmetric/starter/s1_vault_gcm.py
```

**Expected** — exactly these two lines (the second one is Step S2 happening inside the demo):
```
round-trip: True
tampered ciphertext rejected: InvalidTag
```

3. Check that your key file handling works. Create `1_symmetric/my_work/s1_key_check.py`:
   ```python
   import pathlib, sys
   TRACK = pathlib.Path(__file__).resolve().parents[1]
   sys.path.insert(0, str(TRACK / "starter"))
   import s1_vault_gcm as vault

   path = pathlib.Path.home() / ".lab_keys" / "vault.key"    # outside the repository
   key = vault.create_key()
   vault.save_key(key, str(path))
   print(vault.load_key(str(path)) == key)
   ```
   Run `python3 1_symmetric/my_work/s1_key_check.py`. It must print `True`. On macOS/Linux,
   `ls -l ~/.lab_keys/vault.key` must show `-rw-------`.

**Record** (row `S1–S2`): payload = "ran the starter demo"; evidence = the two expected lines; fix = "this is the
correct design (random nonce, authenticated encryption, key outside the repository)"; re-test = the same two lines.

**Done when** both expected lines appear, the key check prints `True`, and the key file lives outside the repository.

**If stuck:** `InvalidTag` on a normal round-trip means the nonce was cut off or not saved: the file must be
`nonce + ciphertext`. `TypeError` about bytes/str means you passed a `str` where bytes are needed.

### Step S2 — Prove that any modification is detected (10 min)

**Goal.** Show that GCM refuses tampered data, a wrong key, and truncated input — with clear errors and no half-written output.

**Do**
1. Create `1_symmetric/my_work/s2_checks.py` (start with the three boilerplate lines from "Before you start", then `import s1_vault_gcm as vault`).
2. In it, build the three checks below with your own code.

**Run**
```bash
python3 1_symmetric/my_work/s2_checks.py
```

**Expected** — your script prints exactly these three lines:
```
wrong key: InvalidTag
short package: ValueError
no output file left: True
```
How to get each one: (a) encrypt with one key, decrypt with a **different** key; (b) call `decrypt_data` with
`b"x" * 10`; (c) write 40 zero bytes to a temporary file, call `decrypt_file` on it, catch the error, and check that
the destination file does **not exist**.

**Record** (row `S1–S2`, same row as S1): add "wrong key, short input and corrupt file are all rejected" to the evidence.

**Done when** all three lines match.

### Step S3 — ECB mode leaks patterns (25 min)

**Goal.** See with your own eyes that ECB encrypts identical plaintext blocks into identical ciphertext blocks, so
the structure of the data stays visible without the key.

**Do**
1. Read `1_symmetric/weak_code/weak_ecb.py`. Find the line that selects ECB (`modes.ECB()`). Do not edit it.
2. Run it. It re-creates the two artifacts (with the same bytes as before — that is harmless) and prints their blocks:
3. Run the comparison tool:
4. Repeat the comparison with AES-GCM. Create `1_symmetric/my_work/s3_gcm_blocks.py` that uses your `encrypt_data`
   to encrypt the plaintext `b"EMPTY-----------" * 5` (80 bytes) **twice**, saving the results as
   `1_symmetric/my_work/gcm_a.enc` and `1_symmetric/my_work/gcm_b.enc`. Then run the tool on those two files.

**Run**
```bash
python3 1_symmetric/weak_code/weak_ecb.py
python3 1_symmetric/tools/compare_blocks.py
python3 1_symmetric/my_work/s3_gcm_blocks.py
python3 1_symmetric/tools/compare_blocks.py 1_symmetric/my_work/gcm_a.enc 1_symmetric/my_work/gcm_b.enc
```

**Expected**
- `compare_blocks.py` on the instructor's files marks repeated blocks and ends with:
  ```
  identical blocks at the same position: [0, 1, 2, 5]
    - 4 of 6 ciphertext blocks are identical across the two files.
  ```
- `compare_blocks.py` on your two GCM files ends with:
  ```
  identical blocks at the same position: none
  ```

**Record** (row `S3`): vulnerable code = `weak_ecb.py`, the `modes.ECB()` line; payload = "compared the blocks of
`order_ecb_a.enc` and `order_ecb_b.enc` with `compare_blocks.py`"; evidence = the `[0, 1, 2, 5]` line and which blocks
repeat; fix = "AES-GCM, as in Step S1"; re-test = the `none` line for your GCM files.

**Done when** you can explain in two sentences why block 1, 2 and 3 of `order_ecb_a.enc` are identical, and why
the GCM files show `none` even though you encrypted the same plaintext twice.

### Step S4 — A moved ECB block goes undetected (15 min)

**Goal.** ECB has no authentication: you can rearrange blocks of someone else's ciphertext and the receiver decrypts it
without any error. GCM refuses the same trick.

**Do**
1. Create `1_symmetric/my_work/s4_move_block.py` with this start:
   ```python
   import pathlib, sys
   TRACK = pathlib.Path(__file__).resolve().parents[1]
   sys.path.insert(0, str(TRACK / "starter"))
   sys.path.insert(0, str(TRACK / "weak_code"))
   import weak_ecb
   import s1_vault_gcm as vault

   data = (TRACK / "artifacts" / "order_ecb_a.enc").read_bytes()
   blocks = [data[i:i + 16] for i in range(0, len(data), 16)]   # 6 blocks of 16 bytes
   # YOUR CODE: copy blocks[4] (the order line) over blocks[1] (the first EMPTY slot)
   # YOUR CODE: join the blocks, call weak_ecb.decrypt_ecb(...) and print the result
   ```
2. Finish the two `YOUR CODE` lines. You never use the key: `decrypt_ecb` is the vault's own function.
3. Add the GCM part: encrypt any 80 bytes with your `vault.create_key()` / `vault.encrypt_data(...)`, **swap two
   16-byte blocks of the ciphertext body** (skip the first 12 nonce bytes), and call `vault.decrypt_data(...)`.

**Run**
```bash
python3 1_symmetric/my_work/s4_move_block.py
```

**Expected**
- The ECB part prints the edited plaintext **with no error**:
  ```
  ORDER-VAULT-----ORDER-0000001---EMPTY-----------EMPTY-----------ORDER-0000001---
  ```
- The GCM part must end with the error `InvalidTag` (catch it and print `InvalidTag`).

**Record** (row `S4`): vulnerable code = `weak_ecb.py` (no authentication); payload = "copied block 4 over block 1";
evidence = the line above; fix = "AES-GCM"; re-test = "the same swap on GCM raises `InvalidTag`".

**Done when** both results appear and you can say who could abuse this in a real order system.

### Step S5 — A reused GCM nonce lets you read a message without the key (25 min)

**Goal.** GCM is only safe if every message gets a **new** nonce. Two messages encrypted with the same key **and**
the same nonce share one keystream, so `C1 xor C2 = P1 xor P2`. If you know one plaintext, you get the other.

**Do**
1. Read `1_symmetric/weak_code/weak_fixed_nonce.py` and find `FIXED_NONCE`. The **key is not provided** — you will not need it.
2. Create `1_symmetric/my_work/s5_nonce_reuse.py`:
   ```python
   import pathlib
   TRACK = pathlib.Path(__file__).resolve().parents[1]
   c1 = (TRACK / "artifacts" / "reused_nonce_1.enc").read_bytes()
   c2 = (TRACK / "artifacts" / "reused_nonce_2.enc").read_bytes()
   p1 = (TRACK / "artifacts" / "reused_nonce_1.txt").read_bytes()   # the leaked plaintext of message 1
   n = len(p1)   # 63 bytes: the last 16 bytes of each ciphertext are the tag, ignore them
   # YOUR CODE: p2 = bytes with p2[i] = c1[i] ^ c2[i] ^ p1[i] for every i in range(n)
   print(p2.decode())
   ```
3. Then show the fix works: with your `encrypt_data` (random nonce), encrypt two messages of equal length, run the same XOR on
   the ciphertext bodies (skip the 12 nonce bytes) and print whether the recovered text equals message 2.

**Run**
```bash
python3 1_symmetric/my_work/s5_nonce_reuse.py
```

**Expected**
- Your script prints the second message, recovered without any key:
  ```
  REPORT|2026-03-03|status=SHIPPED___|amount=07850000|warehouse=B
  ```
- For the fixed version your script prints `False` (the attack no longer recovers the message).

**Record** (row `S5`): vulnerable code = `weak_fixed_nonce.py`, `FIXED_NONCE`; payload = "`C1 xor C2 xor P1` over the first 63
bytes"; evidence = the recovered line; fix = "a random nonce per message, stored as `nonce + ciphertext`"; re-test = "the
attack on the fixed code prints `False`".

**Done when** you recovered the message and you can explain why nobody needed the key.

**If stuck:** you must XOR three byte strings position by position (`zip(c1, c2, p1)`). If the output is gibberish you
probably included the 16 tag bytes, or XOR-ed against the wrong file.

### Step S6 — A key embedded in the code (20 min)

**Goal.** If the key sits next to the encrypted data (or in the same code), the encryption protects nothing. You will
recover a key from source code and decrypt a file you were never given a key for.

**Do**
1. Read `1_symmetric/weak_code/weak_embedded_key.py`. Search for long base64 strings (20+ characters):

**Run**
```bash
grep -nE '"[A-Za-z0-9+/]{20,}={0,2}"' 1_symmetric/weak_code/weak_embedded_key.py
```
(Windows PowerShell: `Select-String -Pattern '"[A-Za-z0-9+/]{20,}={0,2}"' 1_symmetric\weak_code\weak_embedded_key.py`)

**Expected** — one match (your line number may differ):
```
38:_TEMPLATE_CACHE_B64 = "TGFiS2V5Rm9yQkFCMlZhdWx0Q3liZXJTZWN1cmUhISE="
```
2. Decode it: base64-decoded it is 32 bytes (an AES-256 key). The nonce is the shorter base64 string `_IV_DEFAULT` (12 bytes).
3. Create `1_symmetric/my_work/s6_recover_key.py`. **Read the key from the source at runtime — do not paste it into your script**:
   ```python
   import base64, json, pathlib, re
   from cryptography.hazmat.primitives.ciphers.aead import AESGCM

   TRACK = pathlib.Path(__file__).resolve().parents[1]
   source = (TRACK / "weak_code" / "weak_embedded_key.py").read_text()
   key = base64.b64decode(re.findall(r'"([A-Za-z0-9+/]{20,}={0,2})"', source)[0])
   nonce = base64.b64decode(re.search(r'_IV_DEFAULT = "([^"]+)"', source).group(1))
   ciphertext = (TRACK / "artifacts" / "order_vault.enc").read_bytes()
   # YOUR CODE: decrypt with AESGCM(key).decrypt(nonce, ciphertext, None) and print the JSON text
   ```
4. Run it.

**Run**
```bash
python3 1_symmetric/my_work/s6_recover_key.py
```

**Expected** — JSON that contains (among other fields):
```
"unit": "B2B Order Operations"
```

**Record** (row `S6`): vulnerable code = `weak_embedded_key.py`, `_TEMPLATE_CACHE_B64`; payload = "grep for base64 literals, decode,
decrypt with the fixed nonce"; evidence = the `"unit"` line (do **not** write the key); fix = "keep the key outside the code and the
repository (environment variable or a protected file) and use a random nonce"; re-test = "a short note on how the new design would stop the attack".

**Done when** you decrypted the vault without ever being handed the key and you wrote the fix in your own words.

## How to fill in an evidence-sheet row

Open `1_symmetric/evidence_sheet.md`. One row per step, five columns. Example (for a step you
will not do — write your own for yours):

| Case | Vulnerable code (file/line) | Your payload / test step | Output evidence | Fix | Re-test result |
|---|---|---|---|---|---|
| S2 detect modification | — (correct design) | flipped byte 12 of a GCM package with `package[12] ^= 1` | `InvalidTag` raised by `decrypt_data` | not needed: GCM already authenticates | wrong key → `InvalidTag`; 10 bytes → `ValueError` |

Rules for the sheet: short and checkable; paste real output; **never paste a key**.

## When you are stuck

| What you see | Most likely cause | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'cryptography'` | the environment is not active | activate it again (see "Before you start") and re-run `pip install -r requirements.txt` |
| `command not found: python3` (Windows) | Windows uses another launcher | use `py` instead of `python3` |
| `NotImplementedError: S1: create_key` | a starter function is still empty | fill it in, as described in the step |
| `InvalidTag` on a normal decrypt | nonce missing, cut off, or file changed | the stored data must be `nonce + ciphertext`; slice off exactly 12 bytes first |
| `FileNotFoundError` for `artifacts/...` | you are not in `BAB2_Kripto/` | `cd` to `BAB2_Kripto/` and run the command again |
| `ModuleNotFoundError: No module named 'weak_ecb'` | the boilerplate lines are missing from your script | paste the `sys.path.insert` lines from "Before you start" |

If you are still blocked after 5 minutes on one step, move on to the next one and ask the instructor.

## What you hand in from this track

- Your completed `starter/c1_caesar.py` and `starter/s1_vault_gcm.py` and the scripts in `my_work/`, in your repository —
  **without any key**.
- `1_symmetric/evidence_sheet.md`, filled in.
