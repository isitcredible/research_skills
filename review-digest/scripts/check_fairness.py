#!/usr/bin/env python3
"""Fairness sweep for a review issue ledger (ISSUES.md) before rendering.

The upstream `review` is adversarial by design; its register can carry
motive- or direction-of-selection attributions into the ledger. This
sweep scans the ledger with the passage scanner and the fairness battery
(`fairness-questions.json`, same directory): every passage gets an
attribution-strength score (0 = none … 3 = purpose asserted) and an
intent-disclaimer judgment. Detection is the model's, not a wordlist —
a flagged passage means the text *reads as* assigning motive or
direction to the authors.

Corner-landing — a choice coinciding with a convenient endpoint — is
correlation, not intent: the causal arrow runs both ways (the claim may
have driven the choice, or the choice may simply be what the authors
made and reported). Chronology and asymmetric choices are the same
class: version/draft movement toward the claim, or a stated rule
applied where it helps and waived where it hurts, support the
*descriptive* finding (what changed, where the rule bound, the measured
effect) — never a motive attribution on their own. Whether a choice was
*correct* is a descriptive question the ledger may adjudicate; *why* it
was made needs evidence supporting that particular inference.

Each flagged passage is a worklist item for the judgment pass (see
SKILL.md, "Fairness gate"). Resolve a hit by:

  - rewriting to the descriptive claim — what was done, its measured
    effect, its documentation status ("silently dropped" -> "dropped;
    the exclusion is undocumented"); or
  - keeping the attribution where the corpus carries intent-evidence —
    correspondence, a dated referee report, an explicit author statement
    naming why the choice was made, or a documented alternative the
    authors demonstrably saw and rejected — and recording the kept
    wording in `backticks` in FAIRNESS.md beside the ledger, with an
    `evidence:` field naming the corpus file AND a locator in it
    (`file:line`, `file:line-line`, or `file §section`). A keep without
    resolvable evidence is no ruling and suppresses nothing.

A keep is sentence-scoped, not passage-scoped. The battery scores
passages, so a flagged passage carrying a kept phrase is cleared only
by a residual re-score: the sentences overlapping a kept phrase are
removed, the rest is re-scanned with the same battery, and the passage
passes only if that residual scores below --threshold. Another
attribution elsewhere in the passage still needs its own ruling.

The disclaimer dial is context for the pass, not an auto-clear: a
passage can disclaim fabrication in one clause and insinuate in
another, so a high disclaimer score does not suppress a flag.

Hard fails (exit 1): any flagged passage that is neither rewritten nor
recorded in FAIRNESS.md; a missing passage scanner; a timed-out,
unstartable, or incomplete scan. --warn-only for drafts.

Usage:
  python3 check_fairness.py ISSUES.md [--scan-dir DIR]
      [--questions PATH] [--threshold 1.5] [--watch 1.0]
      [--chunk-chars 3000] [--overlap 400] [--timeout 900]
      [--retries 1] [--rescan] [--warn-only]

Requires the operator's passage scanner: PASSAGE_SCANNER names an
executable taking `<scanner> scan FILE --questions BATTERY --output DIR
--chunk-chars N --overlap N` and writing manifest.json, summary.json and
judgments/ under DIR. Unset or not executable, the gate exits with the
scanner-missing message and the manual pass substitutes. Scan output is cached under the ledger's
`.fairness-scan/` and reused while the file is unchanged.
--scan-dir is a CACHE dir the script owns: a `.check-fairness-owned`
marker file gates every deletion — a non-empty dir without it is never
cleared (a fresh owned scan-N subfolder is used instead), and a
symlinked dir must resolve to one the script created.
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
DEFAULT_QUESTIONS = os.path.join(HERE, "fairness-questions.json")


def passage_scanner():
    """The operator-configured passage scanner: the executable named by
    PASSAGE_SCANNER, else None. No other lookup."""
    p = os.path.expanduser(os.environ.get("PASSAGE_SCANNER", ""))
    return p if p and os.path.isfile(p) and os.access(p, os.X_OK) else None


SCANNER = passage_scanner()
OWNED_MARKER = ".check-fairness-owned"
BATTERY_MARKER = ".check-fairness-battery-sha"


def norm(s):
    s = re.sub(r"[*_]", "", s)
    return re.sub(r"\s+", " ", s).strip()


EVIDENCE_LOC = re.compile(
    r"^(?P<file>.+?)(?::(?P<l1>\d+)(?:\s*[-–]\s*(?P<l2>\d+))?"
    r"|\s+§\s*(?P<sec>\S.*))$")


def _evidence_resolves(block, base_dir):
    """An `evidence:` field in block names a file under base_dir AND a
    locator in it — `file:line`, `file:line-line` (lines that exist), or
    `file §section`. A bare filename points at nothing a reader can check."""
    m = re.search(r"evidence:\s*([^;\n]+)", block, re.I)
    if not m:
        return False
    loc = EVIDENCE_LOC.match(m.group(1).strip().strip("`'\"").strip())
    if not loc:
        return False
    path = os.path.join(base_dir, loc.group("file").strip().strip("`'\""))
    if not os.path.isfile(path):
        return False
    if loc.group("l1"):
        lo = int(loc.group("l1"))
        hi = int(loc.group("l2") or lo)
        with open(path, encoding="utf-8", errors="replace") as fh:
            n = sum(1 for _ in fh)
        return 1 <= lo <= hi <= n
    return True


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|(?<=[.!?][\"'”’)\]])\s+")


def residual_text(ptext, keeps):
    """The passage minus every sentence overlapping a kept phrase. Spans
    are located on the casefolded sentences re-joined with single spaces
    (the normalized passage's own spacing); a phrase straddling a
    sentence boundary removes both sentences."""
    sents = [x for x in SENT_SPLIT.split(ptext) if x.strip()]
    low, spans, pos = [], [], 0
    for x in sents:
        f = x.casefold()
        spans.append((pos, pos + len(f)))
        low.append(f)
        pos += len(f) + 1
    joined = " ".join(low)
    hits = []
    for k in keeps:
        start = joined.find(k)
        while start != -1:
            hits.append((start, start + len(k)))
            start = joined.find(k, start + 1)
    return " ".join(x for x, (a, b) in zip(sents, spans)
                    if not any(h0 < b and h1 > a for h0, h1 in hits))


def residual_score(residual, scan_root, questions, a):
    """Re-score the residual alone with the same battery; cached by
    content under the main scan dir. Returns the max passage score."""
    rsha = hashlib.sha256(residual.encode("utf-8")).hexdigest()[:16]
    src = os.path.join(scan_root, f"residual-{rsha}.md")
    if not os.path.exists(src):
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(residual + "\n")
    rdir = run_scan(src, questions, os.path.join(scan_root, f"residual-{rsha}"),
                    a.chunk_chars, a.overlap, a.rescan, a.timeout, a.retries)
    scores = [j["score"] for j in judgments(rdir) if j["score"] is not None]
    return max(scores) if scores else 0.0


def _phrases(block):
    return {span for m in re.finditer(r"`([^`]+)`", block)
            for span in (norm(m.group(1)).casefold(),)
            if len(span) >= 15}


def logged_keeps(ledger_path):
    """Normalized set of kept wordings recorded in FAIRNESS.md beside the
    ledger — `backtick` spans only, and only distinctive phrases (>=15
    chars). A single word like `fabrication` must not be able to mask a
    whole passage.

    A keep counts only when its entry also carries `evidence:` naming a
    file under the ledger's directory — the intent-evidence the keep
    rests on. An `### `-headed entry's evidence covers its phrases; a
    bare list/paragraph line must carry its own `evidence:`. A keep with
    no resolvable evidence is no ruling and suppresses nothing, and a
    keep binds to the recorded wording: changed text re-flags.
    """
    base = os.path.dirname(ledger_path) or "."
    path = os.path.join(base, "FAIRNESS.md")
    if not os.path.exists(path):
        return set()
    text = open(path, encoding="utf-8", errors="replace").read()
    keeps = set()
    for chunk in re.split(r"(?m)^(?=### )", text):
        if _evidence_resolves(chunk, base):
            keeps.update(_phrases(chunk))
        else:
            for ln in chunk.splitlines():
                if _evidence_resolves(ln, base):
                    keeps.update(_phrases(ln))
    return keeps


def _cache_current(scan_dir, sha, qsha):
    """scan_dir holds a complete scan of the current ledger + battery."""
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
                     ".fairness-scan/).")
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
        fh.write("owned by check_fairness.py — safe to clear\n")
    return scan_dir


def _clear_owned(d):
    """Empty a dir this script owns — the marker is the only license."""
    if not os.path.exists(os.path.join(d, OWNED_MARKER)):
        sys.exit(f"internal guard: refusing to clear unowned dir {d}")
    shutil.rmtree(d)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, OWNED_MARKER), "w") as fh:
        fh.write("owned by check_fairness.py — safe to clear\n")


def run_scan(ledger, questions, scan_dir, chunk_chars, overlap, rescan,
             timeout, retries):
    """Ensure a current scan exists; return the dir holding it.
    Cached only while BOTH the ledger and the question battery are
    unchanged — the scanner keys judgments to the battery, so a battery edit
    must force a rescan. Every failure is explicit: a missing CLI, a
    stalled scan (--timeout), or an incomplete judgment set all exit
    nonzero rather than passing the gate on a partial scan."""
    sha = hashlib.sha256(open(ledger, "rb").read()).hexdigest()
    qsha = hashlib.sha256(open(questions, "rb").read()).hexdigest()
    if not rescan:
        for cand in _cache_candidates(scan_dir):
            if _cache_current(cand, sha, qsha):
                return cand
    if not SCANNER:
        sys.exit("no passage scanner (PASSAGE_SCANNER unset or not "
                 "executable) — the fairness sweep cannot scan; run the fairness judgment pass over the "
                 "ledger manually per SKILL.md — never skip it.")
    out_dir = _writable_scan_dir(scan_dir)
    manifest_p = os.path.join(out_dir, "manifest.json")
    summary_p = os.path.join(out_dir, "summary.json")
    cmd = [SCANNER, "scan", os.path.abspath(ledger),
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
    sys.exit("fairness scan could not complete — " + last_err
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
        attr = ans.get("attribution_strength", {})
        disc = ans.get("intent_disclaimer", {})
        out.append({
            "lines": (d.get("line_start"), d.get("line_end")),
            "score": attr.get("score"),
            "probs": attr.get("probabilities", {}),
            "confidence": attr.get("confidence"),
            "disclaimer": disc.get("noul"),
            "text": texts.get(d.get("passage_id"), ""),
        })
    out.sort(key=lambda j: j["lines"][0] or 0)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ledger")
    ap.add_argument("--scan-dir", default=None,
                    help="scan CACHE dir (default: <ledger>/.fairness-scan). "
                         "The script may delete and recreate it — never a "
                         "content folder.")
    ap.add_argument("--questions", default=DEFAULT_QUESTIONS)
    ap.add_argument("--threshold", type=float, default=1.5,
                    help="attribution score that puts a passage on the "
                         "worklist (default 1.5)")
    ap.add_argument("--watch", type=float, default=1.0,
                    help="attribution score worth a non-failing note "
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

    ledger = a.ledger
    scan_dir = a.scan_dir or os.path.join(
        os.path.dirname(ledger) or ".", ".fairness-scan")
    scan_dir = run_scan(ledger, a.questions, scan_dir, a.chunk_chars,
                        a.overlap, a.rescan, a.timeout, a.retries)
    js = judgments(scan_dir)
    if not js:
        sys.exit("no judgments in scan output — see .fairness-scan/")
    keeps = logged_keeps(ledger)

    fails, n_ok = [], 0
    print("== ATTRIBUTION WORKLIST ==")
    for j in js:
        score = j["score"]
        if score is None or score < a.watch:
            continue
        lo, hi = j["lines"]
        ptext = norm(j["text"])
        keep_hit = next((k for k in keeps if k and k in ptext.casefold()),
                        None)
        disc = j["disclaimer"]
        tag = (f'L{lo}-{hi} score={score:.2f} conf={j["confidence"]:.2f}'
               f' disc={disc:.2f}')
        if keep_hit and score >= a.threshold:
            residual = residual_text(ptext, keeps)
            rscore = (residual_score(residual, scan_dir, a.questions, a)
                      if residual else 0.0)
            if rscore < a.threshold:
                n_ok += 1
                print(f'  ok    {tag} — keep `{keep_hit[:70]}` in '
                      f'FAIRNESS.md; rest of passage re-scored '
                      f'{rscore:.2f} < {a.threshold}')
            else:
                fails.append(f"L{lo}-{hi} score={score:.2f} (keep covers "
                             f"only part; residual {rscore:.2f})")
                print(f'  FAIL  {tag} — keep `{keep_hit[:70]}` clears '
                      'only its own sentence(s); the rest of the passage '
                      f're-scores {rscore:.2f} ≥ {a.threshold} — rule on '
                      'the other attribution too')
                print(f'          {residual[:150]}')
        elif keep_hit:
            n_ok += 1
            print(f'  ok    {tag} — keep `{keep_hit[:70]}` in FAIRNESS.md'
                  ' (below threshold)')
        elif score >= a.threshold:
            fails.append(f"L{lo}-{hi} score={score:.2f}")
            print(f'  FAIL  {tag}')
            print(f'          {ptext[:150]}')
        else:
            n_ok += 1
            print(f'  note  {tag} — below threshold; judgment-pass reading')
    print(f"  ({n_ok} cleared/below threshold)")

    print()
    if fails:
        print("FAIL:")
        for f in fails:
            print("  -", f)
        print()
        print("Resolve each flagged passage: rewrite descriptively (what "
              "was done, its measured effect, its documentation status), "
              "or keep it only with intent-evidence in the corpus — and "
              "record the kept wording in `backticks` in FAIRNESS.md "
              "beside the ledger, with `evidence:` naming the corpus file "
              "that holds it. Chronology and asymmetric choices are "
              "descriptive evidence, not intent. The disclaimer dial is "
              "context for your adjudication, not an auto-clear.")
    else:
        print("sweep clean — no passage reads as attributing motive or "
              "direction of selection above threshold.")
    sys.exit(0 if (a.warn_only or not fails) else 1)


if __name__ == "__main__":
    main()
