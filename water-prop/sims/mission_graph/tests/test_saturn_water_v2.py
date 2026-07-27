"""Tests for saturn_water_v2 (electrolysis H2/O2 departure stage)."""

from __future__ import annotations

import math
from dataclasses import replace

from mission_graph.framework import VehicleState
from mission_graph.missions.phase4_electrolysis import (
    ELECTROLYSIS_ENERGY_KWH_PER_KG,
    ELECTROLYSIS_ISP_S,
    ELECTROLYSIS_TEI_DV_KM_S,
    electrolysis_kick_departure,
    phase4_v2,
)
from mission_graph.missions.saturn_mass_demands import (
    KEY_CRYO_TANKAGE,
    KEY_ISRU_PLANT,
    MassContext,
    derive_saturn_vehicle,
    make_saturn_demand_fn,
)
from mission_graph.missions.saturn_water_v1 import saturn_water_v1
from mission_graph.missions.saturn_water_v2 import saturn_water_v2


PARAMS = {
    "chemical_isp_s": 340.0,
    "water_met_isp_s": 800.0,
}


def _state(**kw) -> VehicleState:
    # NOTE the fixture ratio: at 8.51 km/s and 450 s the mass ratio is ~6.9,
    # so the burn consumes ~85 percent of the departure stack — the chunk
    # (payload) must be most of the stack for the option to be feasible.
    base = VehicleState(
        mass_kg=400_000.0, propellant_kg=10_000.0, payload_kg=350_000.0,
        location="saturn_orbit", v_inf_km_s=0.0, time_elapsed_s=0.0,
        epoch_jd=0.0, power_available_kwe=150.0,
    )
    return replace(base, **kw)


# ------------------------------------------------------------------ #
# Mission wiring
# ------------------------------------------------------------------ #

def test_v2_phase_sequence_swaps_only_phase4():
    v1_ids = [p.phase_id for p in saturn_water_v1.phase_sequence]
    v2_ids = [p.phase_id for p in saturn_water_v2.phase_sequence]
    assert v1_ids == v2_ids
    p4 = [p for p in saturn_water_v2.phase_sequence if p.phase_id == "P4_Saturn_departure"][0]
    assert p4 is phase4_v2
    ids = [o.option_id for o in p4.options]
    assert "electrolysis_kick_departure" in ids
    assert "chunk_fed_spiral_departure" in ids  # v0 options retained


def test_v2_reuses_v1_closure_predicates():
    assert saturn_water_v2.closure_predicates is saturn_water_v1.closure_predicates


# ------------------------------------------------------------------ #
# Option physics
# ------------------------------------------------------------------ #

def test_electrolysis_propellant_drawn_from_chunk():
    st = _state()
    ok, why = electrolysis_kick_departure.precondition(st, PARAMS)
    assert ok, why
    out = electrolysis_kick_departure.executor(st, PARAMS)
    ve = ELECTROLYSIS_ISP_S * 9.81e-3
    expected_burn = st.mass_kg * (1.0 - math.exp(-ELECTROLYSIS_TEI_DV_KM_S / ve))
    assert abs((st.payload_kg - out.payload_kg) - expected_burn) < 1.0
    assert out.location == "earth_approach"
    assert out.v_inf_km_s == 10.0


def test_electrolysis_dwell_gate_kills_kilopower():
    st = _state(power_available_kwe=30.0)
    ok, why = electrolysis_kick_departure.precondition(st, PARAMS)
    # ~342 t propellant x 6.7 kWh/kg / 30 kWe = ~8.7 yr > 3 yr ceiling
    assert not ok and "dwell ceiling" in why


def test_electrolysis_charges_reactor_lifetime():
    st = _state()
    out = electrolysis_kick_departure.executor(st, PARAMS)
    burned = st.payload_kg - out.payload_kg
    expected_hours = burned * ELECTROLYSIS_ENERGY_KWH_PER_KG / st.power_available_kwe
    assert abs(out.cumulative_full_power_burn_hours - expected_hours) < 1.0
    params = dict(PARAMS, reactor_lifetime_years=1.0)
    ok, why = electrolysis_kick_departure.precondition(st, params)
    assert not ok and "lifetime" in why


def test_electrolysis_insufficient_chunk_water():
    st = _state(payload_kg=10_000.0)
    ok, why = electrolysis_kick_departure.precondition(st, PARAMS)
    assert not ok and "chunk water" in why


# ------------------------------------------------------------------ #
# Mass model
# ------------------------------------------------------------------ #

def test_mass_context_default_is_v1_identical():
    ctx_v1 = MassContext(chunk_mass_kg=100_000.0, power_available_kwe=30.0)
    demands = make_saturn_demand_fn(ctx_v1)(60_000.0)
    assert KEY_ISRU_PLANT not in demands
    assert KEY_CRYO_TANKAGE not in demands


def test_electrolysis_stage_adds_plant_and_cryo_terms():
    ctx = MassContext(chunk_mass_kg=100_000.0, power_available_kwe=150.0,
                      electrolysis_stage=True)
    demands = make_saturn_demand_fn(ctx)(60_000.0)
    assert demands[KEY_ISRU_PLANT] == 20.0 * 150.0
    f_burn = 1.0 - math.exp(-8.51 * 1000.0 / (9.81 * 450.0))
    assert abs(demands[KEY_CRYO_TANKAGE] - 0.06 * f_burn * 160_000.0) < 1.0
    r_v1 = derive_saturn_vehicle(MassContext(chunk_mass_kg=100_000.0,
                                             power_available_kwe=150.0))
    r_v2 = derive_saturn_vehicle(ctx)
    assert r_v2.converged and r_v2.dry_mass_kg > r_v1.dry_mass_kg
