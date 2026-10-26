#!/usr/bin/env python3
"""Tests for check_coverage.py — numbered equations, figures, n/a
dispositions, and deposit coverage. Each test builds a temp job root and
runs the script as a subprocess.

Run: python3 -m unittest discover -s audit-review/scripts/tests
"""
import csv
import io
import json
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_coverage.py"


def mkpdf(text):
    """A minimal one-page PDF whose text layer pdftotext reads back."""
    content = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += (b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (len(objs) + 1, xref))
    return bytes(out)


def build_root(base, surface=None, extracts=None, ledgers=None, na=None,
               deposit=None, logs=None, reports=None, intake="Deposit: none\n"):
    """Assemble a minimal job root under `base` (a Path). With no deposit
    inventory, 00_INTAKE.md records `Deposit: none` unless intake=None."""
    (base / "review/extracts").mkdir(parents=True, exist_ok=True)
    (base / "analysis").mkdir(parents=True, exist_ok=True)
    if surface is not None:
        (base / "review/extracts/01_paper.txt").write_text(surface)
    for name, text in (extracts or {}).items():
        (base / "review/extracts" / name).write_text(text)
    for rel, text in (ledgers or {}).items():
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    if na is not None:
        (base / "coverage-na.csv").write_text(na)
    if deposit is not None:
        (base / "review/deposit-inventory.json").write_text(
            json.dumps({"files": deposit}))
    elif intake is not None:
        (base / "00_INTAKE.md").write_text(intake)
    for rel, text in (logs or {}).items():
        p = base / "work/logs" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    for rel, text in (reports or {}).items():
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return base


class _JobRootCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_cov(self, *args):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root),
             "--out", "coverage.csv", *args],
            capture_output=True, text=True)
        out_csv = self.root / "coverage.csv"
        rows = {}
        if out_csv.is_file():
            for r in csv.DictReader(io.StringIO(out_csv.read_text())):
                rows.setdefault(r["ref"], r)
        return proc.returncode, proc.stdout, rows


class CoverageTest(_JobRootCase):
    def test_numbered_eq_covered_by_eq_dot(self):
        build_root(self.root, surface="we estimate the model\ny = a + bx   (3)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 3,est.do:14,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 3"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_numbered_eq_uncovered_fails(self):
        build_root(self.root, surface="we estimate the model\ny = a + bx   (4)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 4"]["status"], "open")
        self.assertIn("FAIL printed ref 'eq 4'", out)
        self.assertEqual(rc, 1)

    def test_eq_range_covers_numbered(self):
        build_root(self.root, surface="the result follows\nz = g(w)   (3)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neqs. 2-5,model.do,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 3"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_num_tag_requires_math(self):
        # "Technology (600)" in a table header is not an equation tag
        build_root(self.root,
                   surface="Sector shares\nLink  German  1500-1930  Decimal   Technology (600)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertNotIn("eq 600", rows)
        self.assertEqual(rc, 0, out)

    def test_tag_on_line_after_math_counts(self):
        build_root(self.root,
                   surface="the model is\n  y = a + bx + e\n                              (4)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\n(4),est.do:20,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 4"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_bare_paren_covers_only_in_formula_map(self):
        build_root(self.root, surface="we estimate\ny = a + bx   (3)\n",
                   ledgers={"analysis/code-and-data/results.csv":
                            "spec_id,artifact,estimate\ncol (3),work/x.txt,1.0\n"})
        rc, out, rows = self.run_cov()
        # a results row naming "col (3)" is not an equation reference
        self.assertEqual(rows["eq 3"]["status"], "open")
        self.assertEqual(rc, 1)
        # the same bare "(3)" in the formula map does cover it
        (self.root / "analysis/code-and-data/formula-map.csv").write_text(
            "printed_ref,implementing,status\n(3),est.do:14,identical\n")
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 3"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_extracts_prefer_published_dumps(self):
        build_root(self.root,
                   extracts={"01_paper.txt": "we estimate\ny = a + bx   (4)\n",
                             "03_draft.txt": "earlier draft\nz = g(w)   (9)\n"},
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\n(4),est.do:20,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 4"]["status"], "covered")
        self.assertNotIn("eq 9", rows)   # working-paper surface ignored
        self.assertNotIn("non-published", out)
        self.assertEqual(rc, 0, out)

    def test_extracts_fallback_warns(self):
        build_root(self.root,
                   extracts={"03_draft.txt": "earlier draft\nz = g(w)   (9)\n"},
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\n(9),est.do:20,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertIn("surface includes non-published extracts", out)
        self.assertEqual(rows["eq 9"]["status"], "covered")

    def test_figure_open_fails(self):
        build_root(self.root, surface="Figure 2 plots the series.\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["Figure 2"]["status"], "open")
        self.assertIn("FAIL printed ref 'Figure 2'", out)
        self.assertEqual(rc, 1)

    def test_figure_prose_only_warns(self):
        build_root(self.root, surface="Figure 2 plots the series.\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   reports={"review/code-and-data-REPORT.md":
                            "# Report\n\nFigure 2 was inspected by eye.\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["Figure 2"]["status"], "weak")
        self.assertIn("WARN printed ref 'Figure 2'", out)
        self.assertEqual(rc, 0, out)

    def test_na_row_clears_fail(self):
        build_root(self.root, surface="the result follows\nz = g(w)   (4)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   na="ref,reason\neq 4,appendix identity, audited in claims-REPORT\n")
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 4"]["status"], "n/a")
        self.assertEqual(rc, 0, out)

    def test_na_empty_reason_fails(self):
        build_root(self.root, surface="the result follows\nz = g(w)   (4)\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   na="ref,reason\neq 4,\n")
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["eq 4"]["status"], "n/a")
        self.assertIn("n/a without reason", out)
        self.assertEqual(rc, 1)

    def test_na_glob_clears_deposit(self):
        build_root(self.root, surface="plain text with no refs\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   deposit=[{"path": "lib/a.do", "ext": "do"},
                            {"path": "lib/b.do", "ext": "do"},
                            {"path": "src/c.py", "ext": "py"}],
                   na="ref,reason\nlib/*.do,vendored library code\n")
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["lib/a.do"]["status"], "n/a")
        self.assertEqual(rows["lib/b.do"]["status"], "n/a")
        # the pattern must not touch non-matching or non-deposit rows
        self.assertEqual(rows["src/c.py"]["status"], "open")
        self.assertIn("FAIL deposit file 'src/c.py'", out)
        self.assertEqual(rc, 1)

    def test_na_dir_pattern_clears_deposit(self):
        build_root(self.root, surface="plain text with no refs\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   deposit=[{"path": "ado/helper.ado", "ext": "ado"},
                            {"path": "ado/sub/deep.ado", "ext": "ado"}],
                   na="ref,reason\nado/,community ado files\n")
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["ado/helper.ado"]["status"], "n/a")
        self.assertEqual(rows["ado/sub/deep.ado"]["status"], "n/a")
        self.assertEqual(rc, 0, out)

    def test_na_pattern_matching_nothing_warns(self):
        build_root(self.root, surface="plain text with no refs\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   deposit=[{"path": "a.py", "ext": "py"}],
                   logs={"run.log": "running a.py\n"},
                   na="ref,reason\ngone/,directory dropped from deposit\n")
        rc, out, rows = self.run_cov()
        self.assertIn("n/a pattern 'gone/' matches no coverage row", out)
        self.assertEqual(rows["a.py"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_unmentioned_do_file_fails(self):
        build_root(self.root, surface="plain text with no refs\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   deposit=[{"path": "code/build.do", "ext": "do"}])
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["code/build.do"]["status"], "open")
        self.assertIn("FAIL deposit file 'code/build.do' never read or run", out)
        self.assertEqual(rc, 1)

    def test_r_file_mentioned_in_log_passes(self):
        build_root(self.root, surface="plain text with no refs\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   deposit=[{"path": "code/est.R", "ext": "r"}],
                   logs={"run.log": "12:01 running est.R\n12:40 done\n"})
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["code/est.R"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_unmentioned_dta_warns_only(self):
        build_root(self.root, surface="plain text with no refs\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
                   deposit=[{"path": "data/panel.dta", "ext": "dta"}])
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["data/panel.dta"]["status"], "open")
        self.assertIn("WARN deposit data file 'data/panel.dta'", out)
        self.assertEqual(rc, 0, out)

    def test_inline_paren_is_not_eq_ref(self):
        build_root(self.root, surface="the term (3) above shows nothing\n",
                   ledgers={"analysis/code-and-data/formula-map.csv":
                            "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"})
        rc, out, rows = self.run_cov()
        self.assertNotIn("eq 3", rows)
        self.assertEqual(rc, 0, out)

    def test_display_roman_and_oa_and_case_folding(self):
        build_root(
            self.root,
            surface="A table civil war is not a display, while Table OA.1 and Table 1a are.\n",
            ledgers={"analysis/code-and-data/results.csv":
                     "spec_id,source_cell\n1,Table OA.1\n2,Table 1a\n"})
        rc, out, rows = self.run_cov()
        self.assertNotIn("Table CIVIL", rows)
        self.assertEqual(rows["Table OA.1"]["status"], "covered")
        self.assertEqual(rows["Table 1A"]["status"], "covered")
        self.assertEqual(rc, 0, out)

    def test_deferral_cleared_by_na_and_handoff_excluded(self):
        build_root(
            self.root,
            surface="plain text\n",
            ledgers={"analysis/code-and-data/formula-map.csv":
                     "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"},
            reports={
                "review/active-REPORT.md": "Raw data not in the deposit.\n",
                "review/old-REPORT.md": "Source unshipped in old draft.\n",
            },
            na="ref,reason\nreview/active-REPORT.md:1,discussed in prose only\n")
        (self.root / "HANDOFF.md").write_text(
            "# Handoff\n\n## excluded\n- review/old-REPORT.md | superseded | review/active-REPORT.md\n"
        )
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["review/active-REPORT.md:1"]["status"], "n/a")
        self.assertNotIn("review/old-REPORT.md:1", rows)
        self.assertEqual(rc, 0, out)


class SurfaceAndDepositGateTest(_JobRootCase):
    """No surface -> FAIL; no inventory -> FAIL unless intake says none;
    --paper/--appendix auto-discovery and glob expansion."""

    LEDGER = {"analysis/code-and-data/formula-map.csv":
              "printed_ref,implementing,status\neq. 1,est.do:10,identical\n"}

    def test_no_surface_fails(self):
        build_root(self.root, ledgers=self.LEDGER)
        rc, out, rows = self.run_cov()
        self.assertIn("FAIL no printed-surface source", out)
        self.assertEqual(rc, 1)

    def test_missing_inventory_fails(self):
        build_root(self.root, surface="plain text\n", ledgers=self.LEDGER,
                   intake=None)
        rc, out, rows = self.run_cov()
        self.assertIn("FAIL review/deposit-inventory.json missing", out)
        self.assertEqual(rc, 1)

    def test_missing_inventory_intake_partial_fails(self):
        build_root(self.root, surface="plain text\n", ledgers=self.LEDGER,
                   intake="# Intake\n\nDeposit: partial — code only\n")
        rc, out, rows = self.run_cov()
        self.assertIn("deposit-inventory.json missing", out)
        self.assertEqual(rc, 1)

    def test_intake_deposit_none_passes(self):
        build_root(self.root, surface="plain text\n", ledgers=self.LEDGER,
                   intake="# Intake\n\n- **Deposit:** none — no package shipped\n")
        rc, out, rows = self.run_cov()
        self.assertEqual(rc, 0, out)

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext not installed")
    def test_pdf_autodiscovered(self):
        build_root(self.root, ledgers=self.LEDGER)
        (self.root / "01_paper_Smith_2024_AER.pdf").write_bytes(
            mkpdf("Figure 7 plots the series."))
        rc, out, rows = self.run_cov()
        self.assertEqual(rows["Figure 7"]["status"], "open")
        self.assertNotIn("no printed-surface source", out)
        self.assertEqual(rc, 1)

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext not installed")
    def test_appendix_glob_expanded_under_root(self):
        build_root(self.root, ledgers=self.LEDGER)
        (self.root / "02_appendix_Smith_2024.pdf").write_bytes(
            mkpdf("Table B3 lists the sample."))
        # an unexpanded glob, as a quoted shell argument would arrive
        rc, out, rows = self.run_cov("--paper", "nomatch_*.pdf",
                                     "--appendix", "02_*.pdf")
        self.assertIn("Table B3", rows)
        self.assertEqual(rc, 1)

    def test_expand_pdfs_unit(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import check_coverage as cc
        (self.root / "01_a.pdf").write_bytes(b"x")
        (self.root / "01_b.pdf").write_bytes(b"x")
        (self.root / "sub").mkdir()
        (self.root / "sub/01_c.pdf").write_bytes(b"x")
        self.assertEqual(cc.expand_pdfs(self.root, "", "01_*.pdf"),
                         ["01_a.pdf", "01_b.pdf"])
        self.assertEqual(cc.expand_pdfs(self.root, "sub/01_*.pdf", "01_*.pdf"),
                         ["sub/01_c.pdf"])
        self.assertEqual(cc.expand_pdfs(self.root, "paper.pdf", "01_*.pdf"),
                         ["paper.pdf"])


if __name__ == "__main__":
    unittest.main()
