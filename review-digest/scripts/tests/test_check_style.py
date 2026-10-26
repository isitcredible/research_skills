"""check_style.py — a recorded keep binds to the whole rendered line, not
to the first 150 characters of it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ai-sweep" / "scripts"))

import check_style as cs
from ai_sweep import kept_keep, load_keeps


def test_keep_past_150_characters_clears_its_flag(tmp_path):
    lead = "The classifier is described in the paper at some length " * 3
    quote = '"de facto replicating the work of several judges marking each post"'
    led = tmp_path / "ISSUES.md"
    led.write_text(f"## Issues\n\n{lead}{quote} (p. 1713).\n")
    (tmp_path / "ISSUES.keeps.md").write_text(
        "- `de facto replicating the work of several judges` — the paper's own words, quoted\n")
    flags = cs.verif_flags(str(led))
    assert flags, "the quote should flag before the keep is applied"
    keeps = load_keeps(str(led))
    assert all(kept_keep(full, keeps) for _, _, full in flags)
