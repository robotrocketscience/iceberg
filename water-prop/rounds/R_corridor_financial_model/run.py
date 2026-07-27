"""R-corridor-financial-model — Tier-1 breakeven over the corridor surface.

See STUDY.md. Writes results/breakeven_table.json.
Run: water-prop/.venv/bin/python water-prop/rounds/R_corridor_financial_model/run.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CELLS = {
    "32t_cell": {"delivered_kg": 31_700.0, "lift_kg": 875_000.0, "t_del": 21.1},
    "88t_cell": {"delivered_kg": 87_800.0, "lift_kg": 1_140_000.0, "t_del": 18.7},
}
LAUNCH_USD_PER_KG = {"FH_3000": 3000.0, "SS_early_500": 500.0, "SS_mature_100": 100.0}
VEHICLE_MARGINAL = {"veh_0.5B": 0.5e9, "veh_1.0B": 1.0e9}
OPS_PER_YR = 40e6
RATES = {"corporate_8.7": 0.087, "sovereign_3.0": 0.03, "undiscounted_0": 0.0}
PRICES = {"era100t_5025": 5025.0, "era1000t_2225": 2225.0, "era10000t_505": 505.0,
          "captive_10k": 10_000.0, "captive_25k": 25_000.0}
DECAY = 0.13

def breakeven(cell, launch, veh, r):
    c = CELLS[cell]
    cost0 = LAUNCH_USD_PER_KG[launch] * c["lift_kg"] + VEHICLE_MARGINAL[veh] + OPS_PER_YR * c["t_del"]
    # compound spend (approx all at t=1) to delivery date
    fv = cost0 * (1 + r) ** (c["t_del"] - 1.0)
    return fv / c["delivered_kg"]

def main():
    out = {"breakeven_usd_per_kg": {}, "price_comparators": PRICES,
           "decayed_prices_at_delivery": {}}
    for cell in CELLS:
        for launch in LAUNCH_USD_PER_KG:
            for veh in VEHICLE_MARGINAL:
                for rn, r in RATES.items():
                    k = f"{cell}|{launch}|{veh}|{rn}"
                    out["breakeven_usd_per_kg"][k] = round(breakeven(cell, launch, veh, r))
    for cell in CELLS:
        t = CELLS[cell]["t_del"]
        out["decayed_prices_at_delivery"][cell] = {
            p: round(v * (1 - DECAY) ** t) for p, v in PRICES.items()}
    best = min((v, k) for k, v in out["breakeven_usd_per_kg"].items())
    worst_rel = best[0] / PRICES["era100t_5025"]
    out["summary"] = {
        "cheapest_breakeven": {"case": best[1], "usd_per_kg": best[0]},
        "cheapest_vs_top_defensible_band": round(worst_rel, 1),
    }
    print(json.dumps(out["summary"], indent=1))
    for k, v in sorted(out["breakeven_usd_per_kg"].items(), key=lambda kv: kv[1])[:6]:
        print(f"  {k}: ${v:,}/kg")
    print("decayed prices at delivery:", out["decayed_prices_at_delivery"])
    with open(HERE / "results" / "breakeven_table.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/breakeven_table.json")

if __name__ == "__main__":
    main()
