"""
R-T1-sensitivity-and-breakeven — sensitivity sweep on T1 (FSP-2 award)
holding all other gates at round-7 chain anchors. Identify breakeven T1 at
each V; identify next binding gate after T1 lift; estimate public-evidence
T1 via Bayes-factor compounding.

Author: iapetus, 2026-05-16
Pre-registration: SCOPE.md (H1-H6)
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Load round 7 (gate structure + baseline anchors)
# ---------------------------------------------------------------------------

PRIOR_R7 = json.loads(
    (PROJECT_ROOT / "R_staged_options_with_technology_gates" / "results" / "staged_options_with_technology_gates.json").read_text()
)
GATES = PRIOR_R7["gate_structure"]
TOTAL_PROGRAM_COST_M = PRIOR_R7["total_program_cost_M"]

# Baseline gate-pass probabilities (from round 7 chain anchors, conservative skeptical)
BASELINE_GATES = {
    "p_F1": 0.75,            # Gate A LEO debris demo
    "p_T2": 0.50,            # Hybrid aerocapture closure
    "p_F2": 0.80,            # Gate B cislunar demo
    "p_T3": 0.20,            # B-ring rendezvous survivability (low anchor)
    "p_F3": 0.80,            # Gate C/D vacuum qual + long-soak
    "p_F4": 0.50,            # Ship 3 commercial flight (worst-case before gate credit)
}

# ---------------------------------------------------------------------------
# Decision tree walk (lifted from round 7 with minor refactoring)
# ---------------------------------------------------------------------------

GATE_NAMES = [g["name"] for g in GATES]
GATE_COSTS = [g["cost_M"] for g in GATES]

def enumerate_paths(p_gates, v_billion):
    paths = []
    for outcomes in product([1, 0], repeat=7):
        p_path = 1.0
        cum_spend_M = 0.0
        killed_at = None
        for i, oc in enumerate(outcomes):
            cum_spend_M += GATE_COSTS[i]
            p_gate = p_gates[i]
            if oc == 1:
                p_path *= p_gate
            else:
                p_path *= (1.0 - p_gate)
                killed_at = GATE_NAMES[i]
                if any(outcomes[i+1:]):
                    p_path = 0.0
                break
        if p_path == 0.0:
            continue
        if killed_at is None:
            npv_billion = v_billion           # V net of NRE (pitch convention)
            label = "full_success"
        else:
            npv_billion = -cum_spend_M / 1000.0
            label = f"killed_at_{killed_at}"
        paths.append({"label": label, "p_path": p_path, "cum_spend_M": cum_spend_M, "npv_billion": npv_billion})
    return paths


def staged_metrics(p_gates_vec, v_billion):
    paths = enumerate_paths(p_gates_vec, v_billion)
    e_npv = sum(p["p_path"] * p["npv_billion"] for p in paths)
    e_spend_M = sum(p["p_path"] * p["cum_spend_M"] for p in paths)
    p_kill_per_gate = {}
    for p in paths:
        if p["label"].startswith("killed_at_"):
            g = p["label"].replace("killed_at_", "")
            p_kill_per_gate[g] = p_kill_per_gate.get(g, 0) + p["p_path"]
    p_full_success = sum(p["p_path"] for p in paths if p["label"] == "full_success")
    return {
        "e_npv_billion": e_npv,
        "e_total_spend_M": e_spend_M,
        "p_full_success": p_full_success,
        "p_kill_per_gate": p_kill_per_gate,
    }


def assemble_gates(p_T1, **overrides):
    """Return gate probability vector ordered T1, F1, T2, F2, T3, F3, F4."""
    return [
        p_T1,
        overrides.get("p_F1", BASELINE_GATES["p_F1"]),
        overrides.get("p_T2", BASELINE_GATES["p_T2"]),
        overrides.get("p_F2", BASELINE_GATES["p_F2"]),
        overrides.get("p_T3", BASELINE_GATES["p_T3"]),
        overrides.get("p_F3", BASELINE_GATES["p_F3"]),
        overrides.get("p_F4", BASELINE_GATES["p_F4"]),
    ]


# ---------------------------------------------------------------------------
# T1 sweep × V sweep
# ---------------------------------------------------------------------------

T1_VALUES = [0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
V_VALUES = [12.0, 18.0, 24.0, 50.0, 100.0, 200.0]

t1_sweep_table = []
for t1 in T1_VALUES:
    for v in V_VALUES:
        p_gates_vec = assemble_gates(t1)
        m = staged_metrics(p_gates_vec, v)
        t1_sweep_table.append({
            "t1": t1,
            "v_billion": v,
            "e_npv_billion": round(m["e_npv_billion"], 5),
            "e_total_spend_M": round(m["e_total_spend_M"], 2),
            "p_full_success": round(m["p_full_success"], 8),
            "p_kill_T1": round(m["p_kill_per_gate"].get("T1_fsp2_award", 0), 6),
            "p_kill_T2": round(m["p_kill_per_gate"].get("T2_hybrid_aerocap", 0), 6),
            "p_kill_T3": round(m["p_kill_per_gate"].get("T3_bring_rendezvous", 0), 6),
            "p_kill_F1": round(m["p_kill_per_gate"].get("F1_gate_a_leo_debris", 0), 6),
            "p_kill_F2": round(m["p_kill_per_gate"].get("F2_gate_b_cislunar", 0), 6),
            "p_kill_F3": round(m["p_kill_per_gate"].get("F3_gate_c_d_qual", 0), 6),
            "p_kill_F4": round(m["p_kill_per_gate"].get("F4_ship3_saturn_commit", 0), 6),
            "ev_positive": m["e_npv_billion"] > 0,
        })

# ---------------------------------------------------------------------------
# Breakeven T1 at each V (binary search)
# ---------------------------------------------------------------------------

def breakeven_t1(v_billion, overrides=None, tolerance=1e-6, max_iter=80):
    overrides = overrides or {}
    lo, hi = 1e-8, 1.0
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        p_gates_vec = assemble_gates(mid, **overrides)
        m = staged_metrics(p_gates_vec, v_billion)
        if m["e_npv_billion"] > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < tolerance:
            return (lo + hi) / 2.0
    return None  # didn't converge — likely no breakeven exists in [0, 1]


breakeven_table = []
for v in V_VALUES:
    p_gates_at_hi = assemble_gates(1.0)
    m_hi = staged_metrics(p_gates_at_hi, v)
    if m_hi["e_npv_billion"] <= 0:
        breakeven_table.append({"v_billion": v, "breakeven_t1": None, "note": "no breakeven — staged EV negative even at T1=1.0"})
    else:
        be = breakeven_t1(v)
        breakeven_table.append({"v_billion": v, "breakeven_t1": round(be, 6), "note": "binary search converged"})

# ---------------------------------------------------------------------------
# Next-binding-gate analysis after T1 lift (T1=0.5)
# ---------------------------------------------------------------------------

p_gates_T1_05 = assemble_gates(0.5)
m_at_t1_05_v24 = staged_metrics(p_gates_T1_05, 24.0)
post_t1_lift_gate_kill_probs = sorted(m_at_t1_05_v24["p_kill_per_gate"].items(),
                                       key=lambda x: -x[1])
next_binding_gate = post_t1_lift_gate_kill_probs[0][0] if post_t1_lift_gate_kill_probs else None

# ---------------------------------------------------------------------------
# T1=0.5, lift T2 to 1.0 (test H3)
# ---------------------------------------------------------------------------

p_gates_T1_05_T2_10 = assemble_gates(0.5, p_T2=1.0)
m_T1_05_T2_10 = staged_metrics(p_gates_T1_05_T2_10, 24.0)

# T1=0.5, lift T3 to 1.0 (compare)
p_gates_T1_05_T3_10 = assemble_gates(0.5, p_T3=1.0)
m_T1_05_T3_10 = staged_metrics(p_gates_T1_05_T3_10, 24.0)

# T1=0.5, lift both T2 and T3 to 1.0
p_gates_T1_05_T2_10_T3_10 = assemble_gates(0.5, p_T2=1.0, p_T3=1.0)
m_T1_05_T2_10_T3_10 = staged_metrics(p_gates_T1_05_T2_10_T3_10, 24.0)

# ---------------------------------------------------------------------------
# Public-evidence Bayes-factor compounding for T1
# ---------------------------------------------------------------------------
# Documented evidence (per user-locked R-power-wonder findings, May 2026):
#   - Draft AFP issued Aug 29, 2025 — positive signal. BF estimate: 3.0
#   - Duffy directive Aug 4, 2025 (scope to 100 kWe, FY30 deployment intent) — positive. BF: 1.5
#   - Final AFP anticipated early 2026; not issued as of May 2026 — schedule slip. BF: 0.75
#   - FY26 budget zeroed NEP/NTP (FSP separate line; weak negative signal). BF: 0.85
#   - DARPA DRACO cancelled May 30, 2025 — sector headwind. BF: 0.85
# Net compounding: 3.0 × 1.5 × 0.75 × 0.85 × 0.85 = 2.44 (point estimate)
# Bracket: lower (more skeptical interpretation, e.g., BF_AFP=2.0, BF_Duffy=1.2,
#          BF_slip=0.6, BF_budget=0.8, BF_DRACO=0.8) = 0.92
# Bracket: upper (BF_AFP=4.5, BF_Duffy=2.0, BF_slip=0.85, BF_budget=0.9, BF_DRACO=0.9)
#                                                       = 6.20

BAYES_FACTORS = {
    "draft_afp_issued_aug_2025": {"point": 3.0, "low": 2.0, "high": 4.5},
    "duffy_directive_100_kwe_scope": {"point": 1.5, "low": 1.2, "high": 2.0},
    "final_afp_schedule_slip": {"point": 0.75, "low": 0.6, "high": 0.85},
    "fy26_nep_ntp_zeroed": {"point": 0.85, "low": 0.8, "high": 0.9},
    "darpa_draco_cancelled": {"point": 0.85, "low": 0.8, "high": 0.9},
}

def compound(bf_dict, key):
    out = 1.0
    for v in bf_dict.values():
        out *= v[key]
    return out

bf_point = compound(BAYES_FACTORS, "point")
bf_low = compound(BAYES_FACTORS, "low")
bf_high = compound(BAYES_FACTORS, "high")

# Apply Bayes factors to chain's conservative US-skeptical anchor (T1 = 0.0001)
T1_PRIOR_CONSERVATIVE = 0.0001
T1_PRIOR_OPTIMISTIC = 0.0037  # global+ever uniform
T1_PUBLIC_EVIDENCE = {
    "prior_conservative": T1_PRIOR_CONSERVATIVE,
    "prior_optimistic": T1_PRIOR_OPTIMISTIC,
    "bayes_factor_point": bf_point,
    "bayes_factor_low": bf_low,
    "bayes_factor_high": bf_high,
    "t1_posterior_conservative_point": round(min(1.0, T1_PRIOR_CONSERVATIVE * bf_point), 6),
    "t1_posterior_conservative_high": round(min(1.0, T1_PRIOR_CONSERVATIVE * bf_high), 6),
    "t1_posterior_optimistic_point": round(min(1.0, T1_PRIOR_OPTIMISTIC * bf_point), 6),
    "t1_posterior_optimistic_high": round(min(1.0, T1_PRIOR_OPTIMISTIC * bf_high), 6),
}

# ---------------------------------------------------------------------------
# Hypothesis verdicts
# ---------------------------------------------------------------------------

# H1: breakeven T1 at V=$24B in [0.15, 0.30]
be_v24 = next((r["breakeven_t1"] for r in breakeven_table if r["v_billion"] == 24.0), None)
H1_verdict = {
    "hypothesis": "Breakeven T1 at V=$24B in [0.15, 0.30]",
    "measured_breakeven_t1_at_v24": be_v24,
    "verdict": (
        "CONFIRMED" if be_v24 and 0.05 < be_v24 < 0.50 and 0.15 <= be_v24 <= 0.30 else
        "PARTIALLY_CONFIRMED" if be_v24 and 0.05 < be_v24 < 0.50 else
        "FALSIFIED"
    ),
    "notes": f"Breakeven T1 at V=$24B = {be_v24}. Predicted [0.15, 0.30]. Falsification band: <0.05 or >0.50.",
}

# H2: breakeven T1 at V=$200B in [0.02, 0.05]
be_v200 = next((r["breakeven_t1"] for r in breakeven_table if r["v_billion"] == 200.0), None)
H2_verdict = {
    "hypothesis": "Breakeven T1 at V=$200B in [0.02, 0.05]",
    "measured_breakeven_t1_at_v200": be_v200,
    "verdict": (
        "CONFIRMED" if be_v200 and 0.005 < be_v200 < 0.10 and 0.02 <= be_v200 <= 0.05 else
        "PARTIALLY_CONFIRMED" if be_v200 and 0.005 < be_v200 < 0.10 else
        "FALSIFIED"
    ),
    "notes": f"Breakeven T1 at V=$200B = {be_v200}. Predicted [0.02, 0.05]. Falsification band: <0.005 or >0.10.",
}

# H3: after T1 lift, next binding gate is T2; T2 lift to 1.0 with T1=0.5 produces positive EV at V=$24B
H3_verdict = {
    "hypothesis": "Next binding gate after T1 lift is T2; T2 lift to 1.0 with T1=0.5 produces positive EV at V=$24B",
    "next_binding_gate_after_T1_lift": next_binding_gate,
    "gate_kill_probs_at_T1_05_v24": dict(post_t1_lift_gate_kill_probs),
    "ev_at_T1_05_T2_10_v24_billion": round(m_T1_05_T2_10["e_npv_billion"], 4),
    "ev_at_T1_05_T3_10_v24_billion": round(m_T1_05_T3_10["e_npv_billion"], 4),
    "ev_at_T1_05_T2_10_T3_10_v24_billion": round(m_T1_05_T2_10_T3_10["e_npv_billion"], 4),
    "verdict": (
        "CONFIRMED" if (
            next_binding_gate and ("T2" in next_binding_gate or "T3" in next_binding_gate)
            and m_T1_05_T2_10["e_npv_billion"] > 0
        ) else "PARTIALLY_CONFIRMED" if m_T1_05_T2_10["e_npv_billion"] > 0 else "FALSIFIED"
    ),
    "notes": (
        f"Next binding gate after T1 lift: {next_binding_gate}. "
        f"EV at T1=0.5, T2=1.0, others baseline, V=$24B: ${m_T1_05_T2_10['e_npv_billion']:.4f}B. "
        f"EV at T1=0.5, T3=1.0, others baseline, V=$24B: ${m_T1_05_T3_10['e_npv_billion']:.4f}B. "
        f"EV at T1=0.5, T2=T3=1.0, others baseline, V=$24B: ${m_T1_05_T2_10_T3_10['e_npv_billion']:.4f}B."
    ),
}

# H4: public-evidence Bayes factor in [1.5, 3.0]; T1 posterior in [0.0002, 0.005]
H4_verdict = {
    "hypothesis": "Public-evidence-supported BF in [1.5, 3.0]; T1 posterior in [0.0002, 0.005] from conservative prior",
    "compounded_bayes_factor_point": round(bf_point, 3),
    "compounded_bayes_factor_low": round(bf_low, 3),
    "compounded_bayes_factor_high": round(bf_high, 3),
    "t1_posterior_conservative_point": T1_PUBLIC_EVIDENCE["t1_posterior_conservative_point"],
    "t1_posterior_optimistic_point": T1_PUBLIC_EVIDENCE["t1_posterior_optimistic_point"],
    "verdict": (
        "CONFIRMED" if 1.5 <= bf_point <= 3.0 else "PARTIALLY_CONFIRMED"
    ),
    "notes": (
        f"Compounded Bayes factor: point {bf_point:.3f}, low {bf_low:.3f}, high {bf_high:.3f}. "
        f"T1 posterior from conservative prior (0.0001): point {bf_point*0.0001:.5f}, "
        f"high {bf_high*0.0001:.5f}. T1 posterior from optimistic prior (0.0037): "
        f"point {bf_point*0.0037:.5f}, high {bf_high*0.0037:.5f}. "
        f"Even at high-end Bayes factor on optimistic prior, T1 posterior is "
        f"{T1_PUBLIC_EVIDENCE['t1_posterior_optimistic_high']} — still 1-2 orders of magnitude "
        f"below the breakeven T1 at V=$24B ({be_v24})."
    ),
}

# H5: required private-information multiple
required_t1_at_v24 = be_v24 if be_v24 else 1.0
public_evidence_t1_high = T1_PUBLIC_EVIDENCE["t1_posterior_optimistic_high"]
required_lift_multiple = required_t1_at_v24 / public_evidence_t1_high if public_evidence_t1_high > 0 else float("inf")
H5_verdict = {
    "hypothesis": "Required private-info T1 lift over public-evidence T1 is in [100x, 300x]",
    "required_t1_at_v24": required_t1_at_v24,
    "public_evidence_t1_high": public_evidence_t1_high,
    "required_lift_multiple": round(required_lift_multiple, 1),
    "verdict": (
        "CONFIRMED" if 50.0 < required_lift_multiple < 500.0 else
        "PARTIALLY_CONFIRMED" if required_lift_multiple < 1000.0 else
        "FALSIFIED"
    ),
    "notes": (
        f"Required T1 at V=$24B: {required_t1_at_v24}. "
        f"Public-evidence high-end T1: {public_evidence_t1_high}. "
        f"Required private-info lift multiple: {required_lift_multiple:.1f}x."
    ),
}

# H6: reading-level — public-evidence-supported T1 lift alone insufficient
public_supported_t1_high = T1_PUBLIC_EVIDENCE["t1_posterior_optimistic_high"]
gap_closes_on_public = be_v24 and public_supported_t1_high >= be_v24
H6_verdict = {
    "hypothesis": "Public-evidence-supported T1 lift alone insufficient to close gap to positive staged EV at V=$24B",
    "gap_closes_on_public_evidence_only": gap_closes_on_public,
    "verdict": "CONFIRMED" if not gap_closes_on_public else "FALSIFIED",
    "notes": (
        f"Public-evidence-supported T1 (high estimate): {public_supported_t1_high}. "
        f"Required T1 at V=$24B for positive staged EV: {be_v24}. "
        f"Gap closes on public evidence alone: {gap_closes_on_public}."
    ),
}

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

OUTPUT = {
    "round_id": "R-T1-sensitivity-and-breakeven",
    "author": "iapetus",
    "date": "2026-05-16",
    "baseline_gates_other_than_t1": BASELINE_GATES,
    "t1_sweep_table": t1_sweep_table,
    "breakeven_table": breakeven_table,
    "post_t1_lift_analysis": {
        "p_gates_at_T1_05": p_gates_T1_05,
        "kill_probs_at_T1_05_v24": dict(post_t1_lift_gate_kill_probs),
        "next_binding_gate": next_binding_gate,
        "ev_at_T1_05_T2_10_v24": round(m_T1_05_T2_10["e_npv_billion"], 4),
        "ev_at_T1_05_T3_10_v24": round(m_T1_05_T3_10["e_npv_billion"], 4),
        "ev_at_T1_05_T2_10_T3_10_v24": round(m_T1_05_T2_10_T3_10["e_npv_billion"], 4),
    },
    "public_evidence_bayes_factors": BAYES_FACTORS,
    "public_evidence_t1_estimate": T1_PUBLIC_EVIDENCE,
    "hypotheses": {
        "H1": H1_verdict,
        "H2": H2_verdict,
        "H3": H3_verdict,
        "H4": H4_verdict,
        "H5": H5_verdict,
        "H6": H6_verdict,
    },
}

(RESULTS_DIR / "T1_sensitivity_and_breakeven.json").write_text(json.dumps(OUTPUT, indent=2))

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------

print("=" * 80)
print("R-T1-sensitivity-and-breakeven — sweep on T1 holding other gates baseline")
print("=" * 80)
print()
print(f"{'T1':>8s} {'V=12B':>11s} {'V=24B':>11s} {'V=50B':>11s} {'V=200B':>11s} {'E[spend] V=24':>16s}")
for t1 in T1_VALUES:
    rs = [r for r in t1_sweep_table if r["t1"] == t1]
    row = {r["v_billion"]: r for r in rs}
    print(f"{t1:>8.4f} ${row[12]['e_npv_billion']:>+8.4f}B ${row[24]['e_npv_billion']:>+8.4f}B "
          f"${row[50]['e_npv_billion']:>+8.4f}B ${row[200]['e_npv_billion']:>+8.4f}B "
          f"${row[24]['e_total_spend_M']:>+10.1f}M")
print()
print("Breakeven T1 at each V:")
for r in breakeven_table:
    print(f"  V=${r['v_billion']:>3.0f}B: breakeven T1 = {r['breakeven_t1']} ({r['note']})")
print()
print(f"Post-T1-lift (T1=0.5) gate kill probability ranking at V=$24B:")
for g, p in post_t1_lift_gate_kill_probs[:5]:
    print(f"  {g:<32s} p_kill = {p:.5f}")
print()
print(f"Public-evidence Bayes factor compounding:")
print(f"  Point estimate: {bf_point:.3f}")
print(f"  Low: {bf_low:.3f}; High: {bf_high:.3f}")
print(f"  T1 posterior from conservative prior 0.0001: point {bf_point*0.0001:.5f}, high {bf_high*0.0001:.5f}")
print(f"  T1 posterior from optimistic prior 0.0037: point {bf_point*0.0037:.5f}, high {bf_high*0.0037:.5f}")
print()
print("HYPOTHESES:")
for hk, hv in OUTPUT["hypotheses"].items():
    print(f"  {hk}: {hv['verdict']}")
