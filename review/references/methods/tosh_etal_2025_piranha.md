# The piranha problem — Tosh, Greengard, Goodrich, Gelman, Vehtari & Hsu (2025)

Working distillation of Christopher Tosh, Philip Greengard, Ben
Goodrich, Andrew Gelman, Aki Vehtari & Daniel Hsu, "The Piranha Problem:
Large Effects Swimming in a Small Pond," *Notices of the American
Mathematical Society* 72(6): 702–711 (2025). Verified against the
accepted manuscript dated 2 Apr 2024 ("To appear in the Notices of the
American Mathematical Society" on the last page; source PDF not
distributed) — cite the Notices version; the ms is unpaginated in
journal style.

## The theorem family (§4)

The intuition: if many explanatory variables each have large effects on
one outcome, the effects cannot coexist unless they are themselves
dependent — piranhas in a small tank. The paper formalizes this three
ways:

1. **Correlation**: if many covariates are each highly correlated with
   an outcome, they must be substantially correlated with each other.
   The bounds are ceilings: Van der Corput's inequality (Theorem 1)
   caps Σ|corr(X_i, y)| by √(p + Σ_{i≠j}|corr(X_i, X_j)|), and Theorem 3
   caps Σcorr(X_i, y)² by λ_max of the predictors' correlation matrix —
   so mutually uncorrelated predictors carry at most 1 in total. (The
   floor is on the predictors' inter-correlation: if every |corr(X_i, y)|
   ≥ τ, then Σ_{i≠j}|corr(X_i, X_j)| ≥ p(τ²p − 1).)
2. **Regression**: the ℓ²-norm of the least-squares coefficient vector
   is bounded by the eigenvalues of the predictors' second-moment
   matrix — only so many coefficients can be large.
3. **Mutual information**: an analogous bound for general nonlinear
   dependence.

The consequence for a literature: a domain claiming many large,
consistent, independent effects on one outcome implies either that the
effects are smaller than claimed, or that the "different" inputs are
measuring the same thing, or that their interactions are large enough
to destabilize the system — the papers cannot all be right at face
value.

## Uses in the review skill

- `claims` piranha check: when the paper claims a large
  effect for X on Y while the literature claims large effects of many
  other inputs on the same Y, run the adding-up question — how much
  variance would remain if all claimed effects were real? The check is
  a prior-plausibility prompt, not a finding by itself; the theorems
  give it force only when the claimed magnitudes are quantified.
