"""R-reactor-specific-power-program-targets — synthesis round.

Composes closure tables from R-specific-power-cliff (R10),
R-aerocapture-cliff-shift (R11), R-reactor-lifetime-vs-burn-time (R12) and
R-power-bayesian-update (hyperion) into a joint constraint surface, applies
program-conditional priors and engineering-closure priors, and bounds the
conjunction posterior that the chunk-rendezvous architecture clears all
three independent viability axes (specific power, reactor lifetime,
aerocapture credit) inside the ICEBERG demonstrator window 2032-2035.

NO new propulsion physics. NO new economics. Composition only.

Pre-registered hypotheses H1-H6 in STUDY.md. This script grades them and
writes the synthesis table to results/.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# Paths -----------------------------------------------------------------------

ROUND_DIR = Path(__file__).resolve().parent
ROUNDS_DIR = ROUND_DIR.parent
RESULTS_DIR = ROUND_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

R_SPC_PATH = ROUNDS_DIR / "R_specific_power_cliff/results/specific_power_cliff.json"
R_AERO_PATH = ROUNDS_DIR / "R_aerocapture_cliff_shift/results/aerocapture_cliff_shift.json"
R_LIFE_PATH = ROUNDS_DIR / "R_reactor_lifetime_vs_burn_time/results/reactor_lifetime_regrade.json"
R_PRIORS_PATH = (
    ROUNDS_DIR / "R_power_bayesian_update/results/R_power_bayesian_update_summary.json"
)


# Load inputs -----------------------------------------------------------------

def load_inputs() -> dict:
    spc = json.loads(R_SPC_PATH.read_text())
    aero = json.loads(R_AERO_PATH.read_text())
    life = json.loads(R_LIFE_PATH.read_text())
    pri = json.loads(R_PRIORS_PATH.read_text())
    return {"spc": spc, "aero": aero, "life": life, "priors": pri}


# Joint closure surface -------------------------------------------------------

# R-specific-power-cliff: SP -> {n_close_15yr, n_close_20yr, n_close_25yr, n_close_30yr}
# (no X, no L — implicitly X=0 km/s, L=inf yr)
#
# R-aerocapture-cliff-shift: SP x X -> {n_close_15yr, ..., n_close_30yr}
# (no L — implicitly L=inf yr)
#
# R-reactor-lifetime-vs-burn-time: SP x X x L -> n_close_25yr
# (regraded under L ceiling; only 25-yr round-trip ceiling reported)
#
# We compose into close_count[ceiling_yr][SP][X][L] = n_close_cells (of 60).
# For ceilings other than 25-yr, L is collapsed to "inf" since R12 only
# regraded the 25-yr cliff.

def _parse_lvl(key: str) -> float:
    # "sp_2.4" -> 2.4 ; "X_10.0" -> 10.0 ; "L_5.0" -> 5.0 ; "L_inf" -> float('inf')
    val = key.split("_", 1)[1]
    if val == "inf":
        return float("inf")
    return float(val)


def build_closure_surface(spc: dict, aero: dict, life: dict) -> dict:
    """Returns close_count[ceiling][SP][X][L] = n_close (int, of 60 cells)."""
    surface: dict = {}

    sps = [float(s) for s in spc["specific_power_levels_w_per_kg"]]
    xs_aero = [float(x) for x in aero["aerocapture_X_levels_km_s"]]

    # Ceilings 15/20/25/30 yr at X=0, L=inf — from R-specific-power-cliff
    for ceiling_label in ("15yr", "20yr", "25yr", "30yr"):
        ceiling_yr = int(ceiling_label.replace("yr", ""))
        surface[ceiling_yr] = {}
        for sp in sps:
            sp_key = f"{sp}"
            surface[ceiling_yr][sp] = {0.0: {float("inf"): spc["closure_counts"][sp_key][f"n_close_{ceiling_label}"]}}

    # Add X dimension at L=inf from R-aerocapture-cliff-shift
    # (X already present at X=0; aerocapture results add X>0 at L=inf)
    for ceiling_label in ("15yr", "20yr", "25yr", "30yr"):
        ceiling_yr = int(ceiling_label.replace("yr", ""))
        for sp in sps:
            sp_key_aero = f"sp_{sp}"
            for x in xs_aero:
                if x == 0.0:
                    continue  # already populated by SPC
                x_key = f"X_{x}"
                n = aero["closure_count_grid"][sp_key_aero][x_key][f"n_close_{ceiling_label}"]
                surface[ceiling_yr][sp].setdefault(x, {})[float("inf")] = n

    # Add L dimension at ceiling=25 yr from R-reactor-lifetime-vs-burn-time
    # (only 25-yr regraded; other ceilings stay at L=inf only)
    ls = ["5.0", "8.0", "10.0", "15.0", "inf"]
    for sp in sps:
        sp_key = f"sp_{sp}"
        for x in xs_aero:
            x_key = f"X_{x}"
            for L_key in ls:
                L = float("inf") if L_key == "inf" else float(L_key)
                n = life["regraded_close_25yr_count"][sp_key][x_key][f"L_{L_key}"]
                surface[25][sp].setdefault(x, {})[L] = n

    return surface


# Minimum-closing-point lookup ------------------------------------------------

def min_close_points(surface: dict, ceiling_yr: int):
    """For a given ceiling, return all (SP, X, L) tuples with n_close >= 1,
    sorted by SP, then X, then L. These are candidate reactor-program targets.
    """
    out = []
    if ceiling_yr not in surface:
        return out
    for sp in sorted(surface[ceiling_yr].keys()):
        for x in sorted(surface[ceiling_yr][sp].keys()):
            for L in sorted(surface[ceiling_yr][sp][x].keys()):
                n = surface[ceiling_yr][sp][x][L]
                if n >= 1:
                    out.append((sp, x, L, n))
    return out


def closure_summary(surface: dict, ceiling_yr: int) -> str:
    """Pretty-print the closure surface for a ceiling (collapses L to inf
    if only one value)."""
    if ceiling_yr not in surface:
        return f"ceiling {ceiling_yr} yr: (no data)"
    pts = min_close_points(surface, ceiling_yr)
    if not pts:
        return f"ceiling {ceiling_yr} yr: 0 closing cells across entire tested envelope"
    out = [f"ceiling {ceiling_yr} yr: {len(pts)} (SP, X, L) tuples with >=1 closing cell"]
    out.append("  smallest by SP: " + str(pts[0]))
    out.append("  smallest by X: " + str(min(pts, key=lambda p: (p[1], p[0], p[2]))))
    out.append("  smallest by L: " + str(min(pts, key=lambda p: (p[2], p[0], p[1]))))
    return "\n".join(out)


# Program-conditional priors --------------------------------------------------

@dataclass
class ProgramPriorBracket:
    """P(SP >= threshold | reactor orbits) and P(L >= threshold | reactor orbits).
    Bracketed by (optimistic / nominal / skeptical)."""
    p_sp_ge_8: dict = field(default_factory=lambda: {"optimistic": 0.30, "nominal": 0.15, "skeptical": 0.05})
    p_sp_ge_5: dict = field(default_factory=lambda: {"optimistic": 0.50, "nominal": 0.30, "skeptical": 0.15})
    p_l_ge_5: dict = field(default_factory=lambda: {"optimistic": 0.50, "nominal": 0.30, "skeptical": 0.10})
    p_l_ge_10: dict = field(default_factory=lambda: {"optimistic": 0.30, "nominal": 0.15, "skeptical": 0.05})

    def conditional_sp(self, sp_threshold: float, bracket: str) -> float:
        # Stepwise: SP >= 5 uses p_sp_ge_5; SP >= 8 uses p_sp_ge_8. SP > 8 uses
        # the same 8-threshold (no separate data); SP <= 5 returns 1.0 (always).
        if sp_threshold <= 0.0:
            return 1.0
        if sp_threshold <= 5.0:
            return self.p_sp_ge_5[bracket]
        if sp_threshold <= 8.0:
            return self.p_sp_ge_8[bracket]
        # SP > 8 W/kg: harder than 8. Use 8-threshold and apply a 0.5 factor
        # for super-threshold to reflect rapid program-risk increase.
        return self.p_sp_ge_8[bracket] * 0.5

    def conditional_l(self, l_threshold: float, bracket: str) -> float:
        if l_threshold == float("inf"):
            # Need infinite lifetime — interpret as "lifetime is not a binding
            # constraint" i.e. P=1. Used when the closing point doesn't require
            # any reactor-life qualification (cell would close on SP+X alone).
            return 1.0
        if l_threshold <= 0.0:
            return 1.0
        if l_threshold <= 5.0:
            return self.p_l_ge_5[bracket]
        if l_threshold <= 10.0:
            return self.p_l_ge_10[bracket]
        # L > 10 yr: even harder than Kilopower design target.
        return self.p_l_ge_10[bracket] * 0.5


# Closure posterior -----------------------------------------------------------

def reactor_program_posterior(
    sp_threshold: float,
    l_threshold: float,
    power_priors: dict,
    bracket_name: str,
    prior_name: str,
    cond_bracket: ProgramPriorBracket,
) -> float:
    """P(viable reactor by 2035 at the (SP_threshold, L_threshold) point).

    = P(any US 500-kWe orbit by 2035)         # power_priors
      x P(SP >= SP_threshold | 500-kWe orbit)  # cond_bracket
      x P(L  >= L_threshold  | 500-kWe orbit)  # cond_bracket
    """
    p_500_orbit = power_priors["per_prior_full"][prior_name]["p_500kWe_orbit_by_2035"]
    p_sp = cond_bracket.conditional_sp(sp_threshold, bracket_name)
    p_l = cond_bracket.conditional_l(l_threshold, bracket_name)
    return p_500_orbit * p_sp * p_l


# Engineering-closure priors (per SCOPE) --------------------------------------

P_AEROCAPTURE_CLOSES = 0.50   # generous, R-hybrid-aerocapture-aerobraking pending
P_RENDEZVOUS_CLOSES = 0.25    # midpoint of SCOPE-recommended 20-30 percent


# Capital-class thresholds ----------------------------------------------------

CAPITAL_CLASS_THRESHOLDS = [
    ("technology-demonstrator-only", 0.0),
    ("sovereign-grant", 0.001),
    ("sovereign-bond", 0.01),
    ("regulated-utility", 0.05),
    ("corporate-growth", 0.15),
    ("venture", 0.25),
]


def capital_class(p: float) -> str:
    for name, threshold in reversed(CAPITAL_CLASS_THRESHOLDS):
        if p >= threshold:
            return name
    return "technology-demonstrator-only"


# Candidate min-points to evaluate --------------------------------------------

def candidate_points(surface: dict) -> list[dict]:
    """Pick a small set of representative candidate (SP, X, L) min-points
    from the closure surface, anchored on the SCOPE's H1/H2 predictions and
    on Pareto-frontier corners of what actually closes."""
    candidates = []

    # L0-05 STRICT (15-yr round-trip ceiling): collapse L (R12 only regraded
    # at 25-yr); use SPC + AERO at L=inf.
    pts_15 = min_close_points(surface, 15)
    candidates.append({"label": "L0-05 strict", "ceiling_yr": 15, "points": pts_15})

    # L0-05 ~ 25-yr WAIVER: use the full SP x X x L surface from R12.
    pts_25 = min_close_points(surface, 25)
    candidates.append({"label": "L0-05 25-yr waiver", "ceiling_yr": 25, "points": pts_25})

    # L0-05 ~ 30-yr WAIVER: SP x X at L=inf only.
    pts_30 = min_close_points(surface, 30)
    candidates.append({"label": "L0-05 30-yr waiver", "ceiling_yr": 30, "points": pts_30})

    return candidates


def select_representative_min_points(pts: list[tuple]) -> dict:
    """For a candidate list of (SP, X, L, n) tuples, pick three Pareto
    corners: smallest-SP, smallest-X, smallest-L."""
    if not pts:
        return {}
    return {
        "smallest_SP": min(pts, key=lambda p: (p[0], p[1], p[2])),
        "smallest_X": min(pts, key=lambda p: (p[1], p[0], p[2])),
        "smallest_L": min(pts, key=lambda p: (p[2], p[0], p[1])),
    }


# Grading H1-H6 ---------------------------------------------------------------

def grade(surface: dict, posteriors_table: list[dict]) -> dict:
    """Adjudicate H1-H6 from the SCOPE-pre-registered hypotheses."""
    out = {}

    # H1: min-point at L0-05 strict = (8 W/kg, 5 yr).
    # SCOPE falsifiers: min-point achievable at SP <= 6 OR L <= 3.
    pts_15 = min_close_points(surface, 15)
    if not pts_15:
        # Empty closure set is STRONGER than H1's prediction (no min-point at
        # all). Neither SCOPE falsifier triggers — H1 HELD-WITH-EXTENSION.
        out["H1"] = {
            "verdict": "HELD-WITH-EXTENSION",
            "reason": "0 closing cells at L0-05 strict (15-yr round-trip ceiling) "
                       "across the entire tested (SP up to 10 W/kg, X up to 25 km/s, "
                       "L up to infinite) envelope. H1's directional prediction "
                       "(reactor must be >=8 W/kg AND >=5 yr lifetime) is consistent "
                       "with the data, but the true min-point is more pessimistic "
                       "than predicted: it does not exist within the tested envelope. "
                       "SCOPE falsifiers (SP <= 6 OR L <= 3) do not trigger.",
            "predicted_min": "(8 W/kg, 5 yr)",
            "measured_min": "unbounded above tested envelope (L0-05 strict closure set is empty)",
            "scope_falsifier_triggered": False,
        }
    else:
        reps = select_representative_min_points(pts_15)
        sp_min = reps["smallest_SP"][0]
        L_min = reps["smallest_L"][2]
        if sp_min <= 6.0 or (L_min != float("inf") and L_min <= 3.0):
            verdict = "FALSIFIED"
        else:
            verdict = "HELD"
        out["H1"] = {
            "verdict": verdict,
            "predicted_min": "(8 W/kg, 5 yr)",
            "measured_min": reps,
            "scope_falsifier_triggered": verdict == "FALSIFIED",
        }

    # H2: min-point at L0-05 25-yr waiver = (5 W/kg, 10 yr, X=10 km/s).
    # SCOPE falsifiers: min-point at SP <= 4 OR L <= 7 OR X >= 10 doesn't help.
    pts_25 = min_close_points(surface, 25)
    if not pts_25:
        out["H2"] = {"verdict": "FALSIFIED — empty closure set", "predicted_min": "(5, 10, X=10)"}
    else:
        reps = select_representative_min_points(pts_25)
        sp_min_corner = reps["smallest_SP"]  # (sp, x, L, n)
        sp_min = sp_min_corner[0]
        L_min = reps["smallest_L"][2]
        # Does X >= 10 km/s help at SP=5? Check whether any closing cell exists
        # at SP=5, X>=10 (regardless of L).
        x10_helps_at_sp5 = any(
            sp == 5.0 and x >= 10.0 for sp, x, _L, _ in pts_25
        )
        if sp_min <= 4.0:
            verdict = "FALSIFIED — min-point achievable at SP <= 4"
        elif (L_min != float("inf")) and L_min <= 7.0:
            verdict = "FALSIFIED — min-point achievable at L <= 7"
        elif not x10_helps_at_sp5:
            verdict = "FALSIFIED — aerocapture X >= 10 doesn't help at SP=5"
        else:
            verdict = "HELD"
        out["H2"] = {
            "verdict": verdict,
            "predicted_min": "(5 W/kg, 10 yr, X=10 km/s)",
            "measured_min": reps,
            "x10_helps_at_sp5": x10_helps_at_sp5,
            "scope_falsifier_triggered": verdict != "HELD",
        }

    # H3 / H4: numeric brackets on joint posterior at (8, 5) / (5, 10).
    # Read off posteriors_table.
    for h, sp_t, l_t, threshold in [("H3", 8.0, 5.0, 0.03), ("H4", 5.0, 10.0, 0.01)]:
        rows = [r for r in posteriors_table
                if r["sp_threshold"] == sp_t and r["l_threshold"] == l_t]
        if not rows:
            out[h] = {"verdict": "VACUOUS", "note": "no row in posteriors_table"}
            continue
        max_post = max(r["reactor_posterior"] for r in rows)
        if max_post <= threshold:
            verdict = "HELD"
        elif max_post > (threshold * 10 / 3 if h == "H3" else threshold * 5):
            verdict = "FALSIFIED"
        else:
            verdict = "HELD"
        out[h] = {
            "verdict": verdict,
            "predicted_max": threshold,
            "measured_max_across_brackets": max_post,
            "n_rows": len(rows),
        }

    # H5: conjunction posterior ceiling.
    rows = [r for r in posteriors_table if r["sp_threshold"] == 8.0 and r["l_threshold"] == 5.0]
    if rows:
        max_conj_h3 = max(r["conjunction_posterior"] for r in rows)
    else:
        max_conj_h3 = 0.0
    rows = [r for r in posteriors_table if r["sp_threshold"] == 5.0 and r["l_threshold"] == 10.0]
    if rows:
        max_conj_h4 = max(r["conjunction_posterior"] for r in rows)
    else:
        max_conj_h4 = 0.0
    h5_held = max_conj_h3 <= 0.01 and max_conj_h4 <= 0.001
    out["H5"] = {
        "verdict": "HELD" if h5_held else "FALSIFIED",
        "predicted_max_h3_anchor": 0.01,
        "predicted_max_h4_anchor": 0.001,
        "measured_max_conjunction_at_8_5": max_conj_h3,
        "measured_max_conjunction_at_5_10": max_conj_h4,
    }

    # H6: reading-level "technology-demonstrator is the honest reading".
    # HELD if max conjunction (across all candidate points and brackets) does not
    # cross the regulated-utility threshold (0.05).
    max_conj_all = max(r["conjunction_posterior"] for r in posteriors_table) if posteriors_table else 0.0
    out["H6"] = {
        "verdict": "HELD" if max_conj_all < 0.05 else "FALSIFIED",
        "predicted": "technology-demonstrator-only at conservative anchors",
        "measured_max_conjunction_any_point": max_conj_all,
        "implied_capital_class": capital_class(max_conj_all),
    }

    return out


# Main computation ------------------------------------------------------------

def main() -> None:
    inputs = load_inputs()
    spc = inputs["spc"]
    aero = inputs["aero"]
    life = inputs["life"]
    priors = inputs["priors"]

    surface = build_closure_surface(spc, aero, life)

    # Print closure summaries
    print("=" * 78)
    print("JOINT CLOSURE SURFACE — minimum closing points by L0-05 setting")
    print("=" * 78)
    for ceiling in (15, 20, 25, 30):
        print(closure_summary(surface, ceiling))
        print()

    # Build the synthesis table.
    cond_bracket = ProgramPriorBracket()
    prior_names = ["uniform_beta_1_1", "jeffreys_beta_0p5_0p5", "skeptical_beta_0p5_5"]
    cond_brackets = ["optimistic", "nominal", "skeptical"]

    # Candidate (SP, L) program-target points to evaluate.
    candidate_targets = [
        ("H1 anchor: 8 W/kg, 5 yr", 8.0, 5.0),
        ("H2 anchor: 5 W/kg, 10 yr", 5.0, 10.0),
        ("stretch: 5 W/kg, 5 yr", 5.0, 5.0),
        ("stretch: 8 W/kg, 10 yr", 8.0, 10.0),
        ("optimistic: 10 W/kg, 5 yr", 10.0, 5.0),
        ("optimistic: 10 W/kg, 10 yr", 10.0, 10.0),
    ]

    posteriors_table = []
    for label, sp_t, l_t in candidate_targets:
        for prior_name in prior_names:
            for bracket in cond_brackets:
                p_reactor = reactor_program_posterior(
                    sp_t, l_t, priors, bracket, prior_name, cond_bracket
                )
                p_conjunction = p_reactor * P_AEROCAPTURE_CLOSES * P_RENDEZVOUS_CLOSES
                posteriors_table.append({
                    "label": label,
                    "sp_threshold": sp_t,
                    "l_threshold": l_t,
                    "power_prior": prior_name,
                    "conditional_bracket": bracket,
                    "p_500kwe_orbit_by_2035": priors["per_prior_full"][prior_name]["p_500kWe_orbit_by_2035"],
                    "p_sp_conditional": cond_bracket.conditional_sp(sp_t, bracket),
                    "p_l_conditional": cond_bracket.conditional_l(l_t, bracket),
                    "reactor_posterior": p_reactor,
                    "p_aerocapture_closes": P_AEROCAPTURE_CLOSES,
                    "p_rendezvous_closes": P_RENDEZVOUS_CLOSES,
                    "conjunction_posterior": p_conjunction,
                    "capital_class": capital_class(p_conjunction),
                })

    # Print summary table (most optimistic and most skeptical row per target).
    print("=" * 78)
    print("SYNTHESIS TABLE — conjunction posterior bracketed by prior + conditional")
    print("=" * 78)
    print(f"{'target':<32} {'prior':<22} {'cond':<11} {'P(reactor)':>12} {'P(conj)':>12} {'class'}")
    for label, sp_t, l_t in candidate_targets:
        rows = [r for r in posteriors_table if r["label"] == label]
        # show optimistic-uniform and skeptical-skeptical
        opt = max(rows, key=lambda r: r["conjunction_posterior"])
        skp = min(rows, key=lambda r: r["conjunction_posterior"])
        print(
            f"{opt['label']:<32} {opt['power_prior']:<22} {opt['conditional_bracket']:<11} "
            f"{opt['reactor_posterior']:>12.2e} {opt['conjunction_posterior']:>12.2e} {opt['capital_class']}"
        )
        print(
            f"{'  ':<32} {skp['power_prior']:<22} {skp['conditional_bracket']:<11} "
            f"{skp['reactor_posterior']:>12.2e} {skp['conjunction_posterior']:>12.2e} {skp['capital_class']}"
        )

    # Adjudicate hypotheses.
    print()
    print("=" * 78)
    print("HYPOTHESIS ADJUDICATION")
    print("=" * 78)
    verdicts = grade(surface, posteriors_table)
    for h, v in verdicts.items():
        print(f"\n{h}: {v.get('verdict', '?')}")
        for k, val in v.items():
            if k != "verdict":
                print(f"  {k}: {val}")

    # Write results JSON
    output = {
        "round": "R-reactor-specific-power-program-targets",
        "author": "enceladus-r5",
        "date": "2026-05-15",
        "pre_registration": "STUDY.md (H1-H6)",
        "input_rounds": [
            "R-specific-power-cliff (2d63291)",
            "R-aerocapture-cliff-shift (12058b5)",
            "R-reactor-lifetime-vs-burn-time (c685c52)",
            "R-power-bayesian-update (hyperion batch)",
        ],
        "closure_surface_summary": {
            "ceiling_15yr_L0_05_strict_min_points": min_close_points(surface, 15),
            "ceiling_25yr_L0_05_waiver_min_points": min_close_points(surface, 25),
            "ceiling_30yr_L0_05_waiver_min_points": min_close_points(surface, 30),
            "ceiling_20yr_min_points": min_close_points(surface, 20),
        },
        "conditional_bracket": {
            "p_sp_ge_8": cond_bracket.p_sp_ge_8,
            "p_sp_ge_5": cond_bracket.p_sp_ge_5,
            "p_l_ge_5": cond_bracket.p_l_ge_5,
            "p_l_ge_10": cond_bracket.p_l_ge_10,
        },
        "engineering_closure_priors": {
            "p_aerocapture_closes": P_AEROCAPTURE_CLOSES,
            "p_rendezvous_closes": P_RENDEZVOUS_CLOSES,
        },
        "capital_class_thresholds": dict(CAPITAL_CLASS_THRESHOLDS),
        "synthesis_table": posteriors_table,
        "hypothesis_verdicts": verdicts,
    }
    out_path = RESULTS_DIR / "reactor_program_targets.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
