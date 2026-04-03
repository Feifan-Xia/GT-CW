"""
Weekend Effect Experiment: 7-day calendar with variation in N and r_stay.

Weekdays (Mon-Fri):  N=101, T=60, r_stay=0.3
Weekends (Sat-Sun):  N=75,  T=60, r_stay=0.05  (infrequent transit)
"""

import numpy as np
from minority_game import (
    build_predictor_pool, InductiveAgent, WARMUP, M, T, R_STAY,
    _mean_population_payoff, N_PREDICTORS
)

def run_weekend_cycle(rng, n_weeks=5):
    """
    Simulate 5 weeks of 7-day cycles.
    Returns aggregated stats for weekdays and weekends.
    """
    pool = build_predictor_pool()
    
    # Track separately
    att_weekday, att_weekend = [], []
    pay_weekday, pay_weekend = [], []
    
    # Initialize agents once
    agents = [InductiveAgent(
        rng.choice(list(range(N_PREDICTORS)), 6, replace=False).tolist(),
        rng, epsilon=0.05) for _ in range(101)]
    
    history = list(rng.integers(50, 72, size=WARMUP).astype(float))
    
    # Simulate n_weeks full weeks
    for week in range(n_weeks):
        # Mon-Fri (5 days)
        for day in range(5):
            # Sample only 101 agents (weekday population)
            N_active = 101
            dec = np.array([ag.decide(history, pool) for ag in agents[:N_active]])
            A = int(dec.sum())
            att_weekday.append(A)
            
            # Payoff with r_stay = 0.3
            r_g = 1.0 if A <= T else 0.0
            payoff = np.mean([r_g if dec[i] else 0.3 for i in range(N_active)])
            pay_weekday.append(payoff)
            
            history.append(float(A))
            for ag in agents:
                ag.update(A)
        
        # Sat-Sun (2 days)
        for day in range(2):
            # Only 75 agents on weekend (25% reduction)
            N_active = 75
            dec = np.array([ag.decide(history, pool) for ag in agents[:N_active]])
            A = int(dec.sum())
            att_weekend.append(A)
            
            # Payoff with r_stay = 0.05 (poor transit)
            r_g = 1.0 if A <= T else 0.0
            payoff = np.mean([r_g if dec[i] else 0.05 for i in range(N_active)])
            pay_weekend.append(payoff)
            
            history.append(float(A))
            for ag in agents:
                ag.update(A)
    
    att_weekday = np.array(att_weekday)
    att_weekend = np.array(att_weekend)
    pay_weekday = np.array(pay_weekday)
    pay_weekend = np.array(pay_weekend)
    
    # Compute statistics
    stats = {
        'weekday': {
            'mean_A': np.mean(att_weekday),
            'std_A': np.std(att_weekday),
            'cong_rate': np.mean(att_weekday > T),
            'mean_payoff': np.mean(pay_weekday),
        },
        'weekend': {
            'mean_A': np.mean(att_weekend),
            'std_A': np.std(att_weekend),
            'cong_rate': np.mean(att_weekend > T),
            'mean_payoff': np.mean(pay_weekend),
        }
    }
    
    return stats, att_weekday, att_weekend, pay_weekday, pay_weekend


if __name__ == '__main__':
    from config import SEEDS
    
    # Aggregate results across 100 seeds
    all_stats = {'weekday': [], 'weekend': []}
    cong_diffs = []
    
    print("[Weekend Effect] Running 100 seeds...")
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        stats, _, _, _, _ = run_weekend_cycle(rng, n_weeks=5)
        all_stats['weekday'].append(stats['weekday'])
        all_stats['weekend'].append(stats['weekend'])
        cong_diffs.append((stats['weekend']['cong_rate'] - stats['weekday']['cong_rate']) * 100)
    
    # Compute aggregate statistics
    weekday_cong = np.array([s['cong_rate'] for s in all_stats['weekday']])
    weekend_cong = np.array([s['cong_rate'] for s in all_stats['weekend']])
    weekday_mean_A = np.array([s['mean_A'] for s in all_stats['weekday']])
    weekend_mean_A = np.array([s['mean_A'] for s in all_stats['weekend']])
    weekday_payoff = np.array([s['mean_payoff'] for s in all_stats['weekday']])
    weekend_payoff = np.array([s['mean_payoff'] for s in all_stats['weekend']])
    
    print(f"\n[Weekend Effect] Aggregated Results (100 seeds):")
    print(f"\nWeekday Statistics:")
    print(f"  Mean attendance: {np.mean(weekday_mean_A):.1f} ± {np.std(weekday_mean_A):.1f}")
    print(f"  Congestion rate: {np.mean(weekday_cong):.1%} ± {np.std(weekday_cong):.1%}")
    print(f"  Mean payoff: {np.mean(weekday_payoff):.3f} ± {np.std(weekday_payoff):.3f}")
    
    print(f"\nWeekend Statistics:")
    print(f"  Mean attendance: {np.mean(weekend_mean_A):.1f} ± {np.std(weekend_mean_A):.1f}")
    print(f"  Congestion rate: {np.mean(weekend_cong):.1%} ± {np.std(weekend_cong):.1%}")
    print(f"  Mean payoff: {np.mean(weekend_payoff):.3f} ± {np.std(weekend_payoff):.3f}")
    
    print(f"\nComparative Metrics:")
    print(f"  Attendance difference: {np.mean(weekend_mean_A) - np.mean(weekday_mean_A):+.1f}")
    print(f"  Congestion rate difference: {np.mean(cong_diffs):+.2f}%")
    print(f"  Payoff difference: {np.mean(weekend_payoff) - np.mean(weekday_payoff):+.3f}")
