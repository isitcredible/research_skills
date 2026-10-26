# Elasticities and the inverse hyperbolic sine — Bellemare & Wichman (2020)

Working distillation of Marc F. Bellemare and Casey J. Wichman,
"Elasticities and the Inverse Hyperbolic Sine Transformation," *Oxford
Bulletin of Economics and Statistics* 82(1) (2020): 50–61. The version
audited is the **author final version** (`Bellemare_Wichman_2020_IHS_Elasticities_OBES.pdf`,
not distributed with the skill; May 2019 — pagination differs from the published
version; cite by equation number, not page). Replication files:
`github.com/cjwichman/ihs`.

Use in this battery:

1. **The asinh-on-asinh row** of `scale-sensitive-diagnostics` — the
   exact elasticity formula and when the coefficient is *not* an
   elasticity (§§1–2).
2. **The data requirements** a paper citing IHS must meet — minimum
   input value and zeros share (§3).
3. **The dummy-regressor case** — the exact percentage effect, not
   exp(β̂) − 1 by reflex (§4).

## 1. The four specifications and their elasticities

Writing ỹ = asinh(y) and x̃ = asinh(x), with y = sinh(α̂ + β̂·… + ε̂)
recovered by the hyperbolic sine (their eqs. 3, 7, 12, 15–16):

| Specification | Implied elasticity ξ_yx | Large-value limit |
|---|---|---|
| y ~ x̃ | (β̂/y)·x/√(x² + 1) *(semi-elasticity: β̂·x/√(x² + 1))* | β̂/y for large x *(semi-elasticity: β̂)* |
| ỹ ~ x | β̂·x·√(y² + 1)/y | β̂x for large y |
| ỹ ~ x̃ | β̂·[√(y²+1)/y]·[x/√(x²+1)] | β̂ for large x **and** y |

The asinh–asinh coefficient β̂ approximates the log-log elasticity only
when *both* transformed variables take large values — asinh(t) ≈ ln(2t)
for large t but ≈ t near zero, so at small values the specification is
approximately linear–linear and β̂ is closer to a scaled slope than an
elasticity. Evaluate the exact formula at stated points (conventionally
the means); the correction can move the implied elasticity substantially
(e.g. in the IIG comment, an asinh–asinh coefficient of 1.65 implies an
elasticity of 1.35 at the sample means and 0.16 at the median).

A related consequence — asinh is *not* scale-invariant: rescaling y or
x changes the implied elasticity even though the same rescaling in a
linear–linear spec leaves it unchanged (their §2.5). Unit choices inside
the transform are estimand choices.

## 2. Zeros

Elasticities are undefined at zero (the formulas divide by y or put y
in √(y²+1)/y) — do not evaluate elasticity formulas at zeros; where
zeros are nontrivial, report the exact formulations and say which
evaluation points exclude them. For the deeper "the estimand itself is
unit-dependent under an extensive margin" result, see
`chen_roth_2024_logs_with_zeros.md` — that paper's Remark 6 reads BW's
"rescale so nonzeros are large" advice as *worsening* units dependence;
the constructive part of BW that survives is the exact elasticity
formulas and the data requirements below.

## 3. BW's data requirements (the rules papers cite but violate)

- Apply IHS for (semi-)elasticity estimation only when the **minimum
  nonzero absolute value of the input is ≥ ~10** — their calibration
  shows the elasticity stabilizes for k > 10, with virtually no change
  beyond it.
- IHS is questionable when **more than ~1/3 of the input's values are
  zeros**.
- Fitzgerald et al. (2026, `fitzgerald_etal_2026_loglike.md`) audit the
  citing literature: 99.8% of estimates they re-analyze violate the
  min ≥ 10 rule — a cited guideline is not a complied-with guideline.

## 4. Dummy regressors

For ỹ = α + βd + ε with d ∈ {0,1}: the exact percentage effect is
P̃ = [sinh(α̂+β̂+ε̂) − sinh(α̂+ε̂)]/sinh(α̂+ε̂), which approaches
exp(β̂) − 1 only for large y; their preferred small-sample version
applies the Kennedy-type correction exp(β̂ − 0.5·Var̂(β̂)) − 1. Report
the exact transform-back, not a naked exp(β̂) − 1.

## Reviewer checklist

- asinh–asinh or asinh–levels spec read as an elasticity → compute the
  exact elasticity at named evaluation points (means and the median);
  report the gap between it and the quoted coefficient.
- Check the input distribution against BW's own rules (min ≥ 10;
  ≤ 1/3 zeros) before accepting "we used the standard IHS
  transformation" — and check whether zeros make any elasticity
  undefined regardless (Chen–Roth).
- The rescaling sweep applies to *both* sides: in an asinh–asinh spec,
  rescaling either variable moves the coefficient — run the 2-D grid.
