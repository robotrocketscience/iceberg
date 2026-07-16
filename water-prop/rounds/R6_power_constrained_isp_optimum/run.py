"""R6 -- Power-constrained specific-impulse optimization for ICEBERG.

Question. The R3i analysis concluded that dual-ion at 1 kilovolt grid voltage
delivers 97 percent of the chunk at 275 kWe electrical power. But 275 kWe is
not a realistic power level for any flight program in the next 20 years.
Inverting the framing: given REALISTIC power levels (Kilopower at 10 kWe,
Fission Surface Power at 40 kWe, sub-megawatt at 100 kWe), what is the
power-optimal specific impulse and the maximum achievable chunk-delivery
fraction?

Method. Closed-form solution to the joint energy balance and Tsiolkovsky
constraint. For fixed (power, cruise time, duty cycle, total efficiency,
initial chunk mass, delta-V), solve numerically for the v_e (and therefore
specific impulse) that exactly satisfies the energy budget. The
corresponding delivered mass is m_initial * exp(-delta_v / v_e).

This is the classical NEP "power-optimal Isp" analysis (Jahn, Stuhlinger,
Edelbaum). See src/waterprop/propulsion/nep_optimum.py.

Inputs (ICEBERG nominal, with R2's revised delta-V):
  - delta-V = 5.2 km/s (revised from 4.2 km/s after R2 found the lunar
    gravity-assist tour delivers ~2 km/s, not the conops' assumed 3 km/s)
  - cruise time = 7 yr at 50 percent duty cycle = 1.1e8 effective burn seconds
  - efficiency = 0.4 (typical for water-class electric thrusters)
  - chunk mass m_initial = 5, 50, 200, 500 tons (CHUNK-MASS-RANGE sweep)
  - power = 5, 10, 40, 100, 200, 500, 1000 kWe

Output: tables of (m_initial, power) -> (power-optimal Isp, chunk delivery)
plus comparison plot vs the candidate technology Isp ceilings.

Run:
    uv run python rounds/R6_power_constrained_isp_optimum/run.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from waterprop.propulsion import power_optimal_isp

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ICEBERG mission constants (revised after R2)
DELTA_V_M_S = 5200.0
CRUISE_TIME_S = 7.0 * 365.25 * 86400.0     # 7 years
DUTY_CYCLE = 0.5
EFFICIENCY_TOTAL = 0.4

# Chunk masses spanning the trade range (per docs/CHUNK-MASS-RANGE.md)
CHUNK_MASSES_KG = [5_000, 50_000, 200_000, 500_000]
CHUNK_LABELS = ["5 t (small)", "50 t (Kilopower era)",
                "200 t (Fission Surface Power era)", "500 t (megawatt era)"]

# Power classes covering Kilopower through megawatt
POWER_LEVELS_KW = [5, 10, 20, 40, 70, 100, 200, 500, 1000]


def main() -> None:
    print("R6 -- Power-constrained specific-impulse optimization")
    print("=" * 70)
    print(f"Inputs:")
    print(f"  delta-V (km/s):  {DELTA_V_M_S / 1000.0}")
    print(f"  cruise time:     {CRUISE_TIME_S / 86400.0 / 365.25:.1f} yr")
    print(f"  duty cycle:      {DUTY_CYCLE}")
    print(f"  total efficiency: {EFFICIENCY_TOTAL}")
    print()

    rows = []
    for m_kg, label in zip(CHUNK_MASSES_KG, CHUNK_LABELS):
        print(f"\n=== Chunk mass: {m_kg/1000.0:.0f} t -- {label} ===")
        print(f"{'Power (kWe)':<14}"
              f"{'Optimal Isp (s)':<18}"
              f"{'Delivered (t)':<16}"
              f"{'Delivery (%)':<14}")
        for kw in POWER_LEVELS_KW:
            r = power_optimal_isp(
                power_W=kw * 1000.0,
                cruise_time_s=CRUISE_TIME_S,
                duty_cycle=DUTY_CYCLE,
                efficiency_total=EFFICIENCY_TOTAL,
                m_initial_kg=m_kg,
                delta_v_m_s=DELTA_V_M_S,
            )
            isp = r["isp_s"]
            m_del_t = r["m_delivered_kg"] / 1000.0
            frac = r["delivery_fraction"]
            if np.isnan(isp):
                isp_str = "n/a (infeasible)"
                m_del_str = "n/a"
                frac_str = "n/a"
            else:
                isp_str = f"{isp:>10.0f}"
                m_del_str = f"{m_del_t:>10.2f}"
                frac_str = f"{frac*100:>10.1f} %"
            print(f"{kw:>10.0f}     "
                  f"{isp_str}      "
                  f"{m_del_str}      "
                  f"{frac_str}")
            rows.append({
                "chunk_mass_t": m_kg / 1000.0,
                "power_kWe": kw,
                "power_optimal_isp_s": isp if not np.isnan(isp) else None,
                "delivered_mass_t": m_del_t if not np.isnan(m_del_t) else None,
                "delivery_fraction_pct": frac * 100 if not np.isnan(frac) else None,
            })

    # CSV
    csv_path = RESULTS_DIR / "power_constrained_optimum_sweep.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\nCSV written: {csv_path}")

    # Plot: optimal Isp vs power, one line per chunk mass
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    for m_kg, label in zip(CHUNK_MASSES_KG, CHUNK_LABELS):
        isps = []
        for kw in POWER_LEVELS_KW:
            r = power_optimal_isp(
                power_W=kw * 1000.0,
                cruise_time_s=CRUISE_TIME_S,
                duty_cycle=DUTY_CYCLE,
                efficiency_total=EFFICIENCY_TOTAL,
                m_initial_kg=m_kg,
                delta_v_m_s=DELTA_V_M_S,
            )
            isps.append(r["isp_s"])
        ax.loglog(POWER_LEVELS_KW, isps, "o-", lw=2, label=label)

    # Candidate tech Isp markers
    ax.axhline(600, color="C2", ls=":", alpha=0.5)
    ax.text(800, 600, "MET (R0)", color="C2", fontsize=8, ha="right")
    ax.axhline(2000, color="C1", ls=":", alpha=0.5)
    ax.text(800, 2000, "Pale Blue water ion (R1)", color="C1", fontsize=8, ha="right")
    ax.axhline(310, color="C3", ls=":", alpha=0.5)
    ax.text(800, 310, "HYDROS (R1)", color="C3", fontsize=8, ha="right")
    ax.set_xlabel("Available electrical power (kWe)")
    ax.set_ylabel("Power-optimal specific impulse (s)")
    ax.set_title(f"Optimal Isp vs power, delta-V = {DELTA_V_M_S/1000.0} km/s")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3, which="both")

    # Right panel: delivered mass vs power
    ax = axes[1]
    for m_kg, label in zip(CHUNK_MASSES_KG, CHUNK_LABELS):
        deliveries = []
        for kw in POWER_LEVELS_KW:
            r = power_optimal_isp(
                power_W=kw * 1000.0,
                cruise_time_s=CRUISE_TIME_S,
                duty_cycle=DUTY_CYCLE,
                efficiency_total=EFFICIENCY_TOTAL,
                m_initial_kg=m_kg,
                delta_v_m_s=DELTA_V_M_S,
            )
            deliveries.append(r["m_delivered_kg"] / 1000.0)
        ax.semilogx(POWER_LEVELS_KW, deliveries, "o-", lw=2, label=label)

    ax.set_xlabel("Available electrical power (kWe)")
    ax.set_ylabel("Delivered chunk mass (t)")
    ax.set_title("Delivered mass vs power")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3, which="both")

    # Mark power-class regimes
    for ax in axes:
        ax.axvspan(1, 10, alpha=0.06, color="green")
        ax.axvspan(10, 40, alpha=0.06, color="blue")
        ax.axvspan(40, 200, alpha=0.06, color="orange")
        ax.axvspan(200, 1000, alpha=0.06, color="red")

    fig.suptitle("R6: Power-constrained NEP optimization for ICEBERG (delta-V = 5.2 km/s)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    png_path = RESULTS_DIR / "power_constrained_optimum.png"
    fig.savefig(png_path, dpi=150)
    plt.close(fig)
    print(f"Plot written: {png_path}")

    # Headline findings
    print("\n--- KEY FINDINGS ---")
    print("For a 50-ton chunk at delta-V = 5.2 km/s, 7-year cruise at 50% duty:")
    for kw, label in [(10, "Kilopower"), (40, "Fission Surface Power"),
                       (100, "Sub-megawatt"), (1000, "Megawatt-class roadmap")]:
        r = power_optimal_isp(
            power_W=kw * 1000.0,
            cruise_time_s=CRUISE_TIME_S,
            duty_cycle=DUTY_CYCLE,
            efficiency_total=EFFICIENCY_TOTAL,
            m_initial_kg=50_000.0,
            delta_v_m_s=DELTA_V_M_S,
        )
        if np.isnan(r["isp_s"]):
            print(f"  {kw:>4} kWe ({label}): infeasible (insufficient energy)")
        else:
            print(f"  {kw:>4} kWe ({label}):  optimal Isp = {r['isp_s']:>5.0f} s,  "
                  f"delivered = {r['m_delivered_kg']/1000.0:>5.1f} t ({r['delivery_fraction']*100:>4.1f} %)")


if __name__ == "__main__":
    main()
