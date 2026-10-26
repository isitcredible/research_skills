#!/usr/bin/env python3
"""Coverage sweep for a review issue ledger (ISSUES.md) — the
corpus-to-ledger direction check_facts.py cannot see.

Not a verdict — a worklist. The fact sweep verifies that what is IN the
ledger resolves to the corpus; this sweep verifies that what the corpus
DECLARES reaches the ledger. A silently dropped HIGH finding passes
every value-resolution gate and leaves the tally, the Assessment, and
the bottom line internally consistent and externally wrong.

Usage:
  python3 check_ledger_coverage.py ISSUES.md [--review-dir DIR] [--warn-only]
      [--manifest PATH] [--no-manifest]

Enumerates the corpus's declared findings, in authority order:

  1. Truth-ledger tables — any markdown table whose header carries a
     'Holds' column (the verdict stage's claim ledger) in SYNTHESIS.md
     and *-REPORT.md files. Every row whose Holds cell reads `narrower`
     or `not established` is a declared finding, carrying its
     Centrality; rows that hold carry no obligation. Legacy tables with
     a 'Severity' column (runs before v0.8) are read too: every data row
     is a declared finding.
  2. '### '-headed blocks under a '## Findings'/'## Issues'/'## Results'
     section in SYNTHESIS.md and *-REPORT.md (the F1/I5/C2 finding
     blocks, and any non-ID subsection — recall-first extraction: a
     process note that false-fires costs one `excluded:` line; a missed
     finding costs the digest its worst defect).
  3. List items carrying a severity token under the same sections —
     the fallback for syntheses with bulleted severity findings.
  4. A machine-readable claim ledger (claim-ledger*.csv), ONLY when it
     carries a recognizable holds/outcome/severity/status column — and
     only rows that do not hold (`narrower`, `not established`), whose
     outcome marks failure (incl. untested/unverifiable), or, in a legacy
     ledger, whose `severity` is HIGH/MEDIUM (or Critical). Rows marked
     holding, verified or surviving produce no obligation: a check that
     succeeds is not a finding.

Auto-excluded: ISSUES.md, DIGEST.html, the ruling files
(ISSUES.facts.md, ISSUES.keeps.md, ISSUES.coverage.md, FAIRNESS.md,
ERRATA.md, CHANGELOG.md, HANDOFF*, AGENTS/CLAUDE/MEMORY/README,
00_INTAKE/PROGRESS/VALIDATION) — apparatus, not findings (the list is
corpus_rules.APPARATUS_FILES, shared with render_digest.py). The
work/, lit/ and 04_replication_*/ trees are never walked. *-BRIEF.md files are condensed report twins;
the REPORT is authoritative. ERRATA items are already tracked, and
open finding-bearing ones block finalization on their own.

Manifest binding (when HANDOFF.manifest.json sits beside the ledger or
--manifest names one): each finding is tagged [accepted] / [outside] /
[undeclared]. A finding inside an artifact the audit declared
superseded/withdrawn/exploratory carries no obligation. A finding in
an undeclared report-class file is flagged `undeclared-source` — route
it to ERRATA.md; the audit declares, the compile desk does not.

Matching: normalized token containment proposes the best ledger issue
per finding (plus the runner-up when scores are close). The judgment
pass (fresh-context where the harness can dispatch — see SKILL.md,
Judgment-pass independence) confirms proposed matches and disposes
orphans: mapped, excluded, or dropped. Dropped fixes by extraction —
add the issue and re-run every gate on the added text; believing
upstream wrong is FOR-AUDIT-REVIEW, never a silent omission.

Output:
  == SOURCES ==            enumerated files and finding counts
  == COVERAGE WORKLIST ==  ok/FLAG per obligation
  == SEVERITY ==           per-issue assigned severity against the default
  == ISSUE ANCHORS ==      per-issue upstream-anchor check

Hard fails (exit 1, unless --warn-only): any declared finding neither
mapped nor dispositioned; a `→ issue N` ruling whose issue N no longer
exists or no longer overlaps its finding (deletion and renumbering
re-open the flag); a `→ caveats`/`→ avenues` ruling whose target
section is empty or no longer overlaps; a finding tagged
[undeclared-source]; an issue carrying no `sources:` field —
extraction requires an upstream anchor; an issue whose severity departs
from its default without a `severity-reason:` field.

Dispositions in ISSUES.coverage.md beside the ledger, one per line:

  - `upstream finding phrase ≥15 chars` → issue 3
  - `upstream finding phrase` → issues 3, 5   (a row several issues carry)
  - `upstream finding phrase` → caveats
  - `upstream finding phrase` — excluded: superseded twin of issue 2
  - `upstream finding phrase` — contested: FOR-AUDIT-REVIEW (needs an open,
    finding-bearing ERRATA.md item that quotes the phrase)
  - gate: fresh-context — <date> — sha256:<first-12> — <saved output path>
  - gate: operator|in-context — <date> — sha256:<first-12>

Severity is the digest's reading aid (SKILL.md, "Severity"). Each
truth-ledger row carries a default — not established: High for headline
and supporting claims, Medium for peripheral; narrower: Medium for
headline and supporting, Low for peripheral. An issue's default is the
most severe default among the rows ruled `→ issue N`; an issue mapped
to no truth-ledger row defaults to Low. A corpus with no truth-ledger
rows (a run before v0.8) has no defaults, and severities go unchecked. An issue whose `severity:`
differs from its default FAILs unless it carries a `severity-reason:`
field; every departure is listed either way.

Parking: a truth-ledger row for a headline or supporting claim (or, in
a legacy ledger, a Medium-or-higher finding) may not be ruled
`→ caveats`, `→ avenues`, or `excluded:` — except `excluded: superseded
twin of issue N` with issue N in the ledger.

Phrases bind to the upstream wording — a finding whose text changes
re-flags rather than inheriting a stale ruling. Exit 0 only when no
declared finding stands unmapped and undispositioned.
"""
import argparse
import csv
import json
import os
import re
import sys

sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
# own folder first: `python -I` drops the script's directory from sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from corpus_rules import errata_field, is_apparatus, skip_dir  # noqa: E402

SEV = r"(?:critical|high|medium|low)"
# Critical > High > Medium > Low — for "higher/lower" wording only; the
# carry-through test is equality with a component of the issue's rating.
SEV_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}
SEV_CELL = re.compile(
    r"^\**\s*" + SEV + r"(?:\s*[–\-/]\s*" + SEV + r")?"
    r"(?:\s+for\b.*|\s+scope\b.*|\s+limitation.*)?\s*\**$", re.I)
FINDINGS_HEAD = re.compile(r"^##\s+.*\b(findings?|issues?|results?)\b", re.I)
BLOCK_HEAD = re.compile(r"^###\s+")
FIELD_RE = re.compile(
    r"^(severity-reason|severity|category|evidence|sources|summary)\s*:\s*(.*)$",
    re.I)
HOLDS_CELL = re.compile(r"^\W*(not[\s_-]+established|narrower|holds?)\b", re.I)
CENT_CELL = re.compile(r"^\W*(headline|supporting|peripheral)\b", re.I)
DEFAULT_SEV = {("not established", "headline"): "high",
               ("not established", "supporting"): "high",
               ("not established", "peripheral"): "medium",
               ("narrower", "headline"): "medium",
               ("narrower", "supporting"): "medium",
               ("narrower", "peripheral"): "low"}
FAIL_VOCAB = re.compile(
    r"fail|false|unsupport|does not survive|not establish|invalid|not robust|refute|"
    r"withdraw|mislead|wrong|missing|fragil|collapse|broken|error|"
    # 'unverified-here' is a limit on the review, not a finding
    r"untest|unverif(?!ied[-_ ]here)",
    re.I)
OUTCOME_COL = re.compile(
    r"holds|severity|outcome|verdict|status|result", re.I)

_TRANS = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "−": "-",
    "­": "", "ﬁ": "fi", "ﬂ": "fl",
    " ": " ",
})
STOP = set("""
the and for are was were with that this from into under over between
against among within without their there these those then than they
them its it as at by be been is in on of or to a an no not we you he
she his her our your who whom which what when where how all any each
both more most other some such only own same can will would could
should has have had do does did but if so too very just also
""".split())


def norm(s):
    s = s.translate(_TRANS)
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def toks(s):
    # digit tokens survive: "Table 3 col 2" and "Table 5 col 4" differ
    return {t for t in re.findall(r"[a-z0-9]+", norm(s).casefold())
            if (len(t) >= 3 or t.isdigit()) and t not in STOP}


def sev_key(s):
    """First severity term of a cell/field ('High–Medium' → 'high'), or ''."""
    m = re.match(r"\W*(" + SEV + r")\b", s or "", re.I)
    return m.group(1).lower() if m else ""


def holds_key(s):
    """'not established' | 'narrower' | 'holds' from a Holds cell, or ''."""
    m = HOLDS_CELL.match(norm(s or ""))
    if not m:
        return ""
    v = re.sub(r"[\s_-]+", " ", m.group(1).lower())
    return "holds" if v.startswith("hold") else v


def cent_key(s):
    m = CENT_CELL.match(norm(s or ""))
    return m.group(1).lower() if m else ""


def default_sev(holds, cent):
    """The digest's default severity for a truth-ledger row, or ''."""
    return DEFAULT_SEV.get((holds, cent), "")


def finding(ident, rel, line, text, sev="", holds="", cent=""):
    return {"id": ident, "file": rel, "line": line, "sev": sev,
            "holds": holds, "cent": cent, "default": default_sev(holds, cent),
            "text": text}


def containment(a_toks, b_toks):
    """Share of a's tokens present in b — how much of the finding's
    vocabulary survives into the candidate issue."""
    if not a_toks:
        return 0.0
    return len(a_toks & b_toks) / len(a_toks)


def corpus_md_files(review_dir, ledger_path):
    """[(relpath, abspath)] — every corpus .md under review_dir minus
    apparatus, BRIEFs, dotfile trees and scratch dirs."""
    out = []
    for root, dirs, names in os.walk(review_dir):
        dirs[:] = [d for d in dirs if not skip_dir(d)]
        for name in sorted(names):
            low = name.lower()
            if name.startswith(".") or not low.endswith(".md"):
                continue
            if is_apparatus(name) or low.endswith("-brief.md"):
                continue
            p = os.path.join(root, name)
            if os.path.abspath(p) == os.path.abspath(ledger_path):
                continue
            out.append((os.path.relpath(p, review_dir), p))
    return out


def load_manifest(ledger_path, manifest_arg, disabled):
    """(inputs, excluded) sets from HANDOFF.manifest.json, or None."""
    if disabled:
        return None
    path = manifest_arg or os.path.join(
        os.path.dirname(ledger_path) or ".", "HANDOFF.manifest.json")
    if not os.path.isfile(path):
        return None
    try:
        man = json.load(open(path, encoding="utf-8"))
        inputs, dirs, excluded = set(), [], set()
        for p, rec in man.get("inputs", {}).items():
            p = p.split("§")[0].split("#")[0].strip()
            if isinstance(rec, dict) and rec.get("dir"):
                dirs.append(p.rstrip("/"))
            else:
                inputs.add(p)
        for p in man.get("excluded", {}):
            excluded.add(p.split("§")[0].split("#")[0].strip())
        return {"inputs": inputs, "dirs": tuple(dirs),
                "excluded": excluded}
    except (OSError, json.JSONDecodeError, AttributeError):
        sys.exit(f"check_ledger_coverage: manifest {path} unreadable — rebuild "
                 "it with build_manifest.py")


def man_tag(acc, rel):
    if acc is None:
        return ""
    if rel in acc["excluded"]:
        return "[outside]"
    if rel in acc["inputs"] or any(
            rel.startswith(d + "/") for d in acc["dirs"]):
        return "[accepted]"
    return "[undeclared]"


def split_cells(line):
    """Cells of a markdown table row; an escaped pipe (\\|) stays inside
    its cell, as markdown renders it."""
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") and not body.endswith("\\|") else body
    return [c.strip().replace("\\|", "|")
            for c in re.split(r"(?<!\\)\|", body)]


def table_rows(lines):
    """(row_index, cells) for markdown table data rows — skips header
    and separator rows by requiring a digit-free check is impossible;
    callers filter."""
    for i, line in enumerate(lines):
        if not re.match(r"^\s*\|", line):
            continue
        cells = split_cells(line)
        yield i, cells


def is_separator(cells):
    return all(re.match(r"^:?-{2,}:?$", c) for c in cells if c) \
        and any(c for c in cells)


def findings_from_table(lines, rel, tag):
    """Rows of a truth-ledger table (a 'Holds' column) that do not hold,
    and every row of a legacy table with a 'Severity' column."""
    out, in_table = [], False
    hold_col = cent_col = sev_col = None
    for i, line in enumerate(lines):
        if not re.match(r"^\s*\|", line):
            in_table = False
            hold_col = cent_col = sev_col = None
            continue
        cells = split_cells(line)
        if is_separator(cells):
            continue
        if not in_table:
            in_table = True
            for j, c in enumerate(cells):
                if re.fullmatch(r"\W*holds?\W*", c, re.I):
                    hold_col = j
                elif re.search(r"centrality", c, re.I):
                    cent_col = j
                elif re.search(r"severity", c, re.I):
                    sev_col = j
            continue
        if hold_col is not None:
            if len(cells) <= hold_col:
                continue
            h = holds_key(cells[hold_col])
            if h not in ("narrower", "not established"):
                continue
            c = (cent_key(cells[cent_col]) if cent_col is not None
                 and len(cells) > cent_col else "")
            skip = {hold_col, cent_col}
            text_cells = [x for j, x in enumerate(cells)
                          if j not in skip and len(norm(x)) >= 15]
            if text_cells:
                out.append(finding(f"{tag}:{i+1}", rel, i + 1,
                                   " ".join(text_cells), holds=h, cent=c))
            continue
        if sev_col is None or len(cells) <= sev_col or not SEV_CELL.match(
                cells[sev_col].strip("* ")):
            continue
        text_cells = [x for j, x in enumerate(cells)
                      if j != sev_col and len(norm(x)) >= 15]
        if not text_cells:
            continue
        out.append(finding(f"{tag}:{i+1}", rel, i + 1, " ".join(text_cells),
                           sev=cells[sev_col].strip("* ")))
    return out


def findings_from_blocks(lines, rel, tag):
    """'### ' blocks under a '## Findings'-like section. A block whose
    body is a severity table is skipped — its rows are extracted by
    findings_from_table instead."""
    out, in_find, i = [], False, 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^##\s+", line):
            in_find = bool(FINDINGS_HEAD.match(line))
            i += 1
            continue
        if in_find and BLOCK_HEAD.match(line):
            head = BLOCK_HEAD.sub("", line).strip()
            j = i + 1
            body = []
            while j < len(lines) and not re.match(r"^#{2,3}\s",
                                                  lines[j]):
                body.append(lines[j])
                j += 1
            body_txt = "\n".join(body)
            has_sev_table = any(
                len(c) >= 2 and any(re.search(r"severity", x, re.I)
                                    or re.fullmatch(r"\W*holds?\W*", x, re.I)
                                    for x in c)
                for _, c in table_rows(body))
            if not has_sev_table:
                text = head + " " + norm(
                    " ".join(b.strip() for b in body[:5]))
                out.append(finding(f"{tag}:{i+1}", rel, i + 1,
                                   text.strip()))
            i = j
            continue
        i += 1
    return out


def findings_from_listitems(lines, rel, tag):
    """Bullets carrying an explicit severity token under a Findings
    section — fallback for prose syntheses."""
    out, in_find = [], False
    for i, line in enumerate(lines):
        if re.match(r"^##\s+", line):
            in_find = bool(FINDINGS_HEAD.match(line))
            continue
        if not in_find:
            continue
        m = re.match(r"^\s{0,3}(?:[*+-]|\d+\.)\s+(.*)$", line)
        if not m:
            continue
        txt = m.group(1)
        mm = re.search(r"\bseverity\s*[:=]?\s*(" + SEV + r")\b|\*\*(" +
                       SEV + r")\*\*", txt, re.I)
        if mm and len(norm(txt)) >= 15:
            out.append(finding(f"{tag}:{i+1}", rel, i + 1, norm(txt),
                               sev=(mm.group(1) or mm.group(2) or "")))
    return out


def findings_from_csv(rel, abspath):
    """claim-ledger*.csv rows that do not hold, whose outcome column marks
    failure, or (legacy) whose severity column reads HIGH/MEDIUM/CRITICAL."""
    out = []
    try:
        rows = list(csv.reader(open(abspath, newline="",
                                    encoding="utf-8",
                                    errors="replace")))
    except OSError:
        return out, "unreadable"
    if not rows:
        return out, "empty"
    hdr = [h.strip().lower() for h in rows[0]]
    ocol = next((j for j, h in enumerate(hdr)
                 if OUTCOME_COL.search(h)), None)
    if ocol is None:
        return out, "no outcome column — skipped"
    hcol = next((j for j, h in enumerate(hdr) if h in ("holds", "hold")), None)
    ccol = next((j for j, h in enumerate(hdr) if "centrality" in h), None)
    scol = next((j for j, h in enumerate(hdr) if "severity" in h), None)
    for i, row in enumerate(rows[1:], 2):
        h = holds_key(row[hcol]) if hcol is not None and len(row) > hcol else ""
        c = cent_key(row[ccol]) if ccol is not None and len(row) > ccol else ""
        sev = sev_key(row[scol]) if scol is not None and len(row) > scol else ""
        failed = any(len(row) > j and FAIL_VOCAB.search(row[j])
                     for j, hh in enumerate(hdr)
                     if OUTCOME_COL.search(hh) and j not in (scol, hcol))
        not_holding = h in ("narrower", "not established")
        if not (not_holding or failed
                or SEV_ORDER.get(sev, 0) >= SEV_ORDER["medium"]):
            continue
        text = " ".join(x for j, x in enumerate(row)
                        if j not in (hcol, ccol) and len(norm(x)) >= 10)
        out.append(finding(f"csv:{i}", rel, i, text,
                           sev=(row[scol].strip() if sev else
                                ("" if not_holding else row[ocol].strip())),
                           holds=h if not_holding else "", cent=c))
    return out, None


def parse_ledger(path):
    """issues [{rank,title,fields,body,toks}], sections {name: text}."""
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":
        for k in range(1, len(lines)):
            if lines[k].strip() == "---":
                start = k + 1
                break
    issues, sections, cur, cur_name = [], {}, None, None
    in_issues = False
    for i in range(start, len(lines)):
        line = lines[i]
        m2 = re.match(r"^##\s+(.+?)\s*$", line)
        m3 = re.match(r"^###\s+(\d+)\.\s+(.+?)\s*$", line)
        if m2:
            cur, in_issues = None, m2.group(1).lower() == "issues"
            cur_name = m2.group(1).strip()
            sections.setdefault(cur_name, [])
            continue
        if in_issues and m3:
            issues.append({"rank": int(m3.group(1)),
                           "title": m3.group(2), "fields": {},
                           "body": [], "line": i + 1})
            cur = issues[-1]
            continue
        if cur is not None:
            fm = FIELD_RE.match(line)
            if fm and not cur["body"]:
                cur["fields"][fm.group(1).lower()] = fm.group(2).strip()
            else:
                cur["body"].append(line)
        elif cur_name:
            sections[cur_name].append(line)
    for iss in issues:
        iss["text"] = " ".join(
            [iss["title"], iss["fields"].get("summary", "")]
            + iss["body"])
        iss["toks"] = toks(iss["text"])
    sections = {k: "\n".join(v) for k, v in sections.items()}
    return issues, sections


def load_rulings(ledger_path):
    """ISSUES.coverage.md dispositions: [(phrase, kind, target)]."""
    base = os.path.dirname(ledger_path) or "."
    path = os.path.join(base, "ISSUES.coverage.md")
    rulings = []
    if not os.path.exists(path):
        return rulings
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.search(r"`([^`]+)`\s*(→|--|—|-)\s*(.*)$", line)
        if not m:
            continue
        phrase = norm(m.group(1)).casefold()
        if len(norm(m.group(1))) < 15:
            continue
        tail = m.group(3).strip()
        m_iss = re.match(r"issues?\s+(.*)$", tail, re.I)
        pairs = (re.findall(r"#?(\d+)\s*(?:\(\s*[\"“]([^\"”]+)[\"”]\s*\))?",
                            m_iss.group(1)) if m_iss else [])
        if m_iss and pairs:
            # each target may carry its issue's title fragment: 3 ("Supply headline")
            kind, target = "issue", [(int(n), frag.strip() or None)
                                     for n, frag in pairs]
        elif re.match(r"caveats?", tail, re.I):
            kind, target = "caveats", None
        elif re.match(r"avenues?", tail, re.I):
            kind, target = "avenues", None
        elif re.match(r"excluded\s*:", tail, re.I):
            kind, target = "excluded", tail
        elif re.match(r"contested\s*:", tail, re.I):
            kind, target = "contested", None
        else:
            kind, target = "unparsed", tail
        rulings.append((phrase, kind, target))
    return rulings


def errata_contests(ledger_path, phrase):
    """True when ERRATA.md beside the ledger holds an open, finding-bearing
    FOR-AUDIT-REVIEW item whose text contains the contested phrase — the
    item that makes a `contested:` ruling block finalisation."""
    path = os.path.join(os.path.dirname(ledger_path) or ".", "ERRATA.md")
    if not os.path.isfile(path):
        return False
    text = open(path, encoding="utf-8", errors="replace").read()
    for chunk in re.split(r"(?m)^(?=### )", text):
        if (errata_field(chunk, "status") == "open"
                and errata_field(chunk, "finding-bearing") == "yes"
                and "for-audit-review" in chunk.casefold()
                and phrase in norm(chunk).casefold()):
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ledger")
    ap.add_argument("--review-dir", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--no-manifest", action="store_true")
    ap.add_argument("--warn-only", action="store_true")
    a = ap.parse_args()
    ledger = a.ledger
    review_dir = a.review_dir or os.path.dirname(ledger) or "."
    acc = load_manifest(ledger, a.manifest, a.no_manifest)
    rulings = load_rulings(ledger)
    issues, sections = parse_ledger(ledger)

    # ---- enumerate declared findings --------------------------------
    findings, per_file = [], []
    for rel, p in corpus_md_files(review_dir, ledger):
        lines = open(p, encoding="utf-8",
                     errors="replace").read().splitlines()
        tag = os.path.splitext(os.path.basename(rel))[0]
        got = findings_from_table(lines, rel, tag)
        got += findings_from_blocks(lines, rel, tag)
        got += findings_from_listitems(lines, rel, tag)
        per_file.append((rel, len(got)))
        findings += got
    syn_truth = any(f["holds"] and os.path.basename(f["file"]) == "SYNTHESIS.md"
                    for f in findings)
    if syn_truth:
        # the verdict stage's table is the authority; the claims stage's
        # provisional tables would only double the rows (and can be stale)
        findings = [f for f in findings if not f["holds"]
                    or os.path.basename(f["file"]) == "SYNTHESIS.md"]
    truth_in_md = any(f["holds"] for f in findings)
    for root, dirs, names in os.walk(review_dir):
        dirs[:] = [d for d in dirs if not skip_dir(d)]
        for name in sorted(names):
            if not re.match(r"claim-?ledger.*\.csv$", name, re.I):
                continue
            p = os.path.join(root, name)
            rel = os.path.relpath(p, review_dir)
            got, note = findings_from_csv(rel, p)
            if truth_in_md and any(g["holds"] for g in got):
                # SYNTHESIS's truth table is the authority; the CSV is its
                # generated copy and would only double every obligation
                got = [g for g in got if not g["holds"]]
                note = (note + "; " if note else "") + \
                    "truth rows read from SYNTHESIS.md"
            per_file.append((rel + (f" ({note})" if note else ""),
                             len(got)))
            findings += got

    # ---- dedupe: same declared finding in several files = 1 obligation
    findings.sort(key=lambda f: (man_tag(acc, f["file"]) == "[outside]",
                                 f["file"], f["line"]))
    deduped, dups = [], 0
    for f in findings:
        ft = toks(f["text"])
        tgt = next((d for d in deduped
                    if ft and containment(ft, d["toks"]) >= .85
                    and containment(d["toks"], ft) >= .5), None)
        if tgt is not None:
            tgt["locs"].append((f["file"], f["line"]))
            if SEV_ORDER.get(sev_key(f["sev"]), 0) > SEV_ORDER.get(
                    sev_key(tgt["sev"]), 0):
                tgt["sev"] = f["sev"]
            if SEV_ORDER.get(f["default"], 0) > SEV_ORDER.get(
                    tgt["default"], 0):
                tgt.update(default=f["default"], holds=f["holds"],
                           cent=f["cent"])
            dups += 1
        else:
            f["toks"], f["locs"] = ft, [(f["file"], f["line"])]
            deduped.append(f)

    # ---- ruling resolution ------------------------------------------
    asmt_toks = toks(sections.get("Assessment", ""))
    summ_toks = toks(sections.get("Summary", ""))
    cave_toks = asmt_toks | summ_toks

    phrase_hits = {}

    def ruling_for(f):
        nft = norm(f["text"]).casefold()
        for phrase, kind, target in rulings:
            if phrase in nft:
                phrase_hits.setdefault(phrase, []).append(f["id"])
                return phrase, kind, target
        return None

    def best_issue(ft):
        scored = sorted(((containment(ft, iss["toks"]), iss)
                         for iss in issues), key=lambda x: -x[0])
        return scored[:2]

    fails, flags, oks = [], [], []
    ranks = {i["rank"] for i in issues}
    truth_corpus = any(f["holds"] for f in deduped)
    defaults = {}   # issue rank -> [(default, finding id)]

    for f in deduped:
        tag = man_tag(acc, f["file"])
        sev = (f" [{f['holds']}, {f['cent'] or 'centrality?'}]" if f["holds"]
               else f" [{f['sev']}]" if f["sev"] else "")
        head = (f"{f['id']} ({f['file']}:{f['line']}){sev} "
                f"{tag}".rstrip())
        if tag == "[outside]":
            oks.append(f"  ok      {head} — withdrawn/superseded, "
                       "no obligation")
            continue
        if tag == "[undeclared]":
            fails.append(f"{f['id']} declared finding sits in "
                         f"{f['file']} — a file the handoff never "
                         "declared (route to ERRATA.md; the audit "
                         "declares, the compile desk does not)")
            flags.append(f"  FLAG    {head} — undeclared-source")
            continue
        r = ruling_for(f)
        up = sev_key(f["sev"])
        if r and r[1] == "issue":
            nums = [n for n, _ in r[2]]
            tgts = [next((i for i in issues if i["rank"] == n), None)
                    for n in nums]
            label = ", ".join(str(n) for n in nums)
            unbound = [n for n, frag in r[2] if not frag]
            if truth_corpus and unbound:
                fails.append(f"{f['id']} ruling → issue {label} names no issue "
                             "title — bind each target as `→ issue N (\"title "
                             "words\")` so a renumbered ledger cannot pass")
                flags.append(f"  FLAG    {head} — unbound → issue {label}")
                continue
            stale = [n for (n, frag), tg in zip(r[2], tgts)
                     if frag and tg and norm(frag).casefold()
                     not in norm(tg["title"]).casefold()]
            if stale:
                fails.append(f"{f['id']} ruling → issue "
                             f"{', '.join(map(str, stale))} names a title that "
                             "issue no longer has — the ledger was renumbered "
                             "or retitled; re-adjudicate")
                flags.append(f"  FLAG    {head} — stale title → issue "
                             f"{', '.join(map(str, stale))}")
                continue
            if all(tgts) and any(
                    containment(f["toks"], t["toks"]) >= .15 for t in tgts) \
                    and all(containment(f["toks"], t["toks"]) >= .08
                            for t in tgts):
                if f["default"]:
                    for n in nums:
                        defaults.setdefault(n, []).append(
                            (f["default"], f["id"]))
                oks.append(f"  ok      {head} → issue {label} (ruled)")
                continue
            fails.append(f"{f['id']} ruling → issue {label} no longer "
                         "holds — issue missing or rewritten; "
                         "re-adjudicate")
            flags.append(f"  FLAG    {head} — stale → issue {label} "
                         "ruling")
            continue
        must_issue = (f["cent"] in ("headline", "supporting")
                      or (f["holds"] and not f["cent"])
                      or SEV_ORDER.get(up, 0) >= SEV_ORDER["medium"])
        if r and r[1] in ("caveats", "avenues", "excluded") and must_issue:
            tw = (re.search(r"superseded\s+twin\s+of\s+issue\s+(\d+)",
                            r[2], re.I) if r[1] == "excluded" else None)
            if not (tw and int(tw.group(1)) in ranks):
                what = (f"a {f['cent'] or 'unclassified'} claim that is "
                        f"{f['holds']}" if f["holds"] else f"a {up} finding")
                fails.append(f"{f['id']} is {what}, ruled {r[1]} — "
                             "headline and supporting claims that do not "
                             "hold, and Medium-or-higher legacy findings, "
                             "become issues (or `excluded: superseded twin "
                             "of issue N` with issue N in the ledger)")
                flags.append(f"  FLAG    {head} — ruled {r[1]}")
                continue
        if r and r[1] in ("caveats", "avenues"):
            if cave_toks and containment(f["toks"], cave_toks) >= .10:
                oks.append(f"  ok      {head} → {r[1]} (ruled)")
                continue
            fails.append(f"{f['id']} ruling → {r[1]} no longer "
                         "holds — target section empty or rewritten")
            flags.append(f"  FLAG    {head} — stale → {r[1]} ruling")
            continue
        if r and r[1] == "contested" and not errata_contests(ledger, r[0]):
            fails.append(f"{f['id']} is ruled contested, but ERRATA.md has no "
                         "open finding-bearing FOR-AUDIT-REVIEW item that "
                         "names it — file one (quote the finding), or map it")
            flags.append(f"  FLAG    {head} — contested without an open errata item")
            continue
        if r and r[1] in ("excluded", "contested"):
            oks.append(f"  ok      {head} — {r[1]} (ruled)")
            continue
        if r and r[1] == "unparsed":
            fails.append(f"{f['id']} disposition line unparsed: "
                         f"'{r[2][:60]}' — use → issue N | → caveats | "
                         "→ avenues | excluded: | contested:")
            flags.append(f"  FLAG    {head} — unparsed ruling")
            continue
        cand = best_issue(f["toks"])
        if cand and cand[0][0] >= .5:
            runner = (f" | also #{cand[1][1]['rank']} "
                      f"{cand[1][0]:.2f}" if len(cand) > 1
                      and cand[1][0] >= .25 else "")
            flags.append(f"  FLAG    {head} — proposed → issue "
                         f"{cand[0][1]['rank']} "
                         f"({cand[0][0]:.2f}{runner}); confirm or "
                         "dispose")
            fails.append(f"{f['id']} proposed match issue "
                         f"{cand[0][1]['rank']} unconfirmed")
        else:
            near = (f" — best candidate issue {cand[0][1]['rank']} "
                    f"({cand[0][0]:.2f}, weak)" if cand else "")
            flags.append(f"  FLAG    {head} — no issue, no "
                         f"exclusion{near}\n"
                         f"          \"{norm(f['text'])[:110]}\"")
            fails.append(f"{f['id']} declared finding unmapped and "
                         "undispositioned")

    sev_lines = []
    if not truth_corpus:
        sev_lines.append("  --      no truth-ledger rows in the corpus (a run "
                         "before v0.8): severities are not checked")
    for iss in issues if truth_corpus else []:
        assigned = sev_key(iss["fields"].get("severity", ""))
        reason = iss["fields"].get("severity-reason", "").strip()
        got = defaults.get(iss["rank"], [])
        dflt = (max((d for d, _ in got), key=lambda d: SEV_ORDER[d])
                if got else "low")
        note = "" if got else " (no truth-ledger row mapped)"
        if assigned == dflt:
            sev_lines.append(f"  ok      issue {iss['rank']} {assigned} = default{note}")
        elif reason:
            sev_lines.append(f"  DEPART  issue {iss['rank']} {assigned or '∅'} "
                             f"(default {dflt}{note}) — {reason}")
        else:
            sev_lines.append(f"  FLAG    issue {iss['rank']} {assigned or '∅'} "
                             f"(default {dflt}{note}) — no severity-reason")
            fails.append(f"issue #{iss['rank']} severity {assigned or '∅'} "
                         f"departs from its default {dflt} without a "
                         "severity-reason: field")

    issue_flags = []
    for iss in issues:
        if not iss["fields"].get("sources", "").strip():
            issue_flags.append(iss)
            fails.append(f"issue #{iss['rank']} carries no sources: "
                         "field — extraction requires an upstream "
                         "anchor")

    # ---- report ------------------------------------------------------
    print("== SOURCES ==")
    for rel, n in per_file:
        print(f"  {rel:<55} {n:>3} declared")
    print(f"  ({len(findings)} extracted → {len(deduped)} obligations, "
          f"{dups} duplicates merged)")

    print("\n== COVERAGE WORKLIST ==")
    for line in oks + flags:
        print(line)
    print(f"  ({len(oks)} resolved, {len(flags)} flagged)")

    multi = {p: ids for p, ids in phrase_hits.items() if len(ids) > 1}
    if multi:
        print("\n== AMBIGUOUS RULINGS (one phrase decides several findings) ==")
        for p, ids in sorted(multi.items()):
            print(f"  WARN    `{p[:70]}` → {', '.join(ids)}")

    print("\n== SEVERITY ==")
    for line in sev_lines:
        print(line)
    if not issues:
        print("  (no issues)")

    print("\n== ISSUE ANCHORS ==")
    for iss in issues:
        n = len([s for s in iss["fields"].get("sources", "")
                 .split(";") if s.strip()])
        if iss in issue_flags:
            print(f"  FLAG    issue {iss['rank']} — no sources: field")
        else:
            print(f"  ok      issue {iss['rank']} — {n} source(s)")
    if not issues:
        print("  (no issues — empty ledger is legal)")

    print()
    if fails:
        print("FAIL:")
        for fmsg in fails:
            print("  -", fmsg)
        print("\nDispose each FLAG in ISSUES.coverage.md — "
              "`finding phrase` → issue N | → caveats | → avenues | "
              "excluded: <reason> | contested: FOR-AUDIT-REVIEW — or "
              "extract the dropped finding into the ledger and re-run "
              "every gate on the added text.")
    else:
        print("coverage clean — every declared finding maps to the "
              "ledger or a recorded exclusion. The worklist is the "
              "record: the judgment pass confirms proposed matches "
              "and stands behind each exclusion.")
    sys.exit(0 if (a.warn_only or not fails) else 1)


if __name__ == "__main__":
    main()
