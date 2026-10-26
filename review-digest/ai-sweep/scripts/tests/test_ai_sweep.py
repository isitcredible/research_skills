"""ai_sweep.py — the engine's deterministic parts: the mechanical tell
pass, the keep record, the scoping rules, and the paths that run without
a passage scanner (missing, forced off, private root). A stub scanner
covers the register-scan path without a model."""
import json
import os
import re
import stat
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
ENGINE = SCRIPTS / "ai_sweep.py"
sys.path.insert(0, str(SCRIPTS))

import ai_sweep as sweep  # noqa: E402

SAMPLE = """\
---
title: It is worth noting that frontmatter never renders
---

# Results

It is worth noting that output rose by 3.5 units.

We checked the estimate against the deposited log.

Output rose by 3.5 units in the East region — the treated workshops.

```
It is worth noting that fenced code is skipped.
```

The program was introduced at six workshops in one region and the comparison group sits entirely in the other region, so the estimate compares two regions with different histories and different reporting.
"""


def flags_for(text, path="doc.md", plumb_on=True):
    """Run the mechanical pass over text written to a temporary path."""
    lines = text.splitlines()
    internal = set()
    if lines and lines[0].strip() == "---":
        internal.add(1)
        for i in range(1, len(lines)):
            internal.add(i + 1)
            if lines[i].strip() == "---":
                break
    return sweep.mechanical(lines, internal, path.endswith((".yaml", ".yml")),
                            plumb_on=plumb_on)


def by_level(flags, level):
    return [(ln, label) for ln, lvl, label, _ in flags if lvl == level]


def run(target, *args, env_extra=None, scanner=None):
    env = {k: v for k, v in os.environ.items()
           if k not in ("PASSAGE_SCANNER", "AI_SWEEP_PRIVATE_ROOTS")}
    if scanner:
        env["PASSAGE_SCANNER"] = str(scanner)
    env.update(env_extra or {})
    proc = subprocess.run([sys.executable, "-I", str(ENGINE), str(target),
                           *map(str, args)],
                          capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout + proc.stderr


# --- the mechanical tell pass -------------------------------------------------

def test_stock_phrase_fails_on_its_line_only():
    fails = by_level(flags_for(SAMPLE), "fail")
    assert fails == [(7, "'it is worth' filler"), (7, "'worth X' filler")]


def test_frontmatter_and_fenced_code_are_exempt():
    lines = [ln for ln, _ in by_level(flags_for(SAMPLE), "fail")]
    assert 2 not in lines        # frontmatter title
    assert 14 not in lines       # inside the fence


def test_plumbing_phrase_is_a_hypothesis_not_a_fail():
    flags = flags_for(SAMPLE)
    assert (9, "self-narrating verification / deliberation") in by_level(flags, "plumb")
    assert 9 not in [ln for ln, _ in by_level(flags, "fail")]


def test_no_plumbing_disables_the_phrase_net():
    assert by_level(flags_for(SAMPLE, plumb_on=False), "plumb") == []


def test_reconciliation_gloss_needs_a_number():
    assert by_level(flags_for("In other words, the effect is small.\n"), "plumb") == []
    assert by_level(flags_for("In other words, the effect is 3.5 units.\n"), "plumb") \
        == [(1, "reconciliation gloss")]


def test_em_dash_and_long_sentence_are_notes():
    flags = flags_for(SAMPLE)
    assert [ln for ln, _ in by_level(flags, "emdash")] == [11]
    notes = by_level(flags, "note")
    assert len(notes) == 1 and notes[0][0] == 17
    assert re.match(r"3\d-word prose sentence", notes[0][1])


def test_numbers_and_parentheticals_do_not_count_toward_length():
    sent = ("Freight social savings were 4,677.24M Rs (22.9% of GDP in 1913, "
            "on the benchmark rates and the full network) in the base year.")
    assert sweep.prose_word_count(sent) < 30


def test_skip_fields_exempts_a_whole_block_scalar(tmp_path):
    doc = tmp_path / "page.yaml"
    doc.write_text("title: Results\n"
                   "notes: |\n"
                   "  It is worth noting that this never renders.\n"
                   "  Nor does this.\n"
                   "content: It is worth noting that this renders.\n")
    internal, lines = sweep.internal_lines(str(doc), re.compile(r"^\s*(?:notes)\s*:", re.I))
    assert {2, 3, 4} <= internal and 5 not in internal
    fails = [f for f in sweep.mechanical(lines, internal, True) if f[1] == "fail"]
    assert {f[0] for f in fails} == {5}


# --- the keep record ----------------------------------------------------------

def test_keep_needs_a_reason_and_a_distinctive_phrase(tmp_path):
    doc = tmp_path / "post.md"
    doc.write_text("x\n")
    (tmp_path / "post.keeps.md").write_text(
        "- `it is worth noting that output` — quoted from the source\n"
        "- `the problem is that the` —\n"
        "- `worth it` — too short to bind\n")
    keeps = sweep.load_keeps(str(doc))
    assert keeps == {"it is worth noting that output"}


def test_keep_binds_to_the_wording():
    keeps = {"it is worth noting that output"}
    assert sweep.kept_keep(sweep.norm("It is *worth* noting that output rose."), keeps)
    assert not sweep.kept_keep("It is worth noting that wages rose.", keeps)


def test_recorded_keep_clears_the_fail_in_a_run(tmp_path):
    doc = tmp_path / "post.md"
    doc.write_text("It is worth noting that output rose by 3.5 units.\n")
    code, out = run(doc, "--mechanical-only")
    assert code == 1 and "FAIL  L1" in out
    (tmp_path / "post.keeps.md").write_text(
        "- `It is worth noting that output rose` — the author's own sentence, quoted\n")
    code, out = run(doc, "--mechanical-only")
    assert "FAIL  L1" not in out and "recorded keep" in out
    assert code == 1, "mechanical-only is never the full gate"


# --- runs without a passage scanner -------------------------------------------

def test_missing_scanner_is_incomplete_and_fails(tmp_path):
    doc = tmp_path / "clean.md"
    doc.write_text("Output rose by 3.5 units.\n")
    code, out = run(doc)
    assert code == 1
    assert sweep.SCANNER_MISSING_MSG in out and "INCOMPLETE" in out
    assert not (tmp_path / ".style-scan").exists()


def test_scanner_path_that_is_not_executable_counts_as_missing(tmp_path):
    doc = tmp_path / "clean.md"
    doc.write_text("Output rose by 3.5 units.\n")
    fake = tmp_path / "scanner"
    fake.write_text("#!/bin/sh\nexit 0\n")      # not chmod +x
    code, out = run(doc, scanner=fake)
    assert code == 1 and "INCOMPLETE" in out


def test_warn_only_exits_zero(tmp_path):
    doc = tmp_path / "draft.md"
    doc.write_text("It is worth noting that output rose.\n")
    code, out = run(doc, "--warn-only")
    assert code == 0 and "FAIL" in out


def test_plumbing_hypotheses_do_not_move_the_exit(tmp_path):
    doc = tmp_path / "draft.md"
    doc.write_text("We checked the estimate against the log.\n")
    code, out = run(doc, "--warn-only")
    assert code == 0
    assert "PLUMBING HYPOTHESES" in out and "never silent-cut" in out
    assert doc.read_text() == "We checked the estimate against the log.\n"


# --- the register-scan path, with a stub scanner ------------------------------

STUB = """#!{python}
import hashlib, json, os, sys
args = sys.argv[1:]
target = args[1]
out = args[args.index("--output") + 1]
text = open(target).read()
sha = hashlib.sha256(open(target, "rb").read()).hexdigest()
os.makedirs(os.path.join(out, "judgments"), exist_ok=True)
n = len(text.splitlines())
json.dump({{"passages": [{{"passage_id": "p1", "line_start": 1, "line_end": n,
            "text": text, "source_sha256": sha}}]}},
          open(os.path.join(out, "manifest.json"), "w"))
json.dump({{"line_start": 1, "line_end": n, "passage_id": "p1",
           "response": {{"answers": {{
               "ai_register": {{"score": {score}, "confidence": 0.9}},
               "fact_free_sentences": {{"noul": 0.1}},
               "deliberation_leak": {{"noul": 0.0}}}}}}}},
          open(os.path.join(out, "judgments", "p1.json"), "w"))
json.dump({{"complete": True}}, open(os.path.join(out, "summary.json"), "w"))
"""


def stub_scanner(tmp_path, score):
    p = tmp_path / "bin" / "scanner"
    p.parent.mkdir(exist_ok=True)
    p.write_text(STUB.format(python=sys.executable, score=score))
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return p


def test_scan_score_over_threshold_fails_and_a_keep_clears_it(tmp_path):
    doc = tmp_path / "doc" / "post.md"
    doc.parent.mkdir()
    doc.write_text("Output rose by 3.5 units across the treated workshops.\n")
    scanner = stub_scanner(tmp_path, 2.0)
    code, out = run(doc, scanner=scanner)
    assert code == 1 and "FAIL  L1-1 score=2.00" in out
    assert (doc.parent / ".style-scan" / ".ai-sweep-owned").exists()
    (doc.parent / "post.keeps.md").write_text(
        "- `Output rose by 3.5 units across` — plain statement of the estimate\n")
    code, out = run(doc, scanner=scanner)
    assert code == 0 and "sweep clean" in out


def test_scan_below_watch_is_clean(tmp_path):
    doc = tmp_path / "doc" / "post.md"
    doc.parent.mkdir()
    doc.write_text("Output rose by 3.5 units.\n")
    code, out = run(doc, scanner=stub_scanner(tmp_path, 0.2))
    assert code == 0 and "sweep clean" in out


def test_private_root_never_reaches_the_scanner(tmp_path):
    doc = tmp_path / "private" / "note.md"
    doc.parent.mkdir()
    doc.write_text("Output rose by 3.5 units.\n")
    code, out = run(doc, scanner=stub_scanner(tmp_path, 0.2),
                    env_extra={"AI_SWEEP_PRIVATE_ROOTS": str(tmp_path / "private")})
    assert code == 1 and "private tree" in out
    assert not (doc.parent / ".style-scan").exists()


def test_foreign_scan_dir_is_never_cleared(tmp_path):
    doc = tmp_path / "doc" / "post.md"
    doc.parent.mkdir()
    doc.write_text("Output rose by 3.5 units.\n")
    content = tmp_path / "content"
    content.mkdir()
    (content / "chapter.md").write_text("keep me\n")
    code, out = run(doc, "--scan-dir", content, scanner=stub_scanner(tmp_path, 0.2))
    assert code == 0
    assert (content / "chapter.md").read_text() == "keep me\n"
    assert (content / "scan-1" / ".ai-sweep-owned").exists()
    assert json.loads((content / "scan-1" / "summary.json").read_text())["complete"]
