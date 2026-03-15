"""
Shared utility functions used by multiple modules.
"""

import numpy as np
from config import N, T, R_STAY, M


def rolling_mean(arr, w=10):
    """Compute a rolling mean with window w."""
    return np.convolve(arr, np.ones(w) / w, mode='valid')


def population_payoff(attendance):
    """
    Mean payoff across all N agents for each round.

    Uncongested (A <= T): drivers earn 1, transit users earn R_STAY.
    Congested  (A >  T): drivers earn 0, transit users earn R_STAY.

    Parameters
    ----------
    attendance : array-like of int, shape (M,)

    Returns
    -------
    payoffs : ndarray of float, shape (M,)
    """
    attendance = np.asarray(attendance)
    return np.where(
        attendance <= T,
        (attendance * 1.0 + (N - attendance) * R_STAY) / N,
        (N - attendance) * R_STAY / N,
    )


def run_random_baseline(p_star, rng, rounds=M, n=N):
    """
    Generate attendance series for agents each independently playing p_star.
    Used as the mixed-NE benchmark in payoff comparisons.
    """
    return np.array([int((rng.random(n) < p_star).sum()) for _ in range(rounds)])
