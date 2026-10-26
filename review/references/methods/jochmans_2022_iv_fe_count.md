# IV estimators of fixed-effect count models — Jochmans (2022)

Working distillation of Koen Jochmans, "Bias in Instrumental-Variable
Estimators of Fixed-Effect Models for Count Data," *Economics Letters*
212 (2022): 110318. The version audited is the **working paper**
(`Jochmans_2022_IV_FixedEffects_CountData_EL.pdf`, not distributed with the skill; TSE WP 21-1276, October
2021 version) — cite by section, verify against the published version
before quoting numbers.

Use in this battery:

1. **The conditional check in `scale-sensitive-diagnostics`** — when a
   review proposes IV-Poisson with unit fixed effects as the honest
   alternative to an asinh spec, this is the caveat that must travel
   with the proposal (§1).

## 1. What fails and why (abstract; §§1–2)

The pseudo-Poisson estimator's celebrated immunity to the incidental-
parameters problem does *not* carry over to its instrumental-variable
generalizations. Fixed-effect versions of the two standard IV count-data
estimators —

- **Mullahy (1997)**: orthogonality on E[Y_it exp(−x_it′β) − 1 | α_i, z_it]
- **Windmeijer–Santos Silva (1997)**: orthogonality on
  E[Y_it − α_i exp(x_it′β) | z_it] / α_i

— are **inconsistent under conventional fixed-T asymptotics**, and
asymptotically biased even in long panels; the within-transformation
does not purge the FE consistently because the moment conditions are
nonlinear in the parameters the FE enters. The paper derives the
required bias corrections for long-panel inference and shows them to
work in simulations.

## 2. What still works

In the setting underlying Mullahy's approach, **consistent short-panel
estimation is possible via a differencing strategy** (Wooldridge 1997;
Windmeijer 2000) — but that is a different estimator with its own moment
conditions, not the FE-IV-Poisson practitioners actually run
(`ivpoisson`/`ivppml` with unit FE or dummies, `reghdfe`-style PPML-IV
implementations that assume FE soak up the individual effects cleanly).

## Reviewer checklist

- When the fragility battery proposes "PPML-IV with unit FE" as the
  zeros-tolerant alternative to a log-like specification, the proposal
  must carry this caveat: the estimator is inconsistent under fixed-T
  in general; flag whether the panel is long (bias correction needed)
  or whether a differencing-based estimator is the defensible route.
- If the paper itself uses FE-IV-Poisson silently — a real habit (the
  paper notes published uses with no incidental-parameters discussion) —
  treat fixed-T inconsistency as a first-order concern, not a technical
  footnote.
- Adjacent cribs: `chen_roth_2024_logs_with_zeros.md` (the estimand
  problem this alternative is meant to escape);
  `spurious_space_time_unified_guide.md` (the FE-in-nonlinear-models
  incidental-parameters background).
