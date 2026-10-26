"""check_fairness.py — sentence-scoped keeps (residual re-score) and
evidence locators, and scanner resolution. A fake passage scanner scores a
text 3.0 when it carries attribution language ('to inflate' /
'deliberately'), else 0.0."""
import os
import sys

import pytest

from conftest import ledger, issue, run, write

import check_fairness as cf
import render_digest as rd

FAKE_SCANNER = r'''#!/usr/bin/env python3
import hashlib, json, os, re, sys
src = sys.argv[2]
out = sys.argv[sys.argv.index("--output") + 1]
text = open(src, encoding="utf-8").read()
n = text.count("\n") + 1
score = 3.0 if re.search(r"to inflate|deliberately", text, re.I) else 0.0
os.makedirs(os.path.join(out, "judgments"), exist_ok=True)
sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
json.dump({"passages": [{"passage_id": "p1", "line_start": 1, "line_end": n,
                         "text": text, "source_sha256": sha}]},
          open(os.path.join(out, "manifest.json"), "w"))
json.dump({"passage_id": "p1", "line_start": 1, "line_end": n,
           "response": {"answers": {
               "attribution_strength": {"score": score, "probabilities": {}, "confidence": 0.9},
               "intent_disclaimer": {"noul": 0.1}}}},
          open(os.path.join(out, "judgments", "p1.json"), "w"))
json.dump({"complete": True}, open(os.path.join(out, "summary.json"), "w"))
'''

KEPT = "the authors chose the cutoff to inflate the estimate"
BODY_ONE = ("They dropped the 1990 wave. The authors chose the cutoff to inflate "
            "the estimate, as their referee reply states. The sample is small.")
BODY_TWO = BODY_ONE + " They deliberately omitted the controls."


@pytest.fixture
def env(tmp_path):
    scanner = tmp_path / "fakescanner"
    scanner.write_text(FAKE_SCANNER)
    scanner.chmod(0o755)
    e = dict(os.environ, PASSAGE_SCANNER=str(scanner))
    return e


def fair(tmp_path, env, body, evidence):
    write(tmp_path, {
        "ISSUES.md": ledger(issue(1, "Cutoff choice moves the estimate", "High", body)),
        "corr/referee_reply.txt": "line one\nwe set the cutoff to raise power\nline three\n",
        "FAIRNESS.md": f"- `{KEPT}` — evidence: {evidence}\n"})
    return run("check_fairness.py", tmp_path / "ISSUES.md", env=env)


def test_keep_clears_only_its_sentence(tmp_path, env):
    rc, out = fair(tmp_path, env, BODY_TWO, "corr/referee_reply.txt:2")
    assert "clears only its own sentence" in out
    assert "residual 3.00" in out
    assert rc == 1


def test_keep_clears_passage_when_rest_is_clean(tmp_path, env):
    rc, out = fair(tmp_path, env, BODY_ONE, "corr/referee_reply.txt:2")
    assert "re-scored 0.00" in out
    assert rc == 0, out


@pytest.mark.parametrize("evidence,ok", [
    ("corr/referee_reply.txt:2", True),
    ("corr/referee_reply.txt:1-3", True),
    ("corr/referee_reply.txt §2", True),
    ("`corr/referee_reply.txt:2`", True),
    ("corr/referee_reply.txt", False),          # no locator
    ("corr/referee_reply.txt:9", False),        # line past EOF
    ("corr/referee_reply.txt:3-1", False),      # inverted range
    ("corr/missing.txt:2", False),              # no such file
])
def test_evidence_locator(tmp_path, env, evidence, ok):
    rc, out = fair(tmp_path, env, BODY_ONE, evidence)
    assert (rc == 0) == ok, out


def test_residual_text_drops_only_kept_sentences():
    r = cf.residual_text(cf.norm(BODY_TWO), {KEPT})
    assert "inflate" not in r and "deliberately omitted" in r and "1990 wave" in r


# ---- the scanner is PASSAGE_SCANNER and nothing else ----------------------
def _no_scanner_env(tmp_path):
    """No PASSAGE_SCANNER, but a working scanner reachable by routes the
    gate must never consult: a `scanner` on PATH, ~/.local/bin/scanner, and
    a SCANNER variable."""
    for d in ("pathbin", "home/.local/bin"):
        b = tmp_path / d / "scanner"
        b.parent.mkdir(parents=True, exist_ok=True)
        b.write_text(FAKE_SCANNER)
        b.chmod(0o755)
    e = {k: v for k, v in os.environ.items() if k != "PASSAGE_SCANNER"}
    e["PATH"] = str(tmp_path / "pathbin") + os.pathsep + e.get("PATH", "")
    e["HOME"] = str(tmp_path / "home")
    e["SCANNER"] = str(tmp_path / "pathbin" / "scanner")
    return e


def _assert_scanner_missing(rc, out):
    assert rc == 1, out
    assert "no passage scanner (PASSAGE_SCANNER unset" in out
    assert any(sig in out for sig in rd.SCANNER_MISSING)
    assert "FAIL:" not in out


def test_unset_scanner_takes_missing_route(tmp_path):
    rc, out = fair(tmp_path, _no_scanner_env(tmp_path), BODY_TWO,
                   "corr/referee_reply.txt:2")
    _assert_scanner_missing(rc, out)
    assert not (tmp_path / ".fairness-scan" / "summary.json").exists()


def test_non_executable_scanner_takes_missing_route(tmp_path):
    e = _no_scanner_env(tmp_path)
    plain = tmp_path / "notexec"
    plain.write_text(FAKE_SCANNER)
    plain.chmod(0o644)
    e["PASSAGE_SCANNER"] = str(plain)
    rc, out = fair(tmp_path, e, BODY_TWO, "corr/referee_reply.txt:2")
    _assert_scanner_missing(rc, out)
