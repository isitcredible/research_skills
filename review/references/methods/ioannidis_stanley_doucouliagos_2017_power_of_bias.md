# Power and bias in economics research — Ioannidis, Stanley & Doucouliagos (2017)

Working distillation of John P. A. Ioannidis, T. D. Stanley & Hristos
Doucouliagos, "The Power of Bias in Economics Research," *The Economic
Journal* 127 (October): F236–F265, doi:10.1111/ecoj.12461. Verified
against the published article (EJ furniture on page 1; source PDF not
distributed).

## The headline numbers (abstract + Table results)

Meta-survey of 159 empirical economics literatures: 64,076 reported
estimates drawn from more than 6,700 studies.

- **Median statistical power is 18% or less.** Half of the research
  areas have nearly 90% of their results underpowered.
- **~80% of reported effects are exaggerated** — weighting those
  literatures where adequate power exists: typically by a factor of two,
  with one-third inflated by a factor of four or more.

This is the empirical economics evidence for the Type M / Edlin-factor
check: across published economics, selection on significance in
low-power literatures produces a literature-scale exaggeration of
roughly 2×. It complements Gelman & Carlin (2014), which gives the
per-estimate machinery (`gelman_carlin_2014_type_ms.md`).

## Uses in the review skill

- `code-and-data`: when a paper's headline estimate
  comes from a design with power typical of the field (~18% median),
  the exaggeration finding has literature-level support, not just
  statistical theory.
- `claims` prior-plausibility framing: an estimate far above the
  plausible range in an underpowered literature is the modal outcome of
  the selection process, not an anomaly.
