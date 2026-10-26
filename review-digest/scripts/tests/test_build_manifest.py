"""build_manifest.py — commented/list-marker status lines, and the
docstring template passes its own parser."""
import json
import re
import textwrap

import pytest

from conftest import run, write

import build_manifest as bm

BODY = ("\n## inputs\n- SYNTHESIS.md\n\n## primaries\n- 01_paper.pdf\n"
        "\n## excluded\n\n## conflicts\n- none\n")


@pytest.mark.parametrize("head", [
    "status: COMPLETE            # COMPLETE | INTERIM | BLOCKED\n",
    "- status: COMPLETE  # list-marker form\n",
    "status: COMPLETE\n",
])
def test_status_comment_and_list_marker(tmp_path, head):
    write(tmp_path, {"HANDOFF.md": "# HANDOFF\n" + head + "audit: 2026-10-03   # anchor\n" + BODY,
                     "SYNTHESIS.md": "s", "01_paper.pdf": b"%PDF"})
    rc, out = run("build_manifest.py", tmp_path / "HANDOFF.md")
    assert rc == 0, out
    man = json.loads((tmp_path / "HANDOFF.manifest.json").read_text())
    assert man["status"] == "COMPLETE" and man["audit"] == "2026-10-03"


def test_bad_status_still_fails(tmp_path):
    write(tmp_path, {"HANDOFF.md": "status: DONE  # nope\n" + BODY,
                     "SYNTHESIS.md": "s", "01_paper.pdf": b"%PDF"})
    rc, out = run("build_manifest.py", tmp_path / "HANDOFF.md")
    assert rc == 1 and "status must be one of" in out


def test_docstring_template_passes_its_parser(tmp_path):
    doc = bm.__doc__
    start = doc.index("  # HANDOFF")
    end = doc.index("Header fields")
    template = textwrap.dedent(doc[start:end]).strip() + "\n"
    assert "review/code-and-data-REPORT.md" in template
    write(tmp_path, {"HANDOFF.md": template})
    _, _, inputs, primaries, excluded, _ = bm.parse_handoff(str(tmp_path / "HANDOFF.md"))
    for p in inputs + primaries + [e["path"] for e in excluded]:
        p = re.split(r"\s+#|§", p)[0].strip()
        if p.endswith("/"):
            (tmp_path / p / "x.do").parent.mkdir(parents=True, exist_ok=True)
            (tmp_path / p / "x.do").write_text("x")
        else:
            write(tmp_path, {p: "x"})
    rc, out = run("build_manifest.py", tmp_path / "HANDOFF.md")
    assert rc == 0, out


def _handoff(tmp_path, excluded="", ledger=None):
    files = {"HANDOFF.md": "status: COMPLETE\n\n## inputs\n- SYNTHESIS.md\n"
                           "\n## primaries\n- 01_paper.pdf\n"
                           f"\n## excluded\n{excluded}\n## conflicts\n- none\n",
             "SYNTHESIS.md": "s", "01_paper.pdf": b"%PDF"}
    if ledger is not None:
        files["analysis/claims/claim-ledger.csv"] = ledger
    write(tmp_path, files)
    return run("build_manifest.py", tmp_path / "HANDOFF.md")


def test_excluded_none_accepted(tmp_path):
    rc, out = _handoff(tmp_path, excluded="- none\n")
    assert rc == 0, out
    assert json.loads((tmp_path / "HANDOFF.manifest.json").read_text())["excluded"] == {}


@pytest.mark.parametrize("status,ok", [("settled", True), ("INTERIM", False),
                                       ("interim", False)])
def test_interim_claims_block_complete(tmp_path, status, ok):
    rc, out = _handoff(tmp_path, ledger=f"claim,severity,status\nc1,HIGH,settled\n"
                                        f"c2,MEDIUM,{status}\n")
    assert (rc == 0) == ok, out
    if not ok:
        assert "INTERIM claim(s) at row(s) 3" in out


def test_interim_allowed_when_status_interim(tmp_path):
    write(tmp_path, {"analysis/claims/claim-ledger.csv": "claim,status\nc1,INTERIM\n"})
    rc, out = _handoff(tmp_path, ledger="claim,status\nc1,INTERIM\n")
    assert rc == 1   # COMPLETE handoff
    (tmp_path / "HANDOFF.md").write_text(
        (tmp_path / "HANDOFF.md").read_text().replace("COMPLETE", "INTERIM"))
    rc, out = run("build_manifest.py", tmp_path / "HANDOFF.md")
    assert rc == 0, out


def test_claim_ledger_without_status_column_warns(tmp_path):
    rc, out = _handoff(tmp_path, ledger="claim,severity\nc1,HIGH\n")
    assert rc == 0 and "WARN" in out and "no status column" in out


# ---- an excluded stage/module report must be superseded by a declared input --
def _report_handoff(tmp_path, entry):
    write(tmp_path, {
        "HANDOFF.md": "status: INTERIM\n\n## inputs\n- SYNTHESIS.md\n"
                      "- review/claims-REPORT.md\n\n## primaries\n- 01_paper.pdf\n"
                      f"\n## excluded\n{entry}\n\n## conflicts\n- none\n",
        "SYNTHESIS.md": "s", "01_paper.pdf": b"%PDF", "review/claims-REPORT.md": "c",
        "review/old-claims-REPORT.md": "o", "notes/rebuilt.md": "r",
        "work/snap/claims-REPORT.md": "snapshot"})
    return run("build_manifest.py", tmp_path / "HANDOFF.md")


@pytest.mark.parametrize("entry,ok", [
    ("- review/old-claims-REPORT.md | superseded | rebuilt as review/claims-REPORT.md", True),
    ("- review/old-claims-REPORT.md | superseded | rebuilt as `review/claims-REPORT.md`.", True),
    ("- review/old-claims-REPORT.md | superseded | rebuilt as\n  review/claims-REPORT.md (C4)", True),
    ("- review/old-claims-REPORT.md | superseded | rebuilt as claims-REPORT.md", False),
    ("- review/old-claims-REPORT.md | superseded | replaced by the rebuilt claims report", False),
    ("- review/old-claims-REPORT.md | superseded | replaced by notes/rebuilt.md", False),
    ("- review/old-claims-REPORT.md | not-evidence | module not fired (stub)", False),
    ("- review/old-claims-REPORT.md | withdrawn | wrong sample", False),
    ("- work/snap/claims-REPORT.md | not-evidence | pre-edit snapshot", True),
    ("- notes/rebuilt.md | exploratory | working notes", True),
])
def test_excluded_report_needs_declared_replacement(tmp_path, entry, ok):
    rc, out = _report_handoff(tmp_path, entry)
    assert (rc == 0) == ok, out
    if not ok:
        assert "review/old-claims-REPORT.md" in out
