"""
Module 2: Static (single-shot) game simulation.

Produces:
    Figure 1 -- payoff/mean-attendance sweep over p in [0.10, 0.90]
    Figure 2 -- attendance histogram at p*
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from config import N, T, R_STAY, COL_IND, COL_BR, COL_T, COL_NP, OUT_DIR


# ---------------------------------------------------------------------------
# Core stage-game draw
# ---------------------------------------------------------------------------

def run_static_game(p, rng):
    """
    Single-shot minority game.

    Returns
    -------
    A       : int    -- number of drivers
    payoffs : (N,)   -- per-agent payoff
    """
    drive = rng.random(N) < p
    A = int(drive.sum())
    payoffs = np.where(drive, np.where(A <= T, 1.0, 0.0), R_STAY)
    return A, payoffs


# ---------------------------------------------------------------------------
# Experiment: sweep over p
# ---------------------------------------------------------------------------

def simulate_static(p_star, rng, n_trials=1000):
    """
    Run n_trials draws for each p in {0.10, 0.15, ..., 0.90}.
    Saves Figures 1 and 2.

    Returns
    -------
    congested_frac  : float -- fraction of rounds with A > T at p*
    empirical_mean  : float
    empirical_std   : float
    theoretical_std : float
    """
    p_values = np.arange(0.1, 0.91, 0.05)

    mean_attend, mean_r_go = [], []
    for p in p_values:
        attendances, r_go_list = [], []
        for _ in range(n_trials):
            A, payoffs = run_static_game(p, rng)
            attendances.append(A)
            go_mask = payoffs != R_STAY
            if go_mask.sum() > 0:
                r_go_list.append(payoffs[go_mask].mean())
        mean_attend.append(np.mean(attendances))
        mean_r_go.append(np.mean(r_go_list) if r_go_list else 0.0)

    _plot_static_sweep(p_values, mean_r_go, mean_attend, p_star)

    # -- Figure 2 data --
    n_runs = 500
    att_pstar = np.array([run_static_game(p_star, rng)[0] for _ in range(n_runs)])
    congested_frac  = np.mean(att_pstar > T)
    empirical_mean  = np.mean(att_pstar)
    empirical_std   = np.std(att_pstar)
    theoretical_std = np.sqrt(N * p_star * (1 - p_star))
    print(f"[Static]  Attendance at p*: mean={empirical_mean:.2f}, "
          f"empirical sigma={empirical_std:.2f}, "
          f"theoretical sigma={theoretical_std:.2f}")

    _plot_histogram(att_pstar, congested_frac, p_star)
    return congested_frac, empirical_mean, empirical_std, theoretical_std


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def _plot_static_sweep(p_values, mean_r_go, mean_attend, p_star):
    """Figure 1: indifference condition and mean-attendance sweep."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.plot(p_values, mean_r_go, 'o-', color=COL_IND, lw=2, ms=5,
             label=r'$\mathbb{E}[r \mid drive]$')
    ax1.axhline(R_STAY, color='gray', ls='--', lw=1.5,
                label=f'$r_{{\\mathrm{{transit}}}}={R_STAY}$')
    ax1.axvline(p_star, color=COL_T, ls=':', lw=2,
                label=f'$p^*={p_star:.3f}$')
    ax1.set_xlabel('Probability of driving, $p$', fontsize=11)
    ax1.set_ylabel('Expected payoff of driving', fontsize=11)
    ax1.set_title('(a) Indifference condition: locating $p^*$', fontsize=11)
    ax1.legend(fontsize=9)
    ax1.set_xlim(0.05, 0.95)
    ax1.grid(alpha=0.3)

    ax2.plot(p_values, mean_attend, 's-', color=COL_BR, lw=2, ms=5,
             label=r'$\mathbb{E}[A]$')
    ax2.axhline(T, color=COL_T, ls='--', lw=1.5, label=f'$T={T}$')
    ax2.axvline(p_star, color=COL_T, ls=':', lw=2,
                label=f'$p^*={p_star:.3f}$')
    ax2.axhline(N * p_star, color=COL_NP, ls='--', lw=1.5,
                label=f'$Np^*\\approx{N*p_star:.1f}$')
    ax2.set_xlabel('Probability of driving, $p$', fontsize=11)
    ax2.set_ylabel('Mean attendance $\\mathbb{E}[A]$', fontsize=11)
    ax2.set_title('(b) Mean attendance vs. $p$', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.set_xlim(0.05, 0.95)
    ax2.grid(alpha=0.3)

    fig.suptitle('Figure 1: Static game sweep', fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure1_static_sweep.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Static]  Figure 1 saved.")


def _plot_histogram(att_pstar, congested_frac, p_star):
    """Figure 2: attendance histogram at p*."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(att_pstar, bins=range(35, 86), color=COL_IND, alpha=0.75,
            edgecolor='white', label=f'$p={p_star:.3f}$, {len(att_pstar)} runs')
    ax.axvline(T, color=COL_T, ls='--', lw=2, label=f'$T={T}$')
    ax.axvline(N * p_star, color=COL_NP, ls='--', lw=2,
               label=f'$Np^*={N*p_star:.1f}$')
    ax.set_xlabel('Attendance $A$', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(
        f'Figure 2: Attendance at $p^*$ -- congested in {congested_frac:.0%} of rounds',
        fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure2_histogram_pstar.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Static]  Figure 2 saved.")
