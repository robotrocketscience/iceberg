"""Closed-loop dry-mass derivation tests (R-vehicle-mass-closure-refactor).

Pins the generic fixed-point iterator (framework/dry_mass.py) and the Saturn
subsystem demand functions (missions/saturn_mass_demands.py):
  - convergence + contraction for a well-posed demand,
  - non-convergence as a returned result (not raised) for a non-contracting map,
  - breakdown/subtotal/margin invariants,
  - launch wet/propellant back-out,
  - Saturn powerplant-demand reuse of the locked-belief anchor (decision D1),
  - the load-bearing fact that derived dry mass exceeds the open-loop
    "too-light" swept floor at the audit canonical cell.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mission_graph.framework import (  # noqa: E402
    DerivationResult,
    derive_dry_mass,
    launch_wet_and_propellant,
)
from mission_graph.missions.saturn_mass_demands import (  # noqa: E402
    MassContext,
    KEY_POWERPLANT,
    KEY_TANKAGE,
    derive_saturn_vehicle,
    make_saturn_demand_fn,
    powerplant_demand_kg,
)
from mission_graph.missions.powerplant_constraints import required_powerplant_mass_kg


# -------------------------------------------------------------------- #
# Generic iterator
# -------------------------------------------------------------------- #

def test_constant_demand_converges_to_margined_sum():
    # Demand independent of dry mass: fixed point is exactly (1+margin)*sum.
    def demand(_dry):
        return {"a": 10_000.0, "b": 5_000.0}
    r = derive_dry_mass(demand, dry_margin=0.20)
    assert r.converged
    assert abs(r.dry_mass_kg - 1.20 * 15_000.0) < 1.0
    assert abs(r.subsystem_subtotal_kg - 15_000.0) < 1.0


def test_linear_coupling_converges_when_contraction():
    # demand has a term k*dry; map x -> (1+m)*(fixed + k*x) contracts iff
    # (1+m)*k < 1. Here (1.2)*(0.2) = 0.24 < 1.
    def demand(dry):
        return {"fixed": 10_000.0, "coupled": 0.2 * dry}
    r = derive_dry_mass(demand, dry_margin=0.20)
    assert r.converged
    # closed form: x = 1.2*10000 / (1 - 1.2*0.2) = 12000 / 0.76. Iterator stops
    # at rel_step < tol (1e-3), so compare within that relative tolerance.
    fixed_point = 12_000.0 / 0.76
    assert abs(r.dry_mass_kg - fixed_point) / fixed_point < 2e-3


def test_noncontracting_map_returns_nonconverged_not_raised():
    # (1+m)*k = 1.2*1.0 = 1.2 > 1: diverges. Must return converged=False.
    def demand(dry):
        return {"runaway": 1.0 * dry, "seed": 1_000.0}
    r = derive_dry_mass(demand, dry_margin=0.20, max_iter=80)
    assert isinstance(r, DerivationResult)
    assert not r.converged
    assert r.nonconvergence_reason  # populated


def test_breakdown_consistent_with_dry_mass_when_converged():
    def demand(dry):
        return {"fixed": 8_000.0, "coupled": 0.1 * dry}
    r = derive_dry_mass(demand, dry_margin=0.20)
    assert r.converged
    assert abs((1.0 + r.dry_margin) * r.subsystem_subtotal_kg - r.dry_mass_kg) < 1.0


def test_iterator_rejects_bad_inputs():
    def demand(_dry):
        return {"a": 1.0}
    with pytest.raises(ValueError):
        derive_dry_mass(demand, initial_guess_kg=0.0)
    with pytest.raises(ValueError):
        derive_dry_mass(demand, dry_margin=-0.1)
    with pytest.raises(ValueError):
        derive_dry_mass(demand, max_iter=0)


# -------------------------------------------------------------------- #
# launch_wet_and_propellant
# -------------------------------------------------------------------- #

def test_launch_wet_and_propellant_080_fraction():
    wet, prop = launch_wet_and_propellant(20_000.0, 0.80)
    assert abs(wet - 100_000.0) < 1e-6   # 20t dry / 0.2 = 100t wet
    assert abs(prop - 80_000.0) < 1e-6
    assert abs((wet - prop) - 20_000.0) < 1e-6  # dry recovered


def test_launch_wet_rejects_out_of_range_fraction():
    with pytest.raises(ValueError):
        launch_wet_and_propellant(10_000.0, 1.0)
    with pytest.raises(ValueError):
        launch_wet_and_propellant(10_000.0, -0.1)


# -------------------------------------------------------------------- #
# Saturn demands (decision D1 reuse, coupling, canonical cell)
# -------------------------------------------------------------------- #

def test_powerplant_demand_reuses_locked_anchor():
    ctx = MassContext(chunk_mass_kg=50_000.0, power_available_kwe=30.0)
    assert powerplant_demand_kg(ctx) == required_powerplant_mass_kg(
        30.0, {"reactor_specific_power_w_per_kg": 2.4}
    )
    # 12500 reactor + 8000 radiator + 300 thrusters = 20800 kg at 30 kWe
    assert abs(powerplant_demand_kg(ctx) - 20_800.0) < 1.0


def test_tankage_is_the_dry_to_propellant_coupling():
    ctx = MassContext(chunk_mass_kg=50_000.0, power_available_kwe=10.0)
    fn = make_saturn_demand_fn(ctx)
    # tankage scales with trial dry mass; everything else is constant.
    b1 = fn(20_000.0)
    b2 = fn(40_000.0)
    assert b2[KEY_TANKAGE] > b1[KEY_TANKAGE]
    assert b1[KEY_POWERPLANT] == b2[KEY_POWERPLANT]
    # tankage = 0.05 * (f/(1-f)) * dry = 0.05 * 4 * dry at f=0.80
    assert abs(b1[KEY_TANKAGE] - 0.05 * 4.0 * 20_000.0) < 1e-6


def test_saturn_vehicle_converges_at_canonical_audit_cell():
    # 200 t chunk, 30 kWe single-pass trawl, hybrid aerocapture.
    ctx = MassContext(chunk_mass_kg=200_000.0, power_available_kwe=30.0)
    r = derive_saturn_vehicle(ctx)
    assert r.converged
    # H3 pre-registered bracket is [35,65] t DRY; the derived value lands
    # ABOVE it (~121 t) — H3 falsified. This test pins the falsification
    # so a future anchor change that moves it back into bracket is visible.
    assert r.dry_mass_kg / 1000.0 > 65.0
    assert 115.0 < r.dry_mass_kg / 1000.0 < 130.0


def test_derived_dry_exceeds_open_loop_too_light_floor():
    # The 16 open-loop closers were 50-100 t WET = 10-20 t DRY at 30-55 kWe.
    # Closed-loop dry mass at those coords is far larger -> they were vehicles
    # lighter than their own powerplant. Pin that the derived dry exceeds the
    # 20 t too-light ceiling at every open-loop-closer coordinate.
    for power in (30.0, 55.0):
        for chunk_t in (200.0,):
            ctx = MassContext(chunk_mass_kg=chunk_t * 1000.0, power_available_kwe=power)
            r = derive_saturn_vehicle(ctx)
            assert r.converged
            assert r.dry_mass_kg / 1000.0 > 20.0


def test_demonstrator_minimum_dry_mass_above_bracket():
    # H5 pre-registered [12,25] t. Smallest-chunk / lowest-power cell.
    ctx = MassContext(chunk_mass_kg=10_000.0, power_available_kwe=1.0, electric_thrust_n=1.0)
    r = derive_saturn_vehicle(ctx)
    assert r.converged
    # ~27.7 t -> just ABOVE the bracket (H5 falsified). Pin it.
    assert r.dry_mass_kg / 1000.0 > 25.0
    # And confirm it is TPS-sensitive: dropping aerocapture intent lowers it.
    ctx_no_tps = MassContext(
        chunk_mass_kg=10_000.0, power_available_kwe=1.0, electric_thrust_n=1.0,
        plans_aerocapture=False,
    )
    r2 = derive_saturn_vehicle(ctx_no_tps)
    assert r2.dry_mass_kg < r.dry_mass_kg


def test_high_propellant_fraction_can_break_convergence():
    # At very high propellant fraction the tankage coupling can stop being a
    # contraction: (1+m)*0.05*f/(1-f). At f=0.96: 1.2*0.05*24 = 1.44 > 1.
    ctx = MassContext(chunk_mass_kg=50_000.0, power_available_kwe=10.0, propellant_fraction=0.96)
    r = derive_saturn_vehicle(ctx)
    assert not r.converged
