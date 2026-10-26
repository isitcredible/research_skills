#!/usr/bin/env python3
"""Materialize an audit's HANDOFF.md source dispositions into a hashed
input manifest (HANDOFF.manifest.json).

The audit decides which evidence is accepted — that is a judgment this
script does not make. This script performs only the mechanical half:
resolve each declared input path against the review folder, record its
sha256, parse each excluded artifact's disposition and evidence, and
fail when the declaration is malformed or self-contradictory. The
digest's finalization step then verifies the *current* files against
these recorded hashes, so an accepted source that drifts after the
handoff is detected, not silently re-admitted.

HANDOFF.md lives at the review root beside ISSUES.md:

  # HANDOFF — <review slug> audit to digest
  status: COMPLETE            # COMPLETE | INTERIM | BLOCKED
  audit: 2026-10-03           # anchor (CHANGELOG date or entry)

  ## inputs
  - SYNTHESIS.md
  - review/code-and-data-REPORT.md
  - review/claims-REPORT.md
  - analysis/code-and-data/results.csv
  - analysis/claims/claim-ledger.csv

  ## primaries
  - 01_paper_<authors>_<year>_<journal>.pdf
  - 04_replication_<authors>_<year>/     # dirs allowed — bound by listing

  ## excluded
  - analysis/code-and-data/old-results.csv | superseded | replaced by results.csv (ERRATA E5)
  - review/claims-pre-stress-REPORT.md | superseded | rebuilt as review/claims-REPORT.md
  - review/draft-notes.md | not-evidence | exploratory only; no finding rests on it

  ## conflicts
  - none

Header fields (`status:`, `audit:`) may carry a trailing `# comment`
(stripped) and may be written as `- status: …` list items.

Rules enforced here (exit 1):
  - every `## inputs` path exists under the review folder — inputs are
    bare repo-relative paths, one per bullet (`path §locator` or
    `path # note` tails are stripped; any other trailing text makes the
    path unresolvable and fails here);
  - `## primaries` is required and non-empty: the primary dependencies the
    findings attribute content to or measure against — the published
    article/appendix (or its operative extract), shipped working papers,
    deposited code/data. Files are bound by sha256; a directory is bound
    by its file listing (membership drift fails finalization — declare
    load-bearing members as files when their bytes matter). No primary
    may appear in `## excluded`;
  - every `## excluded` entry names a real file, carries a disposition
    (superseded | withdrawn | exploratory | unresolved | not-evidence)
    and a non-empty evidence field — an entry's evidence may wrap onto
    indented continuation lines, which are joined into the field;
  - a stage or module report (`*-REPORT.md` outside the trees the
    report-class walk skips: work/, lit/, 04_replication_*/ …) is an
    input unless a rebuilt report supersedes it: an excluded report must be
    `superseded`, and its evidence must name the replacement by a path
    declared under `## inputs`;
  - `unresolved` exclusions and non-`none` conflicts are incompatible
    with `status: COMPLETE` — an open finding-bearing conflict means the
    handoff is not complete;
  - no path appears in both lists;
  - `status: COMPLETE` is refused while analysis/claims/claim-ledger.csv
    carries any row whose `status` is INTERIM (a claim-ledger with no
    `status` column WARNs).

`## excluded` and `## conflicts` may each hold a single `- none`.

Usage:
  python3 build_manifest.py HANDOFF.md [--review-dir DIR] [-o OUT]

The manifest is regenerated, never hand-edited — a stale manifest means
re-run this script, not patch the JSON.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus_rules import skip_dir  # noqa: E402

DISPOSITIONS = {"superseded", "withdrawn", "exploratory",
                "unresolved", "not-evidence"}
STATUSES = {"COMPLETE", "INTERIM", "BLOCKED"}


def die(msg):
    sys.exit(f"build_manifest: {msg}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dir_listing_sha256(path):
    """(sha256 of the sorted relative file listing, entry count). Binds a
    directory primary by membership; byte drift inside is not covered —
    declare load-bearing members as file primaries."""
    names = []
    for root, _, files in os.walk(path):
        for fn in files:
            names.append(os.path.relpath(os.path.join(root, fn), path))
    h = hashlib.sha256()
    for n in sorted(names):
        h.update(n.encode("utf-8")); h.update(b"\0")
    return h.hexdigest(), len(names)


def parse_handoff(path):
    """(status, audit, inputs, primaries, excluded, conflicts) from HANDOFF.md."""
    status, audit = None, None
    inputs, primaries, excluded, conflicts = [], [], [], []
    section = None
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        # `key: value  # comment`, optionally as a `- ` list item
        m = re.match(r"^(?:[-*]\s+)?([a-z_-]+):\s*(.+?)\s*$", line)
        if section is None and m:
            key = m.group(1)
            val = re.sub(r"\s+#.*$", "", m.group(2)).strip()
            if key == "status":
                status = val
            elif key == "audit":
                audit = val
            continue
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            title = h.group(1).strip().lower()
            if title in ("inputs", "primaries", "excluded", "conflicts"):
                section = title
            else:
                section = None
            continue
        b = re.match(r"^[-*]\s+(.*\S)\s*$", line)
        if section in ("inputs", "primaries") and b:
            (inputs if section == "inputs" else primaries).append(
                b.group(1))
        elif section == "excluded" and b and b.group(1).strip().lower() == "none":
            continue
        elif section == "excluded" and b:
            parts = [p.strip() for p in b.group(1).split("|")]
            if len(parts) != 3 or not all(parts):
                die(f"line {n}: excluded entry must be "
                    "'path | disposition | evidence', got "
                    f"{b.group(1)!r}")
            excluded.append({"path": parts[0],
                             "disposition": parts[1],
                             "evidence": parts[2]})
        elif section == "conflicts" and b:
            conflicts.append(b.group(1))
        elif line.startswith((" ", "\t")) and line.strip():
            if section == "excluded" and excluded:
                excluded[-1]["evidence"] += " " + line.strip()
            elif (section == "conflicts" and conflicts
                  and conflicts[-1].lower() != "none"):
                conflicts[-1] += " " + line.strip()
    if status is None:
        die("missing 'status:' line (COMPLETE | INTERIM | BLOCKED)")
    if status not in STATUSES:
        die(f"status must be one of {sorted(STATUSES)}, got {status!r}")
    if not inputs:
        die("empty '## inputs' — the handoff declares no accepted evidence")
    if not primaries:
        die("missing or empty '## primaries' — the handoff must declare "
            "the primary dependencies (article, appendix, working papers, "
            "deposited code/data) the findings attribute or measure "
            "against; a handoff that binds only its own reports certifies "
            "revisions, not the evidence chain")
    return status, audit, inputs, primaries, excluded, conflicts


CLAIM_LEDGER = os.path.join("analysis", "claims", "claim-ledger.csv")
PATH_EDGE = "`'\"()[]{}<>,;:."


def is_report(path):
    """A stage or module report: a `*-REPORT.md` outside the trees the
    report-class walk never enters (work/, lit/, the deposit …)."""
    parts = path.strip("/").split("/")
    return (parts[-1].lower().endswith("-report.md")
            and not any(skip_dir(d) for d in parts[:-1]))


def report_exclusion_errors(excluded, in_set):
    """Excluded `*-REPORT.md` entries that are not superseded by a named,
    declared input. A report stops being an input only when a rebuilt
    report replaces it — never by a softer disposition."""
    bad = []
    for e in excluded:
        if not is_report(e["path"]):
            continue
        if e["disposition"] != "superseded":
            bad.append(f"{e['path']} is excluded as {e['disposition']!r} — "
                       "a stage or module report is an input unless a "
                       "rebuilt report supersedes it")
            continue
        named = {t.strip(PATH_EDGE) for t in e["evidence"].split()}
        if not (named - {e["path"]}) & in_set:
            bad.append(f"{e['path']} is superseded but its evidence names "
                       "no replacement declared under '## inputs'")
    return bad


def interim_claims(review_dir):
    """Refuse COMPLETE over a claim ledger that still carries INTERIM rows."""
    path = os.path.join(review_dir, CLAIM_LEDGER)
    if not os.path.isfile(path):
        return
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        rd = csv.DictReader(fh)
        col = next((c for c in (rd.fieldnames or [])
                    if c and c.strip().lower() == "status"), None)
        if col is None:
            print(f"build_manifest: WARN {CLAIM_LEDGER} has no status column — "
                  "cannot confirm no claim is INTERIM", file=sys.stderr)
            return
        interim = [str(i) for i, row in enumerate(rd, 2)
                   if (row.get(col) or "").strip().lower() == "interim"]
    if interim:
        die(f"status is COMPLETE but {CLAIM_LEDGER} carries INTERIM "
            f"claim(s) at row(s) {', '.join(interim)} — settle them or "
            "lower the status")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("handoff")
    ap.add_argument("--review-dir", default=None)
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    handoff = a.handoff
    if not os.path.isfile(handoff):
        die(f"no such file: {handoff}")
    review_dir = a.review_dir or os.path.dirname(os.path.abspath(handoff))
    out = a.out or os.path.join(review_dir, "HANDOFF.manifest.json")

    status, audit, inputs, primaries, excluded, conflicts = \
        parse_handoff(handoff)

    in_set = {p.split("§")[0].split("#")[0].strip() for p in inputs}
    pr_set = {p.split("§")[0].split("#")[0].strip() for p in primaries}
    ex_set = {e["path"] for e in excluded}
    both = in_set & ex_set
    if both:
        die(f"path(s) declared both input and excluded: {sorted(both)}")
    both_pr = pr_set & ex_set
    if both_pr:
        die(f"primary path(s) also declared excluded: {sorted(both_pr)}")

    bad_excl = [e["path"] for e in excluded
                if e["disposition"] not in DISPOSITIONS]
    if bad_excl:
        die(f"excluded path(s) with unknown disposition "
            f"{sorted(DISPOSITIONS)}: {bad_excl}")
    bad_reports = report_exclusion_errors(excluded, in_set)
    if bad_reports:
        die("excluded report(s) without a declared replacement:\n  "
            + "\n  ".join(bad_reports))
    unresolved = [e["path"] for e in excluded
                  if e["disposition"] == "unresolved"]
    real_conflicts = [c for c in conflicts if c.lower() != "none"]
    if status == "COMPLETE" and (unresolved or real_conflicts):
        die("status is COMPLETE but the handoff still declares "
            f"unresolved exclusions {unresolved} or conflicts "
            f"{real_conflicts} — resolve them or lower the status")

    if status == "COMPLETE":
        interim_claims(review_dir)

    missing = [p for p in sorted(in_set)
               if not os.path.isfile(os.path.join(review_dir, p))]
    if missing:
        die(f"declared input(s) not found under {review_dir}: {missing} "
            "— inputs are bare repo-relative paths, one per bullet; "
            "commentary belongs in its own paragraph, not on the path "
            "line")
    missing_pr = [p for p in sorted(pr_set)
                  if not os.path.exists(os.path.join(review_dir, p))]
    if missing_pr:
        die(f"declared primaries not found under {review_dir}: "
            f"{missing_pr} — a primary names the article, appendix, "
            "working papers, or deposit the findings rest on")
    missing_ex = [e["path"] for e in excluded
                  if not os.path.isfile(os.path.join(review_dir,
                                                     e["path"]))]
    if missing_ex:
        die(f"excluded path(s) not found (an exclusion must name the "
            f"file it retires): {missing_ex}")

    input_recs = {p: {"sha256": sha256(os.path.join(review_dir, p))}
                  for p in sorted(in_set)}
    for p in sorted(pr_set):
        pth = os.path.join(review_dir, p)
        if os.path.isdir(pth):
            lsha, n = dir_listing_sha256(pth)
            input_recs[p] = {"dir": True, "primary": True, "entries": n,
                             "listing_sha256": lsha}
        elif p in input_recs:
            input_recs[p]["primary"] = True
        else:
            input_recs[p] = {"sha256": sha256(pth), "primary": True}

    manifest = {
        "handoff_sha256": sha256(handoff),
        "status": status,
        "audit": audit,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "inputs": input_recs,
        "excluded": {e["path"]: {"disposition": e["disposition"],
                                 "evidence": e["evidence"]}
                     for e in excluded},
        "conflicts": real_conflicts,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {out} ({len(input_recs)} inputs incl. {len(pr_set)} "
          f"primaries, {len(manifest['excluded'])} excluded, "
          f"status {status})")


if __name__ == "__main__":
    main()
