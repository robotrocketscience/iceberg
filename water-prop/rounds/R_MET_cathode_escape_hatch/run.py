"""R-microwave-electrothermal-as-cathode-life-escape-hatch — does water microwave-
electrothermal beat water-radio-frequency-ion at Variant B when cathode-life penalty
for radio-frequency-ion is properly priced?

Expected lifetime delivered chunk:
  E[MET] = N * chunk * delivered_fraction_MET                    (deterministic)
  E[RFI] = N_completed * chunk * delivered_fraction_RFI'         (probabilistic)
       N_completed depends on failure mode (tug-loss vs mission-loss) and S swaps

Pre-registration: see STUDY.md (H-mealh-a through H-mealh-h).
"""

from __future__ import annotations

import json
import math
from pathlib import Path


# Delivered fractions from R-all-electric-thruster-sweep, Variant B matrix-impulsive,
# 1 megawatt-electric, chunk 200 t, canonical efficiency.
DELIVERED_FRAC = {
    "water_microwave_electrothermal": 0.356,
    "water_radio_frequency_ion":      0.704,
}

# Per-mission cathode-on time, hour (R-cathode-life-water-plasma Variant B canonical)
CATHODE_ON_HR_PER_MISSION = 5435.0

# Cathode-life anchors (hour per cathode)
LIFE_ANCHORS = {
    "optimistic_50000_hr":   50000.0,
    "mid_case_25000_hr":     25000.0,
    "pessimistic_3000_hr":    3000.0,
}

# Spare-cathode hardware mass (kilogram per slot, integrated)
PER_SLOT_KG = 50.0

# Sweep axes
N_MISSIONS_SWEEP = [1, 5, 10, 20]
PER_SWAP_FAILURE_P = [0.00, 0.01, 0.05, 0.10, 0.25]

# Chunk mass at Variant B reference cell (R-all-electric-thruster-sweep row), tonne
CHUNK_T = 200.0
# Tug dry without spares, tonne (R-electric-outbound at 1 MWe)
TUG_DRY_T = 12.1
# Inbound delta-velocity at Variant B matrix-impulsive, km/s
DV_INBOUND_KM_S = 6.42
# Radio-frequency-ion specific impulse, second
ISP_RFI_S = 2000.0
G0 = 9.80665


def swaps_needed(total_hr: float, life_hr: float) -> int:
    """Number of in-flight cathode swaps required.

    First cathode is the primary, no swap needed to activate it. So if total
    cathode-on time fits inside life_hr, S=0. Otherwise S = ceil(total/life) - 1.
    """
    if total_hr <= life_hr:
        return 0
    return int(math.ceil(total_hr / life_hr)) - 1


def rfi_chunk_with_spare_mass(n_cathodes: int) -> float:
    """Chunk delivered for radio-frequency-ion, accounting for spare-cathode dry-mass
    penalty.

    Tsiolkovsky at Variant B inbound delta-velocity:
        mass_ratio = exp(dv / (Isp * g0)) ≈ 1.39 at Isp 2000, dv 6.42 km/s
        m_prop / m_initial = 1 - 1/mass_ratio ≈ 0.281

    Adding (n_cathodes - 1) * 50 kg of spare-cathode dry mass to tug, the propellant
    requirement scales with initial mass, and the delivered chunk drops accordingly.
    The primary cathode is included in the base tug mass; (n_cathodes - 1) are spares.
    """
    v_e = ISP_RFI_S * G0
    mass_ratio = math.exp(DV_INBOUND_KM_S * 1000.0 / v_e)
    prop_frac = 1.0 - 1.0 / mass_ratio

    spares = max(0, n_cathodes - 1)
    spare_dry_kg = spares * PER_SLOT_KG
    spare_dry_t = spare_dry_kg / 1000.0

    tug_with_spares_t = TUG_DRY_T + spare_dry_t
    m_initial_t = tug_with_spares_t + CHUNK_T
    m_prop_t = m_initial_t * prop_frac
    delivered_t = CHUNK_T - m_prop_t
    return max(0.0, delivered_t) / CHUNK_T


def expected_lifetime_delivered(
    thruster: str,
    n_missions: int,
    life_hr: float,
    p_swap_fail: float,
    failure_mode: str,
) -> dict:
    """Expected total delivered chunk over n_missions for the given thruster, life
    anchor, per-swap failure probability, and failure-mode interpretation.

    Returns:
        dict with per-mission delivered fraction, swaps required, expected lifetime
        delivered fraction (sum over missions, dimensionless), and total delivered tonne.
    """
    total_hr = CATHODE_ON_HR_PER_MISSION * n_missions
    if thruster == "water_microwave_electrothermal":
        # No cathode, no swaps, no failure-probability term.
        frac_per_mission = DELIVERED_FRAC[thruster]
        e_lifetime_frac = n_missions * frac_per_mission
        e_lifetime_tonne = e_lifetime_frac * CHUNK_T
        return {
            "thruster": thruster,
            "n_missions": n_missions,
            "life_hr": life_hr,
            "p_swap_fail": p_swap_fail,
            "failure_mode": failure_mode,
            "swaps": 0,
            "n_cathodes": 0,
            "per_mission_delivered_frac": frac_per_mission,
            "expected_lifetime_delivered_frac": e_lifetime_frac,
            "expected_lifetime_delivered_t": e_lifetime_tonne,
        }
    # Radio-frequency-ion path.
    swaps = swaps_needed(total_hr, life_hr)
    n_cathodes = swaps + 1
    per_mission_frac = rfi_chunk_with_spare_mass(n_cathodes)

    if failure_mode == "mission_loss_per_failure":
        # Each successful swap occurs once across the mission profile. Treat swap
        # failures as Poisson-thinning: expected number of completed missions =
        # n_missions * (1 - p)^swaps. (A swap failure is assumed to lose one
        # mission's chunk and the tug then refurbishes; conservatively assume the
        # expected delivered fraction is reduced by (1 - p)^swaps. This is a
        # simplification of the true mission-by-mission tree but is reasonable
        # for the orders-of-magnitude scoping this round needs.)
        e_completion = (1.0 - p_swap_fail) ** swaps if swaps > 0 else 1.0
        e_lifetime_frac = n_missions * per_mission_frac * e_completion
    elif failure_mode == "tug_loss_per_failure":
        # Any swap failure loses all remaining missions. Expected lifetime
        # delivered fraction = sum over swap success at each step.
        e_completion = (1.0 - p_swap_fail) ** swaps if swaps > 0 else 1.0
        # All-or-nothing: tug completes all n_missions with prob e_completion,
        # otherwise expected proportion completed = (1 - (1-p)^swaps) * average
        # missions before failure. Simplify: take the all-or-nothing case.
        e_lifetime_frac = n_missions * per_mission_frac * e_completion
        # (Note: a more careful model would sum over the geometric distribution
        # of failure timing. For this round the simple all-or-nothing is the
        # conservative answer the orders-of-magnitude scoping wants.)
    else:
        raise ValueError(failure_mode)

    e_lifetime_tonne = e_lifetime_frac * CHUNK_T
    return {
        "thruster": thruster,
        "n_missions": n_missions,
        "life_hr": life_hr,
        "p_swap_fail": p_swap_fail,
        "failure_mode": failure_mode,
        "swaps": swaps,
        "n_cathodes": n_cathodes,
        "per_mission_delivered_frac": per_mission_frac,
        "expected_lifetime_delivered_frac": e_lifetime_frac,
        "expected_lifetime_delivered_t": e_lifetime_tonne,
    }


def find_crossover_p(n_missions: int, life_hr: float, failure_mode: str) -> float:
    """Find the per-swap failure probability at which radio-frequency-ion expected
    lifetime delivery equals microwave-electrothermal expected lifetime delivery.

    Bisection on p in [0, 0.99]. Returns the crossover (or 0.0 / 1.0 sentinel).
    """
    met = expected_lifetime_delivered(
        "water_microwave_electrothermal", n_missions, life_hr, 0.0, failure_mode
    )["expected_lifetime_delivered_frac"]

    def diff(p: float) -> float:
        rfi = expected_lifetime_delivered(
            "water_radio_frequency_ion", n_missions, life_hr, p, failure_mode
        )["expected_lifetime_delivered_frac"]
        return rfi - met

    # If radio-frequency-ion is already worse at p=0, the crossover is below 0.
    if diff(0.0) <= 0.0:
        return 0.0
    # If radio-frequency-ion is still better at p=0.99, no crossover under realistic p.
    if diff(0.99) >= 0.0:
        return 1.0
    lo, hi = 0.0, 0.99
    for _ in range(50):
        mid = (lo + hi) / 2.0
        d = diff(mid)
        if d > 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for life_name, life_hr in LIFE_ANCHORS.items():
        for n_missions in N_MISSIONS_SWEEP:
            for thruster in DELIVERED_FRAC:
                for p in PER_SWAP_FAILURE_P:
                    for failure_mode in ("mission_loss_per_failure", "tug_loss_per_failure"):
                        row = expected_lifetime_delivered(
                            thruster, n_missions, life_hr, p, failure_mode
                        )
                        row["life_anchor"] = life_name
                        results.append(row)

    crossovers = []
    for life_name, life_hr in LIFE_ANCHORS.items():
        for n_missions in N_MISSIONS_SWEEP:
            for failure_mode in ("mission_loss_per_failure", "tug_loss_per_failure"):
                p_crit = find_crossover_p(n_missions, life_hr, failure_mode)
                crossovers.append({
                    "life_anchor": life_name,
                    "life_hr": life_hr,
                    "n_missions": n_missions,
                    "failure_mode": failure_mode,
                    "p_crit": p_crit,
                })

    out = {
        "results": results,
        "crossovers": crossovers,
        "delivered_fraction_baseline": DELIVERED_FRAC,
        "per_mission_cathode_on_hr": CATHODE_ON_HR_PER_MISSION,
        "life_anchors": LIFE_ANCHORS,
    }
    (out_dir / "escape_hatch.json").write_text(json.dumps(out, indent=2))

    # tables.md
    lines = []
    lines.append("# R-microwave-electrothermal-as-cathode-life-escape-hatch — tables\n\n")

    lines.append("## Crossover per-swap failure probability (radio-frequency-ion ties microwave-electrothermal)\n\n")
    lines.append("| Life anchor | N missions | Failure mode | Swaps required | p_crit | At p_crit, microwave-electrothermal wins if real p > | At p_crit, radio-frequency-ion wins if real p < |\n")
    lines.append("|---|---:|---|---:|---:|:---|:---|\n")
    for c in crossovers:
        swaps = swaps_needed(CATHODE_ON_HR_PER_MISSION * c["n_missions"], c["life_hr"])
        p_label = f"{c['p_crit']:.4f}"
        if c["p_crit"] >= 1.0:
            p_label = "no crossover (radio-frequency-ion always wins)"
        elif c["p_crit"] <= 0.0:
            p_label = "0 (microwave-electrothermal already wins at p=0)"
        lines.append(
            f"| {c['life_anchor']} | {c['n_missions']} | {c['failure_mode']} | "
            f"{swaps} | {p_label} | microwave-electrothermal | radio-frequency-ion |\n"
        )

    lines.append("\n## Lifetime delivered chunk, mission-loss-per-failure model (Dawn-realistic)\n\n")
    lines.append("Per mission baseline: microwave-electrothermal 35.6% × 200 t = 71.2 t; radio-frequency-ion 70.4% × 200 t = 140.8 t (before spare-mass penalty)\n\n")
    lines.append("| Life anchor | N missions | Thruster | Swaps | p_swap | Per-mission % | Lifetime delivered (t) |\n")
    lines.append("|---|---:|---|---:|---:|---:|---:|\n")
    for r in results:
        if r["failure_mode"] != "mission_loss_per_failure":
            continue
        if r["n_missions"] not in (10,):
            continue
        if r["p_swap_fail"] not in (0.00, 0.01, 0.05, 0.10):
            continue
        lines.append(
            f"| {r['life_anchor']} | {r['n_missions']} | {r['thruster']} | "
            f"{r['swaps']} | {r['p_swap_fail']:.2f} | "
            f"{r['per_mission_delivered_frac']*100:.1f}% | "
            f"{r['expected_lifetime_delivered_t']:.1f} |\n"
        )

    lines.append("\n## Direct head-to-head at Wang pessimistic 3,000-hour life, 10-mission reuse, mission-loss model\n\n")
    lines.append("| p_swap | microwave-electrothermal lifetime (t) | radio-frequency-ion lifetime (t) | Verdict |\n")
    lines.append("|---:|---:|---:|:---|\n")
    for p in PER_SWAP_FAILURE_P:
        met = next(r for r in results if r["thruster"] == "water_microwave_electrothermal"
                    and r["n_missions"] == 10 and r["life_anchor"] == "pessimistic_3000_hr"
                    and r["p_swap_fail"] == p and r["failure_mode"] == "mission_loss_per_failure")
        rfi = next(r for r in results if r["thruster"] == "water_radio_frequency_ion"
                    and r["n_missions"] == 10 and r["life_anchor"] == "pessimistic_3000_hr"
                    and r["p_swap_fail"] == p and r["failure_mode"] == "mission_loss_per_failure")
        winner = "radio-frequency-ion" if rfi["expected_lifetime_delivered_t"] > met["expected_lifetime_delivered_t"] else "microwave-electrothermal"
        lines.append(
            f"| {p:.2f} | {met['expected_lifetime_delivered_t']:.1f} | "
            f"{rfi['expected_lifetime_delivered_t']:.1f} | {winner} |\n"
        )

    (out_dir / "tables.md").write_text("".join(lines))
    # Print summary
    summary_crossovers = [
        c for c in crossovers
        if c["n_missions"] == 10 and c["failure_mode"] == "mission_loss_per_failure"
    ]
    print(json.dumps({"crossovers_10_mission_realistic_failure_mode": summary_crossovers}, indent=2))


if __name__ == "__main__":
    main(Path(__file__).parent / "results")
