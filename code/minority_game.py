"""
Minority Game — Urban Commuting Simulation
DESE61008 Game Theory & Market Design

Payoff convention (consistent with project spec):
  r = 1   if go  AND  A <= T   (at most T drivers → uncongested)
  r = 0   if go  AND  A >  T   (more than T drivers → congested)
  r = 0.3 if stay              (fixed utility of public transport)

Modules:
    1. Theoretical p* computation
    2. Static game simulation        → Figures 1, 2
    3. Best-Reply repeated game      → Figure 3
    4. Inductive agents              → Figures 4, 5, 6
    5. Homogeneous vs Heterogeneous  → Figure 7
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.stats import binom
import os

# =============================================================================
# CONSTANTS
# =============================================================================
N       = 101     # number of agents
T       = 60      # congestion threshold  (road is fine for A <= T, bad for A > T)
R_STAY  = 0.3     # fixed payoff for staying
M       = 200     # rounds for repeated game
EPSILON = 0.05    # exploration probability
GAMMA   = 0.9     # predictor score decay
DELTA   = 5       # accuracy tolerance window
K       = 6       # predictors per agent
WARMUP  = 10      # warmup rounds to seed history (not counted in output)
SEEDS   = [42, 123, 7]

# Colour palette
COL_T   = '#e74c3c'
COL_NP  = '#27ae60'
COL_BR  = '#2980b9'
COL_IND = '#8e44ad'
COL_RND = '#e67e22'
COL_HOM = '#e74c3c'
COL_HET = '#27ae60'

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

PREDICTOR_NAMES = [
    "last", "avg3", "avg5", "avg7",
    "contrarian", "trend",
    "cong_mom", "thresh_prox",    # indices 6, 7 — novel predictors
    "cycle2", "cycle3", "cycle5",
]
N_PREDICTORS = len(PREDICTOR_NAMES)   # 11
NOVEL_IDX    = [6, 7]                 # indices of novel predictors in pool


# =============================================================================
# MODULE 1 — THEORETICAL p* COMPUTATION
# =============================================================================

def compute_p_star():
    """
    Symmetric mixed NE indifference: E[r | go] = r_stay.
    With payoff r=1 when A <= T:
      E[r | go] = P(A_{-i} + 1 <= T) = P(Bin(N-1, p) <= T-1)
    Solve P(Bin(100, p) <= 59) = 0.3 via Brent's method.
    """
    def indifference(p):
        return binom.cdf(T - 1, N - 1, p) - R_STAY

    p_star = brentq(indifference, 0.4, 0.8)
    print(f"[Module 1] p* = {p_star:.4f}   |   N·p* = {N * p_star:.2f}")
    return p_star


# =============================================================================
# MODULE 2 — STATIC GAME SIMULATION
# =============================================================================

def run_static_game(p, rng):
    """Single-shot minority game. Payoff: 1 if go AND A<=T, 0 if go AND A>T."""
    go = rng.random(N) < p
    A  = int(go.sum())
    payoffs = np.where(go, np.where(A <= T, 1.0, 0.0), R_STAY)
    return A, payoffs


def simulate_static(p_star, rng):
    """Experiments 1 & 2: produce Figures 1 & 2."""
    p_values = np.arange(0.1, 0.91, 0.05)
    n_trials = 1000

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

    # ---- Figure 1 ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.plot(p_values, mean_r_go, 'o-', color=COL_IND, lw=2, ms=5,
             label=r'$\mathbb{E}[r \mid go]$')
    ax1.axhline(R_STAY, color='gray', ls='--', lw=1.5,
                label=f'$r_{{\\mathrm{{stay}}}}={R_STAY}$')
    ax1.axvline(p_star, color=COL_T, ls=':', lw=2,
                label=f'$p^*={p_star:.3f}$')
    ax1.set_xlabel('Probability of going, $p$', fontsize=11)
    ax1.set_ylabel('Expected payoff of going', fontsize=11)
    ax1.set_title('(a) Indifference condition: locating $p^*$', fontsize=11)
    ax1.legend(fontsize=9); ax1.set_xlim(0.05, 0.95); ax1.grid(alpha=0.3)

    ax2.plot(p_values, mean_attend, 's-', color=COL_BR, lw=2, ms=5,
             label=r'$\mathbb{E}[A]$')
    ax2.axhline(T, color=COL_T, ls='--', lw=1.5, label=f'$T={T}$')
    ax2.axvline(p_star, color=COL_T, ls=':', lw=2,
                label=f'$p^*={p_star:.3f}$')
    ax2.axhline(N * p_star, color=COL_NP, ls='--', lw=1.5,
                label=f'$Np^*\\approx{N*p_star:.1f}$')
    ax2.set_xlabel('Probability of going, $p$', fontsize=11)
    ax2.set_ylabel('Mean attendance $\\mathbb{E}[A]$', fontsize=11)
    ax2.set_title('(b) Mean attendance vs. $p$', fontsize=11)
    ax2.legend(fontsize=9); ax2.set_xlim(0.05, 0.95); ax2.grid(alpha=0.3)

    fig.suptitle('Figure 1: Static game sweep', fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure1_static_sweep.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 2] Figure 1 saved.")

    # ---- Figure 2 ----
    n_runs = 500
    att_pstar = np.array([run_static_game(p_star, rng)[0] for _ in range(n_runs)])
    congested_frac  = np.mean(att_pstar > T)
    empirical_mean  = np.mean(att_pstar)
    empirical_std   = np.std(att_pstar)
    theoretical_std = np.sqrt(N * p_star * (1 - p_star))
    print(f"[Module 2] Attendance at p*: mean={empirical_mean:.2f}, "
          f"empirical σ={empirical_std:.2f}, theoretical σ={theoretical_std:.2f}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(att_pstar, bins=range(35, 86), color=COL_IND, alpha=0.75,
            edgecolor='white', label=f'$p={p_star:.3f}$, {n_runs} runs')
    ax.axvline(T, color=COL_T, ls='--', lw=2, label=f'$T={T}$')
    ax.axvline(N * p_star, color=COL_NP, ls='--', lw=2,
               label=f'$Np^*={N*p_star:.1f}$')
    ax.set_xlabel('Attendance $A$', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(
        f'Figure 2: Attendance at $p^*$ — congested in {congested_frac:.0%} of rounds',
        fontsize=11, fontweight='bold')
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure2_histogram_pstar.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 2] Figure 2 saved.")
    return congested_frac, empirical_mean, empirical_std, theoretical_std


# =============================================================================
# MODULE 3 — MYOPIC BEST-REPLY REPEATED GAME
# =============================================================================

def run_best_reply():
    """
    Homogeneous myopic best-reply population.
    Rule: go if last_A <= T (road was uncongested last round), else stay.
    Initialisation: last_A = T (uncongested), so all go in round 1.
    """
    last_A = T        # initial perceived attendance: uncongested
    history = []
    for _ in range(M):
        decision = 1 if last_A <= T else 0
        A = N * decision     # all agents identical → all same choice
        history.append(A)
        last_A = A
    return np.array(history)


def plot_best_reply(history, p_star):
    """Figure 3."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(history, color=COL_BR, lw=1.5, label='Attendance $A_t$')
    ax.axhline(T, color=COL_T, ls='--', lw=1.8, label=f'$T={T}$')
    ax.axhline(N * p_star, color=COL_NP, ls='--', lw=1.8,
               label=f'$Np^*={N*p_star:.1f}$')
    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Attendance $A_t$', fontsize=11)
    ax.set_title(
        'Figure 3: Myopic best-reply dynamics — anti-coordination oscillation',
        fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0, M); ax.set_ylim(-5, N + 5); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure3_best_response.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 3] Figure 3 saved.")


# =============================================================================
# MODULE 4 — INDUCTIVE AGENTS
# =============================================================================

# ---- Predictor functions ----
# Signature: f(history: list, T_hat: float) -> float
# Edge case: return T_hat if insufficient history.

def _pred_last(h, th):      return float(h[-1])
def _pred_avg(h, th, n):    return float(np.mean(h[-n:])) if len(h) >= n else th
def _pred_contrarian(h, th): return float(2.0 * th - h[-1])
def _pred_trend(h, th):
    if len(h) < 2: return th
    return float(np.clip(h[-1] + (h[-1] - h[-2]), 0, N))

def _pred_congestion_momentum(h, th, lam=0.5):
    """Novel 1: partial correction after congestion; otherwise last value."""
    A_prev = float(h[-1])
    return A_prev + lam * (th - A_prev) if A_prev > th else A_prev

def _pred_threshold_proximity(h, th, rho=0.5):
    """Novel 2: exponential smoothing toward threshold (mean-reversion)."""
    return float(th + rho * (h[-1] - th))

def _pred_cycle(h, th, k): return float(h[-k]) if len(h) >= k else th


def build_predictor_pool():
    """Returns list of (name, callable) in PREDICTOR_NAMES order."""
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


# ---- Agent ----

class InductiveAgent:
    """
    Agent with K predictors, exponentially-weighted accuracy scores,
    and ε-greedy exploration.

    T_hat = T (fixed, public knowledge — road capacity is posted).
    Decision: go if best-predictor forecast <= T_hat, else stay.
    """

    def __init__(self, pred_indices: list, rng, epsilon: float = EPSILON):
        self.pred_idx = list(pred_indices)
        self.scores   = np.ones(K, dtype=float)
        self.T_hat    = float(T)
        self._last_fc = np.full(K, float(T))
        self._rng     = rng
        self._epsilon = epsilon

    def decide(self, history: list, pool: list) -> int:
        """Return 1 (go) or 0 (stay)."""
        if self._rng.random() < self._epsilon:
            return int(self._rng.random() < 0.5)
        fc = np.array([pool[i][1](history, self.T_hat) for i in self.pred_idx],
                      dtype=float)
        self._last_fc = fc
        return int(fc[int(np.argmax(self.scores))] <= self.T_hat)

    def update(self, A_actual: int):
        correct = np.abs(self._last_fc - A_actual) < DELTA
        self.scores = self.scores * GAMMA + correct.astype(float)

    def active_global_idx(self) -> int:
        return self.pred_idx[int(np.argmax(self.scores))]


# ---- Simulation ----

def run_inductive(rng, homogeneous: bool = False,
                  epsilon: float = EPSILON,
                  excluded_pred=None):
    """
    Run M rounds of the inductive minority game.

    Parameters
    ----------
    homogeneous   : all agents share identical K predictors
    epsilon       : exploration rate (set 0 for pure exploitation)
    excluded_pred : list of global predictor indices to exclude from pool
                    (used for ablation experiments)

    Returns
    -------
    attendance    : (M,) int array
    active_preds  : (M, N) int array of active global predictor index
    decisions_log : (M, N) int array of decisions (1=go, 0=stay)
    """
    pool      = build_predictor_pool()
    available = [i for i in range(N_PREDICTORS)
                 if excluded_pred is None or i not in excluded_pred]
    k_draw    = min(K, len(available))

    if homogeneous:
        shared = rng.choice(available, k_draw, replace=False).tolist()
        agents = [InductiveAgent(shared[:], rng, epsilon) for _ in range(N)]
    else:
        agents = [
            InductiveAgent(
                rng.choice(available, k_draw, replace=False).tolist(),
                rng, epsilon)
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


# ---- Individual payoff analysis ----

def compute_individual_payoffs(attendance, decisions_log):
    """
    For each agent, compute mean payoff over M rounds.
    Returns array of shape (N,).
    """
    ind = np.zeros(N)
    for t in range(M):
        A   = attendance[t]
        r_g = 1.0 if A <= T else 0.0
        for i in range(N):
            ind[i] += r_g if decisions_log[t, i] == 1 else R_STAY
    return ind / M


# ---- Figures ----

def _rolling(arr, w=10):
    return np.convolve(arr, np.ones(w) / w, mode='valid')


def plot_inductive_attendance(attendance, p_star, window=10):
    """Figure 4."""
    roll = _rolling(attendance, window)
    x_r  = np.arange(window - 1, M)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(attendance, color=COL_IND, lw=0.9, alpha=0.4, label='$A_t$')
    ax.plot(x_r, roll,  color=COL_IND, lw=2.2,
            label=f'Rolling mean (w={window})')
    ax.axhline(T,           color=COL_T,  ls='--', lw=1.8, label=f'$T={T}$')
    ax.axhline(N * p_star,  color=COL_NP, ls='--', lw=1.8,
               label=f'$Np^*={N*p_star:.1f}$')
    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Attendance $A_t$', fontsize=11)
    ax.set_title('Figure 4: Inductive agents — emergence of self-regulation near $T$',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=9); ax.set_xlim(0, M); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure4_inductive_attendance.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 4] Figure 4 saved.")


def plot_predictor_ecology(active_preds):
    """Figure 5: stacked area of predictor usage fractions over time."""
    fracs = np.zeros((M, N_PREDICTORS))
    for t in range(M):
        for pidx in active_preds[t]:
            fracs[t, pidx] += 1
    fracs /= N

    w = 10
    fracs_s = np.apply_along_axis(
        lambda x: np.convolve(x, np.ones(w) / w, mode='same'), 0, fracs)

    cmap   = plt.colormaps.get_cmap('tab20')
    colors = [cmap(i / N_PREDICTORS) for i in range(N_PREDICTORS)]

    fig, ax = plt.subplots(figsize=(11, 4.5))
    bottoms = np.zeros(M)
    for pidx in range(N_PREDICTORS):
        ax.fill_between(range(M), bottoms, bottoms + fracs_s[:, pidx],
                        color=colors[pidx], alpha=0.85,
                        label=PREDICTOR_NAMES[pidx])
        bottoms += fracs_s[:, pidx]

    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Fraction of agents', fontsize=11)
    ax.set_title('Figure 5: Predictor ecology over time',
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, ncol=6, loc='upper center',
              bbox_to_anchor=(0.5, -0.18), frameon=False)
    ax.set_xlim(0, M); ax.set_ylim(0, 1); ax.grid(alpha=0.2)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure5_predictor_ecology.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 4] Figure 5 saved.")

    # Print ecology stats for report
    last50 = fracs[-50:].mean(axis=0)
    print("[Module 4] Mean predictor share (last 50 rounds):")
    for i, name in enumerate(PREDICTOR_NAMES):
        print(f"  {name:14s}: {last50[i]:.3f}")


def _mean_population_payoff(attendance):
    """Mean payoff across all N agents per round. Congestion: A > T."""
    return np.where(
        attendance <= T,
        (attendance * 1.0 + (N - attendance) * R_STAY) / N,
        (N - attendance) * R_STAY / N
    )


def run_random_pstar(p_star, rng):
    return np.array([int((rng.random(N) < p_star).sum()) for _ in range(M)])


def plot_cumulative_payoff(att_br, att_rnd, att_ind, p_star):
    """Figure 6."""
    def cum_avg(att):
        return np.cumsum(_mean_population_payoff(att)) / (np.arange(M) + 1)

    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(cum_avg(att_br),  color=COL_BR,  lw=2, label='Myopic best-reply')
    ax.plot(cum_avg(att_rnd), color=COL_RND, lw=2,
            label=f'Random $p^*={p_star:.3f}$')
    ax.plot(cum_avg(att_ind), color=COL_IND, lw=2, label='Inductive')
    ax.axhline(R_STAY, color='gray', ls=':', lw=1.2,
               label=f'$r_{{\\mathrm{{stay}}}}={R_STAY}$')
    ax.set_xlabel('Round $t$', fontsize=11)
    ax.set_ylabel('Cumulative avg. payoff', fontsize=11)
    ax.set_title('Figure 6: Payoff comparison', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9); ax.set_xlim(0, M); ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure6_payoff_comparison.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 4] Figure 6 saved.")


# =============================================================================
# MODULE 5 — HOMOGENEOUS vs HETEROGENEOUS
# =============================================================================

def plot_homo_hetero(att_het, att_hom, p_star, window=10):
    """Figure 7."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for ax, (att, col, label) in zip(axes, [
        (att_het, COL_HET, 'Heterogeneous (random predictor assignment)'),
        (att_hom, COL_HOM, 'Homogeneous (identical predictors)'),
    ]):
        roll = _rolling(att, window)
        x_r  = np.arange(window - 1, M)
        ax.plot(att,    color=col, lw=0.9, alpha=0.35)
        ax.plot(x_r, roll, color=col, lw=2.2, label=label)
        ax.axhline(T,          color=COL_T,   ls='--', lw=1.8, label=f'$T={T}$')
        ax.axhline(N * p_star, color=COL_NP,  ls='--', lw=1.5,
                   label=f'$Np^*={N*p_star:.1f}$')
        ax.set_ylabel('Attendance $A_t$', fontsize=11)
        ax.legend(fontsize=9, loc='upper right')
        ax.set_ylim(0, N + 5); ax.grid(alpha=0.3)

    axes[-1].set_xlabel('Round $t$', fontsize=11)
    axes[-1].set_xlim(0, M)
    fig.suptitle('Figure 7: Heterogeneous vs Homogeneous population dynamics',
                 fontsize=12, fontweight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, 'figure7_homo_hetero.png'),
                dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("[Module 5] Figure 7 saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 65)
    print("Minority Game — Urban Commuting Simulation")
    print("=" * 65)

    # -- Module 1 --
    p_star = compute_p_star()

    # -- Module 2 --
    rng = np.random.default_rng(SEEDS[0])
    cf, em, es, ts = simulate_static(p_star, rng)
    print(f"[Module 2] Congestion fraction at p*: {cf:.2%}")

    # -- Module 3 --
    att_br = run_best_reply()
    plot_best_reply(att_br, p_star)
    br_mean = np.mean(att_br); br_std = np.std(att_br)
    br_payoff = np.mean(_mean_population_payoff(att_br))
    print(f"[Module 3] BR: mean={br_mean:.1f}, std={br_std:.1f}, "
          f"mean payoff={br_payoff:.3f}")

    # -- Module 4: inductive (primary seed) --
    rng4 = np.random.default_rng(SEEDS[0])
    att_ind, active_preds, dec_log = run_inductive(rng4)
    plot_inductive_attendance(att_ind, p_star)
    plot_predictor_ecology(active_preds)

    rng_rnd = np.random.default_rng(SEEDS[0] + 99)
    att_rnd = run_random_pstar(p_star, rng_rnd)
    plot_cumulative_payoff(att_br, att_rnd, att_ind, p_star)

    # Individual payoff stats
    ind_pay = compute_individual_payoffs(att_ind, dec_log)
    print(f"[Module 4] Individual payoffs — mean: {ind_pay.mean():.3f}, "
          f"std: {ind_pay.std():.3f}, "
          f"min: {ind_pay.min():.3f}, max: {ind_pay.max():.3f}")

    # -- Robustness across seeds --
    print("\n[Robustness] Inductive agents across seeds:")
    for s in SEEDS:
        rng_s = np.random.default_rng(s)
        att_s, _, _ = run_inductive(rng_s)
        print(f"  seed={s}: mean={np.mean(att_s):.2f}, std={np.std(att_s):.2f}, "
              f"congested={np.mean(att_s > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_s)):.3f}")

    # -- Module 5: homo vs hetero --
    rng_hom = np.random.default_rng(SEEDS[1])
    att_hom, _, _ = run_inductive(rng_hom, homogeneous=True)
    plot_homo_hetero(att_ind, att_hom, p_star)

    print("\n[Homo vs Hetero] Quantitative comparison (seed=42 het, seed=123 hom):")
    print(f"  Heterogeneous: mean={np.mean(att_ind):.1f}, "
          f"std={np.std(att_ind):.1f}, "
          f"cong={np.mean(att_ind > T):.1%}")
    print(f"  Homogeneous:   mean={np.mean(att_hom):.1f}, "
          f"std={np.std(att_hom):.1f}, "
          f"cong={np.mean(att_hom > T):.1%}")

    # -- Sensitivity: ε=0 (pure exploitation) --
    print("\n[Sensitivity] ε=0 (pure exploitation, no exploration):")
    for s in SEEDS:
        rng_e = np.random.default_rng(s)
        att_e0, _, _ = run_inductive(rng_e, epsilon=0.0)
        print(f"  seed={s}: mean={np.mean(att_e0):.2f}, "
              f"std={np.std(att_e0):.2f}, "
              f"cong={np.mean(att_e0 > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_e0)):.3f}")

    # -- Ablation: remove novel predictors (indices 6, 7) --
    print("\n[Ablation] Without novel predictors (cong_mom, thresh_prox):")
    for s in SEEDS:
        rng_a = np.random.default_rng(s)
        att_ab, _, _ = run_inductive(rng_a, excluded_pred=NOVEL_IDX)
        print(f"  seed={s}: mean={np.mean(att_ab):.2f}, "
              f"std={np.std(att_ab):.2f}, "
              f"cong={np.mean(att_ab > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_ab)):.3f}")

    print("\n" + "=" * 65)
    print(f"p* = {p_star:.4f}  |  Np* = {N * p_star:.2f}  |  T = {T}")
    print("All 7 figures saved.")
    print("=" * 65)


if __name__ == "__main__":
    main()
