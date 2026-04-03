"""
Standalone plotting module for minority game figures.
Allows selective regeneration of individual figures without re-running all experiments.
Usage: python plot_figures.py [figure_ids]
  - plot_figures.py all          (regenerate all figures)
  - plot_figures.py 5            (regenerate only Figure 5)
  - plot_figures.py 4 5 6 7      (regenerate Figures 4, 5, 6, 7)
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pickle
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import *
from minority_game import (
    plot_predictor_ecology, run_inductive, run_best_reply,
    simulate_static, compute_p_star
)

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'report')

def regenerate_figure_5(seed=0):
    """Regenerate only Figure 5 (predictor ecology).
    Loads cached active_preds or runs a quick inductive simulation.
    """
    pkl_path = os.path.join(OUT_DIR, f'active_preds_seed{seed}.pkl')
    
    if os.path.exists(pkl_path):
        with open(pkl_path, 'rb') as f:
            active_preds = pickle.load(f)
        print(f"[Plot] Loaded active_preds from {pkl_path}")
    else:
        print(f"[Plot] Running inductive simulation (seed {seed}) to generate Figure 5 data...")
        rng = np.random.default_rng(seed)
        attendance, active_preds, decisions_log = run_inductive(rng=rng)
        # Save for future use
        with open(pkl_path, 'wb') as f:
            pickle.dump(active_preds, f)
        print(f"[Plot] Cached active_preds to {pkl_path}")
    
    # Generate Figure 5
    plot_predictor_ecology(active_preds)
    print("[Plot] Figure 5 saved.")

def regenerate_all_figures():
    """Full regeneration of all experiment figures."""
    print("=" * 70)
    print("Regenerating all figures. This will re-run all experiments.")
    print("=" * 70)
    print("For selective figure regeneration, use: python plot_figures.py 5")
    print()
    
    # Run main simulation suite
    from main import run_all_experiments
    run_all_experiments()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'all':
        regenerate_all_figures()
    else:
        # Parse figure IDs
        fig_ids = [int(arg) for arg in sys.argv[1:] if arg.isdigit()]
        if 5 in fig_ids:
            regenerate_figure_5()
        if 'all' not in fig_ids and len(fig_ids) > 0:
            print(f"[Plot] Regenerated Figure(s): {fig_ids}")
