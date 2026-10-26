# Placebo tests as design audits — Eggers, Tuñón & Dafoe (2024) + Hartman & Hidalgo (2018)

Working distillation of the two papers that turn "run a placebo test"
into a checkable procedure. Section references are to the disk PDFs.

- **Eggers, Tuñón & Dafoe, "Placebo Tests for Causal Inference",
  *American Journal of Political Science*** (published version,
  `Eggers_Tunon_Dafoe_2024_PlaceboTests_AJPS.pdf`, not distributed with
  the skill).
- **Hartman & Hidalgo, "An Equivalence Approach to Balance and Placebo
  Tests", *AJPS* 62(4) (2018): 991–1003** — accepted manuscript
  (`Hartman_Hidalgo_2018_Equivalence_AJPS.pdf`, not distributed with the
  skill).

## 1. ETD: the typology and the hidden assumptions

A placebo test alters **one component** of the research design — outcome,
treatment, or population — to produce a comparison that should be null
if the design's assumptions hold (§II–III). The four-part typology:

- **Outcome placebos**: regress the treatment on an outcome it cannot
  affect (pre-treatment outcome; an outcome the treatment mechanism
  excludes).
- **Treatment placebos**: replace the treatment with a fake version
  (a different policy event; a permutation of the assignment).
- **Population placebos**: apply the design where the treatment
  cannot operate.
- Bias assumption vs. distributional-assumption tests split the
  typology by *what* is tested.

The load-bearing finding (§IV): **informative placebos require extra
assumptions, and those assumptions can be as strong as the design
itself.** A placebo result is uninformative when the placebo shares
only some of the original design's vulnerabilities — a null placebo
"confirming" the design may just be a placebo insensitive to the
relevant violation. Their sharper warning: the assumptions needed for
an *informative* placebo can instead justify a procedure that **relaxes
the original assumption rather than testing it** — sometimes the right
response to a weak placebo is a different estimator.

**Review operationalization**: for each placebo a paper reports,
name (a) which design component was altered, (b) which assumption the
test targets, (c) whether the placebo is actually *sensitive* to the
relevant violation (fidelity), and (d) whether the supporting
assumptions that make it informative are stated. A placebo with no
stated sensitivity argument is decoration, not evidence. Pairs with the
placebo-fidelity audit in `shift-share-diagnostics` — a placebo drawn
at the wrong shock level fails ETD's component-alteration logic (it
changes the design, not just the input).

## 2. HH: equivalence testing fixes the backwards null

Conventional balance/placebo tests have the null backwards
(§"Tests of Design"): failing to reject "no difference" is treated as
evidence FOR the design, but non-rejection is weak evidence —
especially underpowered. The remedy (§"Mechanics of an Equivalence
Test"): flip the null — H0 is "difference ≥ ε" for a substantively
chosen equivalence bound ε, and the researcher must *reject it* with a
TOST (two one-sided tests) or equivalent CI check. The choice of ε
forces substantive judgment about what balance matters.

**Review operationalization**: any "covariates are balanced (p > 0.1)"
or "placebo null (p > 0.1)" claim gets flagged — non-rejection ≠
confirmation. The bar is a stated equivalence region and a rejection of
the difference null, or at minimum an honest power statement. Combined
with ETD: ETD tells you whether the placebo can detect the failure
mode; HH tells you whether the *test* is structured to detect it.
