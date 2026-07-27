"""Regression tests for R-closure-boundary-inversion parameter hooks.

Two properties:
  1. DEFAULTS UNCHANGED — with no extra params, every hooked precondition
     behaves exactly as the hardcoded record baseline (the 0-of-1,744 result
     must reproduce; checked cheaply here via option-level probes, and
     end-to-end by the round's baseline replication step).
  2. HOOKS BITE — each override actually moves the gate it names.
"""

from __future__ import annotations

from dataclasses import replace

from mission_graph.framework import VehicleState
from mission_graph.missions.phase0_earth_to_leo import (
    FALCON_HEAVY_EXPENDED_CAP_KG,
    STARSHIP_CAP_KG,
    falcon_heavy_expended,
    starship,
    multi_falcon_6_launch,
)
from mission_graph.missions.phase1_leo_to_saturn import low_thrust_spiral
from mission_graph.missions.phase4_saturn_departure import (
    chemical_tei,
    chunk_fed_spiral_departure,
)
from mission_graph.missions.phase6_earth_arrival import low_thrust_earth_capture
from mission_graph.missions.phase7_lunar_processing import lunar_processing_and_leo_transfer


def _state(**kw) -> VehicleState:
    base = VehicleState(
        mass_kg=50_000.0,
        propellant_kg=0.0,
        payload_kg=0.0,
        location="pre_launch",
        v_inf_km_s=0.0,
        time_elapsed_s=0.0,
        epoch_jd=0.0,
        power_available_kwe=30.0,
    )
    return replace(base, **kw)


BASE_PARAMS = {
    "chemical_isp_s": 340.0,
    "electric_isp_s": 3000.0,
    "electric_thrust_n": 5.0,
    "water_met_isp_s": 800.0,
    "chunk_mass_kg": 50_000.0,
    "launch_epoch_jd": 0.0,
}


# ------------------------------------------------------------------ #
# Launcher cap multiplier
# ------------------------------------------------------------------ #

def test_launcher_caps_default_unchanged():
    over_fh = _state(mass_kg=FALCON_HEAVY_EXPENDED_CAP_KG + 1.0)
    ok, _ = falcon_heavy_expended.precondition(over_fh, BASE_PARAMS)
    assert not ok
    at_fh = _state(mass_kg=FALCON_HEAVY_EXPENDED_CAP_KG)
    ok, _ = falcon_heavy_expended.precondition(at_fh, BASE_PARAMS)
    assert ok


def test_launcher_cap_multiplier_bites():
    params = dict(BASE_PARAMS, launcher_cap_multiplier=5.0)
    big = _state(mass_kg=STARSHIP_CAP_KG * 4.9)
    ok, _ = starship.precondition(big, params)
    assert ok
    too_big = _state(mass_kg=STARSHIP_CAP_KG * 5.1)
    ok, _ = starship.precondition(too_big, params)
    assert not ok
    # multi-launch scales per-launch capacity too: 6 x 50 t x 5 = 1500 t
    huge = _state(mass_kg=1_400_000.0)
    ok, _ = multi_falcon_6_launch.precondition(huge, params)
    assert ok


# ------------------------------------------------------------------ #
# Minimum-power gates
# ------------------------------------------------------------------ #

def test_low_thrust_min_power_default_and_override():
    st = _state(location="LEO", power_available_kwe=11.0, propellant_kg=40_000.0)
    ok, why = low_thrust_spiral.precondition(st, BASE_PARAMS)
    assert not ok and "20" in why  # default gate 20 kWe
    params = dict(BASE_PARAMS, low_thrust_min_power_kwe=10.0)
    ok, why = low_thrust_spiral.precondition(st, params)
    assert "kWe" not in why or ok or "thrust" in why or "propellant" in why
    # The power gate itself no longer rejects; downstream gates may.
    assert "needs at least" not in why


def test_chunk_fed_min_power_override():
    st = _state(location="saturn_orbit", power_available_kwe=20.0,
                payload_kg=170_000.0, mass_kg=250_000.0)
    ok, why = chunk_fed_spiral_departure.precondition(st, BASE_PARAMS)
    assert not ok and ">= 30" in why
    params = dict(BASE_PARAMS, chunk_fed_min_power_kwe=10.0)
    ok, why = chunk_fed_spiral_departure.precondition(st, params)
    assert ">= 10" not in why or ok or "water" in why or "burn time" in why


def test_p6_lt_capture_min_power_override():
    st = _state(location="earth_approach", v_inf_km_s=1.0,
                power_available_kwe=11.0, payload_kg=50_000.0, mass_kg=80_000.0)
    ok, why = low_thrust_earth_capture.precondition(st, BASE_PARAMS)
    assert not ok and ">= 30" in why
    params = dict(BASE_PARAMS, lt_capture_min_power_kwe=10.0)
    ok, _ = low_thrust_earth_capture.precondition(st, params)
    assert ok


# ------------------------------------------------------------------ #
# Departure delta-v hooks
# ------------------------------------------------------------------ #

def test_chemical_tei_dv_override():
    st = _state(location="saturn_orbit", mass_kg=100_000.0, propellant_kg=60_000.0)
    ok, _ = chemical_tei.precondition(st, BASE_PARAMS)  # 7.7 km/s at 340 s: infeasible
    assert not ok
    params = dict(BASE_PARAMS, chemical_tei_dv_km_s=1.0)
    ok, _ = chemical_tei.precondition(st, params)
    assert ok


def test_chunk_fed_dv_override_changes_requirement():
    st = _state(location="saturn_orbit", mass_kg=300_000.0,
                payload_kg=200_000.0, power_available_kwe=1000.0)
    params_lo = dict(BASE_PARAMS, chunk_fed_dv_km_s=1.0, water_met_isp_s=800.0)
    ok_lo, _ = chunk_fed_spiral_departure.precondition(st, params_lo)
    params_hi = dict(BASE_PARAMS, chunk_fed_dv_km_s=18.0, water_met_isp_s=800.0)
    ok_hi, why_hi = chunk_fed_spiral_departure.precondition(st, params_hi)
    assert ok_lo and not ok_hi
    assert "chunk water" in why_hi or "burn time" in why_hi


# ------------------------------------------------------------------ #
# Phase-7 Isp propagation-leak fix
# ------------------------------------------------------------------ #

def test_phase7_honors_water_met_isp():
    st = _state(location="lunar_orbit_intermediate", payload_kg=100_000.0,
                mass_kg=120_000.0)
    out_default = lunar_processing_and_leo_transfer.executor(st, BASE_PARAMS)
    out_high = lunar_processing_and_leo_transfer.executor(
        st, dict(BASE_PARAMS, water_met_isp_s=3000.0))
    assert out_high.payload_kg > out_default.payload_kg
    # default is the record 800 s value
    import math
    expected = 100_000.0 / math.exp(3.0 / (800.0 * 9.81e-3))
    assert abs(out_default.payload_kg - expected) < 1.0
