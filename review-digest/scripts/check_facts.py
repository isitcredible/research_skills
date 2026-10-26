#!/usr/bin/env python3
"""Fact-check sweep for a review issue ledger (ISSUES.md) before rendering.

Not a verdict — a worklist. The sweep prints every quoted span and every
number-bearing sentence in the ledger beside the corpus lines where the
same wording or value appears, so the judgment pass (see SKILL.md,
"Fact-check gate") can confirm each number attaches to the right
quantity — level vs growth rate, % vs percentage points, index vs gap —
and each quote is genuinely verbatim.

Hard fails (exit 1):
  - a "quoted" span found nowhere in the corpus (matching is
    typography- and case-insensitive, verbatim otherwise). A quote
    asserts the source said it; a paraphrase inside quote marks is a
    misquote. Quotes resolve against PRIMARY sources only: the
    review's own prose (review/*-REPORT.md and any other *-REPORT.md /
    *-BRIEF.md, SYNTHESIS.md, ISSUES*.md, FAIRNESS.md, ERRATA.md,
    CHANGELOG.md, HANDOFF.md, analysis/**, and the review-generated work/**) is
    excluded from the
    quote corpus — a quote found only in the review quoting itself is
    unsupported. Numbers still resolve against the whole corpus.
  - an elided quote (… / ... / [...]) with no disposition: every such
    quote is listed under == ELIDED ==, and FAILs until ISSUES.facts.md
    carries a line containing the quote's first 30 characters — the
    judgment pass's confirmation that the elision dropped no negation
    or qualifying clause.
  - a number found nowhere in the corpus, even allowing for the corpus
    carrying more precision (15 matches 15.4; 32 matches 32.41). The
    reverse is a precision upgrade and fails the same way: 3.00 does not
    match a corpus that says only 3.
    A number in the digest must resolve to a file on disk — the same
    discipline as the review itself.

Usage:
  python3 check_facts.py ISSUES.md [--review-dir DIR] [--warn-only]
      [--manifest PATH] [--no-manifest]

Corpus: every .txt/.md/.csv/.tsv/.log/.json/.js file, and deposit code
(.do .ado .r .rmd .qmd .m .sas .sps .jl .py .sql .ipynb .sh), under
--review-dir (default: the ledger's own directory), excluding the ledger
itself, DIGEST.html, the digest's own gate outputs (work/digest/), and
any path inside a dotfile, _versions, bin, tmp, _skill or _bulk directory.
The ledger's `## References` section is quote-checked but not
number-swept: page ranges and volumes are bibliography, not findings.

Accepted-source binding: when a HANDOFF.manifest.json exists beside the
ledger (or --manifest names one), every resolution is annotated
[accepted] or [outside] against the manifest's declared inputs. A value
or quoted fragment resolving ONLY outside the accepted set — a withdrawn
report, an exploratory file, an internal instrument — is a FAIL: a
match somewhere in the corpus is a search aid, not support. Such a flag
clears only by fixing the ledger, extending the audit's declared inputs,
or recording a ruling in ISSUES.facts.md beside the ledger (a
`backticked` phrase from the flagged line plus the reason the outside
match is legitimate — e.g. a derived quantity whose inputs resolve
inside the accepted set).

A declared PDF primary is read through its extract: a file under
review/extracts/ whose stem matches the PDF's (equal, one a prefix of
the other, or the same leading `NN_` packet number) counts as accepted.
When review/extracts/ itself, or any file in it, is a declared input,
everything under review/extracts/ counts as accepted.

Matching ignores zero-width characters and rejoins words hyphenated
at a line break (`enrol-\nment` = `enrolment`), on both sides.
"""
import argparse
import fnmatch
import json
import os
import re
import sys

# code extensions mirror audit-review/scripts/check_coverage.py CODE_EXTS
# (plus .sql) — deposit code is quotable
CODE_EXT = {".do", ".ado", ".r", ".py", ".m", ".jl", ".sas", ".sps", ".ipynb",
            ".rmd", ".qmd", ".sh", ".sql"}
CORPUS_EXT = {".txt", ".md", ".csv", ".tsv", ".log", ".json", ".js"} | CODE_EXT
EXTRACTS_DIR = "review/extracts"
SKIP_DIRS = {"_versions", "bin", "tmp", "_skill", "_bulk"}
# the digest's own saved gate outputs echo every ledger line and number —
# never evidence for either corpus (the rest of work/ — logs — is)
OWN_OUTPUT_DIRS = {"work/digest"}
NUM_RE = re.compile(r"(?<![\w.)])(-?\d[\d,]*\.?\d*)(%|pp|x|×)?")
REF_WORDS = re.compile(
    r"(Table|Tables|Figure|Fig\.?|Equation|Eq\.?|Section|§|Appendix|"
    r"footnote|p\.|page|pp\.|No\.|#|Step)\s*$", re.I)
FIELD_RE = re.compile(
    r"^(severity-reason|severity|category|evidence|sources|paper|verdict|status|date)\s*:", re.I)
QUOTE_CHARS = '"“”'
# The review's own prose — never a primary source for a quotation.
# fnmatch '*' crosses '/', so 'analysis/*' covers analysis/** and 'work/*' covers
# work/** (review work products and the patched working copy of the deposit).
REVIEW_PROSE = ("*-REPORT.md", "*-REPORT-*.md", "*-BRIEF.md", "SYNTHESIS.md",
                "ISSUES*.md", "FAIRNESS.md", "ERRATA.md", "CHANGELOG.md",
                "HANDOFF.md", "PROGRESS.md", "AGENTS.md", "00_INTAKE.md",
                "review/*.md", "analysis/*", "work/*", "_skill/*", "_bulk/*")
ELISION = re.compile(r"\[\.\.\.\]|\[…\]|…|\.\.\.")


def is_review_prose(rel):
    rel = rel.replace(os.sep, "/")
    return any(fnmatch.fnmatch(rel, pat) for pat in REVIEW_PROSE)

_TRANS = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "−": "-",
    "­": "", "ﬁ": "fi", "ﬂ": "fl",
    " ": " ",
    # zero-width characters: U+200B–U+200D, U+2060–U+2064, U+FEFF
    "\u200b": "", "\u200c": "", "\u200d": "", "\u2060": "", "\u2061": "",
    "\u2062": "", "\u2063": "", "\u2064": "", "\ufeff": "",
})
LINEBREAK_HYPHEN = re.compile(r"-[ \t]*\n[ \t]*(?=[a-z])")


def norm(s):
    s = s.translate(_TRANS)
    s = LINEBREAK_HYPHEN.sub("", s)   # "enrol-\nment" -> "enrolment"
    s = re.sub(r"[*_]", "", s)   # markdown emphasis / subscript conventions
    return re.sub(r"\s+", " ", s).strip()


def ledger_lines(path):
    """[(file_lineno, text)] — frontmatter, field lines and leading
    heading/list markers removed; original line numbers kept."""
    raw_lines = open(path, encoding="utf-8").read().splitlines()
    start = 0
    if raw_lines and raw_lines[0].strip() == "---":
        for i in range(1, len(raw_lines)):
            if raw_lines[i].strip() == "---":
                start = i + 1
                break
    out = []
    for n, raw in enumerate(raw_lines, 1):
        if n <= start or FIELD_RE.match(raw):
            continue
        line = raw
        while True:
            stripped = re.sub(r"^\s{0,3}(#{1,6}|[*+-]|\d+\.)\s+", "", line)
            if stripped == line:
                break
            line = stripped
        out.append((n, line))
    return out


def references_linenos(path):
    """Line numbers inside the ledger's `## References` section — the
    number sweep skips them (page ranges and volumes are bibliography)."""
    out, inside = set(), False
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        if re.match(r"^#{1,2}\s", raw):
            inside = bool(re.match(r"^##\s+References\b", raw, re.I))
        elif inside:
            out.add(n)
    return out


def decimals(s):
    return len(s.split(".")[1]) if "." in s else 0


def corpus_lines(review_dir, ledger_path):
    """[(relpath, lineno, raw_line)] for every corpus file."""
    out = []
    for root, dirs, names in os.walk(review_dir):
        dirs[:] = [d for d in dirs
                   if not d.startswith(".") and d not in SKIP_DIRS
                   and os.path.relpath(os.path.join(root, d), review_dir)
                   .replace(os.sep, "/") not in OWN_OUTPUT_DIRS]
        for name in sorted(names):
            p = os.path.join(root, name)
            if (os.path.abspath(p) == os.path.abspath(ledger_path)
                    or name == "DIGEST.html" or name.startswith(".")):
                continue
            if os.path.splitext(name)[1].lower() not in CORPUS_EXT:
                continue
            rel = os.path.relpath(p, review_dir)
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    for i, raw in enumerate(f, 1):
                        out.append((rel, i, raw.rstrip("\n")))
            except OSError:
                continue
    return out


def load_manifest(ledger_path, manifest_arg, disabled):
    """Accepted-input relative paths from HANDOFF.manifest.json, or None.

    Auto-detect: the manifest sitting beside the ledger is used unless
    --no-manifest. The file is a generated record of the audit's source
    dispositions — this script reads it, never writes it.
    """
    if disabled:
        return None
    path = manifest_arg or os.path.join(
        os.path.dirname(ledger_path) or ".", "HANDOFF.manifest.json")
    if not os.path.isfile(path):
        return None
    try:
        man = json.load(open(path, encoding="utf-8"))
        files, dirs, pdf_stems, excluded = set(), [], set(), set()
        for p, rec in man.get("inputs", {}).items():
            p = p.split("§")[0].split("#")[0].strip()
            if isinstance(rec, dict) and rec.get("dir"):
                dirs.append(p.rstrip("/"))
            else:
                files.add(p)
                if p.lower().endswith(".pdf"):
                    pdf_stems.add(os.path.splitext(os.path.basename(p))[0])
        for p in man.get("excluded", {}):
            excluded.add(p.split("§")[0].split("#")[0].strip())
        ex = EXTRACTS_DIR
        all_extracts = (ex in dirs or any(f.startswith(ex + "/") for f in files)
                        or any(ex.startswith(d + "/") for d in dirs))
        return {"files": files, "dirs": tuple(dirs), "pdf_stems": pdf_stems,
                "all_extracts": all_extracts, "excluded": excluded}
    except (OSError, json.JSONDecodeError, AttributeError):
        sys.exit(f"check_facts: manifest {path} unreadable — rebuild it "
                 "with build_manifest.py")


def stem_matches(extract_stem, pdf_stem):
    """An extract dump belongs to a PDF primary: equal stems, one a prefix
    of the other at a `_` boundary, or the same leading `NN_` number."""
    a, b = extract_stem.lower(), pdf_stem.lower()
    if a == b or a.startswith(b + "_") or b.startswith(a + "_"):
        return True
    na, nb = re.match(r"^(\d+)_", a), re.match(r"^(\d+)_", b)
    return bool(na and nb and na.group(1) == nb.group(1))


def acc_has(acc, rel):
    """rel resolves inside the accepted input set — a member file, a path
    beneath a directory input, or the extract of a declared PDF primary."""
    if acc is None:
        return False
    rel = rel.replace(os.sep, "/")
    if rel in acc.get("excluded", ()):
        return False
    if (rel in acc["files"]
            or any(rel.startswith(d + "/") for d in acc["dirs"])):
        return True
    if rel.startswith(EXTRACTS_DIR + "/"):
        if acc.get("all_extracts"):
            return True
        stem = os.path.splitext(os.path.basename(rel))[0]
        return any(stem_matches(stem, ps) for ps in acc.get("pdf_stems", ()))
    return False


def load_rulings(ledger_path):
    """Rulings recorded in ISSUES.facts.md — `backticked` phrases (>=15
    chars) from the flagged ledger line. A ruling binds to the wording it
    covers; changed text re-flags rather than inheriting a stale ruling."""
    base = os.path.dirname(ledger_path) or "."
    path = os.path.join(base, "ISSUES.facts.md")
    if not os.path.exists(path):
        return set()
    text = open(path, encoding="utf-8", errors="replace").read()
    return {norm(m.group(1)).casefold()
            for m in re.finditer(r"`([^`]+)`", text)
            if len(norm(m.group(1))) >= 15}


def load_disposition_lines(ledger_path):
    """Normalized, casefolded lines of ISSUES.facts.md beside the ledger."""
    path = os.path.join(os.path.dirname(ledger_path) or ".", "ISSUES.facts.md")
    if not os.path.exists(path):
        return []
    return [norm(l).casefold()
            for l in open(path, encoding="utf-8", errors="replace")]


def quoted_spans(body_pairs):
    """[(lineno, span)] — alternating quote pairs over the joined body,
    so a multi-line quote pairs correctly and the text *between* two
    quoted spans is never itself misread as quoted."""
    offsets, text = [], []
    pos = 0
    for n, line in body_pairs:
        offsets.append((pos, n))
        text.append(line)
        pos += len(line) + 1
    joined = "\n".join(text)
    scan = joined.translate(_TRANS)
    marks = [m.start() for m in re.finditer('"', scan)]
    spans = []
    i = 0
    while i + 1 < len(marks):
        a, b = marks[i], marks[i + 1]
        span = joined[a + 1:b]
        if len(span) > 300:
            # implausibly long "quote" — the closer is probably an opener;
            # re-pair from it rather than cascading a mis-alignment
            i += 1
            continue
        if len(span) >= 2:
            ln = max(n for off, n in offsets if off <= a)
            spans.append((ln, span))
        i += 2
    return spans


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ledger")
    ap.add_argument("--review-dir", default=None)
    ap.add_argument("--manifest", default=None,
                    help="HANDOFF.manifest.json path (default: the file "
                         "beside the ledger when present)")
    ap.add_argument("--no-manifest", action="store_true",
                    help="ignore any manifest — presence-in-corpus mode")
    ap.add_argument("--warn-only", action="store_true")
    a = ap.parse_args()
    ledger = a.ledger
    review_dir = a.review_dir or os.path.dirname(ledger) or "."
    warn_only = a.warn_only

    accepted = load_manifest(ledger, a.manifest, a.no_manifest)
    rulings = load_rulings(ledger)

    body = ledger_lines(ledger)
    corpus = corpus_lines(review_dir, ledger)

    # quotes resolve against primary sources only — never the review's
    # own prose; numbers (below) use the whole corpus
    qcorpus = [c for c in corpus if not is_review_prose(c[0])]
    blob = norm("\n".join(raw for _, _, raw in qcorpus)).casefold()
    ablob = (norm("\n".join(raw for rel, _, raw in qcorpus
                           if acc_has(accepted, rel))).casefold()
             if accepted is not None else None)
    ncorpus = [(rel, i, norm(raw), raw.strip()) for rel, i, raw in corpus]
    nqcorpus = [c for c in ncorpus if not is_review_prose(c[0])]
    dispositions = load_disposition_lines(ledger)
    elided = []

    # number index: value -> lines; (precision, rounded value) -> lines
    # whose value carries AT LEAST that precision (a corpus "3" never
    # backs a ledger "3.00"); (exact precision, value) -> lines, to name
    # a precision upgrade
    val_index, prec_index, exact_index = {}, {}, {}
    for rel, i, nrm, raw in ncorpus:
        for m in NUM_RE.finditer(raw):
            s = m.group(1).replace(",", "")
            try:
                v = float(s)
            except ValueError:
                continue
            dc = decimals(s)
            idx = val_index.setdefault(v, [])
            if not idx or idx[-1] != (rel, i, raw, dc):
                idx.append((rel, i, raw, dc))
            exact_index.setdefault((dc, v), []).append((rel, i, raw))
            for d in range(min(dc, 6) + 1):
                bucket = prec_index.setdefault((d, round(v, d)), [])
                if not bucket or bucket[-1][:2] != (rel, i):
                    bucket.append((rel, i, raw))
    uniq_vals = list(val_index)
    ref_lines = references_linenos(ledger)

    fails, n_ok = [], 0

    print("== QUOTES ==")
    for ln, span in quoted_spans(body):
        q = norm(span)
        label = q if len(q) <= 70 else q[:67] + "..."
        # elision support: "…" / "..." joins non-contiguous source text —
        # each fragment must be verbatim
        frags = [f for f in ELISION.split(q) if len(f.strip()) >= 2]
        if ELISION.search(q):
            elided.append((ln, q, label))
        missing = [f.strip() for f in frags if f.strip().casefold() not in blob]
        outside = ([f.strip() for f in frags
                    if f.strip().casefold() not in ablob]
                   if ablob is not None else [])
        if not missing and not outside:
            n_ok += 1
            print(f"  ok    L{ln} \"{label}\"")
            hit = next((f"{rel}:{i}: {raw[:110]}"
                        for rel, i, nrm, raw in nqcorpus
                        if frags[0].strip().casefold() in nrm.casefold()), "")
            if hit:
                print(f"          → {hit}")
        elif not missing:
            flagged = q.casefold()
            ruled = any(r in flagged for r in rulings)
            if ruled:
                n_ok += 1
                print(f"  ok    L{ln} \"{label}\" — outside accepted "
                      "inputs but ruled in ISSUES.facts.md")
            else:
                fails.append(
                    f'L{ln} quote "{label}" resolves only outside the '
                    "accepted input set")
                print(f"  FAIL  L{ln} \"{label}\" — verbatim only "
                      "outside accepted inputs (rule in ISSUES.facts.md "
                      "or fix the ledger)")
        else:
            fails.append(f'L{ln} quote "{label}" not found verbatim'
                         + (f" (fragment: \"{missing[0][:50]}\")"
                            if len(frags) > 1 else ""))
            print(f"  FAIL  L{ln} \"{label}\" — no verbatim match"
                  + (f" [missing fragment: \"{missing[0][:50]}\"]"
                     if len(frags) > 1 else ""))
    print(f"  ({n_ok} resolved)")

    # an elision can drop a negation or a qualifying clause while every
    # fragment stays verbatim — each one needs a recorded confirmation
    print("\n== ELIDED ==")
    for ln, q, label in elided:
        key = q[:30].casefold()
        if any(key in d for d in dispositions):
            print(f"  ok    L{ln} \"{label}\" — disposed in ISSUES.facts.md")
        else:
            fails.append(f'L{ln} elided quote "{label}" has no disposition '
                         "in ISSUES.facts.md")
            print(f"  FAIL  L{ln} \"{label}\" — confirm nothing negating or "
                  "qualifying was elided; record a line in ISSUES.facts.md "
                  f"containing \"{q[:30]}\"")
    if not elided:
        print("  (no elided quotes)")

    print("\n== NUMBERS ==")
    n_ok = 0
    for ln, line in body:
        if ln in ref_lines:
            continue
        toks = []
        for m in NUM_RE.finditer(line):
            s = m.group(1).replace(",", "")
            try:
                v = float(s)
            except ValueError:
                continue
            if REF_WORDS.search(line[:m.start(1)]):
                continue
            # noise: bare years match any corpus; bare small ints likewise
            if re.match(r"^(19|20)\d\d$", s):
                continue
            if "." not in s and not m.group(2) and abs(v) < 10:
                continue
            toks.append((s, v, decimals(s)))
        if not toks:
            continue
        print(f"  L{ln} {line.strip()[:130]}")
        for s, v, d in toks:
            if d <= 6:
                hits = prec_index.get((d, round(v, d)), [])
            else:  # high-precision claim: scan unique corpus values
                hits = [h[:3] for c in uniq_vals if round(c, d) == v
                        for h in val_index[c] if h[3] >= d]
            if hits:
                in_hits = [h for h in hits
                           if accepted is None or acc_has(accepted, h[0])]
                shown = (in_hits or hits)[:3]
                if in_hits:
                    n_ok += 1
                else:
                    flagged = norm(line).casefold()
                    ruled = any(r in flagged for r in rulings)
                    if ruled:
                        n_ok += 1
                    else:
                        fails.append(
                            f"L{ln} value {s} resolves only outside the "
                            "accepted input set")
                for rel, i, txt in shown:
                    mark = ("" if accepted is None else
                            " [accepted]" if acc_has(accepted, rel)
                            else " [outside]")
                    print(f"    {s} ~ {rel}:{i}: {txt[:110]}{mark}")
                if len(hits) > len(shown):
                    print(f"    {s} ~ (+{len(hits) - len(shown)} more)")
                if not in_hits:
                    if ruled:
                        print(f"    {s} ~ outside accepted inputs — "
                              "ruled in ISSUES.facts.md")
                    else:
                        print(f"    {s} ~ resolves ONLY outside "
                              "accepted inputs — fix the ledger, extend "
                              "the declared inputs, or rule it in "
                              "ISSUES.facts.md")
            else:
                flagged = norm(line).casefold()
                coarser = [h for d2 in range(d)
                           for h in exact_index.get((d2, v), [])]
                if any(r in flagged for r in rulings):
                    n_ok += 1
                    print(f"    {s} ~ derived / not literal in corpus — "
                          "ruled in ISSUES.facts.md")
                elif coarser:
                    rel, i, txt = coarser[0]
                    fails.append(f"L{ln} value {s} upgrades precision — "
                                 "the corpus carries it only with fewer "
                                 "decimals")
                    print(f"    {s} ~ PRECISION UPGRADE — corpus has "
                          f"fewer decimals: {rel}:{i}: {txt[:110]}")
                else:
                    fails.append(f"L{ln} value {s} not found in corpus")
                    print(f"    {s} ~ NO MATCH")
    print(f"  ({n_ok} values resolved)")

    print()
    if fails:
        print("FAIL:")
        for f in fails:
            print("  -", f)
    else:
        print("sweep clean — now run the judgment pass over the contexts "
              "above: does each number attach to the same quantity in the "
              "ledger and in the corpus line shown? The sweep resolves "
              "values and quotes — not inferences: a clean exit says "
              "nothing about name/specification attributions or whether "
              "a ratio is written as a bound (ISSUES.facts.md carries "
              "those dispositions)")
    sys.exit(0 if (warn_only or not fails) else 1)


if __name__ == "__main__":
    main()
