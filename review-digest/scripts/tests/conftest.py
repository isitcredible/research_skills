"""Shared helpers for the review-digest gate tests (pytest, tmp_path)."""
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

LEDGER_HEAD = """---
paper: Smith 2024, "Short title" (AER)
verdict: record only
status: COMPLETE
---

## Summary
Orientation paragraph.

## Issues
"""


def issue(rank, title, severity, body, sources="SYNTHESIS.md"):
    return (f"\n### {rank}. {title}\nseverity: {severity}\ncategory: Statistical inference\n"
            f"evidence: established\nsources: {sources}\n\n{body}\n")


def ledger(*issues, assessment="What the issues add up to."):
    return LEDGER_HEAD + "".join(issues) + f"\n## Assessment\n{assessment}\n"


def write(root, files):
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(text, bytes):
            p.write_bytes(text)
        else:
            p.write_text(text)


def run(script, *args, env=None, cwd=None):
    proc = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, env=env, cwd=cwd)
    return proc.returncode, proc.stdout + proc.stderr
