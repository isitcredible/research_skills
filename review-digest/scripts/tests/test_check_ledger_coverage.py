"""check_ledger_coverage.py — FAIL_VOCAB stems, truth-ledger and legacy
severity rows, digit tokens, ignore list / skipped dirs, default severity
and departures, and the parking rule."""
import json

import pytest

from conftest import issue, ledger, run, write

import check_ledger_coverage as cc
import corpus_rules

ISS_TITLE = "Headline elasticity collapses under corrected clustering"
FINDING = "The headline elasticity collapses once clustering is corrected"
PHRASE = "headline elasticity collapses once clustering"


def synthesis(sev, text=FINDING):
    return f"# Synthesis\n\n## Findings\n\n| Finding | Severity |\n|---|---|\n| {text} | {sev} |\n"


def cov(tmp_path, files, *extra):
    write(tmp_path, files)
    return run("check_ledger_coverage.py", tmp_path / "ISSUES.md", "--no-manifest", *extra)


# ---- 1. FAIL_VOCAB stems ---------------------------------------------
@pytest.mark.parametrize("outcome", ["untested", "unverifiable as published"])
def test_untested_and_unverifiable_are_declared(tmp_path, outcome):
    write(tmp_path, {"analysis/claims/claim-ledger.csv":
                     f"claim,outcome\nThe elasticity is robust to clustering,{outcome}\n"})
    got, note = cc.findings_from_csv("claim-ledger.csv",
                                     tmp_path / "analysis/claims/claim-ledger.csv")
    assert note is None and len(got) == 1


def test_unverified_here_is_not_a_finding(tmp_path):
    write(tmp_path, {"c.csv": "claim,status\n"
                     "The elasticity is robust to clustering,unverified-here\n"
                     "The deflator matches the source series,unverifiable as published\n"})
    got, _ = cc.findings_from_csv("c.csv", tmp_path / "c.csv")
    assert [g["line"] for g in got] == [3]


# ---- 2. claim-ledger severity rows ------------------------------------
def test_claim_ledger_high_medium_rows_declared(tmp_path):
    write(tmp_path, {"c.csv":
        "claim,what the surviving evidence supports,strongest defence,gap direction,severity,status\n"
        "Elasticity of one,a much smaller elasticity survives,none tested,overstated,HIGH,settled\n"
        "Effect is causal,correlation only survives here,IV weak,overstated,MEDIUM,settled\n"
        "Sample is national,regional sample only covered,none,neutral,LOW,settled\n"})
    got, _ = cc.findings_from_csv("c.csv", tmp_path / "c.csv")
    assert [g["sev"] for g in got] == ["HIGH", "MEDIUM"]


def test_claim_ledger_high_row_reaches_worklist(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(),
        "analysis/claims/claim-ledger.csv":
            "claim,supports,severity,status\n"
            "The headline elasticity is one,a far smaller elasticity,HIGH,settled\n"})
    assert "1 declared" in out
    assert rc == 1


# ---- 3. digit tokens ----------------------------------------------------
def test_digit_tokens_kept():
    assert {"3", "2"} <= cc.toks("Table 3 col 2 coefficient")


def test_table_column_findings_do_not_dedupe(tmp_path):
    syn = ("# S\n\n| Finding | Severity |\n|---|---|\n"
           "| Table 3 col 2 coefficient sign flips under clustering | High |\n"
           "| Table 5 col 4 coefficient sign flips under clustering | High |\n")
    rc, out = cov(tmp_path, {"ISSUES.md": ledger(), "SYNTHESIS.md": syn})
    assert "2 obligations" in out


# ---- 4. ignore list and skipped directories ------------------------------
def test_apparatus_list_shared_and_extended():
    for n in ("00_INTAKE.md", "PROGRESS.md", "validation.md", "Validation.MD"):
        assert corpus_rules.is_apparatus(n)
    assert cc.is_apparatus is corpus_rules.is_apparatus


def test_intake_progress_and_skipped_dirs_not_undeclared(tmp_path):
    finding_md = "## Findings\n\n### F1. Something important is wrong here\nbody\n"
    write(tmp_path, {
        "ISSUES.md": ledger(),
        "HANDOFF.manifest.json": json.dumps({"inputs": {}, "excluded": {}}),
        "00_INTAKE.md": finding_md, "PROGRESS.md": finding_md,
        "VALIDATION.md": finding_md,
        "work/scratch-REPORT.md": finding_md,
        "lit/notes.md": finding_md,
        "04_replication_smith_2024/README-REPORT.md": finding_md,
    })
    rc, out = run("check_ledger_coverage.py", tmp_path / "ISSUES.md")
    assert "undeclared" not in out
    assert rc == 0, out


def test_report_outside_skipped_dirs_still_undeclared(tmp_path):
    write(tmp_path, {
        "ISSUES.md": ledger(),
        "HANDOFF.manifest.json": json.dumps({"inputs": {}, "excluded": {}}),
        "review/claims-REPORT.md":
            "## Findings\n\n### F1. Something important is wrong here\nbody\n"})
    rc, out = run("check_ledger_coverage.py", tmp_path / "ISSUES.md")
    assert "undeclared" in out and rc == 1


# ---- 5. truth ledger: defaults and departures ---------------------------------
def truth(holds, cent="headline", text=FINDING):
    return ("# Synthesis\n\n## Claim ledger\n\n"
            "| Claim (page) | Centrality | Holds | Kernel | Not established | Strongest defence | Status |\n"
            "|---|---|---|---|---|---|---|\n"
            f"| {text} (p. 4) | {cent} | {holds} | a smaller elasticity survives | the elasticity of one | none tested | settled |\n")


def test_truth_rows_that_hold_carry_no_obligation():
    lines = truth("holds").splitlines()
    assert cc.findings_from_table(lines, "SYNTHESIS.md", "S") == []
    got = cc.findings_from_table(truth("not established").splitlines(), "SYNTHESIS.md", "S")
    assert [(g["holds"], g["cent"], g["default"]) for g in got] == [
        ("not established", "headline", "high")]


@pytest.mark.parametrize("holds,cent,dflt", [
    ("not established", "headline", "high"), ("not established", "supporting", "high"),
    ("not established", "peripheral", "medium"), ("narrower", "headline", "medium"),
    ("narrower", "supporting", "medium"), ("narrower", "peripheral", "low"),
    ("holds", "headline", ""), ("not-established", "headline", "high"),
])
def test_default_table(holds, cent, dflt):
    assert cc.default_sev(cc.holds_key(holds), cc.cent_key(cent)) == dflt


@pytest.mark.parametrize("assigned,reason,ok", [
    ("High", "", True), ("Medium", "", False),
    ("Medium", "severity-reason: the kernel is the paper's whole contribution\n", True),
    ("Low", "", False),
])
def test_departure_needs_reason(tmp_path, assigned, reason, ok):
    iss = issue(1, ISS_TITLE, assigned, FINDING + ".")
    if reason:
        iss = iss.replace("category:", reason + "category:", 1)
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(iss),
        "SYNTHESIS.md": truth("not established"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n"})
    assert (rc == 0) == ok, out
    if not ok:
        assert "without a severity-reason" in out
    if reason:
        assert "DEPART" in out


def test_issue_takes_most_severe_mapped_default(tmp_path):
    second = "The headline elasticity loses significance at the design level"
    syn = truth("narrower") + (
        f"| {second} (p. 6) | supporting | not established | sign only | significance | none | settled |\n")
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "High", FINDING + ". " + second + ".")),
        "SYNTHESIS.md": syn,
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n"
                              "- `elasticity loses significance at the design level` → issue 1 (\"Headline elasticity\")\n"})
    assert rc == 0, out
    assert "issue 1 high = default" in out


def test_issue_without_truth_rows_defaults_low(tmp_path):
    files = {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "Medium", FINDING + ".")),
        "SYNTHESIS.md": synthesis("High"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1\n"}
    files["analysis/claims/claim-ledger.csv"] = (
        "claim_id,claim,centrality,holds,kernel,status\n"
        "CL09,The sample is national in scope throughout,peripheral,holds,the sample,settled\n"
        "CL10,An unrelated claim about trade flows here,peripheral,narrower,part,settled\n")
    files["ISSUES.coverage.md"] += "- `unrelated claim about trade flows` — excluded: test fixture\n"
    rc, out = cov(tmp_path, files)
    assert rc == 1 and "default low (no truth-ledger row mapped)" in out
    files["ISSUES.md"] = ledger(issue(1, ISS_TITLE, "Low", FINDING + "."))
    rc, out = cov(tmp_path, files)
    assert "issue 1 low = default (no truth-ledger row mapped)" in out, out


def test_legacy_corpus_severities_unchecked(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "High", FINDING + ".")),
        "SYNTHESIS.md": synthesis("High"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n"})
    assert rc == 0 and "severities are not checked" in out, out


def test_csv_truth_rows_not_doubled_when_synthesis_has_table(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "High", FINDING + ".")),
        "SYNTHESIS.md": truth("not established"),
        "analysis/claims/claim-ledger.csv":
            "claim_id,claim,centrality,holds,kernel,status\n"
            f"CL01,{FINDING},headline,not established,none,settled\n",
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n"})
    assert "truth rows read from SYNTHESIS.md" in out
    assert "1 obligations" in out, out


def test_truth_csv_rows(tmp_path):
    write(tmp_path, {"c.csv":
        "row_id,claim_verbatim,centrality,holds,kernel,status\n"
        "A1,The elasticity is one,headline,not established,none,settled\n"
        "A2,The effect is causal,supporting,narrower,a correlation,settled\n"
        "A3,The sample is national,peripheral,holds,the national sample,settled\n"})
    got, _ = cc.findings_from_csv("c.csv", tmp_path / "c.csv")
    assert [(g["holds"], g["default"]) for g in got] == [
        ("not established", "high"), ("narrower", "medium")]


# ---- 6. parking rule ------------------------------------------------------------
@pytest.mark.parametrize("ruling", ["→ caveats", "→ avenues", "— excluded: process note"])
def test_medium_finding_not_parked(tmp_path, ruling):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(assessment=FINDING + " remains a caveat."),
        "SYNTHESIS.md": synthesis("Medium"),
        "ISSUES.coverage.md": f"- `{PHRASE}` {ruling}\n"})
    assert "become issues" in out and rc == 1


def test_low_finding_may_go_to_caveats(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(assessment=FINDING + " remains a caveat."),
        "SYNTHESIS.md": synthesis("Low"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → caveats\n"})
    assert rc == 0, out


@pytest.mark.parametrize("cent,ok", [("headline", False), ("supporting", False),
                                     ("peripheral", True)])
def test_truth_row_parking_by_centrality(tmp_path, cent, ok):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(assessment=FINDING + " remains a caveat."),
        "SYNTHESIS.md": truth("narrower", cent),
        "ISSUES.coverage.md": f"- `{PHRASE}` → caveats\n"})
    assert (rc == 0) == ok, out


@pytest.mark.parametrize("n,ok", [(1, True), (9, False)])
def test_superseded_twin_exception(tmp_path, n, ok):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, "Some other issue entirely", "High", "Body text.")),
        "SYNTHESIS.md": synthesis("High"),
        "ISSUES.coverage.md": f"- `{PHRASE}` — excluded: superseded twin of issue {n}\n"})
    assert (rc == 0) == ok, out


def test_excluded_file_inside_accepted_dir_is_outside(tmp_path):
    acc = {"inputs": set(), "dirs": ("review",),
           "excluded": {"review/old-REPORT.md"}}
    assert cc.man_tag(acc, "review/old-REPORT.md") == "[outside]"
    assert cc.man_tag(acc, "review/new-REPORT.md") == "[accepted]"


def test_findings_from_table_resets_sev_col_between_tables():
    lines = [
        "| Finding | Severity |",
        "|---|---|",
        "| The first elasticity collapses under clustering | High |",
        "",
        "Some prose between tables.",
        "",
        "| Severity | Finding |",
        "|---|---|",
        "| Medium | The second elasticity collapses under weighting |",
    ]
    got = cc.findings_from_table(lines, "SYNTHESIS.md", "SYNTHESIS")
    assert [(g["sev"], g["text"]) for g in got] == [
        ("High", "The first elasticity collapses under clustering"),
        ("Medium", "The second elasticity collapses under weighting"),
    ]


def test_two_column_severity_table_in_block_not_duplicated():
    lines = [
        "## Findings",
        "### F1. Table of findings",
        "| Finding | Severity |",
        "|---|---|",
        "| The headline elasticity collapses under clustering | High |",
    ]
    assert cc.findings_from_blocks(lines, "SYNTHESIS.md", "SYNTHESIS") == []


def test_dedup_keeps_most_severe_default(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "Medium", FINDING + ".")),
        "01_code-REPORT.md": f"## Findings\n\n### F1. {FINDING}\nBody text.\n",
        "SYNTHESIS.md": truth("not established"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n",
    })
    assert rc == 1 and "default high" in out


def test_row_ruled_to_several_issues_sets_each_default(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "High", FINDING + "."),
                            issue(2, "Elasticity of one fails at design level", "Medium",
                                  FINDING + " again.")),
        "SYNTHESIS.md": truth("not established"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issues 1 (\"Headline elasticity\"), 2 (\"Elasticity of one\")\n"})
    assert "issue 1 high = default" in out
    assert "issue 2 medium (default high) — no severity-reason" in out and rc == 1


def test_skill_copy_and_bulk_not_walked():
    assert corpus_rules.skip_dir("_skill") and corpus_rules.skip_dir("_bulk")


def test_escaped_pipe_stays_inside_its_cell():
    """A claim cell joining two quotes with `\\|` keeps the truth row's
    columns aligned, so the row is still read as a truth row."""
    lines = ["| Claim | Centrality | Holds |", "|---|---|---|",
             r'| "first quoted claim here" \| "second quoted claim here" | headline | not established |']
    rows = cc.findings_from_table(lines, "SYNTHESIS.md", "S")
    assert len(rows) == 1
    assert rows[0]["holds"] == "not established"
    assert rows[0]["cent"] == "headline"
    assert '"first quoted claim here" | "second quoted claim here"' in rows[0]["text"]


def test_unbound_ruling_fails_in_truth_corpus(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "High", FINDING + ".")),
        "SYNTHESIS.md": truth("not established"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1\n"})
    assert rc == 1 and "names no issue title" in out


def test_stale_title_after_renumbering_fails(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, "A different issue now sits at rank one", "High",
                                  FINDING + ".")),
        "SYNTHESIS.md": truth("not established"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n"})
    assert rc == 1 and "names a title that issue no longer has" in out


def test_ambiguous_phrase_warns(tmp_path):
    syn = ("# S\n\n## Findings\n\n| Finding | Severity |\n|---|---|\n"
           "| The headline elasticity collapses once clustering is corrected for manufacturing wages by county | Low |\n"
           "| In services employment, the headline elasticity collapses once clustering is corrected at state level | Low |\n")
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(assessment=FINDING + " remains a caveat in tables three and five."),
        "SYNTHESIS.md": syn,
        "ISSUES.coverage.md": f"- `{PHRASE}` → caveats\n"})
    assert "AMBIGUOUS RULINGS" in out


def test_claims_report_truth_rows_ignored_when_synthesis_has_table(tmp_path):
    rc, out = cov(tmp_path, {
        "ISSUES.md": ledger(issue(1, ISS_TITLE, "High", FINDING + ".")),
        "SYNTHESIS.md": truth("not established"),
        "review/claims-REPORT.md": truth("narrower").replace("# Synthesis", "# Claims"),
        "ISSUES.coverage.md": f"- `{PHRASE}` → issue 1 (\"Headline elasticity\")\n"})
    assert rc == 0, out
    assert "1 obligations" in out


@pytest.mark.parametrize("errata,ok", [
    ("", False),
    ("### E1. Contested finding\nstatus: open\nfinding-bearing: yes\n"
     "class: audit — FOR-AUDIT-REVIEW\nThe review says the headline elasticity collapses once clustering is corrected; the print disagrees.\n", True),
    ("### E1. Contested finding\nstatus: closed\nfinding-bearing: yes\n"
     "FOR-AUDIT-REVIEW: the headline elasticity collapses once clustering is corrected\n", False),
])
def test_contested_needs_open_errata(tmp_path, errata, ok):
    files = {"ISSUES.md": ledger(),
             "SYNTHESIS.md": synthesis("High"),
             "ISSUES.coverage.md": f"- `{PHRASE}` — contested: FOR-AUDIT-REVIEW\n"}
    if errata:
        files["ERRATA.md"] = errata
    rc, out = cov(tmp_path, files)
    assert (rc == 0) == ok, out


@pytest.mark.parametrize("script", ["check_ledger_coverage.py", "check_facts.py",
                                    "check_fairness.py", "check_style.py",
                                    "build_manifest.py", "render_digest.py"])
def test_runs_under_isolated_mode(script):
    """`python -I` drops the script's folder from sys.path; every gate must
    still import its sibling modules."""
    import subprocess
    import sys
    from conftest import SCRIPTS
    p = subprocess.run([sys.executable, "-I", str(SCRIPTS / script), "--help"],
                       capture_output=True, text=True)
    assert "Traceback" not in p.stderr and "No module named" not in p.stderr, p.stderr
