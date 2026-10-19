# Track 3 — Hashing and Password Storage

**Session 2 · Week 4 · about 35 of the 75 practice minutes (the rest is Track 2) · individual work**

Part of Practical 2 (BAB 2) and of Assignment 2 — Cryptography: build, misuse, fix (*Tugas 2*,
rubric C2). Same pattern as the other tracks: **build it correctly → break the weak version → fix it and prove it**.

## What you will do in this track

1. **Build** correct password storage: a salted, slow hash (PBKDF2).
2. **Break** a leaked database of unsalted MD5 hashes with a wordlist — as an attacker would.
3. **Measure** how much slower a proper password hash makes every guess.
4. **Write down evidence** for each one in your evidence sheet. After the session you also do H4 (plain hash vs HMAC); it is
   described in `5_homework/README.md`.

You never design your own hash. You use `hashlib`/`hmac` from the standard library. The attack runs **only** against
this lab's dummy `user_dump.csv`.

## Before you start (once, about 5 minutes)

**Every command in this guide is run from the `BAB2_Kripto/` folder.** Open a terminal there first.

If you already did the setup in Track 1 or 2, only re-activate the environment and skip to step 3. Otherwise:

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
4. Create the folder for the scripts you write yourself: `3_hash/my_work/` (it does not exist yet — make it).
5. Keep `3_hash/evidence_sheet.md` open. You fill one row per step as you go.

**Where you may write — Never edit anything in `weak_code/` or `artifacts/`.**

| Folder | What it holds | You may edit it? |
|---|---|---|
| `starter/` | the two files you complete (`h1_salted_hash.py`, `h3_kdf.py`) | **yes** — edit them in place |
| `my_work/` | scripts you write yourself (H1 checks, H2 attack, H3 comparison) | **yes** — you create this folder |
| `weak_code/` | the instructor's deliberately weak code | no — read it, run it, never change it |
| `artifacts/` | the leaked dump and the wordlist | no — read them, never change them |

**Start every script you write in `my_work/` with these lines:**

```python
import pathlib, sys

TRACK = pathlib.Path(__file__).resolve().parents[1]   # the 3_hash/ folder
sys.path.insert(0, str(TRACK / "starter"))            # lets you `import h1_salted_hash`
sys.path.insert(0, str(TRACK / "weak_code"))          # lets you `import weak_hash_no_salt`
```

## The rules

- **Dummy data only.** The 12 users and their passwords are fake. Never attack anything else.
- **Do not design your own algorithms.** Use `hashlib` and `hmac`.
- **Do not write real or lab passwords/keys into your evidence sheet** beyond what the step asks for.
- A hash is not encryption: you cannot "decrypt" it, you can only guess and compare.

## Session timeline (about 35 of the 75 practice minutes of Session 2)

| Min | Step | Files | Evidence for the sheet |
|---|---|---|---|
| 10 | **H1** Salted hashing (PBKDF2) | `starter/h1_salted_hash.py` | two different hashes; correct/wrong verification |
| 15 | **H2** Crack the MD5 dump with a wordlist | `weak_code/weak_hash_no_salt.py`, `artifacts/user_dump.csv` | the users that fell + an explanation for the rest |
| 10 | **H3** Fix it with a KDF | `starter/h3_kdf.py` | the MD5 vs KDF time-per-guess ratio |
| after | **H4** Plain SHA-256 vs HMAC | `5_homework/starter/h4_integrity.py` | file modified: the plain hash passes, HMAC fails |

## Step-by-step guide

### Step H1 — Build salted password hashing (10 min)

**Goal.** Store a password so that (a) the same password gives a different stored value every time (the **salt**), and
(b) every guess is slow for an attacker (many **iterations**).

**Do**
1. Open `3_hash/starter/h1_salted_hash.py`. Replace `raise NotImplementedError(...)` in the two functions:

   | Function | What it must do |
   |---|---|
   | `make_hash(password, iterations=600_000)` | make a random 16-byte salt (`os.urandom(16)`); compute `hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)`; return one string `pbkdf2_sha256$<iterations>$<salt_base64>$<hash_base64>` |
   | `check(password, stored)` | split the string on `$`; recompute with the **stored** salt and iterations; compare with `hmac.compare_digest`; return `True`/`False` |

   `check` must raise `ValueError` (not crash with another error) if the stored string is malformed (wrong number of parts,
   bad base64), names another algorithm, or has an iteration count of 0 or less or absurdly large (over 10,000,000).
   A **wrong password is not an error**: it returns `False`.

2. Run the built-in check:

**Run**
```bash
python3 3_hash/starter/h1_salted_hash.py
```

**Expected** — exactly these three lines:
```
two hashes differ? True
correct password verifies? True
wrong password verifies? False
```

3. Prove it rejects bad input. Create `3_hash/my_work/h1_checks.py` (boilerplate first, then `import h1_salted_hash as salted`) that prints exactly the
   three lines below. How to get each one: (a) call `check("x", "not a hash")`; (b) call `check("x", "md5$1000$AAAA$AAAA")`; (c) call
   `check("x", "pbkdf2_sha256$0$AAAA$AAAA")`. Each must raise `ValueError`, which you catch and report.

**Run**
```bash
python3 3_hash/my_work/h1_checks.py
```

**Expected** — your script prints:
```
malformed string: ValueError
other algorithm: ValueError
zero iterations: ValueError
```

**Record** (row `H1`): payload = "ran the starter check and `h1_checks.py`"; evidence = the three expected lines of each; fix = "this is the correct
design (salt per password, 600,000 iterations, constant-time compare)"; re-test = the same lines.

**Done when** all the lines match and you can say in one sentence what the salt is for and what the iterations are for.

**If stuck:** `binascii.Error` or `IndexError` from `check` means you did not turn a malformed string into `ValueError` — wrap the split and decode steps in
`try ... except ValueError`. `TypeError` about bytes means you forgot `.encode()` on the password.

### Step H2 — Crack the leaked MD5 dump with a wordlist (15 min)

**Goal.** Experience why unsalted fast hashes are weak: you recover most passwords just by hashing common words and comparing — and the hashes
themselves reveal which users chose the same password.

**Do**
1. Look at the leaked database. It has two columns, `user` and `md5_hash`, and 12 dummy users:

**Run**
```bash
head -3 3_hash/artifacts/user_dump.csv
```
(Windows PowerShell: `Get-Content 3_hash\artifacts\user_dump.csv -TotalCount 3`)

**Expected**
```
user,md5_hash
andi,482c811da5d5b4bc6d497ffa98491e38
budi,8d4db54daf7d67db5f3c96e43f61c609
```

2. See the weak code that produced those hashes. It is plain MD5:

**Run**
```bash
python3 3_hash/weak_code/weak_hash_no_salt.py
```

**Expected** — the same line twice (that is the missing salt):
```
md5('password123') = 482c811da5d5b4bc6d497ffa98491e38
```

3. Write **your own** attack. Create `3_hash/my_work/wordlist_attack.py` (boilerplate first; `import weak_hash_no_salt as weak`). It must:
   1. read the 200 guesses in `3_hash/artifacts/small_wordlist.txt` (one per line);
   2. build a dictionary that maps `weak.store_password(word)` to `word`, for every word;
   3. read `3_hash/artifacts/user_dump.csv` with `csv.DictReader` (columns `user` and `md5_hash`);
   4. print `user: password` for every user whose hash is in your dictionary, and `user: not found` for every other user;
   5. finish with a line `cracked N of 12`.

**Run**
```bash
python3 3_hash/my_work/wordlist_attack.py
```

**Expected** — you will not get a fixed output, but check yourself with these facts: the output has 12 user lines plus the summary; **more than half
but not all** of the users are recovered; and exactly **two users** show the same password (their hashes are identical in the dump).

**Record** (row `H2`): vulnerable code = `weak_hash_no_salt.py` (`store_password`: MD5, no salt; `check_password`: `==`); payload = "dictionary attack with
`small_wordlist.txt` against `user_dump.csv`"; evidence = the `cracked N of 12` line, the two users that share a hash, and the users that were **not** found;
fix = "a salted, slow KDF (Step H1)"; re-test = see Step H3.

Answer in the sheet (2–3 sentences each): why do two users show the same hash? Why did some users survive the attack?

**Done when** you have the `cracked N of 12` line, you can name the two users that share a hash, and you can explain why the others were not found.

**If stuck:** if nobody is found, check the hash is compared as a hex string and that you used `.strip()` on each wordlist line (a trailing newline changes
the hash).

### Step H3 — Fix it with a KDF and measure the cost per guess (10 min)

**Goal.** Prove that your salted PBKDF2 makes each guess thousands of times more expensive than MD5, so the attack from H2 stops being practical.

**Do**
1. Open `3_hash/starter/h3_kdf.py` and fill in `time_per_guess(hash_function, count=20)`: call `hash_function(f"guess{i}")` for `i` from 0 to `count - 1`,
   measure the total time with `time.perf_counter()`, and return the **average seconds per call**.
2. Create `3_hash/my_work/h3_compare.py` (boilerplate first; `import h1_salted_hash as salted`, `import h3_kdf`, `import weak_hash_no_salt as weak`). It must
   print exactly three lines:
   ```
   md5: <seconds> s per guess
   KDF: <seconds> s per guess
   KDF is about <ratio> times slower
   ```
   Use `count=20000` for MD5 and `count=3` for `salted.make_hash` (default 600,000 iterations).
3. Rewrite the login check the safe way. Create `3_hash/my_work/h3_login.py` with a function `login(password, stored)` that uses your `salted.check` (no `==`), and
   print two lines: `login ok: True` for a correct password and `login wrong password: False` for a wrong one.

**Run**
```bash
python3 3_hash/my_work/h3_compare.py
python3 3_hash/my_work/h3_login.py
```

**Expected**
- `h3_compare.py`: the three lines above, with real numbers. The **ratio must be at least 1,000** (typically it is tens of thousands).
- `h3_login.py`:
  ```
  login ok: True
  login wrong password: False
  ```

**Record** (row `H3`): vulnerable code = `weak_hash_no_salt.py`; payload = "measured time per guess for MD5 and for my PBKDF2 hash"; evidence = the three lines of
`h3_compare.py` with the ratio; fix = "salted PBKDF2-HMAC-SHA256, 600,000 iterations, `hmac.compare_digest`"; re-test = the `h3_login.py` lines.

**Done when** the ratio is above 1,000 and you can say what the attacker's wordlist attack would cost now.

## How to fill in an evidence-sheet row

Open `3_hash/evidence_sheet.md`. One row per step, five columns. Example (for a step you will not do — write your own):

| Case | Vulnerable code (file/line) | Your payload / test step | Output evidence | Fix | Re-test result |
|---|---|---|---|---|---|
| H1 salted hash done right | — (correct design) | ran the starter check and `h1_checks.py` | three expected lines; `ValueError` for the three bad strings | not needed | same output on a second run |

Rules for the sheet: short and checkable; paste real output.

## When you are stuck

| What you see | Most likely cause | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'cryptography'` | the environment is not active | activate it again and re-run `pip install -r requirements.txt` |
| `command not found: python3` (Windows) | Windows uses another launcher | use `py` instead of `python3` |
| `NotImplementedError: H1: make_hash` | a starter function is still empty | fill it in, as described in the step |
| `FileNotFoundError` for `artifacts/...` | you are not in `BAB2_Kripto/` | `cd` to `BAB2_Kripto/` and run the command again |
| `ModuleNotFoundError: No module named 'h1_salted_hash'` | the boilerplate lines are missing from your script | paste the `sys.path.insert` lines from "Before you start" |
| nobody is cracked in H2 | trailing newlines in the wordlist | `.strip()` every line before hashing |

If you are still blocked after 5 minutes on one step, move on to the next one and ask the instructor.

## What you hand in from this track

- Your completed `starter/h1_salted_hash.py` and `starter/h3_kdf.py` and the scripts in `my_work/`, in your repository.
- `3_hash/evidence_sheet.md`, filled in.
- After the session: H4 (plain SHA-256 vs HMAC) and the automated tests for this track (`test_hash.py`: 1 base + 3 optional).
  See **`5_homework/README.md`**.
