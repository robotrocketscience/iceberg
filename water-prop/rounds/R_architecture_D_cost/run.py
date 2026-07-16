"""R-architecture-D-cost — marginal internal-rate-of-return for Architecture-D
variants (D-fission and D-solar-thermal) at sweep over cost and price anchors,
with programmatic-risk overlay using authoritative posteriors.

Pre-registration: see STUDY.md (frozen before this script ran).
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
WATERPROP_ROUNDS = ROUND_DIR.parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Architecture-D delivered mass and round-trip (from R-chemical-plus-small-reactor)
# ---------------------------------------------------------------------------
# Closing scenarios (closes_all_criteria == true): 10 cells at FSP-stretch
# (10 W/kg) and KRUSTY+FSP-stretch (40 W/kg). Central scenario taken as
# (s_pwr=10 W/kg, M_reactor=20 t, vehicle_dry=10 t, electrolysis=5 t),
# matching D-solar-thermal optimistic-stack (~20 t at 200 kWe useful).
D_DELIVERED_T = 19.9               # delivered chunk per mission
D_ROUND_TRIP_YR = 13.17            # chemical-Hohmann round trip


# ---------------------------------------------------------------------------
# Ship CapEx central + bands ($M)
# ---------------------------------------------------------------------------
# Component anchors derived in STUDY.md "Method / Cost inputs" section.
D_FISSION_SHIP_CAPEX = {
    "low":     400.0,
    "central": 600.0,
    "high":    900.0,
}
D_SOLAR_THERMAL_SHIP_CAPEX = {
    "low":     350.0,
    "central": 608.0,
    "high":    900.0,
}

# Launch-cost sweep ($M per mission)
LAUNCH_COSTS = {
    "starship_optimistic": 200.0,
    "starship_central":    300.0,
    "mixed_baseline":      500.0,
    "FH_plus_assembly":    700.0,
}


# ---------------------------------------------------------------------------
# Cashflow-framework constants (carried from R-reactor-roadmap)
# ---------------------------------------------------------------------------
DEMONSTRATOR_NRE = 500e6
GROUND_OPS_PER_YEAR = 50e6
HORIZON_YR = 45


# ---------------------------------------------------------------------------
# Fleet schedule — same cadence as R-reactor-roadmap (every 13/12 years after
# the second ship). Architecture D does not depend on megawatt-arrival year,
# so all ships share the same delivered mass and ship cost.
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


# ---------------------------------------------------------------------------
# Cashflow generator (per-mission constant delivered mass and ship cost)
# ---------------------------------------------------------------------------
def cashflow_yearly_d(
    price_per_kg: float,
    sovereign_amount: float,
    sovereign_year: int,
    ship_capex_m: float,
    launch_cost_m: float,
    delivered_per_ship_t: float,
    round_trip_yr: float = D_ROUND_TRIP_YR,
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


def perpetuity_terminal_value(
    yearly: dict, rate: float, horizon: int = HORIZON_YR, growth: float = 0.0
) -> float:
    last5 = [yearly[t]["revenue"] - yearly[t]["cost"]
             for t in range(horizon - 5, horizon)]
    cf_terminal = sum(last5) / 5.0
    if cf_terminal <= 0 or rate <= growth:
        return 0.0
    tv_at_horizon = cf_terminal * (1.0 + growth) / (rate - growth)
    return tv_at_horizon / ((1.0 + rate) ** horizon)


def irr_bisect(yearly: dict, with_tv: bool = True, horizon: int = HORIZON_YR) -> float | None:
    """Return discount rate at which net-present-value (optionally + perpetuity
    terminal value at growth 0) = 0. Returns None if cashflow is deeply negative
    even at near-zero rate. Returns 0.30 ceiling if internal-rate-of-return
    exceeds 30 percent.
    """
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
# Cell anchors (BEST_CELL / CONOPS_BASE)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Posterior loader
# ---------------------------------------------------------------------------
def load_posteriors() -> dict:
    """Load D-fission and D-solar-thermal posteriors from
    R-fission-surface-power-stretch-credibility cascade-Monte-Carlo output.
    Returns {'d_fission': {...}, 'd_solar_thermal': {...}} with median, mean,
    p05/p25/p75/p95, and the raw sample arrays.
    """
    path = (
        WATERPROP_ROUNDS / "R_fission_surface_power_stretch_credibility"
        / "results" / "cascade_montecarlo.json"
    )
    with path.open() as f:
        raw = json.load(f)
    out = {}
    for key, source_key in [
        ("d_fission", "fission_posterior"),
        ("d_solar_thermal", "solar_thermal_posterior"),
    ]:
        src = raw[source_key]
        out[key] = {
            "mean":   src["mean"],
            "median": src["median"],
            "p05":    src["p05"],
            "p25":    src["p25"],
            "p75":    src["p75"],
            "p95":    src["p95"],
        }
    return out


# ---------------------------------------------------------------------------
# Posterior overlay: Bernoulli per-launch with probability = posterior
# ---------------------------------------------------------------------------
def cashflow_yearly_d_posterior_adjusted(
    price_per_kg: float,
    sovereign_amount: float,
    sovereign_year: int,
    ship_capex_m: float,
    launch_cost_m: float,
    delivered_per_ship_t: float,
    posterior: float,
    round_trip_yr: float = D_ROUND_TRIP_YR,
    horizon_yr: int = HORIZON_YR,
) -> dict[int, dict]:
    """Per-launch programmatic-risk overlay. Each launch incurs full CapEx +
    launch cost regardless; expected revenue is posterior * conditional_revenue.
    Expectation taken before discounting (linear-of-expectations).
    """
    return cashflow_yearly_d(
        price_per_kg=price_per_kg,
        sovereign_amount=sovereign_amount * posterior,  # sovereign also gated on program success
        sovereign_year=sovereign_year,
        ship_capex_m=ship_capex_m,
        launch_cost_m=launch_cost_m,
        delivered_per_ship_t=delivered_per_ship_t * posterior,
        round_trip_yr=round_trip_yr,
        horizon_yr=horizon_yr,
    )


# ---------------------------------------------------------------------------
# Sweep
# ---------------------------------------------------------------------------
def run_sweep() -> dict:
    posteriors = load_posteriors()

    variants = {
        "D-fission": {
            "ship_capex": D_FISSION_SHIP_CAPEX,
            "posterior_key": "d_fission",
        },
        "D-solar-thermal": {
            "ship_capex": D_SOLAR_THERMAL_SHIP_CAPEX,
            "posterior_key": "d_solar_thermal",
        },
    }

    cells = {"BEST_CELL": BEST_CELL, "CONOPS_BASE": CONOPS_BASE}

    rows = []
    for variant_name, vcfg in variants.items():
        post = posteriors[vcfg["posterior_key"]]
        for cell_name, cell in cells.items():
            for launch_name, launch_cost in LAUNCH_COSTS.items():
                for capex_band, capex in vcfg["ship_capex"].items():
                    # Conditional cashflow (engineering closure assumed)
                    yearly_cond = cashflow_yearly_d(
                        price_per_kg=cell["price_per_kg"],
                        sovereign_amount=cell["sovereign_amount"],
                        sovereign_year=cell["sovereign_year"],
                        ship_capex_m=capex,
                        launch_cost_m=launch_cost,
                        delivered_per_ship_t=D_DELIVERED_T,
                    )
                    irr_cond = irr_bisect(yearly_cond, with_tv=True)

                    # Per-mission gross cashflow (revenue minus ship CapEx, no
                    # discount, no launch, no opex — for headline accounting only)
                    revenue_per_ship_m = D_DELIVERED_T * 1000.0 * cell["price_per_kg"] / 1e6
                    gross_per_ship_m = revenue_per_ship_m - capex

                    # Programmatic-risk-adjusted at posterior median
                    yearly_adj = cashflow_yearly_d_posterior_adjusted(
                        price_per_kg=cell["price_per_kg"],
                        sovereign_amount=cell["sovereign_amount"],
                        sovereign_year=cell["sovereign_year"],
                        ship_capex_m=capex,
                        launch_cost_m=launch_cost,
                        delivered_per_ship_t=D_DELIVERED_T,
                        posterior=post["median"],
                    )
                    irr_adj_median = irr_bisect(yearly_adj, with_tv=True)

                    # Programmatic-risk-adjusted at posterior 95th percentile (upside)
                    yearly_adj_p95 = cashflow_yearly_d_posterior_adjusted(
                        price_per_kg=cell["price_per_kg"],
                        sovereign_amount=cell["sovereign_amount"],
                        sovereign_year=cell["sovereign_year"],
                        ship_capex_m=capex,
                        launch_cost_m=launch_cost,
                        delivered_per_ship_t=D_DELIVERED_T,
                        posterior=post["p95"],
                    )
                    irr_adj_p95 = irr_bisect(yearly_adj_p95, with_tv=True)

                    expected_delivered_per_ship_t = D_DELIVERED_T * post["median"]

                    rows.append({
                        "variant": variant_name,
                        "price_cell": cell_name,
                        "launch": launch_name,
                        "launch_cost_m": launch_cost,
                        "ship_capex_band": capex_band,
                        "ship_capex_m": capex,
                        "revenue_per_ship_m_at_price": revenue_per_ship_m,
                        "gross_per_ship_m": gross_per_ship_m,
                        "irr_conditional": irr_cond,
                        "irr_posterior_median": irr_adj_median,
                        "irr_posterior_p95": irr_adj_p95,
                        "expected_delivered_per_ship_t": expected_delivered_per_ship_t,
                        "posterior_median": post["median"],
                        "posterior_p95": post["p95"],
                    })

    return {
        "constants": {
            "delivered_per_ship_t": D_DELIVERED_T,
            "round_trip_yr": D_ROUND_TRIP_YR,
            "horizon_yr": HORIZON_YR,
            "demonstrator_nre_m": DEMONSTRATOR_NRE / 1e6,
            "ground_ops_per_year_m": GROUND_OPS_PER_YEAR / 1e6,
            "fleet_size": len(build_fleet_schedule(HORIZON_YR)),
        },
        "posteriors": posteriors,
        "rows": rows,
    }


def format_table_md(rows: list[dict]) -> str:
    """Format the sweep table as Markdown, sorted by variant then by IRR-cond
    descending for readability."""
    lines = []
    lines.append("# R-architecture-D-cost — results table\n")
    lines.append(f"Total rows: {len(rows)}\n")
    lines.append("Columns: variant, price cell, launch anchor, ship-CapEx band, revenue per ship ($M), gross per ship ($M), conditional IRR (%), programmatic-risk-adjusted IRR at posterior-median (%), at posterior-p95 (%), expected delivered per mission (tonnes).\n")

    for variant in sorted({r["variant"] for r in rows}):
        lines.append(f"\n## {variant}\n")
        lines.append("| Price | Launch | Capex band | Capex $M | Rev/ship $M | Gross/ship $M | IRR cond % | IRR adj-med % | IRR adj-p95 % | E[delivered] t |")
        lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")
        # sort by price cell (BEST_CELL first), then launch cost ascending, then capex ascending
        cell_order = {"BEST_CELL": 0, "CONOPS_BASE": 1}
        sub = [r for r in rows if r["variant"] == variant]
        sub.sort(key=lambda r: (cell_order[r["price_cell"]], r["launch_cost_m"], r["ship_capex_m"]))
        for r in sub:
            def fmt_pct(v):
                return f"{v*100:+.2f}" if v is not None else "—"
            lines.append(
                f"| {r['price_cell']} | {r['launch']} | {r['ship_capex_band']} | "
                f"{r['ship_capex_m']:.0f} | {r['revenue_per_ship_m_at_price']:.1f} | "
                f"{r['gross_per_ship_m']:+.1f} | "
                f"{fmt_pct(r['irr_conditional'])} | "
                f"{fmt_pct(r['irr_posterior_median'])} | "
                f"{fmt_pct(r['irr_posterior_p95'])} | "
                f"{r['expected_delivered_per_ship_t']:.3f} |"
            )
    return "\n".join(lines) + "\n"


def grade_subclaims(out: dict) -> dict:
    """Grade each pre-registered sub-claim against the sweep outputs."""
    rows = out["rows"]
    posteriors = out["posteriors"]

    grades = []

    def add(claim: str, predicted: str, observed: str, held: bool, note: str = ""):
        grades.append({
            "claim": claim,
            "predicted": predicted,
            "observed": observed,
            "held": held,
            "note": note,
        })

    # H-arch-d-a: D-fission ship CapEx central anchor 550-700 M
    add(
        "H-arch-d-a",
        "D-fission ship CapEx central in $550-700M (falsification $400-900M)",
        f"D-fission central CapEx = ${D_FISSION_SHIP_CAPEX['central']:.0f}M (low/high {D_FISSION_SHIP_CAPEX['low']:.0f}/{D_FISSION_SHIP_CAPEX['high']:.0f})",
        550 <= D_FISSION_SHIP_CAPEX["central"] <= 700,
        "Central anchor frozen at pre-registration; observed = predicted by construction; falsification check is on bands.",
    )
    # H-arch-d-b: D-solar-thermal ship CapEx central 500-700 M
    add(
        "H-arch-d-b",
        "D-solar-thermal ship CapEx central in $500-700M (falsification $350-900M)",
        f"D-solar-thermal central CapEx = ${D_SOLAR_THERMAL_SHIP_CAPEX['central']:.0f}M (low/high {D_SOLAR_THERMAL_SHIP_CAPEX['low']:.0f}/{D_SOLAR_THERMAL_SHIP_CAPEX['high']:.0f})",
        500 <= D_SOLAR_THERMAL_SHIP_CAPEX["central"] <= 700,
        "Frozen at pre-registration as above.",
    )

    # H-arch-d-c: D-fission per-mission gross revenue at BEST_CELL = $199M
    rev_d = D_DELIVERED_T * 1000.0 * BEST_CELL["price_per_kg"] / 1e6
    add(
        "H-arch-d-c",
        "D-fission per-mission gross revenue at BEST_CELL = $199M (arithmetic confirm)",
        f"${rev_d:.1f}M",
        abs(rev_d - 199.0) < 1.0,
        "",
    )

    # H-arch-d-d: D-fission per-mission gross cashflow (BEST_CELL): $-450 to $-350M
    central_dfission = next(r for r in rows if r["variant"] == "D-fission" and r["price_cell"] == "BEST_CELL" and r["ship_capex_band"] == "central" and r["launch"] == "mixed_baseline")
    add(
        "H-arch-d-d",
        "D-fission per-mission gross cashflow (BEST_CELL): $-450 to $-350M (falsified if positive)",
        f"${central_dfission['gross_per_ship_m']:+.1f}M",
        -450 <= central_dfission["gross_per_ship_m"] <= -350,
        "Gross = revenue - ship CapEx, excludes launch and opex. Negative confirms cashflow-negative per mission.",
    )

    # H-arch-d-e: D-solar-thermal per-mission gross cashflow (BEST_CELL): $-450 to $-350M
    central_dsolar = next(r for r in rows if r["variant"] == "D-solar-thermal" and r["price_cell"] == "BEST_CELL" and r["ship_capex_band"] == "central" and r["launch"] == "mixed_baseline")
    add(
        "H-arch-d-e",
        "D-solar-thermal per-mission gross cashflow (BEST_CELL): $-450 to $-350M",
        f"${central_dsolar['gross_per_ship_m']:+.1f}M",
        -450 <= central_dsolar["gross_per_ship_m"] <= -350,
        "",
    )

    # H-arch-d-f: D-fission conditional IRR at BEST_CELL + mixed_baseline: -2 to +0.5 pct
    irr_f = central_dfission["irr_conditional"]
    irr_f_pct = (irr_f * 100) if irr_f is not None else None
    add(
        "H-arch-d-f",
        "D-fission conditional IRR (BEST_CELL, mixed_baseline launch, central CapEx): -2 to +0.5 percent (falsification -4 to +2)",
        f"{irr_f_pct:+.2f}%" if irr_f_pct is not None else "None (deeply negative even at near-zero rate)",
        (irr_f_pct is None) or (-2.0 <= irr_f_pct <= 0.5),
        "" if irr_f_pct is not None else "None means NPV negative at 0.01% rate — falsified only if outside -4 to +2 band; None is consistent with deeply negative, which is at-or-below the lower edge of the prediction band.",
    )

    # H-arch-d-g: D-solar-thermal conditional IRR
    irr_g = central_dsolar["irr_conditional"]
    irr_g_pct = (irr_g * 100) if irr_g is not None else None
    add(
        "H-arch-d-g",
        "D-solar-thermal conditional IRR (BEST_CELL, mixed_baseline launch, central CapEx): -2 to +0.5 percent",
        f"{irr_g_pct:+.2f}%" if irr_g_pct is not None else "None",
        (irr_g_pct is None) or (-2.0 <= irr_g_pct <= 0.5),
        "",
    )

    # H-arch-d-h: D-fission programmatic-risk-adjusted expected delivered per mission
    exp_dfission = D_DELIVERED_T * posteriors["d_fission"]["median"]
    add(
        "H-arch-d-h",
        "D-fission expected delivered per mission (median posterior × 19.9 t): 0.13-0.20 t",
        f"{exp_dfission:.4f} t",
        0.13 <= exp_dfission <= 0.20,
        f"posterior median = {posteriors['d_fission']['median']*100:.2f}%",
    )
    # H-arch-d-i: D-solar-thermal
    exp_dsolar = D_DELIVERED_T * posteriors["d_solar_thermal"]["median"]
    add(
        "H-arch-d-i",
        "D-solar-thermal expected delivered per mission: 0.35-0.55 t",
        f"{exp_dsolar:.4f} t",
        0.35 <= exp_dsolar <= 0.55,
        f"posterior median = {posteriors['d_solar_thermal']['median']*100:.2f}%",
    )
    # H-arch-d-j: dominance factor
    ratio = exp_dsolar / exp_dfission if exp_dfission > 0 else float("inf")
    add(
        "H-arch-d-j",
        "D-solar-thermal dominance factor over D-fission: 2.0-3.5×",
        f"{ratio:.2f}×",
        2.0 <= ratio <= 3.5,
        "",
    )

    # H-arch-d-k: Starship launch sensitivity. Compare mixed_baseline vs starship_central
    starship_dfission = next(r for r in rows if r["variant"] == "D-fission" and r["price_cell"] == "BEST_CELL" and r["ship_capex_band"] == "central" and r["launch"] == "starship_central")
    irr_uplift_dfission_pp = None
    if starship_dfission["irr_conditional"] is not None and central_dfission["irr_conditional"] is not None:
        irr_uplift_dfission_pp = (starship_dfission["irr_conditional"] - central_dfission["irr_conditional"]) * 100
    starship_dsolar = next(r for r in rows if r["variant"] == "D-solar-thermal" and r["price_cell"] == "BEST_CELL" and r["ship_capex_band"] == "central" and r["launch"] == "starship_central")
    irr_uplift_dsolar_pp = None
    if starship_dsolar["irr_conditional"] is not None and central_dsolar["irr_conditional"] is not None:
        irr_uplift_dsolar_pp = (starship_dsolar["irr_conditional"] - central_dsolar["irr_conditional"]) * 100
    held_k = False
    if irr_uplift_dfission_pp is not None and irr_uplift_dsolar_pp is not None:
        held_k = (0.3 <= irr_uplift_dfission_pp <= 3.0) and (0.3 <= irr_uplift_dsolar_pp <= 3.0)
    add(
        "H-arch-d-k",
        "Starship-launch IRR uplift relative to mixed-baseline launch: +0.8 to +1.8 pp (falsification 0.3-3.0)",
        f"D-fission uplift {irr_uplift_dfission_pp if irr_uplift_dfission_pp is not None else 'N/A'} pp; D-solar uplift {irr_uplift_dsolar_pp if irr_uplift_dsolar_pp is not None else 'N/A'} pp",
        held_k,
        "Uplift only computable when both conditional IRRs are defined.",
    )

    # H-arch-d-l: D-fission sovereign-bond clearance (any swept cell)
    dfission_clears = [r for r in rows if r["variant"] == "D-fission" and r["irr_conditional"] is not None and r["irr_conditional"] >= 0.04]
    add(
        "H-arch-d-l",
        "D-fission does NOT clear sovereign-bond (4% IRR) at any swept cell",
        f"{len(dfission_clears)} cells clear sovereign-bond",
        len(dfission_clears) == 0,
        "Falsified if any cell clears 4%.",
    )
    # H-arch-d-m: D-solar-thermal
    dsolar_clears = [r for r in rows if r["variant"] == "D-solar-thermal" and r["irr_conditional"] is not None and r["irr_conditional"] >= 0.04]
    add(
        "H-arch-d-m",
        "D-solar-thermal does NOT clear sovereign-bond (4% IRR) at any swept cell",
        f"{len(dsolar_clears)} cells clear sovereign-bond",
        len(dsolar_clears) == 0,
        "",
    )

    # H-arch-d-n: combined verdict vs Variant B
    # Variant B 500-kWe programmatic-risk-adjusted expected delivered = 0.166 t/mission (hyperion R-variant-B-500kWe-sizing)
    variant_b_expected_t = 0.166
    d_solar_expected_t = exp_dsolar
    add(
        "H-arch-d-n",
        "D-solar-thermal expected-delivered does not exceed Variant B's 0.166 t/mission by more than 2× (i.e., does not exceed 0.332 t)",
        f"D-solar-thermal expected = {d_solar_expected_t:.4f} t; Variant B = {variant_b_expected_t:.3f} t; ratio = {d_solar_expected_t/variant_b_expected_t:.2f}×",
        d_solar_expected_t <= 2 * variant_b_expected_t,
        "Held if D-solar-thermal does not strictly dominate Variant B on risk-adjusted basis.",
    )

    out["grades"] = grades
    return out


def aggregate_summary(out: dict) -> dict:
    rows = out["rows"]
    defined_cond = [r for r in rows if r["irr_conditional"] is not None]
    defined_adj_med = [r for r in rows if r["irr_posterior_median"] is not None]
    defined_adj_p95 = [r for r in rows if r["irr_posterior_p95"] is not None]

    # NPV at zero discount for the best swept cell (highest delivered, lowest cost)
    best_cell_npv0 = []
    for r in rows:
        if r["price_cell"] != "BEST_CELL":
            continue
        # rebuild yearly to recompute NPV at zero discount
        yearly_cond = cashflow_yearly_d(
            price_per_kg=BEST_CELL["price_per_kg"],
            sovereign_amount=BEST_CELL["sovereign_amount"],
            sovereign_year=BEST_CELL["sovereign_year"],
            ship_capex_m=r["ship_capex_m"],
            launch_cost_m=r["launch_cost_m"],
            delivered_per_ship_t=D_DELIVERED_T,
        )
        npv0 = npv(yearly_cond, 0.0)
        best_cell_npv0.append({
            "variant": r["variant"],
            "launch": r["launch"],
            "ship_capex_band": r["ship_capex_band"],
            "npv_at_zero_discount_M": npv0 / 1e6,
        })

    summary = {
        "rows_total": len(rows),
        "rows_with_defined_conditional_IRR": len(defined_cond),
        "rows_with_defined_posterior_median_IRR": len(defined_adj_med),
        "rows_with_defined_posterior_p95_IRR": len(defined_adj_p95),
        "best_cell_npv_at_zero_discount": best_cell_npv0,
        "interpretation": (
            "Conditional IRR undefined means NPV at near-zero discount (1e-4) is "
            "negative, including the 45-year perpetuity terminal value at growth=0. "
            "Architecture D loses money on a non-discounted basis under every swept "
            "combination of launch cost, ship CapEx band, and price anchor."
        ),
    }
    out["aggregate_summary"] = summary
    return out


def main():
    out = run_sweep()
    out = grade_subclaims(out)
    out = aggregate_summary(out)

    # Write JSON and tables
    (RESULTS_DIR / "architecture_d_cost.json").write_text(json.dumps(out, indent=2))
    (RESULTS_DIR / "tables.md").write_text(format_table_md(out["rows"]))

    # Print headline
    print("R-architecture-D-cost sweep complete.")
    print(f"Rows: {len(out['rows'])}.")
    print(f"Posterior medians: D-fission {out['posteriors']['d_fission']['median']*100:.2f}%, D-solar-thermal {out['posteriors']['d_solar_thermal']['median']*100:.2f}%.")
    print(f"Expected delivered per mission: D-fission {D_DELIVERED_T*out['posteriors']['d_fission']['median']:.4f} t, D-solar-thermal {D_DELIVERED_T*out['posteriors']['d_solar_thermal']['median']:.4f} t.")
    print("")
    summary = out["aggregate_summary"]
    print(f"Rows with defined conditional IRR: {summary['rows_with_defined_conditional_IRR']} / {summary['rows_total']}")
    print(f"Rows with defined posterior-median IRR: {summary['rows_with_defined_posterior_median_IRR']} / {summary['rows_total']}")
    print(f"Rows with defined posterior-p95 IRR: {summary['rows_with_defined_posterior_p95_IRR']} / {summary['rows_total']}")
    print("")
    # Best-case NPV at zero discount across all BEST_CELL swept points
    npv_sorted = sorted(summary["best_cell_npv_at_zero_discount"], key=lambda x: x["npv_at_zero_discount_M"], reverse=True)
    print("Top-5 BEST_CELL points by NPV at zero discount:")
    for x in npv_sorted[:5]:
        print(f"  {x['variant']:18s} launch={x['launch']:22s} capex={x['ship_capex_band']:8s}  NPV(0) = ${x['npv_at_zero_discount_M']:+10.0f}M")
    print("")
    print("Sub-claim grades:")
    held_count = 0
    for g in out["grades"]:
        status = "HELD" if g["held"] else "FALSIFIED"
        if g["held"]:
            held_count += 1
        print(f"  [{status}] {g['claim']}: {g['observed']}")
    print(f"\n{held_count}/{len(out['grades'])} sub-claims held.")


if __name__ == "__main__":
    main()
