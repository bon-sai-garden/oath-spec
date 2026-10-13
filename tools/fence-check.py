#!/usr/bin/env python3
"""fence-check.py: fail when a file bound for publication carries something it must not.

Generic by design: this script names no one. It checks every tracked file for
  - email addresses, 32-hex fingerprints, and internal ticket ids (two letters, a dash, two letters, three digits);
  - secret-shaped file names (*.key, *.pem, *.p12, private*, id_ed25519*, .env);
  - every term in a PRIVATE deny list, kept outside this repository and passed in, so
    the names the fence guards are never published by the fence itself.

    python3 tools/fence-check.py [--deny FILE ...] [--allow-email ADDR ...] [--allow-at FILE:LINE ...] [repo]

The deny file has one term per line, # for comments; a term matches case-insensitively on word
boundaries, or exactly as written when it starts with "=" (a name that is also a common word). With no --deny, the check still runs its generic rules and says the name list was
not checked. --allow-at FILE:LINE lets a denied term stand on that one line, where the owner has ruled
it may (it covers denied terms only; it is printed when used, and an allowance that matches nothing
fails, so a stale one cannot linger). Exit 0 only when nothing is found.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
FPR = re.compile(r"\b[0-9a-f]{32}\b")
TICKET = re.compile(r"\b[A-Z]{2}-[A-Z]{2}\d{3}\b")
SECRET_NAMES = ("*.key", "*.pem", "*.p12", "private*", "id_ed25519*", ".env", "*.env")


def tracked(repo: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"fence-check: {repo} is not a git checkout")
    return [p for p in out.stdout.split("\0") if p]


def load_terms(files: list[str]) -> list[str]:
    terms = []
    for f in files:
        for line in Path(f).read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                terms.append(line)
    return terms


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--deny", action="append", default=[], help="a private deny-list file (repeatable)")
    ap.add_argument("--allow-email", action="append", default=[], help="an address that may appear")
    ap.add_argument("--allow-at", action="append", default=[], metavar="FILE:LINE",
                    help="a line where a denied term stands by the owner's ruling (denied terms only; repeatable)")
    a = ap.parse_args()
    repo = Path(a.repo)
    for f in a.deny:
        if not Path(f).is_file():
            print(f"fence-check: FAIL the deny list {f} is not there, so the names cannot be checked")
            return 1
    terms = load_terms(a.deny)
    # "=Term" matches case-sensitively: for a name that is also an ordinary word (licence text
    # says "comment syntax"); every other term matches in any case.
    deny = [(t, re.compile(rf"(?<![\w]){re.escape(t[1:])}(?![\w])") if t.startswith("=")
             else re.compile(rf"(?i)(?<![\w]){re.escape(t)}(?![\w])")) for t in terms]
    hits, allowed, used = [], [], set()
    for rel in tracked(repo):
        name = Path(rel).name
        if any(fnmatch.fnmatch(name, g) for g in SECRET_NAMES):
            hits.append(f"{rel}: secret-shaped file name")
            continue
        try:
            text = (repo / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue                                  # binary: name checked above
        for n, line in enumerate(text.splitlines(), 1):
            for m in EMAIL.findall(line):
                if m not in a.allow_email:
                    hits.append(f"{rel}:{n}: email address")
            if FPR.search(line):
                hits.append(f"{rel}:{n}: a 32-hex fingerprint")
            if TICKET.search(line):
                hits.append(f"{rel}:{n}: an internal ticket id")
            for t, rx in deny:
                if rx.search(line):
                    if f"{rel}:{n}" in a.allow_at:
                        allowed.append(f"{rel}:{n}: a denied term, allowed by --allow-at"); used.add(f"{rel}:{n}")
                    else:
                        hits.append(f"{rel}:{n}: a denied term")   # the term itself is never printed
    for at in a.allow_at:
        if at not in used:
            hits.append(f"{at}: --allow-at matches no denied term (a stale allowance)")
    for h in allowed:
        print(f"  ~ {h}")
    for h in hits:
        print(f"  ✗ {h}")
    if not a.deny:
        print("fence-check: WARN no --deny list given: names were NOT checked")
    print(f"fence-check: {'FAIL' if hits else 'ok'} — {len(hits)} finding(s), {len(terms)} private term(s) checked")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
