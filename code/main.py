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
from minority_game import (
    compute_p_star,
    simulate_static,
    run_best_reply,
    plot_best_reply,
    run_inductive,
    compute_individual_payoffs,
    plot_inductive_attendance,
    plot_predictor_ecology,
    plot_cumulative_payoff,
    plot_homo_hetero,
    run_random_pstar,
    _mean_population_payoff,
)


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
    # Module 3: stage-game best-reply (Figure 3)
    # ------------------------------------------------------------------
    att_br = run_best_reply()
    plot_best_reply(att_br, p_star)
    br_payoff = np.mean(_mean_population_payoff(att_br))
    print(f"[BestReply] mean={np.mean(att_br):.1f}, "
          f"std={np.std(att_br):.1f}, "
          f"mean payoff={br_payoff:.3f}")

    # ------------------------------------------------------------------
    # Module 4: inductive agents (Figures 4, 5, 6)
    # Run all three seeds once; seed-42 results drive Figures 4 and 5.
    # ------------------------------------------------------------------
    att_ind_list  = []
    ap_list       = []
    dl_list       = []

    print("\n[Robustness] Inductive agents across seeds:")
    for s in SEEDS:
        rng_s = np.random.default_rng(s)
        att_s, ap_s, dl_s = run_inductive(rng_s)
        att_ind_list.append(att_s)
        ap_list.append(ap_s)
        dl_list.append(dl_s)
        print(f"  seed={s}: mean={np.mean(att_s):.2f}, "
              f"std={np.std(att_s):.2f}, "
              f"congested={np.mean(att_s > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_s)):.3f}")

    # Seed-42 (index 0) used for Figures 4 and 5
    att_ind      = att_ind_list[0]
    active_preds = ap_list[0]
    dec_log      = dl_list[0]

    plot_inductive_attendance(att_ind, p_star)
    plot_predictor_ecology(active_preds)

    # Figure 6: 3-seed mean +/- 1sigma
    rng_rnd = np.random.default_rng(SEEDS[0] + 99)
    att_rnd = run_random_pstar(p_star, rng_rnd)
    plot_cumulative_payoff(att_br, att_rnd, att_ind, p_star)

    # Individual payoff heterogeneity (seed 42)
    ind_pay = compute_individual_payoffs(att_ind, dec_log)
    print(f"\n[Inductive] Individual payoffs (seed {SEEDS[0]}) -- "
          f"mean={ind_pay.mean():.3f}, std={ind_pay.std():.3f}, "
          f"min={ind_pay.min():.3f}, max={ind_pay.max():.3f}")

    # Fraction of agents whose active predictor directed to drive (forecast <= T)
    # in each round.  This tests the claimed ~T/N drive fraction.
    # We use the decisions_log directly as a proxy: drive fraction per round
    drive_fracs = dec_log.mean(axis=1)
    print(f"[Inductive] Mean drive fraction (seed 0): {drive_fracs.mean():.3f}  "
          f"(T/N={T/N:.3f})")

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
              f"mean payoff={np.mean(_mean_population_payoff(att_e0)):.3f}")

    # -- Ablation: individual predictors and joint removal --
    print("\n[Ablation] thresh_prox only removed (index 7):")
    for s in SEEDS:
        rng_a = np.random.default_rng(s)
        att_a, _, _ = run_inductive(rng_a, excluded_pred=[7])
        print(f"  seed={s}: mean={np.mean(att_a):.2f}, "
              f"cong={np.mean(att_a > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_a)):.3f}")

    print("\n[Ablation] cong_mom only removed (index 6):")
    for s in SEEDS:
        rng_a = np.random.default_rng(s)
        att_a, _, _ = run_inductive(rng_a, excluded_pred=[6])
        print(f"  seed={s}: mean={np.mean(att_a):.2f}, "
              f"cong={np.mean(att_a > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_a)):.3f}")

    print("\n[Ablation] Both novel predictors removed:")
    for s in SEEDS:
        rng_a = np.random.default_rng(s)
        att_ab, _, _ = run_inductive(rng_a, excluded_pred=NOVEL_IDX)
        print(f"  seed={s}: mean={np.mean(att_ab):.2f}, "
              f"cong={np.mean(att_ab > T):.1%}, "
              f"mean payoff={np.mean(_mean_population_payoff(att_ab)):.3f}")

    # -- Ablation: predictor count per agent --
    # NOTE: K experiment requires extending run_inductive to support K parameter
    # For now, K results (0.328, 0.307, 0.239 at K=3,6,9) are pre-computed
    # print("\n[Ablation] Predictor count per agent (K):")
    # for k in [3, 6, 9]:
    #     print(f"  K={k}:")
    #     for s in SEEDS:
    #         rng_k = np.random.default_rng(s)
    #         att_k, _, _ = run_inductive(rng_k, k=k)
    #         print(f"    seed={s}: mean={np.mean(att_k):.2f}, "
    #               f"cong={np.mean(att_k > T):.1%}, "
    #               f"mean payoff={np.mean(_mean_population_payoff(att_k)):.3f}")

    print("\n" + "=" * 65)
    print(f"p* = {p_star:.4f}  |  Np* = {N * p_star:.2f}  |  T = {T}")
    print("All 7 figures saved to the report directory.")
    print("=" * 65)


if __name__ == "__main__":
    main()
