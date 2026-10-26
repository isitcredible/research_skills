# Basis selection inspired by Section 5 of Conley, Kelly & Kozbur,
# UCD Working Paper WP26/11 (2026). This helper does not compute HAC inference.
# Uses quantile-knotted linear B-splines and selects among the first 1..K PCs
# by absolute nearest-neighbour residual correlation. Rank and residual-df caps
# are implementation safeguards, not an assertion of exact author-code parity.
# Coordinates must be projected planar coordinates in a common distance unit.
# Returned raw-spline support widths use the actual knots. PCA mixes these
# local functions: raw support widths are NOT a valid automatic HAC cutoff.
# Check the support of the basis actually used against Condition 6; see the
# spatial implementation record and software examples.
spatial_prewhiten <- function(y, x, coords, n_splines = 10, max_pcs = NULL) {
  integer_scalar <- function(z) {
    is.numeric(z) && length(z) == 1L && is.finite(z) && z == floor(z)
  }
  coords <- as.matrix(coords)
  x <- as.matrix(x)
  if (!is.numeric(y) || !is.null(dim(y)) || any(!is.finite(y)))
    stop("y must be a finite numeric vector.")
  n <- length(y)
  if (n < 4L || !is.numeric(coords) || nrow(coords) != n ||
      ncol(coords) != 2L || any(!is.finite(coords)))
    stop("coords must be a finite numeric n x 2 matrix, with n >= 4.")
  if (any(apply(coords, 2L, function(z) diff(range(z))) <= 0))
    stop("Both coordinate axes must vary; use an appropriate lower-dimensional method otherwise.")
  if (!is.numeric(x) || nrow(x) != n || any(!is.finite(x)))
    stop("x must be a finite numeric vector/matrix with n rows.")
  if (!integer_scalar(n_splines) || n_splines < 2L)
    stop("n_splines must be an integer >= 2.")
  if (!is.null(max_pcs) && (!integer_scalar(max_pcs) || max_pcs < 1L))
    stop("max_pcs must be a positive integer or NULL.")
  bx <- splines::bs(coords[, 1L], df = n_splines, degree = 1L, intercept = TRUE)
  by <- splines::bs(coords[, 2L], df = n_splines, degree = 1L, intercept = TRUE)
  tensor <- do.call(cbind, lapply(seq_len(ncol(bx)), function(i) bx[, i] * by))
  pca <- prcomp(tensor, center = TRUE, scale. = FALSE)
  # Numerical rank of the realized, centered tensor, not its theoretical ceiling.
  tol <- max(dim(tensor)) * .Machine$double.eps
  basis_rank <- sum(pca$sdev > max(pca$sdev) * tol)
  base <- cbind(Intercept = 1, x)
  base_rank <- qr(base)$rank
  ceiling <- min(basis_rank, floor(n / 2), n - base_rank - 2L)
  if (ceiling < 1L) stop("Insufficient basis rank or residual degrees of freedom for a PC search.")
  if (is.null(max_pcs)) max_pcs <- ceiling
  if (max_pcs > ceiling)
    stop(sprintf("max_pcs exceeds the rank/residual-df search ceiling (%d).", ceiling))
  pcs <- pca$x[, seq_len(max_pcs), drop = FALSE]
  distances <- as.matrix(dist(coords))
  diag(distances) <- Inf
  # Repeated locations allowed: first row in a distance tie is selected.
  nn <- apply(distances, 1L, which.min)
  nn_corrs <- rep(NA_real_, max_pcs)
  fitted_ranks <- integer(max_pcs)
  baseline_residual <- lm.fit(base, y)$residuals
  if (sum(baseline_residual^2) <= .Machine$double.eps * sum((y - mean(y))^2) ||
      sum((y - mean(y))^2) == 0)
    stop("Baseline outcome residual variance is numerically zero.")
  for (k in seq_len(max_pcs)) {
    fit <- lm.fit(cbind(base, pcs[, seq_len(k), drop = FALSE]), y)
    fitted_ranks[k] <- fit$rank
    res <- fit$residuals
    # Skip aliased PCs and degenerate residuals; do not select a numerical fit.
    if (fit$rank != base_rank + k || n - fit$rank < 2L ||
        sum(res^2) <= .Machine$double.eps * sum(baseline_residual^2) ||
        sd(res[nn]) == 0) next
    nn_corrs[k] <- abs(cor(res, res[nn]))
  }
  if (!any(is.finite(nn_corrs))) stop("No nondegenerate candidate PC model; inspect rank and residual variation.")
  score <- replace(nn_corrs, !is.finite(nn_corrs), Inf)
  optimal_k <- which.min(score)
  selected <- pcs[, seq_len(optimal_k), drop = FALSE]
  colnames(selected) <- paste0("PC", seq_len(optimal_k))
  support <- function(b) {
    boundary <- attr(b, "Boundary.knots")
    knots <- c(rep(boundary[1L], 2L), attr(b, "knots"), rep(boundary[2L], 2L))
    list(knots = knots, widths = knots[seq_len(ncol(b)) + 2L] - knots[seq_len(ncol(b))])
  }
  sx <- support(bx); sy <- support(by)
  baseline_nn_corr <- if (sd(baseline_residual[nn]) > 0) abs(cor(baseline_residual, baseline_residual[nn])) else NA_real_
  list(optimal_k = optimal_k, baseline_nn_corr = baseline_nn_corr, nn_corrs = nn_corrs, PCs = selected,
       basis_rank = basis_rank, search_ceiling = ceiling, baseline_rank = base_rank,
       fitted_ranks = fitted_ranks, residual_df = n - fitted_ranks[optimal_k],
       knots = list(x = sx$knots, y = sy$knots),
       raw_support_widths = list(x = sx$widths, y = sy$widths),
       raw_tensor_support_diameter_bound = sqrt(max(sx$widths)^2 + max(sy$widths)^2),
       domain_diameter_bound = sqrt(sum(apply(coords, 2L, function(z) diff(range(z)))^2)),
       coordinate_metric = "projected Euclidean; units supplied by caller")
}
