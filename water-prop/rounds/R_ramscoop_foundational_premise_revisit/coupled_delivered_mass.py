"""Coupled delivered-mass model for R-ramscoop-foundational-premise-revisit.

Reuses the R-chunk-capture-monte-carlo Tier-1 capture-probability posteriors and
couples them to the titan-2 R-conops-chunk-vs-ram-scoop chunk-fed return-Delta-v
bookkeeping in a single model. Answers: does ram-scoop's Tier-1 capture lead survive
the chunk-as-propellant-tank Delta-v penalty when both are carried together?

NO new Monte Carlo: the Tier-1 per-sample (chunk_mass, p_capture) pairs are
regenerated deterministically by replaying the seeded RNG of tier1_closed_form.py,
and the Delta-v stack is taken from titan-2 (not re-derived).

Output: results/coupled_results.json + console summary.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROUND_DIR = Path(__file__).parent
TIER1_DIR = ROUND_DIR.parent / "R_chunk_capture_monte_carlo"
TIER1_JSON = TIER1_DIR / "results" / "tier1_results.json"
TIER1_SCRIPT = TIER1_DIR / "tier1_closed_form.py"
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# --- Delta-v anchors (titan-2 R-conops-chunk-vs-ram-scoop; NOT re-derived) ---
ISP_S = 5000.0           # megawatt-electric specific impulse (titan-2)
G0 = 9.80665             # m/s^2
V_E_KMS = ISP_S * G0 / 1000.0   # exhaust velocity, km/s  (= 49.03 km/s)
DV_INBOUND = 24.7        # km/s interplanetary inbound continuous-thrust (shared)
DV_RESIDENCE_OUT = 7.4   # km/s ram-scoop residence-out increment

DV = {
    "harpoon":  DV_INBOUND,                      # single-chunk capture on a pass
    "ramscoop": DV_INBOUND + DV_RESIDENCE_OUT,   # circularise into B-ring + climb out
    "everting": DV_INBOUND,                       # single-chunk active enclosure (harpoon-class)
}

DRY_MASS_FIXED_T = 200.0   # titan-2 literal dry-mass anchor
DRY_RATIO = 1.0            # titan-2 ratio: 200 t dry per 200 t chunk

L0_04_FLOOR_T = 25.0       # commercial-class delivered-mass floor

# Published Tier-1 medians for the validation gate.
TIER1_MEDIAN_GATE = {"harpoon": 0.36540388732107376,
                     "ramscoop": 0.40494819135141424,
                     "everting": 0.2462997365251492}


# ---------------------------------------------------------------------------
# Replay the Tier-1 seeded RNG to recover per-sample (chunk_mass, p_capture).
# We must consume the RNG stream in the EXACT order tier1_closed_form.main()
# does: for each architecture, posterior-sampling draws first, then the Morris
# trajectories (which advance the stream before the next architecture).
# ---------------------------------------------------------------------------

def _load_tier1_module():
    spec = importlib.util.spec_from_file_location("tier1_closed_form", TIER1_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # register so frozen dataclass resolves its module
    spec.loader.exec_module(mod)
    return mod


def regenerate_tier1_samples() -> dict[str, dict[str, np.ndarray]]:
    """Return {arch: {'mass_t': array, 'p_capture': array}} matching the Tier-1 run."""
    t1 = _load_tier1_module()
    rng = np.random.default_rng(t1.RNG_SEED)
    out: dict[str, dict[str, np.ndarray]] = {}
    for arch in t1.ARCHITECTURES:
        cfg = t1.ARCHITECTURES[arch]
        # 1) posterior sampling: sample_axes draws rng.random(n) per axis, in order
        x = t1.sample_axes(cfg["axes"], t1.N_SAMPLES, rng)
        stages = cfg["stages"](x)
        joint = t1.joint_success(stages)
        out[arch] = {"mass_t": np.asarray(x["chunk_mass_t"]),
                     "p_capture": np.asarray(joint)}
        # 2) advance the stream exactly as main() does (Morris), so the next
        #    architecture's axis draws line up with the published run.
        t1.morris(arch, t1.MORRIS_R, rng)
    return out


# ---------------------------------------------------------------------------
# Coupled delivered-mass model.
# ---------------------------------------------------------------------------

def delivered_if_captured(mass_t: np.ndarray, arch: str, dry_mode: str) -> np.ndarray:
    """Net delivered mass (t) per successful capture, chunk-as-propellant-tank Tsiolkovsky."""
    dv = DV[arch]
    factor = np.exp(-dv / V_E_KMS)
    if dry_mode == "ratio":
        m_dry = DRY_RATIO * mass_t
    elif dry_mode == "fixed":
        m_dry = np.full_like(mass_t, DRY_MASS_FIXED_T)
    else:
        raise ValueError(dry_mode)
    m_final = (m_dry + mass_t) * factor
    return np.maximum(0.0, m_final - m_dry)


def eta_dv(arch: str, dry_mode: str, mass_t: float = 200.0) -> float:
    """Capture-referenced delivered fraction at a reference chunk mass."""
    d = delivered_if_captured(np.array([mass_t]), arch, dry_mode)[0]
    return float(d / mass_t)


def quantile_block(arr: np.ndarray) -> dict:
    q = np.quantile(arr, [0.05, 0.25, 0.5, 0.75, 0.95])
    return {"median": float(q[2]), "q05": float(q[0]), "q25": float(q[1]),
            "q75": float(q[3]), "q95": float(q[4]),
            "mean": float(arr.mean()), "std": float(arr.std()),
            "frac_positive": float((arr > 0).mean())}


def main():
    samples = regenerate_tier1_samples()

    # --- Validation gate: regenerated capture medians must match the published run ---
    gate = {}
    for arch, want in TIER1_MEDIAN_GATE.items():
        got = float(np.median(samples[arch]["p_capture"]))
        gate[arch] = {"published": want, "regenerated": got, "abs_err": abs(got - want)}
    max_err = max(g["abs_err"] for g in gate.values())
    if max_err > 1e-9:
        raise SystemExit(f"VALIDATION GATE FAILED: regenerated medians differ "
                         f"(max abs err {max_err:.3e}). Aborting.\n{json.dumps(gate, indent=2)}")

    results = {
        "round": "R-ramscoop-foundational-premise-revisit",
        "date": "2026-05-26",
        "inputs": {
            "tier1_json": str(TIER1_JSON.relative_to(ROUND_DIR.parent.parent.parent)),
            "v_e_kms": V_E_KMS, "isp_s": ISP_S,
            "dv_kms": DV, "dry_mass_fixed_t": DRY_MASS_FIXED_T, "dry_ratio": DRY_RATIO,
            "l0_04_floor_t": L0_04_FLOOR_T,
        },
        "validation_gate": {"max_abs_err": max_err, "per_arch": gate, "passed": True},
        "eta_dv_at_200t": {dm: {a: eta_dv(a, dm) for a in DV} for dm in ("ratio", "fixed")},
        "delivered_posteriors": {},
        "h4_by_chunk_decile": {},
    }

    archs = list(DV.keys())
    delivered = {dm: {} for dm in ("ratio", "fixed")}
    for dm in ("ratio", "fixed"):
        for a in archs:
            m = samples[a]["mass_t"]
            p = samples[a]["p_capture"]
            dlv = p * delivered_if_captured(m, a, dm)
            delivered[dm][a] = dlv
            results["delivered_posteriors"].setdefault(dm, {})[a] = quantile_block(dlv)

    # --- H4: winner by chunk-mass decile (use harpoon's mass grid as common axis) ---
    # All three architectures draw chunk_mass from the same log-uniform prior; compare
    # delivered_if_captured * p within matched chunk-mass bins. Use a shared mass grid
    # and evaluate the model deterministically (capture prob varies per sample, so we
    # report both the deterministic eta-only crossing and the sampled-median crossing).
    mass_grid = np.logspace(np.log10(10.0), np.log10(200.0), 40)
    for dm in ("ratio", "fixed"):
        rows = []
        for mt in mass_grid:
            # deterministic delivered-if-captured (capture-prob-free) winner
            di = {a: float(delivered_if_captured(np.array([mt]), a, dm)[0]) for a in archs}
            # expected delivered using each arch's MEDIAN capture prob (mass-agnostic median)
            ed = {a: di[a] * TIER1_MEDIAN_GATE[a] for a in archs}
            winner_det = max(di, key=di.get)
            winner_exp = max(ed, key=ed.get)
            rows.append({"mass_t": float(mt),
                         "delivered_if_captured": di,
                         "expected_delivered_at_median_p": ed,
                         "winner_deterministic": winner_det,
                         "winner_expected": winner_exp})
        winners = {r["winner_expected"] for r in rows}

        # Sample-binned decile cross-check: per chunk-mass decile, median delivered
        # mass per architecture from the actual (mass, p) samples. Directly tests
        # H4's "ram-scoop wins at large chunks" prediction with real numbers.
        edges = np.quantile(samples["harpoon"]["mass_t"], np.linspace(0, 1, 11))
        deciles = []
        for k in range(10):
            lo, hi = edges[k], edges[k + 1]
            row = {"chunk_mass_t_range": [float(lo), float(hi)], "median_delivered_t": {}}
            for a in archs:
                m = samples[a]["mass_t"]
                sel = (m >= lo) & (m < hi) if k < 9 else (m >= lo) & (m <= hi)
                row["median_delivered_t"][a] = float(np.median(delivered[dm][a][sel])) if sel.any() else None
            vals = {a: v for a, v in row["median_delivered_t"].items() if v is not None}
            row["winner"] = max(vals, key=vals.get) if vals else None
            deciles.append(row)

        results["h4_by_chunk_decile"][dm] = {
            "deterministic_grid": rows,
            "sampled_deciles": deciles,
            "unique_winners_expected": sorted(winners),
            "unique_winners_sampled_deciles": sorted({d["winner"] for d in deciles if d["winner"]}),
            "trade_is_chunk_mass_dependent": len(winners) > 1,
        }

    # --- Verdicts ---
    def med(dm, a):
        return results["delivered_posteriors"][dm][a]["median"]

    verdicts = {}
    for dm in ("ratio", "fixed"):
        h1_falsified = med(dm, "ramscoop") < med(dm, "harpoon")
        penalty = eta_dv("harpoon", dm) / eta_dv("ramscoop", dm)
        h2_held = 3.0 <= penalty <= 8.0
        best_med = max(med(dm, a) for a in archs)
        h3_held = best_med < L0_04_FLOOR_T
        h4_dependent = results["h4_by_chunk_decile"][dm]["trade_is_chunk_mass_dependent"]
        verdicts[dm] = {
            "H1_ramscoop_lead_survives": {"verdict": "FALSIFIED" if h1_falsified else "HELD",
                                          "ramscoop_median_t": med(dm, "ramscoop"),
                                          "harpoon_median_t": med(dm, "harpoon")},
            "H2_penalty_3x_to_8x": {"verdict": "HELD" if h2_held else "FALSIFIED",
                                    "relative_penalty_x": penalty},
            "H3_none_clears_25t": {"verdict": "HELD" if h3_held else "FALSIFIED",
                                   "best_architecture_median_t": best_med,
                                   "floor_t": L0_04_FLOOR_T},
            "H4_chunk_mass_dependent_trade": {"verdict": "HELD" if h4_dependent else "FALSIFIED",
                                              "unique_winners": results["h4_by_chunk_decile"][dm]["unique_winners_expected"]},
        }
    results["verdicts"] = verdicts

    out_path = RESULTS_DIR / "coupled_results.json"
    out_path.write_text(json.dumps(results, indent=2))

    # --- Console summary ---
    print(f"Wrote {out_path}")
    print(f"\nValidation gate: max abs err on Tier-1 medians = {max_err:.2e}  "
          f"({'PASS' if max_err <= 1e-9 else 'FAIL'})")
    print(f"\nv_e = {V_E_KMS:.2f} km/s   Delta-v: harpoon {DV['harpoon']} | "
          f"ramscoop {DV['ramscoop']} | everting {DV['everting']} km/s")
    print("\neta_dv (capture-referenced delivered fraction) at 200 t chunk:")
    for dm in ("ratio", "fixed"):
        line = "  ".join(f"{a}={eta_dv(a, dm)*100:5.2f}%" for a in archs)
        print(f"  [{dm:5s}] {line}   penalty(harpoon/ramscoop)={eta_dv('harpoon',dm)/eta_dv('ramscoop',dm):.2f}x")
    for dm in ("ratio", "fixed"):
        print(f"\n=== Delivered-mass posteriors [{dm} dry mass] ===")
        for a in archs:
            b = results["delivered_posteriors"][dm][a]
            print(f"  {a:9s}: median={b['median']:6.2f} t  90% CI=[{b['q05']:5.2f}, {b['q95']:6.2f}]  "
                  f"mean={b['mean']:6.2f}  frac>0={b['frac_positive']:.2f}")
        v = verdicts[dm]
        print(f"  H1 {v['H1_ramscoop_lead_survives']['verdict']:9s} "
              f"(ramscoop {v['H1_ramscoop_lead_survives']['ramscoop_median_t']:.2f} t vs "
              f"harpoon {v['H1_ramscoop_lead_survives']['harpoon_median_t']:.2f} t)")
        print(f"  H2 {v['H2_penalty_3x_to_8x']['verdict']:9s} (penalty {v['H2_penalty_3x_to_8x']['relative_penalty_x']:.2f}x)")
        print(f"  H3 {v['H3_none_clears_25t']['verdict']:9s} (best median {v['H3_none_clears_25t']['best_architecture_median_t']:.2f} t vs 25 t floor)")
        print(f"  H4 {v['H4_chunk_mass_dependent_trade']['verdict']:9s} (winners across chunk-mass range: {v['H4_chunk_mass_dependent_trade']['unique_winners']})")
        print(f"  H4 sampled-decile median delivered mass (t) by chunk-mass bin:")
        for d in results["h4_by_chunk_decile"][dm]["sampled_deciles"]:
            mt = d["median_delivered_t"]
            lo, hi = d["chunk_mass_t_range"]
            print(f"    [{lo:6.1f},{hi:6.1f}] t: harpoon={mt['harpoon']:5.2f} ramscoop={mt['ramscoop']:5.2f} "
                  f"everting={mt['everting']:5.2f} -> {d['winner']}")


if __name__ == "__main__":
    main()
