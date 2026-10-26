#!/usr/bin/env python3
"""Tests for check_spec_drift.py.

Run: python3 -m unittest discover -s audit-review/scripts/tests
"""
import csv
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_spec_drift.py"
CHANGES = (
    "id,version,date,kind,scope,requirement,source,removed,note\n"
    "R001,0.1,2026-09-12,baseline,review,Requirement history begins.,review/SKILL.md,,\n"
    "R002,0.1,2026-09-22,added,module:small-n-diagnostics,Report G*.,x,,\n"
    "R003,0.4,2026-10-04,removed,review,Old rule.,x,2026-10-06,\n"
    "R004,0.5,2026-10-07,layout,review,Three stages.,x,,\n"
    "R005,0.6,2026-10-09,added,review:stress,Run the stress stage.,x,,\n"
    "R006,0.6,2026-10-09,added,review,Dropped rule.,x,2026-10-10,\n"
    "R007,0.6,2026-10-09,added,review-digest,Digest gate rule.,x,,\n"
    "R008,0.6,2026-10-09,added,audit-review,Audit gate rule.,x,,\n"
)


class SpecDriftTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.review = base / "review"
        (self.review / "modules/small-n-diagnostics").mkdir(parents=True)
        (self.review / "modules/small-n-diagnostics/SKILL.md").write_text("x\n")
        (self.review / "spec-changes.csv").write_text(CHANGES)
        self.job = base / "job"
        self.job.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_drift(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.job),
                               "--review-skill", str(self.review), *args],
                              capture_output=True, text=True)

    def ids(self):
        with (self.job / "spec-drift.csv").open() as f:
            return [r["id"] for r in csv.DictReader(f)]

    def dispose(self, values):
        p = self.job / "spec-drift.csv"
        with p.open() as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            r["disposition"] = values.get(r["id"], r["disposition"])
        with p.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    def test_needs_version_or_date(self):
        r = self.run_drift("--write")
        self.assertEqual(r.returncode, 1)
        self.assertIn("--run-date", r.stdout)

    def test_by_version_skips_removed_and_older(self):
        (self.job / "00_INTAKE.md").write_text("- **Suite version**: 0.4\n")
        self.assertEqual(self.run_drift("--write").returncode, 0)
        self.assertEqual(self.ids(), ["R004", "R005"])  # R006 dropped; R007/R008 downstream scopes excluded

    def test_by_date(self):
        self.run_drift("--write", "--run-date", "2026-09-20")
        self.assertEqual(self.ids(), ["R002", "R004", "R005"])

    def test_predates_history_rewalks_everything(self):
        self.run_drift("--write", "--run-date", "2026-09-06")
        ids = self.ids()
        self.assertIn("W-module:small-n-diagnostics", ids)
        self.assertIn("W-review:challenge", ids)
        self.assertIn("W-review:verdict", ids)
        self.assertNotIn("R002", ids)

    def test_check_dispositions(self):
        (self.job / "00_INTAKE.md").write_text("Suite version: 0.4\n")
        self.run_drift("--write")
        r = self.run_drift()
        self.assertEqual(r.returncode, 1)
        self.assertIn("blank", r.stdout)
        self.dispose({"R004": "done: missing.md", "R005": "na:"})
        out = self.run_drift().stdout
        self.assertIn("path(s) not found", out)
        self.assertIn("needs a reason", out)
        (self.job / "review").mkdir()
        (self.job / "review/stress-REPORT.md").write_text("x\n")
        self.dispose({"R004": "na: old layout mapped per audit rules",
                      "R005": "done: review/stress-REPORT.md"})
        r = self.run_drift()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_write_keeps_dispositions(self):
        (self.job / "00_INTAKE.md").write_text("Suite version: 0.4\n")
        self.run_drift("--write")
        self.dispose({"R004": "na: kept"})
        self.run_drift("--write")
        with (self.job / "spec-drift.csv").open() as f:
            rows = {r["id"]: r["disposition"] for r in csv.DictReader(f)}
        self.assertEqual(rows["R004"], "na: kept")


if __name__ == "__main__":
    unittest.main()
