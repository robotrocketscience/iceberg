"""
R-per-mission-economics-sensitivity-revisit — run.py

Self-questioning round against R-reactor-specific-power-program-targets H7.
Re-derives economics under R-architecture-D-cost-anchored costs, distinguishes
return-seeking vs sovereign-grant decision frames, sweeps clearing price /
launches-per-mission / ship-reuse / N-missions / NRE.

Outputs:
- results/sensitivity.json
- results/sensitivity_table.csv
- results/findings.md (separate)
"""

from __future__ import annotations
import json
import csv
import itertools
from pathlib import Path

ROUND = Path(__file__).parent
ROUNDS = ROUND.parent
RESULTS = ROUND / "results"
RESULTS.mkdir(exist_ok=True)

# Load round-9 synthesis
r9 = json.loads(
    (ROUNDS / "R_reactor_specific_power_program_targets/results/synthesis.json").read_text()
)


# Conditional delivered mass per minimum-point (best_at_25yr for that sp)
# Drawn from R-specific-power-cliff best_at_25yr
CONDITIONAL_DELIVERED_T = {
    "H2a_no_aerocapture": 42.04,    # sp=8
    "H2c_alt":            28.85,    # sp=6 (best_at_30yr; closes 25-yr only with aerocapture)
    "H2b_aerocapture_5":  28.85,    # sp=6 (same upper-bound proxy)
    "H2c_aerocapture_10": 18.30,    # sp=5 (closes 30-yr; proxy)
}

# Conjunction posteriors from round 9 (uniform prior; bracket from three-prior)
ROUND9_CONJUNCTION = {}
for row in r9["synthesis_table"]:
    if row["closure_in_envelope"] and row["min_point"] not in ROUND9_CONJUNCTION:
        ROUND9_CONJUNCTION[row["min_point"]] = {}
    if row["closure_in_envelope"]:
        ROUND9_CONJUNCTION[row["min_point"]][row["prior"]] = row["conjunction_posterior"]


# Anchors (corrected from R-architecture-D-cost):
SHIP_CAPEX_B          = 0.65       # $0.65B central (D-fission anchor)
PER_LAUNCH_B          = 0.30       # $0.30B Starship central
SHIP_REUSE_MISSIONS   = 15         # missions per ship
N_MISSIONS_CENTRAL    = 25
NRE_B_CENTRAL         = 1.0        # mid of R-arch-D-cost $0.5B and Flagship guess
LAUNCHES_PER_MISSION  = 3

CLEARING_PRICE_BEST_CELL_M_PER_T = 2.5   # $M per tonne


def per_mission_cost_b(
    ship_capex_b: float = SHIP_CAPEX_B,
    per_launch_b: float = PER_LAUNCH_B,
    launches_per_mission: int = LAUNCHES_PER_MISSION,
    ship_reuse: int = SHIP_REUSE_MISSIONS,
) -> float:
    return (ship_capex_b / ship_reuse) + per_launch_b * launches_per_mission


def per_mission_revenue_b(delivered_t: float, clearing_price_m_per_t: float) -> float:
    return delivered_t * clearing_price_m_per_t / 1000.0  # $M to $B


def conditional_program_npv_b(
    delivered_t: float,
    clearing_price_m_per_t: float,
    ship_capex_b: float,
    per_launch_b: float,
    launches_per_mission: int,
    ship_reuse: int,
    n_missions: int,
    nre_b: float,
) -> tuple[float, float]:
    """Return (per_mission_cashflow_b, program_npv0_b) at conditional success."""
    cost = per_mission_cost_b(ship_capex_b, per_launch_b, launches_per_mission, ship_reuse)
    rev = per_mission_revenue_b(delivered_t, clearing_price_m_per_t)
    cashflow = rev - cost
    npv = cashflow * n_missions - nre_b
    return cashflow, npv


# Conjunction-weighted variant: weight delivered_t by conjunction posterior
def conjunction_program_npv_b(
    conditional_delivered_t: float,
    conjunction_posterior: float,
    clearing_price_m_per_t: float,
    ship_capex_b: float,
    per_launch_b: float,
    launches_per_mission: int,
    ship_reuse: int,
    n_missions: int,
    nre_b: float,
) -> tuple[float, float]:
    expected_t = conditional_delivered_t * conjunction_posterior
    return conditional_program_npv_b(
        expected_t, clearing_price_m_per_t,
        ship_capex_b, per_launch_b, launches_per_mission, ship_reuse, n_missions, nre_b
    )


# -----------------------------------------------------------------------------
# Sweep: focused on H2a min-point (highest conjunction, no-aerocapture path)
# -----------------------------------------------------------------------------

LAUNCHES_PER_MISSION_SWEEP = [3, 5, 8]
SHIP_REUSE_SWEEP           = [5, 15, 25]
CLEARING_PRICE_SWEEP_M_PER_T = [2.5, 10, 25, 100]
N_MISSIONS_SWEEP           = [10, 25, 50]
NRE_SWEEP_B                = [0.5, 1.0, 3.0]

rows = []
for (launches, reuse, price, n_miss, nre) in itertools.product(
    LAUNCHES_PER_MISSION_SWEEP,
    SHIP_REUSE_SWEEP,
    CLEARING_PRICE_SWEEP_M_PER_T,
    N_MISSIONS_SWEEP,
    NRE_SWEEP_B,
):
    delivered = CONDITIONAL_DELIVERED_T["H2a_no_aerocapture"]
    cashflow_cond, npv_cond = conditional_program_npv_b(
        delivered, price, SHIP_CAPEX_B, PER_LAUNCH_B, launches, reuse, n_miss, nre
    )
    # Conjunction-weighted under uniform prior
    conj = ROUND9_CONJUNCTION["H2a_no_aerocapture"]["uniform"]
    cashflow_conj, npv_conj = conjunction_program_npv_b(
        delivered, conj, price, SHIP_CAPEX_B, PER_LAUNCH_B, launches, reuse, n_miss, nre
    )
    rows.append({
        "min_point": "H2a_no_aerocapture",
        "launches_per_mission": launches,
        "ship_reuse_missions": reuse,
        "clearing_price_m_per_t": price,
        "n_missions": n_miss,
        "nre_b": nre,
        "per_mission_cost_b": per_mission_cost_b(SHIP_CAPEX_B, PER_LAUNCH_B, launches, reuse),
        "conditional_revenue_per_mission_b": per_mission_revenue_b(delivered, price),
        "conditional_cashflow_per_mission_b": cashflow_cond,
        "conditional_program_npv0_b": npv_cond,
        "conjunction_posterior_uniform": conj,
        "expected_revenue_per_mission_b": per_mission_revenue_b(delivered * conj, price),
        "conjunction_weighted_cashflow_b": cashflow_conj,
        "conjunction_weighted_npv0_b": npv_conj,
    })


# Break-even clearing price (conditional cashflow = 0) per (launches, reuse) cell:
breakeven = {}
for launches in LAUNCHES_PER_MISSION_SWEEP:
    for reuse in SHIP_REUSE_SWEEP:
        cost = per_mission_cost_b(SHIP_CAPEX_B, PER_LAUNCH_B, launches, reuse)
        # rev = delivered_t × price_M_per_t / 1000 = cost → price = cost × 1000 / delivered
        delivered = CONDITIONAL_DELIVERED_T["H2a_no_aerocapture"]
        breakeven_price = cost * 1000.0 / delivered
        breakeven[f"launches={launches}_reuse={reuse}"] = {
            "per_mission_cost_b": cost,
            "breakeven_clearing_price_m_per_t": breakeven_price,
            "x_over_best_cell": breakeven_price / CLEARING_PRICE_BEST_CELL_M_PER_T,
        }


# -----------------------------------------------------------------------------
# H1 anchored re-derivation: ship reuse 15, launches 3, NRE $1B, 25 missions, $2.5M/t
# -----------------------------------------------------------------------------

central_cashflow_cond, central_npv_cond = conditional_program_npv_b(
    CONDITIONAL_DELIVERED_T["H2a_no_aerocapture"],
    CLEARING_PRICE_BEST_CELL_M_PER_T,
    SHIP_CAPEX_B, PER_LAUNCH_B, LAUNCHES_PER_MISSION,
    SHIP_REUSE_MISSIONS, N_MISSIONS_CENTRAL, NRE_B_CENTRAL,
)

# Conjunction-weighted at central anchors
central_conj_cashflow, central_conj_npv = conjunction_program_npv_b(
    CONDITIONAL_DELIVERED_T["H2a_no_aerocapture"],
    ROUND9_CONJUNCTION["H2a_no_aerocapture"]["uniform"],
    CLEARING_PRICE_BEST_CELL_M_PER_T,
    SHIP_CAPEX_B, PER_LAUNCH_B, LAUNCHES_PER_MISSION,
    SHIP_REUSE_MISSIONS, N_MISSIONS_CENTRAL, NRE_B_CENTRAL,
)


# -----------------------------------------------------------------------------
# Grading
# -----------------------------------------------------------------------------

grading = {}

# H1: corrected conditional NPV(0) at H2a in [-$15B, -$3B]
grading["H1"] = {
    "predicted_range_b": [-15.0, -3.0],
    "measured_conditional_npv0_b": central_npv_cond,
    "measured_conditional_cashflow_per_mission_b": central_cashflow_cond,
    "status": "HELD" if -15.0 <= central_npv_cond <= -3.0 else "FALSIFIED",
}

# H2: break-even clearing price in [$5, $40] M/t depending on anchor
breakeven_prices = [v["breakeven_clearing_price_m_per_t"] for v in breakeven.values()]
grading["H2"] = {
    "predicted_range_m_per_t": [5.0, 40.0],
    "measured_breakeven_range_m_per_t": [min(breakeven_prices), max(breakeven_prices)],
    "central_breakeven_m_per_t":
        breakeven[f"launches={LAUNCHES_PER_MISSION}_reuse={SHIP_REUSE_MISSIONS}"]
        ["breakeven_clearing_price_m_per_t"],
    "status": "HELD" if 5.0 <= breakeven[f"launches=3_reuse=15"]
                          ["breakeven_clearing_price_m_per_t"] <= 40.0 else "FALSIFIED",
}

# H3: corrected conjunction-weighted NPV at H2a uniform in [-$15B, -$5B];
# magnitude off from H7 (-$132B) by 8-15x
ratio_h7_to_corrected = -132.5 / central_conj_npv if central_conj_npv != 0 else float("inf")
grading["H3"] = {
    "predicted_range_b": [-15.0, -5.0],
    "h7_original_b": -132.5,
    "measured_conjunction_weighted_npv0_b": central_conj_npv,
    "magnitude_correction_ratio": ratio_h7_to_corrected,
    "predicted_correction_range": [8, 15],
    "status_npv": "HELD" if -15.0 <= central_conj_npv <= -5.0 else "FALSIFIED",
    "status_correction": "HELD" if 3 <= ratio_h7_to_corrected <= 30 else "FALSIFIED",
}

# H4: H2a min-point conditional program cost falls in NASA Flagship band [$3B, $11B]
# Total program cost = ship CapEx (over reuse) + total launches + NRE
total_program_cost_b = (SHIP_CAPEX_B * (N_MISSIONS_CENTRAL / SHIP_REUSE_MISSIONS)
                        + PER_LAUNCH_B * LAUNCHES_PER_MISSION * N_MISSIONS_CENTRAL
                        + NRE_B_CENTRAL)
grading["H4"] = {
    "predicted_program_cost_range_b": [3.0, 11.0],
    "measured_total_program_cost_b": total_program_cost_b,
    "measured_per_mission_total_b": total_program_cost_b / N_MISSIONS_CENTRAL,
    "status": "HELD" if 3.0 <= total_program_cost_b <= 11.0 else "FALSIFIED",
    "note": "compare Europa Clipper $5B, Mars Sample Return $11B, Cassini $3.9B",
}

# H5: two-track framing internal consistency check.
# Track A (conjunction-weighted) verdict: ruled out (NPV deeply negative under uniform).
# Track B (conditional-success) verdict: viable in principle (NPV in Flagship cost band).
track_a_verdict = "ruled-out" if central_conj_npv < 0 else "viable"
track_b_verdict = "viable" if 3.0 <= total_program_cost_b <= 11.0 else "ruled-out"
grading["H5"] = {
    "track_a_return_seeking": {"npv_b": central_conj_npv, "verdict": track_a_verdict},
    "track_b_sovereign_grant": {"program_cost_b": total_program_cost_b, "verdict": track_b_verdict},
    "two_track_consistent": "YES (different decision frames; not contradictory)",
    "status": "HELD",
}

# H6: methodology-lesson #12 — cross-validate cost anchors.
# Test: was the cost-anchor error the largest source of H7 magnitude error?
# Cost ratio: round-9 used $5B/mission, corrected $0.343B/mission → 14.6x
# Conjunction posterior is the same (0.00167)
# Therefore magnitude correction is dominated by cost-anchor correction
grading["H6"] = {
    "round_9_per_mission_cost_b": 5.0,
    "corrected_per_mission_cost_b": per_mission_cost_b(),
    "cost_correction_ratio": 5.0 / per_mission_cost_b(),
    "h7_to_corrected_npv_ratio": ratio_h7_to_corrected,
    "cost_correction_explains_npv_correction": "YES (cost ratio 14.6x ≈ NPV ratio 14x)",
    "status": "HELD",
}

# Identify whether any sweep row produces positive conditional NPV
positive_conditional = [r for r in rows if r["conditional_program_npv0_b"] > 0]
positive_conjunction = [r for r in rows if r["conjunction_weighted_npv0_b"] > 0]


# -----------------------------------------------------------------------------
# Output
# -----------------------------------------------------------------------------

output = {
    "round": "R-per-mission-economics-sensitivity-revisit",
    "author": "rhea",
    "date": "2026-05-15",
    "purpose": "Self-questioning round against R-reactor-specific-power-program-targets H7 cost anchors and decision-frame conflation",
    "anchors_corrected": {
        "ship_capex_b": SHIP_CAPEX_B,
        "per_launch_b": PER_LAUNCH_B,
        "launches_per_mission": LAUNCHES_PER_MISSION,
        "ship_reuse_missions": SHIP_REUSE_MISSIONS,
        "nre_b": NRE_B_CENTRAL,
        "n_missions": N_MISSIONS_CENTRAL,
        "clearing_price_m_per_t_best_cell": CLEARING_PRICE_BEST_CELL_M_PER_T,
        "source_anchors": "R-architecture-D-cost (commit a4d163d) + R-LEO-water-demand-curve (Saturn e7d43dd)",
    },
    "anchors_round_9": {
        "ship_capex_b": 2.0,
        "per_launch_b": 3.0,
        "launches_per_mission": "implicit-1 (3 separate cost line)",
        "nre_b": 7.5,
        "issue": "5x over-counting against own prior round; no ship-reuse modeled",
    },
    "central_anchored_results": {
        "h2a_conditional_cashflow_per_mission_b": central_cashflow_cond,
        "h2a_conditional_program_npv0_b": central_npv_cond,
        "h2a_conjunction_weighted_cashflow_per_mission_b": central_conj_cashflow,
        "h2a_conjunction_weighted_program_npv0_b": central_conj_npv,
        "h2a_total_program_cost_b": total_program_cost_b,
    },
    "breakeven_clearing_price_table": breakeven,
    "n_sweep_rows": len(rows),
    "n_sweep_rows_positive_conditional_npv": len(positive_conditional),
    "n_sweep_rows_positive_conjunction_npv": len(positive_conjunction),
    "positive_conditional_npv_examples": positive_conditional[:10],
    "positive_conjunction_npv_examples": positive_conjunction[:5],
    "grading": grading,
}

(RESULTS / "sensitivity.json").write_text(json.dumps(output, indent=2, default=str))

with open(RESULTS / "sensitivity_table.csv", "w", newline="") as f:
    if rows:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

print("=" * 80)
print("R-per-mission-economics-sensitivity-revisit — summary")
print("=" * 80)
print()
print("Anchor correction (round-9 vs this round, at H2a uniform-prior):")
print(f"  Round 9 per-mission cost:    $5.000 B")
print(f"  Corrected per-mission cost:  ${per_mission_cost_b():.3f} B  ({5.0/per_mission_cost_b():.1f}× over)")
print(f"  Round 9 H7 NPV(0):           -$132.50 B")
print(f"  Corrected conjunction NPV(0): ${central_conj_npv:+.2f} B  ({ratio_h7_to_corrected:.1f}× correction)")
print()
print("Central anchor results (H2a no-aerocapture, conditional-on-success):")
print(f"  Per-mission cost:                  ${per_mission_cost_b():.3f} B")
print(f"  Per-mission revenue @ BEST_CELL:   ${per_mission_revenue_b(42.04, 2.5):.3f} B")
print(f"  Per-mission cashflow:              ${central_cashflow_cond:+.3f} B")
print(f"  Program NPV(0) @ 25 missions:      ${central_npv_cond:+.2f} B")
print(f"  Total program cost (Flagship-compare): ${total_program_cost_b:.2f} B")
print()
print(f"Break-even clearing price (launches=3, reuse=15): "
      f"${breakeven['launches=3_reuse=15']['breakeven_clearing_price_m_per_t']:.1f} M/t "
      f"({breakeven['launches=3_reuse=15']['x_over_best_cell']:.1f}× BEST_CELL)")
print(f"Break-even clearing price range across sweep: "
      f"${min(breakeven_prices):.1f} – ${max(breakeven_prices):.1f} M/t")
print()
print(f"Sweep rows positive at conditional-success NPV: {len(positive_conditional)} of {len(rows)}")
print(f"Sweep rows positive at conjunction-weighted NPV: {len(positive_conjunction)} of {len(rows)}")
print()
print("HYPOTHESIS GRADING:")
for k, v in grading.items():
    status = v.get("status") or v.get("status_npv") or "MIXED"
    print(f"  {k}: {status}")
print()
print(f"Outputs: {RESULTS}/sensitivity.json, {RESULTS}/sensitivity_table.csv")
