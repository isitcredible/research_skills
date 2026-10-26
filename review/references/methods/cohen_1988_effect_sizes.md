# Effect sizes and power — Cohen (1988)

Working distillation of Jacob Cohen, *Statistical Power Analysis for the
Behavioral Sciences*, 2nd ed. (Erlbaum, 1988). Verified against a
579-page scan of the 2nd edition (not distributed); in that scan the
PDF page is the printed page plus roughly +12 to +18 (the offset drifts
across unnumbered table pages — navigate by the running header). All
cites below are to the printed section/page.

Two uses in this battery:

1. **The standardized effect size for the practical-magnitude dimension.**
   Pick the index the test dictates from the table below; always state the
   index, the denominator, and the level at which the regressor varies.
2. **The power/MDE machinery** wherever a stage asks "could this design
   have detected the effect" — few-cluster checks, null results, the
   informative-null branch in `claims`.

## The four-parameter framework (§1.5, p. 14)

Power, significance criterion α, sample size n, and effect size ES are
locked together: any three determine the fourth. The direction a review
almost always needs is **MDE** — given α, effective n/df, and a stated
power, solve for the smallest ES the test could detect. Convention:
power .80 at two-tailed α = .05, which implies a β/α = .20/.05 = 4:1
seriousness trade-off (§1.2, p. 4–5; §11.2, p. 531).

Compute with software, not the printed tables: R `pwr` (`pwr.t.test`,
`pwr.r.test`, `pwr.2p.test`, `pwr.f2.test`, `pwr.chisq.test`) or `pwrss`;
Stata `power`; Python `statsmodels.stats.power`. State α, tails,
df/effective n, and which ES index.

Noncentrality parameters the software solves:

- two-sample t, total N split evenly: δ = d·√N / 2 (per-group n: δ = d·√(n/2))
- paired / one-sample t: δ = d·√n, d using the SD of the difference scores
- ANOVA / multiple-regression F: λ = f²(u + v + 1), u = numerator df,
  v = denominator df (9.3.1)
- chi-square on N: λ = w²·N

## ES index by test family

| Test / design | Index | Definition | small / med / large |
|---|---|---|---|
| Two independent means | d | \|m₁−m₂\| / σ, σ = pooled within-population SD | .20 / .50 / .80 |
| Paired or one-sample mean | d | mean of difference scores / σ of difference scores | .20 / .50 / .80 |
| Product-moment correlation | r | r itself | .10 / .30 / .50 |
| Two independent r's | q | z′₁ − z′₂ (Fisher z transform) | .10 / .30 / .50 |
| Proportion vs .50, sign test | g | P − .50 | .05 / .15 / .25 |
| Two proportions | h | 2arcsin√P₁ − 2arcsin√P₂ | .20 / .50 / .80 |
| Chi-square / contingency | w | √Σ(P₁−P₀)²/P₀; in a table w = √(χ²/N) (= φ in 2×2; Cramér's φ′ = w/√(min(r−1,k−1))) | .10 / .30 / .50 |
| ANOVA F on k means | f | σ of the k means / σ within populations | .10 / .25 / .40 |
| Regression set / subset | f² | R²/(1−R²) whole set; (R²_AB − R²_A)/(1 − R²_AB) for subset B given A | .02 / .15 / .35 |

Equivalences and conversions:

- **d ↔ point-biserial r** (equal-sized groups): r_pb = d / √(d² + 4);
  unequal p,q: r_pb = d / √(d² + 1/(pq)). d = .20/.50/.80 → r_pb =
  .100/.243/.371, r² = .010/.059/.138; the mean of the higher group
  exceeds .579/.691/.788 of the lower group (U₃, §2.2.3).
- **f ↔ d** for k = 2 means: d = 2f (§8.2.3). η² = f²/(1+f²): the f
  conventions map to η² = .0099 / .0588 / .138.
- **f² ↔ proportion of variance:** PV = f²/(1+f²) → .020/.130/.260 at the
  conventions; the implied R or partial R is .14/.36/.51. Cohen set the
  f² conventions deliberately *above* strict equivalence with the r
  conventions because regression models carry several predictors
  (§9.2.2, p. 412–413).
- **Single regressor in a fitted model:** partial R² = t²/(t² + df_resid),
  hence f² = t²/df_resid and partial r = t/√(t² + df_resid). A
  coefficient's d-analogue is β·SD(X)/σ_resid — a one-SD move in X
  shifts Y by that many residual SDs. Compute SD(X) at the level X
  actually varies (the battery's standing rule).
- **w shrinks with table size:** max w = √(min(r,k) − 1), so w = .30 is a
  weaker association in a 6×k table than a 2×2. Cramér's φ′ = w/√(min−1)
  rescales onto [0,1].

## Cohen's own caveats — the failure runs in both directions

- **Conventions are last-resort defaults, not verdicts.** "Recommended
  for use only when no better basis for estimating the ES index is
  available" (§2.2.3, p. 25); "a compromise that should be rejected when
  it seems unsuited to the substantive content" (§9.2.2, p. 414). Where
  the field supplies a benchmark — published effects, the outcome's own
  distribution, a realistic-dose counterfactual — it trumps the
  convention; the convention then serves only as an absolute-magnitude
  yardstick.
- **"Small" ≠ unimportant.** Conventions characterize absolute
  magnitude, not substantive meaning: "the meaning of any given ES is,
  in the final analysis, a function of the context in which it is
  embedded" (§11.2, p. 535). Abelson's paradox: batting skill explains
  0.3% of the variance in a single at-bat and is nonetheless real and
  consequential, because effects cumulate. Rosenthal–Rubin's BESD:
  r = .30 — "only 9% of the variance" — is a survival rate of 35→65%.
  Never kill a result on a small ES label alone; and symmetrically, never
  let "statistically significant" launder a microscopic ES into a
  headline driver. State the number and its human-units translation;
  significance, magnitude, and variance share answer different
  questions.
- **ES is denominator-relative.** The σ in d and f is the
  *within-population* (error) SD: designs that strip out error variance
  (matching, within-unit comparison, covariates) raise the ES for the
  same raw difference (§1.4, p. 13–14). State the denominator — raw
  outcome SD, within-unit SD, and residual SD give different d's — and
  standardize at the level the regressor varies; a sub-unit σ
  manufactures a larger ES.
- **Measurement error attenuates.** Observed ES ≈ true ES × √reliability
  (§11.3). A small measured ES under a noisy outcome or regressor
  understates the true one — relevant both when a paper's "null" may be
  a measurement artifact and when its "robust small effect" is.
- **PV framings mislead both ways.** r² systematically understates how
  association reads to an observer (BESD, §11.2); under a common-cause
  structure the right proportion-of-variance figure can be r, not r²
  (Ozer 1985, cited §11.2). Report the index, not an impression of it.
- **Null ≠ no effect.** A null from an underpowered design is
  uninformative — that is the book's founding result. The
  informative-null question is MDE versus the plausible-effect range,
  not p > .05.

## Wiring

- **`code-and-data` battery — practical magnitude:** compute the
  design's index at the level the regressor varies; label index and
  denominator.
- **`code-and-data` battery — few-cluster / weak-power rows and every null
  family:** solve the design's MDE at stated power and read the interval
  against it.
- **`review` Rule 8 — informative nulls, ours or the paper's:** the branch is decided by
  MDE vs the plausible-effect range.
- **`claims` magnitude assessment:** conventions are the
  absolute-magnitude frame; domain benchmarks and the realistic-dose
  counterfactual carry the substantive verdict.
