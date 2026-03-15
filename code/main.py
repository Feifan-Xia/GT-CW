"""
Minority Game -- Urban Commuting Simulation
DESE61008 Game Theory and Market Design

Entry point: runs all five modules and saves Figures 1-7 to the report
directory so that Markdown image references resolve automatically.

Usage:
    python main.py
"""

import numpy as np

from config import SEEDS, N, T, NOVEL_IDX
from utils import population_payoff, run_random_baseline
from theory import compute_p_star
from static_game import simulate_static
from best_reply import run_best_reply, plot_best_reply
from inductive import (
    run_inductive,
    compute_individual_payoffs,
    plot_inductive_attendance,
    plot_predictor_composition,
    plot_cumulative_payoff,
)
from homo_hetero import plot_homo_hetero


def main():
    print("=" * 65)
    print("Minority Game -- Urban Commuting Simulation")
    print("=" * 65)

    # ------------------------------------------------------------------
    # Module 1: theoretical p*
    # ------------------------------------------------------------------
    p_star = compute_p_star()

    # ------------------------------------------------------------------
    # Module 2: static game (Figures 1, 2)
    # ------------------------------------------------------------------
    rng2 = np.random.default_rng(SEEDS[0])
    cf, em, es, ts = simulate_static(p_star, rng2)
    print(f"[Static]  Congestion fraction at p*: {cf:.2%}")

    # ------------------------------------------------------------------
    # Module 3: myopic best-reply (Figure 3)
    # ------------------------------------------------------------------
    att_br = run_best_reply()
    plot_best_reply(att_br, p_star)
    br_payoff = np.mean(population_payoff(att_br))
    print(f"[BestReply] mean={np.mean(att_br):.1f}, "
          f"std={np.std(att_br):.1f}, "
          f"mean payoff={br_payoff:.3f}")

    # ------------------------------------------------------------------
    # Module 4: inductive agents (Figures 4, 5, 6)
    # ------------------------------------------------------------------
    rng4 = np.random.default_rng(SEEDS[0])
    att_ind, active_preds, dec_log = run_inductive(rng4)
    plot_inductive_attendance(att_ind, p_star)
    plot_predictor_composition(active_preds)

    rng_rnd = np.random.default_rng(SEEDS[0] + 99)
    att_rnd = run_random_baseline(p_star, rng_rnd)
    plot_cumulative_payoff(att_br, att_rnd, att_ind, p_star)

    ind_pay = compute_individual_payoffs(att_ind, dec_log)
    print(f"[Inductive] Individual payoffs -- "
          f"mean={ind_pay.mean():.3f}, std={ind_pay.std():.3f}, "
          f"min={ind_pay.min():.3f}, max={ind_pay.max():.3f}")

    # -- Robustness across seeds --
    print("\n[Robustness] Inductive agents across seeds:")
    for s in SEEDS:
        rng_s = np.random.default_rng(s)
        att_s, _, _ = run_inductive(rng_s)
        print(f"  seed={s}: mean={np.mean(att_s):.2f}, "
              f"std={np.std(att_s):.2f}, "
              f"congested={np.mean(att_s > T):.1%}, "
              f"mean payoff={np.mean(population_payoff(att_s)):.3f}")

    # ------------------------------------------------------------------
    # Module 5: homogeneous vs. heterogeneous (Figure 7)
    # ------------------------------------------------------------------
    rng_hom = np.random.default_rng(SEEDS[1])
    att_hom, _, _ = run_inductive(rng_hom, homogeneous=True)
    plot_homo_hetero(att_ind, att_hom, p_star)

    print("\n[HomoHetero] Quantitative comparison:")
    print(f"  Heterogeneous: mean={np.mean(att_ind):.1f}, "
          f"std={np.std(att_ind):.1f}, "
          f"cong={np.mean(att_ind > T):.1%}")
    print(f"  Homogeneous:   mean={np.mean(att_hom):.1f}, "
          f"std={np.std(att_hom):.1f}, "
          f"cong={np.mean(att_hom > T):.1%}")

    # -- Sensitivity: epsilon=0 (pure exploitation) --
    print("\n[Sensitivity] epsilon=0 (pure exploitation):")
    for s in SEEDS:
        rng_e = np.random.default_rng(s)
        att_e0, _, _ = run_inductive(rng_e, epsilon=0.0)
        print(f"  seed={s}: mean={np.mean(att_e0):.2f}, "
              f"std={np.std(att_e0):.2f}, "
              f"cong={np.mean(att_e0 > T):.1%}, "
              f"mean payoff={np.mean(population_payoff(att_e0)):.3f}")

    # -- Ablation: remove novel predictors --
    print("\n[Ablation] Without novel predictors (cong_mom, thresh_prox):")
    for s in SEEDS:
        rng_a = np.random.default_rng(s)
        att_ab, _, _ = run_inductive(rng_a, excluded_pred=NOVEL_IDX)
        print(f"  seed={s}: mean={np.mean(att_ab):.2f}, "
              f"std={np.std(att_ab):.2f}, "
              f"cong={np.mean(att_ab > T):.1%}, "
              f"mean payoff={np.mean(population_payoff(att_ab)):.3f}")

    print("\n" + "=" * 65)
    print(f"p* = {p_star:.4f}  |  Np* = {N * p_star:.2f}  |  T = {T}")
    print("All 7 figures saved to the report directory.")
    print("=" * 65)


if __name__ == "__main__":
    main()
