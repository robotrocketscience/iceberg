"""Make `mission_graph` importable from the tests directory."""

import sys
from pathlib import Path

# water-prop/sims/ on the path so `from mission_graph.framework import ...` works
_SIMS_DIR = Path(__file__).resolve().parents[2]
if str(_SIMS_DIR) not in sys.path:
    sys.path.insert(0, str(_SIMS_DIR))
