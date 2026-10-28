#!/usr/bin/env python3
"""Render a review issue ledger (ISSUES.md) to a standalone evaluator digest (DIGEST.html).

The HTML is deliberately minimal: a "Summary" (orientation paragraph +
the headline-claims list),
a ranked issue list using native <details>/<summary> disclosure, and an
"Assessment" ending in bullet avenues the evidence leaves open. Inline
CSS, one tiny script for
expand-all, print (save-as-PDF), and a Blob download of the digest as
Markdown. No external resources, no tracking, works from file://.

Usage:
  python3 render_digest.py ISSUES.md [-o DIGEST.html] [--review-dir DIR]
                                     [--no-source-check] [--manifest PATH]
                                     [--finalize] [--stale-check]

Modes:

  default (preview) — render as before. The output embeds machine-readable
    build metadata (an HTML comment) recording the ledger, manifest and
    source hashes it was built from, so staleness is detectable after the
    fact. A preview is never a completed digest.

  --stale-check — do not render; read the embedded metadata of the
    existing DIGEST.html and report CURRENT or STALE against the files on
    disk now, reusing the full --finalize check set (accepted-input and
    primary hashes, HANDOFF↔manifest binding, open conflicts, open
    finding-bearing ERRATA) so CURRENT means the delivery state would
    still pass finalization. Exit 0 = current, 1 = stale / no metadata /
    no digest.

  --finalize — the completed-digest path. Refuses to render unless ALL
    of the following hold, then renders with the metadata marked final:

      * ledger status: COMPLETE and a HANDOFF.manifest.json exists with
        status COMPLETE, no open conflicts, and a handoff_sha256 matching
        the HANDOFF.md on disk (rebuild it with build_manifest.py);
      * every declared input still hashes to the manifest's recorded
        sha256 (an accepted source that drifted refuses);
      * every `sources:` path in the ledger resolves inside the manifest's
        accepted input set (a declared file, or a file inside a declared
        directory primary) — a citation to evidence the audit excluded or
        never declared refuses;
      * every report-class file is declared — inputs,
        excluded-with-disposition, or a named internal instrument.
        Report-class = every *.md at the review root (SYNTHESIS.md …)
        plus every *-REPORT.md beneath it (review/*-REPORT.md, the
        analysis/code-and-data/ module reports), walked with the shared
        corpus_rules skips (work/, lit/, 04_replication_*/ …). An
        undeclared finding-bearing file refuses: exclusion must be a
        declared act, not a silence;
      * no open ERRATA.md item lacks a `finding-bearing: no` field;
      * the fact / coverage / fairness / prose gates exit clean against
        THIS ledger revision. Where the passage scanner is unavailable
        (PASSAGE_SCANNER unset) the sanctioned manual pass substitutes — but only with the recorded
        ruling: `gate: manual pass — <date> — sha256:<first-12>` in
        FAIRNESS.md / ISSUES.keeps.md respectively;
      * the fact and coverage judgment passes declare who judged them:
        `gate: operator|in-context — <date> — sha256:<first-12>`,
        or `gate: fresh-context — <date> — sha256:<first-12> —
        <saved output path>` (the fresh context's saved output must
        exist under the review folder) in ISSUES.facts.md /
        ISSUES.coverage.md. A pass with no declared context is a pass
        that may not have run (Judgment-pass independence — SKILL.md).
        Where the prose scanner itself cannot be imported (the nested
        `ai-sweep` skill absent — ModuleNotFoundError/ImportError), the
        style gate takes the manual-pass route like a missing scanner.
        <first-12> is exactly the first 12 hex digits of the ledger's
        sha256; a shorter or longer prefix is no ruling.

    A hand-edited `status: COMPLETE` is not any of these.

ISSUES.md format (strict — the parser errors, it does not guess):

  ---
  paper: <Authors> <year>, "<Short title>" (<Journal>)
  verdict: Replication: OPEN · 2 HIGH / 3 MEDIUM / 1 LOW   # internal, not rendered
  status: COMPLETE            # COMPLETE | INTERIM | BLOCKED
  date: 2026-09-12
  ---

  ## Summary                  (required — before Issues)
  <markdown — orientation paragraph + headline-claims list>

  ## Issues                (required header — may be empty: a completed
                            review supporting no issue renders as a
                            Summary + Assessment digest)

  ### 1. Short title of the issue
  severity: Medium            # High | Medium | Low — assigned by the digest:
                              # the default from the claim rows mapped to the
                              # issue, or a departure (check_ledger_coverage.py)
  severity-reason: …          # only when departing from the default — internal
  category: Data & measurement
  evidence: established       # established|strong|plausible|unresolved — internal
  summary: One sentence at the top of the expanded view. (optional)
  sources: review/code-and-data-REPORT.md §R2b; work/logs/battery_run.log

  <markdown detail body — paragraphs, lists, tables, code all fine>

  ### 2. Next issue ...

  ## Assessment               (required — after Issues)
  <markdown — what the issues add up to + "Avenues the evidence leaves
  open" bullet list + closing "Caveats" bullet list>

  ## References               (optional — after Assessment; Harvard-style
                               bibliography entries for external works the
                               ledger relies on)

The `sources:`, `evidence:`, and `verdict:` fields are internal ledger
fields — they appear in no output. `sources:` feeds the on-disk evidence
gate; `evidence:` and `verdict:` record the audit trail. Evaluators' agents
can grep the review folder.

Exit status: 0 on success; 1 if any named source file is missing under
--review-dir (default: the ISSUES.md directory). A missing source means the
digest asserts evidence that is not on disk — fix the ledger or pass
--no-source-check only for drafts.
"""
import hashlib
import html as htmllib
import json
import os
import re
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
import time

try:
    import mistune
except ImportError:
    sys.exit("render_digest.py needs the mistune package: "
             "pip3 install mistune")

SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEV_CLASS = {"critical": "sev-critical", "high": "sev-high",
             "medium": "sev-medium", "low": "sev-low"}
EVIDENCE = {"established", "strong", "plausible", "unresolved"}
CATEGORIES = {"Research design", "Data & measurement", "Statistical inference",
              "Reproducibility", "Framing & claims", "Reporting"}
KNOWN_FIELDS = {"severity", "severity-reason", "category", "evidence", "summary",
                "sources"}
# Enum-valued keys may carry a trailing `# comment`, as the template shows.
COMMENTABLE = {"status", "date", "severity", "category", "evidence"}
TRAIL_COMMENT = re.compile(r"\s+#(\s.*)?$")
SECTION_CANON = {"summary": "Summary", "assessment": "Assessment",
                 "references": "References"}

md = mistune.create_markdown(plugins=["table"])


def die(msg):
    sys.exit(f"render_digest: {msg}")


def parse(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")

    meta, i = {}, 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", lines[i])
            if not m:
                die(f"frontmatter line {i+1}: expected 'key: value', got {lines[i]!r}")
            key = m.group(1).lower()
            val = m.group(2).strip()
            if key in COMMENTABLE:
                val = TRAIL_COMMENT.sub("", val)
            meta[key] = val
            i += 1
        i += 1
    for req in ("paper", "verdict", "status"):
        if req not in meta:
            die(f"frontmatter missing required key '{req}'")
    if meta["status"] not in ("COMPLETE", "INTERIM", "BLOCKED"):
        die(f"status must be COMPLETE|INTERIM|BLOCKED, got {meta['status']!r}")

    issues, sections, cur = [], {}, None
    in_issues = False
    seen_issues = False
    field_re = re.compile(r"^([a-z][a-z-]*):\s*(.*)$")

    while i < len(lines):
        line = lines[i]
        m2 = re.match(r"^##\s+(.+?)\s*$", line)
        m3 = re.match(r"^###\s+(\d+)\.\s+(.+?)\s*$", line)
        if m2:
            title = m2.group(1)
            tl = title.lower()
            in_issues = tl == "issues"
            if in_issues:
                seen_issues = True
                if "Summary" not in sections:
                    die(f"line {i+1}: '## Issues' must come after '## Summary'")
                cur = ("issues", None)
            elif tl in SECTION_CANON:
                canon = SECTION_CANON[tl]
                if canon == "Summary" and seen_issues:
                    die(f"line {i+1}: '## {title}' must come before '## Issues'")
                if canon == "Assessment" and not seen_issues:
                    die(f"line {i+1}: '## {title}' must come after '## Issues'")
                if canon == "References" and "Assessment" not in sections:
                    die(f"line {i+1}: '## {title}' must come after '## Assessment'")
                if canon in sections:
                    die(f"line {i+1}: duplicate section '## {title}'")
                cur = ("section", canon)
                sections[canon] = []
            else:
                die(f"line {i+1}: unknown section '## {title}' "
                    f"(allowed: Summary, Issues, Assessment, References)")
            i += 1
            continue
        if m3:
            if not in_issues:
                die(f"line {i+1}: issue block outside '## Issues'")
            issues.append({"rank": int(m3.group(1)), "title": m3.group(2),
                           "fields": {}, "body": [], "lineno": i + 1})
            cur = ("issue", issues[-1])
            i += 1
            continue
        if cur and cur[0] == "issue":
            fm = field_re.match(line)
            if fm and fm.group(1) in KNOWN_FIELDS and not cur[1]["body"]:
                val = fm.group(2).strip()
                if fm.group(1) in COMMENTABLE:
                    val = TRAIL_COMMENT.sub("", val)
                cur[1]["fields"][fm.group(1)] = val
            else:
                cur[1]["body"].append(line)
            i += 1
            continue
        if cur and cur[0] == "section":
            sections[cur[1]].append(line)
            i += 1
            continue
        i += 1

    for req_sec in ("Summary", "Assessment"):
        if not any(l.strip() for l in sections.get(req_sec, [])):
            die(f"missing or empty required section '## {req_sec}'")

    for iss in issues:
        f = iss["fields"]
        for req in ("severity", "category", "evidence", "sources"):
            if req not in f:
                die(f"issue #{iss['rank']} '{iss['title']}' (line {iss['lineno']}): "
                    f"missing field '{req}'")
        sev_key = re.split(r"[–\-/]", f["severity"])[0].strip().lower()
        if sev_key not in SEV_CLASS:
            die(f"issue #{iss['rank']}: severity {f['severity']!r} — "
                f"first component must be Critical/High/Medium/Low")
        iss["sev_class"] = SEV_CLASS[sev_key]
        ev = f["evidence"].strip().lower()
        if ev not in EVIDENCE:
            die(f"issue #{iss['rank']}: evidence {f['evidence']!r} not in {sorted(EVIDENCE)}")
        if f["category"].strip() not in CATEGORIES:
            die(f"issue #{iss['rank']}: category {f['category']!r} not in {sorted(CATEGORIES)}")
        if not any(l.strip() for l in iss["body"]):
            die(f"issue #{iss['rank']}: empty detail body — expanded view must carry "
                f"the technical substance")
        iss["body_raw"] = "\n".join(iss["body"]).strip()
        iss["body_html"] = md(iss["body_raw"])

    return meta, issues, {k: "\n".join(v).strip() for k, v in sections.items()}


def check_sources(issues, review_dir):
    """Resolve each `sources:` path against the review folder.

    A cited path must exist as written; a cited directory is written with
    its trailing slash (`deposit/`), as the handoff manifest declares one.
    A bare filename (no directory
    component) may resolve to a file elsewhere in the tree ONLY when it
    names exactly one file — an unambiguous, recorded resolution. A cited
    path with a directory component is never satisfied by a different file
    sharing its basename: absent `old/results.log` fails even if
    `new/results.log` exists. Ambiguous bare names fail too.
    """
    index = {}
    for root, _, files in os.walk(review_dir):
        for fn in files:
            index.setdefault(fn, []).append(os.path.relpath(os.path.join(root, fn),
                                                            review_dir))
    missing = []
    for iss in issues:
        for src in iss["fields"]["sources"].split(";"):
            fname = src.split("§")[0].split("#")[0].strip()
            if not fname:
                continue
            full = os.path.join(review_dir, fname)
            if os.path.isfile(full) or (fname.endswith("/") and os.path.isdir(full)):
                iss.setdefault("resolved", []).append((fname, fname))
                continue
            base = os.path.basename(fname)
            hits = index.get(base, [])
            if base == fname:
                # bare filename — resolve only when unambiguous
                if len(hits) == 1:
                    iss.setdefault("resolved", []).append((fname, hits[0]))
                elif hits:
                    missing.append((iss["rank"], fname,
                                    f"ambiguous basename — {len(hits)} files "
                                    f"named it: {', '.join(hits[:4])}"))
                else:
                    missing.append((iss["rank"], fname, "not found"))
            else:
                note = ("cited path absent"
                        + (f" — refusing to substitute a file that only "
                           f"shares its basename: {', '.join(hits[:4])}"
                           if hits else ""))
                missing.append((iss["rank"], fname, note))
    return missing


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Internal instruments of the pipeline — not evidence. Every other *.md
# at the review root is report-class and must be declared by the handoff
# (input or excluded-with-disposition): exclusion is a declared act. The
# list is shared with check_ledger_coverage.py (corpus_rules.py).
from corpus_rules import APPARATUS_FILES, errata_field, skip_dir  # noqa: E402


def report_class_files(review_dir):
    """Relative paths of report-class files: every *.md at the root, and
    every *-REPORT.md in the tree (shared skips; apparatus never)."""
    out = []
    for root, dirs, names in os.walk(review_dir):
        dirs[:] = sorted(d for d in dirs if not skip_dir(d))
        at_root = os.path.abspath(root) == os.path.abspath(review_dir)
        for name in sorted(names):
            low = name.lower()
            if name.startswith(".") or not low.endswith(".md"):
                continue
            if low in APPARATUS_FILES:
                continue
            if at_root or low.endswith("-report.md"):
                out.append(os.path.relpath(os.path.join(root, name),
                                           review_dir).replace(os.sep, "/"))
    return out

GATE_SCRIPTS = (("facts", "check_facts.py"),
                ("coverage", "check_ledger_coverage.py"),
                ("fairness", "check_fairness.py"),
                ("style", "check_style.py"))
MANUAL_RULING_FILE = {"facts": "ISSUES.facts.md",
                      "coverage": "ISSUES.coverage.md",
                      "fairness": "FAIRNESS.md",
                      "style": "ISSUES.keeps.md"}
PASS_MODES = ("fresh-context", "operator", "in-context", "manual pass")
SCANNER_MISSING = ("no passage scanner (PASSAGE_SCANNER unset",
                   "INCOMPLETE: the register layer never ran")
# The prose gate imports its engine from the nested ai-sweep skill; an
# absent engine surfaces as an import error, the same "scanner missing"
# condition as an absent passage scanner — for that gate only.
IMPORT_MISSING = ("ModuleNotFoundError", "ImportError")
# A standing failure in a gate's output: the "FAIL:" summary block, or a
# worklist line ("  FAIL  L12 …", as the style shim prints its ledger
# tells with no summary block). Either blocks the manual-pass route.
FAIL_LINE = re.compile(r"FAIL:|^\s*FAIL\s", re.M)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dir_listing_sha256(path):
    """(sha256 of the sorted relative file listing, entry count) — a
    directory input is bound by membership, not contents. Byte-level
    drift inside a dir input is not covered; declare the file itself
    when its bytes matter."""
    names = []
    for root, _, files in os.walk(path):
        for fn in files:
            names.append(os.path.relpath(os.path.join(root, fn), path))
    h = hashlib.sha256()
    for n in sorted(names):
        h.update(n.encode("utf-8")); h.update(b"\0")
    return h.hexdigest(), len(names)


def parse_errata(path):
    """Titles of open ERRATA items that block completion: status: open
    without an explicit `finding-bearing: no`. ###-headed blocks where
    headers exist; a headerless file is one block."""
    text = open(path, encoding="utf-8", errors="replace").read()
    chunks = (re.split(r"(?m)^(?=### )", text) if "### " in text
              else [text])
    blocked = []
    for chunk in chunks:
        if errata_field(chunk, "status") != "open":
            continue
        if errata_field(chunk, "finding-bearing") == "no":
            continue
        title = next((l[4:].strip() for l in chunk.splitlines()
                      if l.startswith("### ")), chunk.strip()[:60])
        blocked.append(title)
    return blocked


def gate_record(path, ledger_sha, modes):
    """A `gate: <mode> — <date> — sha256:<first-12>` ruling bound to THIS
    ledger revision — exactly the first 12 hex digits of its sha256. An unbound or stale-revision claim is no ruling. A
    `fresh-context` ruling must also name the fresh context's saved
    output — `… — sha256:<first-12> — <path>` — and that path must exist
    (relative to the ruling file's folder): a fresh context that left
    no output is unverifiable."""
    if not os.path.isfile(path):
        return False
    base = os.path.dirname(path) or "."
    pat = re.compile(
        r"gate\s*:\s*(%s)\b.*?sha256\s*:\s*([0-9a-f]+)\b"
        r"(?:\s*(?:—|–|--|-)\s*`?([^\s`]+)`?)?" % "|".join(modes),
        re.I)
    for line in open(path, encoding="utf-8", errors="replace"):
        m = pat.search(line)
        if not (m and len(m.group(2)) == 12
                and ledger_sha.startswith(m.group(2).lower())):
            continue
        if m.group(1).lower() == "fresh-context":
            out = m.group(3)
            if not (out and os.path.isfile(os.path.join(base, out))):
                continue
        return True
    return False


def manual_pass_recorded(path, ledger_sha):
    """A `gate: manual pass — <date> — sha256:<first-12>` ruling — the
    sanctioned substitute when the passage scanner is unavailable."""
    return gate_record(path, ledger_sha, ("manual pass",))


def run_gates(ledger, review_dir, manifest_path, refusals):
    """Run the four gate scripts against THIS ledger revision; record
    outcomes. A gate that cannot run for want of the passage scanner is
    covered only by a recorded manual-pass ruling — anything else is a
    refusal. For the sweeps that leave no re-checkable artifact (facts,
    coverage), a green exit is not enough: the judgment pass that worked
    the worklist must declare its context — fresh-context | operator |
    in-context — bound to this revision (Judgment-pass independence)."""
    ledger_sha = sha256_file(ledger)
    results = {}
    for name, script in GATE_SCRIPTS:
        cmd = [sys.executable, os.path.join(HERE, script), ledger]
        if name in ("facts", "coverage"):
            cmd += ["--manifest", manifest_path] if manifest_path else []
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=3600)
        except subprocess.TimeoutExpired:
            refusals.append(f"{name} gate timed out — never certify "
                            "over an unfinished check")
            continue
        out = r.stdout + r.stderr
        if r.returncode == 0:
            results[name] = "exit-0"
            continue
        scanner_down = (any(sig in out for sig in SCANNER_MISSING)
                        or (name == "style"
                            and any(sig in out for sig in IMPORT_MISSING)))
        if scanner_down and not FAIL_LINE.search(out):
            rulings = os.path.join(review_dir, MANUAL_RULING_FILE[name])
            if manual_pass_recorded(rulings, ledger_sha):
                results[name] = "manual pass (recorded)"
            else:
                refusals.append(
                    f"{name} gate: scanner unavailable and no manual "
                    f"ruling for this ledger revision — after the manual "
                    f"pass record 'gate: manual pass — <date> — "
                    f"sha256:{ledger_sha[:12]}' in "
                    f"{MANUAL_RULING_FILE[name]}")
        else:
            tail = [l for l in out.strip().splitlines() if l][-4:]
            refusals.append(f"{name} gate fails for this ledger revision "
                            f"({script} exit {r.returncode}):")
            refusals += [f"    {l}" for l in tail]
    for name in ("facts", "coverage"):
        if results.get(name) is None:
            continue
        rulings = os.path.join(review_dir, MANUAL_RULING_FILE[name])
        if not gate_record(rulings, ledger_sha, PASS_MODES):
            refusals.append(
                f"{name} judgment pass undeclared for this ledger "
                "revision — record who judged the worklist: 'gate: "
                "operator|in-context — <date> — "
                f"sha256:{ledger_sha[:12]}' (fresh-context adds "
                "' — <saved output path>') in "
                f"{MANUAL_RULING_FILE[name]}")
            results[name] += " — no declared judging context"
    return results


def finalize_checks(src, review_dir, issues, manifest_path,
                    require_complete=True):
    """Refusal list for --finalize. An empty list means the handoff is
    current, the accepted set is intact, and nothing finding-bearing is
    undeclared."""
    refusals = []
    man = None
    if not manifest_path or not os.path.isfile(manifest_path):
        refusals.append("no audit handoff — HANDOFF.manifest.json is "
                        "missing (the audit declares accepted inputs in "
                        "HANDOFF.md; build_manifest.py records them)")
    else:
        try:
            man = json.load(open(manifest_path, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            refusals.append(f"manifest unreadable ({exc}) — rebuild it "
                            "with build_manifest.py")
    if man is not None:
        handoff = os.path.join(review_dir, "HANDOFF.md")
        have = sha256_file(handoff) if os.path.isfile(handoff) else None
        if have is None:
            refusals.append("HANDOFF.md is missing — the manifest "
                            "declares a handoff that is not on disk")
        elif man.get("handoff_sha256") != have:
            refusals.append("manifest is stale — HANDOFF.md changed "
                            "since the manifest was built; re-run "
                            "build_manifest.py")
        if require_complete and man.get("status") != "COMPLETE":
            refusals.append(f"handoff status is {man.get('status')!r}, "
                            "not COMPLETE")
        if man.get("conflicts"):
            refusals.append("open finding-bearing conflicts declared: "
                            + "; ".join(man["conflicts"]))
        for rel, rec in sorted(man.get("inputs", {}).items()):
            p = os.path.join(review_dir, rel)
            if isinstance(rec, dict) and rec.get("dir"):
                if not os.path.isdir(p):
                    refusals.append(f"accepted primary missing: {rel}")
                else:
                    lsha, n = dir_listing_sha256(p)
                    if (lsha != rec.get("listing_sha256")
                            or n != rec.get("entries")):
                        refusals.append(f"primary input set changed since "
                                        f"the handoff: {rel} — membership "
                                        "drift in a declared dependency")
            elif not os.path.isfile(p):
                refusals.append(f"accepted input missing: {rel}")
            elif sha256_file(p) != rec.get("sha256"):
                kind = "primary" if rec.get("primary") else "input"
                refusals.append(f"accepted {kind} changed since the "
                                f"handoff: {rel} — the digest would "
                                "certify a revision nobody accepted")
        inputs = set(man.get("inputs", {}))
        excluded = set(man.get("excluded", {}))
        dir_inputs = tuple(rel.rstrip("/") + "/" for rel, rec
                           in man.get("inputs", {}).items()
                           if isinstance(rec, dict) and rec.get("dir"))
        for iss in issues:
            for _, resolved in iss.get("resolved", []):
                if resolved in excluded or not (
                        resolved in inputs
                        or resolved.startswith(dir_inputs)):
                    refusals.append(f"issue #{iss['rank']} cites "
                                    f"{resolved} — outside the accepted "
                                    "input set")
        for name in report_class_files(review_dir):
            if (name in inputs or name in excluded
                    or name.startswith(dir_inputs)):
                continue
            refusals.append(f"undeclared report-class file: {name} — "
                            "declare it an input or an exclusion in "
                            "HANDOFF.md")
        errata = os.path.join(review_dir, "ERRATA.md")
        if os.path.isfile(errata):
            for title in parse_errata(errata):
                refusals.append(f"open ERRATA item blocks completion: "
                                f"{title}")
    return man, refusals


def stale_check(src, out, review_dir):
    """Compare the existing digest's embedded build metadata against the
    files on disk now, then re-run finalization's structural checks so a
    drifted accepted input, a changed HANDOFF.md, or a new open
    finding-bearing ERRATA item is stale too. Mechanical detection: a
    changed ledger, source, manifest, or delivery state makes the
    rendered artifact stale whatever its prose says."""
    if not os.path.isfile(out):
        print(f"NO DIGEST — {out} does not exist")
        sys.exit(1)
    html_doc = open(out, encoding="utf-8", errors="replace").read()
    m = re.search(r"<!-- digest-build (\{.*?\}) -->", html_doc, re.S)
    if not m:
        print(f"STALE — {out} carries no build metadata (rendered before "
              "this check existed); rebuild before trusting it")
        sys.exit(1)
    try:
        meta = json.loads(m.group(1))
    except json.JSONDecodeError:
        print(f"STALE — embedded build metadata unreadable")
        sys.exit(1)
    problems = []
    if meta.get("ledger_sha256") != sha256_file(src):
        problems.append("ledger changed since this render")
    for rel, sha in sorted(meta.get("sources", {}).items()):
        p = os.path.join(review_dir, rel)
        if not os.path.isfile(p):
            problems.append(f"source missing: {rel}")
        elif sha256_file(p) != sha:
            problems.append(f"source changed since this render: {rel}")
    msha = meta.get("manifest_sha256")
    mpath = os.path.join(review_dir, "HANDOFF.manifest.json")
    if msha:
        if not os.path.isfile(mpath):
            problems.append("manifest missing")
        elif sha256_file(mpath) != msha:
            problems.append("manifest changed since this render")
    # Structural staleness — reuse finalization's checks so CURRENT means
    # the delivery state would still pass --finalize: accepted-input and
    # primary hashes, the HANDOFF↔manifest binding, open conflicts, and
    # open finding-bearing ERRATA — not merely that the cited files stand.
    # (Probed and found missing: a changed accepted script, a changed
    # HANDOFF.md, or a new open ERRATA item once returned CURRENT.)
    try:
        _, stale_issues, _ = parse(src)
    except SystemExit as exc:
        problems.append(f"ledger no longer parses: {exc.code}")
        stale_issues = None
    if stale_issues is not None:
        for rank, fname, note in check_sources(stale_issues, review_dir):
            problems.append(f"cited source unresolved — issue #{rank}: "
                            f"{fname} ({note})")
        if os.path.isfile(mpath) or meta.get("mode") == "final":
            _, refusals = finalize_checks(
                src, review_dir, stale_issues, mpath,
                require_complete=(meta.get("mode") == "final"))
            problems += refusals
        else:
            errata = os.path.join(review_dir, "ERRATA.md")
            if os.path.isfile(errata):
                for title in parse_errata(errata):
                    problems.append("open ERRATA item blocks currency: "
                                    f"{title}")
    if problems:
        print(f"STALE — {out} (built {meta.get('built')}, mode "
              f"{meta.get('mode')}):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"CURRENT — {out} (built {meta.get('built')}, "
          f"mode {meta.get('mode')})")
    sys.exit(0)


PROVENANCE = "Produced by AI agents and not independently verified."


def esc(s):
    return htmllib.escape(s, quote=True)


def build_comment(mode, ledger_sha, manifest_sha, source_shas):
    """Invisible build metadata — bound to the delivered file itself, so
    staleness detection never depends on a sidecar surviving. Reader-
    invisible. The one visible statement of origin is PROVENANCE, under the
    title."""
    meta = {"mode": mode,
            "built": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "ledger_sha256": ledger_sha,
            "manifest_sha256": manifest_sha,
            "sources": source_shas}
    return ("<!-- digest-build " + json.dumps(meta, sort_keys=True)
            + " -->")


def render(meta, issues, sections, md_filename, build=""):
    chips = []
    for iss in issues:
        f = iss["fields"]
        summary = (f'<div class="isum">{esc(f["summary"])}</div>'
                   if f.get("summary") else "")
        chips.append(f"""
<details class="issue">
<summary>
  <span class="rank">#{iss['rank']}</span>
  <span class="icol">
    <span class="ititle">{esc(iss['title'])}</span>
    <span class="imeta"><span class="sev {iss['sev_class']}">{esc(f['severity'])}</span> &middot; {esc(f['category'])}</span>
  </span>
</summary>
{summary}
<div class="ibody">
{iss['body_html']}
</div>
</details>""")

    sections_html = {k: md(v) for k, v in sections.items()}

    md_parts = [f"# {meta['paper']}", "", f"*{PROVENANCE}*", "",
                "## Summary", "", sections["Summary"], "",
                "## Potential issues", ""]
    if not issues:
        md_parts.append("The review records no supported issues.")
        md_parts.append("")
    for iss in issues:
        f = iss["fields"]
        md_parts += [f"### {iss['rank']}. {iss['title']}", "",
                     f"*{f['severity']} · {f['category']}*"]
        if f.get("summary"):
            md_parts += ["", f"*{f['summary']}*"]
        md_parts += ["", iss["body_raw"], ""]
    md_parts += ["## Assessment", "", sections["Assessment"], ""]
    if sections.get("References"):
        md_parts += ["## References", "", sections["References"], ""]
    md_json = json.dumps("\n".join(md_parts)).replace("</", "<\\/")

    refs_block = (f"<h2>References</h2>\n{sections_html['References']}"
                  if sections.get("References") else "")
    return TEMPLATE.replace("{{PAPER}}", esc(meta["paper"])) \
        .replace("{{PROVENANCE}}", esc(PROVENANCE)) \
        .replace("{{CLAIMS}}", sections_html["Summary"]) \
        .replace("{{ISSUES}}", "\n".join(chips)) \
        .replace("{{NOISSUES}}", "" if issues else
                 '<p>The review records no supported issues.</p>') \
        .replace("{{CONCLUSION}}", sections_html["Assessment"]) \
        .replace("{{REFERENCES}}", refs_block) \
        .replace("{{MD_JSON}}", md_json) \
        .replace("{{MD_FILE}}", esc(md_filename)) \
        .replace("</body>", build + "\n</body>")


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Review digest — {{PAPER}}</title>
<style>
  :root { --ink:#202122; --mut:#54595d; --line:#a2a9b1; --soft:#c8ccd1;
          --bg:#ffffff; --pale:#f1efe8; --accent:#0645ad; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
         Inter, Helvetica, Arial, sans-serif; color: var(--ink);
         background: var(--bg); max-width: 680px; margin: 0 auto;
         padding: 34px 24px 80px; line-height: 1.6; font-size: 15px;
         position: relative; }
  h1, h2 { font-family: "Linux Libertine", Georgia, "Times New Roman", serif;
           font-weight: 400; color: #000; line-height: 1.3; }
  h1 { font-size: 1.7em; margin: 0 0 .4em; padding-bottom: .22em;
       padding-right: 76px; border-bottom: 1px solid var(--line); }
  .topbar { position: absolute; top: 30px; right: 24px; display: flex;
            gap: 4px; }
  .topbar button { background: none; border: none; padding: 5px;
      cursor: pointer; color: var(--mut); border-radius: 4px;
      display: inline-flex; align-items: center; }
  .topbar button:hover { color: var(--ink); background: var(--pale); }
  h2 { font-size: 1.4em; margin: 1.6em 0 .5em; padding-bottom: .14em;
       border-bottom: 1px solid var(--line); }
  p { margin: .55em 0; }
  .prov { font-size: .9em; color: var(--mut); margin: -.1em 0 1em; }

  .controls { font-size: .9em; color: var(--mut); margin: 0 0 .3em; }
  .controls button { background: none; border: none; padding: 0;
      cursor: pointer; color: var(--accent); font: inherit; }
  .controls button:hover { text-decoration: underline; }
  .controls .dot { margin: 0 .4em; color: var(--soft); }

  details.issue summary { display: flex; align-items: baseline; gap: 10px;
      padding: 10px 4px; cursor: pointer; list-style: none; }
  details.issue summary::-webkit-details-marker { display: none; }
  details.issue summary::before { content: "\\25B8"; color: var(--mut);
      font-size: .72em; flex: none; transition: transform .12s; }
  details.issue[open] summary::before { transform: rotate(90deg); }
  details.issue summary:hover { background: var(--pale); }
  .rank { color: var(--mut); font-size: .88em; flex: none; min-width: 1.8em; }
  .icol { flex: 1; }
  .ititle { font-weight: 600; display: block; }
  .imeta { display: block; font-size: .84em; color: var(--mut);
           margin-top: 1px; }
  .sev { font-weight: 600; }
  .sev-critical { color: #b32424; }
  .sev-high     { color: #ac6600; }
  .sev-medium   { color: #7a6a00; }
  .sev-low      { color: var(--mut); }

  .isum { color: var(--mut); font-style: italic;
          padding: 0 4px 12px 34px; }
  .ibody { padding: 0 4px 18px 34px; }
  .ibody p { margin: .6em 0; }
  .ibody > :first-child, .isum > :first-child { margin-top: .1em; }
  .ibody ul, .ibody ol { margin: .6em 0; padding-left: 1.6em; }
  .ibody table { border-collapse: collapse; margin: .8em 0; }
  .ibody th, .ibody td { border: 1px solid var(--line); padding: .3em .7em;
                         text-align: left; }
  .ibody th { background: var(--pale); }
  .ibody code { background: var(--pale); padding: .05em .3em;
                font-size: .9em; }
  .ibody pre { background: var(--pale); padding: 10px 12px;
               overflow-x: auto; }
  .ibody pre code { background: none; border: none; padding: 0; }

  @media print {
    .controls, .topbar { display: none; }
    details.issue summary::before { content: "\\25BE"; }
    details.issue summary:hover { background: none; }
  }
</style>
</head>
<body>
<div class="topbar">
  <button type="button" id="pdf" title="Save as PDF" aria-label="Save as PDF">
    <svg viewBox="0 0 16 16" width="17" height="17" fill="none"
         stroke="currentColor" stroke-width="1.3" stroke-linecap="round"
         stroke-linejoin="round" aria-hidden="true">
      <path d="M4 1.5h5.5L13 5v9.5H4z"/>
      <path d="M9.5 1.5V5H13"/>
      <path d="M8 7.2v4.1m0 0l-1.7-1.7M8 11.3l1.7-1.7"/>
    </svg>
  </button>
  <button type="button" id="md" title="Save as Markdown" aria-label="Save as Markdown">
    <svg viewBox="0 0 24 15" width="24" height="15" fill="none"
         stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
         stroke-linejoin="round" aria-hidden="true">
      <rect x="1" y="1" width="22" height="13" rx="1.6"/>
      <path d="M4.5 10.5V4.5l3 4 3-4v6"/>
      <path d="M16 4.5v4.5m0 0l-2-2m2 2l2-2"/>
    </svg>
  </button>
</div>
<h1>{{PAPER}}</h1>
<p class="prov">{{PROVENANCE}}</p>

<h2>Summary</h2>
{{CLAIMS}}

<h2>Potential issues</h2>
<div class="controls">
  <button type="button" id="ex">expand all</button><span class="dot">&middot;</span><button type="button" id="co">collapse all</button>
</div>

{{ISSUES}}{{NOISSUES}}

<h2>Assessment</h2>
{{CONCLUSION}}

{{REFERENCES}}

<script>
const DIGEST_MD = {{MD_JSON}};
document.getElementById('ex').onclick = function () {
  document.querySelectorAll('details').forEach(function (d) { d.open = true; });
};
document.getElementById('co').onclick = function () {
  document.querySelectorAll('details').forEach(function (d) { d.open = false; });
};
document.getElementById('pdf').onclick = function () { window.print(); };
document.getElementById('md').onclick = function () {
  var blob = new Blob([DIGEST_MD], {type: 'text/markdown;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = "{{MD_FILE}}";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(a.href);
};
window.onbeforeprint = function () {
  document.querySelectorAll('details').forEach(function (d) { d.open = true; });
};
</script>
</body>
</html>
"""


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)
    src = args[0]
    out, review_dir, check = None, None, True
    finalize_mode = stale = False
    manifest_arg = None
    i = 1
    while i < len(args):
        if args[i] == "-o":
            out = args[i + 1]; i += 2
        elif args[i] == "--review-dir":
            review_dir = args[i + 1]; i += 2
        elif args[i] == "--manifest":
            manifest_arg = args[i + 1]; i += 2
        elif args[i] == "--no-source-check":
            check = False; i += 1
        elif args[i] == "--finalize":
            finalize_mode = True; i += 1
        elif args[i] == "--stale-check":
            stale = True; i += 1
        else:
            die(f"unknown argument {args[i]!r}")
    if not os.path.isfile(src):
        die(f"no such file: {src}")
    review_dir = review_dir or os.path.dirname(os.path.abspath(src))
    out = out or os.path.join(review_dir, "DIGEST.html")

    if stale:
        stale_check(src, out, review_dir)   # exits

    meta, issues, sections = parse(src)

    missing = check_sources(issues, review_dir)
    for rank, fname, note in missing:
        print(f"  MISSING SOURCE — issue #{rank}: {fname} "
              f"({note}; under {review_dir})", file=sys.stderr)
    if check and missing:
        sys.exit(f"render_digest: {len(missing)} named source file(s) missing; "
                 f"the digest asserts evidence that is not on disk. "
                 f"Fix ISSUES.md or pass --no-source-check for drafts.")

    manifest_path = manifest_arg or os.path.join(
        review_dir, "HANDOFF.manifest.json")
    manifest_path = manifest_path if os.path.isfile(manifest_path) \
        or finalize_mode else None
    ledger_sha = sha256_file(src)

    mode, gate_results = "preview", {}
    if finalize_mode:
        if not check:
            die("--finalize cannot be combined with --no-source-check")
        if meta["status"] != "COMPLETE":
            die(f"finalize refuses: ledger status is {meta['status']!r} "
                "— an INTERIM or BLOCKED review renders only as a "
                "bounded preview, never a completed digest")
        man, refusals = finalize_checks(src, review_dir, issues,
                                        manifest_path)
        if man is not None:
            gate_results = run_gates(src, review_dir, manifest_path,
                                     refusals)
        if refusals:
            print("FINALIZE REFUSED:", file=sys.stderr)
            for r in refusals:
                print(f"  - {r}", file=sys.stderr)
            sys.exit(1)
        mode = "final"
        print("handoff current, gates green for this ledger revision — "
              "rendering final digest")

    source_shas = {}
    for iss in issues:
        for _, resolved in iss.get("resolved", []):
            p = os.path.join(review_dir, resolved)
            if os.path.isfile(p):
                source_shas[resolved] = sha256_file(p)
    manifest_sha = (sha256_file(manifest_path)
                    if manifest_path and os.path.isfile(manifest_path)
                    else None)
    comment = build_comment(mode, ledger_sha, manifest_sha, source_shas)

    md_filename = os.path.splitext(os.path.basename(out))[0] + ".md"
    html_doc = render(meta, issues, sections, md_filename, build=comment)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html_doc)
    print(f"wrote {out} ({len(issues)} issues, "
          f"{len(html_doc)/1024:.0f} KB) [{mode}]")
    if gate_results:
        print("gates: " + "; ".join(f"{k} {v}"
                                    for k, v in gate_results.items()))


if __name__ == "__main__":
    main()
