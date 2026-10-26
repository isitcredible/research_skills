#!/usr/bin/env python3
"""Tests for deposit_inventory.py — content sniffing, name hints, empty
files, symlinks. Synthetic files in tmp_path; the script runs as a
subprocess against them.

Run: python3 -m pytest review/assets/tests
"""
import bz2
import gzip
import json
import lzma
import os
import subprocess
import sys
sys.dont_write_bytecode = True  # never leave __pycache__ in the skill folder
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "deposit_inventory.py"
sys.path.insert(0, str(SCRIPT.parent))
import deposit_inventory as di  # noqa: E402

# Stata 114, LOHI: ds_format, byteorder, filetype, unused, nvar, nobs,
# data_label[81], time_stamp[18]
LEGACY_DTA = (bytes([0x72, 0x02, 0x01, 0x00]) + b"\x03\x00" + b"\x0a\x00\x00\x00"
              + b"\x00" * 81 + b"12 Mar 2010 10:00\x00")
SAS_HEAD = (b"\x00" * 12 + bytes.fromhex("c2ea8160b31411cfbd92080009c7318c181f1011")
            + b"\x00" * 64)


def inventory(tmp_path, files):
    dep = tmp_path / "deposit"
    dep.mkdir()
    for rel, data in files.items():
        p = dep / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    out = tmp_path / "inv.json"
    proc = subprocess.run([sys.executable, str(SCRIPT), str(dep), "--out", str(out)],
                          capture_output=True, text=True)
    assert proc.returncode in (0, None), proc.stderr
    inv = json.loads(out.read_text())
    return {r["path"]: r for r in inv["files"]}, inv["summary"]


@pytest.mark.parametrize("name,data", [
    ("main.do", b"set more off\nuse data.dta\n"),
    ("clean.R", b"rm(list = ls())\nlibrary(haven)\n"),
    ("regions.csv", b"region,pop\nnorth,10\n"),
])
def test_text_starting_with_q_r_s_is_not_stata(tmp_path, name, data):
    rows, _ = inventory(tmp_path, {name: data})
    assert rows[name]["sniffed_format"] == "text"
    assert rows[name]["ext_matches_content"] is True


def test_legacy_dta_header_detected(tmp_path):
    rows, summary = inventory(tmp_path, {"panel.dta": LEGACY_DTA})
    r = rows["panel.dta"]
    assert r["sniffed_format"] == "stata-dta-legacy"
    assert r["ext_matches_content"] is True
    assert r["provenance"] == "unknown"
    assert "panel.dta" in summary["probe_queue"]


@pytest.mark.parametrize("release", [0x68, 0x69, 0x6c, 0x6e, 0x6f, 0x71, 0x72, 0x73])
@pytest.mark.parametrize("order", [1, 2])
@pytest.mark.parametrize("unused", [0x00, 0x01, 0x77, 0xff])
def test_legacy_dta_releases(release, order, unused):
    # unused byte varies in real deposits (0x00, 0x01 per spec, 0x77, 0xff)
    head = bytes([release, order, 1, unused]) + b"\x00" * 8
    assert di.sniff_head(head) == "stata-dta-legacy"


def test_legacy_dta_rejects_bad_header():
    assert di.sniff_head(bytes([0x72, 0x03, 0x01, 0x00]) + b"\x00") != "stata-dta-legacy"
    assert di.sniff_head(bytes([0x72, 0x02, 0x02, 0x00]) + b"\x00") != "stata-dta-legacy"
    assert di.sniff_head(bytes([0x74, 0x02, 0x01, 0x00]) + b"\x00") != "stata-dta-legacy"
    assert di.sniff_head(bytes([0x72, 0x02, 0x01])) != "stata-dta-legacy"


@pytest.mark.parametrize("name,data,fmt", [
    ("model.rda", gzip.compress(b"RDX2\nX\n\x00\x00\x00\x02"), "gzip"),
    ("model.rds", gzip.compress(b"X\n\x00\x00\x00\x03"), "gzip"),
    ("model.RData", bz2.compress(b"RDX2\nX\n\x00\x00\x00\x02"), "bzip2"),
    ("model.rda", lzma.compress(b"RDX3\nX\n\x00\x00\x00\x03"), "xz"),
    ("model.rda", b"RDX2\nX\n\x00\x00\x00\x02", "rdata"),
    ("model.rda", b"RDA2\nA\n2\n", "rdata"),
])
def test_rdata_signatures_match_extension(tmp_path, name, data, fmt):
    rows, summary = inventory(tmp_path, {name: data})
    r = rows[name]
    assert r["sniffed_format"] == fmt
    assert r["ext_matches_content"] is True
    assert r["provenance"] == "unknown"
    assert name not in summary["ext_mismatches"]


def test_rds_mismatch_and_hdf5_data_role(tmp_path):
    rows, summary = inventory(tmp_path, {
        "bad.rds": b"<html>error</html>\n",
        "grid.h5": b"\x89HDF\r\n\x1a\n" + b"\x00" * 32,
    })
    assert rows["bad.rds"]["ext_matches_content"] is False
    assert "bad.rds" in summary["ext_mismatches"]
    assert rows["grid.h5"]["sniffed_format"] == "hdf5"
    assert rows["grid.h5"]["ext_matches_content"] is True
    assert rows["grid.h5"]["provenance"] == "unknown"
    assert "grid.h5" in summary["probe_queue"]


def test_sas7bdat_magic(tmp_path):
    rows, _ = inventory(tmp_path, {"survey.sas7bdat": SAS_HEAD})
    assert rows["survey.sas7bdat"]["sniffed_format"] == "sas7bdat"
    assert rows["survey.sas7bdat"]["ext_matches_content"] is True
    # the old 4-byte guess no longer claims SAS
    assert di.sniff_head(b"\xd2\xd7N(rest") != "sas7bdat"


def test_empty_csv_flagged(tmp_path):
    rows, summary = inventory(tmp_path, {"empty.csv": b""})
    r = rows["empty.csv"]
    assert r["zero_bytes"] is True
    assert r["sniffed_format"] == "empty"
    assert r["provenance"] == "unknown"
    assert summary["zero_byte_files"] == ["empty.csv"]
    assert "empty.csv" not in summary["ext_mismatches"]


def test_name_hint_does_not_decide_provenance(tmp_path):
    rows, summary = inventory(tmp_path, {"sample_main.csv": b"id,y\n1,2\n",
                                         "sim_driver.do": b"set more off\n"})
    r = rows["sample_main.csv"]
    assert r["name_hint"] == "sample_"
    assert r["provenance"] == "unknown"
    assert "sample_main.csv" in summary["probe_queue"]
    assert rows["sim_driver.do"]["name_hint"] == "sim"
    assert rows["sim_driver.do"]["provenance"] == "not_data_or_text"
    assert "declared_synthetic_by_name" not in summary["by_provenance"]


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="no symlinks")
def test_symlinks_recorded(tmp_path):
    dep = tmp_path / "deposit"
    (dep / "real").mkdir(parents=True)
    (dep / "real/a.csv").write_bytes(b"x,y\n1,2\n")
    os.symlink("real/a.csv", dep / "link.csv")
    os.symlink("real", dep / "linkdir")
    os.symlink("nowhere.csv", dep / "dangling.csv")
    out = tmp_path / "inv.json"
    subprocess.run([sys.executable, str(SCRIPT), str(dep), "--out", str(out)],
                   check=True, capture_output=True)
    rows = {r["path"]: r for r in json.loads(out.read_text())["files"]}
    assert rows["link.csv"]["symlink_target"] == "real/a.csv"
    assert rows["link.csv"]["sha256"] == rows["real/a.csv"]["sha256"]
    assert rows["linkdir"]["sniffed_format"] == "symlink-dir"
    assert "linkdir/a.csv" not in rows          # not descended
    assert rows["dangling.csv"]["sniffed_format"] == "broken-symlink"
    assert rows["dangling.csv"]["provenance"] == "unknown"
