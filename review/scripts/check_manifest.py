#!/usr/bin/env python3
"""check_manifest.py — assert the battery manifest's claims are checkable facts.

Run from the job root (the review folder) before COMPLETE is reported, and by
audit-review's gate walk. A manifest row's `state` is a claim this script can
check; prose scope is not coverage.

Checks (FAIL = exit 1):

0. Schema. The manifest has at least one data row; carries the columns
   `id, family, hypothesis, spec, artifact, seed, state, validity,
   row_role`; every row fills `id, family, hypothesis, spec, state,
   validity, row_role` (`artifact`/`seed` may read `NA` for unrun or
   deterministic checks, never blank); and `state` ∈ {done, NONREPRODUCED,
   PROXY, BLOCKED, NOT_RUN, NOT_APPLICABLE}, `validity` ∈ {clean,
   unvalidated, invalid}, `row_role` ∈ {verdict-bearing, rebuttal}.
   Legacy aliases (state `executed`/`not_computable`/`queued`, columns
   `check_id`/`status`) are accepted with a WARN. results.csv must exist.
1. Every row in an artifact-bearing state (`done`, `NONREPRODUCED`, `PROXY`)
   names an `artifact` that resolves to an existing, non-empty file under
   the job tree — `NA` is no artifact. A missing `seed` column WARNs (legacy
   manifests); a blank seed in a present column FAILs.
2. Every artifact-bearing row has a `results.csv` row — matched by artifact
   path or by manifest ID → results `spec_id`.
3. Consumer coverage is bidirectional. Forward: every consumer enumerated on
   a shared-object construction-ledger item (a `consumers: F1, F2` line under
   the item's heading, bare or as a `-`/`*`/`+` list item, indented or not) maps to a manifest row carrying `ledger_item: <item>`
   and `consumer: <family>` — or an explicit NOT_RUN/BLOCKED row on
   that consumer. Reverse: every manifest row's `ledger_item` resolves to a
   ledger item whose `consumers:` set contains that row's `consumer` — an
   item with no `consumers:` line FAILs every row referencing it, so a shared
   object cannot opt out of coverage by leaving the field empty.
4. Variant rows (`variant_of` non-empty) carry `patch:` (the diff against the
   shipped builder) and `moments:` (the self-describing sidecar), both
   resolving to real files.
8. Module walk (`analysis/code-and-data/module-walk.md`) exists. Every module
   it marks fired has a non-empty report: a backticked `.md` path on its row
   that resolves, or `analysis/code-and-data/<module>-REPORT.md`. Every
   module ruled not applicable has its stub. A fired module whose report is
   a not-applicable stub (a line `Status: NOT_APPLICABLE — <reason>`) FAILs.
   A missing report is unfinished work, never an open item.
9. Robustness-claims ledger (`analysis/paper/robustness-claims.csv`) exists,
   and every row carries a `classification` (SUPPORTED / QUALIFIED /
   CONTRADICTED / UNRESOLVED) and its `evidence`. A completed scan that
   found no robustness sentence is one row classified NONE_FOUND, its
   `evidence` naming the search stems; NONE_FOUND beside other rows FAILs.
   A header-only file WARNs: it cannot tell an empty scan from a skipped
   one. Legacy `review_assessment` is accepted with a WARN, but a blank one
   still FAILs. A robustness claim with no assessment is unfinished work,
   never an open item.
10. Assumption ledger (`analysis/code-and-data/assumption-ledger.csv`).
   Required when the module walk fires `whimsical-assumptions-diagnostics`;
   checked whenever it exists. Every row fills `id, assumption, kind,
   grounding, conclusions, effect, warrant, ruling`; `kind`, `effect`,
   `warrant` and `ruling` are in their enums; any effect but UNTESTED names
   one or more `artifact` paths (`;`-separated) that all exist; every warrant but UNANCHORED names a
   `warrant_source`; a WHIMSICAL row has a critical effect (SIGN_FLIP,
   MATERIAL, BUILT_IN, NO_COUNTERPART) and an unwarranted grade (CONTESTED,
   CONTRADICTED, UNANCHORED, CONVENIENCE); a FRAGILE row has effect
   THRESHOLD and an unwarranted grade; a DISCARDED or CONSUMED row says
   "routed to: …" in its note.

Checks (WARN = printed, no exit change — judgment, not mechanism):

5. Same-`estimand_id` rows in results.csv whose estimates disagree beyond
   3·max(SE) — an in-run consensus flag: two artifacts claiming one estimand
   cannot both be the corrected quantity.
6. Variant moments divergence — where a moments file is JSON carrying
   outcome_mean/outcome_sd under "baseline" and "variant" keys, a variant
   outcome mean >10× baseline (or |Δmean| > 10·SD_baseline) flags the row:
   a large move can be the finding, but it must be explained, never passed
   through silently.
7. `unvalidated` rows with no `patch`/`moments` pointer — nothing for a
   validator to check.

Usage (from anywhere — paths resolve under --root):
    python3 check_manifest.py [--root <job root>] [--manifest PATH]
        [--results PATH] [--ledger PATH]
Defaults: --root ., manifest analysis/code-and-data/battery-manifest.csv,
results analysis/code-and-data/results.csv, ledger
analysis/code-and-data/construction-ledger.md. When a default path does not
exist under --root but the same filename does under analysis/fragility/
(the six-stage layout, v0.4 and earlier), the legacy file is used and a NOTE is printed.
Exit 0 = clean or warnings only; 1 = FAILs present.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

DONE = {"done", "executed", "nonreproduced", "proxy"}   # artifact-bearing states
OPEN = {"not_run", "not_computable", "blocked", "queued"}  # resolved-open states

# Canonical enums (code-and-data SKILL.md, Manifest). Matched
# case-insensitively; legacy aliases pass with a WARN.
STATES = ("done", "NONREPRODUCED", "PROXY", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE")
STATE_ALIASES = {"executed": "done", "not_computable": "BLOCKED", "queued": "NOT_RUN"}
VALIDITY = ("clean", "unvalidated", "invalid")
ROW_ROLES = ("verdict-bearing", "rebuttal")
REQUIRED_COLS = ("id", "family", "hypothesis", "spec", "artifact", "seed",
                 "state", "validity", "row_role")
NONEMPTY_COLS = ("id", "family", "hypothesis", "spec", "state", "validity", "row_role")
COL_ALIASES = {"id": "check_id", "state": "status"}   # legacy column names
NA = "na"   # explicit not-applicable token for artifact/seed


def load_csv(path):
    if not path.exists():
        return None, [], f"missing {path}"
    with path.open(newline="") as fh:
        rd = csv.DictReader(fh)
        rows = list(rd)
        cols = [c.strip() for c in (rd.fieldnames or [])]
    return rows, cols, None


def enum_check(rid, col, val, canon, aliases, fails, warns):
    """FAIL a value outside the canonical enum; WARN on an accepted alias
    or a non-canonical spelling of a canonical value."""
    low = {c.lower(): c for c in canon}
    if val.lower() in low:
        if val != low[val.lower()]:
            warns.append(f"{rid}: {col}='{val}' — canonical spelling is '{low[val.lower()]}'")
        return
    if val.lower() in aliases:
        warns.append(f"{rid}: {col}='{val}' is a legacy alias — write '{aliases[val.lower()]}'")
        return
    fails.append(f"{rid}: {col}='{val}' not in {{{', '.join(canon)}}}")


def schema_check(cols, mrows, fails, warns):
    """Check 0 — required columns, non-empty fields, enums."""
    have = set(cols)
    for c in REQUIRED_COLS:
        if c in have:
            continue
        alias = COL_ALIASES.get(c)
        if alias and alias in have:
            warns.append(f"manifest column '{alias}' is a legacy alias — rename it '{c}'")
        elif c == "seed":
            warns.append("manifest has no 'seed' column — add it (NA for deterministic checks)")
        else:
            fails.append(f"manifest missing required column '{c}'")
    for i, row in enumerate(mrows, 2):
        rid = field(row, "id", "check_id") or f"row {i}"
        for c in NONEMPTY_COLS:
            if not field(row, c, COL_ALIASES.get(c, c)):
                fails.append(f"{rid}: required field '{c}' is empty")
        for c in ("artifact", "seed"):
            if c in have and not field(row, c):
                fails.append(f"{rid}: '{c}' is blank — write NA if none applies")
        st = field(row, "state", "status")
        if st:
            enum_check(rid, "state", st, STATES, STATE_ALIASES, fails, warns)
        for c, canon in (("validity", VALIDITY), ("row_role", ROW_ROLES)):
            v = field(row, c)
            if v:
                enum_check(rid, c, v, canon, {}, fails, warns)


def field(row, *names):
    for n in names:
        v = row.get(n)
        if v:
            return v.strip()
    return ""


def paths(row, *names):
    """A path field may carry several ';'-joined files — check each. An
    explicit `NA` names no file."""
    return [p.strip() for p in field(row, *names).split(";")
            if p.strip() and p.strip().lower() != NA]


def ledger_consumers(path):
    """Parse `consumers:` declarations out of construction-ledger.md.

    An item is a `##`/`- item:`/`L<n>`-headed block; a `consumers:` line under
    it lists the result-family/check ids the shared object feeds. Returns
    [(item_id, consumer_ids)] where consumer_ids is None when the item
    declares no `consumers:` line — an unenumerated dependency.
    """
    out = []
    if not path.exists():
        return out
    item = None
    seen = {}
    order = []
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"^(#{1,4}\s+|-\s*item:\s*)(\S+)", line.strip(), re.I)
        if m:
            item = m.group(2).rstrip(":")
            if item not in seen:
                seen[item] = None
                order.append(item)
            continue
        # bare, indented, or as a `-`/`*`/`+` list item
        m = re.match(r"^(?:[-*+]\s+)?consumers\s*:\s*(.+)$", line.strip(), re.I)
        if m and item:
            cs = [c.strip() for c in re.split(r"[,\s]+", m.group(1)) if c.strip()]
            if cs and cs[0].lower() in ("none", "n/a"):
                cs = []
            seen[item] = (seen[item] or []) + cs
    return [(i, seen[i]) for i in order]


def moments_flag(path):
    try:
        data = json.loads(path.read_text())
        b, v = data["baseline"], data["variant"]
        mb, mv = float(b["outcome_mean"]), float(v["outcome_mean"])
        sd = float(b["outcome_sd"])
        if abs(mb) > 0 and abs(mv / mb) > 10:
            return f"variant outcome mean {mv:g} is {abs(mv/mb):.0f}× baseline {mb:g}"
        if sd > 0 and abs(mv - mb) > 10 * sd:
            return f"variant outcome mean moved {abs(mv-mb)/sd:.0f} SD from baseline"
    except Exception:
        return None
    return None


DEFAULTS = {
    "manifest": "analysis/code-and-data/battery-manifest.csv",
    "results": "analysis/code-and-data/results.csv",
    "ledger": "analysis/code-and-data/construction-ledger.md",
}
LEGACY_DIR = "analysis/fragility"
MODULE_WALK = "analysis/code-and-data/module-walk.md"
ROBUSTNESS = "analysis/paper/robustness-claims.csv"
NA_STUB = re.compile(r"^[ \t>#*_`]*Status[*_`]*[ \t]*:[ \t*_`]*NOT_APPLICABLE[*_`]*[ \t]*[—–:-]+[ \t]*\w", re.M)


def module_walk_check(root, fails):
    """Check 8: fired modules have reports; not-applicable modules have stubs."""
    walk = root / MODULE_WALK
    if not walk.is_file():
        fails.append(f"{MODULE_WALK} missing — the module-dispatch walk is a required artifact")
        return set()
    seen = 0
    fired_mods = set()
    for line in walk.read_text(errors="replace").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        mods = [m.lower() for c in cells for m in re.findall(r"\b([a-z][a-z-]*-diagnostics)\b", c, re.I)]
        if not mods:
            continue
        mod = mods[0]
        flags = [re.sub(r"[*_`]", "", c).strip().lower() for c in cells]
        if any(f in ("no", "not fired", "not applicable", "na", "n/a") for f in flags):
            fired = False
        elif any(f in ("yes", "gap") or ("fire" in f and not f.startswith("not")) for f in flags):
            fired = True          # "fired", "should fire", "gap": all owe a report
        else:
            continue
        seen += 1
        if fired:
            fired_mods.add(mod)
        listed = [x for c in cells for x in re.findall(r"`([^`]+\.md)`", c)]
        cands = listed + [f"analysis/code-and-data/{mod}-REPORT.md",
                          f"analysis/code-and-data/{mod.replace('-diagnostics', '')}-REPORT.md"]
        found = [root / c for c in cands if (root / c).is_file() and (root / c).stat().st_size > 0]
        ok = bool(found)
        if fired and any(NA_STUB.search(f.read_text(errors="replace")) for f in found):
            fails.append(f"module {mod}: fired but its report is a not-applicable stub — run the module")
        if not ok:
            kind = "report" if fired else "not-applicable stub"
            fails.append(f"module {mod}: {'fired' if fired else 'not fired'} but no {kind} found "
                         f"({', '.join(listed) or 'no path on its walk row'})")
    if not seen:
        fails.append(f"{MODULE_WALK}: no module rows with a fired/not-fired value")
    return fired_mods


def robustness_check(root, fails, warns):
    """Check 9: every robustness claim is classified, with evidence (paper SKILL.md)."""
    path = root / ROBUSTNESS
    if not path.is_file():
        fails.append(f"{ROBUSTNESS} missing — the paper stage's robustness-claims ledger is required")
        return
    rows, cols, err = load_csv(path)
    if err:
        fails.append(err); return
    canon = ("SUPPORTED", "QUALIFIED", "CONTRADICTED", "UNRESOLVED")
    if "classification" in cols:
        ccol, ecol = "classification", "evidence"
    elif "review_assessment" in cols:
        warns.append(f"{ROBUSTNESS}: legacy column review_assessment — the spec's columns are "
                     "claim, page, cited_exhibit, outcomes_covered, classification, evidence")
        ccol, ecol = "review_assessment", None
    else:
        fails.append(f"{ROBUSTNESS}: no classification column"); return
    if not rows:
        warns.append(f"{ROBUSTNESS}: header only — a completed scan with no robustness sentence "
                     "is one NONE_FOUND row whose evidence names the search stems")
        return
    blank, bad, noev = [], [], []
    nf = [r for r in rows if ccol == "classification"
          and (r.get(ccol) or "").strip().upper().split()[:1] == ["NONE_FOUND"]]
    if nf and len(rows) > 1:
        fails.append(f"{ROBUSTNESS}: NONE_FOUND beside {len(rows) - 1} other row(s) — an empty scan is the only row")
    for i, r in enumerate(rows, 2):
        rid = field(r, "claim_id") or f"row {i}"
        v = (r.get(ccol) or "").strip()
        if not v:
            blank.append(rid); continue
        if ccol == "classification" and v.split()[0].strip(":;,.").upper() not in canon + ("NONE_FOUND",):
            bad.append(f"{rid}={v[:20]}")
        if ecol and ecol in cols and not (r.get(ecol) or "").strip():
            noev.append(rid)
    def lst(x): return f"{', '.join(x[:12])}{' …' if len(x) > 12 else ''}"
    if blank:
        fails.append(f"{ROBUSTNESS}: {len(blank)} of {len(rows)} robustness claims unassessed ({lst(blank)})")
    if bad:
        fails.append(f"{ROBUSTNESS}: classification outside {'/'.join(canon)} ({lst(bad)})")
    if noev:
        fails.append(f"{ROBUSTNESS}: {len(noev)} classified claims carry no evidence ({lst(noev)})")


ASSUMPTIONS = "analysis/code-and-data/assumption-ledger.csv"
WHIMSY = "whimsical-assumptions-diagnostics"
A_COLS = ("id", "assumption", "kind", "grounding", "conclusions", "relaxation",
          "artifact", "effect", "warrant", "warrant_source", "ruling", "note")
A_NONEMPTY = ("id", "assumption", "kind", "grounding", "conclusions", "effect",
              "warrant", "ruling")
A_KINDS = ("stated", "structural", "closure", "exclusion", "bridge")
A_EFFECTS = ("SIGN_FLIP", "MATERIAL", "IMMATERIAL", "BUILT_IN", "NO_COUNTERPART", "THRESHOLD", "UNTESTED")
A_WARRANTS = ("SUPPORTED", "CONTESTED", "CONTRADICTED", "UNANCHORED", "CONVENIENCE")
A_RULINGS = ("WHIMSICAL", "FRAGILE", "CRITICAL_WARRANTED", "INERT", "DISCARDED", "CONSUMED", "UNRESOLVED")


def assumption_check(root, fired_mods, fails, warns):
    """Check 10: the whimsical-assumptions ledger's rows are checkable facts."""
    path = root / ASSUMPTIONS
    if not path.is_file():
        if WHIMSY in fired_mods:
            fails.append(f"{ASSUMPTIONS} missing — {WHIMSY} fired, so its ledger is required")
        return
    rows, cols, _ = load_csv(path)
    missing = [c for c in A_COLS if c not in cols]
    if missing:
        fails.append(f"{ASSUMPTIONS}: missing column(s) {', '.join(missing)}")
        return
    if not rows:
        fails.append(f"{ASSUMPTIONS}: header but no rows — an empty inventory is not coverage")
        return
    for i, r in enumerate(rows, 2):
        rid = f"{ASSUMPTIONS} {field(r, 'id') or f'line {i}'}"
        empty = [c for c in A_NONEMPTY if not field(r, c)]
        if empty:
            fails.append(f"{rid}: empty {', '.join(empty)}")
            continue
        for col, canon in (("kind", A_KINDS), ("effect", A_EFFECTS),
                           ("warrant", A_WARRANTS), ("ruling", A_RULINGS)):
            enum_check(rid, col, field(r, col), canon, {}, fails, warns)
        eff, war, rul = (field(r, c).upper() for c in ("effect", "warrant", "ruling"))
        if eff != "UNTESTED":
            art = field(r, "artifact")
            arts = [x.strip() for x in art.split(";") if x.strip()]
            bad = [x for x in arts if x.lower() == NA or not (root / x).is_file()]
            if not arts or bad:
                fails.append(f"{rid}: effect {eff} needs artifact path(s) that exist, "
                             f"';'-separated (bad: '{'; '.join(bad) or 'blank'}') — "
                             f"a relaxation is a construction")
        if war != "UNANCHORED" and not field(r, "warrant_source"):
            fails.append(f"{rid}: warrant {war} needs a warrant_source")
        if rul == "WHIMSICAL":
            if eff not in ("SIGN_FLIP", "MATERIAL", "BUILT_IN", "NO_COUNTERPART"):
                fails.append(f"{rid}: WHIMSICAL with effect {eff} — not shown critical")
            if war not in ("CONTESTED", "CONTRADICTED", "UNANCHORED", "CONVENIENCE"):
                fails.append(f"{rid}: WHIMSICAL with warrant {war} — not shown unwarranted")
        if rul == "FRAGILE":
            if eff != "THRESHOLD":
                fails.append(f"{rid}: FRAGILE with effect {eff} — FRAGILE reports a THRESHOLD")
            if war not in ("CONTESTED", "CONTRADICTED", "UNANCHORED", "CONVENIENCE"):
                fails.append(f"{rid}: FRAGILE with warrant {war} — not shown unwarranted")
        if rul in ("DISCARDED", "CONSUMED") and "routed to" not in field(r, "note").lower():
            fails.append(f"{rid}: {rul} without 'routed to: …' in note — name where it went")


def resolve_layout(root, rel, default):
    """Three-stage path (v0.5 on); fall back to the legacy analysis/fragility/ twin when only
    that exists (and the caller did not pass an explicit path)."""
    if rel != default or (root / rel).exists():
        return rel, False
    legacy = str(Path(LEGACY_DIR) / Path(rel).name)
    if (root / legacy).exists():
        return legacy, True
    return rel, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--manifest", default=DEFAULTS["manifest"])
    ap.add_argument("--results", default=DEFAULTS["results"])
    ap.add_argument("--ledger", default=DEFAULTS["ledger"])
    a = ap.parse_args()
    root = Path(a.root).resolve()
    fails, warns = [], []

    legacy = False
    for opt in ("manifest", "results", "ledger"):
        rel, fell = resolve_layout(root, getattr(a, opt), DEFAULTS[opt])
        setattr(a, opt, rel)
        legacy = legacy or fell
    if legacy:
        print(f"NOTE legacy layout: {LEGACY_DIR}/")

    mrows, mcols, err = load_csv(root / a.manifest)
    if err:
        print(f"FAIL {err}"); return 1
    if not mrows:
        print(f"FAIL {a.manifest}: header but no data rows — an empty battery is not coverage")
        return 1
    rrows, _, err = load_csv(root / a.results)
    if err:
        fails.append(f"{err} — every artifact-bearing row needs a results.csv row")
        rrows = []
    schema_check(mcols, mrows, fails, warns)

    res_artifacts = {field(r, "artifact") for r in rrows if field(r, "artifact")}
    res_specs = {field(r, "spec_id") for r in rrows if field(r, "spec_id")}

    for i, row in enumerate(mrows, 2):
        rid = field(row, "id", "check_id") or f"row {i}"
        state = field(row, "state", "status").lower()
        art = ";".join(paths(row, "artifact"))   # NA ⇒ no artifact

        # 1 — done-class ⇒ real artifact(s)
        if state in DONE:
            if not art:
                fails.append(f"{rid}: state={state} with no artifact")
            else:
                for ap_ in paths(row, "artifact"):
                    p = (root / ap_).resolve()
                    if not p.is_file() or p.stat().st_size == 0:
                        fails.append(f"{rid}: artifact '{ap_}' missing or empty")
        # 2 — artifact ⇒ results row (any of the joined paths counts)
        if art and not set(paths(row, "artifact")) & res_artifacts and rid not in res_specs:
            fails.append(f"{rid}: artifact '{art}' has no results.csv row")
        # 4 — variant rows ⇒ patch + moments (each ';'-joined file real when done)
        if field(row, "variant_of") and state in DONE:
            for col in ("patch", "moments"):
                pvals = paths(row, col)
                if not pvals:
                    fails.append(f"{rid}: variant of {row['variant_of']} has no {col}:")
                for v in pvals:
                    if not (root / v).resolve().is_file():
                        fails.append(f"{rid}: {col} '{v}' missing")
            for mp in paths(row, "moments"):
                mpf = (root / mp).resolve()
                if mpf.is_file():
                    flag = moments_flag(mpf)
                    if flag:
                        warns.append(f"{rid}: {flag} — explain or quarantine the row")
        # 7 — unvalidated with nothing to validate
        if field(row, "validity") == "unvalidated" and not (field(row, "patch") or field(row, "moments")):
            warns.append(f"{rid}: validity=unvalidated with no patch/moments — nothing to validate")

    # 3 — consumer coverage, both directions: declared consumers must have
    # rows, and rows' ledger_items must sit inside the declared consumers.
    declared = dict(ledger_consumers(root / a.ledger))
    for item, consumers in declared.items():
        covered = {field(r, "consumer", "family") for r in mrows
                   if field(r, "ledger_item") == item}
        for c in consumers or []:
            if c not in covered:
                fails.append(f"ledger {item}: consumer '{c}' has no manifest row")
    for i, row in enumerate(mrows, 2):
        li = field(row, "ledger_item")
        if not li:
            continue
        rid = field(row, "id", "check_id") or f"row {i}"
        if li not in declared or declared[li] is None:
            fails.append(f"{rid}: ledger_item '{li}' has no consumers: line — declare the set or 'none'")
        else:
            cons = field(row, "consumer", "family")
            if cons not in declared[li]:
                fails.append(f"{rid}: consumer '{cons or '∅'}' not in ledger {li} consumers: {declared[li]}")

    # 5 — same-estimand disagreement (within-run consensus)
    groups = {}
    for r in rrows:
        eid = field(r, "estimand_id")
        try:
            est, se = float(field(r, "estimate")), float(field(r, "std_error"))
        except ValueError:
            continue
        if eid:
            groups.setdefault(eid, []).append((est, se, field(r, "spec_id")))
    for eid, rows in groups.items():
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                (e1, s1, id1), (e2, s2, id2) = rows[i], rows[j]
                lim = 3 * max(s1, s2)
                if lim > 0 and abs(e1 - e2) > lim:
                    warns.append(f"estimand {eid}: {id1}={e1:g} vs {id2}={e2:g} "
                                 f"differ by {abs(e1-e2):.3g} (>3·max SE) — one may be a defective variant")

    # 8, 9 — module reports and robustness assessments are completeness, not open items
    fired_mods = module_walk_check(root, fails)
    robustness_check(root, fails, warns)
    assumption_check(root, fired_mods, fails, warns)  # 10

    for w in warns:
        print(f"WARN {w}")
    for f in fails:
        print(f"FAIL {f}")
    print(f"{'FAIL' if fails else 'PASS'} — {len(fails)} fail(s), {len(warns)} warn(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
