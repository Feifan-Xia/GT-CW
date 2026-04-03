"""
Section 5.4: 100-seed homogeneous vs heterogeneous comparison with visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from minority_game import run_inductive

if __name__ == '__main__':
    from config import SEEDS
    
    print("[Section 5.4] Running 100-seed homogeneous vs heterogeneous comparison...")
    
    att_het_list = []
    att_hom_list = []
    
    # Run all 100 seeds
    for i, seed in enumerate(SEEDS):
        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/100 seeds...")
        
        rng = np.random.default_rng(seed)
        
        # Heterogeneous
        att_het, _, _ = run_inductive(rng, homogeneous=False)
        att_het_list.append(att_het)
        
        # Homogeneous
        rng2 = np.random.default_rng(seed + 1000)  # Different seed for homogeneous to get different shared pool
        att_hom, _, _ = run_inductive(rng2, homogeneous=True)
        att_hom_list.append(att_hom)
    
    # Compute statistics
    from minority_game import T
    
    het_means = np.array([np.mean(a) for a in att_het_list])
    het_stds = np.array([np.std(a) for a in att_het_list])
    het_congs = np.array([np.mean(a > T) for a in att_het_list])
    
    hom_means = np.array([np.mean(a) for a in att_hom_list])
    hom_stds = np.array([np.std(a) for a in att_hom_list])
    hom_congs = np.array([np.mean(a > T) for a in att_hom_list])
    
    print(f"\nHeterogeneous (100 seeds):")
    print(f"  Mean attendance: {np.mean(het_means):.1f} ± {np.std(het_means):.1f}")
    print(f"  Std attendance: {np.mean(het_stds):.1f} ± {np.std(het_stds):.1f}")
    print(f"  Congestion rate: {np.mean(het_congs):.1%} ± {np.std(het_congs):.1%}")
    
    print(f"\nHomogeneous (100 seeds):")
    print(f"  Mean attendance: {np.mean(hom_means):.1f} ± {np.std(hom_means):.1f}")
    print(f"  Std attendance: {np.mean(hom_stds):.1f} ± {np.std(hom_stds):.1f}")
    print(f"  Congestion rate: {np.mean(hom_congs):.1%} ± {np.std(hom_congs):.1%}")
    
    # Create comprehensive visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    
    # Plot 1: Mean attendance distribution
    axes[0, 0].hist(het_means, bins=15, alpha=0.6, label='Heterogeneous', color='#27ae60', edgecolor='black')
    axes[0, 0].hist(hom_means, bins=15, alpha=0.6, label='Homogeneous', color='#e74c3c', edgecolor='black')
    axes[0, 0].axvline(T, color='gray', ls='--', lw=2, label=f'$T={T}$')
    axes[0, 0].set_xlabel('Mean Attendance', fontsize=11)
    axes[0, 0].set_ylabel('Frequency', fontsize=11)
    axes[0, 0].set_title('Distribution of Mean Attendance (100 seeds)', fontsize=11, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # Plot 2: Std attendance distribution
    axes[0, 1].hist(het_stds, bins=15, alpha=0.6, label='Heterogeneous', color='#27ae60', edgecolor='black')
    axes[0, 1].hist(hom_stds, bins=15, alpha=0.6, label='Homogeneous', color='#e74c3c', edgecolor='black')
    axes[0, 1].set_xlabel('Attendance Std Dev', fontsize=11)
    axes[0, 1].set_ylabel('Frequency', fontsize=11)
    axes[0, 1].set_title('Distribution of Attendance Volatility (100 seeds)', fontsize=11, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # Plot 3: Congestion rate distribution
    axes[1, 0].hist(het_congs * 100, bins=15, alpha=0.6, label='Heterogeneous', color='#27ae60', edgecolor='black')
    axes[1, 0].hist(hom_congs * 100, bins=15, alpha=0.6, label='Homogeneous', color='#e74c3c', edgecolor='black')
    axes[1, 0].set_xlabel('Congestion Rate (%)', fontsize=11)
    axes[1, 0].set_ylabel('Frequency', fontsize=11)
    axes[1, 0].set_title('Distribution of Congestion Rate (100 seeds)', fontsize=11, fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # Plot 4: Scatter plot of mean vs std
    axes[1, 1].scatter(het_means, het_stds, alpha=0.6, s=50, color='#27ae60', 
                      label='Heterogeneous', edgecolors='black', linewidth=0.5)
    axes[1, 1].scatter(hom_means, hom_stds, alpha=0.6, s=50, color='#e74c3c',
                      label='Homogeneous', edgecolors='black', linewidth=0.5)
    axes[1, 1].axvline(T, color='gray', ls='--', lw=1.5, label=f'$T={T}$')
    axes[1, 1].set_xlabel('Mean Attendance', fontsize=11)
    axes[1, 1].set_ylabel('Attendance Std Dev', fontsize=11)
    axes[1, 1].set_title('Mean vs Volatility Trade-off (100 seeds)', fontsize=11, fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report')
    fig.savefig(os.path.join(report_dir, 'section54_homogeneous_100seeds.png'),
                dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved: {os.path.join(report_dir, 'section54_homogeneous_100seeds.png')}")
    plt.close(fig)
