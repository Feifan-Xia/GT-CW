"""
Section 5.4: 100-seed homogeneous vs heterogeneous time series with 1-sigma band.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from minority_game import run_inductive, T, M

if __name__ == '__main__':
    from config import SEEDS
    
    print("[Section 5.4] Generating time series plots for 100 seeds...")
    
    att_het_list = []
    att_hom_list = []
    
    for i, seed in enumerate(SEEDS):
        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/100 seeds...")
        
        rng = np.random.default_rng(seed)
        
        # Heterogeneous
        att_het, _, _ = run_inductive(rng, homogeneous=False)
        att_het_list.append(att_het)
        
        # Homogeneous
        rng2 = np.random.default_rng(seed + 1000)
        att_hom, _, _ = run_inductive(rng2, homogeneous=True)
        att_hom_list.append(att_hom)
    
    # Compute mean and std across 100 seeds
    att_het_arr = np.array(att_het_list)  # (100, 200)
    att_hom_arr = np.array(att_hom_list)  # (100, 200)
    
    mean_het = np.mean(att_het_arr, axis=0)
    std_het = np.std(att_het_arr, axis=0)
    
    mean_hom = np.mean(att_hom_arr, axis=0)
    std_hom = np.std(att_hom_arr, axis=0)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Top: Heterogeneous
    time = np.arange(M)
    ax1.plot(time, mean_het, color='#27ae60', lw=2.5, label='Mean attendance (100 seeds)')
    ax1.fill_between(time, mean_het - std_het, mean_het + std_het,
                     color='#27ae60', alpha=0.3, label='±1 σ')
    ax1.axhline(T, color='gray', ls='--', lw=1.5, label=f'T={T}')
    ax1.set_ylabel('Attendance $A_t$', fontsize=11)
    ax1.set_title('Heterogeneous population: 100 seeds', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9, loc='upper right')
    ax1.set_xlim(0, M)
    ax1.grid(alpha=0.3)
    
    # Bottom: Homogeneous
    ax2.plot(time, mean_hom, color='#e74c3c', lw=2.5, label='Mean attendance (100 seeds)')
    ax2.fill_between(time, mean_hom - std_hom, mean_hom + std_hom,
                     color='#e74c3c', alpha=0.3, label='±1 σ')
    ax2.axhline(T, color='gray', ls='--', lw=1.5, label=f'T={T}')
    ax2.set_xlabel('Round $t$', fontsize=11)
    ax2.set_ylabel('Attendance $A_t$', fontsize=11)
    ax2.set_title('Homogeneous population: 100 seeds', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9, loc='upper right')
    ax2.set_xlim(0, M)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Save
    report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report')
    fig.savefig(os.path.join(report_dir, 'section54_timeseries_100seeds.png'),
                dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: section54_timeseries_100seeds.png")
    plt.close(fig)
    
    # Print statistics
    print(f"\nHeterogeneous (100 seeds) - averages:")
    print(f"  Mean attendance: {np.mean(mean_het):.1f}")
    print(f"  Mean volatility (±1σ): {np.mean(std_het):.1f}")
    print(f"  Congestion rate: {np.mean(mean_het > T):.1%}")
    
    print(f"\nHomogeneous (100 seeds) - averages:")
    print(f"  Mean attendance: {np.mean(mean_hom):.1f}")
    print(f"  Mean volatility (±1σ): {np.mean(std_hom):.1f}")
    print(f"  Congestion rate: {np.mean(mean_hom > T):.1%}")
