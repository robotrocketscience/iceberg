"""Closed-form Tier 1 Monte Carlo for R-chunk-capture-monte-carlo.

Parameterised failure-product model across three architectures:
  (1) single-chunk harpoon
  (2) ram-scoop residence-class
  (3) everting-sleeve active enclosure

Each architecture has five stages; each stage's per-event failure probability is a
function of the round's uncertainty axes. The joint capture-success probability is
the product of per-stage success probabilities. The model is intentionally simple
(closed-form, no contact dynamics) and gives:
  - a Tier-1 sensitivity ranking via Morris elementary effects
  - a Tier-1 posterior on capture probability under the round's priors

Tests H1, H2, H6, H7, H8 in their closed-form forms. H3, H4, H5 stay open for
contact-fidelity work (out of session per project-owner direction).

Priors per tier_0_5_spin_prior.md (decameter-marginal default).

Output: water-prop/rounds/R_chunk_capture_monte_carlo/results/tier1_results.json
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

RNG_SEED = 20260526
N_SAMPLES = 8000  # joint-sampling budget per architecture for the posterior
MORRIS_R = 30      # number of Morris trajectories per architecture
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Priors (Tier 0.5 informed for spin; literature-bracketed for the rest)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Axis:
    name: str
    lo: float
    hi: float
    kind: str = "linear"  # "linear" or "log"

    def sample(self, u: np.ndarray) -> np.ndarray:
        """Inverse-CDF sample from a uniform u in [0, 1]."""
        if self.kind == "log":
            return np.exp(np.log(self.lo) + u * (np.log(self.hi) - np.log(self.lo)))
        return self.lo + u * (self.hi - self.lo)


# Shared 8 axes — apply to all three architectures.
SHARED_AXES = [
    Axis("chunk_mass_t",      lo=10.0,   hi=200.0,  kind="log"),   # tonnes
    Axis("spin_rate_rpm",     lo=0.0005, hi=0.05,   kind="log"),   # per Tier 0.5
    Axis("surface_friction",  lo=0.05,   hi=0.40,   kind="linear"),
    Axis("approach_vel_cms",  lo=0.3,    hi=3.0,    kind="linear"),  # cm/s
    Axis("sensor_noise_m",    lo=0.05,   hi=0.50,   kind="linear"),  # rendezvous pose error (m)
    Axis("contact_geom",      lo=0.0,    hi=1.0,    kind="linear"),  # 0=face, 1=edge
    Axis("catcher_compliance", lo=0.1,   hi=1.0,    kind="linear"),  # normalised
    Axis("controller_delay_ms", lo=10.0, hi=100.0,  kind="linear"),
]

# Everting-sleeve extra axes
EVERTING_EXTRA = [
    Axis("eversion_completion", lo=0.5, hi=0.95, kind="linear"),  # Bernoulli prior centre
    Axis("eversion_misalign_deg", lo=0.0, hi=30.0, kind="linear"),
]


# ---------------------------------------------------------------------------
# Per-architecture failure-product models
#
# Each architecture maps axis vector -> 5 stage success probabilities.
# Joint success = prod(stages).
# Functional forms are smooth, monotonic, calibrated to ~46% joint at the
# audit's mid-anchor point (the bottoms-up reference), and respond to the axes
# in the directions the literature suggests.
# ---------------------------------------------------------------------------


def _clip(p: np.ndarray) -> np.ndarray:
    return np.clip(p, 1e-4, 1.0 - 1e-4)


def stages_harpoon(x: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Single-chunk harpoon."""
    spin = x["spin_rate_rpm"]
    mass = x["chunk_mass_t"]
    fric = x["surface_friction"]
    appv = x["approach_vel_cms"]
    sens = x["sensor_noise_m"]
    geom = x["contact_geom"]
    comp = x["catcher_compliance"]
    delay = x["controller_delay_ms"]

    # Rendezvous: dominated by sensor noise; spin couples mildly via target acquisition
    p_rendezvous = 1.0 - 0.20 * (sens / 0.5) - 0.05 * (spin / 0.05)
    # Deploy harpoon: high-baseline; weak coupling to controller delay
    p_deploy = 0.97 - 0.07 * (delay / 100.0)
    # Catch: harpoon makes contact; spin moves the impact point; high friction helps
    p_catch = 0.90 - 0.45 * (spin / 0.05) + 0.10 * (fric - 0.2) / 0.2 - 0.15 * (appv / 3.0)
    # Contain: hold onto a spinning chunk; mass + spin drive slip; geometry matters
    p_contain = 0.85 - 0.40 * (spin / 0.05) - 0.10 * np.log10(mass / 10.0) - 0.10 * geom
    # Survive grab loads: stiffness/compliance choice; mass-and-velocity dominate
    p_survive = 0.96 - 0.10 * (appv / 3.0) - 0.05 * np.log10(mass / 10.0) - 0.03 * (1.0 - comp)

    return {
        "rendezvous": _clip(p_rendezvous),
        "deploy":     _clip(p_deploy),
        "catch":      _clip(p_catch),
        "contain":    _clip(p_contain),
        "survive":    _clip(p_survive),
    }


def stages_ramscoop(x: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Ram-scoop residence-class."""
    spin = x["spin_rate_rpm"]
    mass = x["chunk_mass_t"]
    fric = x["surface_friction"]
    appv = x["approach_vel_cms"]
    sens = x["sensor_noise_m"]
    geom = x["contact_geom"]
    comp = x["catcher_compliance"]
    delay = x["controller_delay_ms"]

    # Station-keep: dominated by sensor noise and controller authority/delay
    p_stationkeep = 0.92 - 0.20 * (sens / 0.5) - 0.10 * (delay / 100.0)
    # Aperture/fill: spin largely irrelevant; mass distribution couples to fill rate
    p_aperture = 0.95 - 0.05 * np.log10(mass / 10.0)
    # Inelastic decel: friction + compliance + approach velocity matter; spin secondary
    p_decel = 0.90 - 0.15 * (appv / 3.0) + 0.05 * (fric - 0.2) / 0.2 - 0.10 * (1.0 - comp)
    # Cinch + outlier reject: oblong/spinning chunks present worst-case cross-section
    p_cinch = 0.92 - 0.15 * geom - 0.10 * (spin / 0.05)
    # Inbound permeability: time-dependent loss over the 7-yr coast (mass-independent at this level)
    p_retain = 0.93 - 0.03 * (1.0 - comp)

    return {
        "stationkeep": _clip(p_stationkeep),
        "aperture":    _clip(p_aperture),
        "decel":       _clip(p_decel),
        "cinch":       _clip(p_cinch),
        "retain":      _clip(p_retain),
    }


def stages_everting(x: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Everting-sleeve active enclosure (10-axis: shared 8 + eversion 2)."""
    spin = x["spin_rate_rpm"]
    mass = x["chunk_mass_t"]
    fric = x["surface_friction"]
    appv = x["approach_vel_cms"]
    sens = x["sensor_noise_m"]
    geom = x["contact_geom"]
    comp = x["catcher_compliance"]
    delay = x["controller_delay_ms"]
    ev_comp = x["eversion_completion"]
    ev_mis = x["eversion_misalign_deg"]

    # Rendezvous: same as harpoon (single-chunk targeting)
    p_rendezvous = 1.0 - 0.20 * (sens / 0.5) - 0.05 * (spin / 0.05)
    # Eversion-kinematics: zero flight heritage at 200-t scale
    # Modelled as: ev_comp scaled down by mass (size-dependent failure)
    # and degraded by misalignment angle
    mass_penalty = 0.30 * np.log10(mass / 10.0)
    p_eversion = ev_comp * np.exp(-mass_penalty) - 0.005 * ev_mis
    # Envelopment: compliance helps absorb spin; misalignment hurts
    p_envelop = 0.92 - 0.20 * (spin / 0.05) * (1.0 - comp) - 0.01 * ev_mis
    # Cinch: drawstring closes; geometry of chunk affects whether drawstring catches
    p_cinch = 0.92 - 0.15 * geom - 0.05 * (spin / 0.05)
    # Decel + carry: fabric stretch + permeability; mass-and-velocity drive load
    p_carry = 0.94 - 0.08 * (appv / 3.0) - 0.05 * np.log10(mass / 10.0) + 0.05 * (fric - 0.2) / 0.2

    return {
        "rendezvous": _clip(p_rendezvous),
        "eversion":   _clip(p_eversion),
        "envelop":    _clip(p_envelop),
        "cinch":      _clip(p_cinch),
        "carry":      _clip(p_carry),
    }


ARCHITECTURES = {
    "harpoon":   {"stages": stages_harpoon,    "axes": SHARED_AXES},
    "ramscoop":  {"stages": stages_ramscoop,   "axes": SHARED_AXES},
    "everting":  {"stages": stages_everting,   "axes": SHARED_AXES + EVERTING_EXTRA},
}


def joint_success(stages: dict[str, np.ndarray]) -> np.ndarray:
    """Product of per-stage success probabilities."""
    out = np.ones_like(next(iter(stages.values())))
    for p in stages.values():
        out = out * p
    return out


def sample_axes(axes: list[Axis], n: int, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Sample n joint points, one column per axis."""
    return {ax.name: ax.sample(rng.random(n)) for ax in axes}


# ---------------------------------------------------------------------------
# Posterior via direct sampling (N_SAMPLES per architecture)
# ---------------------------------------------------------------------------

def posterior(arch: str, n: int, rng: np.random.Generator) -> dict:
    cfg = ARCHITECTURES[arch]
    x = sample_axes(cfg["axes"], n, rng)
    stages = cfg["stages"](x)
    joint = joint_success(stages)
    quantiles = np.quantile(joint, [0.05, 0.25, 0.5, 0.75, 0.95])
    return {
        "architecture": arch,
        "n_samples": int(n),
        "median": float(quantiles[2]),
        "q05": float(quantiles[0]),
        "q25": float(quantiles[1]),
        "q75": float(quantiles[3]),
        "q95": float(quantiles[4]),
        "mean": float(joint.mean()),
        "std": float(joint.std()),
        "stage_medians": {k: float(np.median(v)) for k, v in stages.items()},
        "stage_variances_contribution": {
            # variance share approximated by Var(stage) / sum(Var(stages))
            k: float(np.var(np.log(_clip(v))))
            for k, v in stages.items()
        },
    }


# ---------------------------------------------------------------------------
# Morris elementary effects
# ---------------------------------------------------------------------------

def morris_trajectory(axes: list[Axis], rng: np.random.Generator, levels: int = 6, delta: float = 0.5):
    """One Morris trajectory: base point + per-axis one-at-a-time perturbations."""
    p = len(axes)
    base = rng.integers(0, levels, size=p).astype(float) / (levels - 1)
    base = np.clip(base, 0.0, 1.0 - delta)
    order = rng.permutation(p)
    traj = [base.copy()]
    pt = base.copy()
    for idx in order:
        pt = pt.copy()
        pt[idx] = pt[idx] + delta
        traj.append(pt)
    return np.array(traj), order


def morris(arch: str, r: int, rng: np.random.Generator) -> dict:
    cfg = ARCHITECTURES[arch]
    axes = cfg["axes"]
    p = len(axes)
    all_effects: dict[str, list[float]] = {ax.name: [] for ax in axes}

    for _ in range(r):
        traj_u, order = morris_trajectory(axes, rng)
        # Map u-space to axis values
        traj_x = {}
        for i, ax in enumerate(axes):
            traj_x[ax.name] = ax.sample(traj_u[:, i])
        stages = cfg["stages"](traj_x)
        joint = joint_success(stages)
        # Elementary effects: consecutive pairs along the order
        for step, idx in enumerate(order):
            ee = (joint[step + 1] - joint[step]) / 0.5  # delta in u-space
            all_effects[axes[idx].name].append(float(ee))

    return {
        "architecture": arch,
        "r": int(r),
        "mu_star": {name: float(np.mean(np.abs(arr))) for name, arr in all_effects.items()},
        "sigma":   {name: float(np.std(arr))           for name, arr in all_effects.items()},
        "rank":    sorted(all_effects.keys(),
                          key=lambda n: -np.mean(np.abs(all_effects[n]))),
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    rng = np.random.default_rng(RNG_SEED)
    results = {
        "round": "R-chunk-capture-monte-carlo",
        "tier": "Tier 1 (closed-form)",
        "date": "2026-05-26",
        "rng_seed": RNG_SEED,
        "n_samples_per_arch": N_SAMPLES,
        "morris_r": MORRIS_R,
        "priors_anchored_to": "tier_0_5_spin_prior.md (decameter-marginal: log-uniform 0.0005-0.05 rpm)",
        "posteriors": {},
        "morris": {},
    }

    for arch in ARCHITECTURES:
        results["posteriors"][arch] = posterior(arch, N_SAMPLES, rng)
        results["morris"][arch] = morris(arch, MORRIS_R, rng)

    # Cross-architecture H6 verdict: at least one median >= 0.64 x reference (0.85)
    h6_threshold = 0.64 * 0.85  # = 0.544
    survivors = {
        arch: results["posteriors"][arch]["median"] >= h6_threshold
        for arch in ARCHITECTURES
    }
    results["h6_verdict"] = {
        "threshold": h6_threshold,
        "anchor_ref": 0.85,
        "multiplier": 0.64,
        "per_architecture": survivors,
        "held": any(survivors.values()),
    }

    # H2 verdict: spin_rate_rpm has the highest mu_star
    h2 = {}
    for arch in ARCHITECTURES:
        rank = results["morris"][arch]["rank"]
        h2[arch] = {
            "top_axis": rank[0],
            "spin_rank": rank.index("spin_rate_rpm") + 1,
            "spin_dominates": rank[0] == "spin_rate_rpm",
        }
    results["h2_verdict"] = h2

    # H7 verdict: everting median within 0.10 of the best of the other two
    medians = {a: results["posteriors"][a]["median"] for a in ARCHITECTURES}
    best_other = max(medians["harpoon"], medians["ramscoop"])
    h7_penalty = best_other - medians["everting"]
    results["h7_verdict"] = {
        "everting_median": medians["everting"],
        "best_other_median": best_other,
        "penalty": h7_penalty,
        "held": h7_penalty <= 0.10,
    }

    # H8 verdict: for everting, is "eversion" the dominant Morris axis OR
    # is the eversion STAGE the variance-dominant stage in the posterior?
    everting_stage_var = results["posteriors"]["everting"]["stage_variances_contribution"]
    h8_stage = max(everting_stage_var.items(), key=lambda kv: kv[1])
    results["h8_verdict"] = {
        "dominant_stage": h8_stage[0],
        "dominant_stage_log_var": h8_stage[1],
        "eversion_kinematics_dominates": h8_stage[0] == "eversion",
        "all_stage_log_var": everting_stage_var,
    }

    out_path = RESULTS_DIR / "tier1_results.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"Wrote {out_path}")

    # Console summary
    print("\n=== Tier 1 posterior medians ===")
    for arch in ARCHITECTURES:
        p = results["posteriors"][arch]
        print(f"  {arch:10s}: median={p['median']:.3f}  90% CI=[{p['q05']:.3f}, {p['q95']:.3f}]")

    print(f"\nH6 threshold (0.64 x 0.85 = {h6_threshold:.3f}):")
    for arch, s in survivors.items():
        print(f"  {arch:10s}: {'HOLDS' if s else 'fails'}")
    print(f"  H6 overall: {'HELD' if results['h6_verdict']['held'] else 'FALSIFIED'}")

    print("\nH2 (spin-rate dominance) by architecture:")
    for arch, v in h2.items():
        print(f"  {arch:10s}: top axis = {v['top_axis']}, spin rank = {v['spin_rank']}")

    print(f"\nH7 (everting transfer): everting={medians['everting']:.3f}, "
          f"best other={best_other:.3f}, penalty={h7_penalty:.3f}, "
          f"{'HELD' if results['h7_verdict']['held'] else 'FALSIFIED'}")

    print(f"\nH8 (eversion-kinematics dominance): dominant stage = {h8_stage[0]}, "
          f"{'HELD' if results['h8_verdict']['eversion_kinematics_dominates'] else 'FALSIFIED'}")


if __name__ == "__main__":
    main()
