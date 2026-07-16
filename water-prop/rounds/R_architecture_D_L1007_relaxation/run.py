"""R-architecture-D-L1007-relaxation —
   Does chunk-mass cap relaxation rescue Architecture D economics?

Pre-registration: see STUDY.md (frozen before this script ran).

Falsification target: round 6's "Architecture D is structurally money-losing
at zero discount under every conservative anchor swept" headline. Holds chunk
at L1-007 200-t cap; this round questions that assumption.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
WATERPROP_ROUNDS = ROUND_DIR.parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Propulsion constants
# ---------------------------------------------------------------------------
ISP_S = 450.0
G0 = 9.80665
V_E_KM_S = ISP_S * G0 / 1000.0  # 4.413
DV_INBOUND_KM_S = 6.42
MR_INBOUND = math.exp(DV_INBOUND_KM_S / V_E_KM_S)  # 4.284

# Vehicle subsystems
VEH_DRY_T = 10.0
ELECTROLYSIS_T_DFISSION = 5.0  # separate proton-exchange-membrane plant
ELECTROLYSIS_T_DSOLAR = 0.0    # SOEC integrated into stack (no separate plant)

# Saturn-side energy budget
SATURN_OPS_YR = 1.0
ELECTROLYSIS_KWH_PER_KG = 8.0

# Subsystem specific masses
FSP_STRETCH_SPEC_PWR_W_PER_KG = 10.0   # D-fission reactor specific power
DSOLAR_STACK_KG_PER_KWE = 101.0        # D-solar-thermal stack specific mass (optimistic)

# Round-trip and fleet schedule constants
D_ROUND_TRIP_YR = 13.17
DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
HORIZON_YR = 45

# Variant B reference (matrix-impulsive baseline; see STUDY validity caveat 4)
VARIANT_B_DELIVERED_AT_200T = 128.8
VARIANT_B_SHIP_CAPEX_M = 650.0
VARIANT_B_POSTERIOR_CHAINED = 0.0013
VARIANT_B_ROUND_TRIP_YR = 14.5  # R-reactor-roadmap chemical-kick

# Posteriors from R-fission-surface-power-stretch-credibility cascade-Monte-Carlo
D_FISSION_POSTERIOR_MEDIAN = 0.0078
D_SOLAR_POSTERIOR_MEDIAN = 0.0203
D_FISSION_POSTERIOR_P95 = 0.0187
D_SOLAR_POSTERIOR_P95 = 0.0555

# Launch-cost sweep
LAUNCH_COSTS = {
    "starship_optimistic": 200.0,
    "starship_central":    300.0,
    "mixed_baseline":      500.0,
    "FH_plus_assembly":    700.0,
}

# Price anchors
BEST_CELL = {
    "price_per_kg": 10000.0,
    "sovereign_amount": 2e9,
    "sovereign_year": 11,
}
CONOPS_BASE = {
    "price_per_kg": 2000.0,
    "sovereign_amount": 0.0,
    "sovereign_year": 11,
}

# Chunk sweep
CHUNK_VALUES_T = [200, 250, 300, 350, 400, 450, 482]


# ---------------------------------------------------------------------------
# Architecture-D mass cascade with right-sized power subsystem
# ---------------------------------------------------------------------------
def architecture_d_mass_cascade(chunk_t: float, variant: str) -> dict:
    """Return delivered mass, subsystem mass, dry-at-Saturn, and ship CapEx
    for Architecture D at the given chunk mass and variant.

    variant: 'd_fission' or 'd_solar_thermal'.
    """
    # Inbound propellant required (chunk-fed at MR_INBOUND)
    p_inb = chunk_t * (1.0 - 1.0 / MR_INBOUND)

    # Saturn-side electrolysis energy
    energy_kwh = p_inb * 1000.0 * ELECTROLYSIS_KWH_PER_KG
    p_kwe_required = energy_kwh / (SATURN_OPS_YR * 8760.0)

    # Right-sized subsystem mass
    if variant == "d_fission":
        m_subsystem_t = p_kwe_required / FSP_STRETCH_SPEC_PWR_W_PER_KG
        m_electrolysis_t = ELECTROLYSIS_T_DFISSION
        # CapEx scaling: $600M at M_reactor=20 t baseline; $8M-per-extra-tonne marginal.
        ship_capex_m = 600.0 + (m_subsystem_t - 20.0) * 8.0
    elif variant == "d_solar_thermal":
        m_subsystem_t = p_kwe_required * DSOLAR_STACK_KG_PER_KWE / 1000.0
        m_electrolysis_t = ELECTROLYSIS_T_DSOLAR
        # CapEx scaling: $608M at M_stack=20 t baseline; $6M-per-extra-tonne marginal.
        ship_capex_m = 608.0 + (m_subsystem_t - 20.0) * 6.0
    else:
        raise ValueError(f"unknown variant {variant}")

    m_dry_sat = VEH_DRY_T + m_subsystem_t + m_electrolysis_t
    delivered_t = chunk_t / MR_INBOUND - m_dry_sat * (1.0 - 1.0 / MR_INBOUND)

    return {
        "chunk_t": chunk_t,
        "variant": variant,
        "p_inb_t": p_inb,
        "energy_kwh": energy_kwh,
        "p_kwe_required": p_kwe_required,
        "m_subsystem_t": m_subsystem_t,
        "m_dry_at_saturn_t": m_dry_sat,
        "delivered_t": delivered_t,
        "ship_capex_m": ship_capex_m,
    }


def variant_b_at_chunk(chunk_t: float) -> dict:
    """Variant B 500-kWe chemical-kick scaled linearly with chunk mass.
    See STUDY validity caveat 4 — uses matrix-impulsive 128.8 t baseline.
    """
    delivered_t = VARIANT_B_DELIVERED_AT_200T * (chunk_t / 200.0)
    return {
        "chunk_t": chunk_t,
        "variant": "variant_B_500kWe_matrix_impulsive",
        "delivered_t": delivered_t,
        "ship_capex_m": VARIANT_B_SHIP_CAPEX_M,
        "round_trip_yr": VARIANT_B_ROUND_TRIP_YR,
    }


# ---------------------------------------------------------------------------
# Fleet schedule and cashflow model (carried from R-reactor-roadmap)
# ---------------------------------------------------------------------------
def build_fleet_schedule(horizon_yr: int = HORIZON_YR) -> list[dict]:
    schedule = [{"ship_no": 1, "launch_year": 0.0}]
    schedule.append({"ship_no": 2, "launch_year": 7.0})
    ship_no = 3
    year = 8.0
    while year < horizon_yr:
        schedule.append({"ship_no": ship_no, "launch_year": year})
        ship_no += 1
        year += 13.0 / 12.0
    return schedule


def cashflow_yearly(
    price_per_kg: float,
    sovereign_amount: float,
    sovereign_year: int,
    ship_capex_m: float,
    launch_cost_m: float,
    delivered_per_ship_t: float,
    round_trip_yr: float,
    horizon_yr: int = HORIZON_YR,
) -> dict[int, dict]:
    schedule = build_fleet_schedule(horizon_yr)
    yearly = {yr: {"cost": 0.0, "revenue": 0.0} for yr in range(horizon_yr)}
    yearly[0]["cost"] += DEMONSTRATOR_NRE

    for ship in schedule:
        ly = int(ship["launch_year"])
        if ly >= horizon_yr:
            continue
        yearly[ly]["cost"] += (ship_capex_m + launch_cost_m) * 1e6
        dy = ly + int(round(round_trip_yr))
        if dy < horizon_yr:
            yearly[dy]["revenue"] += delivered_per_ship_t * 1000.0 * price_per_kg

    for yr in range(horizon_yr):
        yearly[yr]["cost"] += GROUND_OPS_PER_YEAR

    if sovereign_amount > 0 and 0 <= sovereign_year < horizon_yr:
        yearly[sovereign_year]["revenue"] += sovereign_amount

    return yearly


def npv(yearly: dict, rate: float, horizon: int = HORIZON_YR) -> float:
    return sum(
        (yearly[t]["revenue"] - yearly[t]["cost"]) / ((1.0 + rate) ** t)
        for t in range(horizon)
    )


def perpetuity_terminal_value(yearly: dict, rate: float, horizon: int = HORIZON_YR, growth: float = 0.0) -> float:
    last5 = [yearly[t]["revenue"] - yearly[t]["cost"] for t in range(horizon - 5, horizon)]
    cf_terminal = sum(last5) / 5.0
    if cf_terminal <= 0 or rate <= growth:
        return 0.0
    tv_at_horizon = cf_terminal * (1.0 + growth) / (rate - growth)
    return tv_at_horizon / ((1.0 + rate) ** horizon)


def irr_bisect(yearly: dict, with_tv: bool = True, horizon: int = HORIZON_YR) -> float | None:
    def f(r: float) -> float:
        return npv(yearly, r, horizon) + (perpetuity_terminal_value(yearly, r, horizon) if with_tv else 0.0)

    lo, hi = 1e-4, 0.30
    f_lo, f_hi = f(lo), f(hi)
    if f_lo <= 0:
        return None
    if f_hi > 0:
        return hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------
def run_sweep() -> dict:
    rows = []
    cells = {"BEST_CELL": BEST_CELL, "CONOPS_BASE": CONOPS_BASE}

    for chunk in CHUNK_VALUES_T:
        # D-fission and D-solar-thermal mass cascades
        dfis = architecture_d_mass_cascade(chunk, "d_fission")
        dsol = architecture_d_mass_cascade(chunk, "d_solar_thermal")
        vb = variant_b_at_chunk(chunk)

        for cell_name, cell in cells.items():
            for launch_name, launch_m in LAUNCH_COSTS.items():
                # --- D-fission ---
                yearly_cond_dfis = cashflow_yearly(
                    cell["price_per_kg"], cell["sovereign_amount"], cell["sovereign_year"],
                    dfis["ship_capex_m"], launch_m, dfis["delivered_t"], D_ROUND_TRIP_YR,
                )
                irr_dfis_cond = irr_bisect(yearly_cond_dfis)
                rev_dfis = dfis["delivered_t"] * 1000.0 * cell["price_per_kg"] / 1e6
                gross_dfis = rev_dfis - dfis["ship_capex_m"]
                yearly_adj_dfis = cashflow_yearly(
                    cell["price_per_kg"], cell["sovereign_amount"] * D_FISSION_POSTERIOR_MEDIAN, cell["sovereign_year"],
                    dfis["ship_capex_m"], launch_m, dfis["delivered_t"] * D_FISSION_POSTERIOR_MEDIAN, D_ROUND_TRIP_YR,
                )
                irr_dfis_adj = irr_bisect(yearly_adj_dfis)
                rows.append({
                    "variant": "D-fission",
                    "chunk_t": chunk,
                    "price_cell": cell_name,
                    "launch": launch_name,
                    "launch_cost_m": launch_m,
                    "delivered_t": dfis["delivered_t"],
                    "m_subsystem_t": dfis["m_subsystem_t"],
                    "ship_capex_m": dfis["ship_capex_m"],
                    "revenue_per_ship_m": rev_dfis,
                    "gross_per_ship_m": gross_dfis,
                    "irr_conditional": irr_dfis_cond,
                    "irr_posterior_median": irr_dfis_adj,
                    "expected_delivered_t": dfis["delivered_t"] * D_FISSION_POSTERIOR_MEDIAN,
                })

                # --- D-solar-thermal ---
                yearly_cond_dsol = cashflow_yearly(
                    cell["price_per_kg"], cell["sovereign_amount"], cell["sovereign_year"],
                    dsol["ship_capex_m"], launch_m, dsol["delivered_t"], D_ROUND_TRIP_YR,
                )
                irr_dsol_cond = irr_bisect(yearly_cond_dsol)
                rev_dsol = dsol["delivered_t"] * 1000.0 * cell["price_per_kg"] / 1e6
                gross_dsol = rev_dsol - dsol["ship_capex_m"]
                yearly_adj_dsol = cashflow_yearly(
                    cell["price_per_kg"], cell["sovereign_amount"] * D_SOLAR_POSTERIOR_MEDIAN, cell["sovereign_year"],
                    dsol["ship_capex_m"], launch_m, dsol["delivered_t"] * D_SOLAR_POSTERIOR_MEDIAN, D_ROUND_TRIP_YR,
                )
                irr_dsol_adj = irr_bisect(yearly_adj_dsol)
                rows.append({
                    "variant": "D-solar-thermal",
                    "chunk_t": chunk,
                    "price_cell": cell_name,
                    "launch": launch_name,
                    "launch_cost_m": launch_m,
                    "delivered_t": dsol["delivered_t"],
                    "m_subsystem_t": dsol["m_subsystem_t"],
                    "ship_capex_m": dsol["ship_capex_m"],
                    "revenue_per_ship_m": rev_dsol,
                    "gross_per_ship_m": gross_dsol,
                    "irr_conditional": irr_dsol_cond,
                    "irr_posterior_median": irr_dsol_adj,
                    "expected_delivered_t": dsol["delivered_t"] * D_SOLAR_POSTERIOR_MEDIAN,
                })

                # --- Variant B reference (matrix-impulsive) ---
                yearly_cond_vb = cashflow_yearly(
                    cell["price_per_kg"], cell["sovereign_amount"], cell["sovereign_year"],
                    VARIANT_B_SHIP_CAPEX_M, launch_m, vb["delivered_t"], VARIANT_B_ROUND_TRIP_YR,
                )
                irr_vb_cond = irr_bisect(yearly_cond_vb)
                rev_vb = vb["delivered_t"] * 1000.0 * cell["price_per_kg"] / 1e6
                gross_vb = rev_vb - VARIANT_B_SHIP_CAPEX_M
                yearly_adj_vb = cashflow_yearly(
                    cell["price_per_kg"], cell["sovereign_amount"] * VARIANT_B_POSTERIOR_CHAINED, cell["sovereign_year"],
                    VARIANT_B_SHIP_CAPEX_M, launch_m, vb["delivered_t"] * VARIANT_B_POSTERIOR_CHAINED, VARIANT_B_ROUND_TRIP_YR,
                )
                irr_vb_adj = irr_bisect(yearly_adj_vb)
                rows.append({
                    "variant": "Variant B (matrix-impulsive ref)",
                    "chunk_t": chunk,
                    "price_cell": cell_name,
                    "launch": launch_name,
                    "launch_cost_m": launch_m,
                    "delivered_t": vb["delivered_t"],
                    "m_subsystem_t": None,
                    "ship_capex_m": VARIANT_B_SHIP_CAPEX_M,
                    "revenue_per_ship_m": rev_vb,
                    "gross_per_ship_m": gross_vb,
                    "irr_conditional": irr_vb_cond,
                    "irr_posterior_median": irr_vb_adj,
                    "expected_delivered_t": vb["delivered_t"] * VARIANT_B_POSTERIOR_CHAINED,
                })

    return {
        "constants": {
            "v_e_km_s": V_E_KM_S,
            "MR_inbound": MR_INBOUND,
            "dv_inbound_km_s": DV_INBOUND_KM_S,
            "saturn_ops_yr": SATURN_OPS_YR,
            "electrolysis_kwh_per_kg": ELECTROLYSIS_KWH_PER_KG,
            "fsp_stretch_spec_pwr_w_per_kg": FSP_STRETCH_SPEC_PWR_W_PER_KG,
            "dsolar_stack_kg_per_kwe": DSOLAR_STACK_KG_PER_KWE,
            "round_trip_yr": D_ROUND_TRIP_YR,
            "posteriors": {
                "d_fission_median": D_FISSION_POSTERIOR_MEDIAN,
                "d_solar_thermal_median": D_SOLAR_POSTERIOR_MEDIAN,
                "variant_B_chained": VARIANT_B_POSTERIOR_CHAINED,
            },
        },
        "rows": rows,
    }


def find_break_even_chunk(rows: list[dict], variant: str, price_cell: str = "BEST_CELL") -> tuple:
    """Find the smallest chunk where gross_per_ship_m crosses zero."""
    sub = [r for r in rows if r["variant"] == variant and r["price_cell"] == price_cell and r["launch"] == "mixed_baseline"]
    sub.sort(key=lambda r: r["chunk_t"])
    # Use unique chunk values (gross_per_ship is independent of launch cost)
    seen = set()
    unique_sub = []
    for r in sub:
        if r["chunk_t"] not in seen:
            unique_sub.append(r)
            seen.add(r["chunk_t"])
    for i, r in enumerate(unique_sub[:-1]):
        if r["gross_per_ship_m"] < 0 <= unique_sub[i+1]["gross_per_ship_m"]:
            # Linear interpolate
            c1, c2 = r["chunk_t"], unique_sub[i+1]["chunk_t"]
            g1, g2 = r["gross_per_ship_m"], unique_sub[i+1]["gross_per_ship_m"]
            break_even = c1 + (0 - g1) * (c2 - c1) / (g2 - g1)
            return (break_even, c1, c2)
    return (None, None, None)


def grade_subclaims(out: dict) -> dict:
    rows = out["rows"]
    grades = []

    def add(claim, predicted, observed, held, note=""):
        grades.append({"claim": claim, "predicted": predicted, "observed": observed, "held": held, "note": note})

    # H7-a: right-sized reactor at chunk 200 t — M_reactor 12-16 t, delivered 22-27 t
    dfis_200 = architecture_d_mass_cascade(200, "d_fission")
    add("H7-a",
        "Right-sized reactor at chunk 200 t: M_reactor 14 t (band 12-16), delivered 24.5 t (band 22-27)",
        f"M_reactor = {dfis_200['m_subsystem_t']:.2f} t, delivered = {dfis_200['delivered_t']:.2f} t",
        12.0 <= dfis_200["m_subsystem_t"] <= 16.0 and 22.0 <= dfis_200["delivered_t"] <= 27.0,
    )

    # H7-b: D-fission gross break-even chunk
    be_dfis, c1, c2 = find_break_even_chunk(rows, "D-fission")
    add("H7-b",
        "D-fission gross cashflow break-even chunk: 450-480 t (falsification 400-550)",
        f"break-even ≈ {be_dfis:.0f} t between chunks {c1}-{c2}" if be_dfis else "no break-even in swept range",
        be_dfis is not None and 400 <= be_dfis <= 550,
    )

    # H7-c: D-solar-thermal break-even
    be_dsol, c1s, c2s = find_break_even_chunk(rows, "D-solar-thermal")
    add("H7-c",
        "D-solar-thermal break-even chunk: 460-490 t (falsification 410-560)",
        f"break-even ≈ {be_dsol:.0f} t between chunks {c1s}-{c2s}" if be_dsol else "no break-even in swept range",
        be_dsol is not None and 410 <= be_dsol <= 560,
    )

    # H7-d: D-fission conditional IRR at chunk 482, BEST_CELL, mixed_baseline, central CapEx
    dfis_482 = next(r for r in rows if r["variant"] == "D-fission" and r["chunk_t"] == 482 and r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline")
    irr_d_pct = dfis_482["irr_conditional"] * 100 if dfis_482["irr_conditional"] is not None else None
    add("H7-d",
        "D-fission conditional IRR at chunk 482, BEST_CELL, mixed_baseline: -1.0 to +2.5 percent (falsification -3 to +4)",
        f"{irr_d_pct:+.2f}%" if irr_d_pct is not None else "None",
        (irr_d_pct is None and False) or (irr_d_pct is not None and -3.0 <= irr_d_pct <= 4.0),
    )

    # H7-e: D-solar-thermal conditional IRR at chunk 482, BEST_CELL, Starship-optimistic
    dsol_482_so = next(r for r in rows if r["variant"] == "D-solar-thermal" and r["chunk_t"] == 482 and r["price_cell"] == "BEST_CELL" and r["launch"] == "starship_optimistic")
    irr_dsol_so_pct = dsol_482_so["irr_conditional"] * 100 if dsol_482_so["irr_conditional"] is not None else None
    add("H7-e",
        "D-solar-thermal conditional IRR at chunk 482, BEST_CELL, Starship-optimistic: +2.0 to +5.0 percent (falsification 0 to +6)",
        f"{irr_dsol_so_pct:+.2f}%" if irr_dsol_so_pct is not None else "None",
        irr_dsol_so_pct is not None and 0.0 <= irr_dsol_so_pct <= 6.0,
    )

    # H7-f: D-fission expected delivered at chunk 482: 0.45-0.75 t
    add("H7-f",
        "D-fission expected delivered at chunk 482: 0.45-0.75 t (falsification 0.30-1.00)",
        f"{dfis_482['expected_delivered_t']:.3f} t",
        0.30 <= dfis_482["expected_delivered_t"] <= 1.00,
    )

    # H7-g: D-solar-thermal expected delivered at chunk 482
    dsol_482 = next(r for r in rows if r["variant"] == "D-solar-thermal" and r["chunk_t"] == 482 and r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline")
    add("H7-g",
        "D-solar-thermal expected delivered at chunk 482: 1.3-1.8 t (falsification 0.8-2.5)",
        f"{dsol_482['expected_delivered_t']:.3f} t",
        0.8 <= dsol_482["expected_delivered_t"] <= 2.5,
    )

    # H7-h: Variant B expected delivered at chunk 482
    vb_482 = next(r for r in rows if "Variant B" in r["variant"] and r["chunk_t"] == 482 and r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline")
    add("H7-h",
        "Variant B expected delivered at chunk 482: 0.38-0.45 t (falsification 0.25-0.60)",
        f"{vb_482['expected_delivered_t']:.3f} t",
        0.25 <= vb_482["expected_delivered_t"] <= 0.60,
    )

    # H7-i: D-solar/Variant B dominance factor at chunk 482
    ratio_482 = dsol_482["expected_delivered_t"] / vb_482["expected_delivered_t"]
    add("H7-i",
        "D-solar-thermal / Variant B dominance factor at chunk 482: 3.5-4.5× (falsification 2.5-6.0)",
        f"{ratio_482:.2f}×",
        2.5 <= ratio_482 <= 6.0,
    )

    # H7-j: sovereign-bond clearance for D
    dfis_clears = [r for r in rows if r["variant"] == "D-fission" and r["irr_conditional"] is not None and r["irr_conditional"] >= 0.04]
    dsol_clears_so = [r for r in rows if r["variant"] == "D-solar-thermal" and r["launch"] == "starship_optimistic" and r["irr_conditional"] is not None and r["irr_conditional"] >= 0.04]
    dsol_482_clears_so = irr_dsol_so_pct is not None and irr_dsol_so_pct >= 4.0
    add("H7-j",
        "Sovereign-bond clearance: D-fission does not clear anywhere; D-solar-thermal Starship-optimistic clears at chunk ≥ 450 t",
        f"D-fission clears: {len(dfis_clears)} cells; D-solar Starship-opt clears: {len(dsol_clears_so)} cells; D-solar Starship-opt clears at chunk 482: {dsol_482_clears_so}",
        len(dfis_clears) == 0 and dsol_482_clears_so,
    )

    # H7-k: Variant B per-mission cashflow dominance over D at every chunk
    # Compare gross_per_ship at BEST_CELL between Variant B and D-fission and D-solar at each chunk
    dominance_failed = []
    for chunk in CHUNK_VALUES_T:
        vb_g = next(r for r in rows if "Variant B" in r["variant"] and r["chunk_t"] == chunk and r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline")["gross_per_ship_m"]
        df_g = next(r for r in rows if r["variant"] == "D-fission" and r["chunk_t"] == chunk and r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline")["gross_per_ship_m"]
        ds_g = next(r for r in rows if r["variant"] == "D-solar-thermal" and r["chunk_t"] == chunk and r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline")["gross_per_ship_m"]
        if df_g >= vb_g or ds_g >= vb_g:
            dominance_failed.append((chunk, vb_g, df_g, ds_g))
    add("H7-k",
        "Variant B per-mission cashflow dominates D at every chunk, by 5-10× at BEST_CELL",
        f"dominance held at all {len(CHUNK_VALUES_T)} chunks; dominance ratio at chunk 482 = {next(r['gross_per_ship_m'] for r in rows if 'Variant B' in r['variant'] and r['chunk_t']==482 and r['price_cell']=='BEST_CELL' and r['launch']=='mixed_baseline') / next(r['gross_per_ship_m'] for r in rows if r['variant']=='D-fission' and r['chunk_t']==482 and r['price_cell']=='BEST_CELL' and r['launch']=='mixed_baseline'):.1f}×" if not dominance_failed else f"failed at chunks {[d[0] for d in dominance_failed]}",
        len(dominance_failed) == 0,
    )

    # H7-l: falsification check on round 6 headline
    any_pos_d_gross = any(r["gross_per_ship_m"] > 0 for r in rows if r["variant"] in ("D-fission", "D-solar-thermal") and r["price_cell"] == "BEST_CELL")
    add("H7-l",
        "Falsifies round-6 'structurally money-losing' headline: at chunk ≥ 450-470 t Architecture D becomes per-mission cashflow-positive",
        f"any D variant has positive gross/ship in sweep: {any_pos_d_gross}",
        any_pos_d_gross,
        "Round 6's headline holds only at L1-007 cap; falsifies at L1-007 relaxation upward.",
    )

    # H7-m: combined verdict
    vb_dominates_cashflow = len(dominance_failed) == 0
    dsol_dominates_expected_delivered = ratio_482 >= 2.5
    add("H7-m",
        "Combined: Variant B per-mission-cashflow-superior AND D-solar dominates Variant B on expected-delivered",
        f"VB cashflow dominance: {vb_dominates_cashflow}; D-solar expected-delivered dominance at chunk 482: {ratio_482:.2f}×",
        vb_dominates_cashflow and dsol_dominates_expected_delivered,
    )

    out["grades"] = grades
    return out


def format_table_md(out: dict) -> str:
    rows = out["rows"]
    lines = []
    lines.append("# R-architecture-D-L1007-relaxation — results table\n")
    lines.append(f"Total rows: {len(rows)}\n")

    # Per-variant summary at BEST_CELL, mixed_baseline launch (chunk-mass effects most visible)
    lines.append("## BEST_CELL × mixed_baseline launch — chunk-mass sweep\n")
    lines.append("| Variant | Chunk t | M_sub t | Capex $M | Delivered t | Rev/ship $M | Gross/ship $M | IRR cond % | IRR adj-med % | E[delivered] t |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    sub = [r for r in rows if r["price_cell"] == "BEST_CELL" and r["launch"] == "mixed_baseline"]
    variant_order = {"D-fission": 0, "D-solar-thermal": 1, "Variant B (matrix-impulsive ref)": 2}
    sub.sort(key=lambda r: (r["chunk_t"], variant_order.get(r["variant"], 99)))
    for r in sub:
        irr_c = f"{r['irr_conditional']*100:+.2f}" if r["irr_conditional"] is not None else "—"
        irr_a = f"{r['irr_posterior_median']*100:+.2f}" if r["irr_posterior_median"] is not None else "—"
        msub = f"{r['m_subsystem_t']:.1f}" if r["m_subsystem_t"] is not None else "—"
        lines.append(f"| {r['variant']} | {r['chunk_t']:.0f} | {msub} | {r['ship_capex_m']:.0f} | {r['delivered_t']:.1f} | {r['revenue_per_ship_m']:.1f} | {r['gross_per_ship_m']:+.1f} | {irr_c} | {irr_a} | {r['expected_delivered_t']:.3f} |")

    # D-solar-thermal at Starship-optimistic — the cell that closes sovereign-bond per H7-e
    lines.append("\n## D-solar-thermal × Starship-optimistic launch × BEST_CELL — sovereign-bond closure check\n")
    lines.append("| Chunk t | Delivered t | Capex $M | Gross/ship $M | IRR cond % | Above sovereign-bond 4%? |")
    lines.append("|---:|---:|---:|---:|---:|---|")
    sub2 = [r for r in rows if r["variant"] == "D-solar-thermal" and r["launch"] == "starship_optimistic" and r["price_cell"] == "BEST_CELL"]
    sub2.sort(key=lambda r: r["chunk_t"])
    for r in sub2:
        irr_c = f"{r['irr_conditional']*100:+.2f}" if r["irr_conditional"] is not None else "—"
        clears = "YES" if r["irr_conditional"] is not None and r["irr_conditional"] >= 0.04 else "no"
        lines.append(f"| {r['chunk_t']:.0f} | {r['delivered_t']:.1f} | {r['ship_capex_m']:.0f} | {r['gross_per_ship_m']:+.1f} | {irr_c} | {clears} |")

    return "\n".join(lines) + "\n"


def main():
    out = run_sweep()
    out = grade_subclaims(out)
    (RESULTS_DIR / "architecture_d_L1007_relaxation.json").write_text(json.dumps(out, indent=2))
    (RESULTS_DIR / "tables.md").write_text(format_table_md(out))

    print(f"R-architecture-D-L1007-relaxation sweep complete. Rows: {len(out['rows'])}.\n")
    print("Right-sized mass cascade per chunk (D-fission):")
    for c in CHUNK_VALUES_T:
        m = architecture_d_mass_cascade(c, "d_fission")
        print(f"  chunk {c:>4d} t → P_kWe = {m['p_kwe_required']:>5.1f}, M_reactor = {m['m_subsystem_t']:>5.1f} t, dry@Sat = {m['m_dry_at_saturn_t']:>5.1f} t, delivered = {m['delivered_t']:>5.1f} t, capex = ${m['ship_capex_m']:>5.0f}M")
    print("")
    print("Sub-claim grades:")
    held = 0
    for g in out["grades"]:
        status = "HELD" if g["held"] else "FALSIFIED"
        if g["held"]:
            held += 1
        print(f"  [{status}] {g['claim']}: {g['observed']}")
    print(f"\n{held}/{len(out['grades'])} sub-claims held.")


if __name__ == "__main__":
    main()
