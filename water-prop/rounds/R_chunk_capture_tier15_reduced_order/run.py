"""Tier 1.5 reduced-order harpoon capture model — mechanics-derived event chain.

See STUDY.md for pre-registered hypotheses, priors, and declared model-form risks.

Run from project root:
  cd water-prop && uv run python rounds/R_chunk_capture_tier15_reduced_order/run.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RNG_SEED = 20260612
N = 50_000
RESULTS = Path(__file__).parent / "results"
RESULTS.mkdir(exist_ok=True)

# Fixed design parameters (STUDY.md)
M_PROJ_KG = 5.0
A_TIP_M2 = 2e-3
A_ANCHOR_M2 = 0.02
BARB_DEPTH_REQ_M = 0.15
STANDOFF_M = 20.0
M_SC_KG = 80_000.0
CRUSH_OVER_SHEAR = 3.0
REEL_TENSION_FACTOR = 0.10   # steady reel tension as fraction of anchor capacity
WRAP_FRACTION = 0.5          # fraction of half-rotation before wrap binds


AXES = (
    # name, lo, hi, kind
    ("chunk_mass_t",          10.0,   200.0,  "log"),
    ("spin_rate_rpm",         0.0005, 0.05,   "log"),
    ("approach_vel_cms",      0.3,    3.0,    "lin"),
    ("sensor_noise_m",        0.05,   0.50,   "lin"),
    ("surface_friction",      0.05,   0.40,   "lin"),
    ("chunk_density_kg_m3",   300.0,  900.0,  "lin"),
    ("aspect_ratio",          1.0,    2.5,    "lin"),
    ("ice_shear_strength_kpa", 10.0,  200.0,  "log"),
    ("tether_stiffness_n_m",  1e3,    1e5,    "log"),
    ("tether_strength_kn",    5.0,    50.0,   "lin"),
    ("projectile_speed_ms",   2.0,    10.0,   "lin"),
    ("reel_speed_cms",        1.0,    10.0,   "lin"),
)
NAMES = [a[0] for a in AXES]


def sample_axes(u: np.ndarray) -> dict[str, np.ndarray]:
    """u: (n, len(AXES)) uniforms -> axis dict."""
    out = {}
    for i, (name, lo, hi, kind) in enumerate(AXES):
        if kind == "log":
            out[name] = np.exp(np.log(lo) + u[:, i] * (np.log(hi) - np.log(lo)))
        else:
            out[name] = lo + u[:, i] * (hi - lo)
    return out


def capture_event(x: dict[str, np.ndarray], rng: np.random.Generator | None = None,
                  n: int | None = None):
    """Mechanics-derived harpoon capture chain.

    Returns (success: bool array, mode: int array) where mode encodes the FIRST
    failure in the chain: 0=success, 1=miss, 2=glance, 3=shallow_penetration,
    4=tear_out, 5=tether_snap, 6=wrap_bind.

    Aleatoric draws (aim error direction/magnitude, impact-point location) use
    `rng` when given; for the Jansen sensitivity runs `rng=None` uses the
    EXPECTED-geometry deterministic chain so indices reflect the epistemic axes.
    """
    m_chunk = x["chunk_mass_t"] * 1000.0
    omega = x["spin_rate_rpm"] * 2.0 * np.pi / 60.0          # rad/s
    v_app = x["approach_vel_cms"] / 100.0                     # m/s
    sigma_aim = x["sensor_noise_m"]
    mu_fric = x["surface_friction"]
    rho = x["chunk_density_kg_m3"]
    ar = x["aspect_ratio"]
    sig_shear = x["ice_shear_strength_kpa"] * 1e3             # Pa
    k_tether = x["tether_stiffness_n_m"]
    f_tether_max = x["tether_strength_kn"] * 1e3              # N
    v_proj = x["projectile_speed_ms"]
    v_reel = x["reel_speed_cms"] / 100.0                      # m/s

    n_s = len(m_chunk)

    # Chunk geometry: prolate ellipsoid, semi-axes (a, b, b), a = ar * b
    # volume = 4/3 pi a b^2 = m/rho  ->  b = (3 m / (4 pi rho ar))^(1/3)
    b = (3.0 * m_chunk / (4.0 * np.pi * rho * ar)) ** (1.0 / 3.0)
    a = ar * b
    sil = np.sqrt(a * b)          # effective silhouette radius (geometric mean)

    # --- 1. Hit / miss ---------------------------------------------------- #
    t_flight = STANDOFF_M / v_proj
    drift = omega * sil * t_flight                 # surface motion during flight
    if rng is not None:
        err = sigma_aim * np.sqrt(rng.standard_normal(n_s) ** 2
                                  + rng.standard_normal(n_s) ** 2)  # Rayleigh
        u_hit = rng.random(n_s)                    # impact-point offset fraction
    else:
        err = sigma_aim * np.sqrt(np.pi / 2.0)     # Rayleigh mean
        u_hit = np.full(n_s, 0.5)                  # expected offset
    total_err = err + drift
    miss = total_err > sil

    # --- 2. Glance-off ---------------------------------------------------- #
    # Offset fraction at impact -> local incidence angle on the ellipsoid.
    # sin(theta) ~ radial offset fraction, worsened by elongation when hitting
    # the long flank.
    offset_frac = np.clip((total_err / sil) * u_hit + (1.0 - u_hit) * 0.3, 0.0, 0.99)
    sin_th = np.clip(offset_frac * (0.5 + 0.5 * (ar - 1.0) / 1.5 + 0.5), 0.0, 0.999)
    tan_th = sin_th / np.sqrt(1.0 - sin_th ** 2)
    # Bite criterion: barb + friction defeat ricochet up to tan(theta) <= mu + bite
    glance = tan_th > (mu_fric + 0.60)

    # --- 3. Penetration --------------------------------------------------- #
    v_n = v_proj * np.sqrt(1.0 - sin_th ** 2)      # normal component
    sig_crush = CRUSH_OVER_SHEAR * sig_shear
    depth = 0.5 * M_PROJ_KG * v_n ** 2 / (sig_crush * A_TIP_M2)
    shallow = depth < BARB_DEPTH_REQ_M

    # --- 4. Anchor retention vs snatch load -------------------------------- #
    mu_red = (M_SC_KG * m_chunk) / (M_SC_KG + m_chunk)
    f_snatch = v_app * np.sqrt(k_tether * mu_red)
    capacity = sig_shear * A_ANCHOR_M2 * np.minimum(depth / BARB_DEPTH_REQ_M, 2.0)
    f_total = f_snatch + REEL_TENSION_FACTOR * capacity
    tear_out = f_total > capacity
    snap = f_total > f_tether_max

    # --- 5. Wrap race ------------------------------------------------------ #
    t_reel = STANDOFF_M / v_reel
    wrap_window = WRAP_FRACTION * np.pi / np.maximum(omega, 1e-9)
    wrap = t_reel > wrap_window

    # First-failure accounting
    mode = np.zeros(n_s, dtype=int)
    alive = ~miss
    mode[miss] = 1
    g = alive & glance;            mode[g] = 2;  alive &= ~glance
    s = alive & shallow;           mode[s] = 3;  alive &= ~shallow
    sn = alive & snap;             mode[sn] = 5; alive &= ~snap
    t = alive & tear_out;          mode[t] = 4;  alive &= ~tear_out
    w = alive & wrap;              mode[w] = 6;  alive &= ~wrap
    return alive, mode


MODE_NAMES = {0: "success", 1: "miss", 2: "glance", 3: "shallow_penetration",
              4: "tear_out", 5: "tether_snap", 6: "wrap_bind"}


def jansen_total_order(n_base: int = 8192, seed: int = RNG_SEED):
    """Total-order indices on P(success | epistemic axes) via expected-geometry chain."""
    rng = np.random.default_rng(seed)
    k = len(AXES)
    A = rng.random((n_base, k))
    B = rng.random((n_base, k))

    def f(u):
        ok, _ = capture_event(sample_axes(u), rng=None)
        return ok.astype(float)

    fA = f(A)
    var = fA.var(ddof=1)
    st = {}
    for i in range(k):
        ABi = A.copy()
        ABi[:, i] = B[:, i]
        st[NAMES[i]] = float(((fA - f(ABi)) ** 2).mean() / (2.0 * var)) if var > 0 else 0.0
    return st


def main():
    rng = np.random.default_rng(RNG_SEED)
    u = rng.random((N, len(AXES)))
    x = sample_axes(u)
    ok, mode = capture_event(x, rng=rng)

    p_capture = ok.mean()
    # Binomial-free posterior over the prior: per-sample Bernoulli outcome; report
    # the prior-predictive mean and a bootstrap interval over axis uncertainty.
    boot = []
    for _ in range(400):
        idx = rng.integers(0, N, N)
        boot.append(ok[idx].mean())
    q05, q50, q95 = np.quantile(boot, [0.05, 0.5, 0.95])

    fail_counts = {MODE_NAMES[m]: int((mode == m).sum()) for m in range(7)}
    n_fail = N - int(ok.sum())
    fail_share = {k: (v / n_fail if n_fail else 0.0)
                  for k, v in fail_counts.items() if k != "success"}

    print(f"Tier 1.5 harpoon capture probability: mean {p_capture:.3f} "
          f"(bootstrap [{q05:.3f}, {q95:.3f}])  vs Tier-1 closed-form median 0.365")
    print("failure-mode shares (of all failures):")
    for k_, v in sorted(fail_share.items(), key=lambda kv: -kv[1]):
        print(f"  {k_:>20s}: {v:.3f}  ({fail_counts[k_]} of {n_fail})")

    st = jansen_total_order()
    print("total-order sensitivity (expected-geometry chain), top 6:")
    for name, s in sorted(st.items(), key=lambda kv: -kv[1])[:6]:
        print(f"  {name:>22s}: {s:.3f}")

    # T15-H5 design corner: approach <= 1 cm/s, k <= 3e3 N/m, reel <= 3 cm/s
    corner = (x["approach_vel_cms"] <= 1.0) & (x["tether_stiffness_n_m"] <= 3e3) \
             & (x["reel_speed_cms"] <= 3.0)
    p_corner = ok[corner].mean() if corner.sum() > 200 else float("nan")
    print(f"design corner (n={int(corner.sum())}): P = {p_corner:.3f} "
          f"(gain {p_corner - p_capture:+.3f} vs overall)")

    # Conditional medians by mass decile for the coupling step
    mult = p_capture / 0.85

    out = {
        "p_capture_mean": float(p_capture),
        "bootstrap_ci": [float(q05), float(q95)],
        "tier1_median_ref": 0.365,
        "failure_shares": fail_share,
        "total_order_sensitivity": st,
        "design_corner_p": float(p_corner),
        "implied_capture_multiplier_vs_085": float(mult),
        "n": N, "seed": RNG_SEED,
    }
    (RESULTS / "tier15_results.json").write_text(json.dumps(out, indent=2))
    print(f"implied capture_efficiency_multiplier vs 0.85 anchor: {mult:.3f}")
    print(f"wrote {RESULTS / 'tier15_results.json'}")


if __name__ == "__main__":
    main()
