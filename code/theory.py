"""
Module 1: Theoretical computation of the symmetric mixed Nash equilibrium p*.

Indifference condition: E[r | drive] = r_transit
  P(Bin(N-1, p) <= T-1) = R_STAY
Solved via Brent's method on [0.4, 0.8].
"""

from scipy.optimize import brentq
from scipy.stats import binom
from config import N, T, R_STAY


def compute_p_star():
    """
    Return the unique symmetric mixed NE probability p*.

    P(Bin(100, p) <= 59) is strictly decreasing in p, so the solution
    is unique.
    """
    def indifference(p):
        return binom.cdf(T - 1, N - 1, p) - R_STAY

    p_star = brentq(indifference, 0.4, 0.8)
    print(f"[Theory]  p* = {p_star:.4f}   |   N*p* = {N * p_star:.2f}")
    return p_star
