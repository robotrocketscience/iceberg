"""Tier-1.5 ram-scoop containment chain + harpoon cross-check + delivered-mass coupling.

Pre-registration: STUDY.md (this directory). Re-scoped execution of SCOPE.md per
rhea-5 / rhea-3 integrated recommendations; MuJoCo/Drake Tier 2/3 remains open.

Run from project root:
  python water-prop/rounds/R_chunk_capture_contact_fidelity/run.py
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

RNG_SEED = 20260724
N = 50_000
HERE = Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

# Fixed design parameters (STUDY.md)
R_AP_M = 15.0          # aperture radius
L_BAG_M = 30.0         # bag depth
JAM_FRACTION = 0.8     # silhouette semi-major axis > JAM_FRACTION * R_AP -> jam
CEIL_REF_MASS_T = 1.0  # Round J ceiling reference mass (coefficient axis is at 1 t)

# Round J anchors: ceiling coefficient at 1 t spans pessimistic contact-patch
# lightweight (~2.4 m/s) to strong Zylon whole-bag (24.6 m/s); scales m^(-1/6).
CEIL_COEFF_LO = 2.4
CEIL_COEFF_HI = 24.6

AXES = (
    # name, lo, hi, kind  (first five shared with Tier-1 / rhea-5 Tier-1.5)
    ("chunk_mass_t",          10.0,   200.0,  "log"),
    ("spin_rate_rpm",         0.0005, 0.05,   "log"),
    ("approach_vel_cms",      0.3,    3.0,    "lin"),
    ("sensor_noise_m",        0.05,   0.50,   "lin"),
    ("surface_friction",      0.05,   0.40,   "lin"),
    ("chunk_density_kg_m3",   300.0,  900.0,  "lin"),
    ("aspect_ratio",          1.0,    2.5,    "lin"),
    ("restitution_e",         0.02,   0.30,   "log"),
    ("ceiling_coeff_ms",      CEIL_COEFF_LO, CEIL_COEFF_HI, "log"),
    ("drawstring_speed_ms",   0.1,    1.0,    "log"),
    ("gnc_residual_ms",       0.001,  1.0,    "log"),
    ("ice_tensile_kpa",       1.0,    100.0,  "log"),
)
NAMES = [a[0] for a in AXES]

MODE_NAMES = {0: "captured_coherent", 1: "aperture_miss", 2: "oversize_jam",
              3: "bounce_out", 4: "containment_tear", 5: "captured_rubble"}


def sample_axes(u: np.ndarray) -> dict[str, np.ndarray]:
    out = {}
    for i, (name, lo, hi, kind) in enumerate(AXES):
        if kind == "log":
            out[name] = np.exp(np.log(lo) + u[:, i] * (np.log(hi) - np.log(lo)))
        else:
            out[name] = lo + u[:, i] * (hi - lo)
    return out


def containment_event(x: dict[str, np.ndarray], rng: np.random.Generator | None,
                      pin_residual_low: bool):
    """Ram-scoop Tier-1.5 chain. Returns (water_captured, coherent, mode).

    pin_residual_low=True: shared-prior run (A) — GNC residual pinned to its low
    end so v_op sits in the Tier-1 0.3-3 cm/s comparability band.
    """
    m_chunk = x["chunk_mass_t"] * 1000.0
    omega = x["spin_rate_rpm"] * 2.0 * np.pi / 60.0
    v_app = x["approach_vel_cms"] / 100.0
    sigma_pose = x["sensor_noise_m"]
    rho = x["chunk_density_kg_m3"]
    ar = x["aspect_ratio"]
    e_rest = x["restitution_e"]
    c_ceil = x["ceiling_coeff_ms"]
    v_draw = x["drawstring_speed_ms"]
    resid = np.full_like(v_app, 0.001) if pin_residual_low else x["gnc_residual_ms"]
    sig_ice = x["ice_tensile_kpa"] * 1e3

    n_s = len(m_chunk)

    # Chunk geometry (prolate ellipsoid, rhea-5 convention)
    b = (3.0 * m_chunk / (4.0 * np.pi * rho * ar)) ** (1.0 / 3.0)
    a = ar * b
    sil = np.sqrt(a * b)

    # Operating velocity: the GNC-achievable null residual floors the approach
    v_op = np.maximum(v_app, resid)

    # --- 1. Aperture entry ------------------------------------------------- #
    # Pose error (Rayleigh) + spin-driven surface drift over the entry transit.
    t_entry = L_BAG_M / v_op
    drift = np.minimum(omega * sil * t_entry, sil)  # bounded by chunk size
    if rng is not None:
        err = sigma_pose * np.sqrt(rng.standard_normal(n_s) ** 2
                                   + rng.standard_normal(n_s) ** 2)
    else:
        err = sigma_pose * np.sqrt(np.pi / 2.0)
    miss = (err + drift + sil) > R_AP_M

    # --- 2. Oversize jam ---------------------------------------------------- #
    jam = a > JAM_FRACTION * R_AP_M

    # --- 3. Bounce-out race ------------------------------------------------- #
    # Chunk transits depth L, rebounds inelastically (restitution e), returns to
    # the aperture plane; the drawstring closes radially at v_draw from entry.
    t_return = L_BAG_M / v_op + L_BAG_M / (e_rest * v_op)
    r_open_at_return = np.maximum(R_AP_M - v_draw * t_return, 0.0)
    bounce_out = r_open_at_return > sil  # chunk fits through what remains open

    # --- 4. Containment tear (Round J derived ceiling) ---------------------- #
    v_ceiling = c_ceil * (x["chunk_mass_t"] / CEIL_REF_MASS_T) ** (-1.0 / 6.0)
    tear = v_op > v_ceiling

    # --- 5. Fragmentation (contained rubble, Round J reading) --------------- #
    v_frag = np.sqrt(3.0 * sig_ice / (2.0 * rho))
    frag = v_op > v_frag

    mode = np.zeros(n_s, dtype=int)
    alive = ~miss
    mode[miss] = 1
    j = alive & jam;        mode[j] = 2; alive &= ~jam
    bo = alive & bounce_out; mode[bo] = 3; alive &= ~bounce_out
    tr = alive & tear;      mode[tr] = 4; alive &= ~tear
    coherent = alive & ~frag
    rubble = alive & frag
    mode[rubble] = 5
    water_captured = alive  # rubble still captures water (Round J)
    return water_captured, coherent, mode


def jansen_total_order(pin_v_op_ms: float | None = None, n_base: int = 8192):
    """Total-order indices. Below the cliff the outcome is constant (variance 0),
    so H-K3's indices are computed at a pinned cliff velocity where variance exists."""
    rng = np.random.default_rng(RNG_SEED)
    k = len(AXES)
    A = rng.random((n_base, k))
    B = rng.random((n_base, k))

    def f(u):
        x = sample_axes(u)
        if pin_v_op_ms is not None:
            x["approach_vel_cms"] = np.full(len(u), pin_v_op_ms * 100.0)
            x["gnc_residual_ms"] = np.full(len(u), 1e-4)
        ok, _, _ = containment_event(x, rng=None, pin_residual_low=False)
        return ok.astype(float)

    fA = f(A)
    var = fA.var(ddof=1)
    st = {}
    for i in range(k):
        ABi = A.copy()
        ABi[:, i] = B[:, i]
        st[NAMES[i]] = float(((fA - f(ABi)) ** 2).mean() / (2.0 * var)) if var > 0 else 0.0
    return st


def run_block(tag: str, pin_residual_low: bool, rng: np.random.Generator):
    u = rng.random((N, len(AXES)))
    x = sample_axes(u)
    ok, coherent, mode = containment_event(x, rng=rng,
                                           pin_residual_low=pin_residual_low)
    boot = []
    for _ in range(400):
        idx = rng.integers(0, N, N)
        boot.append(ok[idx].mean())
    q05, q95 = np.quantile(boot, [0.05, 0.95])
    counts = {MODE_NAMES[m]: int((mode == m).sum()) for m in MODE_NAMES}
    print(f"\n--- {tag} ---")
    print(f"P(water captured) = {ok.mean():.3f} [{q05:.3f}, {q95:.3f}]   "
          f"P(coherent chunk) = {coherent.mean():.3f}")
    for k_, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k_:>18s}: {v/N:.3f}")
    return {"tag": tag, "p_water": float(ok.mean()), "p_coherent": float(coherent.mean()),
            "bootstrap_ci": [float(q05), float(q95)],
            "mode_shares": {k_: v / N for k_, v in counts.items()}}, x, ok


def cliff_profile():
    """H-K4: capture vs pinned operating velocity (expected geometry)."""
    rng = np.random.default_rng(RNG_SEED + 1)
    v_ops = np.array([0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0])
    rows = []
    for v in v_ops:
        u = rng.random((20_000, len(AXES)))
        x = sample_axes(u)
        x["approach_vel_cms"] = np.full(20_000, v * 100.0)
        x["gnc_residual_ms"] = np.full(20_000, 1e-4)
        ok, coherent, mode = containment_event(x, rng=rng, pin_residual_low=False)
        share_bo = float((mode == 3).mean())
        share_tear = float((mode == 4).mean())
        rows.append({"v_op_ms": float(v), "p_water": float(ok.mean()),
                     "p_coherent": float(coherent.mean()),
                     "share_bounce_out": share_bo, "share_tear": share_tear})
        print(f"  v_op {v:6.3f} m/s: P(water) {ok.mean():.3f}  "
              f"P(coherent) {coherent.mean():.3f}  bounce_out {share_bo:.3f}  "
              f"tear {share_tear:.3f}")
    return rows


def harpoon_cross_check():
    """Reuse rhea-5's Tier-1.5 harpoon model verbatim (D-3)."""
    path = (HERE.parent / "R_chunk_capture_tier15_reduced_order" / "run.py")
    spec = importlib.util.spec_from_file_location("tier15_harpoon", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rng = np.random.default_rng(mod.RNG_SEED)
    u = rng.random((mod.N, len(mod.AXES)))
    x = mod.sample_axes(u)
    ok, _ = mod.capture_event(x, rng=rng)
    return float(ok.mean())


def main():
    rng = np.random.default_rng(RNG_SEED)

    out_a, _, _ = run_block("run A — shared-prior band (Tier-1 comparability)",
                            pin_residual_low=True, rng=rng)
    out_b, _, _ = run_block("run B — GNC-residual live (operating envelope)",
                            pin_residual_low=False, rng=rng)

    print("\nH-K4 containment-cliff profile (expected geometry):")
    cliff = cliff_profile()

    st = jansen_total_order(pin_v_op_ms=3.0)
    print("\ntotal-order sensitivity (pinned at cliff, v_op = 3 m/s), top 6:")
    for name, s in sorted(st.items(), key=lambda kv: -kv[1])[:6]:
        print(f"  {name:>20s}: {s:.3f}")

    # H-K4 gate numbers
    p_1cm = next(r["p_water"] for r in cliff if abs(r["v_op_ms"] - 0.01) < 1e-9)
    p_1m = next(r["p_water"] for r in cliff if abs(r["v_op_ms"] - 1.0) < 1e-9)
    print(f"\nH-K4 collapse (1 cm/s -> 1 m/s): {p_1m - p_1cm:+.3f} (gate: <= -0.2)")

    p_harpoon = harpoon_cross_check()
    print(f"\nharpoon cross-check (rhea-5 model, verbatim): {p_harpoon:.3f}")

    # rhea-3 eta_dv coupling at the 200-t anchor: harpoon 20.85 %, ram-scoop 3.92 %
    eta_h, eta_rs = 0.2085, 0.0392
    p_rs = out_a["p_water"]
    lead = (p_harpoon * eta_h) / max(p_rs * eta_rs, 1e-9)
    print(f"H-K2 delivered-mass lead (harpoon/ram-scoop, 200-t anchor): {lead:.2f}x")

    # H-K5: binomial half-width at n = 1200 at the run-A operating point
    hw = 1.96 * np.sqrt(p_rs * (1 - p_rs) / 1200.0)
    print(f"H-K5 binomial half-width at n=1200, p={p_rs:.3f}: {hw:.4f}")

    payload = {
        "round": "R_chunk_capture_contact_fidelity (Tier-1.5 re-scoped execution)",
        "seed": RNG_SEED, "n": N,
        "run_a_shared_prior": out_a,
        "run_b_residual_live": out_b,
        "cliff_profile": cliff,
        "total_order_sensitivity_at_cliff_3ms": st,
        "hk4_collapse_1cms_to_1ms": float(p_1m - p_1cm),
        "harpoon_cross_check_p": p_harpoon,
        "tier1_ramscoop_ref": 0.405,
        "eta_dv": {"harpoon": eta_h, "ramscoop": eta_rs, "source": "rhea-3 coupled model, 200 t anchor"},
        "hk2_delivered_lead_x": float(lead),
        "hk5_halfwidth_n1200": float(hw),
    }
    (RESULTS / "tier15_ramscoop_results.json").write_text(json.dumps(payload, indent=2))
    print(f"\nwrote {RESULTS / 'tier15_ramscoop_results.json'}")


if __name__ == "__main__":
    main()
