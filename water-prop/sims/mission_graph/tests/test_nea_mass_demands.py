"""Tests for the closed-loop NEA vehicle mass-demand module (R-near-earth-asteroid).

Guards the load-bearing claim of the round: a near-Earth-asteroid vehicle on
40-kWe SOLAR-electric power closes the closed-loop dry-mass fixed point, where
the Saturn fission vehicle's closure inventory is 0/150 (titan-6). The seam the
NEA architecture reuses is the mission-agnostic `derive_dry_mass` iterator; only
the mission-specific demand functions change (framework-abstraction test, H6).
"""

from __future__ import annotations

from mission_graph.missions.nea_mass_demands import (
    NeaMassContext, derive_nea_vehicle, solar_powerplant_demand_kg,
    delivered_water_kg,
)
from mission_graph.missions.saturn_mass_demands import powerplant_demand_kg as saturn_pp
from mission_graph.missions.saturn_mass_demands import MassContext as SaturnCtx


def test_delivered_water_is_exactly_inputs():
    # 500 t boulder, 1.8% water, 90% extraction -> 8.1 t (NOT the SCOPE's 14 t).
    assert delivered_water_kg(500_000.0, 0.018, 0.90) == 500_000.0 * 0.018 * 0.90
    assert abs(delivered_water_kg(500_000.0, 0.018, 0.90) / 1000.0 - 8.1) < 1e-6
    # 3% reproduces the SCOPE's 14 t headline (~13.5 t).
    assert abs(delivered_water_kg(500_000.0, 0.030, 0.90) / 1000.0 - 13.5) < 1e-6


def test_solar_powerplant_is_far_lighter_than_fission():
    """The load-bearing axis: solar at 1 AU vs KRUSTY fission at the same power."""
    power_kwe = 40.0
    nea_ctx = NeaMassContext(boulder_mass_kg=500_000.0, power_available_kwe=power_kwe)
    solar_kg = solar_powerplant_demand_kg(nea_ctx)
    fission_kg = saturn_pp(SaturnCtx(chunk_mass_kg=200_000.0, power_available_kwe=power_kwe))
    # Solar (array+PMAD) is at least 10x lighter than reactor+MARVL+thrusters.
    assert solar_kg < fission_kg / 10.0
    # Sanity bounds on the solar stack (array 40000/150 ~267 kg + PMAD 120 kg).
    assert 300.0 < solar_kg < 800.0


def test_nea_mass_loop_converges_and_contains_powerplant():
    ctx = NeaMassContext(boulder_mass_kg=500_000.0, power_available_kwe=40.0)
    res = derive_nea_vehicle(ctx)
    assert res.converged
    pp_kg = solar_powerplant_demand_kg(ctx) + ctx.thrusters_kg_per_kwe * ctx.power_available_kwe
    # Self-consistent dry mass must be able to contain its own powerplant.
    assert res.dry_mass_kg > pp_kg
    # And the dry mass is a plausible single-vehicle figure (tens of tonnes).
    assert 20_000.0 < res.dry_mass_kg < 100_000.0


def test_reuses_framework_iterator_unchanged():
    """H6: NEA derivation goes through the mission-agnostic derive_dry_mass."""
    import mission_graph.framework as fw
    import mission_graph.missions.nea_mass_demands as nea
    # The NEA module imports the framework iterator rather than defining its own.
    assert nea.derive_dry_mass is fw.derive_dry_mass
