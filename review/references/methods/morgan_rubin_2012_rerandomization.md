# Rerandomization and covariate balance — Morgan & Rubin (2012)

Working distillation of Kari Lock Morgan and Donald B. Rubin,
"Rerandomization to Improve Covariate Balance in Experiments," *Annals of
Statistics* 40(2) (2012), 1263–1282 — the published article (open access,
Project Euclid). Verified against the published PDF (not distributed with the skill);
cites below are to printed page/section.

Use in this battery:

1. `experiment-diagnostics` — the randomization-inference and balance rows:
   what a "balanced" randomization commits the analyst to, and what an
   unaccounted rerandomization does to the reported inference.
2. Any design where treatment was assigned with balance checks —
   stratified, paired, or rerandomized assignment changes the sampling
   distribution the analyst must randomize over.

## 1. The procedure and its pedigree

Rerandomization (§1, pp. 1263–1264): specify an explicit imbalance
criterion in advance; if the realized assignment fails it, discard and
re-draw. The idea is Fisher's — his 1926 warning that pure randomization
can deliver badly unbalanced allocations is quoted in the paper — and it
has been common practice (e.g. in clinical trials and survey sampling)
long before formal analysis. The paper's contribution is the distribution
theory: what rerandomization does to the estimator's sampling
distribution.

## 2. The key result: tighter but not normal

- With balance checked on covariates via Mahalanobis distance (the
  natural multivariate criterion), rerandomization yields an estimator
  whose sampling distribution is more concentrated around the true
  effect than under pure randomization — but **not Gaussian**
  (pp. 1264–1266, §§2–3). That Gaussian-theory analysis is "no longer
  valid" is the critics' objection, which MR answer (pp. 1264–1265):
  unadjusted analysis becomes conservative, and randomization inference
  stays valid once the rerandomization is accounted for.
- Consequence for the audit: an experiment that rerandomized (or
  stratified/paired to the same effect) and then analyzes with
  pure-randomization theory gets *conservative* inference — tests reject
  true nulls less often than nominal, CIs cover more than nominal
  (pp. 1264–1265). That is the rare safe direction: the machinery
  under-rejects. The fix is randomization inference over the *actual*
  restricted assignment set (their §4 builds CIs by inverting the
  restricted randomization distribution).

## 3. Review-side implications

- **Check the assignment mechanism, not just the balance table.** A
  "randomized" design that screened allocations for balance before
  enrollment is a rerandomized design; its randomization inference must
  permute assignments subject to the same screen. Young-style
  permutation over unrestricted assignments is wrong in the safe
  direction — but it is still the wrong distribution.
- **Balance was the design's job, not the analysis's.** If the paper
  presents balance as a diagnostic that happened to pass, but the
  allocation was actually screened, the inference machinery must honor
  the screen. If balance was achieved ex post by dropping units, that is
  selection, not rerandomization — route to the attrition/selection rows.
- **Re-randomization vs stratification**: the same machinery covers
  blocked/paired designs — any restriction on the assignment set changes
  the null distribution; enumerate or simulate over the restricted set.

## 4. Reviewer checklist

- Was the assignment screened? (Protocol, registration, or code — not
  the prose claim "randomized.")
- If yes: RI must permute within the screened assignment set; report the
  screen definition.
- If the paper used pure-randomization SEs on a screened design: the
  reported inference is conservative — note it, but do not let it stand
  as the audit's inference either.
