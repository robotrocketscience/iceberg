"""R3i -- Dual-ion architecture: hydrogen-ion plus oxygen-ion from water
electrolysis.

Question. If we electrolyze water on board and accelerate both the
hydrogen and the oxygen as separate gridded-ion thruster beams at the same
grid voltage, what is the mass-weighted specific impulse, the electrical
power required for ICEBERG-class thrust, and the chunk-delivery fraction?
How does this compare to single-technology water-prop options
(microwave electrothermal, water radio-frequency ion, hydrogen-ion alone)?

Method. Closed-form ion-kinematics from
src/waterprop/propulsion/dual_ion.py. Sweep grid voltage from 100 volts
to 10 kilovolts. Compute per-species exhaust velocity, mass-weighted
specific impulse, thrust per kilowatt electrical, and chunk-delivery
fraction at the ICEBERG inbound-leg delta-V (4.2 kilometers per second).

What this captures.
  - Mass-weighted specific impulse: thrust = sum(m_dot_i * v_e_i), so
    Isp_avg = (f_H * v_H + f_O * v_O) / g0.
  - Energy bookkeeping: jet power per kilogram of water consumed.
  - Tsiolkovsky-equation chunk delivery for a chunk-fed propulsion leg.

What this does NOT capture.
  - Grid life under oxygen-ion erosion. Pure oxygen-ion at acceleration
    voltages of 1 kilovolt-plus is the most chemically aggressive ion
    thruster propellant possible from common substances. Grid lifetime
    is the dominant uncertainty for this architecture; flagged in
    STUDY.md.
  - Electron-neutralizer cathode operation in an oxidizing environment.
  - Mass overhead of two thruster systems plus electrolyzer.
  - Beam divergence and other geometrical efficiency factors beyond a
    scalar efficiency_total parameter.

Run:
    uv run python rounds/R3i_dual_ion_architecture/run.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from waterprop.propulsion import (
    dual_ion_isp_s,
    dual_ion_thrust_per_kw,
    delivery_fraction_chunk_fed,
)

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

ICEBERG_DELTA_V_KM_S = 4.2          # inbound leg
ICEBERG_THRUST_TARGET_N = 1.5       # nominal from round 0 analysis


def main() -> None:
    print("R3i -- Dual-ion architecture (hydrogen-ion + oxygen-ion from electrolyzed water)")
    print("=" * 80)

    voltages = np.array([100, 300, 1000, 3000, 10000], dtype=float)

    # Sweep both options: H+ (atomic hydrogen ions, theoretical maximum) and
    # H2+ (diatomic, more realistic at low ionization-fraction operating
    # points where H2 is not fully dissociated).
    for use_h2_plus, label in [(False, "atomic hydrogen ion (H+)"),
                               (True, "diatomic hydrogen ion (H2+)")]:
        print(f"\n=== {label} as the hydrogen species ===")
        print(f"{'Grid voltage (V)':<18}"
              f"{'Isp_H (s)':<12}"
              f"{'Isp_O (s)':<12}"
              f"{'Isp_avg (s)':<14}"
              f"{'Thrust per kW (mN)':<22}"
              f"{'kW for 1.5 N':<14}"
              f"{'Chunk delivery':<14}")
        rows = []
        for V in voltages:
            r = dual_ion_thrust_per_kw(grid_voltage_V=V,
                                        efficiency_total=0.4,
                                        use_h2_plus=use_h2_plus)
            isp = r["isp_avg_s"]
            thrust_per_kw = r["thrust_per_kw_electrical_N"]
            kw_for_target = ICEBERG_THRUST_TARGET_N / thrust_per_kw
            delivery = delivery_fraction_chunk_fed(isp, ICEBERG_DELTA_V_KM_S)
            print(f"{V:>12.0f}     "
                  f"{r['isp_H_s']:>9.0f}   "
                  f"{r['isp_O_s']:>9.0f}   "
                  f"{isp:>11.0f}   "
                  f"{thrust_per_kw * 1000:>18.2f}   "
                  f"{kw_for_target:>10.1f}   "
                  f"{delivery * 100:>10.1f} %")
            rows.append({
                "grid_voltage_V": V,
                "hydrogen_species": "H+" if not use_h2_plus else "H2+",
                "isp_H_s": r["isp_H_s"],
                "isp_O_s": r["isp_O_s"],
                "isp_avg_s": isp,
                "thrust_per_kw_mN": thrust_per_kw * 1000,
                "electrical_kw_for_1p5_N": kw_for_target,
                "chunk_delivery_fraction": delivery,
            })

        # Write CSV
        suffix = "h2_plus" if use_h2_plus else "h_plus"
        csv_path = RESULTS_DIR / f"dual_ion_sweep_{suffix}.csv"
        with csv_path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"  CSV: {csv_path}")

    # -------- Comparison plot with single-tech options --------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: specific impulse vs grid voltage, both hydrogen species
    voltages_fine = np.geomspace(100, 10000, 50)
    isp_h_plus = []
    isp_h2_plus = []
    for V in voltages_fine:
        r1 = dual_ion_isp_s(V, use_h2_plus=False)
        r2 = dual_ion_isp_s(V, use_h2_plus=True)
        isp_h_plus.append(r1["isp_avg_s"])
        isp_h2_plus.append(r2["isp_avg_s"])

    ax = axes[0]
    ax.loglog(voltages_fine, isp_h_plus, "-", lw=2, color="C0",
              label="Dual-ion (H+ + O+)")
    ax.loglog(voltages_fine, isp_h2_plus, "--", lw=2, color="C0",
              label="Dual-ion (H2+ + O+)", alpha=0.7)
    # Reference Isp lines for other water-prop options
    ax.axhline(600, color="C2", ls=":", alpha=0.7, label="MET realistic (R0): 600 s")
    ax.axhline(2000, color="C1", ls=":", alpha=0.7, label="Pale Blue water ion (R1): 2000 s")
    ax.axhline(310, color="C3", ls=":", alpha=0.7, label="Tethers HYDROS (R1): 310 s")
    ax.set_xlabel("Grid voltage (V)")
    ax.set_ylabel("Mass-weighted specific impulse (s)")
    ax.set_title("Dual-ion specific impulse vs grid voltage")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3, which="both")

    # Right: chunk delivery fraction vs grid voltage for both species choices
    delivery_h_plus = [delivery_fraction_chunk_fed(i, ICEBERG_DELTA_V_KM_S) for i in isp_h_plus]
    delivery_h2_plus = [delivery_fraction_chunk_fed(i, ICEBERG_DELTA_V_KM_S) for i in isp_h2_plus]

    ax = axes[1]
    ax.semilogx(voltages_fine, np.array(delivery_h_plus) * 100, "-", lw=2,
                color="C0", label="Dual-ion (H+ + O+)")
    ax.semilogx(voltages_fine, np.array(delivery_h2_plus) * 100, "--", lw=2,
                color="C0", label="Dual-ion (H2+ + O+)", alpha=0.7)
    # Reference delivery fractions
    delivery_met = delivery_fraction_chunk_fed(600, ICEBERG_DELTA_V_KM_S) * 100
    delivery_pb = delivery_fraction_chunk_fed(2000, ICEBERG_DELTA_V_KM_S) * 100
    delivery_hyd = delivery_fraction_chunk_fed(310, ICEBERG_DELTA_V_KM_S) * 100
    ax.axhline(delivery_met, color="C2", ls=":", alpha=0.7,
               label=f"MET realistic: {delivery_met:.0f} %")
    ax.axhline(delivery_pb, color="C1", ls=":", alpha=0.7,
               label=f"Pale Blue: {delivery_pb:.0f} %")
    ax.axhline(delivery_hyd, color="C3", ls=":", alpha=0.7,
               label=f"HYDROS: {delivery_hyd:.0f} %")
    ax.set_xlabel("Grid voltage (V)")
    ax.set_ylabel("Chunk-fed delivery fraction (%)")
    ax.set_title(f"Delivery fraction at delta-V = {ICEBERG_DELTA_V_KM_S} km/s")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_ylim([40, 102])
    ax.grid(alpha=0.3, which="both")

    fig.suptitle("R3i: Dual-ion architecture compared with single-tech water options",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    plot_path = RESULTS_DIR / "dual_ion_comparison.png"
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)
    print(f"\nPlot written: {plot_path}")

    # -------- Headline findings --------
    print("\n--- KEY FINDINGS ---")
    r_1kV = dual_ion_thrust_per_kw(grid_voltage_V=1000.0, use_h2_plus=False)
    delivery_1kV = delivery_fraction_chunk_fed(r_1kV["isp_avg_s"], ICEBERG_DELTA_V_KM_S)
    print(f"Dual-ion (H+ + O+) at 1 kV grid:")
    print(f"  Isp_avg = {r_1kV['isp_avg_s']:.0f} s")
    print(f"  Thrust per kW electrical = {r_1kV['thrust_per_kw_electrical_N'] * 1000:.2f} mN/kW")
    print(f"  Electrical power for 1.5 N thrust = "
          f"{ICEBERG_THRUST_TARGET_N / r_1kV['thrust_per_kw_electrical_N']:.0f} kW")
    print(f"  Chunk-fed delivery fraction at 4.2 km/s = {delivery_1kV * 100:.1f} %")

    r_100V = dual_ion_thrust_per_kw(grid_voltage_V=100.0, use_h2_plus=False)
    delivery_100V = delivery_fraction_chunk_fed(r_100V["isp_avg_s"], ICEBERG_DELTA_V_KM_S)
    print(f"\nDual-ion (H+ + O+) at 100 V grid:")
    print(f"  Isp_avg = {r_100V['isp_avg_s']:.0f} s")
    print(f"  Electrical power for 1.5 N thrust = "
          f"{ICEBERG_THRUST_TARGET_N / r_100V['thrust_per_kw_electrical_N']:.0f} kW")
    print(f"  Chunk-fed delivery fraction at 4.2 km/s = {delivery_100V * 100:.1f} %")

    print(f"\nComparison with single-tech baselines:")
    print(f"  MET (R0, 600 s): delivery = "
          f"{delivery_fraction_chunk_fed(600, ICEBERG_DELTA_V_KM_S) * 100:.0f} %")
    print(f"  Pale Blue water ion (R1, 2000 s): delivery = "
          f"{delivery_fraction_chunk_fed(2000, ICEBERG_DELTA_V_KM_S) * 100:.0f} %")
    print(f"\nDual-ion at 1 kV requires roughly 20x the power of MET to win "
          f"~{(delivery_1kV - delivery_fraction_chunk_fed(600, ICEBERG_DELTA_V_KM_S)) * 100:.0f} "
          f"percentage points of delivery.")
    print(f"Dual-ion at 100 V requires roughly 6x the power of MET to win "
          f"~{(delivery_100V - delivery_fraction_chunk_fed(600, ICEBERG_DELTA_V_KM_S)) * 100:.0f} "
          f"percentage points of delivery.")


if __name__ == "__main__":
    main()
