"""R-bottoms-up-vehicle-cost — subsystem-level Monte Carlo on first-unit vehicle
cost for Variant B / Arch E_500 / Arch E_200, propagated through R7's fleet-ramp
NPV and R8's two-factor clearing-price model.

Usage:
    python3 run.py

Outputs to results/:
    cost_distributions.csv        — per-architecture first-unit cost MC stats
    cost_distributions.json       — full sample arrays (downsampled)
    npv_prob_grid.csv             — P(NPV≥0) for each (arch, WACC, LR, cost-regime)
    hypothesis_scoring.md         — H-bvc-a ... H-bvc-n scoring
    summary.md                    — human-readable headline

The cost MC is deliberately wide on reactor / thruster lines (factor-3 5-95% span)
because nuclear-electric components above the FSP Phase-1 / KRUSTY power class have
no calibrated cost-estimating relationship.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# Re-use R7 architecture + NPV machinery
HERE = Path(__file__).resolve().parent
R7_DIR = HERE.parent / "R_fleet_ramp_NPV"
sys.path.insert(0, str(R7_DIR))
from run import Architecture, fleet_ramp_npv, wright_unit_cost  # noqa: E402

RESULTS_DIR = HERE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(20260515)
N_COST_SAMPLES = 10_000
N_PRICE_SAMPLES = 10_000  # matches R8


# ---------------------------------------------------------------------------
# Subsystem cost stacks. Median is in $M. Sigma is on the log-scale: a sigma of
# 0.20 means roughly +/- 50% 5-95% spread; sigma 0.55 means roughly factor-3.
# Anchors documented in STUDY.md §Heritage anchors.
# ---------------------------------------------------------------------------
@dataclass
class Subsystem:
    name: str
    median_M: float
    log_sigma: float  # log-normal sigma; ~0.20 ≈ ±50%, ~0.55 ≈ factor-3


@dataclass
class CostStack:
    arch_name: str
    subsystems: list[Subsystem]
    integration_test_frac_median: float = 0.20
    integration_test_frac_logsigma: float = 0.25  # ~ ±28%
    program_overhead_frac_median: float = 0.25
    program_overhead_frac_logsigma: float = 0.28  # ~ ±32%


VARIANT_B_STACK = CostStack(
    arch_name="VariantB_500kWe",
    subsystems=[
        Subsystem("reactor_kp_class_10kWe", 300.0, 0.55),    # KP-class + Stirling; high uncertainty
        Subsystem("chemical_kick_stage", 64.0, 0.20),         # liquid stage heritage
        Subsystem("bag_harvest", 60.0, 0.30),                 # novel deployable
        Subsystem("solar_housekeeping", 30.0, 0.20),
        Subsystem("pmad", 60.0, 0.25),
        Subsystem("avionics_gnc_comms", 160.0, 0.20),
        Subsystem("structure_tanks", 60.0, 0.20),
        Subsystem("thermal_control", 45.0, 0.20),
    ],
)

# Note: Variant B uses a 500 kWe reactor PER ROUND-7's Architecture definition
# (VariantB_500kWe). R7 uses chemical Saturn-departure + 500-kWe electric for
# cruise. STUDY.md reference cell A above describes a Kilopower-10-kWe version;
# the model below uses ROUND-7's actual Variant B (500-kWe reactor + chemical
# kick), so the reactor subsystem cost should be the 500-kWe stack with chemical
# kick added. Replacing 300 -> ~1500 (500-kWe reactor) + keep chemical kick line:

VARIANT_B_R7_MATCHED_STACK = CostStack(
    arch_name="VariantB_500kWe",
    subsystems=[
        Subsystem("reactor_500kWe_brayton", 1500.0, 0.55),  # same 500-kWe reactor as Arch E
        Subsystem("pmad_500kWe", 160.0, 0.25),
        Subsystem("radiator_marvl", 360.0, 0.30),
        Subsystem("chemical_kick_stage", 64.0, 0.20),         # B-specific: chemical Saturn departure
        Subsystem("bag_harvest", 60.0, 0.30),
        Subsystem("thruster_array_smaller", 240.0, 0.45),     # ~8 thrusters for 500 kWe cruise (B uses electric for cruise too)
        Subsystem("avionics_gnc_comms", 160.0, 0.20),
        Subsystem("structure_tanks", 80.0, 0.20),             # bigger tankage for kick propellant
        Subsystem("thermal_control", 45.0, 0.20),
    ],
)

ARCH_E_500_STACK = CostStack(
    arch_name="E_500kWe_200t",
    subsystems=[
        Subsystem("reactor_500kWe_fission_brayton", 1500.0, 0.55),
        Subsystem("pmad_500kWe", 160.0, 0.25),
        Subsystem("radiator_marvl", 360.0, 0.30),
        Subsystem("thruster_array_20x_AEPS", 600.0, 0.45),   # 20 units × $30M, factor-2.5 span
        Subsystem("bag_harvest", 60.0, 0.30),
        Subsystem("avionics_gnc_comms", 160.0, 0.20),
        Subsystem("structure_tanks", 40.0, 0.20),
        Subsystem("thermal_control", 45.0, 0.20),
    ],
)

ARCH_E_200_STACK = CostStack(
    arch_name="E_200kWe_100t",
    subsystems=[
        Subsystem("reactor_200kWe_fission_brayton", 800.0, 0.55),
        Subsystem("pmad_200kWe", 80.0, 0.25),
        Subsystem("radiator_marvl_smaller", 150.0, 0.30),
        Subsystem("thruster_array_8x_AEPS", 240.0, 0.45),
        Subsystem("bag_harvest", 30.0, 0.30),
        Subsystem("avionics_gnc_comms", 160.0, 0.20),
        Subsystem("structure_tanks", 25.0, 0.20),
        Subsystem("thermal_control", 30.0, 0.20),
    ],
)


def sample_first_unit_cost(stack: CostStack, n: int, rng: np.random.Generator) -> dict:
    """Return n samples of first-unit total + per-subsystem breakdown for one stack."""
    hardware_total = np.zeros(n)
    subsystem_samples: dict[str, np.ndarray] = {}
    for sub in stack.subsystems:
        # Log-normal: median = exp(mu), so mu = ln(median). Sigma is on log scale.
        mu = math.log(sub.median_M)
        samples = rng.lognormal(mean=mu, sigma=sub.log_sigma, size=n)
        subsystem_samples[sub.name] = samples
        hardware_total += samples

    it_frac = rng.lognormal(
        mean=math.log(stack.integration_test_frac_median),
        sigma=stack.integration_test_frac_logsigma,
        size=n,
    )
    overhead_frac = rng.lognormal(
        mean=math.log(stack.program_overhead_frac_median),
        sigma=stack.program_overhead_frac_logsigma,
        size=n,
    )
    it = hardware_total * it_frac
    subtotal_with_it = hardware_total + it
    overhead = subtotal_with_it * overhead_frac
    first_unit = subtotal_with_it + overhead

    return {
        "hardware_total": hardware_total,
        "integration_test": it,
        "program_overhead": overhead,
        "first_unit": first_unit,
        "subsystems": subsystem_samples,
    }


# ---------------------------------------------------------------------------
# R8 clearing-price MC. Sigmas reproduced from R_LEO_water_demand_curve/STUDY.md.
# ---------------------------------------------------------------------------
def sample_clearing_price(n: int, rng: np.random.Generator) -> np.ndarray:
    """Returns n samples of clearing price in $/kg-to-LEO."""
    # Starship $/kg: 5th %ile 200, median 1500, 95th %ile 15000.
    mu_s = math.log(1500.0)
    sigma_s = (math.log(15000.0) - math.log(200.0)) / (2.0 * 1.6448536)
    starship = rng.lognormal(mean=mu_s, sigma=sigma_s, size=n)

    # In-space markup: 5th %ile 1.2, median 3.5, 95th %ile 15.
    mu_m = math.log(3.5)
    sigma_m = (math.log(15.0) - math.log(1.2)) / (2.0 * 1.6448536)
    markup = rng.lognormal(mean=mu_m, sigma=sigma_m, size=n)

    return starship * markup


# ---------------------------------------------------------------------------
# Architectures used in NPV propagation (round-7 values)
# ---------------------------------------------------------------------------
ARCH_VB = Architecture("VariantB_500kWe", 500.0, 200.0, 2000.0, 14.50, 80.0, 500.0)
ARCH_E500 = Architecture("E_500kWe_200t", 500.0, 200.0, 2934.0, 23.60, 50.0, 300.0)
ARCH_E200 = Architecture("E_200kWe_100t", 200.0, 100.0, 2000.0, 22.54, 30.0, 250.0)

ARCHS_AND_STACKS = [
    (ARCH_VB, VARIANT_B_R7_MATCHED_STACK),
    (ARCH_E500, ARCH_E_500_STACK),
    (ARCH_E200, ARCH_E_200_STACK),
]


def npv_break_even_revenue_for_cost(
    arch: Architecture,
    first_unit_cost_M: float,
    wacc: float,
    learning_rate: float,
    cadence_per_yr: float = 2.0,
    horizon_yr: float = 40.0,
    reusable: bool = False,
) -> float | None:
    """NPV = pv_capital(cost) + revenue × pv_revenue_factor.
    pv_capital and pv_revenue_factor depend only on (arch, wacc, learning_rate),
    so we can pre-compute one of each per (arch, wacc, lr) and then vectorize
    over cost and revenue.

    This wrapper is for clarity in scoring; the vectorized path is below.
    """
    arch_with_cost = Architecture(
        arch.name, arch.reactor_kwe, arch.chunk_t, arch.isp_s,
        arch.round_trip_yr, arch.delivered_t, first_unit_cost_M,
    )
    zero_rev = fleet_ramp_npv(
        arch_with_cost, wacc, revenue_per_mission_M=0.0,
        learning_rate=learning_rate, cadence_per_yr=cadence_per_yr,
        horizon_yr=horizon_yr, reusable=reusable,
    )
    one_rev = fleet_ramp_npv(
        arch_with_cost, wacc, revenue_per_mission_M=1.0,
        learning_rate=learning_rate, cadence_per_yr=cadence_per_yr,
        horizon_yr=horizon_yr, reusable=reusable,
    )
    constant = zero_rev["npv_M"]
    factor = one_rev["pv_revenue_M"]
    if factor <= 0:
        return None
    return -constant / factor


def precompute_factors(arch: Architecture, wacc: float, learning_rate: float):
    """Compute pv_capital_per_first_unit and pv_revenue_factor once.

    Because fleet_ramp_npv with first_unit_cost=1 gives the PV capital coefficient
    (scaling linearly in first_unit_cost), and revenue gives PV revenue factor,
    we can decompose:
        NPV(cost, rev) = -cost × pv_capital_factor + rev × pv_revenue_factor
    """
    # Compute pv_capital_factor: run fleet_ramp_npv with first_unit_cost = 1.0
    arch_unit = Architecture(
        arch.name, arch.reactor_kwe, arch.chunk_t, arch.isp_s,
        arch.round_trip_yr, arch.delivered_t, 1.0,
    )
    res = fleet_ramp_npv(
        arch_unit, wacc, revenue_per_mission_M=1.0,
        learning_rate=learning_rate, cadence_per_yr=2.0,
        horizon_yr=40.0, reusable=False,
    )
    # pv_capital_M is for first_unit_cost = 1.0, so it equals -pv_capital_factor.
    pv_capital_factor = -res["pv_capital_M"]  # positive coefficient
    pv_revenue_factor = res["pv_revenue_M"]
    return pv_capital_factor, pv_revenue_factor


def prob_npv_positive(
    arch: Architecture,
    first_unit_costs_M: np.ndarray,
    revenues_per_mission_M: np.ndarray,
    wacc: float,
    learning_rate: float,
) -> float:
    """Vectorized P(NPV ≥ 0). Pairs cost samples with revenue samples 1:1
    (independence assumed)."""
    pv_cap_factor, pv_rev_factor = precompute_factors(arch, wacc, learning_rate)
    npv = -first_unit_costs_M * pv_cap_factor + revenues_per_mission_M * pv_rev_factor
    return float(np.mean(npv >= 0.0))


def npv_distribution(
    arch: Architecture,
    first_unit_costs_M: np.ndarray,
    revenues_per_mission_M: np.ndarray,
    wacc: float,
    learning_rate: float,
) -> np.ndarray:
    pv_cap_factor, pv_rev_factor = precompute_factors(arch, wacc, learning_rate)
    return -first_unit_costs_M * pv_cap_factor + revenues_per_mission_M * pv_rev_factor


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print(f"R-bottoms-up-vehicle-cost — running with n_cost={N_COST_SAMPLES}, n_price={N_PRICE_SAMPLES}")

    # Step 1: per-architecture cost MC.
    cost_results: dict[str, dict] = {}
    for arch, stack in ARCHS_AND_STACKS:
        samples = sample_first_unit_cost(stack, N_COST_SAMPLES, RNG)
        cost_results[arch.name] = samples

    # Cost summary table.
    print("\nFirst-unit cost summary ($M):")
    print(f"  {'arch':<22} {'5%ile':>10} {'median':>10} {'mean':>10} {'95%ile':>10} {'spread (95/5)':>14}")
    cost_summary_rows = []
    for arch, _ in ARCHS_AND_STACKS:
        fu = cost_results[arch.name]["first_unit"]
        p5, p50, mean, p95 = (
            float(np.percentile(fu, 5)),
            float(np.percentile(fu, 50)),
            float(np.mean(fu)),
            float(np.percentile(fu, 95)),
        )
        spread = p95 / p5
        print(f"  {arch.name:<22} {p5:>10.0f} {p50:>10.0f} {mean:>10.0f} {p95:>10.0f} {spread:>14.2f}")
        cost_summary_rows.append({
            "arch": arch.name, "p5_M": p5, "p50_M": p50, "mean_M": mean,
            "p95_M": p95, "spread_95_over_5": spread,
        })

    # Step 2: subsystem-share check for Arch E_500 (H-bvc-e).
    e500 = cost_results["E_500kWe_200t"]
    reactor = e500["subsystems"]["reactor_500kWe_fission_brayton"]
    pmad = e500["subsystems"]["pmad_500kWe"]
    thruster = e500["subsystems"]["thruster_array_20x_AEPS"]
    big_three = reactor + pmad + thruster
    big_three_share = float(np.mean(big_three / e500["hardware_total"]))
    print(f"\nArch E_500: reactor+PMAD+thrusters share of hardware = {big_three_share*100:.1f}%")
    print("(Note: hardware fraction; total first-unit share is slightly lower because I&T + overhead inflate denominator equally.)")
    big_three_first_unit_share = float(np.mean(big_three / e500["first_unit"]))
    print(f"Arch E_500: reactor+PMAD+thrusters share of FIRST UNIT total = {big_three_first_unit_share*100:.1f}%")

    # Step 3: recurring-unit cost at unit 33 with LR 15%.
    lr15_exp = math.log(1.0 - 0.15) / math.log(2.0)
    factor_unit33_lr15 = 33.0 ** lr15_exp
    print(f"\nWright's-Law factor at unit 33, LR 15%: {factor_unit33_lr15:.3f}")
    recurring_summary = []
    for arch, _ in ARCHS_AND_STACKS:
        fu = cost_results[arch.name]["first_unit"]
        rec = fu * factor_unit33_lr15
        p50_rec = float(np.percentile(rec, 50))
        print(f"  {arch.name:<22} recurring median = ${p50_rec:.0f}M")
        recurring_summary.append({
            "arch": arch.name, "recurring_p50_lr15_M": p50_rec,
            "recurring_p5_M": float(np.percentile(rec, 5)),
            "recurring_p95_M": float(np.percentile(rec, 95)),
        })

    # Step 4: clearing price → revenue/mission for each arch.
    clearing = sample_clearing_price(N_PRICE_SAMPLES, RNG)
    rev_per_mission: dict[str, np.ndarray] = {}
    for arch, _ in ARCHS_AND_STACKS:
        # revenue = clearing_$/kg × delivered_t × 1000 kg/t / 1e6 = clearing × delivered_t / 1000
        rev_per_mission[arch.name] = clearing * arch.delivered_t / 1000.0  # in $M
    print(f"\nClearing price draws: median ${float(np.percentile(clearing,50)):.0f}/kg, "
          f"5–95% ${float(np.percentile(clearing,5)):.0f}–${float(np.percentile(clearing,95)):.0f}/kg")

    # Step 5: cost samples paired with revenue samples. Independent draws.
    # Resample if N_PRICE != N_COST. Here equal.
    npv_grid_rows = []
    wacc_set = [0.03, 0.087]
    lr_set = [0.0, 0.10, 0.15, 0.20]

    print("\nP(NPV ≥ 0) grid:")
    print(f"  {'arch':<22} {'WACC':>5} {'LR':>5} {'regime':<22} {'P(NPV≥0)':>10}")
    for arch, _ in ARCHS_AND_STACKS:
        fu = cost_results[arch.name]["first_unit"]
        rev = rev_per_mission[arch.name]
        for wacc in wacc_set:
            for lr in lr_set:
                # regime A: first-unit cost (no learning amortization in this round's cost MC;
                # learning is handled inside fleet_ramp_npv via wright_unit_cost given first_unit_cost).
                # So we pass first-unit cost into NPV; NPV's wright_unit_cost applies LR to fleet ramp.
                p_first_unit = prob_npv_positive(arch, fu, rev, wacc, lr)
                npv_grid_rows.append({
                    "arch": arch.name, "wacc": wacc, "lr": lr,
                    "regime": "bottoms_up_first_unit", "p_npv_pos": p_first_unit,
                })
                print(f"  {arch.name:<22} {wacc:>5.3f} {lr:>5.2f} {'bottoms_up_first_unit':<22} {p_first_unit:>10.4f}")

    # Also reproduce R8 baseline using placeholder cost = arch.first_unit_cost_M
    print("\nR8 placeholder baseline (sanity check vs round-8 published 51.1% / 42.8% etc.):")
    for arch, _ in ARCHS_AND_STACKS:
        rev = rev_per_mission[arch.name]
        fu_placeholder = np.full(N_PRICE_SAMPLES, arch.first_unit_cost_M)
        for wacc in [0.03, 0.087]:
            for lr in [0.15]:
                p = prob_npv_positive(arch, fu_placeholder, rev, wacc, lr)
                npv_grid_rows.append({
                    "arch": arch.name, "wacc": wacc, "lr": lr,
                    "regime": "r8_placeholder_constant", "p_npv_pos": p,
                })
                print(f"  {arch.name:<22} {wacc:>5.3f} {lr:>5.2f} {'r8_placeholder':<22} {p:>10.4f}")

    # ----- Hypothesis scoring -----
    p5_vb = float(np.percentile(cost_results["VariantB_500kWe"]["first_unit"], 5))
    p50_vb = float(np.percentile(cost_results["VariantB_500kWe"]["first_unit"], 50))
    p95_vb = float(np.percentile(cost_results["VariantB_500kWe"]["first_unit"], 95))
    p50_e500 = float(np.percentile(cost_results["E_500kWe_200t"]["first_unit"], 50))
    p5_e500 = float(np.percentile(cost_results["E_500kWe_200t"]["first_unit"], 5))
    p95_e500 = float(np.percentile(cost_results["E_500kWe_200t"]["first_unit"], 95))
    p50_e200 = float(np.percentile(cost_results["E_200kWe_100t"]["first_unit"], 50))

    rec_vb_p50 = p50_vb * factor_unit33_lr15
    rec_e500_p50 = p50_e500 * factor_unit33_lr15

    # P(NPV+) helpers
    def p_lookup(arch_name, wacc, lr, regime):
        for row in npv_grid_rows:
            if row["arch"] == arch_name and row["wacc"] == wacc and row["lr"] == lr and row["regime"] == regime:
                return row["p_npv_pos"]
        return None

    p_vb_sov_lr0_bu = p_lookup("VariantB_500kWe", 0.03, 0.0, "bottoms_up_first_unit")
    p_e500_sov_lr0_bu = p_lookup("E_500kWe_200t", 0.03, 0.0, "bottoms_up_first_unit")
    p_vb_sov_lr15_bu = p_lookup("VariantB_500kWe", 0.03, 0.15, "bottoms_up_first_unit")
    p_e500_sov_lr15_bu = p_lookup("E_500kWe_200t", 0.03, 0.15, "bottoms_up_first_unit")
    p_e200_sov_lr15_bu = p_lookup("E_200kWe_100t", 0.03, 0.15, "bottoms_up_first_unit")
    p_vb_sov_lr15_pl = p_lookup("VariantB_500kWe", 0.03, 0.15, "r8_placeholder_constant")
    p_e500_sov_lr15_pl = p_lookup("E_500kWe_200t", 0.03, 0.15, "r8_placeholder_constant")
    p_e200_sov_lr15_pl = p_lookup("E_200kWe_100t", 0.03, 0.15, "r8_placeholder_constant")

    scoring = []

    def score(hyp_id, predicted, measured, holds):
        scoring.append({
            "id": hyp_id, "predicted": predicted, "measured": measured,
            "verdict": "HELD" if holds else "FALSIFIED",
        })

    # H-bvc-a: Variant B median first unit in $0.9B–$1.6B
    score("H-bvc-a", "Variant B median first-unit $900M–$1600M",
          f"${p50_vb:.0f}M", 900.0 <= p50_vb <= 1600.0)
    # H-bvc-b: E_500 median first unit in $3.5B–$5.5B
    score("H-bvc-b", "Arch E_500 median first-unit $3500M–$5500M",
          f"${p50_e500:.0f}M", 3500.0 <= p50_e500 <= 5500.0)
    # H-bvc-c: E_200 median first unit in $1.8B–$2.8B
    score("H-bvc-c", "Arch E_200 median first-unit $1800M–$2800M",
          f"${p50_e200:.0f}M", 1800.0 <= p50_e200 <= 2800.0)
    # H-bvc-d: ratio E_500/B between 3.0× and 5.0×
    ratio_e500_vb = p50_e500 / p50_vb
    score("H-bvc-d", "Cost ratio E_500/VariantB 3.0×–5.0×",
          f"{ratio_e500_vb:.2f}×", 3.0 <= ratio_e500_vb <= 5.0)
    # H-bvc-e: reactor+PMAD+thrusters > 55% of E_500 first unit
    score("H-bvc-e", "Reactor+PMAD+thruster share > 55% of Arch E_500 first-unit",
          f"{big_three_first_unit_share*100:.1f}% (first-unit basis)",
          big_three_first_unit_share > 0.55)
    # H-bvc-f: spread (p95/p5) ≥ 3.5 for any arch
    spread_vb = p95_vb / p5_vb
    spread_e500 = p95_e500 / p5_e500
    max_spread = max(spread_vb, spread_e500)
    score("H-bvc-f", "Cost spread (95/5 percentile) ≥ 3.5× for at least one architecture",
          f"VariantB {spread_vb:.2f}×, E_500 {spread_e500:.2f}× (max {max_spread:.2f}×)",
          max_spread >= 3.5)
    # H-bvc-g: recurring Variant B in $400M–$700M
    score("H-bvc-g", "Variant B recurring unit (LR15 unit-33) $400M–$700M",
          f"${rec_vb_p50:.0f}M", 400.0 <= rec_vb_p50 <= 700.0)
    # H-bvc-h: recurring E_500 in $1.5B–$2.5B
    score("H-bvc-h", "Arch E_500 recurring unit (LR15 unit-33) $1500M–$2500M",
          f"${rec_e500_p50:.0f}M", 1500.0 <= rec_e500_p50 <= 2500.0)
    # H-bvc-i: bottoms-up Variant B P(NPV+) at sov 3%, no learning (LR 0 to bound worst-case): drops <20% vs placeholder
    # Compare bottoms-up LR=0 to placeholder LR=0.15 (the R8 published number).
    p_vb_sov_lr0_pl = p_lookup("VariantB_500kWe", 0.03, 0.15, "r8_placeholder_constant")
    score("H-bvc-i", f"P(NPV+) Variant B sov 3% bottoms-up no-learning < 20% (R8 placeholder LR15 was {p_vb_sov_lr15_pl*100:.1f}%)",
          f"{p_vb_sov_lr0_bu*100:.1f}%", p_vb_sov_lr0_bu < 0.20)
    # H-bvc-j: bottoms-up Arch E_500 P(NPV+) sov 3% no-learning < 5%
    score("H-bvc-j", "P(NPV+) Arch E_500 sov 3% bottoms-up no-learning < 5%",
          f"{p_e500_sov_lr0_bu*100:.1f}%", p_e500_sov_lr0_bu < 0.05)
    # H-bvc-k: Variant B P(NPV+) sov 3% LR15 bottoms-up in (35%, 60%) — recurring should be near placeholder
    score("H-bvc-k", "P(NPV+) Variant B sov 3% LR15 bottoms-up in (35%, 60%)",
          f"{p_vb_sov_lr15_bu*100:.1f}% (R8 placeholder was {p_vb_sov_lr15_pl*100:.1f}%)",
          0.35 < p_vb_sov_lr15_bu < 0.60)
    # H-bvc-l: strict-dominance survives across all (WACC, LR) under both regimes
    dominance_violations = []
    for wacc in wacc_set:
        for lr in lr_set:
            for regime in ["bottoms_up_first_unit", "r8_placeholder_constant"]:
                if regime == "r8_placeholder_constant" and lr != 0.15:
                    continue
                pvb = p_lookup("VariantB_500kWe", wacc, lr, regime)
                pe5 = p_lookup("E_500kWe_200t", wacc, lr, regime)
                pe2 = p_lookup("E_200kWe_100t", wacc, lr, regime)
                if pvb is None or pe5 is None or pe2 is None:
                    continue
                # Variant B should be ≥ each E variant
                if pe5 > pvb + 1e-9:
                    dominance_violations.append(f"E_500 > VB at wacc={wacc} lr={lr} regime={regime} ({pe5:.4f} vs {pvb:.4f})")
                if pe2 > pvb + 1e-9:
                    dominance_violations.append(f"E_200 > VB at wacc={wacc} lr={lr} regime={regime} ({pe2:.4f} vs {pvb:.4f})")
    score("H-bvc-l", "Variant B strict-dominance over Arch E variants on P(NPV+) across all WACC×LR",
          f"{len(dominance_violations)} violation(s): {dominance_violations[:3]}",
          len(dominance_violations) == 0)
    # H-bvc-m: corporate 8.7% bottoms-up: no arch ≥ 20% under any LR
    corp_max = 0.0
    for arch, _ in ARCHS_AND_STACKS:
        for lr in lr_set:
            p = p_lookup(arch.name, 0.087, lr, "bottoms_up_first_unit")
            if p is not None:
                corp_max = max(corp_max, p)
    score("H-bvc-m", "At corporate 8.7%, no architecture ≥ 20% P(NPV+) under any LR",
          f"max P(NPV+) across all arch/LR = {corp_max*100:.2f}%",
          corp_max < 0.20)
    # H-bvc-n: cost sub-linear in mass for E_500 vs E_200
    # E_500 mass ~6.8 t, E_200 mass ~3.6 t → mass ratio 1.89
    mass_ratio = 6.8 / 3.6
    cost_ratio = p50_e500 / p50_e200
    score("H-bvc-n", f"E_500/E_200 cost ratio < mass ratio ({mass_ratio:.2f})",
          f"cost ratio = {cost_ratio:.2f}", cost_ratio < mass_ratio)

    # ----- Write outputs -----
    # CSV: cost distributions summary
    import csv
    with (RESULTS_DIR / "cost_distributions.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["arch", "p5_M", "p50_M", "mean_M", "p95_M", "spread_95_over_5"])
        w.writeheader()
        for row in cost_summary_rows:
            w.writerow(row)

    # CSV: NPV grid
    with (RESULTS_DIR / "npv_prob_grid.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["arch", "wacc", "lr", "regime", "p_npv_pos"])
        w.writeheader()
        for row in npv_grid_rows:
            w.writerow(row)

    # JSON: downsampled cost arrays
    downsample = 500
    cost_json = {}
    for arch, _ in ARCHS_AND_STACKS:
        cost_json[arch.name] = {
            "first_unit": cost_results[arch.name]["first_unit"][::N_COST_SAMPLES // downsample].tolist(),
            "hardware_total": cost_results[arch.name]["hardware_total"][::N_COST_SAMPLES // downsample].tolist(),
        }
    (RESULTS_DIR / "cost_distributions.json").write_text(json.dumps(cost_json))

    # Markdown: hypothesis scoring
    lines = ["# R-bottoms-up-vehicle-cost — hypothesis scoring",
             "",
             "| ID | Predicted | Measured | Verdict |",
             "|---|---|---|---|"]
    for h in scoring:
        lines.append(f"| {h['id']} | {h['predicted']} | {h['measured']} | **{h['verdict']}** |")
    (RESULTS_DIR / "hypothesis_scoring.md").write_text("\n".join(lines) + "\n")

    held = sum(1 for h in scoring if h["verdict"] == "HELD")
    falsified = sum(1 for h in scoring if h["verdict"] == "FALSIFIED")
    print(f"\nScoring: {held} HELD, {falsified} FALSIFIED out of {len(scoring)}.")

    # Summary
    summary_lines = [
        "# R-bottoms-up-vehicle-cost — summary",
        "",
        "## First-unit cost distributions",
        "",
        "| Arch | 5%ile | median | mean | 95%ile | spread (95/5) | R7 placeholder | median / placeholder |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    arch_placeholders = {"VariantB_500kWe": 500.0, "E_500kWe_200t": 300.0, "E_200kWe_100t": 250.0}
    for row in cost_summary_rows:
        ph = arch_placeholders[row["arch"]]
        summary_lines.append(
            f"| {row['arch']} | ${row['p5_M']:.0f}M | ${row['p50_M']:.0f}M | ${row['mean_M']:.0f}M | "
            f"${row['p95_M']:.0f}M | {row['spread_95_over_5']:.2f}× | ${ph:.0f}M | {row['p50_M']/ph:.2f}× |"
        )
    summary_lines += [
        "",
        f"## Recurring unit cost (Wright LR 15%, unit 33; factor {factor_unit33_lr15:.3f})",
        "",
        "| Arch | recurring p50 | first-unit p50 | R7 placeholder | recurring vs placeholder |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in recurring_summary:
        ph = arch_placeholders[row["arch"]]
        fu = next(r for r in cost_summary_rows if r["arch"] == row["arch"])
        summary_lines.append(
            f"| {row['arch']} | ${row['recurring_p50_lr15_M']:.0f}M | ${fu['p50_M']:.0f}M | ${ph:.0f}M | "
            f"{row['recurring_p50_lr15_M']/ph:.2f}× |"
        )
    summary_lines += [
        "",
        "## P(NPV ≥ 0) at key cells",
        "",
        "| Arch | regime | WACC | LR | P(NPV+) |",
        "|---|---|---:|---:|---:|",
    ]
    key_cells = [
        ("VariantB_500kWe", "r8_placeholder_constant", 0.03, 0.15),
        ("VariantB_500kWe", "bottoms_up_first_unit", 0.03, 0.15),
        ("VariantB_500kWe", "bottoms_up_first_unit", 0.03, 0.0),
        ("VariantB_500kWe", "bottoms_up_first_unit", 0.087, 0.15),
        ("E_500kWe_200t",   "r8_placeholder_constant", 0.03, 0.15),
        ("E_500kWe_200t",   "bottoms_up_first_unit", 0.03, 0.15),
        ("E_500kWe_200t",   "bottoms_up_first_unit", 0.03, 0.0),
        ("E_500kWe_200t",   "bottoms_up_first_unit", 0.087, 0.15),
        ("E_200kWe_100t",   "r8_placeholder_constant", 0.03, 0.15),
        ("E_200kWe_100t",   "bottoms_up_first_unit", 0.03, 0.15),
    ]
    for arch_name, regime, wacc, lr in key_cells:
        p = p_lookup(arch_name, wacc, lr, regime)
        summary_lines.append(f"| {arch_name} | {regime} | {wacc:.3f} | {lr:.2f} | {p*100:.1f}% |")

    summary_lines += [
        "",
        f"## Scoring: {held} HELD / {falsified} FALSIFIED of {len(scoring)}",
        "",
        "See `hypothesis_scoring.md` for per-hypothesis verdicts.",
    ]
    (RESULTS_DIR / "summary.md").write_text("\n".join(summary_lines) + "\n")
    print(f"\nWrote {RESULTS_DIR}/{{cost_distributions.csv, npv_prob_grid.csv, cost_distributions.json, hypothesis_scoring.md, summary.md}}")


if __name__ == "__main__":
    main()
