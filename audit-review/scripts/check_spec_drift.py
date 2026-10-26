#!/usr/bin/env python3
"""Spec drift: what the current review suite requires that a run was never asked to do.

Reads the run's suite version from `Suite version: <x>` in <job>/00_INTAKE.md
(or --run-date for a run that never recorded one) and the review skill's
spec-changes.csv. Every `added`, `changed` or `layout` row newer than the run
and still in force (blank `removed`) is pending. A run older than the `baseline` row predates the requirement
history: it gets one full re-walk item per stage and per diagnostic module
instead.

  --write   create or refresh <job>/spec-drift.csv (existing dispositions kept)
  (default) check it: every pending item present, each disposition either
            `done: <path>[; <path>...]` (paths exist under the job root) or
            `na: <reason>`

Exit 0 on PASS, 1 on FAIL.
"""
import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

ACTIVE = {"added", "changed", "layout"}  # `process` rows change how a run executes, not what it must produce
DOWNSTREAM_SCOPES = {"review-digest", "audit-review"}  # downstream skills have their own gates
STAGES = ("paper", "code-and-data", "claims", "challenge", "verdict")
OUT_HEADER = ["id", "version", "date", "kind", "scope", "requirement", "disposition"]


def vtuple(v):
    parts = [int(x) for x in v.split(".")]
    return tuple(parts + [0] * (3 - len(parts)))


def run_version(root):
    intake = root / "00_INTAKE.md"
    if not intake.exists():
        return None
    m = re.search(r"Suite version\**:\**\s*v?(\d+\.\d+(?:\.\d+)?)",
                  intake.read_text(encoding="utf-8", errors="replace"), re.I)
    return m.group(1) if m else None


def load_changes(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pending_items(changes, review_dir, version, run_date):
    baseline = [r for r in changes if r["kind"] == "baseline"]
    if version is None and baseline and run_date < dt.date.fromisoformat(baseline[0]["date"]):
        b = baseline[0]
        scopes = [f"review:{s}" for s in STAGES]
        mods = review_dir / "modules"
        if mods.is_dir():
            scopes += [f"module:{p.name}" for p in sorted(mods.iterdir())
                       if (p / "SKILL.md").exists()]
        return [{"id": f"W-{s}", "version": b["version"], "date": b["date"],
                 "kind": "rewalk", "scope": s,
                 "requirement": f"Run predates the requirement history ({b['date']}): "
                                f"walk the current {s} instructions in full against the run."}
                for s in scopes]
    if version is not None:
        keep = lambda r: vtuple(r["version"]) > vtuple(version)
    else:
        keep = lambda r: dt.date.fromisoformat(r["date"]) >= run_date
    return [{k: r[k] for k in OUT_HEADER[:-1]}
            for r in changes
            if r["kind"] in ACTIVE and not r.get("removed")
            and r.get("scope", "").strip() not in DOWNSTREAM_SCOPES and keep(r)]


def read_worklist(path):
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def check_disposition(root, d):
    d = (d or "").strip()
    if d.startswith("na:"):
        return None if d[3:].strip() else "na: needs a reason"
    if d.startswith("done:"):
        paths = [p.strip() for p in d[5:].split(";") if p.strip()]
        if not paths:
            return "done: needs at least one artifact path"
        missing = [p for p in paths if not (root / p).exists()]
        return f"done: path(s) not found: {', '.join(missing)}" if missing else None
    return "blank" if not d else f"disposition must start 'done:' or 'na:', got '{d[:40]}'"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", required=True, help="job root")
    ap.add_argument("--review-skill",
                    default=str(Path(__file__).resolve().parents[2] / "review"),
                    help="path to the review skill (holds spec-changes.csv)")
    ap.add_argument("--run-date", help="YYYY-MM-DD the run's stages were executed "
                    "(only when 00_INTAKE.md records no suite version)")
    ap.add_argument("--write", action="store_true", help="create/refresh spec-drift.csv")
    a = ap.parse_args()
    root, review_dir = Path(a.root), Path(a.review_skill)
    changes = load_changes(review_dir / "spec-changes.csv")

    version = run_version(root)
    run_date = dt.date.fromisoformat(a.run_date) if a.run_date else None
    if version is None and run_date is None:
        print("FAIL: 00_INTAKE.md records no 'Suite version:'; pass --run-date "
              "(the date the run's stages were executed, from its logs or CHANGELOG)")
        return 1
    basis = f"suite version {version}" if version else f"run date {run_date}"
    items = pending_items(changes, review_dir, version, run_date)

    out = root / "spec-drift.csv"
    existing = read_worklist(out)
    if a.write:
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=OUT_HEADER)
            w.writeheader()
            for it in items:
                w.writerow({**it, "disposition": existing.get(it["id"], {}).get("disposition", "")})
        print(f"wrote {out.name}: {len(items)} pending item(s) against {basis}")
        return 0

    if not out.exists():
        print(f"FAIL: no spec-drift.csv ({len(items)} pending item(s) against {basis}); "
              f"run with --write, then dispose of every row")
        return 1
    fails = []
    for it in items:
        row = existing.get(it["id"])
        if row is None:
            fails.append(f"{it['id']} ({it['scope']}): missing from spec-drift.csv; re-run --write")
            continue
        err = check_disposition(root, row.get("disposition"))
        if err:
            fails.append(f"{it['id']} ({it['scope']}): {err} — {it['requirement'][:90]}")
    for f in fails:
        print(f"FAIL: {f}")
    print(f"{'FAIL' if fails else 'PASS'}: {len(items)} pending item(s) against {basis}, "
          f"{len(items) - len(fails)} disposed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
