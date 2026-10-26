#!/usr/bin/env python3
"""check_coverage.py — completeness over the paper's surface and the packet,
not just the run's index.

Substance passes verify declared rows; this script generates the rows that
were never declared — the objects no pass can see because they were filed as
description instead of checked. Run from the job root; writes coverage.csv.

FAIL rows (exit 1) — remediate by deriving the row or marking it n/a in
coverage-na.csv:

1. PRINTED SURFACE. Every equation tag — lettered (A.9, B.2, OA.1 …) or
   numbered, a `(N)` tag at the end of a line the way pdftotext lands
   display-equation numbers — and every printed `Table <id>` or
   `Figure <id>` in the paper text must resolve to a row in at least one
   --ledger file (formula map, battery manifest, claim ledger, data
   findings). A numbered `(N)` counts as an equation tag only when its
   line — or one of the two lines above it — carries a math symbol
   (`= ≤ ≥ ≈ ≡ ∝ ∑ ∏ ∫ ∂ ∈`). A numbered `eq N` is covered by `eq N`,
   `eq. N`, `Eq. (N)`, `equation N`, or a range that contains it
   (`eqs. 3-5`, `(3)–(5)`); the bare `(N)` form counts only in
   formula-map ledgers, and prose mentions count as weak only in the
   eq/equation forms. A lettered tag is covered by the bare tag or an
   expanded `A.2-A.4` range. Prose mention alone fails every equation;
   tables and figures fail when absent and warn when prose-carried. An
   absent ref is an unaudited object — the canonical miss is a printed
   equation with no formula-map row.
2. DEPOSIT-ABSENCE CLAIMS. Every `unshipped`/`not in the deposit`/`source
   unshipped` phrase in --reports files must carry a `listing: <path>`
   pointer to a saved find/ls output under the job tree demonstrating absence
   across the source class. "Raw X unshipped" is a checkable claim; without
   the listing it is an unverified one.
3. DEPOSIT FILES. Every code file in the deposit inventory
   (review/deposit-inventory.json, or --deposit) must be named in at least
   one of: the --reports files, the ledger files, or a file under
   work/logs/ — a code file never named was never read or run. Unmentioned
   data files warn. A missing inventory FAILs unless `00_INTAKE.md` at
   the root records `Deposit: none` — no inventory, no deposit coverage.
4. NO SURFACE. No printed-surface source at all (no readable PDF text and
   no extracts) FAILs: an unenumerated surface is not a covered one.

Dispositions: coverage-na.csv at the job root (override with --na) carries
`ref,reason` rows; a `ref` equal to a coverage row's ref (`eq 3`, `eq A.9`,
`Table IV`, `Figure 2`, or a deposit file path) reports that row `n/a`
instead of failing it. A `ref` containing `*`/`?` or ending in `/` is a
pattern (fnmatch; a trailing `/` covers everything under that directory)
and clears matching deposit rows only. An empty reason is a FAIL; an n/a
row or pattern that matches no coverage row warns.

WARN rows (never block):

- `infeasible`/`not computable`/`deferred` phrases — the auditor adjudicates
  what evidence suffices; a data-absence claim wants a listing, a design
  fact wants its moments/stat.
- A printed `Table`/`Figure` ref carried by prose only — confirm a row
  exists.
- A deposit data file never named in the run's record.
- An extract set with no `01_`/`02_`-named (published) file warns that
  working papers inflate the surface.

--paper/--appendix: omitted, they auto-discover `01_*.pdf` / `02_*.pdf`
at the --root top level; given, each may be a glob pattern, expanded
relative to --root here (quote it — the shell need not expand it).

Usage:
  python3 check_coverage.py --root . \
      [--paper '01_*.pdf'] [--appendix '02_*.pdf'] \
      [--extracts review/extracts] \
      [--ledger analysis/code-and-data/formula-map.csv ...] \
      [--reports review analysis SYNTHESIS.md] \
      [--deposit review/deposit-inventory.json] [--na coverage-na.csv] \
      [--out coverage.csv]

With no --ledger the ledgers default to every `*.csv` under `analysis/`,
every `analysis/**/construction-ledger.md`, and `review/claims-REPORT.md`.
"""
import argparse
import csv
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EQ = re.compile(r"\(([A-Z]{1,2}\.\d+[a-z]?)\)")
EQ_NUM = re.compile(r"\((\d{1,3}[a-z]?)\)[.,;:]?[^\S\n]*$")
DISPLAY = re.compile(
    r"\b(?i:Table|Figure)\s+([IVXLC]+\b|[A-Za-z]{1,2}\.?\d+[A-Za-z]?\b|\d+[A-Za-z]?\b)"
)
DEFERRAL = re.compile(
    r"(unshipped|not\s+shipped|not\s+in\s+the\s+(deposit|package|packet)|"
    r"absent\s+from\s+the\s+(deposit|package|packet)|"
    r"no\s+source\s+(data|material)|source\s+unshipped)", re.I)
ADJUDICATE = re.compile(
    r"(infeasible|cannot\s+be\s+(re)?(computed|verified|checked)|"
    r"not\s+computable|deferred)", re.I)
LISTING = re.compile(r"(?:listing|checked|inventory)\s*[:=]\s*<?([^\s>)`,;]+)", re.I)

# ledger coverage tokens for a numbered equation ref
NUM_PAREN = re.compile(r"\(\s*(\d{1,3}[a-z]?)\s*\)")
NUM_TAG = re.compile(r"\b(?:eqs?|equations?)\.?\s*\(?\s*(\d{1,3}[a-z]?)\b", re.I)
NUM_RANGE = re.compile(
    r"\b(?:eqs?|equations?)\.?\s*\(?\s*(\d{1,3})\s*\)?\s*[-–—]\s*\(?\s*(\d{1,3})\b", re.I)
NUM_PAREN_RANGE = re.compile(
    r"\(\s*(\d{1,3})\s*\)\s*[-–—]\s*\(\s*(\d{1,3})\s*\)")

MATH_CHARS = set("=≤≥≈≡∝∑∏∫∂∈")

# deposit file classes (extensions, lower-case) — DATA_EXTS mirrors
# review/assets/deposit_inventory.py
CODE_EXTS = {"do", "ado", "r", "py", "m", "jl", "sas", "sps", "ipynb",
             "rmd", "qmd", "sh"}
DATA_EXTS = {"dta", "tab", "dat", "raw", "dbf", "mat", "csv", "tsv",
             "xlsx", "xls", "sav", "por", "rds", "rda", "feather",
             "parquet", "sqlite", "db", "sas7bdat", "xpt", "bin", "rdata",
             "h5", "hdf5"}


def expand_pdfs(root, spec, default_glob):
    """--paper/--appendix value -> [relative paths]. Empty: auto-discover
    `default_glob` at the root's top level. A glob is expanded under root;
    a literal path is returned as given (missing files are skipped later)."""
    pat = spec or default_glob
    if spec and not any(ch in spec for ch in "*?["):
        return [spec]
    return sorted(str(p.relative_to(root)) for p in root.glob(pat) if p.is_file())


INTAKE_NO_DEPOSIT = re.compile(r"^[\s>#*_+-]*deposit[\s*_]*:[\s*_]*none\b", re.I | re.M)


def intake_says_no_deposit(root):
    p = root / "00_INTAKE.md"
    return p.is_file() and bool(INTAKE_NO_DEPOSIT.search(p.read_text(errors="replace")))


def handoff_excluded(root):
    """Paths listed under `## excluded` in HANDOFF.md (`path | disposition | ...`)."""
    p = root / "HANDOFF.md"
    if not p.is_file():
        return set()
    sec = re.search(r"^##\s+excluded\b(.*?)(?=^##\s|\Z)",
                    p.read_text(errors="replace"), re.I | re.M | re.S)
    if not sec:
        return set()
    out = set()
    for line in sec.group(1).splitlines():
        s = re.sub(r"^\s*[-*+]\s*", "", line.strip())
        if "|" not in s:
            continue
        cell = s.split("|", 1)[0].strip().strip("`")
        if cell and cell.lower() != "path" and not set(cell) <= {"-", ":"}:
            out.add(cell.lstrip("./"))
    return out


def paper_text(root, pdfs):
    for rel in pdfs:
        p = root / rel
        if not p.is_file():
            continue
        try:
            out = subprocess.run(["pdftotext", "-q", str(p), "-"],
                                 capture_output=True, text=True, timeout=120)
            if out.stdout.strip():
                yield out.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired):
            yield ""


def extract_text(root, extdir):
    """All files under the extracts dir — prefer the published `01_*`/`02_*`
    dumps when they exist so working-paper extracts don't inflate the
    surface; returns (texts, used_published_only)."""
    d = root / extdir
    if not d.is_dir():
        return [], False
    files = [f for f in sorted(d.rglob("*")) if f.is_file()]
    published = [f for f in files if f.name.startswith(("01_", "02_"))]
    use = published or files
    return [f.read_text(errors="replace") for f in use], bool(published)


def norm(ref):
    return ref.replace(" ", "").rstrip(".")


def num_eq_tags(text, allow_bare_paren):
    """Numbered-equation tags a text covers: `eq`/`equation` forms and
    expanded ranges (`eqs. 3-5`, `(3)–(5)`) always; bare `(N)` tags only
    when allow_bare_paren — a stray "(3)" in a results table must not
    cover eq 3."""
    tags = set()
    if allow_bare_paren:
        tags.update(NUM_PAREN.findall(text))
    tags.update(m.group(1) for m in NUM_TAG.finditer(text))
    for pat in (NUM_RANGE, NUM_PAREN_RANGE):
        for m in pat.finditer(text):
            lo, hi = int(m.group(1)), int(m.group(2))
            if 0 <= hi - lo <= 200:
                tags.update(str(n) for n in range(lo, hi + 1))
    return tags


def default_ledgers(root):
    """Every *.csv under analysis/, every construction-ledger.md beneath it,
    and review/claims-REPORT.md when present — the three-stage ledger set."""
    specs = []
    adir = root / "analysis"
    if adir.is_dir():
        specs += sorted(str(p.relative_to(root)) for p in adir.rglob("*.csv"))
        specs += sorted(str(p.relative_to(root))
                        for p in adir.rglob("construction-ledger.md"))
    if (root / "review/claims-REPORT.md").is_file():
        specs.append("review/claims-REPORT.md")
    return specs


def load_na(root, rel):
    """coverage-na.csv -> {ref: reason}; rows with no ref are skipped."""
    p = root / rel
    if not p.is_file():
        return {}
    out = {}
    with p.open(newline="") as fh:
        for row in csv.DictReader(fh):
            ref = (row.get("ref") or "").strip()
            if ref:
                out[ref] = (row.get("reason") or "").strip()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--paper", default="")
    ap.add_argument("--appendix", default="")
    ap.add_argument("--extracts", default="review/extracts")
    ap.add_argument("--ledger", action="append", default=[])
    ap.add_argument("--reports", nargs="*", default=["review", "analysis", "SYNTHESIS.md"])
    ap.add_argument("--deposit", default="")
    ap.add_argument("--na", default="coverage-na.csv")
    ap.add_argument("--out", default="coverage.csv")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    fails, warns, rows = [], [], []
    excluded = handoff_excluded(root)

    def is_excluded(path):
        rel = str(path.relative_to(root))
        return rel in excluded or any(rel.startswith(e.rstrip("/") + "/") for e in excluded)

    # --- printed surface -----------------------------------------------------
    pdfs = expand_pdfs(root, a.paper, "01_*.pdf") + expand_pdfs(root, a.appendix, "02_*.pdf")
    texts = list(paper_text(root, pdfs)) if pdfs else []
    texts = [t for t in texts if t]
    if not texts:
        texts, published_only = extract_text(root, a.extracts)
        if texts and not published_only:
            warns.append("surface includes non-published extracts — no 01_/02_ dump; "
                         "working papers inflate the ref set")
    if not texts:
        fails.append("no printed-surface source (no readable PDF text, no extracts) — "
                     "the surface cannot be enumerated, so nothing is shown covered")
    surface = "\n".join(texts)

    # ref -> (kind, match token). Equations match on the bare tag ("A.9",
    # "3"); displays on the printed phrase ("Table III").
    refs = {}
    for m in EQ.finditer(surface):
        refs.setdefault("eq " + m.group(1), ("equation", m.group(1)))
    # a numbered tag is an equation number only in a math context — its line
    # or one of the two above must carry a math symbol, else "(600)" in a
    # table header would mint a ref
    surface_lines = surface.splitlines()
    for i, line in enumerate(surface_lines):
        m = EQ_NUM.search(line)
        if m and MATH_CHARS.intersection("\n".join(surface_lines[max(0, i - 2):i + 1])):
            refs.setdefault("eq " + m.group(1), ("equation", m.group(1)))
    for m in DISPLAY.finditer(surface):
        word = line_word = surface[m.start():m.end()].split()[0].title()
        ref = word + " " + m.group(1).upper()
        refs.setdefault(ref, ("display", ref))

    ledger_specs = a.ledger or default_ledgers(root)
    ledgers = []
    for lpath in ledger_specs:
        lp = root / lpath
        ledgers.append((lpath, lp.read_text(errors="replace") if lp.is_file() else ""))
        if not lp.is_file():
            warns.append(f"ledger '{lpath}' missing — refs it should carry will read open")
    ledger_blob = "\n".join(t for _, t in ledgers)
    report_files = []
    for rp in a.reports:
        p = root / rp
        if p.is_dir():
            report_files += [f for f in p.rglob("*.md") if not is_excluded(f)]
        elif p.is_file() and not is_excluded(p):
            report_files.append(p)
    report_blob = "\n".join(f.read_text(errors="replace") for f in report_files)

    # Covered ref sets per ledger: lettered raw tags plus expanded hyphen
    # ranges — "OA eq. A.2-A.4" covers A.2, A.3, A.4 — and the numbered-tag
    # set for `(N)` refs.
    ledger_tags = []
    for lp, t in ledgers:
        tags = set(re.findall(r"[A-Z]{1,2}\.\d+[a-z]?", t))
        for m in re.finditer(r"([A-Z]{1,2})\.(\d+)[a-z]?\s*[-–]\s*([A-Z]{1,2})\.(\d+)[a-z]?", t):
            if m.group(1) == m.group(3):
                for n in range(int(m.group(2)), int(m.group(4)) + 1):
                    tags.add(f"{m.group(1)}.{n}")
        ledger_tags.append((lp, t, tags, num_eq_tags(t, Path(lp).name.startswith("formula-map"))))
    report_num_eqs = num_eq_tags(report_blob, False)

    for ref in sorted(refs):
        kind, token = refs[ref]
        if kind == "equation" and token[0].isdigit():
            carriers = [lp for lp, t, tags, ntags in ledger_tags if token in ntags]
            weak = not carriers and token in report_num_eqs
        elif kind == "equation":
            carriers = [lp for lp, t, tags, ntags in ledger_tags if token in tags]
            weak = not carriers and norm(token) in norm(report_blob)
        else:
            ntok = norm(token).lower()
            carriers = [lp for lp, t in ledgers if ntok in norm(t).lower()]
            weak = not carriers and ntok in norm(report_blob).lower()
        status = "covered" if carriers else ("weak" if weak else "open")
        rows.append({"ref": ref, "kind": kind, "carrier": ";".join(carriers),
                     "status": status})

    # --- deposit coverage ------------------------------------------------------
    deposit = a.deposit
    if not deposit and (root / "review/deposit-inventory.json").is_file():
        deposit = "review/deposit-inventory.json"
    if not deposit and not intake_says_no_deposit(root):
        fails.append("review/deposit-inventory.json missing and 00_INTAKE.md does not "
                     "record 'Deposit: none' — run deposit_inventory.py or record the absence")
    if deposit:
        dp = root / deposit
        if not dp.is_file():
            fails.append(f"deposit inventory '{deposit}' missing — deposit coverage cannot run")
        else:
            logs_blob = "\n".join(
                f.read_text(errors="replace")
                for f in sorted((root / "work/logs").rglob("*"))
                if f.is_file()) if (root / "work/logs").is_dir() else ""
            try:
                inv = json.loads(dp.read_text(errors="replace"))
            except json.JSONDecodeError as e:
                warns.append(f"deposit inventory '{deposit}' unreadable ({e}) — deposit coverage skipped")
                inv = {}
            for frow in inv.get("files", []):
                ext = (frow.get("ext") or "").lower()
                if ext not in CODE_EXTS and ext not in DATA_EXTS:
                    continue
                path = frow.get("path", "")
                if ".ipynb_checkpoints/" in path:  # editor autosave copies
                    continue
                base = os.path.basename(path.split("::")[-1])
                where = []
                if base and base in report_blob:
                    where.append("reports")
                if base and base in ledger_blob:
                    where.append("ledger")
                if base and base in logs_blob:
                    where.append("logs")
                status = "covered" if where else "open"
                rows.append({"ref": path, "kind": "deposit",
                             "carrier": ";".join(where), "status": status,
                             "_class": "code" if ext in CODE_EXTS else "data"})

    # --- deferral evidence ----------------------------------------------------
    # deposit-absence claims need a saved listing (FAIL unless cleared in
    # coverage-na.csv); bare infeasibility claims are adjudicated by the
    # auditor (WARN — pass 3 owns the judgment).
    for f in sorted(set(report_files)):
        lines = f.read_text(errors="replace").splitlines()
        for ln, line in enumerate(lines, 1):
            if not (DEFERRAL.search(line) or ADJUDICATE.search(line)):
                continue
            win = "\n".join(lines[max(0, ln - 3):ln + 2])
            hit = LISTING.search(win)
            ok = False
            if hit:
                cand = hit.group(1).rstrip(".")
                tgt = (root / cand).resolve()
                ok = tgt.is_file() and root in tgt.parents
            if ok:
                continue
            rel = f.relative_to(root)
            frag = line.strip()[:80]
            if DEFERRAL.search(line):
                rows.append({"ref": f"{rel}:{ln}", "kind": "deferral",
                             "carrier": "", "status": "open", "_frag": frag})
            else:
                warns.append(f"{rel}:{ln}: infeasibility claim — adjudicate the evidence — '{frag}'")

    # --- dispositions ----------------------------------------------------------
    # a coverage-na.csv row whose ref equals a coverage row's ref clears that
    # row to n/a — with a recorded reason. A ref carrying `*`/`?` or ending in
    # `/` is a deposit-only pattern (fnmatch; trailing `/` = the directory's
    # whole subtree).
    na = load_na(root, a.na)
    matched = set()
    for ref, reason in na.items():
        if "*" in ref or "?" in ref or ref.endswith("/"):
            if ref.endswith("/") and "*" not in ref and "?" not in ref:
                hits = [r for r in rows
                        if r["kind"] == "deposit" and r["ref"].startswith(ref)]
            else:
                hits = [r for r in rows if r["kind"] == "deposit"
                        and fnmatch.fnmatch(r["ref"], ref)]
            for r in hits:
                r["status"] = "n/a"
            if not hits:
                warns.append(f"n/a pattern '{ref}' matches no coverage row")
            elif not reason:
                fails.append(f"'{ref}': n/a without reason")
            matched.add(ref)
    for row in rows:
        if row["ref"] in na and row["ref"] not in matched:
            matched.add(row["ref"])
            row["status"] = "n/a"
            if not na[row["ref"]]:
                fails.append(f"'{row['ref']}': n/a without reason")
    for ref in sorted(set(na) - matched):
        warns.append(f"n/a row '{ref}' matches no coverage row")

    for row in rows:
        ref, kind, status = row["ref"], row["kind"], row["status"]
        if status in ("covered", "n/a"):
            continue
        weak = status == "weak"
        if kind == "equation":
            # the formula map is a per-equation mandate — a prose mention is
            # not a row
            fails.append(f"printed ref '{ref}' has no formula-map row"
                         + (" (prose mention only)" if weak else ""))
        elif kind == "display":
            if weak:
                warns.append(f"printed ref '{ref}' carried by prose only — confirm a row exists")
            else:
                fails.append(f"printed ref '{ref}' has no row or mention — an unaudited object")
        elif kind == "deposit":
            if row.get("_class") == "code":
                fails.append(f"deposit file '{ref}' never read or run")
            else:
                warns.append(f"deposit data file '{ref}' never read or run — confirm it was audited")
        elif kind == "deferral":
            fails.append(f"{ref}: deposit-absence claim has no evidence listing — '{row.get('_frag', '')}'")

    out = Path(a.out)
    if not out.is_absolute():
        out = root / out
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ref", "kind", "carrier", "status"])
        w.writeheader()
        for row in rows:
            w.writerow({k: v for k, v in row.items() if not k.startswith("_")})
    for w_ in warns:
        print(f"WARN {w_}")
    for fl in fails:
        print(f"FAIL {fl}")
    print(f"{'FAIL' if fails else 'PASS'} — {len(fails)} fail(s), {len(warns)} warn(s), "
          f"{len(rows)} coverage rows -> {out}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
