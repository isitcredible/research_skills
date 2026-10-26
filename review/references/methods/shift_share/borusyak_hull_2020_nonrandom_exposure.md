# Non-random exposure to exogenous shocks — Borusyak & Hull (2020/2023)

Working distillation of Kirill Borusyak and Peter Hull, "Non-Random
Exposure to Exogenous Shocks." This crib was verified against **the
NBER working paper, w27845** (`Borusyak_Hull_2020_NBER_w27845_NonrandomExposure.pdf`,
not distributed) — the published version is *Econometrica* 91(6) (2023):
2155–2185 and numbers may have moved; verify against the published
version before quoting any figure from it. Cites below are to the WP's
sections/pages.

Use in this battery:

1. **The non-random-exposure row** of `shift-share-diagnostics` — when
   exogenous shocks still produce biased estimates because *exposure* is
   non-random (§§1–2).
2. **The recentering fix** — construction of z̃_ℓ = z_ℓ − μ_ℓ and what
   it does and does not solve (§3).
3. **Shock-counterfactual randomization inference** — the RI procedure
   that handles "exposure clustering" and is weak-IV robust (§4).

## 1. The problem (§§1–2)

A shift-share-style instrument z_ℓ built from plausibly exogenous shocks
is still biased when *exposure* to the shocks is non-random: units
located near where shocks land accumulate high z_ℓ, and if that location
correlates with potential outcomes, E[z_ℓ·ε_ℓ] ≠ 0 even though the
shocks were random. Randomness of the shock is not enough — what matters
is whether the *realized assignment of shocks to exposed units* was
as-good-as-random. Canonical example (their application): China's
high-speed-rail construction produces a market-access instrument
mechanically concentrated in the centre of the country; places near
growing cities are differentially exposed whatever the shocks.

## 2. Shock counterfactuals (§3)

The framework formalizes the natural experiment: specify the **set of
counterfactual shock realizations** that "may as well have been
realized" — the assignment process. In a true experiment this is the
randomization protocol; in a natural experiment the researcher states
it (e.g., which rail upgrades could plausibly have been built where,
which sectors could have gotten which shock). This is the substantive
move: the counterfactual set IS the identifying assumption made
explicit.

## 3. Recentering (§§3–4)

Let μ_ℓ = E[z_ℓ over counterfactual draws of the shocks] — the expected
instrument for unit ℓ, computed by simulation. The **recentered
instrument** is

  z̃_ℓ = z_ℓ − μ_ℓ.

z̃_ℓ is mean-independent of the confounded component by construction:
units' different *expected* exposures are removed, leaving only the
chance deviation of realized from expected exposure. Equivalently,
controlling for μ_ℓ in the regression combines recentering with partialling
out residual variation. Under heterogeneous effects, recentered IV
identifies a **convex weighted average** of treatment effects (§4).

**What it does not do:** it needs the researcher to name the
counterfactual shock process. Permuting shocks across fixed share
geography is how μ_ℓ is built — μ_ℓ is the average instrument over the
permuted or counterfactual shocks (§3.3, eq. 8, WP pp. 15–16) — so the audit question is
whether the permutation class matches the assignment process (all
permutations only when shocks are exchangeable; within-cluster or
matched-group permutations otherwise, §3.3). Recentering fixes the point
estimate's bias; it is not primarily an inference fix.

## 4. Randomization inference over shock counterfactuals (§5)

The same counterfactual draws support RI: recompute the test statistic
under each counterfactual shock assignment to get its null distribution.

- **Exact under constant treatment effects**, with no restrictions on
  the unobservables.
- **Robust to weak instruments** (RI does not depend on first-stage
  strength).
- Solves **"exposure clustering"**: units are not independent when they
  share exposure to the same shocks; permuting at the shock level
  respects that dependence — the geographic/network-distance
  generalization of Conley-style clustering.

**Specification test** the paper uses: after recentering, z̃_ℓ should be
uncorrelated with predetermined observables (their Figure 1/§6: raw
market-access growth is geographically concentrated; recentered MA is
not, and passes RI spec tests against predetermined controls).

## 5. Applications (§§6–7)

- **China HSR market access** (employment effects): recentering removes
  the mechanical concentration of the instrument near growing centres;
  estimates change and RI CIs are reported.
- **Medicaid eligibility (ACA)**: incorporating non-random exposure
  variation *while recentering* isolates the same policy variation and
  *improves* first-stage power — recentering is not only a bias fix; it
  can sharpen the experiment.

## Reviewer checklist

- Exposure clustered geographically or along a network → suspect
  non-random exposure even when shocks are exogenous; a shuffle-the-
  shocks placebo is informative only if its permutation class matches
  the shock assignment process, and an unrecentered estimate is not
  cleared by placebo coefficients centred on zero.
- The fix requires a defensible counterfactual shock set — demand the
  paper state what could "as well have happened" before accepting a
  recentered estimate.
- Post-recentering spec test: z̃_ℓ vs predetermined controls — insist on
  seeing it.
- For the shock-exogeneity framework these instruments sit in, see
  `bhj_2022_quasi_experimental_ssiv.md`; for shock-level SEs, see
  `akm_2019_shift_share_inference.md`. The Borusyak (2025) *JEP*
  practical guide (`Borusyak_2025_PracticalGuide.pdf`) is the
  textbook-level summary of the whole program.
