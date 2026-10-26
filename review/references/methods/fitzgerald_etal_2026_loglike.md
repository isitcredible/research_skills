# Non-robustness in log-like specifications — Fitzgerald, Adema, Fiala, Kujansuu & Valenta (2026)

Working distillation of Jack Fitzgerald, Joop Adema, Lenka Fiala, Essi
Kujansuu and David Valenta, "Non-Robustness in Log-Like Specifications,"
I4R Discussion Paper 284 / MetaArXiv 2026 — **working paper** (audited:
the June 2026 MetaArXiv draft, `Fitzgerald_etal_2026_LogLike_I4Rdp284.pdf`,
not distributed with the skill;
under submission, no published version exists). Cite by section, not
page, until a published version lands.

Use in this battery:

1. **The rescaling sweep's extension to a hypothesis-test** — the
   "sweet spot" diagnostic: unit scale as an uncontrolled researcher
   degree of freedom (§1).
2. **The compliance check** — papers citing Bellemare–Wichman's data
   requirements while violating them (§2).
3. **The alternative-specification roster** — what to propose instead of
   a log-like transform (§3).

## 1. Scale as a multiple-testing problem (abstract; §§3–5)

Because test statistics in log-like specifications are scale-variant,
rescaling the input before transformation is a researcher degree of
freedom that can be (and empirically is) used to overfit significance:

- **Sweet spot**: 38% of the 46-paper sample's estimates sit where
  re-scaling either up *or* down shrinks the t-statistic — the published
  scale is a local maximum of significance, the signature of selection
  on the units axis.
- Significance conclusions change under modest specification changes
  for **14–37%** of estimates defending main claims.
- Statistically significant results are ~40% more frequent in this
  literature than in economics generally.
- Review use: run the rescaling sweep *in both directions* and locate
  the published scale on the |t|-vs-scale surface — at a sweet spot the
  estimate's significance is partly manufactured by the units choice.

## 2. The compliance record (§§2, 5–7)

- 99.8% of re-analyzed estimates log-transform a variable whose minimum
  non-zero |value| is below Bellemare–Wichman's ≥10 rule.
- 32% (38%) of transformed outcomes (exposures) are non-positive in over
  a third of observations — beyond BW's zeros-share caution.
- For 13% (41%) of transformed outcome (exposure) variables *all* values
  are strictly positive — no zeros, so the only reason for a log-like
  transform over plain logs is absent.
- Poisson alternatives were inestimable for 45% of sample estimates
  (non-convergence, negative outcomes) — an alternative is only an
  answer where it actually runs; say when it doesn't.

## 3. The harmonized alternatives (§8)

Their principle: recommend only methods with scale-invariant
coefficients and test statistics and minimal researcher DFs.

- **Normalized estimands** (Chen & Roth's term): re-express the
  estimand relative to a constant — the control-group mean E[Y(0)], a
  pre-treatment mean, a standard deviation, or an exogenous constant.
  Under a scale-equivariant specification the t-statistic is unchanged
  by normalization. Sign-flip caveat: normalizing by a mean that can be
  negative flips the sign of the relative effect — use a dispersion
  measure (SD) there instead. Dividing outcomes and treatments by unit
  means to express everything as percentage deviations from baseline
  (as in the IIG comment's county-mean normalization) is the panel
  instance: it tolerates zeros because nothing is logged.
- **Poisson QMLE** on the untransformed outcome: for binary treatments
  e^{β_Pois} − 1 is the effect as a share of the untreated mean —
  scale-invariant, zeros-native.
- **Quantile regression** (Liu & Kaplan 2025) for consistent
  intensive-margin logarithmic slopes; Stata `lzqreg`, R `lzrq`.

## Reviewer checklist

- Any load-bearing `asinh`/`ln(1+·)` spec → the two-direction rescaling
  sweep; a sweet-spot estimate (t shrinks both ways) is a
  selection-on-units finding, not a robustness curiosity.
- Check the input against the cited guidelines: min |value| ≥ 10,
  ≤ 1/3 zeros, and whether any non-positive values exist at all.
- When proposing the honest alternative, name it from the roster:
  normalized estimand / Poisson / quantile — and note when Poisson
  cannot be estimated (45% of the published record).
- Related but distinct cribs: `chen_roth_2024_logs_with_zeros.md` (the
  estimand-level result), `bellemare_wichman_2020_ihs_elasticities.md`
  (the elasticity formulas and data rules), `mcconnell_2024_forest_logs.md`
  (the DiD levels-vs-logs sign-flip).
