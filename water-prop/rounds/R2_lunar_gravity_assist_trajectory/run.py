"""R2 -- Lunar gravity assist trajectory analysis.

Question. The conops claims a 3-flyby lunar gravity assist tour delivers
about 3 km/s of arrival velocity reduction at zero propellant cost. Risk
B01 is that this might not hold across the lunar nodal regression cycle.
What is the actual distribution of delivered braking velocity across
(arrival velocity at infinity) and (lunar geometry inclination)?

Method. Patched-conic two-body model from
src/waterprop/trajectory/lunar_flyby.py. For each combination of:
  - arrival v_inf relative to Earth: 4 to 8 km/s
  - lunar flyby periapsis altitude: 100 to 5000 km
  - relative inclination between trajectory plane and Moon orbital plane:
    0 to 30 degrees (covers the lunar nodal cycle range)
compute the total braking velocity from three sequential maximum-braking
flybys and the per-flyby breakdown.

Outputs. Tables and plots in results/.

Run:
    uv run python rounds/R2_lunar_gravity_assist_trajectory/run.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from waterprop.trajectory import three_flyby_tour, single_flyby_braking

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def main() -> None:
    print("R2 -- Lunar gravity assist trajectory analysis")
    print("=" * 60)

    # Primary sweep: ICEBERG nominal arrival case.
    v_inf_arrival_km_s = 6.0
    periapsis_altitudes_km = [100.0, 500.0, 1000.0, 2000.0, 5000.0]
    inclinations_deg = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]

    print(f"\nNominal ICEBERG inbound v_inf at Earth: {v_inf_arrival_km_s} km/s")
    print(f"Sweep: periapsis altitudes (km) = {periapsis_altitudes_km}")
    print(f"Sweep: trajectory-Moon inclinations (deg) = {inclinations_deg}")
    print()

    # ---- Per-flyby Delta-V at v_inf = 6 km/s, varying altitude and inclination ----
    print("Single-flyby Delta-V (Earth frame, km/s) at v_inf = 6 km/s")
    print(f"{'altitude (km)':<15}", end="")
    for incl in inclinations_deg:
        print(f"i={incl:>4.0f}deg ", end="")
    print()
    for alt in periapsis_altitudes_km:
        print(f"{alt:>10.0f}     ", end="")
        for incl in inclinations_deg:
            _, dv = single_flyby_braking(v_inf_arrival_km_s, alt, incl)
            print(f"{dv:>8.3f}   ", end="")
        print()

    # ---- 3-flyby tour total Delta-V vs inclination at fixed altitude ----
    print("\nThree-flyby tour: total braking Delta-V (km/s) at periapsis altitude 100 km")
    print(f"{'v_inf (km/s)':<14}", end="")
    for incl in inclinations_deg:
        print(f"i={incl:>4.0f}deg ", end="")
    print()
    v_inf_sweep = [4.0, 5.0, 6.0, 7.0, 8.0]
    rows = []
    for v_inf in v_inf_sweep:
        print(f"{v_inf:>10.1f}     ", end="")
        for incl in inclinations_deg:
            tour = three_flyby_tour(v_inf, 100.0, incl)
            print(f"{tour['total_delta_v_km_s']:>8.3f}   ", end="")
            rows.append({
                "v_inf_initial_km_s": v_inf,
                "periapsis_altitude_km": 100.0,
                "inclination_deg": incl,
                "total_delta_v_km_s": tour["total_delta_v_km_s"],
                "v_inf_final_km_s": tour["v_inf_final_km_s"],
                "flyby_1_dv_km_s": tour["per_flyby"][0]["delta_v_km_s"],
                "flyby_2_dv_km_s": tour["per_flyby"][1]["delta_v_km_s"],
                "flyby_3_dv_km_s": tour["per_flyby"][2]["delta_v_km_s"],
            })
        print()

    # ---- Write CSV ----
    csv_path = RESULTS_DIR / "three_flyby_tour_sweep.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nCSV written: {csv_path}")

    # ---- Plot: total Delta-V vs inclination for several v_inf cases ----
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    for v_inf in v_inf_sweep:
        totals = []
        for incl in inclinations_deg:
            t = three_flyby_tour(v_inf, 100.0, incl)
            totals.append(t["total_delta_v_km_s"])
        ax.plot(inclinations_deg, totals, "o-", label=f"v_inf = {v_inf:.0f} km/s", lw=2)
    ax.axhline(3.0, color="k", ls="--", alpha=0.6, label="Conops claim: 3 km/s")
    ax.set_xlabel("Trajectory-Moon inclination (deg)")
    ax.set_ylabel("Total braking Delta-V from 3 flybys (km/s)")
    ax.set_title("Three-flyby tour at periapsis altitude 100 km")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # Right panel: per-flyby decomposition at v_inf = 6 km/s, varying inclination
    ax = axes[1]
    flyby1, flyby2, flyby3 = [], [], []
    for incl in inclinations_deg:
        t = three_flyby_tour(6.0, 100.0, incl)
        flyby1.append(t["per_flyby"][0]["delta_v_km_s"])
        flyby2.append(t["per_flyby"][1]["delta_v_km_s"])
        flyby3.append(t["per_flyby"][2]["delta_v_km_s"])
    width = 1.5
    x = np.array(inclinations_deg, dtype=float)
    ax.bar(x - width, flyby1, width=width, label="Flyby 1", color="C0")
    ax.bar(x, flyby2, width=width, label="Flyby 2", color="C1")
    ax.bar(x + width, flyby3, width=width, label="Flyby 3", color="C2")
    ax.set_xlabel("Trajectory-Moon inclination (deg)")
    ax.set_ylabel("Per-flyby Delta-V (km/s)")
    ax.set_title("Per-flyby decomposition at v_inf = 6 km/s")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("Lunar gravity assist tour: braking Delta-V across geometry",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    plot_path = RESULTS_DIR / "lunar_gravity_assist_sweep.png"
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)
    print(f"Plot written: {plot_path}")

    # ---- Headline findings ----
    print("\n--- KEY FINDINGS ---")
    tour_best = three_flyby_tour(6.0, 100.0, 0.0)
    tour_worst = three_flyby_tour(6.0, 100.0, 30.0)
    print(f"Best-case 3-flyby tour (v_inf=6 km/s, incl=0): "
          f"{tour_best['total_delta_v_km_s']:.3f} km/s")
    print(f"Worst-case 3-flyby tour (v_inf=6 km/s, incl=30): "
          f"{tour_worst['total_delta_v_km_s']:.3f} km/s")
    print(f"Conops claim: 3.0 km/s")


if __name__ == "__main__":
    main()
