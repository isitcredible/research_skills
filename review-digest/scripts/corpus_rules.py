"""Shared corpus rules for the digest gates — one definition, imported by
check_ledger_coverage.py and render_digest.py so the two never drift.

APPARATUS_FILES: internal instruments of the pipeline (lower-cased
basenames) — not evidence, never report-class, never need declaring; a
`not-evidence` exclusion of one (00_INTAKE.md, PROGRESS.md) is accepted
and changes nothing. SKILL.md step 6 lists the same set.
skip_dir(): directories never walked when enumerating report-class
files — scratch/computation trees, the untouched deposit, the
literature folder, and a copy of the skill tree a job carries
(`_skill/`) or its bulk scratch (`_bulk/`) hold no review findings.
errata_field(): the value of an ERRATA.md item field (`status:`,
`finding-bearing:`), read the same way by both gates.
"""
import re

APPARATUS_FILES = frozenset({
    "issues.md", "errata.md", "fairness.md", "changelog.md",
    "handoff.md", "handoff.manifest.json", "issues.keeps.md",
    "issues.facts.md", "issues.coverage.md", "readme.md",
    "agents.md", "claude.md", "style.md", "memory.md",
    "validation.md", "00_intake.md", "progress.md",
})

SKIP_DIRS = frozenset({"_versions", "bin", "tmp", "work", "lit", "_skill", "_bulk"})
SKIP_DIR_PREFIXES = ("04_replication_",)


def is_apparatus(name):
    return name.lower() in APPARATUS_FILES


def skip_dir(name):
    """True for a directory the report-class walk must not enter."""
    return (name.startswith(".") or name in SKIP_DIRS
            or name.startswith(SKIP_DIR_PREFIXES))


def errata_field(chunk, key):
    """Lower-cased value of `key:` in an ERRATA.md item, or None. The key
    is case-insensitive and may sit in a `- `/`* ` list item and in
    `**bold**` (`**status:** open`, `**status**: open`) — a field the
    gates cannot read must not pass as absent."""
    m = re.search(r"(?im)^\s*(?:[-*+]\s+)?[*_]{0,2}%s[*_]{0,2}\s*:"
                  r"[ \t*_]*([\w-]+)" % re.escape(key), chunk)
    return m.group(1).lower() if m else None
