# Cryptography Practical Exam — Practical 2 (75 minutes, individual)

> **Language:** **English** | [Versi Bahasa Indonesia](exam_instructions_id.md)

> [!IMPORTANT]
> - Work strictly individually using only the files in your assigned package folder.
> - DO NOT write raw private keys to your report.
> - DO NOT work on any other package folder than the one assigned to you.
> - DO NOT work together with other students or share your answers.
> - DO NOT design custom encryption algorithms; use standard, vetted primitives from `cryptography` or standard libraries.
> - DO NOT use AI tools to generate your answers. You may use AI for clarifying questions about Python or cryptography syntax, but not for generating your deliverables. (**Consequences of AI-generated answers will be considered academic dishonesty and will result in a zero score for the station and also for the entire practical exam. Be careful when asking AI questions.**)
> - Work carefully and avoid typos; your answers must be reproducible by the instructor.
> - **ALL VIOLATIONS of the above rules will result in a zero score for the station and also for the entire practical exam.**

You receive one package folder (e.g., `package_A/`, `package_B/`, `package_C/`, `package_D/`, or `package_E/`) containing **three stations**.
Total time: **75 minutes** (recommended: **25 minutes per station**).
You may use Python, the standard library, the `cryptography` library, and your practical notes.

## Deliverables & Scoring Rubric

For **each** station, hand in an answer file in Markdown inside your assigned package directory:
- `answer_symmetric.md` (for `symmetric/`)
- `answer_asymmetric.md` (for `asymmetric/`)
- `answer_hash.md` (for `hash/`)

> [!TIP]
> **Code Workflow (Creating New Files vs. Editing Existing):**
> When developing your fixes for Section 3, **create a new file** (e.g., `fixed_daily_report.py`, `fixed_send_status.py`, `fixed_pin.py`) rather than overwriting the original vulnerable scripts. This preserves the original scripts so your Section 2 attack evidence remains reproducible and allows side-by-side verification.
> **Note:** Regardless of whether you create separate script files or edit in place, **you must copy your complete replacement code and verification output directly into Section 3 (`## 3. Fix`) of your Markdown answer file**, as the grading tool evaluates the Markdown reports.

Each answer file is evaluated according to the course **RPS Practical Rubric (Rubrik C2 — Praktikum Defensif)** across four assessment dimensions (100 points per station):

1. **Accuracy of Results / Ketepatan Hasil (35 points)**
   - **Finding (10 pts)**: Accurately identify the cryptographic weakness and its exact location (file name and line numbers).
   - **Evidence (25 pts)**: Provide reproducible execution commands/code with 100% accurate data recovery or exploit proof.
2. **Method & Security Implementation / Metode & Pengamanan (25 points)**
   - **Fix Implementation (25 pts)**: Provide working Python replacement code that fixes the weakness using standard, vetted primitives from `cryptography` or standard libraries without hardcoded secrets.
3. **Verification Proof & Boundaries / Verifikasi & Batasan (25 points)**
   - **Verification Proof (15 pts)**: Verifiable execution proof showing that the earlier attack no longer succeeds against your fix.
   - **Security Boundaries & Limitations (10 pts)**: Explicitly identify the operational limits and remaining boundaries of the defense (e.g., offline brute-force limits of low-entropy secrets, rate limiting requirements).
4. **Individual Explanation / Penjelasan Individu (15 points)**
   - **Explanation (15 pts)**: Explain concisely in your own words why the original weakness poses severe security risks in production systems.

## Stations Overview

| Station | Scenario and Provided Files | Target Objective |
|---|---|---|
| `symmetric/` | Daily warehouse reporting (`daily_report.py`, `report_monday.enc`, `report_tuesday.enc`) | Recover the plaintexts of both encrypted reports, demonstrate the underlying cryptographic flaw, and implement a secure file encryption fix. |
| `asymmetric/` | Order status transmission to a partner (`send_status.py`, `order_status.csv`, `public_key.pem`) | Recover the true status of all orders in `order_status.csv` using only the public key, identify why the current scheme is vulnerable, and implement a secure public-key transmission fix. |
| `hash/` | Cashier PIN storage in a legacy application (`weak_pin.py`, `pin_dump.csv`) | Crack and recover all 4-digit PINs from `pin_dump.csv`, explain the storage flaws, provide a secure credential storage fix, and explain remaining offline limits of 4-digit PINs. |

## Useful Commands for the Exam

### General Setup and Submission Validation
```bash
# Verify Python environment and cryptography library
python3 -c "import cryptography; print(cryptography.__version__)"

# Move into your assigned exam package
cd 4_practical_exam/package_A       # (or package_B, package_C, package_D, package_E, depending on your assignment)

# Validate your deliverables at any time during the exam
python3 validate_submission.py
```

---

### Station 1: `symmetric/` — Daily Warehouse Reports
```bash
cd symmetric

# 1. View script usage and available options
python3 daily_report.py

# 2. Decrypt encrypted warehouse reports using the provided script
python3 daily_report.py decrypt report_monday.enc
python3 daily_report.py decrypt report_tuesday.enc

# 3. Test encrypting data with the script
python3 daily_report.py encrypt <input_file> <output_file>
```

---

### Station 2: `asymmetric/` — Partner Order Status Transmission
```bash
cd ../asymmetric

# 1. View script usage and accepted statuses
python3 send_status.py

# 2. Encrypt candidate statuses to observe how the script generates ciphertexts
python3 send_status.py PROCESSING
python3 send_status.py PENDING
python3 send_status.py SHIPPED

# 3. Inspect the encrypted order status records
head -n 5 order_status.csv
```

---

### Station 3: `hash/` — Legacy Cashier PIN Storage
```bash
cd ../hash

# 1. View script usage
python3 weak_pin.py

# 2. Compute the hash of candidate PINs using the script
python3 weak_pin.py 1234
python3 weak_pin.py 0000

# 3. Inspect the leaked cashier hash dump
head -n 5 pin_dump.csv
```

---

## Evaluation Guidance for Section 3 (Fix & Verification Proof)

To earn full points for **Section 3 (Fix)**, your report must provide working Python replacement code and include verifiable proof that the earlier exploit fails:

### 1. Station 1 (`symmetric/`) — File Encryption Fix
- **Objective:** Fix the file encryption implementation so that confidential reports are protected even when encrypting multiple files under the same key.
- **Guidance:** Inspect how keys and initialization parameters are handled in `daily_report.py`. Under what conditions does repeated encryption leak relationships between plaintexts? How should initialization data be managed so that recipients can decrypt independently without compromising confidentiality?
- **Proof Requirement:** Execute your fixed code on two test messages and demonstrate that ciphertexts no longer leak plaintext relationships or cross-message patterns.

### 2. Station 2 (`asymmetric/`) — Order Status Transmission Fix
- **Objective:** Replace the broken public-key mechanism with a secure public-key encryption scheme that protects message confidentiality.
- **Guidance:** Investigate why the current public-key implementation allows an eavesdropper to determine the contents of an encrypted message without possessing the private key, especially when the message space is small. What standard mechanism ensures that repeated encryptions of the same plaintext cannot be identified or precomputed?
- **Proof Requirement:** Encrypt candidate status messages multiple times with the public key and demonstrate that ciphertexts are completely randomized and resistant to precomputed dictionary lookup.

### 3. Station 3 (`hash/`) — PIN Storage Fix
- **Objective:** Replace the weak legacy hash storage with a modern credential storage implementation.
- **Guidance:** Investigate why storing raw hashes is unsafe for user credentials. How can a storage scheme ensure that two users who choose the exact same PIN do not end up with identical stored values? How can the work factor be increased to deter offline brute-force guessing?
- **Proof Requirement:** Store the same 4-digit PIN for two different test accounts and demonstrate that their stored values are completely distinct, while your verification routine correctly authenticates the valid PIN and rejects an invalid PIN.

## Self-Validating Your Submission

Your package folder includes `validate_submission.py`. Run it at any time from your assigned package root:

```bash
python3 validate_submission.py
```

This automated validator checks that:
- All three answer files (`answer_symmetric.md`, `answer_asymmetric.md`, `answer_hash.md`) are present.
- All four required sections (Finding, Evidence, Fix, Explanation) exist in each file.
- No unedited template placeholders (`<...>`) remain.
- No raw private key text is committed.

## Answer File Template

Use this structure for each station report:

```markdown
# Station Answer: <symmetric | asymmetric | hash>

## 1. Finding
- Weakness: <Concise description of the flaw>
- Location: <filename>:<line_numbers>

## 2. Evidence
<Python code used to recover data or demonstrate the exploit>

Output:
<Execution output demonstrating recovered data or attack result>

## 3. Fix
<Corrected Python implementation>

Verification Proof:
<Output proving that the attack fails against the new implementation>

## 4. Explanation
<One paragraph explaining why this flaw is dangerous in production systems, followed by an analysis of remaining operational boundaries or limitations.>
```
