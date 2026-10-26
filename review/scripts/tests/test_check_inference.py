#!/usr/bin/env python3
"""Tests for check_inference.py — the few-cluster inference gate.

Run: python3 -m unittest discover -s review/scripts/tests
"""
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
import subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_inference.py"


def run(root):
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root), "--list"], capture_output=True, text=True)
    return r.returncode, r.stdout


class InferenceGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        (self.root / "work/scripts").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_plain_boottest_fails(self):
        (self.root / "work/scripts/a.do").write_text("reg y x, cluster(s)\nboottest x, weight(webb) reps(9999)\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F1", out)

    def test_jk_and_continuation_pass(self):
        (self.root / "work/scripts/a.do").write_text(
            "boottest x, weight(webb) ///\n   reps(9999) jk noci\nassert !missing(r(p))\n* boottest x in a comment\n"
        )
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_which_and_comments_ignored(self):
        (self.root / "work/scripts/a.do").write_text(
            "which boottest\nhelp boottest\ncap noisily boottest x, jk noci reps(9999)\nassert !missing(r(p))\n"
        )
        (self.root / "work/scripts/b.py").write_text('# compare with boottest (x)\n"""docs: wildboottest(model)"""\nx = 1\n')
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_prefixed_plain_boottest_fails(self):
        (self.root / "work/scripts/a.do").write_text("capture noisily boottest x, reps(9999)\nassert !missing(r(p))\n")
        self.assertEqual(run(self.root)[0], 1)

    def test_robustness_tag_passes(self):
        (self.root / "work/scripts/a.do").write_text("boottest x, nonull reps(9999) // WCU-robustness\nassert !missing(r(p))\n")
        self.assertEqual(run(self.root)[0], 0)

    def test_r_default_type_fails_and_31_passes(self):
        f = self.root / "work/scripts/b.R"
        f.write_text('b <- fwildclusterboot::boottest(fit, clustid="s", param="x", B=9999)\n')
        self.assertEqual(run(self.root)[0], 1)
        f.write_text('b <- fwildclusterboot::boottest(fit, clustid="s", param="x", B=9999, bootstrap_type="31")\n')
        self.assertEqual(run(self.root)[0], 0)

    def test_r_type_33_is_wcr_b_and_fails(self):
        (self.root / "work/scripts/c.R").write_text('b <- fwildclusterboot::boottest(fit, clustid="s", param="x", B=9999, bootstrap_type="33")\n')
        self.assertEqual(run(self.root)[0], 1)

    def test_r_type_33_tagged_wcr_b_robustness_passes(self):
        (self.root / "work/scripts/c.R").write_text('b <- fwildclusterboot::boottest(fit, clustid="s", param="x", B=9999, bootstrap_type="33")  # WCR-B-robustness\n')
        self.assertEqual(run(self.root)[0], 0)

    def test_stata_honest_variant_tags_pass(self):
        (self.root / "work/scripts/a.do").write_text(
            "boottest x, reps(9999) // WCR-C-robustness\nassert !missing(r(p))\n"
            "boottest x, reps(9999) // WRE-robustness\nassert !missing(r(p))\n"
        )
        self.assertEqual(run(self.root)[0], 0)

    def test_wcr_s_tag_is_not_a_robustness_pass(self):
        (self.root / "work/scripts/a.do").write_text("boottest x, reps(9999) // WCR-S-robustness\nassert !missing(r(p))\n")
        self.assertEqual(run(self.root)[0], 1)

    def test_wcr_b_named_in_report_passes(self):
        (self.root / "SYNTHESIS.md").write_text("WCR-B p .03 sits beside WCR-S p .04.\n")
        self.assertEqual(run(self.root)[0], 0)

    def test_bare_wcr_in_report_fails(self):
        (self.root / "SYNTHESIS.md").write_text("The estimate is negative (WCR p .01).\nWCR-S p .04 is fine.\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("SYNTHESIS.md:1", out); self.assertNotIn("SYNTHESIS.md:2", out)

    def test_handoff_excluded_files_skipped(self):
        (self.root / "analysis").mkdir(parents=True, exist_ok=True)
        (self.root / "analysis/notes.md").write_text("old WCR p .01\n")
        self.assertEqual(run(self.root)[0], 1)
        (self.root / "HANDOFF.md").write_text("## inputs\n- SYNTHESIS.md\n## excluded\n- analysis/notes.md | exploratory | notes\n## conflicts\n")
        self.assertEqual(run(self.root)[0], 0)

    def test_shift_share_needs_rejection_table(self):
        d = self.root / "analysis/code-and-data"; d.mkdir(parents=True)
        (d / "shift-share-diagnostics-REPORT.md").write_text("# Shift-share\n")
        self.assertEqual(run(self.root)[0], 1)
        (d / "shift-share-diagnostics-REPORT.md").write_text(
            "# Shift-share\nShock-level jackknife (CV3) SE = .14.\n## Placebo-shock rejection rates\n| test | rate |\nRandomization p = .08.\n"
        )
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_not_applicable_stubs_owe_no_module_lines(self):
        d = self.root / "analysis/code-and-data"; d.mkdir(parents=True)
        (d / "shift-share-diagnostics-REPORT.md").write_text("# Shift-share\nNo exposure-weighted regressor.\n")
        (d / "iv-diagnostics-REPORT.md").write_text("# IV\nNo instrument.\n")
        code, out = run(self.root); self.assertEqual(code, 1)
        for f in ("F4", "F7", "F12", "F13"): self.assertIn(f, out)
        (d / "shift-share-diagnostics-REPORT.md").write_text("# Shift-share\nStatus: NOT_APPLICABLE — no exposure-weighted regressor or instrument.\n")
        (d / "iv-diagnostics-REPORT.md").write_text("# IV\n**Status:** `NOT_APPLICABLE` — no instrument in any result family.\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)
        (d / "iv-diagnostics-REPORT.md").write_text("# IV\nStatus: NOT_APPLICABLE\n")   # no reason: not a stub
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F7", out)

    def test_deposit_copies_ignored(self):
        for d in ("work/pkg", "work/pkg_variant/dofiles", "work/ado_local", "04_replication_x"):
            (self.root / d).mkdir(parents=True)
            (self.root / d / "x.do").write_text("boottest x, reps(999)\n")
        self.assertEqual(run(self.root)[0], 0)
        (self.root / "work/scripts/package.do").write_text("boottest x, reps(999)\n")
        self.assertEqual(run(self.root)[0], 1)


    def test_superseded_list(self):
        (self.root / "work/old").mkdir(parents=True); (self.root / "work/new").mkdir(parents=True)
        (self.root / "work/old/a.do").write_text("boottest x, reps(999)\n")
        sup = self.root / "inference-superseded.csv"
        sup.write_text("path,reason,replaced_by\nwork/old,historical WCR-C runs,work/new\n")
        self.assertEqual(run(self.root)[0], 0)
        sup.write_text("path,reason,replaced_by\nwork/old,,work/new\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F5", out)
        sup.write_text("path,reason,replaced_by\nwork/old,x,work/missing\n")
        self.assertEqual(run(self.root)[0], 1)


    def test_untagged_vtf_fails_and_tagged_passes(self):
        (self.root / "work/scripts/v.do").write_text("capture noisily vtf y (x=z) [aw=w], cluster(s)\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F6", out)
        (self.root / "work/scripts/v.do").write_text("capture noisily vtf y (x=z) [aw=w], cluster(s) // VtF-CR1-robustness\n* vtf in a comment\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_iv_report_needs_jackknife_vtf(self):
        d = self.root / "analysis/code-and-data"; d.mkdir(parents=True)
        (d / "iv-diagnostics-REPORT.md").write_text("VtF on CR1: [-.59, -.21]\nMOP effective F = 3.1.\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F7", out)
        (d / "iv-diagnostics-REPORT.md").write_text("VtF on CR1: [-.59, -.21]\nVtF, state jackknife inputs (F 2.98): unbounded\nMOP effective F = 3.1.\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_boottest_ar_fails_unless_tagged(self):
        f = self.root / "work/scripts/ar.do"
        f.write_text("boottest x, ar reps(9999)\nassert !missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F8", out)
        # Tagged AR companion row does not use jk and must pass both F8 and F1
        f.write_text("boottest x, ar reps(9999) // AR-boottest-robustness\nassert !missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)
        # cluster(ar) is a cluster varname, not the ar option
        f.write_text("boottest x, cluster(ar) jk noci reps(9999)\nassert !missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_boottest_jk_in_comment_or_cluster_arg_fails_f1(self):
        f = self.root / "work/scripts/jk_trap.do"
        f.write_text("boottest x, reps(9999) // jk omitted\nassert !missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F1", out)
        f.write_text("boottest x, cluster(jk) reps(9999)\nassert !missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F1", out)

    def test_boottest_jk_requires_noci_and_p_assert(self):
        f = self.root / "work/scripts/jk.do"
        f.write_text("boottest x, jk reps(9999)\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F9", out); self.assertIn("F10", out)
        f.write_text("boottest x, jk noci reps(9999)\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertNotIn("F9", out); self.assertIn("F10", out)
        f.write_text("boottest x, jk noci reps(9999)\nlocal p = r(p)\nassert `p' < .\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F10", out)
        # Commented or un-negated missing(r(p)) must fail F10
        f.write_text("boottest x, jk noci reps(9999)\n// assert !missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F10", out)
        f.write_text("boottest x, jk noci reps(9999)\nassert missing(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F10", out)
        f.write_text("boottest x, jk noci reps(9999)\nassert r(p) < .\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)
        f.write_text("boottest x, jk noci reps(9999)\nassert !mi(r(p))\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_honestdid_requires_universal_base_and_positive_positions(self):
        f = self.root / "work/scripts/did.do"
        f.write_text("csdid y, ivar(i) time(t) gvar(g)\nestat event, estore(cs)\nhonestdid, pre(3/6) post(7/11)\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F11", out)
        f.write_text("csdid y, ivar(i) time(t) gvar(g) long2\nestat event, estore(cs)\nhonestdid, pre(-4/-1) post(0/4)\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F11", out)
        f.write_text("csdid y, ivar(i) time(t) gvar(g) long2\nestat event, estore(cs)\nhonestdid, pre(3/6) post(7/11)\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)
        r = self.root / "work/scripts/did.R"
        r.write_text('out <- did::att_gt(yname="y", tname="t", idname="i", gname="g", data=d)\nHonestDiD::createSensitivityResults(betahat, sigma)\n')
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F11", out)
        r.write_text('out <- did::att_gt(yname="y", tname="t", idname="i", gname="g", base_period="universal", data=d)\nHonestDiD::createSensitivityResults(betahat, sigma)\n')
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_shift_share_requires_ri_and_shock_jackknife_and_allows_subheadings(self):
        d = self.root / "analysis/code-and-data"; d.mkdir(parents=True)
        p = d / "shift-share-diagnostics-REPORT.md"
        p.write_text("# Shift-share\n## Placebo-shock rejection rates\n| test | rate |\n| AKM | .18 |\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F4", out); self.assertIn("F12", out)
        p.write_text("# Shift-share\n## Placebo-shock rejection rates\n### Subheading inside section\nRandomization p = .09.\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertNotIn("F4", out); self.assertIn("F12", out)
        p.write_text("# Shift-share\nDelete-one-shock jackknife SE = .12.\n## Placebo-shock rejection rates\n### Subheading inside section\nRandomization p = .09.\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_iv_report_needs_effective_f_and_lowercase_mop_fails(self):
        d = self.root / "analysis/code-and-data"; d.mkdir(parents=True)
        p = d / "iv-REPORT.md"
        p.write_text("First-stage Cragg-Donald F = 18.4; mop up the table.\nVtF on jackknife inputs: [-.5, .2]\n")
        code, out = run(self.root); self.assertEqual(code, 1); self.assertIn("F13", out)
        p.write_text("Montiel Olea-Pflueger effective F = 6.2.\nVtF on jackknife inputs: [-.5, .2]\n")
        code, out = run(self.root); self.assertEqual(code, 0, out)

    def test_cointegration_and_cv3_warns(self):
        (self.root / "work/scripts/eg.R").write_text("# Engle-Granger cointegration test\nadf <- ur.df(e, type='none', lags=2)\n")
        (self.root / "work/scripts/cv3.py").write_text(
            "# hand-coded CV3 cluster jackknife\ny_til = demean(y, fe)\nfor g in clusters:\n    b.append(ols(y_til[c != g], x_til[c != g]))\n"
        )
        code, out = run(self.root); self.assertEqual(code, 0, out)
        self.assertIn("ur.df()", out); self.assertIn("CV3/jackknife loop", out)

if __name__ == "__main__":
    unittest.main()
