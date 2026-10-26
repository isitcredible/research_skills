# Audit cases — the incident museum

Real failures that shaped `audit-review`'s gates. The SKILL.md carries the invariant; this file carries what violating it looked like. Keep entries short — the rule is the point, the case is the proof.

## 2b — print-fidelity

- **Phantom baseline.** One audit measured the whole fragility battery against OLS baselines read off the wrong printed column; every "collapse" was relative to a phantom.
- **Spec attribution by resemblance.** An audit inferred a printed table's regressor list from output resemblance, missed the fixed effects in the deposited code, and built its central remediation on a spec the authors never ran.

## 2c — claim-to-row provenance

- **Right number, wrong row.** A review's reports cited a subgroup-panel SE/p pair that was in fact the full-panel spatial-HAC SE mislabeled onto the subgroup row. The correct CSV existed; the reports had drifted from it.

## 2d — anomaly propagation

- **Duplicated cells, untouched claim.** Two appendix-table columns duplicated a later table's cells to every printed digit; the anomaly was logged but never traced back to the instrument-robustness claim citing them — the claim's evidentiary basis had quietly ceased to exist.
- **Ledger gap under a clean pass.** A review's robustness ledger never opened two appendix instrument tables the paper cited; an audit verifying every *existing* row against print missed it — the unopened rows held more fragility cells for the flagship outcome.

