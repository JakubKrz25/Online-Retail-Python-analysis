"""Own implementations of resampling methods (to be written while reading ch. 2-3).

Each function should be checked against its scipy counterpart:
    scipy.stats.bootstrap, scipy.stats.permutation_test
and against simulations with known ground truth in theory/.
"""
import numpy as np


def bootstrap_distribution(x, statistic, n_resamples=10_000, rng=None):
    """Return the bootstrap replicates statistic(x*_b), b = 1..B.

    x* is drawn i.i.d. from the empirical distribution F_n of x
    (i.e. sampling with replacement, same size n).
    """
    raise NotImplementedError("Chapter 2")


def bootstrap_ci(x, statistic, level=0.95, method="percentile", n_resamples=10_000, rng=None):
    """Bootstrap confidence interval for statistic(F).

    method: "percentile" or "bca" (start with percentile, add BCa after theory/02_bootstrap).
    """
    raise NotImplementedError("Chapter 2")


def permutation_test(x, y, statistic, n_resamples=10_000, alternative="two-sided", rng=None):
    """Two-sample permutation test of H0: x and y come from the same distribution.

    Under H0 the pooled sample is exchangeable, so the null distribution of
    statistic(x, y) is obtained by randomly reassigning group labels.
    Return (observed statistic, p-value).
    """
    raise NotImplementedError("Chapter 3")


def benjamini_hochberg(p_values, alpha=0.05):
    """Return a boolean mask of rejected hypotheses controlling FDR at level alpha."""
    raise NotImplementedError("Chapter 3")
