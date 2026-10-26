#!/usr/bin/env python3
"""Few-cluster inference gate for a review run.

Why this exists. Models reach for the wild cluster bootstrap as *the* few-clusters answer,
and for `boottest`'s default (WCR-C: ordinary restricted residuals, CV1 t-statistic) as the
way to run it. That is the training default, and in a design with a handful of effective
clusters or shocks it is wrong: lead with the cluster jackknife (CV3), use the restricted
bootstrap only in MacKinnon-Nielsen-Webb's WCR-S form (boottest option `jk`), and settle a
shift-share design by randomization over the shocks. Prose rules did not stop the default,
so this script checks the run's files.

Checks (FAIL exits 1):
  F1  every Stata `boottest` call names the jackknifed DGP (`jk` / `jackknife`), or carries a comment
      tag `<variant>-robustness` naming the variant it actually runs — `WCR-C`, `WCR-V`, `WCR-B`,
      `WCU` (or `WCU-C` etc.) or `WRE` (companion or robustness rows, never the sole cited result);
  F2  every R/Python wild-bootstrap call (fwildclusterboot / wildboottest) sets bootstrap_type
      "31" (WCR-S), or carries the robustness tag of its variant ("11" WCR-C, "13" WCR-V, "33" WCR-B);
  F3  report text never cites a bare "WCR" / "wild cluster bootstrap" without its variant
      (WCR-S, WCR-C, WCR-V, WCR-B, WCU, WRE) in the same line;
  F4  a run with a shift-share report carries a "Placebo-shock rejection rates" section
      (rejection rates of every unit-level test the run cites, across reassigned shocks), and that section
      gives the randomization (permutation) p of the actual statistic;
  F6  every Stata `vtf` call carries the tag `VtF-CR1-robustness`: vtf.ado takes only robust or cluster() (CR1/HC1)
      variance and has no jackknife input, so its output is a CR1 companion row, never the VtF result in a design with
      few or unequal clusters or shocks;
  F7  a run with an IV-diagnostics report carries a VtF set computed on jackknife inputs: a line naming VtF with
      `jackknife` or `CV3` (jackknife covariance of the reduced-form and first-stage coefficients, F-hat and r-hat
      from it), or a line `VtF-jackknife: not applicable — <reason>`.
  F8  no Stata `boottest` call uses the Anderson–Rubin option (`ar`/`arubin`) unless tagged
      `AR-boottest-robustness`: its bootstrap DGP applies the model constraints only, not the null, so the
      AR set comes from the transformed outcome y - b0*endog, tested at zero over a grid;
  F9  every Stata `boottest` call with `jk` carries `noci`: boottest prints a confidence set by default for one
      hypothesis, and with `jk` that set inverts nonzero nulls where `jk` is not WCR-S;
  F10 every Stata `boottest` call is followed within six lines by `assert !missing(r(p))` (or `assert r(p) < .`):
      a refused model exits with rc 0 and a missing r(p);
  F11 a Stata do-file that runs `honestdid` runs every `csdid` in it with `long2` (universal base; `long` reverses
      the pre-period signs, the default base varies), and passes `pre()`/`post()` as positions in e(b), never
      negative event times; an R file that runs HonestDiD on `did::att_gt` sets `base_period = "universal"`;
  F12 a run with a shift-share report carries a shock-level jackknife (a line naming the shock-level jackknife or
      CV3) or a line `Shock-level jackknife: not applicable — <reason>`;
  F13 a run with an IV-diagnostics report carries the Montiel Olea–Pflueger effective F (a line naming `effective F`,
      `F_eff`, `Montiel Olea`, `MOP`, or `weakivtest`), or a line `Effective-F: not applicable — <reason>`.
  A module report that is a not-applicable stub (a line `Status: NOT_APPLICABLE — <reason>`, the marker
  code-and-data/SKILL.md gives stubs) owes none of F4, F7, F12, F13; check_manifest.py fails a stub on a
  module the walk marks fired.
  F5  `inference-superseded.csv` (path,reason,replaced_by), if present, is well formed: every row names an
      existing path, a reason, and an existing replacement. Listed scripts are skipped by the script checks
      (F1, F2, F6, F8–F11, WARN): they are historical runs whose numbers no report cites as primary inference
      (a replacement battery recomputes them). Report text (F3) is never exempt.
Skipped as the authors' deposited code or third-party code: pkg/ and pkg_*/ (the deposit,
copies of it run under a variant, patch folders), ado/ and ado_*/ (installed Stata packages),
04_replication_*. Review-run bootstraps belong in work/scripts/.
WARN:
  - hand-written wild bootstraps in Python/R (Webb/Rademacher draws) that never mention the jackknife: confirm
    the DGP is WCR-S, or tag the file as robustness;
  - hand-written cluster-jackknife / CV3 loops that demean or partial out fixed effects once outside the loop
    instead of re-estimating them in each leave-out fit;
  - R `ur.df()` calls in cointegration / residual checks that do not call `urca:::.urcval` for MacKinnon
    response-surface critical values.

Usage: python3 check_inference.py --root <job> [--list]
"""
import argparse, re, sys
from pathlib import Path

SKIP_DIRS = {"pkg", "ado", "lit", "downloads", "__pycache__", ".git", "dl"}
SKIP_PREFIXES = ("pkg_", "ado_", "04_replication")
VTF_TAG = re.compile(r"VtF-CR1-robustness", re.I)
ROBUST_TAG = re.compile(r"(WCU(-[BCSV])?|WCR-[BCV]|WRE)-robustness", re.I)
NA_STUB = re.compile(r"^[ \t>#*_`]*Status[*_`]*[ \t]*:[ \t*_`]*NOT_APPLICABLE[*_`]*[ \t]*[—–:-]+[ \t]*\w", re.M)
REPORT_GLOBS = ["SYNTHESIS.md", "ISSUES.md", "review/*.md", "review/**/*.md", "analysis/**/*.md", "analysis/**/*.csv"]


def skipped(parts):
    return any(x in SKIP_DIRS or x.startswith(SKIP_PREFIXES) for x in parts)


def walk(root, suffixes):
    for p in root.rglob("*"):
        if p.suffix.lower() in suffixes and p.is_file():
            if skipped(p.relative_to(root).parts[:-1]):
                continue
            yield p


PREFIX = r"((cap(t|tu|tur|ture)?|qui(e|et|etl|etly)?|n(o|oi|ois|oisi|oisil|oisily)?)\s+)*"
JK_OPT = re.compile(r"\b(jk|jack|jackk|jackkn|jackkni|jackknif|jackknife)\b")
AR_OPT = re.compile(r"\bar(u(b(i(n)?)?)?)?\b", re.I)
AR_TAG = re.compile(r"AR-boottest-robustness", re.I)
P_ASSERT = re.compile(
    PREFIX + r"assert\b.*(?:"
    r"!\s*(?:missing|mi|miss|missi|missin)\(\s*r\(p\)\s*\)"
    r"|(?:missing|mi|miss|missi|missin)\(\s*r\(p\)\s*\)\s*==\s*0"
    r"|r\(p\)\s*(?:<|!=|~=|~=)\s*\.(?!\d)"
    r"|\.(?!\d)\s*(?:>|!=|~=|~=)\s*r\(p\)"
    r")"
)


def strip_stata_comments(line):
    s = re.sub(r"/\*.*?\*/", " ", line).strip()
    if s.startswith("*") or s.startswith("//"):
        return ""
    return re.sub(r"(^|\s)//.*$", "", s).strip()


def has_p_assert(after_lines):
    return any(P_ASSERT.match(strip_stata_comments(l)) for l in after_lines)


def extract_section(text, title_re):
    m = re.search(rf"^(#+)\s*{title_re}\b", text, re.M | re.I)
    if not m:
        return None
    lvl = len(m.group(1))
    rest = text[m.end():]
    end = re.search(rf"^#{{1,{lvl}}}\s", rest, re.M)
    return rest[:end.start()] if end else rest


def cmd_calls(text, cmd):
    """Yield (lineno, last line index, logical line) for Stata `cmd` calls, joining /// continuations,
    skipping comment lines."""
    lines = text.splitlines(); i = 0
    pat = re.compile(PREFIX + cmd + r"\b")
    while i < len(lines):
        raw = lines[i]; start = i
        while raw.rstrip().endswith("///") and i + 1 < len(lines):
            i += 1; raw = raw.rstrip()[:-3] + " " + lines[i]
        s = raw.strip()
        if not s.startswith("*") and not s.startswith("//") and pat.match(s):
            yield start + 1, i, raw
        i += 1


def stata_calls(text):
    """Yield (lineno, logical line) for boottest calls."""
    for ln, _, raw in cmd_calls(text, "boottest"):
        yield ln, raw


def vtf_calls(text):
    """Yield (lineno, logical line) for Stata vtf calls."""
    for ln, _, raw in cmd_calls(text, "vtf"):
        yield ln, raw


def options(call):
    """The option list of a Stata call: comments removed, text after the first top-level comma, parenthesised
    arguments blanked (so `cluster(ar)` is not the `ar` option)."""
    s = re.sub(r"/\*.*?\*/", " ", call)
    s = re.sub(r"(^|\s)//.*$", " ", s)
    depth = 0
    for k, ch in enumerate(s):
        depth += ch in "([{"; depth -= ch in ")]}"
        if ch == "," and depth == 0:
            s = s[k + 1:]; break
    else:
        return ""
    prev = None
    while prev != s:
        prev, s = s, re.sub(r"\([^()]*\)", "()", s)
    return s


def r_call_args(code, start):
    """Text of the R call whose name starts at `start`, through its balanced closing paren."""
    k = code.find("(", start); depth = 0
    for j in range(k, len(code)):
        depth += code[j] == "("; depth -= code[j] == ")"
        if depth == 0:
            return code[start: j + 1]
    return code[start:]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--list", action="store_true")
    a = ap.parse_args(); root = Path(a.root).resolve()
    fails, warns = [], []
    superseded = []
    sup = root / "inference-superseded.csv"
    if sup.exists():
        import csv
        for i, r in enumerate(csv.DictReader(sup.open()), 2):
            path, reason, rep = (r.get("path") or "").strip(), (r.get("reason") or "").strip(), (r.get("replaced_by") or "").strip()
            if not path or not reason or not rep or not (root / path).exists() or not (root / rep).exists():
                fails.append(f"F5 inference-superseded.csv:{i}: needs an existing path, a reason and an existing replaced_by ({path!r})")
            else:
                superseded.append(path.rstrip("/"))
    def is_sup(p):
        rel = str(p.relative_to(root))
        return any(rel == s_ or rel.startswith(s_ + "/") for s_ in superseded)

    for p in walk(root, {".do"}):
        if is_sup(p):
            continue
        text = p.read_text(errors="ignore"); lines = text.splitlines(); rel = p.relative_to(root)
        for ln, last, call in cmd_calls(text, "boottest"):
            o = options(call)
            if AR_OPT.search(o) and not AR_TAG.search(call):
                fails.append(f"F8 {rel}:{ln}: boottest `ar` (bootstrap DGP not null-imposed) without `AR-boottest-robustness`: {call.strip()[:120]}")
            if JK_OPT.search(o) and not re.search(r"\bnoci\b", o):
                fails.append(f"F9 {rel}:{ln}: boottest `jk` without `noci` (its default confidence set is not WCR-S): {call.strip()[:120]}")
            if not has_p_assert(lines[last + 1: last + 7]):
                fails.append(f"F10 {rel}:{ln}: boottest not followed by `assert !missing(r(p))` (a refusal returns rc 0, r(p) missing): {call.strip()[:120]}")
            if ROBUST_TAG.search(call) or (AR_OPT.search(o) and AR_TAG.search(call)):
                continue
            if not JK_OPT.search(o):
                fails.append(f"F1 {rel}:{ln}: boottest without `jk` (WCR-C default): {call.strip()[:120]}")

        for ln, call in vtf_calls(text):
            if not VTF_TAG.search(call):
                fails.append(f"F6 {rel}:{ln}: vtf (CR1/HC1 variance only) without `VtF-CR1-robustness`: {call.strip()[:120]}")

        hd = list(cmd_calls(text, "honestdid"))
        if hd:
            for ln, _, call in cmd_calls(text, "csdid"):
                if not re.search(r"\blong2\b", options(call)):
                    fails.append(f"F11 {rel}:{ln}: csdid without `long2` in a file that runs honestdid (needs a universal base): {call.strip()[:120]}")
            for ln, _, call in hd:
                if re.search(r"\b(pre|post)\s*\(\s*-", call):
                    fails.append(f"F11 {rel}:{ln}: honestdid pre()/post() given as event times; they are positions in e(b): {call.strip()[:120]}")

        if re.search(r"\b(cv3|cluster[._ -]?jackknif|leave[._ -]?one[._ -]?cluster)", text, re.I):
            do_code = "\n".join(strip_stata_comments(l) for l in lines)
            for lp in re.finditer(r"^\s*(foreach|forvalues)\b", do_code, re.M):
                if re.search(r"\b(reghdfe|areg)\b.*\bresid", do_code[:lp.start()], re.I) \
                        and not re.search(r"\b(reghdfe|areg|xtreg)\b|\bi\.", do_code[lp.start():], re.I):
                    warns.append(f"WARN {rel}: hand-written CV3/jackknife loop partials or demeans before `{lp.group(1)}` without re-estimating fixed effects inside the loop")
                    break

    for p in walk(root, {".r", ".py"}):
        if is_sup(p):
            continue
        t = p.read_text(errors="ignore"); rel = p.relative_to(root)
        code = "\n".join(l if not l.lstrip().startswith("#") else "" for l in t.splitlines())
        code = re.sub(r'(\'\'\'|""")(.|\n)*?\1', lambda m_: "\n" * m_.group(0).count("\n"), code)
        for m in re.finditer(r"(fwildclusterboot::)?\bboottest\s*\(|wildboottest\s*\(", code):
            seg = code[m.start(): m.start() + 600]
            line = code[: m.start()].count("\n") + 1
            if ROBUST_TAG.search(seg):
                continue
            if not re.search(r"bootstrap_type\s*=\s*['\"]31['\"]", seg):
                fails.append(f"F2 {rel}:{line}: wild bootstrap without bootstrap_type '31' (WCR-S)")
        if re.search(r"\b(HonestDiD|createSensitivityResults(_relativeMagnitudes)?|honest_did)\b", code):
            for m in re.finditer(r"(did::)?\batt_gt\s*\(", code):
                seg = r_call_args(code, m.start())
                line = code[: m.start()].count("\n") + 1
                if not re.search(r"base_period\s*=\s*['\"]universal['\"]", seg):
                    fails.append(f"F11 {rel}:{line}: att_gt without base_period = 'universal' in a file that runs HonestDiD")
        if re.search(r"\b(webb|rademacher)\b", t, re.I) and re.search(r"wild|bootstrap", t, re.I) \
                and not re.search(r"jackknif|WCR-S|wcr_s|bootstrap_type", t, re.I) and not ROBUST_TAG.search(t):
            warns.append(f"WARN {rel}: hand-written wild bootstrap with no jackknifed DGP; confirm WCR-S or tag as robustness")
        if re.search(r"\bur\.df\s*\(", code) and re.search(r"cointegrat|engle[._ -]?granger", t, re.I) \
                and not re.search(r"\.urcval\b", code):
            warns.append(f"WARN {rel}: ur.df() in a cointegration file without urca:::.urcval() (ur.df prints raw unit-root critical values, not MacKinnon cointegration response surfaces)")
        if re.search(r"\b(cv3|cluster[._ -]?jackknif|leave[._ -]?one[._ -]?cluster)", t, re.I):
            for lp in re.finditer(r"^\s*for\b", code, re.M):
                if re.search(r"demean|within_transform|resid\(|feols|reghdfe", code[:lp.start()], re.I) \
                        and not re.search(r"feols|plm|lfe::felm|Absorb|C\(|factor\(", code[lp.start():]):
                    warns.append(f"WARN {rel}: hand-written CV3/jackknife loop partials or demeans before `for` without re-estimating fixed effects inside the loop")
                    break

    excluded = set()                              # HANDOFF.md `## excluded` entries are not evidence: not scanned
    hp = root / "HANDOFF.md"
    if hp.exists():
        sec = re.search(r"^## excluded[ \t]*$(.*?)(?=^## |\Z)", hp.read_text(errors="ignore"), re.M | re.S)
        if sec:
            for line in sec.group(1).splitlines():
                m_ = re.match(r"^\s*-\s*`?([^|`]+?)`?\s*\|", line)
                if m_:
                    excluded.add(m_.group(1).strip())
    bare = re.compile(r"\bWCR\b(?![-‑–]\s?[BCSV]\b)|wild cluster bootstrap", re.I)
    variant = re.compile(r"\b(WCR[-‑–][BCSV]|WCU([-‑–][BCSV])?|WRE)\b", re.I)
    seen = set()
    for g in REPORT_GLOBS:
        for p in root.glob(g):
            if p in seen or not p.is_file() or skipped(p.relative_to(root).parts[:-1]) \
                    or str(p.relative_to(root)) in excluded:
                continue
            seen.add(p)
            for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
                if bare.search(line) and not variant.search(line):
                    fails.append(f"F3 {p.relative_to(root)}:{i}: wild bootstrap cited without its variant")

    def stub(p):
        return bool(NA_STUB.search(p.read_text(errors="ignore")))
    ss = [p for p in (list(root.glob("analysis/code-and-data/shift-share*REPORT.md")) + list(root.glob("review/*shift-share*.md")))
          if str(p.relative_to(root)) not in excluded and not stub(p)]
    sjk = re.compile(r"shock[- ]level\s+jackknif|delete-one-shock|jackknif.*shock|shock.*jackknif|CV3.*shock|shock.*CV3|Shock-level jackknife:\s*not applicable", re.I)
    for p in ss:
        rel = str(p.relative_to(root))
        txt = p.read_text(errors="ignore")
        sec = extract_section(txt, r"Placebo-shock rejection rates")
        if sec is None:
            fails.append(f"F4 shift-share report present but no 'Placebo-shock rejection rates' section: {rel}")
        elif not re.search(r"randomi[sz]ation|permutation|\bRI\b", sec, re.I):
            fails.append(f"F4 shift-share 'Placebo-shock rejection rates' section without randomization/permutation p of the actual statistic: {rel}")
        if not any(sjk.search(l) for l in txt.splitlines()):
            fails.append(f"F12 shift-share report without a shock-level jackknife (CV3): {rel}")

    ivr_cands = list(root.glob("analysis/code-and-data/iv-diagnostics*REPORT.md")) + list(root.glob("analysis/code-and-data/iv-REPORT.md")) + list(root.glob("review/*iv-diagnostics*.md"))
    ivr = []
    for p in ivr_cands:
        if p not in ivr and str(p.relative_to(root)) not in excluded and not stub(p):
            ivr.append(p)
    vjk = re.compile(r"VtF.*(jackknif|CV3)|(jackknif|CV3).*VtF|VtF-jackknife:\s*not applicable", re.I)
    eff = re.compile(r"(?:(?i:effective\s+F|F[_~]?eff\b|Montiel\s+Olea|Olea.{0,20}Pflueger|weakivtest|Effective-F:\s*not applicable)|\bMOP\b)")
    for p in ivr:
        rel = str(p.relative_to(root))
        txt = p.read_text(errors="ignore")
        if not any(vjk.search(l) for l in txt.splitlines()):
            fails.append(f"F7 IV-diagnostics report without a VtF set on jackknife inputs: {rel}")
        if not any(eff.search(l) for l in txt.splitlines()):
            fails.append(f"F13 IV-diagnostics report without Montiel Olea-Pflueger effective F: {rel}")

    by = {}
    for f in fails:
        k = f.split()[0]; by[k] = by.get(k, 0) + 1
    for f in (fails if a.list else fails[:40]): print(f)
    if len(fails) > 40 and not a.list: print(f"... {len(fails) - 40} more (use --list)")
    for w in warns: print(w)
    print(f"check_inference: {len(fails)} FAIL ({', '.join(f'{k} {v}' for k, v in sorted(by.items(), key=lambda kv: (int(kv[0][1:]), kv[0]))) or 'none'}), {len(warns)} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
