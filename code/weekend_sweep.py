"""
Weekend Effect - Parameter sweeping to find equilibrium congestion.

Test different population reduction levels to see when weekend congestion
matches or slightly exceeds weekday congestion.
"""

import numpy as np
from minority_game import (
    build_predictor_pool, InductiveAgent, WARMUP, M, T, R_STAY,
    _mean_population_payoff, N_PREDICTORS
)

def run_weekend_cycle_with_n(rng, n_weekend, n_weeks=5):
    """
    Simulate with custom weekend population.
    """
    pool = build_predictor_pool()
    
    att_weekday, att_weekend = [], []
    
    agents = [InductiveAgent(
        rng.choice(list(range(N_PREDICTORS)), 6, replace=False).tolist(),
        rng, epsilon=0.05) for _ in range(101)]
    
    history = list(rng.integers(50, 72, size=WARMUP).astype(float))
    
    for week in range(n_weeks):
        # Mon-Fri
        for day in range(5):
            dec = np.array([ag.decide(history, pool) for ag in agents[:101]])
            A = int(dec.sum())
            att_weekday.append(A)
            history.append(float(A))
            for ag in agents:
                ag.update(A)
        
        # Sat-Sun
        for day in range(2):
            dec = np.array([ag.decide(history, pool) for ag in agents[:n_weekend]])
            A = int(dec.sum())
            att_weekend.append(A)
            history.append(float(A))
            for ag in agents:
                ag.update(A)
    
    weekday_cong = np.mean(np.array(att_weekday) > T)
    weekend_cong = np.mean(np.array(att_weekend) > T)
    
    return weekday_cong, weekend_cong


if __name__ == '__main__':
    from config import SEEDS
    
    # Test different reduction levels
    reductions = [5, 8, 10, 12, 15, 20, 25]
    n_populations = [96, 93, 91, 89, 86, 81, 76]  # Corresponding N values (101 * (1 - pct/100))
    
    print("[Parameter Sweep] Testing different weekend population levels:")
    print("Reduction% | N_weekend | Weekday Cong | Weekend Cong | Difference")
    print("-" * 70)
    
    for pct, n_w in zip(reductions, n_populations):
        weekday_congs = []
        weekend_congs = []
        
        for seed in SEEDS[:20]:  # Quick test with first 20 seeds
            rng = np.random.default_rng(seed)
            w_cong, we_cong = run_weekend_cycle_with_n(rng, n_w, n_weeks=3)
            weekday_congs.append(w_cong)
            weekend_congs.append(we_cong)
        
        avg_w = np.mean(weekday_congs)
        avg_we = np.mean(weekend_congs)
        diff = avg_we - avg_w
        
        print(f"{pct:4}%     | {n_w:3}       | {avg_w:.1%}         | {avg_we:.1%}        | {diff:+.2%}")
