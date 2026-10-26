# Weak instruments: relative bias, size distortion — Stock & Yogo (2002/2005)

Working distillation of James H. Stock and Motohiro Yogo, "Testing for
Weak Instruments in Linear IV Regression." This crib was verified
against **the NBER technical working paper, TWP 284**
(`Stock_Yogo_2002_NBER_TWP284_TestingWeakInstrumentsIV.pdf`, not
distributed). The published version is the chapter in *Identification and
Inference for Econometric Models: Essays in Honor of Thomas
Rothenberg* (Andrews & Stock eds., 2005) — the canonical critical-value
tables. Table numbering matches between the two, but verify any
specific cell against the published chapter before quoting. Cites below
are to the TWP's tables/sections.

Use in this battery:

1. **The weak-IV row of `iv-diagnostics`** for i.i.d.-error designs —
   what the Stock–Yogo critical values are tests *of* (§§1–2), and why
   "F > 10" is not a general rule (§3).
2. **Estimator choice under weak IV** — why LIML/Fuller-k enter the
   fragility assessment (§4).
3. **Boundary**: SY assume i.i.d./homoskedastic errors; under robust,
   clustered, or HAC inference use Montiel Olea–Pflueger — see
   `montiel_olea_pflueger_2013_weak_iv.md`.

## 1. Two different definitions of "weak" (§3, TWP §§2–4)

SY define weak instruments two ways, with **separate critical-value
tables** — a first-stage F must be judged against the right one:

- **Maximal relative bias** (Table 1): the IV estimator's bias relative
  to the OLS bias, worst-case over the correlation between the
  first-stage and second-stage errors. Thresholds b ∈ {.05, .10, .20,
  .30}. For n = 1 endogenous regressor the table begins at K2 = 3
  instruments (K2 = 3: CVs 13.91 / 9.08 / 6.46 / 5.39 for b =
  .05/.10/.20/.30).
- **Maximal Wald size distortion** (Table 2, TSLS): actual size of a
  nominal 5% Wald test, thresholds r ∈ {.10, .15, .20, .25}. For n = 1,
  r = .15: K2 = 1 → 8.96, K2 = 2 → 11.59, K2 = 3 → 12.83, rising
  steadily in K2; the r = .10 column is far larger throughout.

Critical values grow with both K2 (number of instruments) and n
(endogenous regressors). The scalar object underlying everything is
the **concentration parameter** μ²/n — the population first-stage F —
scaled into the mineval test statistic.

## 2. Where "F > 10" comes from and why it misleads (§5)

The b = .10 relative-bias column for n = 1 stays in the 9–11.5 range
across K2 — the paper's text: the 5% critical value for the
relative-bias test with b = .10 is *approximately* 11 for all K2 (n=1).
That single column is the entire basis of the folklore rule. It does
not cover:

- **size distortion** — under the r = .10 column the required F is far
  above 10 for moderate K2;
- **n > 1 endogenous regressors** — the multivariate (mineval) test and
  larger CVs;
- **non-i.i.d. errors** — the tables are computed under homoskedastic
  normality; under clustering nothing in them applies (use MOP);
- **just-identified IV** — K2 = 1 has no bias-table entry; the
  just-ID 2SLS median-bias problem is a different object.

## 3. Estimator choice under weak instruments (§4, TWP)

- TSLS bias does **not** vanish under many-weak-instrument asymptotics;
  it tends to the OLS bias — weak instruments don't just add noise,
  they import the endogeneity.
- **LIML and Fuller-k** are approximately median-unbiased in the same
  limit (maximal relative bias ≈ 0 for LIML under many-weak-IV
  asymptotics) — with their own size CVs (Tables 3–4). LIML/Fuller is
  the more robust estimator when K2 is large and instruments weak; its
  trade-off is thicker-tailed dispersion.
- Pretesting on the first-stage F and then running ordinary Wald
  inference is not a fix: it neither controls bias nor size; the
  remedy is a weak-IV-robust confidence set (Anderson–Rubin, CLR),
  not a pass/fail F screen.

## Reviewer checklist

- Match the printed F to the error model: i.i.d. → Cragg–Donald against
  SY tables; robust/clustered → the MOP effective F against MOP critical
  values (the effective F equals the robust F only when K = 1), with
  one endogenous regressor; with several, Lewis–Mertens.
  `ivreg2`'s `e(widstat)` is CD without `vce`, KP under
  `robust`/`cluster()`.
- Name which SY question the paper's check answers: bias (Table 1) or
  size (Table 2), and whether b/r, n, K2 in the table match the spec.
- "F > 10" quoted for a many-instrument or clustered spec is a finding
  in itself, not a defense.
- Still demand the weak-IV-robust CI — AR or CLR reported beside the
  Wald interval. A passing F does not substitute for it.
