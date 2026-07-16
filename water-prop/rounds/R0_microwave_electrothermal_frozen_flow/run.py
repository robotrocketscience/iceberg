"""S01 — Water-MET frozen-flow vs equilibrium expansion sweep.

Sweeps chamber T and P, computes Isp under both expansion limits, writes a
table CSV and a comparison plot. Pure runner: physics lives in
src/waterprop/thermo/nozzle.py.

Run:
    uv run python studies/S01_met_frozen_flow/run.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from waterprop.constants import TORR_TO_PA
from waterprop.thermo import expand_equilibrium, expand_frozen

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def sweep(
    T_c_grid: np.ndarray,
    P_c_torr_grid: np.ndarray,
    P_exit_pa: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Run the (T_c, P_c) sweep. Returns (Isp_equilibrium, Isp_frozen) arrays."""
    Isp_eq = np.full((len(T_c_grid), len(P_c_torr_grid)), np.nan)
    Isp_fr = np.full_like(Isp_eq, np.nan)
    for i, T_c in enumerate(T_c_grid):
        for j, P_torr in enumerate(P_c_torr_grid):
            P_pa = P_torr * TORR_TO_PA
            try:
                Isp_eq[i, j], _, _ = expand_equilibrium(T_c, P_pa, P_exit_pa)
            except Exception as e:
                print(f"  eq fail at T={T_c} P={P_torr} torr: {type(e).__name__}")
            try:
                Isp_fr[i, j], _, _ = expand_frozen(T_c, P_pa, P_exit_pa)
            except Exception as e:
                print(f"  fr fail at T={T_c} P={P_torr} torr: {type(e).__name__}")
    return Isp_eq, Isp_fr


def write_csv(
    out: Path,
    T_c_grid: np.ndarray,
    P_c_torr_grid: np.ndarray,
    Isp_eq: np.ndarray,
    Isp_fr: np.ndarray,
) -> None:
    """Write a long-format CSV of all sweep points."""
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["T_c_K", "P_c_torr", "Isp_equilibrium_s", "Isp_frozen_s",
                    "frozen_penalty_pct"])
        for i, T_c in enumerate(T_c_grid):
            for j, P_torr in enumerate(P_c_torr_grid):
                eq = Isp_eq[i, j]
                fr = Isp_fr[i, j]
                pen = 100.0 * (eq - fr) / eq if (np.isfinite(eq) and np.isfinite(fr) and eq > 0) else np.nan
                w.writerow([T_c, P_torr,
                            f"{eq:.2f}" if np.isfinite(eq) else "",
                            f"{fr:.2f}" if np.isfinite(fr) else "",
                            f"{pen:.2f}" if np.isfinite(pen) else ""])


def print_tables(
    T_c_grid: np.ndarray,
    P_c_torr_grid: np.ndarray,
    Isp_eq: np.ndarray,
    Isp_fr: np.ndarray,
) -> None:
    """Print three tables to stdout: equilibrium Isp, frozen Isp, penalty."""
    def _print(title: str, arr: np.ndarray, fmt: str) -> None:
        print(f"\n{title}")
        header = f"{'T_c\\P_c (torr)':<15}" + "".join(f"{P:>8d}" for P in P_c_torr_grid)
        print(header)
        for i, T_c in enumerate(T_c_grid):
            row = f"{T_c:>10d} K   "
            for j in range(len(P_c_torr_grid)):
                v = arr[i, j]
                row += f"{v:>8.0f}" if np.isfinite(v) else f"{'nan':>8}"
            print(row)

    _print("Shifting-equilibrium Isp (s) — full recombination, optimistic", Isp_eq, "8.0f")
    _print("Frozen-flow Isp (s) — no recombination, conservative", Isp_fr, "8.0f")

    print("\nFrozen-flow penalty (% of equilibrium Isp lost)")
    header = f"{'T_c\\P_c (torr)':<15}" + "".join(f"{P:>8d}" for P in P_c_torr_grid)
    print(header)
    for i, T_c in enumerate(T_c_grid):
        row = f"{T_c:>10d} K   "
        for j in range(len(P_c_torr_grid)):
            eq, fr = Isp_eq[i, j], Isp_fr[i, j]
            if np.isfinite(eq) and np.isfinite(fr) and eq > 0:
                pct = 100.0 * (eq - fr) / eq
                row += f"{pct:>7.1f}%"
            else:
                row += f"{'nan':>8}"
        print(row)


def make_plot(
    T_c_grid: np.ndarray,
    P_c_torr_grid: np.ndarray,
    Isp_eq: np.ndarray,
    Isp_fr: np.ndarray,
    out: Path,
) -> None:
    """Two-panel comparison plot: Isp vs T at one P, and Isp vs P at one T."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

    P_ref_torr = 100
    j_ref = int(np.where(P_c_torr_grid == P_ref_torr)[0][0])
    ax = axes[0]
    ax.plot(T_c_grid, Isp_eq[:, j_ref], "o-", lw=2, color="C0",
            label="Equilibrium expansion (upper bound)")
    ax.plot(T_c_grid, Isp_fr[:, j_ref], "s-", lw=2, color="C3",
            label="Frozen-flow expansion (lower bound)")
    ax.fill_between(T_c_grid, Isp_fr[:, j_ref], Isp_eq[:, j_ref],
                    alpha=0.18, color="gray", label="Real-world band")
    ax.axhline(700, ls=":", color="k", alpha=0.5, label="Open-lit water-MET (~700 s)")
    ax.axhline(1000, ls=":", color="C2", alpha=0.5, label="R2.1 estimated ceiling (1000 s)")
    ax.set_xlabel("Chamber temperature (K)")
    ax.set_ylabel("Specific impulse (s)")
    ax.set_title(f"Isp vs chamber T at P_c = {P_ref_torr} torr")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3)

    T_ref = 7000
    i_ref = int(np.where(T_c_grid == T_ref)[0][0])
    ax = axes[1]
    ax.semilogx(P_c_torr_grid, Isp_eq[i_ref, :], "o-", lw=2, color="C0",
                label="Equilibrium expansion")
    ax.semilogx(P_c_torr_grid, Isp_fr[i_ref, :], "s-", lw=2, color="C3",
                label="Frozen-flow expansion")
    ax.fill_between(P_c_torr_grid, Isp_fr[i_ref, :], Isp_eq[i_ref, :],
                    alpha=0.18, color="gray")
    ax.set_xlabel("Chamber pressure (torr)")
    ax.set_title(f"Isp vs chamber P at T_c = {T_ref} K")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3, which="both")

    fig.suptitle("Water-MET: shifting-equilibrium vs frozen-flow Isp ceilings",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main() -> None:
    print("S01 — Water-MET frozen-flow vs equilibrium expansion analysis")
    print("=" * 60)

    T_c_grid = np.array([3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000])
    P_c_torr_grid = np.array([1, 3, 10, 30, 100, 300, 1000])

    print(f"Chamber T sweep (K):   {T_c_grid.tolist()}")
    print(f"Chamber P sweep (torr): {P_c_torr_grid.tolist()}")
    print(f"Exit P: 1 Pa (vacuum approximation)")

    Isp_eq, Isp_fr = sweep(T_c_grid, P_c_torr_grid)
    print_tables(T_c_grid, P_c_torr_grid, Isp_eq, Isp_fr)

    csv_path = RESULTS_DIR / "met_isp_table.csv"
    write_csv(csv_path, T_c_grid, P_c_torr_grid, Isp_eq, Isp_fr)
    print(f"\nTable written:  {csv_path}")

    png_path = RESULTS_DIR / "met_frozen_flow.png"
    make_plot(T_c_grid, P_c_torr_grid, Isp_eq, Isp_fr, png_path)
    print(f"Plot written:   {png_path}")

    best_eq = np.unravel_index(np.nanargmax(Isp_eq), Isp_eq.shape)
    best_fr = np.unravel_index(np.nanargmax(Isp_fr), Isp_fr.shape)
    print("\n--- KEY FINDINGS ---")
    print(f"Max equilibrium Isp: {Isp_eq[best_eq]:.0f} s "
          f"at T_c={T_c_grid[best_eq[0]]} K, P_c={P_c_torr_grid[best_eq[1]]} torr")
    print(f"Max frozen-flow Isp: {Isp_fr[best_fr]:.0f} s "
          f"at T_c={T_c_grid[best_fr[0]]} K, P_c={P_c_torr_grid[best_fr[1]]} torr")


if __name__ == "__main__":
    main()
