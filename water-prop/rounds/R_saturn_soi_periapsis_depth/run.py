"""Saturn-Orbit-Insertion periapsis-depth trade — Oberth vs ring-crossing risk.

Five sweeps mapping to pre-registered H1–H5 in STUDY.md.

Outputs:
  results/oberth_curve.csv          — H1: SOI Δv vs r_p_burn
  results/cassini_benchmark.csv     — H2: model vs Cassini's 626 m/s
  results/ring_zones.csv            — H3: zonal optical-depth lookup
  results/zero_inclination_zones.csv — H3: which r_p_burn zones are viable
  results/argument_trim_cost.csv    — H4: cost of moving ring crossings
  results/mission_risk_budget.csv   — H5: mission-integrated impact risk
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

GM_SATURN = 37931207.7    # km^3 / s^2
R_SATURN  = 60268.0       # km (1-bar equatorial radius)
ATM_FLOOR = 61500.0       # km (safe r_p above 1-bar)
R_TITAN   = 1208547.0     # km (from Horizons cache, 2045-01-01)
V_TITAN   = 5.631         # km/s

V_INF_HOHMANN = 5.44      # km/s nominal Earth->Saturn Hohmann arrival

# -----------------------------------------------------------------------------
# Ring zones — vertical optical depth τ at the zone midpoint.
# Sources: Cuzzi (2010) Icarus; Hedman & Stewart (2009); Colwell et al. (2009).
# τ given here are typical zone-averaged values. Real τ has km-scale structure.
# -----------------------------------------------------------------------------

@dataclass
class RingZone:
    name: str
    r_inner_km: float
    r_outer_km: float
    tau_typical: float
    tau_max: float  # local peak τ seen in occultations

RING_ZONES = [
    RingZone("Below D-ring (sub-rings)",     ATM_FLOOR, 67000.0, 0.0,     0.0),
    RingZone("D-ring",                       67000.0,   74500.0, 5.0e-4,  1.0e-3),
    RingZone("C-ring",                       74500.0,   92000.0, 0.10,    0.30),
    RingZone("B-ring",                       92000.0,   117580.0, 2.0,    5.0),
    RingZone("Cassini Division",             117580.0,  122170.0, 0.10,   0.15),
    RingZone("A-ring",                       122170.0,  136775.0, 0.60,   0.80),
    RingZone("Encke Gap",                    133210.0,  133610.0, 1.0e-3, 1.0e-2),
    RingZone("Keeler Gap",                   136405.0,  136605.0, 1.0e-3, 1.0e-2),
    RingZone("F-ring",                       139700.0,  140700.0, 0.10,   0.50),
    RingZone("F-G gap",                      140700.0,  166000.0, 1.0e-5, 1.0e-4),
    RingZone("G-ring",                       166000.0,  175000.0, 1.0e-6, 1.0e-5),
    RingZone("E-ring (diffuse)",             180000.0,  480000.0, 1.0e-6, 1.0e-5),
    RingZone("Outside E-ring",               480000.0,  1.0e10,   0.0,    0.0),
]


def ring_zone_at(r_km: float) -> RingZone:
    """Return the RingZone containing radius r_km, or 'Outside' if r_km is in a gap."""
    for z in RING_ZONES:
        if z.r_inner_km <= r_km < z.r_outer_km:
            return z
    return RING_ZONES[-1]  # default to "Outside E-ring"


# -----------------------------------------------------------------------------
# Physics
# -----------------------------------------------------------------------------

def soi_dv(r_p_km: float, r_a_km: float, v_inf_kms: float = V_INF_HOHMANN) -> dict:
    """Single-burn SOI cost at periapsis r_p to capture into ellipse (r_p, r_a)."""
    v_p_hyp = float(np.sqrt(v_inf_kms ** 2 + 2 * GM_SATURN / r_p_km))
    a = 0.5 * (r_p_km + r_a_km)
    v_p_ell = float(np.sqrt(GM_SATURN * (2 / r_p_km - 1 / a)))
    period_days = 2 * np.pi * np.sqrt(a ** 3 / GM_SATURN) / 86400.0
    return {
        "r_p_km": r_p_km,
        "r_a_km": r_a_km,
        "v_p_hyperbolic_kms": v_p_hyp,
        "v_p_ellipse_kms": v_p_ell,
        "soi_dv_kms": v_p_hyp - v_p_ell,
        "orbit_period_days": period_days,
        "ring_zone_at_periapsis": ring_zone_at(r_p_km).name,
        "tau_at_periapsis": ring_zone_at(r_p_km).tau_typical,
    }


def impact_prob_per_crossing(r_crossing_km: float, inclination_deg: float) -> float:
    """Leading-order probability of intersecting a ring particle on one ring-plane crossing.

    For inclinations >~10°, treat the geometric optical depth τ as the probability
    that a random vertical line through the ring (the spacecraft's effective
    path) intersects a particle. For shallow inclinations, lateral path through
    the ring scales as csc(i), increasing intersection probability.
    """
    zone = ring_zone_at(r_crossing_km)
    tau = zone.tau_typical
    i_rad = np.radians(max(0.5, inclination_deg))  # clamp away from zero
    # Vertical-pass geometry: probability scales with csc(i) for small i, then
    # saturates at 1 - exp(-τ) for nearly vertical passes.
    optical = 1.0 - np.exp(-tau / np.sin(i_rad))
    return float(min(1.0, optical))


def argument_of_periapsis_trim_cost(
    r_a_km: float, r_p_km: float, delta_omega_deg: float
) -> float:
    """Δv to rotate the argument-of-periapsis by Δω, performed at apoapsis.

    Simple formula: Δv = 2·v(r_a)·sin(Δω/2), valid for in-plane rotation of the
    apsidal line while preserving energy and angular momentum magnitude.
    """
    a = 0.5 * (r_p_km + r_a_km)
    v_a = float(np.sqrt(GM_SATURN * (2 / r_a_km - 1 / a)))
    return float(2 * v_a * np.sin(np.radians(delta_omega_deg / 2)))


# -----------------------------------------------------------------------------
# Sweeps
# -----------------------------------------------------------------------------

def sweep_oberth_curve(out_dir: Path) -> None:
    """H1 — SOI Δv vs r_p_burn at fixed target apoapsis."""
    r_p_grid = np.linspace(ATM_FLOOR, 4.15 * R_SATURN, 80)
    rows = []
    targets = {
        "r_a = r_titan":   R_TITAN,
        "r_a = 3 r_titan": 3 * R_TITAN,
        "r_a = 6 r_titan": 6 * R_TITAN,
    }
    for r_p in r_p_grid:
        for name, r_a in targets.items():
            d = soi_dv(r_p, r_a)
            rows.append({"target": name, "r_p_R_saturn": r_p / R_SATURN, **d})
    write_csv(out_dir / "oberth_curve.csv", rows)

    fig, ax = plt.subplots(figsize=(9, 5))
    for name, r_a in targets.items():
        xs = [r["r_p_R_saturn"] for r in rows if r["target"] == name]
        ys = [r["soi_dv_kms"] for r in rows if r["target"] == name]
        ax.plot(xs, ys, label=name)
    # ring-zone shading
    for z in RING_ZONES:
        if z.r_inner_km > 4.15 * R_SATURN: continue
        if z.tau_typical >= 0.1:
            color = "tab:red"; alpha = 0.20
        elif z.tau_typical >= 1e-3:
            color = "tab:orange"; alpha = 0.10
        else:
            color = "tab:green"; alpha = 0.05
        ax.axvspan(z.r_inner_km / R_SATURN, z.r_outer_km / R_SATURN, color=color, alpha=alpha)
    # Cassini reference
    ax.axvline(80250 / R_SATURN, ls="--", color="black", alpha=0.7,
               label="Cassini SOI r_p (80,250 km)")
    ax.set_xlabel("SOI periapsis radius [Saturn radii]")
    ax.set_ylabel("SOI propulsive Δv [km/s]")
    ax.set_title("H1 — Oberth curve at v_∞ = 5.44 km/s\nshading = ring optical depth zones")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_xlim(1.0, 4.15)
    fig.tight_layout()
    fig.savefig(out_dir / "oberth_curve.png", dpi=130)
    plt.close(fig)


def cassini_benchmark(out_dir: Path) -> None:
    """H2 — Reproduce Cassini's 626 m/s SOI burn and bracket sub-D-ring saving."""
    rows = []
    # Cassini: r_p = 80,250 km, initial orbit a ~ 4.6e6 km (apoapsis 9.13e6 km)
    cassini_r_p = 80250.0
    cassini_r_a = 9.13e6
    d_cassini = soi_dv(cassini_r_p, cassini_r_a)
    d_cassini["case"] = "Cassini actual (r_p=80250 km, r_a=9.13e6 km)"
    rows.append(d_cassini)

    # Iceberg sub-D-ring options at same final orbit (a = 4.6e6 km):
    for rp in [61500.0, 63000.0, 65000.0, 67000.0, 70000.0, 75000.0, 80250.0]:
        d = soi_dv(rp, cassini_r_a)
        d["case"] = f"sub-D-ring sweep at r_p={rp:.0f} km"
        rows.append(d)

    # Same sweep but at ICEBERG-relevant r_a = 3 r_titan (3.6e6 km):
    for rp in [61500.0, 63000.0, 65000.0, 67000.0, 70000.0, 80250.0, 120000.0, 150000.0]:
        d = soi_dv(rp, 3 * R_TITAN)
        d["case"] = f"ICEBERG r_a=3r_titan at r_p={rp:.0f} km"
        rows.append(d)

    write_csv(out_dir / "cassini_benchmark.csv", rows)


def zero_inclination_zones(out_dir: Path) -> None:
    """H3 — Which r_p_burn zones are operationally viable at zero inclination
    (worst case where periapsis radius = ring-plane-crossing radius)?
    """
    rows = []
    # Sample at zone midpoints + some interior points.
    sample_points = []
    for z in RING_ZONES:
        if z.r_inner_km > 250000.0: continue
        sample_points.append((z.r_inner_km + z.r_outer_km) / 2)
        sample_points.append(z.r_inner_km + 0.01 * (z.r_outer_km - z.r_inner_km))
    sample_points = sorted(set(round(p, 1) for p in sample_points if p > ATM_FLOOR))

    for r_p in sample_points:
        d = soi_dv(r_p, 3 * R_TITAN)
        # impact probability if SOI ring crossing happens at r_p (zero-inclination case)
        p_impact_zero_i = impact_prob_per_crossing(r_p, inclination_deg=0.5)
        p_impact_low_i = impact_prob_per_crossing(r_p, inclination_deg=10.0)
        p_impact_hohmann_i = impact_prob_per_crossing(r_p, inclination_deg=26.7)
        rows.append({
            "r_p_km": r_p,
            "ring_zone": d["ring_zone_at_periapsis"],
            "tau": d["tau_at_periapsis"],
            "soi_dv_kms": d["soi_dv_kms"],
            "p_impact_inc_0p5deg": p_impact_zero_i,
            "p_impact_inc_10deg": p_impact_low_i,
            "p_impact_inc_26p7deg": p_impact_hohmann_i,
        })
    write_csv(out_dir / "zero_inclination_zones.csv", rows)


def argument_trim_cost(out_dir: Path) -> None:
    """H4 — Cost of rotating argument-of-periapsis to move ring crossings."""
    rows = []
    # Three target apoapsis cases; sweep Δω = 30° to 180°
    for r_a_factor in [1, 3, 6]:
        r_a = r_a_factor * R_TITAN
        r_p = 63000.0  # deep periapsis case
        for dw in [10, 30, 60, 90, 120, 180]:
            dv = argument_of_periapsis_trim_cost(r_a, r_p, dw)
            rows.append({
                "r_a_titan_radii": r_a_factor,
                "r_p_km": r_p,
                "delta_omega_deg": dw,
                "trim_dv_kms": dv,
            })
    write_csv(out_dir / "argument_trim_cost.csv", rows)

    fig, ax = plt.subplots(figsize=(8, 5))
    for r_a_factor in [1, 3, 6]:
        xs = [r["delta_omega_deg"] for r in rows if r["r_a_titan_radii"] == r_a_factor]
        ys = [r["trim_dv_kms"] * 1000.0 for r in rows if r["r_a_titan_radii"] == r_a_factor]
        ax.plot(xs, ys, marker="o", label=f"r_a = {r_a_factor}×r_titan")
    ax.axhline(100, ls="--", color="gray", alpha=0.5, label="H4 budget 100 m/s")
    ax.set_xlabel("argument-of-periapsis rotation [deg]")
    ax.set_ylabel("propulsive cost at apoapsis [m/s]")
    ax.set_title("H4 — cost of rotating apsidal line (in-plane, at apoapsis)")
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "argument_trim_cost.png", dpi=130)
    plt.close(fig)


def mission_risk_budget(out_dir: Path) -> None:
    """H5 — Integrated mission-level impact risk across all ring-plane crossings."""
    inclination = 26.7  # deg (Hohmann arrival default)

    # Crossing inventory for a typical ICEBERG round-trip:
    # 1. SOI inbound: 1 or 2 crossings depending on arg-of-periapsis. Best-case
    #    nodes outside main rings: crossings in F-G gap (τ ~1e-5).
    #    Worst-case zero-inclination: crossing at periapsis radius.
    # 2. Titan tour pumping: 2 flybys, 2-3 orbits each → ~5 crossings. Same
    #    argument-of-periapsis pattern → F-G gap crossings if controlled.
    # 3. B-ring rendezvous: descent + transit + ascent per chunk capture.
    #    For one chunk, 2 crossings AT B-ring radius (~100,000 km, τ ~2-5).
    #    This is operationally unavoidable — must enter B-ring to grab chunk.
    # 4. Departure: 1 crossing to leave Saturn system.

    crossings = [
        # (name, count, r_crossing_km)
        ("SOI inbound (nodes in F-G gap)",   1, 152000.0),
        ("Titan tour orbit crossings (F-G gap)", 5, 152000.0),
        ("B-ring inbound rendezvous",        1, 100000.0),
        ("B-ring outbound (post-capture)",   1, 100000.0),
        ("Departure crossing (F-G gap)",     1, 152000.0),
    ]
    rows = []
    p_no_impact_cumulative = 1.0
    for name, n, r in crossings:
        p_one = impact_prob_per_crossing(r, inclination)
        p_n_no = (1.0 - p_one) ** n
        contribution = 1.0 - p_n_no
        rows.append({
            "phase": name,
            "n_crossings": n,
            "r_crossing_km": r,
            "ring_zone": ring_zone_at(r).name,
            "tau": ring_zone_at(r).tau_typical,
            "p_impact_per_crossing": p_one,
            "p_no_impact_after_n": p_n_no,
            "contribution_to_failure": contribution,
        })
        p_no_impact_cumulative *= p_n_no

    total_p_failure = 1.0 - p_no_impact_cumulative
    # contribution share of each phase
    for r in rows:
        r["share_of_total_risk_pct"] = 100.0 * r["contribution_to_failure"] / total_p_failure if total_p_failure > 0 else 0.0
    rows.append({
        "phase": "TOTAL mission impact-failure probability",
        "n_crossings": sum(r["n_crossings"] for r in rows if isinstance(r["n_crossings"], int)),
        "r_crossing_km": float("nan"),
        "ring_zone": "—",
        "tau": float("nan"),
        "p_impact_per_crossing": float("nan"),
        "p_no_impact_after_n": p_no_impact_cumulative,
        "contribution_to_failure": total_p_failure,
        "share_of_total_risk_pct": 100.0,
    })
    write_csv(out_dir / "mission_risk_budget.csv", rows)

    # alternative scenario: SOI crossings inside B-ring (worst-case zero-inc)
    crossings_bad = [
        ("SOI inbound at B-ring (zero-inc, periapsis in B-ring)",  1, 100000.0),
        ("Titan tour crossings (also through B-ring)",            5, 100000.0),
        ("B-ring inbound rendezvous",                             1, 100000.0),
        ("B-ring outbound",                                       1, 100000.0),
        ("Departure (zero-inc)",                                  1, 100000.0),
    ]
    rows_bad = []
    p_no_impact_bad = 1.0
    for name, n, r in crossings_bad:
        p_one = impact_prob_per_crossing(r, inclination_deg=0.5)  # zero inclination
        p_n_no = (1.0 - p_one) ** n
        p_no_impact_bad *= p_n_no
        rows_bad.append({
            "phase": name,
            "n_crossings": n,
            "r_crossing_km": r,
            "tau": ring_zone_at(r).tau_typical,
            "p_impact_per_crossing": p_one,
            "p_no_impact_after_n": p_n_no,
        })
    rows_bad.append({
        "phase": "TOTAL (worst-case zero-inclination)",
        "n_crossings": sum(r["n_crossings"] for r in rows_bad),
        "r_crossing_km": float("nan"),
        "tau": float("nan"),
        "p_impact_per_crossing": float("nan"),
        "p_no_impact_after_n": p_no_impact_bad,
    })
    write_csv(out_dir / "mission_risk_budget_zero_inc.csv", rows_bad)


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list({k for r in rows for k in r.keys()})
    # preserve insertion order of first row's keys for readability
    ordered_keys = list(rows[0].keys())
    for r in rows:
        for k in r.keys():
            if k not in ordered_keys:
                ordered_keys.append(k)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ordered_keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> int:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    print("[H1] Oberth curve sweep ...");          sweep_oberth_curve(out_dir)
    print("[H2] Cassini benchmark ...");           cassini_benchmark(out_dir)
    print("[H3] Zero-inclination ring zones ...");  zero_inclination_zones(out_dir)
    print("[H4] Argument-of-periapsis trim ...");   argument_trim_cost(out_dir)
    print("[H5] Mission risk budget ...");          mission_risk_budget(out_dir)
    print("\nDone. Outputs in", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
