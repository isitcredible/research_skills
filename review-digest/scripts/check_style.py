#!/usr/bin/env python3
"""Prose-register sweep for a review issue ledger (ISSUES.md).

The engine is canonical in the `ai-sweep` skill nested in this one, resolved
relative to this file so the packaged skills/ layout resolves the same
way. This shim preserves the ledger defaults: the ledger question
battery (style-questions.json, beside this file) and the internal-field
exemption list — severity/category/evidence/sources et al. render
nowhere and are exempt; `summary:` IS rendered and stays scanned.

A ledger-specific mechanical layer runs after the engine:
  1. the failures-only rule for reproduction/verification claims. A check
     that succeeded is the baseline, not a finding — no rendered sentence
     may report one ('the printed cell verifies exactly', 'the estimate is
     verified', 'no executed specification fails to reproduce'). Only a
     FAILED check is stated, as a fact about the deposit ('the funnel's
     intermediate stages could not be reproduced from the shipped code').
  2. no bare section locators or review-internal section references in
     rendered prose ('The §1 model', 'in §7.3', 'and §IV does not',
     '(version-diff §2.1)'). Name the substance in words first; a paper
     section locator may follow in parentheses ('the microcredit
     application (§7.3, p. 35)'), never stand in for the thing itself.

Each rendered line is split into clauses; a clause carrying a
verification lexeme (verif*, reproduc*, replicat* verb forms, recover*,
regenerat*) fails unless the clause negates it — and a universal
negative ('no specification fails to reproduce', 'no failures surfaced
in the reproduction') asserts success and flags anyway. Negated
failure mentions pass silently; borderline hits are ruled on the
judgment pass like any other flag.

Behaviour, flags, and exit codes are otherwise the generic engine's;
see the ai-sweep SKILL.md.
"""
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
HERE = os.path.dirname(os.path.realpath(__file__))
ENGINE_DIR = os.path.normpath(os.path.join(
    HERE, os.pardir, "ai-sweep", "scripts"))
ENGINE = os.path.join(ENGINE_DIR, "ai_sweep.py")
sys.path.insert(0, ENGINE_DIR)

from ai_sweep import internal_lines, load_keeps, kept_keep  # noqa: E402

SKIP_FIELDS = "severity-reason|severity|category|evidence|sources|paper|verdict|status|date"

# Reproduction/verification lexemes. Verb-only for 'replicat*' so the
# noun 'replication' (the package, the files) does not flag. Broad on
# purpose, same philosophy as the engine's stock tells: a false
# positive costs one keep on the read.
VERIF_LEX = re.compile(
    r"\b(?:verif\w*|reproduc\w*|replicat(?:e|es|ed|ing)|"
    r"recover\w*|regenerat\w*)\b", re.I)

# Clause boundaries for the polarity check — a negation in a different
# clause does not clear the lexeme ('is verified internally BUT not
# against source records' flags on its first clause).
CLAUSE_SPLIT = re.compile(r"[,;:—–()]|\bbut\b|\bhowever\b", re.I)

NEG = re.compile(
    r"\b(?:not|n't|never|cannot|can't|couldn'?t|could not|"
    r"without|fails? to|unable to|nowhere|no)\b", re.I)

# Universal negatives that assert success: 'no executed specification
# fails to reproduce' = every one succeeded; 'no failures surfaced' =
# all clean. A plain 'no X reproduces' is a FAILURE report and stays
# exempt — the fail-family term must follow the quantifier.
UNIV_NEG = re.compile(
    r"\b(?:no|none|nothing|not a single|not one)\b"
    r"[^.]{0,80}?\bfail\w*\b", re.I)

PAREN_SPAN = re.compile(r"\([^)]*\)")
BARE_SEC = re.compile(r"§+\s*[0-9IVXivxA-Za-z]")
INTERNAL_SEC = re.compile(
    r"\b(?:report|version-diff|research-design|spec-accuracy|"
    r"fragility-battery|check-story|data-audit|code-and-data|"
    r"synthesis|crib|stage\s+[1-6])\b[^.)\n]{0,30}§+\s*[0-9A-Za-z]",
    re.I)


def verif_flags(path):
    """(lineno, clause, normed line) verification-success candidates on
    rendered lines — frontmatter, internal fields, and fenced code never
    flag. One flag per line; the clause excerpt shows which segment hit,
    the normed line lets a recorded keep bind to the whole line."""
    skip_re = re.compile(r"^\s*(?:" + SKIP_FIELDS + r")\s*:", re.I)
    internal, lines = internal_lines(path, skip_re)
    flags = []
    fence = False
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if fence or i in internal or not stripped:
            continue
        for clause in CLAUSE_SPLIT.split(ln):
            if not VERIF_LEX.search(clause):
                continue
            if UNIV_NEG.search(clause) or not NEG.search(clause):
                flags.append((i, norm_excerpt(clause),
                              norm_line(ln)))
                break
    return flags


def sec_flags(path):
    """(lineno, reason, excerpt, normed line) for unparenthesized §
    locators ('the §3.6 simulation', 'in §7.3') or review-internal §
    references ('version-diff §2.1') on rendered lines."""
    skip_re = re.compile(r"^\s*(?:" + SKIP_FIELDS + r")\s*:", re.I)
    internal, lines = internal_lines(path, skip_re)
    flags = []
    fence = False
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if fence or i in internal or not stripped:
            continue
        m_int = INTERNAL_SEC.search(ln)
        if m_int:
            flags.append((i, "review-internal section reference — name "
                             "the substance; provenance belongs in sources:",
                          norm_excerpt(m_int.group(0)), norm_line(ln)))
            continue
        outside = PAREN_SPAN.sub(" ", ln)
        m_bare = BARE_SEC.search(outside)
        if m_bare:
            flags.append((i, "bare § locator in prose — name what the "
                             "section is in words first (a locator may "
                             "follow in parentheses)",
                          norm_excerpt(ln), norm_line(ln)))
    return flags


def norm_line(s):
    s = re.sub(r"[*_]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_excerpt(s):
    return norm_line(s)[:150]


TAKES_VALUE = {"--scan-dir", "--questions", "--skip-fields", "--plumb",
               "--threshold", "--watch", "--chunk-chars", "--overlap",
               "--timeout", "--retries"}


def main():
    argv = sys.argv[1:]
    warn_only = "--warn-only" in argv
    target, i = None, 0
    while i < len(argv) and target is None:
        if argv[i] in TAKES_VALUE:
            i += 2
            continue
        if not argv[i].startswith("-"):
            target = argv[i]
        i += 1
    rc = subprocess.call(
        [sys.executable, ENGINE,
         "--questions", os.path.join(HERE, "style-questions.json"),
         "--skip-fields", SKIP_FIELDS,
         "--no-plumbing"]
        + argv)
    flags = []
    if target:
        for lo, excerpt, full in verif_flags(target):
            flags.append((lo, "verification-success claim — reproduction "
                              "claims are failures-only", excerpt, full))
        flags.extend(sec_flags(target))
    if flags:
        keeps = load_keeps(target)
        standing = []
        for lo, reason, excerpt, full in flags:
            if kept_keep(full, keeps):
                continue
            standing.append((lo, reason, excerpt))
        flags = standing
    if flags:
        print("\n== LEDGER TELLS ==")
        for lo, reason, excerpt in flags:
            print(f"  FAIL  L{lo} {reason}")
            print(f"          {excerpt}")
        print("\nResolve in place: a check that succeeded is the "
              "baseline, never a finding — cut the claim, or restate "
              "the fact it checks ('236 is the printed first stage', "
              "not '236 verifies'). A clause reporting a FAILED check "
              "('could not be reproduced from the shipped code') "
              "passes; a universal negative ('no specification fails "
              "to reproduce') is a success claim and fails. A section "
              "of the paper must be named by its substance first ('the "
              "wage simulation (§3.6, p. 48)'), never as a bare § "
              "locator in running prose ('the §3.6 simulation', 'in "
              "§7.3'), and review-internal section references belong "
              "only in sources:. A keep is a ruling: record the kept "
              "wording in `backticks` with a one-line reason in "
              "<ledger-stem>.keeps.md beside the ledger — an unrecorded "
              "keep re-flags and fails.")
    sys.exit(0 if (warn_only or (rc == 0 and not flags)) else 1)


if __name__ == "__main__":
    main()
