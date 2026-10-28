"""render_digest.py — shared ignore list, import-error scanner route,
fresh-context output path, docstring layout."""
import hashlib
import json

import pytest

from conftest import write

import corpus_rules
import render_digest as rd

SHA = "ab" * 32


def test_apparatus_list_is_the_shared_one():
    assert rd.APPARATUS_FILES is corpus_rules.APPARATUS_FILES


def test_intake_progress_validation_not_undeclared(tmp_path):
    write(tmp_path, {"HANDOFF.md": "status: COMPLETE\n",
                     "00_INTAKE.md": "x", "PROGRESS.md": "x", "VALIDATION.md": "x",
                     "notes.md": "x"})
    sha = hashlib.sha256((tmp_path / "HANDOFF.md").read_bytes()).hexdigest()
    write(tmp_path, {"HANDOFF.manifest.json": json.dumps(
        {"handoff_sha256": sha, "status": "COMPLETE", "inputs": {}, "excluded": {}})})
    _, refusals = rd.finalize_checks(str(tmp_path / "ISSUES.md"), str(tmp_path), [],
                                     str(tmp_path / "HANDOFF.manifest.json"))
    undeclared = [r for r in refusals if "undeclared report-class" in r]
    assert undeclared == ["undeclared report-class file: notes.md — declare it an "
                          "input or an exclusion in HANDOFF.md"]


def _refusals(tmp_path, files, inputs=(), excluded=()):
    write(tmp_path, {"HANDOFF.md": "status: COMPLETE\n", **files})
    sha = hashlib.sha256((tmp_path / "HANDOFF.md").read_bytes()).hexdigest()
    man = {"handoff_sha256": sha, "status": "COMPLETE",
           "inputs": {p: {"sha256": rd.sha256_file(str(tmp_path / p))} for p in inputs},
           "excluded": {p: {"disposition": "superseded", "evidence": "x"} for p in excluded}}
    write(tmp_path, {"HANDOFF.manifest.json": json.dumps(man)})
    _, refusals = rd.finalize_checks(str(tmp_path / "ISSUES.md"), str(tmp_path), [],
                                     str(tmp_path / "HANDOFF.manifest.json"))
    return [r for r in refusals if "undeclared report-class" in r]


LAYOUT = {"SYNTHESIS.md": "s", "review/claims-REPORT.md": "c",
          "analysis/code-and-data/iv-REPORT.md": "m",
          "analysis/code-and-data/construction-ledger.md": "not report-class",
          "review/claims-BRIEF.md": "brief twin, not -REPORT",
          "work/scratch-REPORT.md": "skipped dir",
          "04_replication_smith_2024/notes-REPORT.md": "skipped dir",
          "lit/review-REPORT.md": "skipped dir"}


def test_undeclared_module_report_refuses(tmp_path):
    undeclared = _refusals(tmp_path, LAYOUT,
                           inputs=("SYNTHESIS.md", "review/claims-REPORT.md"))
    assert undeclared == ["undeclared report-class file: "
                          "analysis/code-and-data/iv-REPORT.md — declare it an "
                          "input or an exclusion in HANDOFF.md"]


def test_all_subtree_reports_undeclared_refuse(tmp_path):
    undeclared = _refusals(tmp_path, LAYOUT)
    assert len(undeclared) == 3
    for p in ("SYNTHESIS.md", "review/claims-REPORT.md",
              "analysis/code-and-data/iv-REPORT.md"):
        assert any(p in r for r in undeclared)


def test_declared_reports_pass(tmp_path):
    assert _refusals(tmp_path, LAYOUT,
                     inputs=("SYNTHESIS.md", "review/claims-REPORT.md"),
                     excluded=("analysis/code-and-data/iv-REPORT.md",)) == []
    assert _refusals(tmp_path, LAYOUT,
                     inputs=("SYNTHESIS.md", "review/claims-REPORT.md",
                             "analysis/code-and-data/iv-REPORT.md")) == []


# ---- fresh-context rulings must name an existing saved output ------------
@pytest.mark.parametrize("line,ok", [
    (f"gate: fresh-context — 2026-10-10 — sha256:{SHA[:12]} — work/fresh/out.md", True),
    (f"gate: fresh-context — 2026-10-10 — sha256:{SHA[:12]} — `work/fresh/out.md`", True),
    (f"gate: fresh-context — 2026-10-10 — sha256:{SHA[:12]} — work/fresh/missing.md", False),
    (f"gate: fresh-context — 2026-10-10 — sha256:{SHA[:12]}", False),
    (f"gate: operator — 2026-10-10 — sha256:{SHA[:12]}", True),
    (f"gate: in-context — 2026-10-10 — sha256:{SHA[:12]}", True),
    ("gate: operator — 2026-10-10 — sha256:ffffffffffff", False),
    (f"gate: operator — 2026-10-10 — sha256:{SHA[:1]}", False),
    (f"gate: operator — 2026-10-10 — sha256:{SHA[:11]}", False),
    (f"gate: operator — 2026-10-10 — sha256:{SHA[:13]}", False),
    (f"gate: operator — 2026-10-10 — sha256:{SHA}", False),
    (f"gate: manual pass — 2026-10-10 — sha256:{SHA[:4]}", False),
])
def test_gate_record(tmp_path, line, ok):
    write(tmp_path, {"work/fresh/out.md": "fresh-context worklist output\n",
                     "ISSUES.facts.md": line + "\n"})
    assert rd.gate_record(str(tmp_path / "ISSUES.facts.md"), SHA, rd.PASS_MODES) is ok


# ---- an absent prose engine takes the manual-pass route --------------------
def fake_gates(tmp_path, style_body, facts_body="import sys; sys.exit(0)"):
    d = tmp_path / "fakegates"
    write(d, {"check_facts.py": facts_body,
              "check_ledger_coverage.py": "import sys; sys.exit(0)",
              "check_fairness.py": "import sys; sys.exit(0)",
              "check_style.py": style_body})
    return d


MISSING_ENGINE = "import ai_sweep_absent_engine\n"


def run_gates_with(tmp_path, monkeypatch, gates_dir, rulings):
    review = tmp_path / "job"
    write(review, {"ISSUES.md": "ledger\n", **rulings})
    monkeypatch.setattr(rd, "HERE", str(gates_dir))
    sha = rd.sha256_file(str(review / "ISSUES.md"))
    refusals = []
    results = rd.run_gates(str(review / "ISSUES.md"), str(review), None, refusals)
    return results, refusals, sha


def test_import_error_with_manual_ruling_passes(tmp_path, monkeypatch):
    review_sha = hashlib.sha256(b"ledger\n").hexdigest()
    rulings = {f: f"gate: operator — 2026-10-10 — sha256:{review_sha[:12]}\n"
               for f in ("ISSUES.facts.md", "ISSUES.coverage.md")}
    rulings["ISSUES.keeps.md"] = f"gate: manual pass — 2026-10-10 — sha256:{review_sha[:12]}\n"
    results, refusals, _ = run_gates_with(
        tmp_path, monkeypatch, fake_gates(tmp_path, MISSING_ENGINE), rulings)
    assert results["style"] == "manual pass (recorded)"
    assert refusals == []


def test_import_error_without_ruling_refuses(tmp_path, monkeypatch):
    review_sha = hashlib.sha256(b"ledger\n").hexdigest()
    rulings = {f: f"gate: operator — 2026-10-10 — sha256:{review_sha[:12]}\n"
               for f in ("ISSUES.facts.md", "ISSUES.coverage.md")}
    _, refusals, _ = run_gates_with(
        tmp_path, monkeypatch, fake_gates(tmp_path, MISSING_ENGINE), rulings)
    assert any("style gate: scanner unavailable" in r for r in refusals)


NO_SCANNER = ("import sys; sys.exit('no passage scanner (PASSAGE_SCANNER unset "
              "or not executable) — the fairness sweep cannot scan')")


@pytest.mark.parametrize("recorded", [True, False])
def test_unset_passage_scanner_takes_manual_route(tmp_path, monkeypatch, recorded):
    review_sha = hashlib.sha256(b"ledger\n").hexdigest()
    rulings = {f: f"gate: operator — 2026-10-10 — sha256:{review_sha[:12]}\n"
               for f in ("ISSUES.facts.md", "ISSUES.coverage.md")}
    if recorded:
        rulings["FAIRNESS.md"] = f"gate: manual pass — 2026-10-10 — sha256:{review_sha[:12]}\n"
    gates = fake_gates(tmp_path, "import sys; sys.exit(0)")
    write(gates, {"check_fairness.py": NO_SCANNER})
    results, refusals, _ = run_gates_with(tmp_path, monkeypatch, gates, rulings)
    if recorded:
        assert results["fairness"] == "manual pass (recorded)" and refusals == []
    else:
        assert any("fairness gate: scanner unavailable" in r for r in refusals)


def test_import_error_in_other_gate_is_a_failure(tmp_path, monkeypatch):
    review_sha = hashlib.sha256(b"ledger\n").hexdigest()
    rulings = {"ISSUES.facts.md": f"gate: manual pass — x — sha256:{review_sha[:12]}\n",
               "ISSUES.coverage.md": f"gate: operator — x — sha256:{review_sha[:12]}\n"}
    _, refusals, _ = run_gates_with(
        tmp_path, monkeypatch,
        fake_gates(tmp_path, "import sys; sys.exit(0)", facts_body=MISSING_ENGINE),
        rulings)
    assert any("facts gate fails" in r for r in refusals)


def test_docstring_uses_current_layout():
    assert "sources: review/code-and-data-REPORT.md §R2b; work/logs/battery_run.log" in rd.__doc__


# ---- ERRATA fields: case, list bullets and bold all parse ------------------
@pytest.mark.parametrize("body,blocks", [
    ("status: open\n", True),
    ("Status: open\n", True),
    ("STATUS: Open\n", True),
    ("- status: open\n", True),
    ("* status: open\n", True),
    ("**status:** open\n", True),
    ("**status**: open\n", True),
    ("- **Status:** **open**\n", True),
    ("status: closed\n", False),
    ("status: open\nfinding-bearing: no\n", False),
    ("status: open\nFinding-bearing: No\n", False),
    ("status: open\n- finding-bearing: no\n", False),
    ("- **status:** open\n**finding-bearing:** no\n", False),
    ("status: open\nfinding-bearing: yes\n", True),
])
def test_errata_fields_parse_in_any_case_bullet_or_bold(tmp_path, body, blocks):
    write(tmp_path, {"ERRATA.md": "# Errata\n\n### E1. Slip in Table 2\n" + body})
    assert rd.parse_errata(str(tmp_path / "ERRATA.md")) == (
        ["E1. Slip in Table 2"] if blocks else [])


# ---- an issue may cite a file inside a declared directory primary ----------
def _source_refusals(tmp_path, cited, excluded=()):
    write(tmp_path, {"HANDOFF.md": "status: COMPLETE\n",
                     "04_replication_x/code/main.do": "reg y x",
                     "04_replication_x/code/old.do": "reg y z",
                     "04_replication_xyz/other.do": "x",
                     "loose.log": "x"})
    sha = hashlib.sha256((tmp_path / "HANDOFF.md").read_bytes()).hexdigest()
    lsha, n = rd.dir_listing_sha256(str(tmp_path / "04_replication_x"))
    man = {"handoff_sha256": sha, "status": "COMPLETE",
           "inputs": {"04_replication_x/": {"dir": True, "primary": True,
                                            "entries": n, "listing_sha256": lsha}},
           "excluded": {p: {"disposition": "superseded", "evidence": "x"}
                        for p in excluded}}
    write(tmp_path, {"HANDOFF.manifest.json": json.dumps(man)})
    issues = [{"rank": 1, "fields": {"sources": cited}}]
    assert rd.check_sources(issues, str(tmp_path)) == []
    _, refusals = rd.finalize_checks(str(tmp_path / "ISSUES.md"), str(tmp_path),
                                     issues, str(tmp_path / "HANDOFF.manifest.json"))
    return [r for r in refusals if "outside the accepted" in r]


def test_source_inside_directory_primary_accepted(tmp_path):
    assert _source_refusals(tmp_path, "04_replication_x/code/main.do §L4") == []


def test_cited_directory_primary_accepted(tmp_path):
    """A source may cite a declared directory input itself, slash and all."""
    assert _source_refusals(tmp_path, "04_replication_x/") == []


def test_cited_directory_without_slash_is_missing(tmp_path):
    write(tmp_path, {"04_replication_x/code/main.do": "reg y x"})
    issues = [{"rank": 1, "fields": {"sources": "04_replication_x"}}]
    assert len(rd.check_sources(issues, str(tmp_path))) == 1


@pytest.mark.parametrize("cited,excluded", [
    ("loose.log", ()),
    ("04_replication_xyz/other.do", ()),
    ("04_replication_x/code/old.do", ("04_replication_x/code/old.do",)),
])
def test_source_outside_directory_primary_refused(tmp_path, cited, excluded):
    assert len(_source_refusals(tmp_path, cited, excluded)) == 1


def test_template_comments_on_enum_fields_are_stripped(tmp_path):
    p = tmp_path / "ISSUES.md"
    p.write_text(
        "---\n"
        'paper: A 2020, "T" (J)\n'
        "verdict: Replication: OPEN · 0 HIGH / 1 MEDIUM / 0 LOW   # internal\n"
        "status: INTERIM   # copied from SYNTHESIS.md's status line\n"
        "---\n\n## Summary\nS.\n\n## Issues\n\n"
        "### 1. Title\n"
        "severity: Medium    # the upstream row's\n"
        "category: Reporting\n"
        "evidence: strong   # internal\n"
        "sources: SYNTHESIS.md\n\nBody.\n\n## Assessment\nA.\n",
        encoding="utf-8")
    parsed = rd.parse(str(p))
    meta, issues = parsed[0], parsed[1]
    assert meta["status"] == "INTERIM"
    f = issues[0]["fields"]
    assert f["severity"] == "Medium" and f["evidence"] == "strong"


def test_finalize_checks_handles_none_manifest_path(tmp_path):
    man, refusals = rd.finalize_checks(str(tmp_path / "ISSUES.md"), str(tmp_path), [], None)
    assert man is None and any("HANDOFF.manifest.json is missing" in r for r in refusals)


def test_finalize_checks_allows_interim_when_require_complete_false(tmp_path):
    write(tmp_path, {"HANDOFF.md": "status: INTERIM\n"})
    sha = hashlib.sha256((tmp_path / "HANDOFF.md").read_bytes()).hexdigest()
    write(tmp_path, {"HANDOFF.manifest.json": json.dumps(
        {"handoff_sha256": sha, "status": "INTERIM", "inputs": {}, "excluded": {}})})
    _, ref_final = rd.finalize_checks(
        str(tmp_path / "ISSUES.md"), str(tmp_path), [],
        str(tmp_path / "HANDOFF.manifest.json"), require_complete=True)
    _, ref_preview = rd.finalize_checks(
        str(tmp_path / "ISSUES.md"), str(tmp_path), [],
        str(tmp_path / "HANDOFF.manifest.json"), require_complete=False)
    assert any("not COMPLETE" in r for r in ref_final)
    assert ref_preview == []


def test_sec_flags_catches_bare_and_internal_section_refs(tmp_path):
    import check_style as cs
    p = tmp_path / "ISSUES.md"
    p.write_text(
        "---\npaper: A 2020\n---\n"
        "sources: review/paper-REPORT.md §P1\n"
        "The microcredit application (§7.3, p. 35) drops pooling.\n"
        "The §3.6 simulation flips sign.\n"
        "See the earlier check (version-diff §2.1).\n",
        encoding="utf-8")
    hits = cs.sec_flags(str(p))
    assert [h[0] for h in hits] == [6, 7]
    assert "bare § locator" in hits[0][1]
    assert "review-internal" in hits[1][1]




def test_severity_reason_is_a_field_not_body(tmp_path):
    p = tmp_path / "ISSUES.md"
    p.write_text(
        "---\n"
        'paper: A 2020, "T" (J)\n'
        "verdict: Replication: OPEN · 1 not established / 0 narrower / 3 hold\n"
        "status: COMPLETE\n"
        "---\n\n## Summary\nS.\n\n## Issues\n\n"
        "### 1. Title\n"
        "severity: Medium\n"
        "severity-reason: the kernel is the paper's whole contribution\n"
        "category: Reporting\n"
        "evidence: strong\n"
        "sources: SYNTHESIS.md\n\nBody.\n\n## Assessment\nA.\n",
        encoding="utf-8")
    parsed = rd.parse(str(p))
    iss = parsed[1][0]
    assert iss["fields"]["severity-reason"].startswith("the kernel")
    assert not any("severity-reason" in line for line in iss["body"])


def test_digest_with_no_issues_renders(tmp_path):
    from conftest import run
    p = tmp_path / "ISSUES.md"
    p.write_text(
        "---\n"
        'paper: A 2020, "T" (J)\n'
        "verdict: Replication: OPEN · 0 not established / 0 narrower / 5 hold\n"
        "status: COMPLETE\n"
        "---\n\n## Summary\nEvery claim holds as printed.\n\n## Issues\n\n"
        "## Assessment\nThe evidence supports the paper's claims.\n",
        encoding="utf-8")
    rc, out = run("render_digest.py", p)
    assert rc == 0 and "0 issues" in out, out


def test_missing_cited_source_refused_even_beside_a_twin(tmp_path):
    write(tmp_path, {"new/results.log": "x"})
    issues = [{"rank": 1, "fields": {"sources": "old/results.log"}}]
    assert rd.check_sources(issues, str(tmp_path)) != []


# ---- a worklist FAIL line (no "FAIL:" block) blocks the manual route -------
@pytest.mark.parametrize("tail,ok", [
    ("print('sweep clean')", True),
    ("print('  FAIL  L12 verification-success claim')", False),
    ("print('FAIL:'); print('  - L3 score=2.1')", False),
])
def test_style_fail_line_blocks_manual_pass(tmp_path, monkeypatch, tail, ok):
    review_sha = hashlib.sha256(b"ledger\n").hexdigest()
    rulings = {f: f"gate: operator — 2026-10-10 — sha256:{review_sha[:12]}\n"
               for f in ("ISSUES.facts.md", "ISSUES.coverage.md")}
    rulings["ISSUES.keeps.md"] = f"gate: manual pass — 2026-10-10 — sha256:{review_sha[:12]}\n"
    style = (f"import sys\n{tail.replace('; ', chr(10))}\n"
             "print('INCOMPLETE: the register layer never ran')\nsys.exit(1)\n")
    results, refusals, _ = run_gates_with(
        tmp_path, monkeypatch, fake_gates(tmp_path, style), rulings)
    if ok:
        assert results["style"] == "manual pass (recorded)" and refusals == []
    else:
        assert any("style gate fails" in r for r in refusals)


# ---- apparatus: SKILL.md and corpus_rules agree; declaring one is harmless --
def test_skill_apparatus_list_matches_corpus_rules():
    import re
    from conftest import SCRIPTS
    text = (SCRIPTS.parent / "SKILL.md").read_text()
    block = re.search(r"Apparatus — (.*?) — is never", text, re.S).group(1)
    names = {n.lower() for n in re.findall(r"`([^`]+)`", block)}
    assert names == set(corpus_rules.APPARATUS_FILES)


def test_apparatus_declared_not_evidence_is_accepted(tmp_path):
    write(tmp_path, {"HANDOFF.md": "status: COMPLETE\n", "00_INTAKE.md": "x",
                     "PROGRESS.md": "x", "CHANGELOG.md": "x"})
    sha = hashlib.sha256((tmp_path / "HANDOFF.md").read_bytes()).hexdigest()
    excl = {n: {"disposition": "not-evidence"} for n in ("00_INTAKE.md", "PROGRESS.md")}
    write(tmp_path, {"HANDOFF.manifest.json": json.dumps(
        {"handoff_sha256": sha, "status": "COMPLETE", "inputs": {}, "excluded": excl})})
    _, refusals = rd.finalize_checks(str(tmp_path / "ISSUES.md"), str(tmp_path), [],
                                     str(tmp_path / "HANDOFF.manifest.json"))
    assert refusals == []


def test_provenance_line_under_title_in_html_and_markdown(tmp_path):
    from conftest import run
    p = tmp_path / "ISSUES.md"
    p.write_text(
        "---\n"
        'paper: A 2020, "T" (J)\n'
        "verdict: Replication: OPEN · 0 not established / 0 narrower / 5 hold\n"
        "status: COMPLETE\n"
        "---\n\n## Summary\nEvery claim holds as printed.\n\n## Issues\n\n"
        "## Assessment\nThe evidence supports the paper's claims.\n",
        encoding="utf-8")
    rc, out = run("render_digest.py", p)
    assert rc == 0, out
    html = (tmp_path / "DIGEST.html").read_text(encoding="utf-8")
    title = html.index("<h1>")
    assert html.index(rd.PROVENANCE) > title
    assert html.index(rd.PROVENANCE) < html.index("<h2>Summary</h2>")
    assert json.dumps(f"*{rd.PROVENANCE}*")[1:-1] in html
