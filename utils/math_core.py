# utils/math_core.py
# Pure Mutual Information implementation — no Streamlit dependency.
# Information Theory × Finance series — github.com/information-theory-finance

import numpy as np
from typing import Tuple


def joint_pmf(x: np.ndarray, y: np.ndarray, bins: int = 20) -> np.ndarray:
    """
    Estimate the joint probability mass function P(X, Y) via 2D histogram.

    Returns
    -------
    joint : (bins × bins) array, sums to 1
    """
    joint, _, _ = np.histogram2d(x, y, bins=bins)
    total = joint.sum()
    if total == 0:
        raise ValueError("Empty data: cannot compute joint PMF")
    return joint / total


def marginal_pmfs(joint: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Return marginal PMFs P(X) and P(Y) from a joint PMF."""
    return joint.sum(axis=1), joint.sum(axis=0)


def mutual_information(
    x: np.ndarray,
    y: np.ndarray,
    bins: int = 20,
    base: float = 2.0,
) -> float:
    """
    Estimate mutual information I(X; Y) = ∑ P(x,y) log P(x,y) / (P(x) P(y)).

    Parameters
    ----------
    x, y : aligned 1-D arrays of floats
    bins : histogram bins for joint PMF estimation
    base : log base (2 → bits, e → nats)

    Returns
    -------
    mi : float ≥ 0
    """
    joint = joint_pmf(x, y, bins=bins)
    px, py = marginal_pmfs(joint)

    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            pij = joint[i, j]
            if pij > 0 and px[i] > 0 and py[j] > 0:
                mi += pij * np.log(pij / (px[i] * py[j]))
    return float(mi / np.log(base))


def mi_from_correlation(rho: float, base: float = 2.0) -> float:
    """
    Closed-form MI for a bivariate normal with correlation ρ.
    I(X;Y) = -½ log₂(1 - ρ²)

    Useful as a theoretical reference to validate the histogram estimator.
    """
    if abs(rho) >= 1.0:
        return float("inf")
    return float(-0.5 * np.log(1 - rho**2) / np.log(base))


def rolling_mi(
    x: np.ndarray,
    y: np.ndarray,
    window: int = 60,
    bins: int = 15,
    base: float = 2.0,
) -> np.ndarray:
    """
    Rolling mutual information between two aligned time series.

    Parameters
    ----------
    x, y   : 1-D arrays of equal length (e.g., log returns of two assets)
    window : rolling window size in periods
    bins   : histogram bins for joint PMF estimation
    base   : log base

    Returns
    -------
    result : array same length as x, NaN for first ``window`` entries
    """
    n = len(x)
    result = np.full(n, np.nan)
    for i in range(window, n + 1):
        xi = x[i - window : i]
        yi = y[i - window : i]
        try:
            result[i - 1] = mutual_information(xi, yi, bins=bins, base=base)
        except (ValueError, ZeroDivisionError):
            result[i - 1] = np.nan
    return result


def mi_vs_correlation_grid(
    rho_values: np.ndarray,
    bins: int = 20,
    n_samples: int = 5_000,
    base: float = 2.0,
    seed: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    For each correlation value, generate bivariate normal data and estimate MI.
    Also compute the theoretical MI for comparison.

    Returns
    -------
    mi_estimated   : array of histogram-estimated MI values
    mi_theoretical : array of closed-form MI values
    """
    rng = np.random.default_rng(seed)
    mi_est = np.zeros(len(rho_values))
    mi_theo = np.zeros(len(rho_values))
    for k, rho in enumerate(rho_values):
        cov = [[1, rho], [rho, 1]]
        data = rng.multivariate_normal([0, 0], cov, n_samples)
        mi_est[k] = mutual_information(data[:, 0], data[:, 1], bins=bins, base=base)
        mi_theo[k] = mi_from_correlation(rho, base=base)
    return mi_est, mi_theo
