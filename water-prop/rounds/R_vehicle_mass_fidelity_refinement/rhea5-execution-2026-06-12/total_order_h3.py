"""H3 — total-order sensitivity sensitivity of derived dry mass to subsystem anchors.

Jansen (1999) total-order estimator, hand-rolled on numpy (SALib not in env;
deviation D-D in STUDY.md). Parameter ranges are pre-registered in STUDY.md —
locked anchors (KRUSTY reactor specific power, MARVL radiator) get narrow
ranges; first-pass anchors (capture, TPS, structure, comms, bus, tankage,
margin) get wide ones. Model output: converged dry mass at the canonical cell
(30 kWe, 200 t chunk, ram-scoop bag, f = 0.80, aerocapture carried).

Run from project root:
  python3 water-prop/rounds/R_vehicle_mass_fidelity_refinement/total_order_h3.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


def _ensure_import_path():
    here = Path(__file__).resolve()
    sims_dir = here.parents[2] / "sims"
    if str(sims_dir) not in sys.path:
        sys.path.insert(0, str(sims_dir))


_ensure_import_path()

from mission_graph.framework import derive_dry_mass  # noqa: E402

POWER_KWE = 30.0
CHUNK_KG = 200_000.0
THRUST_N = 5.0
APERTURE_M2 = 50.0
ENTRY_V_KM_S = 11.0
F_PROP = 0.80

# (name, low, high) — pre-registered in STUDY.md H3.
PARAMS = (
    ("capture_coeff",        0.04,   0.16),   # x chunk
    ("capture_base_kg",      500.0,  2000.0),
    ("aperture_kg_per_m2",   25.0,   100.0),
    ("tps_chunk_coeff",      0.05,   0.20),   # x chunk
    ("tps_v_kg_per_kms",     100.0,  400.0),
    ("structure_coeff",      0.025,  0.10),   # x chunk
    ("comms_floor_kg",       1000.0, 4000.0),
    ("bus_floor_kg",         1000.0, 3000.0),
    ("reactor_w_per_kg",     2.2,    2.6),    # locked, narrow
    ("radiator_base_kg",     4500.0, 5500.0), # locked, narrow
    ("radiator_kg_per_kwe",  90.0,   110.0),  # locked, narrow
    ("tankage_coeff",        0.03,   0.08),   # x propellant
    ("dry_margin",           0.15,   0.25),
)
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS])
HI = np.array([p[2] for p in PARAMS])
K = len(PARAMS)


def dry_mass_model(x: np.ndarray) -> float:
    """Derived dry mass (kg) for one parameter vector; np.nan if non-converged."""
    p = dict(zip(NAMES, x))
    thrusters_kg = 10.0 * POWER_KWE  # titan-3 anchor, held fixed (locked-adjacent)
    fixed = {
        "powerplant": POWER_KWE * 1000.0 / p["reactor_w_per_kg"]
                      + p["radiator_base_kg"] + p["radiator_kg_per_kwe"] * POWER_KWE
                      + thrusters_kg,
        "bus": p["bus_floor_kg"],
        "capture_mechanism": p["capture_base_kg"] + p["capture_coeff"] * CHUNK_KG
                             + p["aperture_kg_per_m2"] * APERTURE_M2,
        "aerocapture_tps": p["tps_chunk_coeff"] * CHUNK_KG + p["tps_v_kg_per_kms"] * ENTRY_V_KM_S,
        "primary_structure": p["structure_coeff"] * CHUNK_KG + 100.0 * (THRUST_N / 1000.0),
        "comms_guidance_computer": p["comms_floor_kg"],
    }

    def demand_fn(dry_kg: float):
        propellant = (F_PROP / (1.0 - F_PROP)) * dry_kg
        out = dict(fixed)
        out["tankage"] = p["tankage_coeff"] * propellant
        return out

    r = derive_dry_mass(demand_fn, initial_guess_kg=50_000.0, dry_margin=p["dry_margin"])
    return r.dry_mass_kg if r.converged else np.nan


def jansen_total_order(n_base: int = 4096, seed: int = 42):
    """Saltelli A/B/AB_i sampling + Jansen total-order estimator."""
    rng = np.random.default_rng(seed)
    A = LO + (HI - LO) * rng.random((n_base, K))
    B = LO + (HI - LO) * rng.random((n_base, K))

    fA = np.array([dry_mass_model(x) for x in A])
    var_total = np.nanvar(fA, ddof=1)

    st = {}
    for i in range(K):
        ABi = A.copy()
        ABi[:, i] = B[:, i]
        fABi = np.array([dry_mass_model(x) for x in ABi])
        st[NAMES[i]] = float(np.nanmean((fA - fABi) ** 2) / (2.0 * var_total))
    return st, float(np.nanmean(fA)), float(np.nanstd(fA, ddof=1)), int(np.isnan(fA).sum())


def _selftest():
    """Estimator sanity: additive model f = 2*x0 + x1, x2 inert -> known indices."""
    rng = np.random.default_rng(0)
    n = 8192
    A = rng.random((n, 3)); B = rng.random((n, 3))
    f = lambda X: 2.0 * X[:, 0] + X[:, 1]
    fA = f(A)
    var = fA.var(ddof=1)
    st = []
    for i in range(3):
        ABi = A.copy(); ABi[:, i] = B[:, i]
        st.append(((fA - f(ABi)) ** 2).mean() / (2 * var))
    # analytic: V0=4/12, V1=1/12, V2=0 -> ST = .8, .2, 0
    assert abs(st[0] - 0.8) < 0.03 and abs(st[1] - 0.2) < 0.03 and st[2] < 0.01, st
    print(f"estimator self-test passed: ST = {[round(s, 3) for s in st]} (expect [0.8, 0.2, 0.0])")


def main():
    _selftest()
    st, mean_dry, std_dry, n_nan = jansen_total_order()
    print(f"\ncanonical cell (30 kWe, 200 t chunk): dry mass {mean_dry/1000:.1f} ± {std_dry/1000:.1f} t "
          f"(non-converged samples: {n_nan})")
    print("total-order sensitivity indices (Jansen), sorted:")
    for name, s in sorted(st.items(), key=lambda kv: -kv[1]):
        print(f"  {name:>22s}: {s:.3f}")
    grouped = {
        "capture_total": st["capture_coeff"] + st["capture_base_kg"] + st["aperture_kg_per_m2"],
        "tps_total": st["tps_chunk_coeff"] + st["tps_v_kg_per_kms"],
        "powerplant_total": st["reactor_w_per_kg"] + st["radiator_base_kg"] + st["radiator_kg_per_kwe"],
    }
    print("grouped (sum of member total-order indices, approximate):")
    for k, v in sorted(grouped.items(), key=lambda kv: -kv[1]):
        print(f"  {k:>22s}: {v:.3f}")
    print(f"\nH3 gate: capture grouped >= 0.15 AND largest single source -> "
          f"{'HELD' if grouped['capture_total'] >= 0.15 and grouped['capture_total'] == max(grouped.values()) else 'check FINDINGS'}")

    out = Path(__file__).parent / "results"
    out.mkdir(exist_ok=True)
    (out / "total_order_h3.json").write_text(json.dumps({
        "cell": {"power_kwe": POWER_KWE, "chunk_kg": CHUNK_KG},
        "mean_dry_kg": mean_dry, "std_dry_kg": std_dry,
        "total_order": st, "grouped": grouped,
    }, indent=2))
    print(f"wrote {out / 'total_order_h3.json'}")


if __name__ == "__main__":
    main()
