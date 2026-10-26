#!/usr/bin/env python3
"""Prose-register sweep for a piece of writing before it reaches a reader.

Drafts carry machine register even under careful writing — stock filler,
evaluative adverbs, rhetorical scaffolding, sentences about the document
itself. The law is a plain-prose discipline, scoped to its
negative side: every sentence delivers a fact; no scaffolding, no
self-credentialing, no evaluative filler. Voice mechanics (connective
placement, em-dash austerity, sentence-length targets) are calibrated on
the operator's byline prose; a swept document may not be that voice, so
they surface as notes, not fails.

This sweep runs two layers over the reader-facing prose:

  - a mechanical tell pass — stock AI filler ('it is worth noting',
    evaluative adverbs, 'delve', 'sheds light on', 'the problem is'),
    with em-dashes and over-long sentences as non-failing notes;
  - a passage-scanner scan (--questions battery): every passage gets an ai_register
    score (0 = plain declarative … 3 = dominant machine register), a
    fact_free_sentences judgment, and a deliberation_leak probability —
    the plumbing axis (the test is whose activity is the subject: the writers'
    checking, worry, or rejected routes vs the reader-facing facts).
    Detection is the model's, not a wordlist — a flagged passage means
    the text *reads as* performing the argument rather than stating
    material.

The plumbing axis is hypothesis-tier: PLUMB_RES phrase hits and
deliberation_leak passages go to the report for the operator's ruling
(CUT / REWRITE with the finding as subject / KEEP) — they
never hard-fail the run. --no-plumbing disables the axis; --plumb sets
the dial threshold (default 0.5).

Non-rendered text is exempt: a YAML frontmatter block never scans;
lines matching --skip-fields (e.g. 'system_prompt|notes') are exempt,
and a matching field that opens a YAML block scalar ('field: |',
'field: >-') exempts the whole block. Comment lines in .yaml/.yml
files are exempt. A scan flag whose range sits entirely inside exempt
lines is auto-cleared.

Targets under the operator's private roots (AI_SWEEP_PRIVATE_ROOTS) never reach the
passage scanner: the register layer is skipped and the sweep runs
mechanical-only, deliberately. --mechanical-only forces the same on any
target.

Each flagged item is a worklist entry for the judgment pass (see the
skill's SKILL.md). Resolve a hit by:

  - rewriting to fact-delivering prose — register rewrites preserve
    every fact (numbers, claims, severities unchanged); or
  - keeping the wording where the flag is a false positive. A keep is a
    ruling, so it is recorded: the exact kept wording in `backticks`
    (a distinctive phrase, not a single word) plus a one-line reason go
    into `<file-stem>.keeps.md` beside the target — `- `phrase` —
    <reason>`. The sweep reads it: a flagged line or passage carrying
    the recorded phrase clears while the wording stands; an unrecorded
    keep re-flags and fails, and an entry with no reason clears nothing.
    The record binds to the text — changed wording reopens the flag.

The fact_free_sentences dial is context for the pass, not an
auto-clear: a passage can score low on register and still carry a
sentence about the document itself.

Hard fails (exit 1): any mechanical fail-level tell or flagged passage
standing unruled, a missing passage scanner (without
--mechanical-only), or a timed-out, unstartable, or incomplete scan.
A mechanical-only sweep is never the full gate. --warn-only for drafts.

Usage:
  python3 ai_sweep.py FILE [--scan-dir DIR]
      [--questions PATH] [--skip-fields REGEX] [--mechanical-only]
      [--no-plumbing] [--plumb 0.5]
      [--threshold 1.5] [--watch 1.0] [--chunk-chars 3000]
      [--overlap 400] [--timeout 900] [--retries 1]
      [--rescan] [--warn-only]

The register layer needs the operator's passage scanner: PASSAGE_SCANNER
names an executable taking `<scanner> scan FILE --questions BATTERY
--output DIR --chunk-chars N --overlap N` and writing manifest.json,
summary.json and judgments/ under DIR. Unset or not executable, the
sweep is mechanical-tells only, exits INCOMPLETE, and the judgment pass still
must run. Scan output is cached under the file's `.style-scan/` and
reused while file and battery are unchanged.
--scan-dir is a CACHE dir the script owns: a `.ai-sweep-owned` marker
file gates every deletion — a non-empty dir without it is never cleared
(a fresh owned scan-N subfolder is used instead), and a symlinked dir
must resolve to one the script created.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QUESTIONS = os.path.join(HERE, "prose-questions.json")


def passage_scanner():
    """The operator-configured passage scanner: the executable named by
    PASSAGE_SCANNER, else None. No other lookup."""
    p = os.path.expanduser(os.environ.get("PASSAGE_SCANNER", ""))
    return p if p and os.path.isfile(p) and os.access(p, os.X_OK) else None


SCANNER = passage_scanner()
SCANNER_MISSING_MSG = "no passage scanner (PASSAGE_SCANNER unset or not executable)"

# Roots whose contents must never reach the passage scanner — the
# operator's private tree. AI_SWEEP_PRIVATE_ROOTS is a colon-separated
# list of absolute paths; each entry is expanded and resolved. There is
# no built-in default: set the variable, or no path is treated as private.
PRIVATE_ROOTS = [
    os.path.expanduser(p) for p in
    os.environ.get("AI_SWEEP_PRIVATE_ROOTS", "").split(os.pathsep) if p]
OWNED_MARKER = ".ai-sweep-owned"
BATTERY_MARKER = ".check-style-battery-sha"

BLOCK_SCALAR_RE = re.compile(r"[|>][+-]?\d*\s*(?:#.*)?$")

# Stock AI/machine-register phrasing — the negative-discipline layer
# of the style guide. Broad on purpose: a false positive costs one
# keep on the read, a missed tell reaches the reader. Voice mechanics
# (sentence-initial connectives, punctuation frequency, sentence-length
# targets) are NOT here — they belong to a voice calibration on the
# operator's byline prose, and a swept document may not be that voice.
STOCK_RES = [
    (re.compile(r"\bit(?:'s| is) worth\b", re.I),
     "'it is worth' filler"),
    (re.compile(r"\bworth (?:noting|being|knowing|repeating|emphasiz|"
                r"highlight|underscor|sitting|dwelling|recalling|"
                r"remember)\w*\b", re.I),
     "'worth X' filler"),
    (re.compile(r"\b(?:notably|crucially|remarkably|importantly|"
                r"interestingly|strikingly|tellingly|fundamentally)\b",
                re.I),
     "evaluative adverb"),
    (re.compile(r"\bdelv(?:e|es|ed|ing)\b", re.I), "'delve'"),
    (re.compile(r"\bshed(?:s|ding)? light\b|"
                r"\bunderscor(?:e|es|ed|ing)\b|"
                r"\bhighlight(?:s|ed|ing)? the importance\b", re.I),
     "stock metaphor"),
    (re.compile(r"\bat its core\b|\bfirst and foremost\b|"
                r"\bneedless to say\b|"
                r"\bit bears (?:noting|mentioning|repeating|"
                r"reiterating)\b", re.I),
     "stock filler"),
    (re.compile(r"\bthe problem is\b|\bthe real (?:problem|issue|"
                r"question|story) is\b|\bhere is the thing\b|"
                r"\bthe thing is\b", re.I),
     "meta-vocabulary"),
    (re.compile(r"\bthat (?:is|being) said\b|\bhaving said that\b",
                re.I),
     "stock connective"),
    (re.compile(r"\btaken together\b|\ball told\b", re.I),
     "stock summarizing move"),
    (re.compile(r"\bplays? a (?:crucial|key|vital|central|significant|"
                r"critical|pivotal) role\b|\bserves? to\b", re.I),
     "stock filler"),
    (re.compile(r"\bit is (?:clear|evident|apparent) that\b|"
                r"\bit should be noted\b", re.I),
     "throat-clearing"),
    (re.compile(r"\bnot only\b.{1,60}\bbut also\b", re.I),
     "'not only … but also' balance-beam"),
    (re.compile(r"\bit'?s not (?:just|only|simply|merely)\b", re.I),
     "setup-negation scaffolding"),
    (re.compile(r"\blean(?:s|ed|ing)? into\b|\bresonates?\b|"
                r"\bthat lands\b|\bhold space\b", re.I),
     "AI-casual register"),
]

# Deliberation-leak hypotheses — the plumbing catalogue. A different
# fault class from the stock tells: the prose can be perfectly declarative and still be
# plumbing, because the test is WHOSE ACTIVITY IS THE SUBJECT — the
# writers' checking, worry, or rejected routes — not how it reads.
# These are hypotheses by design: "we controlled for X" is a legitimate
# data step ("what was done to the data stays; why we explored,
# worried, or checked goes"). A plumb flag goes to the report for the
# operator's ruling — never an auto-fail, never a silent cut.
# Entries: (regex, label, needs_digit).
PLUMB_RES = [
    (re.compile(r"\bwe (?:checked|verified|confirmed|recomputed|"
                r"re-?ran|were careful|considered|explored|"
                r"initially (?:found|saw|got|estimated))\b", re.I),
     "self-narrating verification / deliberation", False),
    (re.compile(r"\bit might be objected\b|\bthis is not to say\b|"
                r"\blest the reader\b|\bwe are not claiming\b|"
                r"\bto be clear\b", re.I),
     "pre-empted objection", False),
    (re.compile(r"\b(?:an|the) (?:alternative|earlier) (?:specification|"
                r"version|approach|estimate|model)\b|"
                r"\bone could instead\b", re.I),
     "rejected-alternative tour", False),
    (re.compile(r"\bafter correcting\b|\ban? earlier version\b", re.I),
     "process autopsy", False),
    (re.compile(r"\bthere is a concern that\b|"
                r"\bit should be noted that we\b", re.I),
     "method worry narrated", False),
    (re.compile(r"\bas we (?:show|showed|saw|demonstrate|documented)\b",
                re.I),
     "self-narrating verification", False),
    (re.compile(r"\bequivalent to\b|\bin other words\b|\bthat is,\b",
                re.I),
     "reconciliation gloss", True),
]

EMDASH_RE = re.compile(r"—|(?<=\w)--(?=\w)| -- ")

WORD_LIMIT = 30
QUOTE_CHARS = set("\"'‘’“”")
PAREN_RE = re.compile(r"\([^)]*\)")
DIGIT_RE = re.compile(r"\d")
LETTER_RE = re.compile(r"[A-Za-z]")


def prose_word_count(sent):
    """Words of actual prose in a sentence: parentheticals dropped and
    number-bearing tokens not counted. 'freight social savings
    4,677.24M Rs (22.9% of GDP)' is one fact, not a sprawling sentence.
    The 30-word rule applies to the prose that remains."""
    s = PAREN_RE.sub(" ", sent)
    return sum(1 for w in s.split()
               if LETTER_RE.search(w) and not DIGIT_RE.search(w))


def norm(s):
    s = re.sub(r"[*_]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def keeps_path(target):
    """The exception record beside the target: <stem>.keeps.md."""
    stem = os.path.splitext(os.path.basename(target))[0]
    return os.path.join(os.path.dirname(os.path.abspath(target))
                        or ".", stem + ".keeps.md")


def load_keeps(target):
    """Recorded keeps from <stem>.keeps.md: `- `phrase` — reason`.

    A keep is a ruling: the exact kept wording as a `backticked`
    phrase (>=15 chars — a short token would mask whole passages) plus a
    non-empty reason. An entry without a reason clears nothing, and a
    keep binds to the recorded wording — changed text re-flags.
    """
    keeps = set()
    path = keeps_path(target)
    if not os.path.exists(path):
        return keeps
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = re.match(r"\s*[-*]\s*`([^`]+)`\s*[-—–:]\s*(\S.*)$", ln)
        if m and len(norm(m.group(1))) >= 15:
            keeps.add(norm(m.group(1)).casefold())
    return keeps


def kept_keep(normed_text, keeps):
    """The recorded keep covering this text, if one matches."""
    return next((k for k in keeps if k in normed_text.casefold()), None)


def internal_lines(path, skip_re):
    """Line numbers (1-based) that never reach a reader: the YAML
    frontmatter block, '#' comment lines in .yaml/.yml files, lines
    whose field name matches --skip-fields, and the whole of any YAML
    block scalar ('field: |', 'field: >-') a skipped field opens."""
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    internal = set()
    if lines and lines[0].strip() == "---":
        internal.add(1)
        for i in range(1, len(lines)):
            internal.add(i + 1)
            if lines[i].strip() == "---":
                break
    is_yaml = path.endswith((".yaml", ".yml"))
    block_indent = None
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if block_indent is not None:
            if not stripped or len(ln) - len(ln.lstrip()) > block_indent:
                internal.add(i)
                continue
            block_indent = None
        if is_yaml and stripped.startswith("#"):
            internal.add(i)
            continue
        if skip_re and skip_re.match(ln):
            internal.add(i)
            value = ln.split(":", 1)[1].strip()
            if BLOCK_SCALAR_RE.match(value):
                block_indent = len(ln) - len(ln.lstrip())
    return internal, lines


FIELD_LINE_RE = re.compile(r"^\s*(?:-\s*)?[\w-]+\s*:\s*(.*)$")


def prose_blocks(lines, internal, is_yaml):
    """Reader-facing prose paragraphs as (first_lineno, joined_text).
    Skips fenced code, embedded <style>/<script> blocks, table rows,
    internal lines, and headings-only lines (the `### N. Title` heading
    text itself still gets the phrase/openers checks per-line below).
    In YAML files a field line ('key: …', '- id: …') is a structural
    boundary — its own scalar value stays in the running block, the
    key never glues onto a paragraph."""
    blocks = []
    buf, start, fence, embed = [], None, False, None
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if stripped.startswith("```"):
            fence = not fence
            if buf:
                blocks.append((start, " ".join(buf)))
                buf, start = [], None
            continue
        if fence or i in internal or not stripped \
                or stripped.startswith("|"):
            if buf:
                blocks.append((start, " ".join(buf)))
                buf, start = [], None
            continue
        low = stripped.lower()
        if embed:
            if low.startswith(embed):
                embed = None
            continue
        for tag in ("<style", "<script"):
            if low.startswith(tag):
                if tag.replace("<", "</") not in low:
                    embed = tag.replace("<", "</")
                break
        if embed or low.startswith(("<style", "<script")):
            if buf:
                blocks.append((start, " ".join(buf)))
                buf, start = [], None
            continue
        if is_yaml:
            m = FIELD_LINE_RE.match(ln)
            if m:
                if buf:
                    blocks.append((start, " ".join(buf)))
                    buf, start = [], None
                val = m.group(1).strip()
                if val and not BLOCK_SCALAR_RE.match(val) \
                        and not val.startswith(("|", ">")):
                    buf, start = [val], i
                continue
        if start is None:
            start = i
        buf.append(stripped)
    if buf:
        blocks.append((start, " ".join(buf)))
    return blocks


def sentences(text):
    """Naive sentence split on .!? followed by whitespace + capital or
    end of text. Good enough for a length check."""
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'‘“])", text)
            if s.strip()]


def mechanical(lines, internal, is_yaml=False, plumb_on=True):
    """(lineno, level, label, excerpt) — 'fail', 'plumb', or 'note'."""
    flags = []
    fence, embed = False, None
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if fence or i in internal or not stripped:
            continue
        low = stripped.lower()
        if embed:
            if low.startswith(embed):
                embed = None
            continue
        for tag in ("<style", "<script"):
            if low.startswith(tag):
                if tag.replace("<", "</") not in low:
                    embed = tag.replace("<", "</")
                break
        if embed or low.startswith(("<style", "<script")):
            continue
        for rx, label in STOCK_RES:
            if rx.search(ln):
                flags.append((i, "fail", label, norm(ln)[:150]))
        if plumb_on:
            for rx, label, needs_digit in PLUMB_RES:
                if needs_digit and not DIGIT_RE.search(ln):
                    continue
                if rx.search(ln):
                    flags.append((i, "plumb", label, norm(ln)[:150]))
        if EMDASH_RE.search(ln):
            flags.append((i, "emdash", "em-dash", norm(ln)[:150]))
    for start, block in prose_blocks(lines, internal, is_yaml):
        for sent in sentences(block):
            if (prose_word_count(sent) > WORD_LIMIT
                    and not (QUOTE_CHARS & set(sent))):
                flags.append((start, "note",
                              f"{prose_word_count(sent)}-word prose "
                              f"sentence — worth reading for "
                              f"clause-piling",
                              sent[:150]))
    return flags


def _cache_current(scan_dir, sha, qsha):
    """scan_dir holds a complete scan of the current target + battery."""
    manifest_p = os.path.join(scan_dir, "manifest.json")
    summary_p = os.path.join(scan_dir, "summary.json")
    marker_p = os.path.join(scan_dir, BATTERY_MARKER)
    if not (os.path.exists(manifest_p) and os.path.exists(summary_p)):
        return False
    try:
        man = json.load(open(manifest_p))
        summ = json.load(open(summary_p))
        same = any(p.get("source_sha256") == sha
                   for p in man.get("passages", []))
        try:
            marker = open(marker_p).read().strip()
        except OSError:
            marker = ""
    except (OSError, json.JSONDecodeError):
        return False
    return bool(same and summ.get("complete") and marker == qsha)


def _cache_candidates(scan_dir):
    """Where a valid cache may live: scan_dir itself, plus owned scan-N
    subfolders a prior run created to preserve foreign content."""
    yield scan_dir
    if os.path.isdir(scan_dir) and not os.path.islink(scan_dir):
        for name in sorted(os.listdir(scan_dir)):
            p = os.path.join(scan_dir, name)
            if (name.startswith("scan-") and os.path.isdir(p)
                    and os.path.exists(os.path.join(p, OWNED_MARKER))):
                yield p


def _writable_scan_dir(scan_dir):
    """A directory this script may clear and refill.

    A dir is writable only when it does not exist, is empty, or carries
    this script's ownership marker — a bare `manifest.json` or
    `summary.json` filename does NOT authorize clearing anything. A
    non-empty dir without the marker is foreign content: never deleted,
    and the newest owned `scan-N` subfolder inside it is reused (or a
    fresh one created), so a content folder passed by mistake survives
    untouched. A symlinked --scan-dir is resolved and used only if the
    resolved directory is provably ours.
    """
    if os.path.islink(scan_dir):
        real = os.path.realpath(scan_dir)
        if not (os.path.isdir(real)
                and os.path.exists(os.path.join(real, OWNED_MARKER))):
            sys.exit(f"refusing to use --scan-dir {scan_dir}: it is a "
                     f"symlink to {real}, which this script did not "
                     "create — ownership cannot be verified. Point "
                     "--scan-dir at a dedicated cache dir (e.g. "
                     ".style-scan/).")
        return real
    if os.path.exists(scan_dir) and not os.path.isdir(scan_dir):
        sys.exit(f"--scan-dir {scan_dir} exists and is not a directory")
    marker_p = os.path.join(scan_dir, OWNED_MARKER)
    if not os.path.isdir(scan_dir):
        os.makedirs(scan_dir)
    elif os.listdir(scan_dir) and not os.path.exists(marker_p):
        # non-empty foreign dir — never cleared. Reuse the newest owned
        # scan-N, else create a fresh one.
        owned = [os.path.join(scan_dir, n)
                 for n in sorted(os.listdir(scan_dir))
                 if n.startswith("scan-")
                 and os.path.isdir(os.path.join(scan_dir, n))
                 and os.path.exists(os.path.join(scan_dir, n,
                                                 OWNED_MARKER))]
        if owned:
            scan_dir = owned[-1]
        else:
            n = 1
            while os.path.exists(os.path.join(scan_dir, f"scan-{n}")):
                n += 1
            scan_dir = os.path.join(scan_dir, f"scan-{n}")
            os.makedirs(scan_dir)
        marker_p = os.path.join(scan_dir, OWNED_MARKER)
    with open(marker_p, "w") as fh:
        fh.write("owned by ai_sweep.py — safe to clear\n")
    return scan_dir


def _clear_owned(d):
    """Empty a dir this script owns — the marker is the only license."""
    if not os.path.exists(os.path.join(d, OWNED_MARKER)):
        sys.exit(f"internal guard: refusing to clear unowned dir {d}")
    shutil.rmtree(d)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, OWNED_MARKER), "w") as fh:
        fh.write("owned by ai_sweep.py — safe to clear\n")


def run_scan(target, questions, scan_dir, chunk_chars, overlap, rescan,
             timeout, retries):
    """Ensure a current scan exists; return the dir holding it.
    Cached only while BOTH the target and the question battery are
    unchanged — the scanner keys judgments to the battery, so a battery edit
    must force a rescan. Every failure is explicit: a stalled scan
    (--timeout), an unstartable CLI, or an incomplete judgment set all
    exit nonzero rather than passing the gate on a partial scan. Callers
    check SCANNER is set before calling."""
    sha = hashlib.sha256(open(target, "rb").read()).hexdigest()
    qsha = hashlib.sha256(open(questions, "rb").read()).hexdigest()
    if not rescan:
        for cand in _cache_candidates(scan_dir):
            if _cache_current(cand, sha, qsha):
                return cand
    out_dir = _writable_scan_dir(scan_dir)
    manifest_p = os.path.join(out_dir, "manifest.json")
    summary_p = os.path.join(out_dir, "summary.json")
    cmd = [SCANNER, "scan", os.path.abspath(target),
           "--questions", questions, "--output", out_dir,
           "--chunk-chars", str(chunk_chars),
           "--overlap", str(overlap)]
    last_err = "scan did not run"
    for _ in range(1 + max(0, retries)):
        _clear_owned(out_dir)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=timeout)
        except subprocess.TimeoutExpired:
            last_err = f"scanner timed out after {timeout}s"
            continue
        except OSError as exc:
            last_err = f"scanner could not start: {exc}"
            continue
        if not os.path.exists(summary_p):
            last_err = ("scan produced no summary:\n"
                        f"{r.stdout}\n{r.stderr}").rstrip()
            continue
        try:
            summ = json.load(open(summary_p))
        except (OSError, json.JSONDecodeError) as exc:
            last_err = f"summary.json unreadable: {exc}"
            continue
        if summ.get("complete"):
            with open(os.path.join(out_dir, BATTERY_MARKER), "w") as fh:
                fh.write(qsha)
            return out_dir
        # incomplete — report the unjudged range if the manifest survives
        judged = set()
        jdir = os.path.join(out_dir, "judgments")
        for name in os.listdir(jdir) if os.path.isdir(jdir) else []:
            if name.endswith(".json"):
                judged.add(name[:-5])
        missing = ["(manifest unreadable — range unknown)"]
        try:
            man = json.load(open(manifest_p))
            missing = [f"{p['line_start']}-{p['line_end']}"
                       for p in man.get("passages", [])
                       if p["passage_id"] not in judged]
            if not missing:
                missing = ["(all manifest passages judged, yet "
                           "summary.json never reported complete)"]
        except (OSError, json.JSONDecodeError, KeyError):
            pass
        last_err = ("scan incomplete — unjudged passages at lines "
                    + ", ".join(missing))
    sys.exit("register scan could not complete — " + last_err
             + ". Re-run with --rescan; do not treat the gate as passed "
               "over an unjudged range.")


def judgments(scan_dir):
    texts = {}
    try:
        man = json.load(open(os.path.join(scan_dir, "manifest.json")))
        texts = {p["passage_id"]: p.get("text", "")
                 for p in man.get("passages", [])}
    except (OSError, json.JSONDecodeError, KeyError):
        pass
    out = []
    jdir = os.path.join(scan_dir, "judgments")
    for name in sorted(os.listdir(jdir)):
        if not name.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(jdir, name)))
        except (OSError, json.JSONDecodeError):
            continue
        ans = d.get("response", {}).get("answers", {})
        reg = ans.get("ai_register", {})
        ff = ans.get("fact_free_sentences", {})
        dl = ans.get("deliberation_leak", {})
        out.append({
            "lines": (d.get("line_start"), d.get("line_end")),
            "score": reg.get("score"),
            "probs": reg.get("probabilities", {}),
            "confidence": reg.get("confidence"),
            "fact_free": ff.get("noul"),
            "plumb": dl.get("noul"),
            "text": texts.get(d.get("passage_id"), ""),
        })
    out.sort(key=lambda j: j["lines"][0] or 0)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--scan-dir", default=None,
                    help="scan CACHE dir (default: <file>/.style-scan). "
                         "The script may delete and recreate it — never a "
                         "content folder.")
    ap.add_argument("--questions", default=DEFAULT_QUESTIONS)
    ap.add_argument("--skip-fields", default=None, metavar="REGEX",
                    help="field-name pattern for lines that never render "
                         "(e.g. 'system_prompt|notes'); a matching "
                         "'field: |' block scalar exempts its whole block")
    ap.add_argument("--mechanical-only", action="store_true",
                    help="skip the register scan layer entirely")
    ap.add_argument("--no-plumbing", action="store_true",
                    help="disable the deliberation-leak axis (both the "
                         "phrase net and the battery dial)")
    ap.add_argument("--plumb", type=float, default=0.5,
                    help="deliberation_leak probability that puts a "
                         "passage on the plumbing worklist (default 0.5)")
    ap.add_argument("--threshold", type=float, default=1.5,
                    help="register score that puts a passage on the "
                         "worklist (default 1.5)")
    ap.add_argument("--watch", type=float, default=1.0,
                    help="register score worth a non-failing note "
                         "(default 1.0)")
    ap.add_argument("--chunk-chars", type=int, default=3000)
    ap.add_argument("--overlap", type=int, default=400)
    ap.add_argument("--timeout", type=float, default=900,
                    help="per-attempt scanner timeout in seconds "
                         "(default 900); a stalled CLI is an error, "
                         "never a hang")
    ap.add_argument("--retries", type=int, default=1,
                    help="extra scan attempts after a failed one "
                         "(default 1); retries are bounded")
    ap.add_argument("--rescan", action="store_true",
                    help="ignore the cached scan and rescan")
    ap.add_argument("--warn-only", action="store_true")
    a = ap.parse_args()

    target = a.file
    skip_re = (re.compile(r"^\s*(?:" + a.skip_fields + r")\s*:", re.I)
               if a.skip_fields else None)
    internal, lines = internal_lines(target, skip_re)
    keeps = load_keeps(target)
    kfile = os.path.basename(keeps_path(target))
    is_yaml = target.endswith((".yaml", ".yml"))
    fails, plumbs, n_ok = [], [], 0

    print("== MECHANICAL TELLS ==")
    emdash_lines = []
    for lo, level, label, excerpt in mechanical(
            lines, internal, is_yaml, plumb_on=not a.no_plumbing):
        if level == "emdash":
            emdash_lines.append(lo)
            continue
        if level == "fail":
            k = kept_keep(norm(lines[lo - 1]), keeps)
            if k:
                n_ok += 1
                print(f"  ok    L{lo} {label} — recorded keep in "
                      f"{kfile} (`{k[:60]}`)")
                continue
            fails.append(f"L{lo} {label}")
            print(f"  FAIL  L{lo} {label}")
            print(f"          {excerpt}")
        elif level == "plumb":
            k = kept_keep(norm(lines[lo - 1]), keeps)
            if k:
                n_ok += 1
                print(f"  ok    L{lo} plumb {label} — recorded keep "
                      f"(`{k[:60]}`)")
                continue
            plumbs.append(f"L{lo} {label}")
            print(f"  plumb L{lo} {label}")
            print(f"          {excerpt}")
        else:
            print(f"  note  L{lo} {label}")
            print(f"          {excerpt}")
    if emdash_lines:
        print(f"  note  em-dashes on {len(emdash_lines)} lines "
              f"(plain prose is em-dash-sparse, ~1/1500 words): "
              + ", ".join(f"L{l}" for l in emdash_lines))

    scan_dir = a.scan_dir or os.path.join(
        os.path.dirname(target) or ".", ".style-scan")
    real = os.path.realpath(target)
    under_private = any(
        real == os.path.realpath(root)
        or real.startswith(os.path.realpath(root) + os.sep)
        for root in PRIVATE_ROOTS)
    scan_blocked = False
    if under_private:
        print("\nfile sits under the operator's private tree — the "
              "passage scanner never receives it; the sweep is "
              "mechanical-tells only and INCOMPLETE. A mechanical-only "
              "pass is never the full gate; run the judgment pass over "
              "the file manually.")
        scanned = None
        scan_blocked = True
    elif a.mechanical_only:
        print("\n--mechanical-only: register layer skipped — the sweep "
              "is INCOMPLETE until the judgment pass runs over the file "
              "manually. A mechanical-only pass is never the full gate.")
        scanned = None
        scan_blocked = True
    elif not SCANNER:
        print(f"\n{SCANNER_MISSING_MSG} — the register "
              "layer CANNOT run; the sweep is mechanical-tells only and "
              "INCOMPLETE. Run the judgment pass over the file manually "
              "— a mechanical-only sweep is never the full gate.")
        scanned = None
        scan_blocked = True
    else:
        scanned = run_scan(target, a.questions, scan_dir, a.chunk_chars,
                           a.overlap, a.rescan, a.timeout, a.retries)
    if scanned is None:
        js = []
    else:
        js = judgments(scanned)
        if not js:
            sys.exit("no judgments in scan output — see .style-scan/")

    n_ok = 0
    if scanned is not None:
        print("\n== REGISTER WORKLIST ==")
    for j in js:
        score = j["score"]
        plumb_p = j["plumb"]
        reg = score is not None and score >= a.watch
        plm = (plumb_p is not None and plumb_p >= a.plumb
               and not a.no_plumbing)
        if not reg and not plm:
            continue
        lo, hi = j["lines"]
        if lo and hi and all(i in internal
                             for i in range(lo, hi + 1)):
            n_ok += 1
            print(f"  ok    L{lo}-{hi} — internal "
                  f"fields only, never rendered")
            continue
        ptext = norm(j["text"])
        k = kept_keep(ptext, keeps)
        if k:
            n_ok += 1
            print(f"  ok    L{lo}-{hi} — recorded keep in {kfile} "
                  f"(`{k[:60]}`)")
            continue
        ff = j["fact_free"]
        tag = (f'L{lo}-{hi} score={(score or 0):.2f} '
               f'conf={(j["confidence"] or 0):.2f} ff={(ff or 0):.2f}'
               + (f' plumb={plumb_p:.2f}' if plm else ''))
        if plm:
            plumbs.append(f"L{lo}-{hi} deliberation-leak "
                          f"p={plumb_p:.2f}")
        if reg and score >= a.threshold:
            fails.append(f"L{lo}-{hi} score={score:.2f}")
            print(f'  FAIL  {tag}')
            print(f'          {ptext[:150]}')
        elif plm:
            print(f'  plumb {tag}')
            print(f'          {ptext[:150]}')
        else:
            n_ok += 1
            print(f'  note  {tag} — below threshold; judgment-pass reading')
    if scanned is not None:
        print(f"  ({n_ok} cleared/below threshold)")

    if plumbs:
        print("\n== PLUMBING HYPOTHESES ==")
        for p in plumbs:
            print("  -", p)
        print("Deliberation-leak candidates — the test is whose "
              "activity is the subject. Report only, never silent-cut: "
              "the operator rules on each (CUT / REWRITE with the "
              "finding as subject / KEEP recorded in "
              f"{keeps_path(target)} — an unrecorded keep re-flags).")

    print()
    if fails:
        print("FAIL:")
        for f in fails:
            print("  -", f)
        print()
        print("Resolve each flagged item in place: rewrite to "
              "fact-delivering prose (the fix is usually deletion — a scaffolding "
              "sentence loses nothing when cut), or keep it where the "
              "flag is a false positive — recording a keep is part of "
              "the ruling: the kept wording in `backticks` plus a "
              "one-line reason go into <file-stem>.keeps.md beside the "
              "target; an unrecorded keep re-flags and fails. "
              "Register rewrites preserve every fact: "
              "numbers, claims, and severities do not move. The "
              "fact_free dial is context for your adjudication, not "
              "an auto-clear.")
    else:
        print("sweep clean — no passage reads as machine register "
              "above threshold, and no mechanical tell is unresolved.")
    if scan_blocked:
        print("\nINCOMPLETE: the register layer never ran — a "
              "mechanical-only sweep is not the full gate. Run the "
              "judgment pass over the file manually.")
    sys.exit(0 if (a.warn_only or (not fails and not scan_blocked))
             else 1)


if __name__ == "__main__":
    main()
