"""check_facts.py — quotes resolve only in primary sources; elided
quotes need a recorded disposition."""
import json

import pytest

from conftest import issue, ledger, run, write

QUOTE = "the policy had no effect on enrolment"


def facts(tmp_path, body, files):
    write(tmp_path, {"ISSUES.md": ledger(issue(1, "Quote check", "High", body)), **files})
    return run("check_facts.py", tmp_path / "ISSUES.md", "--no-manifest")


def test_quote_in_primary_extract_resolves(tmp_path):
    rc, out = facts(tmp_path, f'The paper says "{QUOTE}".',
                    {"review/extracts/01_paper.txt": f"We find {QUOTE} at all.\n"})
    assert rc == 0, out


@pytest.mark.parametrize("prose", [
    "review/claims-REPORT.md", "SYNTHESIS.md", "ISSUES.facts.md", "FAIRNESS.md",
    "ERRATA.md", "CHANGELOG.md", "HANDOFF.md", "analysis/claims/notes.md",
    "analysis/code-and-data/iv-REPORT.md",
])
def test_quote_only_in_review_prose_fails(tmp_path, prose):
    rc, out = facts(tmp_path, f'The paper says "{QUOTE}".',
                    {prose: f"The paper says {QUOTE}.\n"})
    assert "not found verbatim" in out and rc == 1


def test_numbers_still_resolve_in_review_prose(tmp_path):
    rc, out = facts(tmp_path, "The corrected estimate is 0.437.",
                    {"review/code-and-data-REPORT.md": "corrected estimate 0.437\n"})
    assert rc == 0, out


SOURCE = "The policy had, in the first year, no effect on enrolment at all.\n"


@pytest.mark.parametrize("mark", ["…", "...", "[...]", "[…]"])
def test_elided_quote_needs_disposition(tmp_path, mark):
    q = f"The policy had {mark} no effect on enrolment"
    files = {"review/extracts/01_paper.txt": SOURCE}
    rc, out = facts(tmp_path, f'They write "{q}".', files)
    assert "== ELIDED ==" in out and "has no disposition" in out and rc == 1
    files["ISSUES.facts.md"] = (f"- elided: \"{q[:30]}\" — dropped clause is a "
                                "time qualifier only; no negation removed\n")
    rc, out = facts(tmp_path, f'They write "{q}".', files)
    assert rc == 0, out


def test_elision_fragments_must_still_be_verbatim(tmp_path):
    q = "The policy had … a large effect on enrolment"
    rc, out = facts(tmp_path, f'They write "{q}".',
                    {"review/extracts/01_paper.txt": SOURCE,
                     "ISSUES.facts.md": f"- \"{q[:30]}\" ok\n"})
    assert "missing fragment" in out and rc == 1


def manifest(inputs):
    return json.dumps({"inputs": {p: ({"dir": True} if p.endswith("/") else {"sha256": "x"})
                                  for p in inputs}, "excluded": {}})


@pytest.mark.parametrize("extract,inputs,ok", [
    ("01_paper.txt", ["01_paper_x.pdf"], True),          # leading NN_ match
    ("01_paper_x.txt", ["01_paper_x.pdf"], True),        # equal stem
    ("01_paper_x_p1-20.txt", ["01_paper_x.pdf"], True),  # prefix
    ("03_draft.txt", ["01_paper_x.pdf"], False),         # another document
    ("03_draft.txt", ["01_paper_x.pdf", "review/extracts/02_app.txt"], True),
    ("03_draft.txt", ["review/extracts/"], True),
])
def test_pdf_primary_accepts_its_extract(tmp_path, extract, inputs, ok):
    write(tmp_path, {"HANDOFF.manifest.json": manifest(inputs),
                     f"review/extracts/{extract}": f"We find {QUOTE} at all.\n",
                     "review/extracts/02_app.txt": "appendix\n"})
    write(tmp_path, {"ISSUES.md": ledger(issue(1, "Quote", "High", f'It says "{QUOTE}".'))})
    rc, out = run("check_facts.py", tmp_path / "ISSUES.md")
    assert (rc == 0) == ok, out
    if not ok:
        assert "only outside the accepted input set" in out


@pytest.mark.parametrize("name", ["04_replication_x/main.do", "04_replication_x/clean.R",
                                  "04_replication_x/build.sql", "04_replication_x/est.sas"])
def test_deposit_code_quotable(tmp_path, name):
    rc, out = facts(tmp_path, 'The code reads "keep if year >= 1990".',
                    {name: 'keep if year >= 1990 & region != "South"\n'})
    assert rc == 0, out


def test_zero_width_and_linebreak_hyphen(tmp_path):
    zw_quote = "the policy had no ef\u200bfect on enrol\ufeffment"
    rc, out = facts(tmp_path, f'The paper says "{zw_quote}".',
                    {"review/extracts/01_paper.txt":
                     "We find the policy had no effect on enrol-\nment at all.\n"})
    assert rc == 0, out


def test_derived_number_ruled_in_facts_md_passes(tmp_path):
    body = "The coefficient falls from 0.50 to 0.20, a drop of 0.30."
    files = {"review/claims-REPORT.md": "falls from 0.50 to 0.20\n"}
    rc, out = facts(tmp_path, body, files)
    assert rc == 1 and "value 0.30 not found in corpus" in out
    files["ISSUES.facts.md"] = "- `falls from 0.50 to 0.20, a drop of 0.30` — derived difference 0.50 - 0.20 = 0.30\n"
    rc, out = facts(tmp_path, body, files)
    assert rc == 0, out


def test_excluded_file_inside_accepted_dir_not_accepted(tmp_path):
    man = json.dumps({
        "inputs": {"review/": {"dir": True}},
        "excluded": {"review/extracts/01_paper.txt": {"disposition": "superseded"}},
    })
    write(tmp_path, {
        "HANDOFF.manifest.json": man,
        "review/extracts/01_paper.txt": f"We find {QUOTE} at all.\n",
        "ISSUES.md": ledger(issue(1, "Quote", "High", f'It says "{QUOTE}".')),
    })
    rc, out = run("check_facts.py", tmp_path / "ISSUES.md")
    assert rc == 1 and "only outside the accepted input set" in out



def test_quotes_never_resolve_in_challenge_reports_progress_or_skill_copy(tmp_path):
    from conftest import ledger, issue, run, write
    q = "the silver window carries every magnitude in the paper"
    write(tmp_path, {
        "ISSUES.md": ledger(issue(1, "Title of the issue here", "High",
                                  f'The paper says "{q}".')),
        "review/challenge-REPORT-C.md": q + "\n",
        "PROGRESS.md": q + "\n",
        "_skill/review/SKILL.md": q + "\n",
    })
    rc, out = run("check_facts.py", tmp_path / "ISSUES.md", "--no-manifest")
    assert rc == 1 and "not found verbatim" in out


# ---- precision upgrades, the digest's own outputs, References -------------
@pytest.mark.parametrize("ledger_val,corpus,ok", [
    ("3.00", "3 hold", False),         # corpus has less precision: upgrade
    ("3.10", "rate 3.1 here", False),
    ("3.0", "rate 3.04 here", True),    # corpus has more precision: fine
    ("15", "rate 15.4 here", True),
    ("3.00", "rate 3.00 here", True),
    ("0.12345678", "p 0.1234567812", True),   # >6 decimals, corpus finer
    ("0.12000000", "p 0.12", False),          # >6 decimals, upgrade
])
def test_precision_upgrade_fails(tmp_path, ledger_val, corpus, ok):
    rc, out = facts(tmp_path, f"The value is {ledger_val} overall.",
                    {"review/claims-REPORT.md": corpus + "\n"})
    assert (rc == 0) == ok, out
    if not ok and "." in ledger_val and len(ledger_val) < 8:
        assert "upgrades precision" in out


def test_digest_outputs_never_join_the_corpus(tmp_path):
    body = f'The estimate is 0.437, and the paper says "{QUOTE}".'
    files = {"work/digest/facts.r1.txt": f"L12 The estimate is 0.437 {QUOTE}\n"}
    rc, out = facts(tmp_path, body, files)
    assert rc == 1 and "value 0.437 not found" in out and "not found verbatim" in out
    files["work/logs/est.log"] = "estimate 0.437\n"
    files["review/extracts/01_paper.txt"] = f"We find {QUOTE} at all.\n"
    rc, out = facts(tmp_path, body, files)
    assert rc == 0, out


def test_references_numbers_not_swept_but_quotes_checked(tmp_path):
    refs = "\n## References\nJones, A. (2019) 'A paper', Journal, 82(1), pp. 39–67.\n"
    write(tmp_path, {"ISSUES.md": ledger(issue(1, "Refs", "High", "Body text.")) + refs})
    rc, out = run("check_facts.py", tmp_path / "ISSUES.md", "--no-manifest")
    assert rc == 0, out
    write(tmp_path, {"ISSUES.md": ledger(issue(1, "Refs", "High", "Body text."))
                     + refs.replace("'A paper'", '"A paper never printed"')})
    rc, out = run("check_facts.py", tmp_path / "ISSUES.md", "--no-manifest")
    assert rc == 1 and "not found verbatim" in out
