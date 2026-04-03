"""
Shared constants, colour palette, and output directory.
All other modules import from here.

Payoff convention (consistent with project spec):
  r = 1   if drive  AND  A <= T   (at most T drivers: road uncongested)
  r = 0   if drive  AND  A >  T   (more than T drivers: road congested)
  r = 0.3 if transit              (fixed utility of alternative transport)
"""

import os

# ---------------------------------------------------------------------------
# Game parameters
# ---------------------------------------------------------------------------
N       = 101     # number of agents
T       = 60      # congestion threshold
R_STAY  = 0.3     # utility of alternative transport (transit)
M       = 200     # rounds per repeated-game run
EPSILON = 0.05    # exploration probability (epsilon-greedy)
GAMMA   = 0.9     # predictor score decay factor
DELTA   = 5       # accuracy tolerance window for score update
K       = 6       # predictors assigned to each agent
WARMUP  = 10      # warm-up rounds to seed history (excluded from output)
SEEDS   = list(range(100))

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
COL_T   = '#e74c3c'
COL_NP  = '#27ae60'
COL_BR  = '#2980b9'
COL_IND = '#8e44ad'
COL_RND = '#e67e22'
COL_HOM = '#e74c3c'
COL_HET = '#27ae60'

# ---------------------------------------------------------------------------
# Output directory: figures are saved alongside the report so that
# Markdown image references resolve automatically.
# ---------------------------------------------------------------------------
_CODE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR   = os.path.join(os.path.dirname(_CODE_DIR), 'report')

# ---------------------------------------------------------------------------
# Predictor registry
# ---------------------------------------------------------------------------
PREDICTOR_NAMES = [
    "last", "avg3", "avg5", "avg7",
    "contrarian", "trend",
    "cong_mom", "thresh_prox",    # indices 6, 7 -- novel predictors
    "cycle2", "cycle3", "cycle5",
]
N_PREDICTORS = len(PREDICTOR_NAMES)   # 11
NOVEL_IDX    = [6, 7]                 # global indices of novel predictors
