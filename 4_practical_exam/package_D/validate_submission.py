#!/usr/bin/env python3
"""
Practical Exam — Submission Validator.
Run this script from your package folder to verify your deliverables:
    python3 validate_submission.py
"""

from __future__ import annotations

import pathlib
import re
import sys

REQUIRED_FILES = [
    ("answer_symmetric.md", "symmetric"),
    ("answer_asymmetric.md", "asymmetric"),
    ("answer_hash.md", "hash"),
]
REQUIRED_SECTIONS = [
    ("1. Finding", r"(?i)##\s*1\.\s*finding"),
    ("2. Evidence", r"(?i)##\s*2\.\s*evidence"),
    ("3. Fix", r"(?i)##\s*3\.\s*fix"),
    ("4. Explanation", r"(?i)##\s*4\.\s*explanation"),
]


def check_file(path: pathlib.Path) -> list[str]:
    issues = []
    if not path.exists():
        return [f"File missing: {path.name}"]
    content = path.read_text(encoding="utf-8", errors="replace")
    if len(content.strip()) < 80:
        issues.append(f"{path.name} is too short or empty")
    for sec_name, pattern in REQUIRED_SECTIONS:
        if not re.search(pattern, content):
            issues.append(f"{path.name}: missing section '{sec_name}'")
    if "<" in content and ">" in content:
        placeholders = re.findall(r"<[A-Za-z0-9_\-\s:|]+>", content)
        if placeholders:
            issues.append(f"{path.name}: placeholder text still present: {placeholders[:3]}")
    banned_tag = ("BEGIN RSA " + "PRIVATE " + "KEY")
    if banned_tag in content:
        issues.append(f"{path.name}: WARNING - contains raw private key block (never submit private keys)")
    return issues


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent
    print(f"=== Validating Practical Exam Submission in {root.name} ===\n")
    all_ok = True
    for filename, station in REQUIRED_FILES:
        target = root / filename
        if not target.exists() and (root / station / filename).exists():
            target = root / station / filename
        issues = check_file(target)
        if not issues:
            print(f"  PASS  {filename} (found in {target.parent.name}/)")
        else:
            all_ok = False
            print(f"  FAIL  {filename}")
            for iss in issues:
                print(f"        -> {iss}")
    print()
    if all_ok:
        print("All 3 answer files are properly structured and ready for submission!")
        return 0
    else:
        print("Please resolve the issues above before final submission.")
        return 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
