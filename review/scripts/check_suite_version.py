#!/usr/bin/env python3
"""Gate for edits to the review suite (review, audit-review, review-digest).

Checks:
  1. The three SKILL.md frontmatters carry the same `metadata.version`.
  2. review/spec-changes.csv is well formed: header, unique ids, parseable
     versions and dates, known kinds, no row newer than the suite version.
     `removed` holds the date a requirement stopped being in force (blank
     while it stands); `note` is free text.
  3. Where the skills tree is a git repository: if tag v<version> exists, the
     suite must not differ from it (a change after tagging needs a version
     bump); the version must not be older than the newest v* tag.

Versioning: v<major>.<minor>[.<patch>]. Below 1.0 the suite is in testing.
Internal changes bump the last digit (0.6 -> 0.6.1 -> 0.6.2); a release
bumps the minor (1.0, 1.1, ...). Every change that adds or alters what a run,
audit or digest must do gets a row in spec-changes.csv at the new version;
wording-only changes bump the version without a row. A `process` row records
a change to how a run is executed (agent sizing, model routing, cost) that
leaves its outputs unchanged; spec-drift audits ignore it.

Run: python3 check_suite_version.py [--root <skills tree>] [--no-git]
Exit 0 on PASS, 1 on FAIL.
"""
import argparse
import csv
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

SUITE = ("review", "audit-review", "review-digest")
HEADER = ["id", "version", "date", "kind", "scope", "requirement", "source", "removed",
          "note"]
KINDS = {"baseline", "added", "changed", "removed", "layout", "process"}
VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")


def vtuple(v):
    parts = [int(x) for x in v.split(".")]
    return tuple(parts + [0] * (3 - len(parts)))


def frontmatter_version(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    meta = re.search(r"^metadata:\s*\n((?:[ \t]+.*\n?)*)", m.group(1) + "\n", re.M)
    if not meta:
        return None
    v = re.search(r"^[ \t]+version:\s*[\"']?([0-9.]+)[\"']?\s*$", meta.group(1), re.M)
    return v.group(1) if v else None


def check_changes(path, version, fails):
    if not path.exists():
        fails.append(f"missing {path.name}")
        return
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows or rows[0] != HEADER:
        fails.append(f"{path.name}: header must be {','.join(HEADER)}")
        return
    seen = set()
    for n, row in enumerate(rows[1:], start=2):
        if len(row) != len(HEADER):
            fails.append(f"{path.name}:{n}: {len(row)} fields, expected {len(HEADER)}")
            continue
        r = dict(zip(HEADER, row))
        if not re.fullmatch(r"R\d{3,}", r["id"]):
            fails.append(f"{path.name}:{n}: id '{r['id']}' is not R<digits>")
        elif r["id"] in seen:
            fails.append(f"{path.name}:{n}: duplicate id {r['id']}")
        seen.add(r["id"])
        if not VERSION_RE.match(r["version"]):
            fails.append(f"{path.name}:{n}: version '{r['version']}' unparseable")
        elif version and vtuple(r["version"]) > vtuple(version):
            fails.append(f"{path.name}:{n}: row version {r['version']} is newer "
                         f"than the suite version {version}")
        try:
            dt.date.fromisoformat(r["date"])
        except ValueError:
            fails.append(f"{path.name}:{n}: date '{r['date']}' is not YYYY-MM-DD")
        if r["kind"] not in KINDS:
            fails.append(f"{path.name}:{n}: kind '{r['kind']}' not in {sorted(KINDS)}")
        if not r["requirement"].strip():
            fails.append(f"{path.name}:{n}: empty requirement")
        if r["removed"]:
            try:
                removed = dt.date.fromisoformat(r["removed"])
            except ValueError:
                fails.append(f"{path.name}:{n}: removed '{r['removed']}' is not YYYY-MM-DD")
            else:
                try:
                    if removed < dt.date.fromisoformat(r["date"]):
                        fails.append(f"{path.name}:{n}: removed before it was added")
                except ValueError:
                    pass  # bad `date` already reported


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True)


def check_git(root, version, fails, notes):
    if git(root, "rev-parse", "--is-inside-work-tree").returncode != 0:
        notes.append("not a git repository: tag checks skipped")
        return
    tags = [t for t in git(root, "tag", "-l", "v*").stdout.split()
            if VERSION_RE.match(t[1:])]
    newest = max(tags, key=lambda t: vtuple(t[1:]), default=None)
    if newest and vtuple(version) < vtuple(newest[1:]):
        fails.append(f"suite version {version} is older than tag {newest}")
    tag = f"v{version}"
    if tag not in tags:
        notes.append(f"{tag} is not tagged yet; tag it when the version is "
                     f"settled: git tag -a {tag} -m '<summary>'")
        return
    changed = git(root, "diff", "--name-only", tag, "--", *SUITE).stdout.split()
    untracked = git(root, "ls-files", "--others", "--exclude-standard",
                    "--", *SUITE).stdout.split()
    drift = sorted(set(changed + untracked))
    if drift:
        shown = ", ".join(drift[:8]) + (" ..." if len(drift) > 8 else "")
        fails.append(f"suite changed since {tag} ({len(drift)} files: {shown}); "
                     f"bump metadata.version in all three SKILL.md files and add "
                     f"spec-changes.csv rows for any changed requirement")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]),
                    help="skills tree holding review/, audit-review/, review-digest/")
    ap.add_argument("--no-git", action="store_true", help="skip tag checks")
    a = ap.parse_args()
    root = Path(a.root)
    fails, notes = [], []

    versions = {}
    for s in SUITE:
        p = root / s / "SKILL.md"
        v = frontmatter_version(p) if p.exists() else None
        if v is None:
            fails.append(f"{s}/SKILL.md: no metadata.version in frontmatter")
        elif not VERSION_RE.match(v):
            fails.append(f"{s}/SKILL.md: version '{v}' unparseable")
        versions[s] = v
    distinct = {v for v in versions.values() if v}
    if len(distinct) > 1:
        fails.append("versions differ: " +
                     ", ".join(f"{s}={v}" for s, v in versions.items()))
    version = versions.get("review")
    version = version if version and VERSION_RE.match(version) else None

    check_changes(root / "review" / "spec-changes.csv", version, fails)
    if version and not a.no_git:
        check_git(root, version, fails, notes)

    for n in notes:
        print(f"NOTE: {n}")
    for f in fails:
        print(f"FAIL: {f}")
    print(f"{'FAIL' if fails else 'PASS'}: review suite version {version or '?'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
