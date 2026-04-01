"""
Module 4: Inductive agents following Arthur (1994).

Each agent holds K predictors drawn at random from a shared pool of 11.
Predictor scores are updated by exponential smoothing, and the agent
follows the highest-scoring predictor with epsilon-greedy exploration.

Produces:
    Figure 4 -- attendance time series (convergence near T)
    Figure 5 -- active predictor composition over time
    Figure 6 -- cumulative payoff comparison
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from config import (
    N, T, R_STAY, M, EPSILON, GAMMA, DELTA, K, WARMUP,
    COL_IND, COL_BR, COL_RND, COL_T, COL_NP, COL_HET,
    PREDICTOR_NAMES, N_PREDICTORS, NOVEL_IDX,
    OUT_DIR,
)
from utils import rolling_mean, population_payoff


# =============================================================================
# Predictor functions
# Signature: f(history: list[float], T_hat: float) -> float
# If insufficient history, return T_hat (no bias toward driving or transit).
# =============================================================================

def _pred_last(h, th):
    return float(h[-1])

def _pred_avg(h, th, n):
    return float(np.mean(h[-n:])) if len(h) >= n else th

def _pred_contrarian(h, th):
    return float(2.0 * th - h[-1])

def _pred_trend(h, th):
    if len(h) < 2:
        return th
    return float(np.clip(h[-1] + (h[-1] - h[-2]), 0, N))

def _pred_congestion_momentum(h, th, lam=0.5):
    """
    Novel predictor 1: partial correction after congestion.
    If last attendance exceeded threshold, predicts partial recovery toward T
    rather than full reversal -- models cautious driver loss-aversion.
    Otherwise returns the last value unchanged.
    """
    A_prev = float(h[-1])
    return A_prev + lam * (th - A_prev) if A_prev > th else A_prev

def _pred_threshold_proximity(h, th, rho=0.5):
    """
    Novel predictor 2: mean-reversion toward threshold.
    Captures the belief that attendance gravitates toward road capacity.
    """
    return float(th + rho * (h[-1] - th))

def _pred_cycle(h, th, k):
    return float(h[-k]) if len(h) >= k else th


def build_predictor_pool():
    """
    Return the full predictor pool as a list of (name, callable) pairs,
    ordered to match PREDICTOR_NAMES.
    """
    return [
        ("last",        lambda h, th: _pred_last(h, th)),
        ("avg3",        lambda h, th: _pred_avg(h, th, 3)),
        ("avg5",        lambda h, th: _pred_avg(h, th, 5)),
        ("avg7",        lambda h, th: _pred_avg(h, th, 7)),
        ("contrarian",  lambda h, th: _pred_contrarian(h, th)),
        ("trend",       lambda h, th: _pred_trend(h, th)),
        ("cong_mom",    lambda h, th: _pred_congestion_momentum(h, th)),
        ("thresh_prox", lambda h, th: _pred_threshold_proximity(h, th)),
        ("cycle2",      lambda h, th: _pred_cycle(h, th, 2)),
        ("cycle3",      lambda h, th: _pred_cycle(h, th, 3)),
        ("cycle5",      lambda h, th: _pred_cycle(h, th, 5)),
    ]


# =============================================================================
# Agent
# =============================================================================

class InductiveAgent:
    """
    Agent with K predictors, exponentially-weighted accuracy scores,
    and epsilon-greedy exploration.

    T_hat = T (fixed, public knowledge: road capacity is posted).
    Decision:
        drive   if best-scoring predictor forecast <= T_hat
        transit otherwise
    """

    def __init__(self, pred_indices: list, rng, epsilon: float = EPSILON):
        self.pred_idx  = list(pred_indices)
        self.scores    = np.ones(len(pred_indices), dtype=float)
        self.T_hat     = float(T)
        self._last_fc  = np.full(len(pred_indices), float(T))
        self._rng      = rng
        self._epsilon  = epsilon

    def decide(self, history: list, pool: list) -> int:
        """Return 1 (drive) or 0 (transit)."""
        if self._rng.random() < self._epsilon:
            return int(self._rng.random() < 0.5)
        fc = np.array(
            [pool[i][1](history, self.T_hat) for i in self.pred_idx],
            dtype=float,
        )
        self._last_fc = fc
        return int(fc[int(np.argmax(self.scores))] <= self.T_hat)

    def update(self, A_actual: int):
        """Update predictor scores based on realised attendance."""
        correct = np.abs(self._last_fc - A_actual) < DELTA
        self.scores = self.scores * GAMMA + correct.astype(float)

    def active_global_idx(self) -> int:
        """Global index of the currently active (highest-scoring) predictor."""
        return self.pred_idx[int(np.argmax(self.scores))]


# =============================================================================
# Simulation
# =============================================================================

def run_inductive(
    rng,
    homogeneous: bool = False,
    epsilon: float = EPSILON,
    excluded_pred=None,
    k: int = K,
):
    """
    Run M rounds of the inductive minority game.

    Parameters
    ----------
    homogeneous   : all agents share the same K predictors (tests diversity effect)
    epsilon       : exploration probability (0 = pure exploitation)
    excluded_pred : list of global predictor indices excluded from draw
                    (used for ablation experiments)
    k             : number of predictors per agent (default K=6)

    Returns
    -------
    attendance    : (M,)   int array
    active_preds  : (M, N) int array -- active global predictor index per agent
    decisions_log : (M, N) int array -- decisions (1=drive, 0=transit)
    """
    pool      = build_predictor_pool()
    available = [
        i for i in range(N_PREDICTORS)
        if excluded_pred is None or i not in excluded_pred
    ]
    k_draw = min(k, len(available))

    if homogeneous:
        shared = rng.choice(available, k_draw, replace=False).tolist()
        agents = [InductiveAgent(shared[:], rng, epsilon) for _ in range(N)]
    else:
        agents = [
            InductiveAgent(
                rng.choice(available, k_draw, replace=False).tolist(),
                rng, epsilon,
            )
            for _ in range(N)
        ]

    history       = list(rng.integers(50, 72, size=WARMUP).astype(float))
    attendance    = np.zeros(M, dtype=int)
    active_preds  = np.zeros((M, N), dtype=int)
    decisions_log = np.zeros((M, N), dtype=int)

    for t in range(M):
        dec = np.array([ag.decide(history, pool) for ag in agents])
        A   = int(dec.sum())
        attendance[t]    = A
        active_preds[t]  = [ag.active_global_idx() for ag in agents]
        decisions_log[t] = dec
        history.append(float(A))
        for ag in agents:
            ag.update(A)

    return attendance, active_preds, decisions_log


def compute_individual_payoffs(attendance, decisions_log):
    """
    Compute mean payoff per agent over M rounds.

    Returns
    -------
    per_agent_payoff : (N,) float array
    """
    ind = np.zeros(N)
    r_g = np.where(attendance <= T, 1.0, 0.0)
    for t in range(M):
        drive_mask = decisions_log[t] == 1
        ind[drive_mask]  += r_g[t]
        ind[~drive_mask] += R_STAY
    return ind / M


# =============================================================================
# Figures
# =============================================================================

def plot_inductive_attendance(attendance, p_star, window=10):
    """Figure 4: attendance time series -- convergence near T."""
    roll = rolling_mean(attendance, window)
    x_r  = np.arange(window - 1, M)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(attendance, color=COL_IND, lw=0.9, alpha=0.4, label='$A_t$')
    ax.plot(x_r, roll, color=COL_IND, lw=2.2,
            label=f'Rolling mean (w={window})')
    ax.axhline(T, color=COL_T, ls='--', lw=1.8, label=f'$T={T}$')
    ax.axhline(N * p_star, color=COL_NP, ls='--', lw=1.8,
               label=f'$Np^*={N*p_star:.1f}$')
    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Attendance $A_t$', fontsize=11)
    ax.set_title(
        'Figure 4: Inductive agents -- emergent near-threshold coordination',
        fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0, M)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure4_inductive_attendance.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Inductive] Figure 4 saved.")


def plot_predictor_composition(active_preds):
    """Figure 5: stacked area of active predictor composition over time."""
    fracs = np.zeros((M, N_PREDICTORS))
    for t in range(M):
        for pidx in active_preds[t]:
            fracs[t, pidx] += 1
    fracs /= N

    w = 10
    fracs_s = np.apply_along_axis(
        lambda x: np.convolve(x, np.ones(w) / w, mode='same'), 0, fracs
    )

    cmap   = plt.colormaps.get_cmap('tab20')
    colors = [cmap(i / N_PREDICTORS) for i in range(N_PREDICTORS)]

    # Group predictors for better visualization
    groups = {
        'basic': ['last'],
        'averaging': ['avg3', 'avg5', 'avg7'],
        'opposite': ['contrarian'],
        'momentum': ['trend'],
        'novel': ['cong_mom', 'thresh_prox'],
        'cyclic': ['cycle2', 'cycle3', 'cycle5']
    }
    
    # Assign colors per group, with varying alpha for intra-group distinction
    group_colors = {
        'basic': COL_BR,      # blue
        'averaging': COL_IND, # purple
        'opposite': COL_RND,  # orange
        'momentum': COL_T,    # red
        'novel': COL_NP,      # green
        'cyclic': COL_HET     # green (different shade)
    }
    
    alphas = [0.9, 0.7, 0.5]  # for multiple in same group

    fig, ax = plt.subplots(figsize=(11, 4.5))
    bottoms = np.zeros(M)
    for group_name, pred_names in groups.items():
        base_color = group_colors[group_name]
        for i, pred_name in enumerate(pred_names):
            pidx = PREDICTOR_NAMES.index(pred_name)
            alpha = alphas[min(i, len(alphas)-1)]
            ax.fill_between(range(M), bottoms, bottoms + fracs_s[:, pidx],
                            color=base_color, alpha=alpha,
                            label=pred_name)
            bottoms += fracs_s[:, pidx]

    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Fraction of agents', fontsize=11)
    ax.set_title('Figure 5: Active predictor composition over time',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, ncol=6, loc='upper center',
              bbox_to_anchor=(0.5, -0.18), frameon=False)
    ax.set_xlim(0, M)
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.2)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure5_predictor_ecology.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Inductive] Figure 5 saved.")

    # Summary for report
    last50 = fracs[-50:].mean(axis=0)
    print("[Inductive] Mean predictor share (last 50 rounds):")
    for i, name in enumerate(PREDICTOR_NAMES):
        print(f"  {name:14s}: {last50[i]:.3f}")


def plot_cumulative_payoff(att_br, att_rnd, att_ind_list, p_star):
    """
    Figure 6: cumulative average payoff across the three dynamics.

    att_ind_list : list of (M,) int arrays, one per seed.
                   The mean across seeds is plotted as the solid inductive
                   line; the +/-1 sigma band shows cross-seed variability.
    """
    def cum_avg(att):
        return np.cumsum(population_payoff(att)) / (np.arange(M) + 1)

    ind_curves = np.array([cum_avg(att) for att in att_ind_list])
    ind_mean   = ind_curves.mean(axis=0)
    ind_std    = ind_curves.std(axis=0)
    rounds     = np.arange(M)

    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(cum_avg(att_br),  color=COL_BR,  lw=2, label='Stage-game best-reply')
    ax.plot(cum_avg(att_rnd), color=COL_RND, lw=2,
            label=f'Random $p^*={p_star:.3f}$ (mixed NE)')
    ax.plot(rounds, ind_mean, color=COL_IND, lw=2,
            label=f'Inductive (mean, {len(att_ind_list)} seeds)')
    ax.fill_between(rounds, ind_mean - ind_std, ind_mean + ind_std,
                    color=COL_IND, alpha=0.2, label='$\\pm 1\\sigma$ across seeds')
    ax.axhline(R_STAY, color='gray', ls=':', lw=1.2,
               label=f'$r_{{\\mathrm{{transit}}}}={R_STAY}$')
    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Cumulative avg. payoff', fontsize=11)
    ax.set_title('Figure 6: Cumulative payoff comparison', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0, M)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure6_payoff_comparison.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Inductive] Figure 6 saved.")
