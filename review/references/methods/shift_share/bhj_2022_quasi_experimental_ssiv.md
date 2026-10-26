# Quasi-experimental shift-share designs — Borusyak, Hull & Jaravel (2022)

Working distillation of Kirill Borusyak, Peter Hull and Xavier Jaravel,
"Quasi-Experimental Shift-Share Research Designs," *Review of Economic
Studies* 89(1) (2022): 181–213 — the published article (DOI
10.1093/restud/rdab030), not a working paper. Verified against the
published PDF (`BHJ_2022_ReStud.pdf`, not distributed); printed page =
PDF page + 180 (PDF
p.1 = printed p. 181). The online appendix is `BHJ_2022_ReStud_appendix.pdf`;
`w24997.pdf` is the earlier NBER working-paper version — cite the ReStud
version. All cites are to the printed page.

Use in this battery:

1. **The shock-exogeneity claim** behind every "quasi-experimental"
   shift-share — what must be exogenous, and what may be endogenous (§1).
2. **The Col 1 → 2 → 3 specification walk** in `shift-share-diagnostics`
   — the incomplete-shares control and the period-interaction control,
   why they are different corrections (§§2–3).
3. **Shock-level balance/falsification** — the unit-level balance table
   answers a different question (§4).

## 1. The identifying assumption (§§2–3, pp. 184–195)

Instrument z_ℓ = Σ_s s_ℓs g_s: exposure shares s_ℓs times shocks g_s.
BHJ's framework takes **the shocks g_s as quasi-randomly assigned**
(conditional on observables and fixed effects); the exposure shares are
allowed to be endogenous — this is the point that distinguishes it from
the shares-as-instruments reading (see `gpss_2020_bartik_instrument.md`).

- Equivalence result (§2): orthogonality of the shift-share instrument
  and the residual *is* orthogonality of the shocks to an
  exposure-weighted residual — the identifying content lives entirely at
  shock level.
- Asymptotics: consistency and inference under **many shocks** (s → ∞),
  not many locations. A paper with 700 locations and 40 industries has a
  40-observation natural experiment.
- **Shock-level confounders** (Assumption 3 / §4.1): if shocks are
  exogenous only conditional on shock-level observables q_s, it suffices
  to control for the *exposure-weighted sum* of those confounders,
  Σ_s s_ℓs q_s — not for the confounders at location level.

## 2. Incomplete shares (§4.2, pp. 196–199)

Complete shares: Σ_s s_ℓs = 1 (or constant) for every ℓ. When the share
sum S̄_ℓ = Σ_s s_ℓs varies across observations, the instrument is
contaminated: z_ℓ also loads on S̄_ℓ itself (the exposure-weighted sum of
a *constant* shock), so the instrument reflects exposure level, not just
shock variation.

**Fix: control for S̄_ℓ** — the sum of exposure shares enters the
regression as a regressor (equivalently, it is the exposure-weighted sum
of the constant shock and belongs in the control set under Assumption 3).
First check whether shares are complete on the estimation sample — the
fix applies only when they are not.

## 3. Panel data: the period interaction (§4.3, pp. 199–201)

- Shares complete within each period → period fixed effects isolate
  within-period shock variation (only shocks varying over time identify).
- Shares **incomplete** → period FEs must be **interacted with S̄_ℓt**:
  the period-interacted sum-of-shares is the control that restores
  within-period isolation (their fn 31 and §4.3). This is the
  consequential correction, not the cheap one.

## 4. Specification tests (§5, pp. 201–206)

- **Shock-level balance**: regress the shocks g_s (weighted by average
  exposure) on shock-level observables — under the design they should be
  unrelated. A location-level balance table tests share exogeneity — a
  different, Goldsmith-Pinkham-style design claim.
- **Exposure-robust standard errors**: clustered at the level that makes
  residual exposure shares independent; implemented in the application.
- First-stage at the shock level; the effective shock count governs
  power, not the location count.

## 5. The canonical application (§6, Table 4, pp. 206–212)

Re-estimating the methods paper's canonical industry-shift regression:

| Spec | β̂ | SE | Correction |
|---|---|---|---|
| Col 1 (as published form) | −0.596 | 0.114 | exposure-robust SE |
| Col 2 | −0.489 | 0.100 | + sum-of-shares S̄_t control (incomplete-shares fix) |
| Col 3 | −0.267 | 0.099 | + period-interacted share controls (within-period isolation) |

The instrument uses lagged industry shares whose sum S̄_ℓt
varies across locations and periods → incomplete shares (p. 206). The
cheap Col-2 fix moves the coefficient modestly; the Col-3
period-interaction correction more than halves it (Table 4, pp.
208–209). A paper that runs only the sum-of-shares control has not run
the walk. Their fn 47 (p. 208): conventional state-clustered SEs are
generally too low; AKM SEs are slightly larger than their
exposure-robust SEs in most columns; **null-imposed shock-level LM
confidence intervals are 30–50% wider, asymmetrically** (more on the
left — much larger negative effects are not rejected).

## Reviewer checklist

- Ask first: are shares complete on the estimation sample? If not, the
  Col-1 instrument is already mis-specified.
- Run the whole Col 1→2→3 walk, not just the share-sum control; report
  each step with exposure-robust SEs.
- Shock-level balance: regress g_s on shock observables, exposure-
  weighted. Do not accept location-level balance as the answer.
- "Shocks are plausibly exogenous" claims are claims about a shock-level
  assignment process — make the paper name it.
- When shares are geographically clustered and exposure itself is
  non-random, see `borusyak_hull_2020_nonrandom_exposure.md` — the
  recentering fix; for shock-level inference see
  `akm_2019_shift_share_inference.md`.
