# Type S and Type M errors — Gelman & Carlin (2014)

Working distillation of Andrew Gelman & John Carlin, "Beyond Power
Calculations: Assessing Type S (Sign) and Type M (Magnitude) Errors,"
*Perspectives on Psychological Science* 9(6): 641–651. Verified against
the final manuscript (`Gelman_Carlin_2014_beyond_power_calculations.pdf`,
not distributed): "To appear in Perspectives on Psychological Science" on
the last page — text matches the published article; cite the journal
version, navigate by the manuscript's page numbers.

## The two error rates (§2, pp. 5–7)

Given a design — postulated true effect D and standard error s — that
declares estimates significant when |estimate| > 1.96·s:

- **Power** = 1 − Φ(1.96 − D/s) + Φ(−1.96 − D/s).
- **Type S error rate** = P(estimate has the wrong sign | significant)
  = Φ(−1.96 − D/s) / power (normal case).
- **Exaggeration ratio (expected Type M error)** =
  E[|estimate| / |D| | significant] — computed by simulation of the
  sampling distribution truncated above the significance threshold.

Their `retrodesign()` R function takes (D, s, α, df, n.sims) and returns
power, Type S rate, and exaggeration ratio. The retrospective use —
running the *completed* study's own s against a plausible D from outside
the data — is the review application: the authors' significant estimate
is not evidence for D.

## Benchmarks

- 80% power at two-sided α = .05 → Type S ≈ 1.2×10⁻⁶, exaggeration ratio
  1.12. High power is safe; the machinery matters exactly where designs
  are noisy.
- Kanazawa example (§3.1): estimate 8 pp, p = .015 → SE = 3.3%; the
  literature supports true differences well under 1 pp. Design analysis
  (Table 1): true D = 0.1 pp → Type S 46%, exaggeration ratio **77**;
  D = 0.3 pp → ~40%, **25**; D = 1.0 pp → 19%, **8**. An estimate
  selected by significance in a noisy design is expected to be far too
  large and often the wrong sign.

## Uses in the review skill

- `code-and-data` (selection-on-significance
  inflation): the formal machinery behind "a significant estimate from a
  noisy design is biased upward in expectation." The MDE comparison the
  check asks for is a retrospective Type M calculation against a
  plausible D.
- The **Edlin factor** the same check names is Aaron Edlin's informal
  heuristic — reported effect ÷ largest plausible effect; no published
  paper. Its sources are Gelman's blog posts ("How large is the
  underlying coefficient? An application of the Edlin factor,"
  2023-04-24; "The Edlin factor strikes again," 2025-08-19 — archive
  `20230424144712_*` / `20250820072138_*`). This paper is the formal
  version of the same idea.
- `claims` informative-null framing and the main `SKILL.md`
  sampling-vs-misspecification note: significance adds selection, not
  just noise.

Economics-side evidence for the same phenomenon: Ioannidis, Stanley &
Doucouliagos (2017), `ioannidis_stanley_doucouliagos_2017_power_of_bias.md`.
