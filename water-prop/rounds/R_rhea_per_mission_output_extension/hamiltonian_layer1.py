"""Hamiltonian Layer 1 (regime diagnostics) over the 100 per-sample cumulative-NPV
trajectories emitted by R-heterogeneous-cadence run.py --emit-trajectories.

Implements the /decision-framework:hamiltonian Layer 1 algorithm (Steps 1-5) in code
so it can run in batch over 100 trajectories rather than 100 manual skill invocations.
Linear q-space (NPV is additive and crosses zero, per skill caveat 5).

Per skill spec (~/.claude/commands/decision-framework/hamiltonian.md):
  q_t = value_t - value_0
  dq/dt = q_t - q_{t-1};  T_t = 0.5 (dq/dt)^2;  V_t = -q_t;  H_t = T_t + V_t
  regime thresholds theta_T, theta_V = medians of T, |V| across steps
  conservation: slope of OLS H_t ~ t  (<-0.1 DISSIPATIVE, >+0.1 ENERGY-INJECTING)
  sustainability = sum(gain in ACCUMULATION steps) / sum(gain in profitable steps)

Output: results/hamiltonian_layer1_per_sample.json
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

ROUND_DIR = Path(__file__).parent
TRAJ_PATH = ROUND_DIR.parent / "R_heterogeneous_cadence" / "results" / "per_sample_trajectories.json"
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def ols_slope(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else 0.0


def classify_regime(T: float, V_abs: float, theta_T: float, theta_V: float) -> str:
    hi_T = T >= theta_T
    hi_V = V_abs >= theta_V
    if hi_T and not hi_V:
        return "MOMENTUM"
    if not hi_T and hi_V:
        return "ACCUMULATION"
    if hi_T and hi_V:
        return "TRANSITION"
    return "QUIESCENT"


def layer1(values: list[float]) -> dict:
    """Layer 1 regime diagnostics on a single cumulative-NPV trajectory."""
    v0 = values[0]
    q = [v - v0 for v in values]
    steps = []
    for t in range(1, len(q)):
        dq = q[t] - q[t - 1]
        T = 0.5 * dq * dq
        V = -q[t]
        steps.append({"t": t, "value": values[t], "q": q[t], "dq": dq,
                      "T": T, "V": V, "H": T + V,
                      "gain": values[t] - values[t - 1]})
    if not steps:
        return {"n_steps": 0, "sustainability_ratio": None, "sustainability_label": "N/A",
                "conservation_slope": None, "conservation_label": "N/A", "regime_fractions": {}}

    theta_T = statistics.median(s["T"] for s in steps)
    theta_V = statistics.median(abs(s["V"]) for s in steps)
    for s in steps:
        s["regime"] = classify_regime(s["T"], abs(s["V"]), theta_T, theta_V)

    # conservation
    slope = ols_slope([s["t"] for s in steps], [s["H"] for s in steps])
    cons_label = ("DISSIPATIVE" if slope < -0.1 else
                  "ENERGY-INJECTING" if slope > 0.1 else "APPROXIMATELY CONSERVED")

    # sustainability
    profitable = [s for s in steps if s["gain"] > 0]
    accum = [s for s in profitable if s["regime"] == "ACCUMULATION"]
    sum_prof = sum(s["gain"] for s in profitable)
    if sum_prof > 0:
        ratio = sum(s["gain"] for s in accum) / sum_prof
        sus_label = ("STABLE" if ratio >= 0.60 else
                     "MOMENTUM-DEPENDENT" if ratio < 0.30 else "MIXED")
    else:
        ratio = None
        sus_label = "NO-GAINS"  # monotonic-decline trajectory (NPV-negative, cost-dominated)

    n = len(steps)
    regimes = ["MOMENTUM", "ACCUMULATION", "TRANSITION", "QUIESCENT"]
    frac = {r: sum(1 for s in steps if s["regime"] == r) / n for r in regimes}
    transitions = sum(1 for i in range(1, n) if steps[i]["regime"] != steps[i - 1]["regime"])

    return {"n_steps": n, "sustainability_ratio": ratio, "sustainability_label": sus_label,
            "conservation_slope": slope, "conservation_label": cons_label,
            "regime_fractions": frac, "regime_transitions": transitions,
            "theta_T": theta_T, "theta_V": theta_V}


def auc(scores: list[float], labels: list[int]) -> float:
    """AUC via the Mann-Whitney rank statistic. labels: 1=positive outcome."""
    pos = [s for s, l in zip(scores, labels) if l == 1]
    neg = [s for s, l in zip(scores, labels) if l == 0]
    if not pos or not neg:
        return float("nan")
    wins = sum((sp > sn) + 0.5 * (sp == sn) for sp in pos for sn in neg)
    return wins / (len(pos) * len(neg))


def main():
    data = json.loads(TRAJ_PATH.read_text())
    trajs = data["trajectories"]

    per_sample = []
    for tr in trajs:
        l1 = layer1(tr["per_mission_cumulative_npv_M_usd"])
        per_sample.append({
            "sample_id": tr["sample_id"],
            "cadence_class": tr["cadence_class"],
            "regime": tr["regime"],
            "clearing_per_kg": tr["clearing_per_kg"],
            "final_program_npv_M_usd": tr["final_program_npv_M_usd"],
            "npv_positive": tr["final_program_npv_M_usd"] > 0,
            **l1,
        })

    def summarize(records: list[dict]) -> dict:
        n = len(records)
        defined = [r for r in records if r["sustainability_ratio"] is not None]
        labels = {}
        for lab in ("STABLE", "MIXED", "MOMENTUM-DEPENDENT", "NO-GAINS"):
            labels[lab] = sum(1 for r in records if r["sustainability_label"] == lab)
        cons = {}
        for lab in ("DISSIPATIVE", "APPROXIMATELY CONSERVED", "ENERGY-INJECTING"):
            cons[lab] = sum(1 for r in records if r["conservation_label"] == lab)
        npv_pos = sum(1 for r in records if r["npv_positive"])
        return {
            "n": n,
            "n_npv_positive": npv_pos,
            "pct_npv_positive": 100.0 * npv_pos / n if n else 0.0,
            "sustainability_labels": labels,
            "pct_momentum_dependent": 100.0 * labels["MOMENTUM-DEPENDENT"] / n if n else 0.0,
            "pct_stable": 100.0 * labels["STABLE"] / n if n else 0.0,
            "pct_no_gains": 100.0 * labels["NO-GAINS"] / n if n else 0.0,
            "conservation_labels": cons,
            "median_sustainability_defined": (statistics.median(r["sustainability_ratio"] for r in defined)
                                              if defined else None),
            "median_conservation_slope": statistics.median(r["conservation_slope"] for r in records),
        }

    het = [r for r in per_sample if r["cadence_class"] == "het"]
    hom = [r for r in per_sample if r["cadence_class"] == "hom"]
    het_s, hom_s = summarize(het), summarize(hom)
    all_s = summarize(per_sample)

    # H4: conservation slope predicts NPV-positive outcome. DISSIPATIVE (more negative
    # slope) should track winning -> score = -slope.
    scores = [-r["conservation_slope"] for r in per_sample]
    labels = [1 if r["npv_positive"] else 0 for r in per_sample]
    h4_auc = auc(scores, labels)

    # --- Verdicts ---
    momentum_all = all_s["pct_momentum_dependent"]
    h2 = "HELD" if 25.0 <= momentum_all <= 50.0 else "FALSIFIED"
    h3_gap = het_s["pct_momentum_dependent"] - hom_s["pct_momentum_dependent"]
    h3 = "HELD" if 5.0 <= h3_gap <= 20.0 else "FALSIFIED"
    h4 = "HELD" if (h4_auc == h4_auc and h4_auc > 0.7) else "FALSIFIED"  # NaN-safe
    h6 = "HELD" if h3 == "HELD" else "FALSIFIED"

    out = {
        "round": "R-rhea-per-mission-output-extension",
        "source": str(TRAJ_PATH.name),
        "method": "hamiltonian Layer 1 (skill Steps 1-5), linear q-space, batch over 100 trajectories",
        "aggregate": {"all": all_s, "het": het_s, "hom": hom_s},
        "h4_auc_conservation_predicts_npv_positive": h4_auc,
        "verdicts": {
            "H2_25_to_50pct_momentum_dependent": {"verdict": h2, "pct_momentum_dependent_all": momentum_all},
            "H3_het_higher_momentum_than_hom": {"verdict": h3, "gap_pp": h3_gap,
                                                "het_pct": het_s["pct_momentum_dependent"],
                                                "hom_pct": hom_s["pct_momentum_dependent"]},
            "H4_conservation_predicts_outcome_auc_gt_0.7": {"verdict": h4, "auc": h4_auc},
            "H6_het_concentration_driven": {"verdict": h6, "note": "tracks H3"},
        },
        "per_sample": per_sample,
    }
    out_path = RESULTS_DIR / "hamiltonian_layer1_per_sample.json"
    out_path.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {out_path}")

    print(f"\nTrajectory lengths: het N={het[0]['n_steps']+1}, hom N={hom[0]['n_steps']+1} (missions)")
    for name, s in (("ALL", all_s), ("het", het_s), ("hom", hom_s)):
        print(f"\n[{name}] n={s['n']}  NPV+={s['pct_npv_positive']:.1f}%")
        print(f"   sustainability: STABLE {s['sustainability_labels']['STABLE']}  "
              f"MIXED {s['sustainability_labels']['MIXED']}  "
              f"MOMENTUM-DEP {s['sustainability_labels']['MOMENTUM-DEPENDENT']}  "
              f"NO-GAINS {s['sustainability_labels']['NO-GAINS']}")
        print(f"   conservation: {s['conservation_labels']}")
        print(f"   median sustainability (defined)={s['median_sustainability_defined']}  "
              f"median H-slope={s['median_conservation_slope']:.3f}")
    print(f"\nH2 {h2}  (all MOMENTUM-DEP {momentum_all:.1f}%, band 25-50%)")
    print(f"H3 {h3}  (het {het_s['pct_momentum_dependent']:.1f}% - hom {hom_s['pct_momentum_dependent']:.1f}% "
          f"= {h3_gap:+.1f}pp, band +5..+20pp)")
    print(f"H4 {h4}  (AUC conservation->NPV+ = {h4_auc:.3f}, band >0.7)")
    print(f"H6 {h6}  (tracks H3)")


if __name__ == "__main__":
    main()
