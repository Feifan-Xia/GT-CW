"""
Module 3: Myopic best-reply repeated game.

All agents apply the stage-game best response to last period's realised
attendance. Because all agents are identical, this produces permanent
0<->101 oscillation.

Produces:
    Figure 3 -- attendance time series under myopic best-reply dynamics
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from config import N, T, M, COL_BR, COL_T, COL_NP, OUT_DIR


def run_best_reply():
    """
    Simulate M rounds of homogeneous myopic best-reply dynamics.

    Rule: drive if A_{t-1} <= T (road was uncongested), else take transit.
    Initialisation: perceived prior attendance = T (uncongested),
    so all 101 agents drive in round 1.

    Returns
    -------
    attendance : (M,) int array
    """
    last_A   = T
    history  = []
    for _ in range(M):
        decision = 1 if last_A <= T else 0
        A = N * decision       # homogeneous: all agents make the same choice
        history.append(A)
        last_A = A
    return np.array(history)


def plot_best_reply(history, p_star):
    """Figure 3: attendance under myopic best-reply dynamics."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(history, color=COL_BR, lw=1.5, label='Attendance $A_t$')
    ax.axhline(T, color=COL_T, ls='--', lw=1.8, label=f'$T={T}$')
    ax.axhline(N * p_star, color=COL_NP, ls='--', lw=1.8,
               label=f'$Np^*={N*p_star:.1f}$')
    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Attendance $A_t$', fontsize=11)
    ax.set_title(
        'Figure 3: Myopic best-reply dynamics -- oscillatory anti-coordination regime',
        fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0, M)
    ax.set_ylim(-5, N + 5)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure3_best_response.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[BestReply] Figure 3 saved.")
