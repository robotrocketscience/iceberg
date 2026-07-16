"""R-L0-10-relaxation-impact — does L0-09 charitable bind tighter than relaxed L0-10?

Cross-check three charitable readings of L0-09 against the rolling-5-launch block
form of L0-10 across the (launch_cadence, p) grid. Identify the (cadence, p)
frontier where all readings clear 0.95 and where rolling-5-L0-10 clears its
relaxed target.

Outputs:
    results/cadence_p_sweep.json
    results/coordinated_revision.json
    results/tables.md

Deterministic; runtime < 1 s.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from itertools import product


# ------------------------------- readings ------------------------------- #


def reading_a_slot_met(launch_cadence_per_yr: float, p: float,
                       contracted_rate_per_yr: float = 1.0) -> float:
    """Reading (a) — delivery-cadence-met: fraction of contracted slots met on schedule.

    At cadence c with per-mission p, expected deliveries per year = c × p. If
    contracted = 1 / yr, slot-met fraction = min(1, c × p / contracted_rate)."""
    rate = launch_cadence_per_yr * p
    return min(1.0, rate / contracted_rate_per_yr)


def reading_b_window_has_delivery(launch_cadence_per_yr: float, p: float) -> float:
    """Reading (b) — P(rolling 12-month window has >= 1 delivery), Poisson approximation."""
    rate = launch_cadence_per_yr * p
    return 1.0 - math.exp(-rate * 1.0)


def reading_c_queue_depth(launch_cadence_per_yr: float, p: float,
                          round_trip_yr: float = 14.0) -> float:
    """Reading (c) — steady-state successful-mission queue depth."""
    return launch_cadence_per_yr * p * round_trip_yr


# ------------------------------- L0-10 forms ------------------------------- #


def l0_10_block_5_score(p: float, threshold: float) -> float:
    """P(at least ceil(5*threshold) of 5 consecutive launches succeed | per-mission p).

    For threshold = 0.90, need >= 5 successes (i.e., all 5) → P = p^5.
    For threshold = 0.80, need >= 4 successes → P = p^5 + 5*p^4*(1-p).
    For threshold = 0.75, need >= 4 successes → same as 0.80 (since ceil(3.75) = 4).
    For threshold = 0.60, need >= 3 successes.
    """
    k_required = math.ceil(5 * threshold)
    total = 0.0
    for k in range(k_required, 6):
        # Binomial coefficient: C(5, k)
        coef = math.comb(5, k)
        total += coef * (p ** k) * ((1 - p) ** (5 - k))
    return total


# ------------------------------- sweep ------------------------------- #


def cadence_p_sweep() -> dict:
    cadences = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 12.0]
    p_values = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 0.99]

    grid = []
    for c, p in product(cadences, p_values):
        row = {
            "launch_cadence_per_yr": c,
            "per_mission_p": p,
            "annual_delivery_rate": c * p,
            "reading_a_slot_met": reading_a_slot_met(c, p),
            "reading_b_window_has_delivery": reading_b_window_has_delivery(c, p),
            "reading_c_queue_depth": reading_c_queue_depth(c, p),
            "l0_10_block5_p0p80_threshold": l0_10_block_5_score(p, 0.80),
            "l0_10_block5_p0p90_threshold": l0_10_block_5_score(p, 0.90),
            "l0_10_block5_p0p75_threshold": l0_10_block_5_score(p, 0.75),
        }
        # Convenience flags
        row["clears_reading_a_0p95"] = row["reading_a_slot_met"] >= 0.95
        row["clears_reading_b_0p95"] = row["reading_b_window_has_delivery"] >= 0.95
        row["clears_l0_10_block5_0p90"] = row["l0_10_block5_p0p90_threshold"] >= 0.95
        row["clears_l0_10_block5_0p80"] = row["l0_10_block5_p0p80_threshold"] >= 0.95
        grid.append(row)
    return {"grid": grid, "cadences": cadences, "p_values": p_values}


# ------------------------------- coordinated revision ------------------------------- #


def coordinated_revision() -> dict:
    """For each candidate L0-10 relaxation, find (cadence, p) pairs that satisfy
    all three L0-09 readings AT THE MATCHING RELAXED THRESHOLD and clear the
    rolling-5 form of relaxed L0-10."""
    candidates = []
    for relaxed_target in [0.75, 0.80, 0.85, 0.90]:
        # If L0-09 is also relaxed to the same target:
        cadences = [1.0, 2.0, 4.0]
        for c in cadences:
            # Find minimum p that clears all readings at relaxed_target:
            p_min = None
            for p_int in range(50, 100):
                p = p_int / 100.0
                ok_a = reading_a_slot_met(c, p) >= relaxed_target
                ok_b = reading_b_window_has_delivery(c, p) >= relaxed_target
                ok_l0_10 = l0_10_block_5_score(p, relaxed_target) >= 0.95
                if ok_a and ok_b and ok_l0_10:
                    p_min = p
                    break
            candidates.append({
                "relaxed_target": relaxed_target,
                "launch_cadence_per_yr": c,
                "minimum_p_required": p_min,
                "feasible": p_min is not None,
            })
    return {"candidates": candidates}


# ------------------------------- L0-10-only minima ------------------------------- #


def l0_10_only_minima() -> dict:
    """What is the minimum p that clears L0-10's rolling-5 block at >= 0.95 confidence
    for each per-mission threshold?"""
    out = {}
    for t in [0.75, 0.80, 0.85, 0.90]:
        for p_int in range(50, 100):
            p = p_int / 100.0
            if l0_10_block_5_score(p, t) >= 0.95:
                out[f"threshold_{t}"] = {"min_p": p, "block5_score_at_min_p": l0_10_block_5_score(p, t)}
                break
        else:
            out[f"threshold_{t}"] = {"min_p": None, "block5_score_at_min_p": None}
    return out


# ------------------------------- driver ------------------------------- #


def main():
    here = Path(__file__).parent
    out = here / "results"
    out.mkdir(exist_ok=True)

    sweep = cadence_p_sweep()
    rev = coordinated_revision()
    l0_only = l0_10_only_minima()

    (out / "cadence_p_sweep.json").write_text(json.dumps(sweep, indent=2))
    (out / "coordinated_revision.json").write_text(json.dumps(rev, indent=2))
    (out / "l0_10_only_minima.json").write_text(json.dumps(l0_only, indent=2))

    md = [
        "# R-L0-10-relaxation-impact — results tables",
        "",
        "## 1. L0-10 rolling-5-block minimum p",
        "",
        "L0-10 says success rate >= threshold across any rolling block of 5 launches. P(rolling-5-block clears) >= 0.95 requires minimum per-mission p as:",
        "",
        "| L0-10 threshold | Minimum per-mission p | P(block clears) at min p |",
        "|---|---|---|",
    ]
    for t, v in l0_only.items():
        threshold = t.replace("threshold_", "")
        md.append(f"| {threshold} | {v['min_p']:.2f} | {v['block5_score_at_min_p']:.4f} |")
    md += [
        "",
        "**Reading:** at L0-10's nominal threshold 0.90, the rolling-5-block clauses requires per-mission p ≥ {} for >= 0.95 confidence the block passes. Relaxed thresholds 0.80 and 0.75 share the same min p because both round up to 4-of-5 needed.".format(
            l0_only["threshold_0.9"]["min_p"]
        ),
        "",
        "## 2. Three L0-09 charitable readings × cadence × p",
        "",
        "**Reading (a) — slot-met fraction at 1 / yr contracted cadence.**",
        "**Reading (b) — P(rolling 12-month window has >= 1 delivery), Poisson.**",
        "**Reading (c) — steady-state queue depth (14-yr round-trip).**",
        "",
        "### Reading (a) — slot-met fraction (>= 0.95 to clear)",
        "",
        "| cadence \\ p | 0.50 | 0.70 | 0.80 | 0.90 | 0.95 | 0.99 |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in sweep["cadences"]:
        cells = []
        for p in [0.50, 0.70, 0.80, 0.90, 0.95, 0.99]:
            v = reading_a_slot_met(c, p)
            flag = "✓" if v >= 0.95 else " "
            cells.append(f"{v:.2f} {flag}")
        md.append(f"| {c:.1f} | " + " | ".join(cells) + " |")

    md += [
        "",
        "### Reading (b) — P(window has delivery) (>= 0.95 to clear)",
        "",
        "| cadence \\ p | 0.50 | 0.70 | 0.80 | 0.90 | 0.95 | 0.99 |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in sweep["cadences"]:
        cells = []
        for p in [0.50, 0.70, 0.80, 0.90, 0.95, 0.99]:
            v = reading_b_window_has_delivery(c, p)
            flag = "✓" if v >= 0.95 else " "
            cells.append(f"{v:.3f} {flag}")
        md.append(f"| {c:.1f} | " + " | ".join(cells) + " |")

    md += [
        "",
        "### Reading (c) — queue depth (>= 1.0 to clear; usually trivial)",
        "",
        "| cadence \\ p | 0.50 | 0.70 | 0.80 | 0.90 |",
        "|---|---|---|---|---|",
    ]
    for c in sweep["cadences"]:
        cells = []
        for p in [0.50, 0.70, 0.80, 0.90]:
            v = reading_c_queue_depth(c, p)
            flag = "✓" if v >= 1.0 else " "
            cells.append(f"{v:.1f} {flag}")
        md.append(f"| {c:.1f} | " + " | ".join(cells) + " |")

    md += [
        "",
        "## 3. Coordinated revision: minimum p that clears all readings at a relaxed target",
        "",
        "If L0-09 is *also* relaxed to the same target as L0-10 (matched coordinated revision), what minimum per-mission p satisfies (a) slot-met, (b) window-has-delivery at the relaxed threshold, AND (c) L0-10 rolling-5-block at >= 0.95 confidence?",
        "",
        "| Relaxed L0-09 = L0-10 target | Launch cadence (per yr) | Minimum p required | Feasible? |",
        "|---|---|---|---|",
    ]
    for cand in rev["candidates"]:
        p_str = f"{cand['minimum_p_required']:.2f}" if cand['feasible'] else "—"
        feas = "yes" if cand['feasible'] else "no"
        md.append(
            f"| {cand['relaxed_target']:.2f} | {cand['launch_cadence_per_yr']:.1f} | "
            f"{p_str} | {feas} |"
        )

    md += [
        "",
        "## 4. Headline cross-check",
        "",
        "At L0-07's launch-cadence floor of 1 / yr and per-mission p = 0.80 (the user's Option B/C target):",
        "",
    ]
    p_target = 0.80
    c_floor = 1.0
    md += [
        f"- Reading (a) slot-met fraction: {reading_a_slot_met(c_floor, p_target):.3f} (clears 0.80 target ? **{'yes' if reading_a_slot_met(c_floor, p_target) >= 0.80 else 'NO'}**; clears 0.95 ? **{'yes' if reading_a_slot_met(c_floor, p_target) >= 0.95 else 'NO'}**)",
        f"- Reading (b) window-has-delivery: {reading_b_window_has_delivery(c_floor, p_target):.3f} (clears 0.80 ? **{'yes' if reading_b_window_has_delivery(c_floor, p_target) >= 0.80 else 'NO'}**; clears 0.95 ? **{'yes' if reading_b_window_has_delivery(c_floor, p_target) >= 0.95 else 'NO'}**)",
        f"- Reading (c) queue depth: {reading_c_queue_depth(c_floor, p_target):.1f} (clears 1.0 ? yes)",
        f"- L0-10 block-5 at threshold 0.80: {l0_10_block_5_score(p_target, 0.80):.3f} (clears 0.95 ? **{'yes' if l0_10_block_5_score(p_target, 0.80) >= 0.95 else 'NO'}**)",
        "",
        "At L0-07 cadence and p = 0.80, reading (a) of L0-09 fails — only 80 % of yearly slots met, well below 0.95 — but it does clear a *relaxed* L0-09 target at 0.80. Reading (b) fails badly (0.551 << 0.95). Reading (c) is trivially satisfied. L0-10 block-5 at threshold 0.80 also fails (0.737 << 0.95), meaning the per-mission p that clears the rolling-5 form of L0-10 = 0.80 is much higher than 0.80 itself.",
    ]

    (out / "tables.md").write_text("\n".join(md))
    print((out / "tables.md").read_text())


if __name__ == "__main__":
    main()
