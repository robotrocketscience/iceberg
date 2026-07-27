"""R-closing-path-self-consistency — ledger walk (H1) + corrected-kick re-sweep (H2-H4).

See STUDY.md. Run from project root:
  cd water-prop && uv run python rounds/R_closing_path_self_consistency/run.py
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import replace
from pathlib import Path


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[2] / "sims"
    for p in (sims_dir, sims_dir / "mission_graph" / "missions" / "sweeps"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))


_ensure_import_path()

import mission_graph.missions.phase1_leo_to_saturn as p1mod  # noqa: E402
from mission_graph.framework import Mission, Option, Phase, walk  # noqa: E402
from mission_graph.missions.saturn_water_v1 import (  # noqa: E402
    saturn_water_v1, context_from_coords, make_derived_mass_transform,
)
from mission_graph.missions.saturn_mass_demands import derive_saturn_vehicle  # noqa: E402
from saturn_water_v1_closure_sweep import (  # noqa: E402
    base_params, run_closed_loop, cell_closes, _base_state,
)

RESULTS = Path(__file__).parent / "results"
RESULTS.mkdir(exist_ok=True)

G0 = 9.81
MAX_MANIFEST_KG = 300_000.0   # most permissive: six-Falcon-Heavy raw deliverable

CLOSING_COORDS = {"power_kwe": 30.0, "chunk_mass_kg": 200_000.0, "electric_thrust_n": 5.0}
CLOSING_PATH_OPTIONS = (
    "multi_falcon_4_launch", "autonomous_assembly", "falcon_heavy_plus_helios_kick",
    "mars_jupiter_gravity_assist", "direct_chemical_capture", "single_pass_trawl",
    "chunk_fed_spiral_departure", "inbound_ballistic", "hybrid_aerocapture_aerobraking",
    "passthrough_already_at_leo",
)


# ------------------------------------------------------------------ #
# H1: ledger walk of the exact closing path
# ------------------------------------------------------------------ #

def ledger_walk():
    bp = dict(base_params())
    bp["propellant_fraction"] = 0.20
    ctx = context_from_coords(CLOSING_COORDS, bp)
    derived = derive_saturn_vehicle(ctx)
    dry = derived.dry_mass_kg

    transform = make_derived_mass_transform(bp)
    state = _base_state()
    state = replace(state, power_available_kwe=CLOSING_COORDS["power_kwe"])
    bp["chunk_mass_kg"] = CLOSING_COORDS["chunk_mass_kg"]
    bp["electric_thrust_n"] = CLOSING_COORDS["electric_thrust_n"]
    state = transform(state, CLOSING_COORDS)

    print(f"derived dry mass: {dry/1000:.1f} t  (launch wet {state.mass_kg/1000:.1f} t, "
          f"propellant {state.propellant_kg/1000:.1f} t)")

    # Walk phase by phase, choosing exactly the closing path's options.
    option_iter = iter(CLOSING_PATH_OPTIONS)
    violations = []
    rows = []
    for phase in saturn_water_v1.phase_sequence:
        want = next(option_iter)
        opt = next(o for o in phase.options if o.option_id == want)
        ok, why = opt.precondition(state, bp)
        if not ok:
            print(f"  !! precondition fails at {phase.phase_id}.{want}: {why}")
            return None
        state = opt.executor(state, bp)
        hardware_floor = dry  # vehicle hardware cannot be expelled (no jettison modeled on this path)
        violated = state.mass_kg < hardware_floor - 1.0
        if violated:
            violations.append(phase.phase_id)
        rows.append({
            "node": f"{phase.phase_id}.{want}",
            "mass_t": state.mass_kg / 1000.0,
            "propellant_t": state.propellant_kg / 1000.0,
            "payload_t": state.payload_kg / 1000.0,
            "years": state.time_elapsed_s / (365.25 * 86400.0),
            "mass_below_derived_dry": bool(violated),
        })
        flag = "  << BELOW DERIVED DRY" if violated else ""
        print(f"  {phase.phase_id:>22s}.{want:<32s} mass={state.mass_kg/1000:>7.1f}t "
              f"prop={state.propellant_kg/1000:>6.1f}t payload={state.payload_kg/1000:>6.1f}t{flag}")
    return {"derived_dry_t": dry / 1000.0, "rows": rows, "violations": violations}


# ------------------------------------------------------------------ #
# H2-H4: corrected kick model (self-consistent stack), round-local patch
# ------------------------------------------------------------------ #

def _corrected_kick(kick_dv_km_s, kick_dry_kg, kick_isp_s, option_id, desc):
    """Kick must push itself + vehicle; stack gated by the max launch manifest."""

    def stack_propellant(vehicle_wet_kg):
        # kick_prop = (vehicle + kick_dry + kick_prop) * (1 - e^{-dv/(g isp)})
        f_burn = 1.0 - math.exp(-kick_dv_km_s * 1000.0 / (G0 * kick_isp_s))
        return (vehicle_wet_kg + kick_dry_kg) * f_burn / (1.0 - f_burn)

    def pre(state, params):
        if state.location != "LEO":
            return (False, f"kick needs LEO, got {state.location}")
        if state.epoch_jd is None or not p1mod.in_earth_saturn_launch_window(state.epoch_jd):
            return (False, "outside launch window")
        kick_prop = stack_propellant(state.mass_kg)
        stack = state.mass_kg + kick_dry_kg + kick_prop
        if stack > MAX_MANIFEST_KG:
            return (False, f"corrected kick stack {stack/1000:.0f} t exceeds max manifest "
                           f"{MAX_MANIFEST_KG/1000:.0f} t (vehicle {state.mass_kg/1000:.0f} t "
                           f"+ kick {(kick_dry_kg + kick_prop)/1000:.0f} t)")
        residual_dv = max(0.0, p1mod.TSI_DV_HOHMANN_KM_S - kick_dv_km_s)
        _, need = p1mod.rocket_equation_burn(state.mass_kg, residual_dv, params["chemical_isp_s"])
        if state.propellant_kg < need:
            return (False, f"not enough vehicle propellant for residual {residual_dv:.2f} km/s: "
                           f"need {need:.0f} kg, have {state.propellant_kg:.0f}")
        return (True, "feasible")

    def exe(state, params):
        # Kick expels its own propellant and is jettisoned: vehicle state unchanged in mass
        # by the kick itself; vehicle then burns the residual from its own tank.
        residual_dv = max(0.0, p1mod.TSI_DV_HOHMANN_KM_S - kick_dv_km_s)
        m_after, burned = p1mod.rocket_equation_burn(state.mass_kg, residual_dv, params["chemical_isp_s"])
        return replace(
            state, mass_kg=m_after, propellant_kg=state.propellant_kg - burned,
            location="saturn_approach", v_inf_km_s=p1mod.ARRIVAL_VINF_KM_S,
            time_elapsed_s=state.time_elapsed_s + p1mod.COAST_HOHMANN_YEARS * p1mod.SECONDS_PER_YEAR,
        )

    return Option(option_id=option_id, description=desc, phase_id="P1_LEO_to_Saturn",
                  precondition=pre, executor=exe, params_required=("chemical_isp_s",),
                  notes="Round-local corrected kick: self-consistent stack, manifest-gated.")


def patched_mission():
    fixed_options = []
    for o in p1mod.phase1.options:
        if o.option_id == "falcon_heavy_plus_star_kick":
            fixed_options.append(_corrected_kick(
                p1mod.STAR_KICK_DV_KM_S, p1mod.STAR_KICK_DRY_MASS_KG, p1mod.STAR_KICK_ISP_S,
                o.option_id, o.description))
        elif o.option_id == "falcon_heavy_plus_helios_kick":
            fixed_options.append(_corrected_kick(
                p1mod.HELIOS_KICK_DV_KM_S, p1mod.HELIOS_KICK_DRY_MASS_KG, p1mod.HELIOS_KICK_ISP_S,
                o.option_id, o.description))
        else:
            fixed_options.append(o)
    phase1_fixed = Phase(phase_id="P1_LEO_to_Saturn",
                         description=p1mod.phase1.description,
                         options=tuple(fixed_options))
    seq = tuple(phase1_fixed if ph.phase_id == "P1_LEO_to_Saturn" else ph
                for ph in saturn_water_v1.phase_sequence)
    return Mission(mission_id="saturn_water_v1_kickfix",
                   objective=saturn_water_v1.objective,
                   phase_sequence=seq,
                   closure_predicates=saturn_water_v1.closure_predicates)


def corrected_sweep():
    import saturn_water_v1_closure_sweep as sweep_mod
    mission_fixed = patched_mission()
    orig = sweep_mod.saturn_water_v1
    out = {}
    try:
        sweep_mod.saturn_water_v1 = mission_fixed  # round-local swap for run_closed_loop
        for m in (1.0, 0.43):
            for f in (0.15, 0.18, 0.20, 0.22, 0.25, 0.30, 0.80):
                cells = sweep_mod.run_closed_loop(extra_params={
                    "propellant_fraction": f, "plans_aerocapture": True,
                    "capture_efficiency_multiplier": m})
                c = {p: sum(1 for cc in cells if sweep_mod.cell_closes(cc, p))
                     for p in ("arrived_at_depot", "delivered_floor_10t",
                               "delivered_floor_20t", "delivered_floor")}
                best = 0.0
                for cell in cells:
                    if cell.skipped_reason:
                        continue
                    for r in cell.results:
                        if r.is_feasible and r.leaf_state.location == "LEO_depot":
                            best = max(best, r.leaf_state.payload_kg / 1000)
                out[f"m={m},f={f}"] = {**c, "best_t": round(best, 1)}
                print(f"  m={m:.2f} f={f:.2f}: arrived={c['arrived_at_depot']:>3d} "
                      f"10t={c['delivered_floor_10t']:>3d} 20t={c['delivered_floor_20t']:>3d} "
                      f"30t={c['delivered_floor']:>3d}  best={best:.1f}t")
    finally:
        sweep_mod.saturn_water_v1 = orig
    return out


def main():
    print("=== H1: ledger walk of the closing path (BUGGY kick model, as-shipped) ===")
    ledger = ledger_walk()

    print("\n=== H2-H4: corrected-kick closure sweep ===")
    table = corrected_sweep()

    (RESULTS / "self_consistency.json").write_text(json.dumps(
        {"ledger": ledger, "corrected_sweep": table}, indent=2))
    print(f"\nwrote {RESULTS / 'self_consistency.json'}")


if __name__ == "__main__":
    main()
