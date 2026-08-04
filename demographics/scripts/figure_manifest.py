#!/usr/bin/env python3
"""
Record, for each shipped figure, its hash and the hash of the script that draws
it. verify_manuscript.py compares against this.

Why not mtimes: a clone or a rebase rewrites them, so an mtime check reports
current figures as stale and cannot be trusted in CI. Content hashes survive
both. Run this after regenerating figures, and commit the manifest.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from constants import ROOT  # noqa: E402

SCRIPTS = ROOT / "scripts"
FIGS = ROOT / "figures"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    bodies = {s: s.read_text(encoding="utf-8", errors="ignore")
              for s in SCRIPTS.glob("*.py")}
    man = {}
    for fig in sorted(FIGS.glob("*.png")):
        for src, body in bodies.items():
            if fig.name in body:
                man[fig.name] = {"producer": src.name,
                                 "producer_sha": _sha(src),
                                 "figure_sha": _sha(fig)}
                break
    (FIGS / "MANIFEST.json").write_text(json.dumps(man, indent=2, sort_keys=True),
                                        encoding="utf-8")
    print(f"wrote {FIGS / 'MANIFEST.json'} — {len(man)} figures")


if __name__ == "__main__":
    main()
