#!/usr/bin/env python3
"""deposit_inventory.py — per-file inventory of a replication deposit.

Emits review/deposit-inventory.json: every file hashed, sized, magic-sniffed
against its extension, and given a provisional provenance class. Provenance is
assigned from CONTENT signals only; a filename suffix is recorded but never
decides, and neither does a name substring ("sample_", "sim", "toy" …) — those
are recorded as `name_hint` and nothing more. Every data-bearing file lands in
`unknown` — the queue a human/agent must schema-probe before the deposit may
be declared synthetic, restricted, or genuine. Zero-byte files are flagged
(`zero_bytes`, summary `zero_byte_files`).

Usage:
    python3 deposit_inventory.py <deposit_dir> --out review/deposit-inventory.json

Stdlib only. Streaming sha256. Symlinks: a link to a file is followed and
hashed as its target (row carries `symlink_target`); a link to a directory
is NOT descended (os.walk default) and a dangling link cannot be read —
both are recorded as rows (`symlink-dir` / `broken-symlink`) in the probe
queue, never silently dropped.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import zipfile

MAGIC = [
    (b"<stata_dta>", "stata-dta-117+"),
    (b"PK\x03\x04", "zip-container"),          # xlsx/docx/zip all land here
    (b"%PDF", "pdf"),
    (b"\x1f\x8b", "gzip"),
    (b"BZh", "bzip2"),
    (b"\xfd7zXZ\x00", "xz"),
    (b"Rdata", "rdata"), (b"RDX", "rdata"),
    (b"RDA2\n", "rdata"), (b"RDA3\n", "rdata"),   # ascii save()
    (b"RDB2\n", "rdata"), (b"RDB3\n", "rdata"),   # native-binary save()
    (b"SQLite format 3", "sqlite"),
    (b"\x89HDF", "hdf5"),
    # SAS7BDAT: 12 NUL bytes then a fixed 20-byte signature
    (b"\x00" * 12 + bytes.fromhex("c2ea8160b31411cfbd92080009c7318c181f1011"),
     "sas7bdat"),
    (b"PAR1", "parquet"),
]
# save()/saveRDS() compress by default — gzip, bzip2, xz, or raw RData
RDATA_FORMATS = {"rdata", "gzip", "bzip2", "xz"}

# recorded as `name_hint` only — a name never decides provenance
SYNTHETIC_NAME_HINTS = ("fake", "sim", "synthetic", "mock", "dummy", "sample_",
                        "placeholder", "toy")
ARCHIVE_EXTS = {"zip", "rar", "7z", "tar", "gz", "bz2"}
DOC_EXTS = {"pdf", "docx", "doc", "txt", "md", "rtf", "tex", "html",
            "htm", "log", "out", "json", "xml", "yaml",
            "yml", "do", "ado", "r", "py", "m", "jl", "sas", "ipynb",
            "sh", "bat", "lst", "smcl", "manifest"}
# data-bearing: a regression could `use` these — they need provenance before
# any deposit-level "synthetic/genuine" characterization
DATA_EXTS = {"dta", "tab", "dat", "raw", "dbf", "mat", "csv", "tsv",
             "xlsx", "xls", "sav", "por", "rds", "rda", "rdata", "feather",
             "parquet", "sqlite", "db", "sas7bdat", "xpt", "bin", "h5", "hdf5"}
DATA_FORMATS = {"stata-dta-117+", "stata-dta-legacy", "sas7bdat",
                "parquet", "sqlite", "rdata", "hdf5"}
TEXT_FORMATS = {"text", "text-legacy", "empty"}   # provenance: not binary data
OS_META_NAMES = {".ds_store", "thumbs.db", "desktop.ini", ".localized"}


def is_os_metadata(name, path):
    if name.lower() in OS_META_NAMES or name.startswith("._"):
        return True
    return "__MACOSX" in path.split(os.sep) or "__MACOSX/" in path


def sniff(path, nbytes=8192):
    try:
        with open(path, "rb") as f:
            head = f.read(nbytes)
    except OSError:
        return "unreadable", False
    return sniff_head(head), True


def ext_of(path):
    return os.path.splitext(path)[1].lower().lstrip(".")


def ext_match(ext, fmt):
    """Does the declared extension plausibly match the sniffed content?"""
    table = {
        "dta": {"stata-dta-117+", "stata-dta-legacy"},
        "xlsx": {"zip-container"}, "docx": {"zip-container"},
        "xlsm": {"zip-container"}, "pptx": {"zip-container"},
        "zip": {"zip-container"}, "jar": {"zip-container"},
        "pdf": {"pdf"}, "rdata": RDATA_FORMATS, "rda": RDATA_FORMATS, "rds": RDATA_FORMATS,
        "bz2": {"bzip2"}, "xz": {"xz"},
        "sqlite": {"sqlite"}, "db": {"sqlite", "binary-other"},
        "parquet": {"parquet"}, "sas7bdat": {"sas7bdat"},
        "gz": {"gzip"}, "h5": {"hdf5"}, "hdf5": {"hdf5"},
        "csv": {"text", "text-legacy"}, "tsv": {"text", "text-legacy"},
        "txt": {"text", "text-legacy"},
        "do": {"text", "text-legacy"}, "ado": {"text", "text-legacy"},
        "r": {"text", "text-legacy"}, "py": {"text", "text-legacy"},
        "m": {"text", "text-legacy"}, "jl": {"text", "text-legacy"},
        "sas": {"text", "text-legacy"},
        "json": {"text", "text-legacy"}, "xml": {"text", "text-legacy"},
        "md": {"text", "text-legacy"},
        "log": {"text", "text-legacy"}, "out": {"text", "text-legacy"},
        "tex": {"text", "text-legacy"},
        "sh": {"text", "text-legacy"}, "yaml": {"text", "text-legacy"},
        "yml": {"text", "text-legacy"},
        # binary under a text-claiming extension IS the mismatch worth flagging
        "tab": {"text", "text-legacy"},
    }
    # flag only known-format extensions; unknown exts (.bak, .eps) are not
    # mismatches. An empty file is flagged on its own (zero_bytes).
    return ext not in table or fmt in table[ext] or fmt == "empty"


def sha256_of(path, block=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(block)
            if not b:
                return h.hexdigest()
            h.update(b)


def name_hint(name):
    """Synthetic-sounding name substrings, recorded for the prober — never
    a provenance decision ("sim" also matches "simulation_results.dta")."""
    low = name.lower()
    hits = [h for h in SYNTHETIC_NAME_HINTS if h in low]
    return ",".join(hits) or None


def provisional_provenance(name, ext, fmt, path):
    if is_os_metadata(name, path):
        return "os_metadata"
    if fmt in DATA_FORMATS or ext in DATA_EXTS:
        return "unknown"   # data-bearing, whatever its name → probe queue
    if ext in ARCHIVE_EXTS or ext in DOC_EXTS or fmt in TEXT_FORMATS:
        return "not_data_or_text"
    return "unclassified_binary"


def inventory_zip_members(zpath, rel):
    """Enumerate members of a zip container as pseudo-rows.

    Members get first-bytes sniffing but no content hash (hashing would
    decompress the whole archive); the archive file itself is hashed as a
    normal row. Provenance heuristics run on member names + sniffed format.
    """
    rows = []
    try:
        with zipfile.ZipFile(zpath) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                name = info.filename
                ext = ext_of(name)
                try:
                    with zf.open(info) as f:
                        head = f.read(8192)
                    fmt = sniff_head(head)
                except Exception:
                    fmt = "unreadable"
                rows.append({
                    "path": rel + "::" + name,
                    "bytes": info.file_size,
                    "sha256": None,
                    "ext": ext,
                    "sniffed_format": fmt,
                    "ext_matches_content": ext_match(ext, fmt),
                    "mtime": "%04d-%02d-%02dT%02d:%02d:%02d" % info.date_time,
                    "provenance": provisional_provenance(os.path.basename(name), ext, fmt, name),
                    "name_hint": name_hint(os.path.basename(name)),
                    "zero_bytes": info.file_size == 0,
                    "archive_member": True,
                })
    except (zipfile.BadZipFile, OSError) as e:
        rows.append({"path": rel + "::[unreadable archive]",
                     "bytes": 0, "sha256": None, "ext": "", "sniffed_format": "error",
                     "ext_matches_content": True, "mtime": "", "provenance": "unknown",
                     "archive_member": True, "error": str(e)})
    return rows


def is_legacy_dta(head):
    """Stata formats 104–115 open with a 4-byte header: ds_format (release
    0x68–0x73), byteorder (1 = HILO, 2 = LOHI), filetype (always 1), and an
    `unused` byte. The unused byte is NOT tested: Stata's dta_113 spec
    lists it as 0x01, most files carry 0x00, and real deposits carry 0x77
    and 0xff there. A first-byte test alone mistakes "set more off",
    "rm(" and "region," for Stata files; bytes 1–2 rule text out."""
    return (len(head) >= 4 and 0x68 <= head[0] <= 0x73
            and head[1] in (1, 2) and head[2] == 1)


def sniff_head(head):
    if not head:
        return "empty"
    for sig, fmt in MAGIC:
        if head.startswith(sig):
            return fmt
    if is_legacy_dta(head):
        return "stata-dta-legacy"
    if b"\x00" in head:
        return "binary-other"
    try:
        head.decode("utf-8")
        return "text"
    except UnicodeDecodeError:
        # no NUL but not UTF-8 — legacy/foreign-encoded text (Shift-JIS,
        # Latin-1), i.e. a document or raw corpus, not a binary dataset
        return "text-legacy"


def link_row(p, rel, name, fmt, err):
    """A row for an entry that cannot be hashed — a dangling link or a
    linked directory. Recorded (probe queue), never silently dropped."""
    row = {"path": rel, "bytes": None, "sha256": None, "ext": ext_of(name),
           "sniffed_format": fmt, "ext_matches_content": True, "mtime": "",
           "provenance": "unknown", "name_hint": name_hint(name),
           "zero_bytes": False}
    if os.path.islink(p):
        row["symlink_target"] = os.readlink(p)
    if err is not None:
        row["error"] = str(err)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deposit")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = []
    for root, dirs, files in os.walk(args.deposit):
        dirs.sort()
        for d in dirs:   # os.walk lists but never descends linked dirs
            dp = os.path.join(root, d)
            if os.path.islink(dp):
                rows.append(link_row(dp, os.path.relpath(dp, args.deposit), d,
                                     "symlink-dir", None))
        for fn in sorted(files):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, args.deposit)
            try:
                st = os.stat(p)
            except OSError as e:     # dangling symlink or unreadable entry
                rows.append(link_row(p, rel, fn, "broken-symlink"
                                     if os.path.islink(p) else "unreadable", e))
                continue
            ext = ext_of(fn)
            fmt, _ = sniff(p)
            row = {
                "path": rel,
                "bytes": st.st_size,
                "sha256": sha256_of(p),
                "ext": ext,
                "sniffed_format": fmt,
                "ext_matches_content": ext_match(ext, fmt),
                "mtime": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                "provenance": provisional_provenance(fn, ext, fmt, rel),
                "name_hint": name_hint(fn),
                "zero_bytes": st.st_size == 0,
            }
            if os.path.islink(p):
                row["symlink_target"] = os.readlink(p)
            rows.append(row)
            if fmt == "zip-container" and ext == "zip":
                rows.extend(inventory_zip_members(p, rel))

    summary = {
        "deposit": os.path.abspath(args.deposit),
        "files": len(rows),
        "by_format": {},
        "by_provenance": {},
        "ext_mismatches": [r["path"] for r in rows
                           if not r["ext_matches_content"]
                           and r["provenance"] != "os_metadata"],
        "probe_queue": [r["path"] for r in rows if r["provenance"] == "unknown"],
        "zero_byte_files": [r["path"] for r in rows if r.get("zero_bytes")],
    }
    for r in rows:
        summary["by_format"][r["sniffed_format"]] = summary["by_format"].get(r["sniffed_format"], 0) + 1
        summary["by_provenance"][r["provenance"]] = summary["by_provenance"].get(r["provenance"], 0) + 1

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"summary": summary, "files": rows}, f, indent=1)
    print(f"{len(rows)} files -> {args.out}")
    print(f"probe_queue: {len(summary['probe_queue'])}  ext_mismatches: {len(summary['ext_mismatches'])}"
          f"  zero_byte: {len(summary['zero_byte_files'])}")


if __name__ == "__main__":
    sys.exit(main())
