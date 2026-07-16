"""Constraint 1 (reactor lifetime vs cumulative full-power burn) tests.

R-framework-matrix-parity (titan-4). Ground-truth anchor: enceladus-r5
R-reactor-lifetime-vs-burn-time — KRUSTY 28-h flight heritage, Kilopower 10-yr
design target, ~11-12 yr cumulative burn at the megawatt cells it falsified.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mission_graph.framework import VehicleState  # noqa: E402
from mission_graph.missions.powerplant_constraints import (  # noqa: E402
    electric_burn_hours,
    lifetime_ok,
)


def _state(cumulative_hours: float = 0.0) -> VehicleState:
    return VehicleState(
        mass_kg=100_000.0,
        propellant_kg=0.0,
        payload_kg=0.0,
        location="saturn_orbit",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=None,
        power_available_kwe=30.0,
        cumulative_full_power_burn_hours=cumulative_hours,
    )


def test_state_defaults_cumulative_burn_to_zero():
    s = VehicleState(
        mass_kg=1.0, propellant_kg=0.0, payload_kg=0.0, location="x",
        v_inf_km_s=0.0, time_elapsed_s=0.0, epoch_jd=None, power_available_kwe=1.0,
    )
    assert s.cumulative_full_power_burn_hours == 0.0


def test_electric_burn_hours_zero_for_no_power_or_no_propellant():
    assert electric_burn_hours(1000.0, 800.0, 0.0) == 0.0
    assert electric_burn_hours(0.0, 800.0, 30.0) == 0.0


def test_electric_burn_hours_scales_with_propellant_and_inverse_power():
    # F = 2P/v_e; burn_s = m_prop * v_e^2 / (2P). Doubling propellant doubles
    # the burn; doubling power halves it.
    base = electric_burn_hours(10_000.0, 2000.0, 30.0)
    assert electric_burn_hours(20_000.0, 2000.0, 30.0) == 2 * base
    assert math.isclose(electric_burn_hours(10_000.0, 2000.0, 60.0), base / 2)


def test_lifetime_nonbinding_by_default():
    # No reactor_lifetime_years param -> always feasible regardless of burn.
    ok, _ = lifetime_ok(_state(cumulative_hours=10 * 8760), {}, 50 * 8760.0)
    assert ok is True


def test_lifetime_nonbinding_when_infinite():
    ok, _ = lifetime_ok(_state(), {"reactor_lifetime_years": math.inf}, 1e9)
    assert ok is True


def test_lifetime_binds_when_projected_exceeds_ceiling():
    # 4 yr already on the clock + a 2 yr burn = 6 yr projected; ceiling 5 yr.
    s = _state(cumulative_hours=4.0 * 8760)
    ok, why = lifetime_ok(s, {"reactor_lifetime_years": 5.0}, 2.0 * 8760)
    assert ok is False
    assert "reactor lifetime 5" in why


def test_lifetime_survives_under_ceiling():
    # 4 yr + 2 yr = 6 yr projected; ceiling 10 yr (Kilopower design target).
    s = _state(cumulative_hours=4.0 * 8760)
    ok, _ = lifetime_ok(s, {"reactor_lifetime_years": 10.0}, 2.0 * 8760)
    assert ok is True


def test_kilopower_28h_heritage_is_orders_of_magnitude_short():
    # enceladus-r5 ground truth: KRUSTY flight heritage 28 h vs a multi-year
    # mission burn. A reactor with a 28-h lifetime fails any non-trivial burn.
    s = _state()
    krusty_lifetime_years = 28.0 / 8760.0
    ok, _ = lifetime_ok(s, {"reactor_lifetime_years": krusty_lifetime_years}, 1.0 * 8760)
    assert ok is False
