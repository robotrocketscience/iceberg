"""R-delivery-irr-curve — marginal internal-rate-of-return as a function of
per-ship chunk delivery, independent of rescue mechanism.

Reuses R-reactor-roadmap's cashflow model. The only modification is to
parameterize per-ship delivery for the at-or-above-500-kilowatt-electric cells.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
WATERPROP_ROUNDS = ROUND_DIR.parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Load R-reactor-roadmap module by file path (sibling round, not a package).
RRR_PATH = WATERPROP_ROUNDS / "R_reactor_roadmap" / "run.py"
spec = importlib.util.spec_from_file_location("rrr", RRR_PATH)
rrr = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(RRR_PATH.parent))
spec.loader.exec_module(rrr)


# Sweep grid: 100 to 2000 tonnes per ship; finer resolution near the predicted
# hurdle crossovers (180-250 for 4%, 420-520 for 8%, 630-750 for 10%).
DELIVERY_SWEEP_T = [
    100, 128.8, 150, 180, 200, 220, 240, 260,
    300, 400, 440, 460, 482, 500, 520,
    588, 640, 680, 700, 720, 750,
    800, 1000, 1200, 1500, 2000,
]

# Hurdle rates of interest.
HURDLES = {
    "sovereign_bond_4pct":     0.04,
    "regulated_utility_8pct":  0.08,
    "corporate_growth_10pct":  0.10,
}


def marginal_irr_at_delivery(delivery_t: float, cdf: dict) -> tuple[float, dict]:
    """Override the MARVL chunk-delivery table at 500-kilowatt-electric and
    1-megawatt-electric eras, recompute the conditional curve + marginal."""
    rrr.MARVL_CHUNK_DELIVERED_T["Chemical_kick_500kWe"] = float(delivery_t)
    rrr.MARVL_CHUNK_DELIVERED_T["MW_1000kWe"]           = float(delivery_t)
    curve = rrr.conditional_irr_curve(rrr.BEST_CELL, with_tv=True)
    marg = rrr.marginal_irr(curve, cdf)
    return marg["marginal_irr"], {
        "marginal_irr": marg["marginal_irr"],
        "p_never_branch": marg["p_never_branch"],
        "irr_never_branch": marg["irr_never_branch"],
        "irr_at_mw_year_8": curve["8"]["irr"],
        "irr_at_mw_year_20": curve["20"]["irr"],
    }


def interp_hurdle_crossover(rows: list[dict], hurdle: float) -> float | None:
    """Linear interpolation of delivery at which marginal_irr == hurdle.
    Returns None if the curve does not cross the hurdle within the sweep envelope.
    """
    for i in range(1, len(rows)):
        a, b = rows[i - 1], rows[i]
        if a["marginal_irr"] < hurdle <= b["marginal_irr"]:
            # Linear interpolation in (delivery_t, marginal_irr).
            x0, y0 = a["delivery_t"], a["marginal_irr"]
            x1, y1 = b["delivery_t"], b["marginal_irr"]
            if y1 == y0:
                return x0
            return x0 + (hurdle - y0) * (x1 - x0) / (y1 - y0)
    return None


def main() -> None:
    print("=" * 92)
    print("R-delivery-irr-curve — marginal internal-rate-of-return vs per-ship delivery")
    print("=" * 92)
    print()

    cdf = rrr.load_pbr_cdf()

    rows = []
    print(f"  {'delivery_t':>12} {'marginal_irr':>14} {'P(never)':>10} {'IRR_never':>12}")
    for d in DELIVERY_SWEEP_T:
        marg, detail = marginal_irr_at_delivery(d, cdf)
        rows.append({
            "delivery_t": d,
            **detail,
        })
        irr_never_str = (
            f"{detail['irr_never_branch'] * 100:.2f}%"
            if detail["irr_never_branch"] is not None else "n/a"
        )
        print(f"  {d:>12.1f} {marg * 100:>12.2f}%  {detail['p_never_branch'] * 100:>9.2f}% {irr_never_str:>12}")
    print()

    print("Hurdle crossover deliveries (linear interpolation between sweep points):")
    crossovers = {}
    for name, hurdle in HURDLES.items():
        x = interp_hurdle_crossover(rows, hurdle)
        crossovers[name] = x
        if x is None:
            print(f"  {name:<28} hurdle={hurdle * 100:.0f}% not reached in [{rows[0]['delivery_t']}, {rows[-1]['delivery_t']}] tonnes per ship")
        else:
            print(f"  {name:<28} hurdle={hurdle * 100:.0f}%  crossover ≈ {x:.1f} tonnes per ship")
    print()

    # Concavity check: differences between successive 500-tonne-spaced increments.
    print("Concavity check (H-dic-f): change in marginal internal-rate-of-return per +500 t increment")
    test_pts = [500, 1000, 1500, 2000]
    irrs = {d: next(r["marginal_irr"] for r in rows if r["delivery_t"] == d) for d in test_pts}
    diffs = [(test_pts[i], irrs[test_pts[i]] - irrs[test_pts[i - 1]]) for i in range(1, len(test_pts))]
    for d, diff in diffs:
        print(f"  +500 t -> {d} t: delta marginal_irr = {diff * 100:+.2f} percentage points")
    concave = all(diffs[i][1] < diffs[i - 1][1] for i in range(1, len(diffs)))
    print(f"  monotonically decreasing increments (concave)? {concave}")
    print()

    # Pre-registration grading.
    def find_irr(d_target: float) -> float | None:
        for r in rows:
            if r["delivery_t"] == d_target:
                return r["marginal_irr"]
        return None

    print("Pre-registration grading (H-dic):")

    def grade(name: str, measured, lo, hi):
        if measured is None:
            verdict = "n/a"
        elif lo <= measured <= hi:
            verdict = "HELD"
        else:
            verdict = "FALSIFIED"
        meas_str = f"{measured:.2f}" if measured is not None else "n/a"
        print(f"  {name:<10} measured={meas_str}  range=[{lo}, {hi}]  -> {verdict}")

    grade("H-dic-a", crossovers["sovereign_bond_4pct"], 180, 260)
    grade("H-dic-b", crossovers["regulated_utility_8pct"], 420, 520)
    grade("H-dic-c", crossovers["corporate_growth_10pct"], 630, 750)
    grade("H-dic-d", (find_irr(200) or 0) * 100, 3.0, 4.5)
    grade("H-dic-e", (find_irr(482) or 0) * 100, 7.5, 9.0)
    print(f"  H-dic-f   measured concave={concave}  expected=True  "
          f"-> {'HELD' if concave else 'FALSIFIED'}")
    grade("H-dic-g", (find_irr(588) or 0) * 100, 8.5, 10.2)

    # Persist.
    record = {
        "delivery_sweep_t": DELIVERY_SWEEP_T,
        "rows": rows,
        "hurdle_crossovers": crossovers,
        "concave_above_500t": concave,
    }
    out_path = RESULTS_DIR / "delivery_irr.json"
    with out_path.open("w") as f:
        json.dump(record, f, indent=2, default=str)
    print()
    print(f"Result JSON: {out_path}")


if __name__ == "__main__":
    main()
