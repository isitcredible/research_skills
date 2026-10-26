#!/usr/bin/env python3
"""Tests for check_manifest.py — the three-stage default layout and the legacy
analysis/fragility/ fallback.

Run: python3 -m unittest discover -s review/scripts/tests
"""
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_manifest.py"

HEADER = ("id,family,hypothesis,spec,artifact,seed,state,validity,row_role,"
          "ledger_item,consumer\n")
MANIFEST = HEADER + "c1,F1,h1,s1,{artifact},NA,done,clean,verdict-bearing,,\n"
RESULTS_OK = "spec_id,artifact,estimate,std_error\nc1,work/out.txt,1.0,0.1\n"
WALK_OK = ("| module | fired | evidence | report |\n|---|---|---|---|\n"
           "| iv-diagnostics | yes | 2SLS | `analysis/code-and-data/iv-diagnostics-REPORT.md` |\n"
           "| rdd-diagnostics | no | no cutoff | `analysis/code-and-data/rdd-diagnostics-REPORT.md` |\n")
ROBUST_OK = ("claim,page,cited_exhibit,outcomes_covered,classification,evidence\n"
             "robust to X,p.1,Table 1,all,SUPPORTED,work/out.txt\n")


def write_completeness(root, walk=WALK_OK, robust=ROBUST_OK, reports=True):
    """Checks 8-9 artifacts: module walk + reports/stubs, robustness-claims ledger."""
    cd = root / "analysis/code-and-data"; cd.mkdir(parents=True, exist_ok=True)
    (cd / "module-walk.md").write_text(walk)
    if reports:
        (cd / "iv-diagnostics-REPORT.md").write_text("# iv report\n")
        (cd / "rdd-diagnostics-REPORT.md").write_text("# stub: no cutoff\n")
    pp = root / "analysis/paper"; pp.mkdir(parents=True, exist_ok=True)
    (pp / "robustness-claims.csv").write_text(robust)


class ManifestLayoutTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        write_completeness(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def run_manifest(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            capture_output=True, text=True)

    def test_v5_default_layout(self):
        d = self.root / "analysis/code-and-data"
        d.mkdir(parents=True, exist_ok=True)
        (self.root / "work").mkdir()
        (self.root / "work/out.txt").write_text("ok\n")
        (d / "results.csv").write_text("spec_id,artifact,estimate,std_error\n")
        (d / "construction-ledger.md").write_text("# ledger\n")
        # manifest row claims an artifact that is absent -> proves the file
        # at the three-stage path was the one read
        (d / "battery-manifest.csv").write_text(
            MANIFEST.format(artifact="work/missing.txt"))
        proc = self.run_manifest()
        self.assertNotIn("legacy layout", proc.stdout)
        self.assertIn("FAIL c1: artifact 'work/missing.txt' missing or empty",
                      proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_legacy_fragility_fallback(self):
        d = self.root / "analysis/fragility"
        d.mkdir(parents=True, exist_ok=True)
        (self.root / "work").mkdir()
        (self.root / "work/out.txt").write_text("ok\n")
        (d / "results.csv").write_text("spec_id,artifact,estimate,std_error\n")
        (d / "construction-ledger.md").write_text("# ledger\n")
        (d / "battery-manifest.csv").write_text(
            MANIFEST.format(artifact="work/missing.txt"))
        proc = self.run_manifest()
        self.assertIn("NOTE legacy layout: analysis/fragility/", proc.stdout)
        self.assertIn("FAIL c1: artifact 'work/missing.txt' missing or empty",
                      proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_legacy_passes_clean(self):
        d = self.root / "analysis/fragility"
        d.mkdir(parents=True, exist_ok=True)
        (self.root / "work").mkdir()
        (self.root / "work/out.txt").write_text("ok\n")
        (d / "results.csv").write_text(
            "spec_id,artifact,estimate,std_error\nc1,work/out.txt,1.0,0.1\n")
        (d / "construction-ledger.md").write_text("# ledger\n")
        (d / "battery-manifest.csv").write_text(
            MANIFEST.format(artifact="work/out.txt"))
        proc = self.run_manifest()
        self.assertIn("NOTE legacy layout: analysis/fragility/", proc.stdout)
        self.assertIn("PASS", proc.stdout)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_v5_wins_over_legacy(self):
        for sub in ("analysis/code-and-data", "analysis/fragility", "work"):
            (self.root / sub).mkdir(parents=True, exist_ok=True)
        (self.root / "work/out.txt").write_text("ok\n")
        # three-stage manifest present (clean); legacy manifest would FAIL if read
        v5 = self.root / "analysis/code-and-data"
        (v5 / "battery-manifest.csv").write_text(
            MANIFEST.format(artifact="work/out.txt"))
        (v5 / "results.csv").write_text(
            "spec_id,artifact,estimate,std_error\nc1,work/out.txt,1.0,0.1\n")
        (v5 / "construction-ledger.md").write_text("# ledger\n")
        legacy = self.root / "analysis/fragility"
        (legacy / "battery-manifest.csv").write_text(
            MANIFEST.format(artifact="work/missing.txt"))
        proc = self.run_manifest()
        self.assertNotIn("legacy layout", proc.stdout)
        self.assertIn("PASS", proc.stdout)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_explicit_manifest_no_fallback(self):
        d = self.root / "analysis/fragility"
        d.mkdir(parents=True, exist_ok=True)
        (d / "battery-manifest.csv").write_text(
            MANIFEST.format(artifact="work/missing.txt"))
        proc = self.run_manifest("--manifest", "custom/manifest.csv")
        # an explicit path that does not exist errors as missing, never
        # silently reads the legacy twin
        self.assertIn("missing", proc.stdout)
        self.assertNotIn("legacy layout", proc.stdout)
        self.assertEqual(proc.returncode, 1)


class ManifestSchemaTest(unittest.TestCase):
    """Check 0 — schema, enums, empty manifest, missing results."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.d = self.root / "analysis/code-and-data"
        self.d.mkdir(parents=True)
        (self.root / "work").mkdir()
        (self.root / "work/out.txt").write_text("ok\n")
        (self.d / "results.csv").write_text(RESULTS_OK)
        (self.d / "construction-ledger.md").write_text("# ledger\n")
        write_completeness(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def run_manifest(self, manifest, cwd=None):
        (self.d / "battery-manifest.csv").write_text(manifest)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            capture_output=True, text=True, cwd=cwd)

    def test_clean_passes(self):
        proc = self.run_manifest(MANIFEST.format(artifact="work/out.txt"))
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_runs_from_elsewhere_with_root(self):
        proc = self.run_manifest(MANIFEST.format(artifact="work/out.txt"),
                                 cwd=tempfile.gettempdir())
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_header_only_fails(self):
        proc = self.run_manifest(HEADER)
        self.assertIn("header but no data rows", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_missing_results_fails(self):
        (self.d / "results.csv").unlink()
        proc = self.run_manifest(MANIFEST.format(artifact="work/out.txt"))
        self.assertIn("FAIL missing", proc.stdout)
        self.assertNotIn("WARN missing", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_bad_enums_fail(self):
        proc = self.run_manifest(
            HEADER + "c1,F1,h1,s1,work/out.txt,NA,finished,robust,main,,\n")
        for col in ("state='finished'", "validity='robust'", "row_role='main'"):
            self.assertIn(col, proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_alias_state_warns(self):
        proc = self.run_manifest(
            HEADER + "c1,F1,h1,s1,work/out.txt,NA,executed,clean,verdict-bearing,,\n")
        self.assertIn("WARN c1: state='executed' is a legacy alias", proc.stdout)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_canonical_upper_states_pass(self):
        rows = "".join(
            f"c{i},F1,h1,s1,NA,NA,{st},clean,rebuttal,,\n"
            for i, st in enumerate(("BLOCKED", "NOT_RUN", "NOT_APPLICABLE")))
        rows += "".join(
            f"d{i},F1,h1,s1,work/out.txt,NA,{st},clean,rebuttal,,\n"
            for i, st in enumerate(("NONREPRODUCED", "PROXY")))
        (self.d / "results.csv").write_text(
            RESULTS_OK + "d0,work/out.txt,1.0,0.1\n")
        proc = self.run_manifest(HEADER + rows)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_nonreproduced_and_proxy_need_artifact(self):
        for st in ("NONREPRODUCED", "PROXY"):
            proc = self.run_manifest(
                HEADER + f"c1,F1,h1,s1,NA,NA,{st},clean,verdict-bearing,,\n")
            self.assertIn(f"state={st.lower()} with no artifact", proc.stdout)
            self.assertEqual(proc.returncode, 1)
            proc = self.run_manifest(
                HEADER + f"c1,F1,h1,s1,work/gone.txt,NA,{st},clean,verdict-bearing,,\n")
            self.assertIn("artifact 'work/gone.txt' missing or empty", proc.stdout)
            self.assertEqual(proc.returncode, 1)

    def test_missing_seed_column_warns_only(self):
        proc = self.run_manifest(
            "id,family,hypothesis,spec,artifact,state,validity,row_role\n"
            "c1,F1,h1,s1,work/out.txt,done,clean,verdict-bearing\n")
        self.assertIn("WARN manifest has no 'seed' column", proc.stdout)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_missing_required_column_fails(self):
        proc = self.run_manifest(
            "id,state,artifact,validity,row_role\n"
            "c1,done,work/out.txt,clean,verdict-bearing\n")
        for c in ("family", "hypothesis", "spec"):
            self.assertIn(f"missing required column '{c}'", proc.stdout)
        self.assertIn("no 'seed' column", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_empty_required_field_fails(self):
        proc = self.run_manifest(
            HEADER + "c1,,h1,,work/out.txt,NA,done,clean,verdict-bearing,,\n")
        self.assertIn("required field 'family' is empty", proc.stdout)
        self.assertIn("required field 'spec' is empty", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_blank_seed_fails_na_passes(self):
        proc = self.run_manifest(
            HEADER + "c1,F1,h1,s1,work/out.txt,,done,clean,verdict-bearing,,\n")
        self.assertIn("'seed' is blank", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_done_with_na_artifact_fails(self):
        proc = self.run_manifest(
            HEADER + "c1,F1,h1,s1,NA,NA,done,clean,verdict-bearing,,\n")
        self.assertIn("state=done with no artifact", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_consumers_list_item_recognised(self):
        (self.d / "construction-ledger.md").write_text(
            "## L1 shared deflator\n  - consumers: F1, F2\n")
        proc = self.run_manifest(
            HEADER + "c1,F1,h1,s1,work/out.txt,NA,done,clean,verdict-bearing,L1,F1\n")
        # F2 declared under a list marker — must be enforced
        self.assertIn("ledger L1: consumer 'F2' has no manifest row", proc.stdout)
        self.assertNotIn("has no consumers: line", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_consumers_star_marker_covered_passes(self):
        (self.d / "construction-ledger.md").write_text(
            "## L1 shared deflator\n* consumers: F1\n")
        proc = self.run_manifest(
            HEADER + "c1,F1,h1,s1,work/out.txt,NA,done,clean,verdict-bearing,L1,F1\n")
        self.assertEqual(proc.returncode, 0, proc.stdout)


class CompletenessGateTest(ManifestSchemaTest):
    """Checks 8-9 — missing module reports and unassessed robustness claims FAIL."""
    CLEAN = HEADER + "c1,F1,h1,s1,work/out.txt,NA,done,clean,verdict-bearing,,\n"

    def test_fired_module_without_report_fails(self):
        (self.d / "iv-diagnostics-REPORT.md").unlink()
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("module iv-diagnostics: fired but no report found", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_should_fire_gap_row_fails(self):
        write_completeness(self.root, walk=WALK_OK +
                           "| theory-diagnostics | **SHOULD FIRE** | none | **GAP** |\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("module theory-diagnostics: fired but no report found", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_not_fired_without_stub_fails(self):
        (self.d / "rdd-diagnostics-REPORT.md").unlink()
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("module rdd-diagnostics: not fired but no not-applicable stub", proc.stdout)

    def test_unassessed_robustness_claim_fails(self):
        write_completeness(self.root, robust=ROBUST_OK + "similar for Y,p.2,Table 2,all,,\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("1 of 2 robustness claims unassessed", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_bad_classification_fails(self):
        write_completeness(self.root, robust=ROBUST_OK + "similar for Y,p.2,Table 2,all,OPEN,x\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("classification outside", proc.stdout)

    def test_fired_module_with_stub_report_fails(self):
        (self.d / "iv-diagnostics-REPORT.md").write_text("# IV\nStatus: NOT_APPLICABLE — no instrument.\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("module iv-diagnostics: fired but its report is a not-applicable stub", proc.stdout)
        self.assertEqual(proc.returncode, 1)
        (self.d / "rdd-diagnostics-REPORT.md").write_text("# RDD\nStatus: NOT_APPLICABLE — no cutoff.\n")
        (self.d / "iv-diagnostics-REPORT.md").write_text("# iv report\n")
        self.assertEqual(self.run_manifest(self.CLEAN).returncode, 0)

    def test_header_only_robustness_warns(self):
        write_completeness(self.root, robust=ROBUST_OK.splitlines()[0] + "\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("WARN analysis/paper/robustness-claims.csv: header only", proc.stdout)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_none_found_scan(self):
        head = ROBUST_OK.splitlines()[0] + "\n"
        write_completeness(self.root, robust=head + "none,NA,NA,NA,NONE_FOUND,searched robust; similar; unchanged; sensitiv\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertNotIn("header only", proc.stdout)
        write_completeness(self.root, robust=head + "none,NA,NA,NA,NONE_FOUND,\n")
        self.assertIn("carry no evidence", self.run_manifest(self.CLEAN).stdout)
        write_completeness(self.root, robust=ROBUST_OK + "none,NA,NA,NA,NONE_FOUND,searched robust\n")
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("NONE_FOUND beside 1 other row", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_missing_walk_fails(self):
        (self.d / "module-walk.md").unlink()
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("module-walk.md missing", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_blocked_variant_row_does_not_require_patch_or_moments(self):
        hdr = HEADER.rstrip("\n") + ",variant_of,patch,moments\n"
        rows = (
            "c1,F1,h1,s1,work/out.txt,NA,done,clean,verdict-bearing,,,,\n"
            "c2,F1,h1,s2,NA,NA,BLOCKED,clean,rebuttal,,,c1,NA,NA\n"
        )
        proc = self.run_manifest(hdr + rows)
        self.assertEqual(proc.returncode, 0, proc.stdout)


A_HDR = ("id,assumption,kind,grounding,conclusions,relaxation,artifact,effect,"
         "warrant,warrant_source,ruling,note\n")
A_OK = (A_HDR +
        "A1,sigma<1,structural,eq 1 p.9,CL16,sigma=1.5,work/out.txt,SIGN_FLIP,"
        "CONTESTED,lit survey p.3,WHIMSICAL,\n"
        "A2,closed economy,closure,eq 4,CL01,open,work/out.txt,IMMATERIAL,"
        "UNANCHORED,,INERT,\n"
        "A3,no learning,exclusion,eqs 1-4,CL02,,NA,UNTESTED,UNANCHORED,,UNRESOLVED,\n")
WHIMSY_ROW = ("| whimsical-assumptions-diagnostics | yes | model | "
              "`analysis/code-and-data/whimsical-assumptions-diagnostics-REPORT.md` |\n")


class AssumptionLedgerTest(ManifestSchemaTest):
    """Check 10 — the whimsical-assumptions ledger."""
    CLEAN = HEADER + "c1,F1,h1,s1,work/out.txt,NA,done,clean,verdict-bearing,,\n"

    def fire(self, ledger=None):
        write_completeness(self.root, walk=WALK_OK + WHIMSY_ROW)
        (self.d / "whimsical-assumptions-diagnostics-REPORT.md").write_text("# report\n")
        if ledger is not None:
            (self.d / "assumption-ledger.csv").write_text(ledger)

    def test_clean_ledger_passes(self):
        self.fire(A_OK)
        proc = self.run_manifest(self.CLEAN)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_fired_without_ledger_fails(self):
        self.fire()
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("assumption-ledger.csv missing", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_not_fired_no_ledger_passes(self):
        proc = self.run_manifest(self.CLEAN)
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_effect_without_artifact_fails(self):
        self.fire(A_OK.replace("work/out.txt,SIGN_FLIP", "NA,SIGN_FLIP"))
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("effect SIGN_FLIP needs artifact path(s)", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_multiple_artifacts_and_prose(self):
        self.fire(A_OK.replace("work/out.txt,SIGN_FLIP", "work/out.txt; work/out.txt,SIGN_FLIP"))
        self.assertEqual(self.run_manifest(self.CLEAN).returncode, 0)
        self.fire(A_OK.replace("work/out.txt,SIGN_FLIP", "run.sh -> work/out.txt,SIGN_FLIP"))
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("needs artifact path(s)", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_whimsical_needs_both_legs(self):
        self.fire(A_OK.replace("SIGN_FLIP,CONTESTED,lit survey p.3,WHIMSICAL",
                               "IMMATERIAL,SUPPORTED,lit survey p.3,WHIMSICAL"))
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("not shown critical", proc.stdout)
        self.assertIn("not shown unwarranted", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_graded_warrant_needs_source(self):
        self.fire(A_OK.replace("CONTESTED,lit survey p.3", "CONTRADICTED,"))
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("warrant CONTRADICTED needs a warrant_source", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_fragile_needs_threshold_and_unwarranted(self):
        rows = (A_HDR +
                "A1,x,bridge,p.1,CL1,,work/out.txt,THRESHOLD,CONTRADICTED,p.2,FRAGILE,flips at 0.79\n"
                "A2,y,bridge,p.1,CL1,,work/out.txt,MATERIAL,SUPPORTED,p.2,FRAGILE,\n")
        self.fire(rows)
        proc = self.run_manifest(self.CLEAN)
        self.assertNotIn("A1:", proc.stdout)
        self.assertIn("A2: FRAGILE with effect MATERIAL", proc.stdout)
        self.assertIn("A2: FRAGILE with warrant SUPPORTED", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_consumed_and_discarded_need_routing(self):
        rows = (A_HDR +
                "A1,x,closure,eq 1,CL1,,work/out.txt,NO_COUNTERPART,CONVENIENCE,p.2,"
                "CONSUMED,routed to: theory-diagnostics TH-1\n"
                "A2,y,stated,p.3,CL2,,NA,UNTESTED,UNANCHORED,,DISCARDED,value dispute\n")
        self.fire(rows)
        proc = self.run_manifest(self.CLEAN)
        self.assertNotIn("A1:", proc.stdout)
        self.assertIn("A2: DISCARDED without 'routed to", proc.stdout)
        self.assertEqual(proc.returncode, 1)

    def test_bad_enum_and_empty_grounding_fail(self):
        self.fire(A_OK.replace("structural", "vibes").replace("eq 4,", ","))
        proc = self.run_manifest(self.CLEAN)
        self.assertIn("kind='vibes' not in", proc.stdout)
        self.assertIn("A2: empty grounding", proc.stdout)
        self.assertEqual(proc.returncode, 1)


if __name__ == "__main__":
    unittest.main()
