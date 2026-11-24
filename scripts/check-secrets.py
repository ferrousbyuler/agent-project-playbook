#!/usr/bin/env python3
"""Fail if staged-looking secret patterns appear in tracked text files.

This is a small, dependency-free scan for a public template. It is not a
replacement for a dedicated scanner such as gitleaks. Matches are reported
by file and pattern name only; the matching line is never printed.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = [
    ("private_key_header", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----")),
    ("assignment_api_key", re.compile(r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}")),
    ("generic_bearer", re.compile(r"(?i)authorization:\s*bearer\s+\S+")),
]

SKIP_DIRS = {".git", ".github", "__pycache__", "node_modules", "graphify-out", "quarantine"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip", ".gz", ".whl"}


def tracked_files() -> list[Path]:
    try:
        out = subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT, text=False
        )
        names = [n.decode("utf-8", "replace") for n in out.split(b"\0") if n]
        return [ROOT / n for n in names]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = []
        for p in ROOT.rglob("*"):
            if not p.is_file():
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            files.append(p)
        return files


def main() -> int:
    hits = []
    for path in tracked_files():
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name, rx in PATTERNS:
            if rx.search(text):
                rel = path.relative_to(ROOT).as_posix()
                hits.append({"file": rel, "pattern": name})
    if hits:
        print("secret-pattern hits (values not shown):")
        for h in hits:
            print(f"  {h['file']}: {h['pattern']}")
        return 2
    print("ok: no listed secret patterns in scanned text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
