"""Constraint 4 (vis-viva LEO capture-burn correction) tests.

R-framework-matrix-parity (titan-4). Ground truth: titan-3
R-delta-velocity-anchor-audit (42120cf) — 7.3 km/s direct capture at v_inf ~10.3,
4.2 km/s post-lunar-GA at residual v_inf ~4.47.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mission_graph.missions.phase6_earth_arrival import (  # noqa: E402
    direct_propulsive_capture_dv,
)


def test_legacy_formula_is_default():
    # No params, or visviva off -> legacy 0.4*v_inf + 0.3.
    assert abs(direct_propulsive_capture_dv(10.0) - 4.3) < 1e-9
    assert abs(direct_propulsive_capture_dv(10.0, {}) - 4.3) < 1e-9
    assert abs(direct_propulsive_capture_dv(10.0, {"visviva_capture": False}) - 4.3) < 1e-9


def test_visviva_reproduces_titan3_direct_anchor():
    # titan-3: direct capture from v_inf 10.3 = 7.3 km/s.
    dv = direct_propulsive_capture_dv(10.3, {"visviva_capture": True})
    assert abs(dv - 7.3) < 0.05


def test_visviva_reproduces_titan3_post_lga_anchor():
    # titan-3: post-lunar-GA residual v_inf 4.47 -> ~4.1-4.2 km/s capture.
    dv = direct_propulsive_capture_dv(4.47, {"visviva_capture": True})
    assert abs(dv - 4.2) < 0.2


def test_visviva_has_escape_velocity_floor_at_low_vinf():
    # Legacy gives 0.7 km/s at v_inf=1; vis-viva floor is ~3.2 km/s (you must
    # still slow from escape to circular even at v_inf -> 0).
    legacy = direct_propulsive_capture_dv(1.0)
    visviva = direct_propulsive_capture_dv(1.0, {"visviva_capture": True})
    assert abs(legacy - 0.7) < 1e-9
    assert visviva > 3.0
    assert visviva > legacy + 2.0


def test_visviva_monotonic_in_vinf():
    f = lambda v: direct_propulsive_capture_dv(v, {"visviva_capture": True})
    assert f(1.0) < f(5.0) < f(10.0)
