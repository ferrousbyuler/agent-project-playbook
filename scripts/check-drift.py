#!/usr/bin/env python3
"""Inventory required repo files and, optionally, hash-compare a live tree.

If LIVE_ROOT is unset, this checks that every path in drift-manifest.json
exists in the repo and exits 0. If LIVE_ROOT is set, each entry with a
live_path is SHA-256 compared to the repo copy. Drift exits 2.

This script never deletes files and never writes into the live tree.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "drift-manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    live_root = os.environ.get("LIVE_ROOT")
    live_base = Path(live_root) if live_root else None
    missing = []
    drifted = []
    checked = []
    for entry in manifest.get("files") or []:
        rel = entry["repo"]
        repo_path = ROOT / rel
        row = {"repo": rel, "exists": repo_path.is_file()}
        if not repo_path.is_file():
            missing.append(rel)
            checked.append(row)
            continue
        row["repo_sha256"] = sha256(repo_path)
        row["bytes"] = repo_path.stat().st_size
        live_rel = entry.get("live_path")
        if live_base is not None and live_rel:
            live_path = live_base / live_rel
            row["live_path"] = str(live_path)
            if not live_path.is_file():
                row["live_exists"] = False
                drifted.append({**row, "reason": "live copy missing"})
            else:
                live_hash = sha256(live_path)
                row["live_sha256"] = live_hash
                row["live_exists"] = True
                if live_hash != row["repo_sha256"]:
                    drifted.append({**row, "reason": "hash mismatch"})
        checked.append(row)
    report = {
        "ok": not missing and not drifted,
        "repo_root": str(ROOT),
        "live_root_configured": live_base is not None,
        "checked": len(checked),
        "missing": missing,
        "drifted": drifted,
        "files": checked,
    }
    # repo_root is the clone path on whatever machine ran the script;
    # it is not a committed personal path.
    print(json.dumps(report, indent=2))
    if missing or drifted:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
