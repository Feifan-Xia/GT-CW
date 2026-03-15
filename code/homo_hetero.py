"""
Module 5: Homogeneous vs. heterogeneous population comparison.

Produces:
    Figure 7 -- attendance time series for both population types
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from config import N, T, M, COL_T, COL_NP, COL_HOM, COL_HET, OUT_DIR
from utils import rolling_mean


def plot_homo_hetero(att_het, att_hom, p_star, window=10):
    """Figure 7: side-by-side attendance dynamics for each population type."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    pairs = [
        (att_het, COL_HET, 'Heterogeneous (random predictor assignment)'),
        (att_hom, COL_HOM, 'Homogeneous (shared predictor set)'),
    ]
    for ax, (att, col, label) in zip(axes, pairs):
        roll = rolling_mean(att, window)
        x_r  = np.arange(window - 1, M)
        ax.plot(att, color=col, lw=0.9, alpha=0.35)
        ax.plot(x_r, roll, color=col, lw=2.2, label=label)
        ax.axhline(T, color=COL_T, ls='--', lw=1.8, label=f'$T={T}$')
        ax.axhline(N * p_star, color=COL_NP, ls='--', lw=1.5,
                   label=f'$Np^*={N*p_star:.1f}$')
        ax.set_ylabel('Attendance $A_t$', fontsize=11)
        ax.legend(fontsize=9, loc='upper right')
        ax.set_ylim(0, N + 5)
        ax.grid(alpha=0.3)

    axes[-1].set_xlabel('Round $t$', fontsize=11)
    axes[-1].set_xlim(0, M)
    fig.suptitle('Figure 7: Heterogeneous vs. Homogeneous population dynamics',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure7_homo_hetero.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[HomoHetero] Figure 7 saved.")
