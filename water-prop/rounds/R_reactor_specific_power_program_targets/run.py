"""
R-reactor-specific-power-program-targets — synthesis round.

Composes four prior closure tables (R-arch-E-specific-power-flown-anchored,
R-specific-power-cliff, R-aerocapture-cliff-shift, R-reactor-lifetime-vs-burn-time)
with R-power-bayesian-update's three-prior FSP posterior to produce joint
posterior probabilities on "any cell restored in matrix" under each candidate
reactor-program profile + engineering-closure conjunction.

No new propulsion physics. Re-uses enceladus-r5 closure_verdict counts.

Author: iapetus, 2026-05-15 (latest+9)
Pre-registration: STUDY.md (H1-H6)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROUNDS = Path(__file__).resolve().parent.parent
RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(exist_ok=True)


def load_json(rel: str) -> dict[str, Any]:
    with open(ROUNDS / rel) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 1. Load inputs
# ---------------------------------------------------------------------------

sp_cliff = load_json("R_specific_power_cliff/results/specific_power_cliff.json")
aero_cliff = load_json("R_aerocapture_cliff_shift/results/aerocapture_cliff_shift.json")
lifetime = load_json("R_reactor_lifetime_vs_burn_time/results/reactor_lifetime_regrade.json")
bayes = load_json("R_power_bayesian_update/results/R_power_bayesian_update_summary.json")

# ---------------------------------------------------------------------------
# 2. Build min-point search over (sp, X, L) joint grid
#
# The R-reactor-lifetime-vs-burn-time regraded grid already overlays all three
# axes. It reports the count of cells that survive close_25yr AND lifetime gate
# for each (sp, X, L) triple. We search for minimum survival points along each
# axis.
# ---------------------------------------------------------------------------

regrade = lifetime["regraded_close_25yr_count"]
sp_levels = lifetime["specific_power_levels_w_per_kg"]    # [2.4, 5, 6, 7, 8, 9, 10]
X_levels = lifetime["aerocapture_X_levels_km_s"]          # [0, 5, 10, 15, 20, 25]
L_levels = lifetime["lifetime_ceilings_yr"]               # ["5.0", "8.0", "10.0", "15.0", "inf"]

# strict L0-05 close (≤20-yr round-trip ceiling) is NOT in this table — that table
# uses close_25yr. R-specific-power-cliff confirms zero close_20yr cells anywhere
# in the tested grid up to sp=10 W/kg → L0-05 strict is UNREACHABLE within tested
# specific-power range. We document this in the synthesis but compute waiver-only.

# For each (sp, X, L) triple, count is regrade[f"sp_{sp}"][f"X_{X}"][f"L_{L}"]

def count_at(sp: float, X: float, L: str) -> int:
    return regrade[f"sp_{sp}"][f"X_{X:.1f}"][f"L_{L}"]


# Closure verdict at L0-05 strict (close_20yr): all zero from sp_cliff
sp_cliff_strict_close_20yr = {
    sp: sp_cliff["closure_counts"][str(sp)]["n_close_20yr"]
    for sp in sp_levels
}
l0_05_strict_unreachable = all(v == 0 for v in sp_cliff_strict_close_20yr.values())

# Find minimum (sp, X, L) point where ≥1 cell closes at L0-05 ≥25-yr waiver
min_points = []
for sp in sp_levels:
    for X in X_levels:
        for L in L_levels:
            c = count_at(sp, X, L)
            if c > 0:
                min_points.append((sp, X, L, c))

# Minimum along each axis
min_sp_overall = min(p[0] for p in min_points) if min_points else None
min_L_overall = None  # need to map "L_5.0" etc to numeric

def L_num(s: str) -> float:
    return float("inf") if s == "inf" else float(s)

min_L_overall = min(L_num(p[2]) for p in min_points) if min_points else None
min_X_overall = min(p[1] for p in min_points) if min_points else None

# ---------------------------------------------------------------------------
# 3. Identify lowest reactor-program-targets points
#
# We want the *floor* of the reactor program target. The closure surface is
# monotone: more sp, more L, more X all help. So the floor is at the corners.
# Find the (sp, L) corner with smallest sp at each candidate aerocapture credit.
# ---------------------------------------------------------------------------

# At X=0 (no aerocapture), find min sp such that L=10, 15, inf has ≥1 cell.
min_sp_at_X_for_L = {}
for X in X_levels:
    for L in L_levels:
        for sp in sp_levels:
            if count_at(sp, X, L) > 0:
                min_sp_at_X_for_L[(X, L)] = sp
                break
        else:
            min_sp_at_X_for_L[(X, L)] = None  # no closure at any sp tested

# Corner candidates: report the smallest sp at each (X, L) pair
corners = []
for (X, L), sp in sorted(min_sp_at_X_for_L.items()):
    if sp is not None:
        c = count_at(sp, X, L)
        corners.append({
            "X_km_s": X,
            "L_yr": L_num(L) if L != "inf" else "inf",
            "min_sp_w_per_kg": sp,
            "cell_count_at_min": c,
        })

# ---------------------------------------------------------------------------
# 4. Bayesian conjunction
#
# Anchor on R-power-bayesian-update three-prior bracket:
#   p_fsp_orbit_by_2035: 0.0292 / 0.0493 / 0.0892 (skeptical / jeffreys / uniform)
#
# The Bayesian-update round already conditions on scope via
#   p_500kWe_funded_given_fsp = 0.6
#   p_megawatt_funded_given_fsp = 0.45
#
# We need to ALSO condition on (specific power ≥ S_min, lifetime ≥ L_min). These
# conditionals are subjective — anchored on FSP-1 design spec and Kilopower
# heritage. Document the priors transparently.
#
# p(sp ≥ S_min | orbit, scope 500 kWe):
#   FSP-1 design target ~4-6 W/kg system-level (stretch 6); Kilopower target
#   2.4 W/kg flown. National Academies 2021: "very little advancement" in NEP
#   specific power in past decade. KRUSTY 2.4 W/kg flown anchor.
#   Subjective bracket:
# ---------------------------------------------------------------------------

p_sp_geq_given_orbit_500kWe = {
    5.0: 0.40,   # 5 W/kg is FSP-1 stretch-territory, somewhat plausible
    6.0: 0.25,   # 6 W/kg is FSP-1 stretch ceiling
    7.0: 0.15,   # above current design spec, requires program lift
    8.0: 0.08,   # 3x KRUSTY heritage, significant program risk
    9.0: 0.04,
    10.0: 0.02,  # 4x KRUSTY heritage, near-paper-study territory
}

# p(L ≥ L_min | orbit, scope 500 kWe, sp ≥ S_min):
#   FSP design target 10-15 yr cumulative; KRUSTY 28-hr ground test, no flight
#   heritage on cumulative full-power burn. Treat as independent of sp.
p_L_geq_given_orbit_500kWe = {
    5.0: 0.80,   # 5 yr ≈ Brayton-flight-rated minimum, low bar
    8.0: 0.55,
    10.0: 0.40,  # Kilopower design target — at design spec
    15.0: 0.15,  # 50% above design spec, lift required
    float("inf"): 1.0,  # nominally always satisfied (degenerate case)
}

# Conjunction with the two engineering rounds (per SCOPE):
P_HYBRID_AEROCAP = 0.50            # R-hybrid-aerocapture-aerobraking SCOPE-pending
P_RENDEZVOUS_LOW = 0.20            # R-bring-rendezvous-survivability pessimistic
P_RENDEZVOUS_HI  = 0.30            # optimistic

# Reactor-orbit-with-scope joint posteriors from Bayesian update
# These already condition orbit on scope-500-kWe via the p_500kWe_funded_given_fsp factor
p_500kWe_orbit_by_2035 = {
    "skeptical": bayes["per_prior_full"]["skeptical_beta_0p5_5"]["p_500kWe_orbit_by_2035"],
    "jeffreys": bayes["per_prior_full"]["jeffreys_beta_0p5_0p5"]["p_500kWe_orbit_by_2035"],
    "uniform": bayes["per_prior_full"]["uniform_beta_1_1"]["p_500kWe_orbit_by_2035"],
}

# ---------------------------------------------------------------------------
# 5. Compute joint posteriors at each corner
# ---------------------------------------------------------------------------

# We need an aerocapture-credit prior. R-hybrid-aerocapture-aerobraking is a
# binary SCOPE round (closes or not), but its closure level matters. We assume:
#   - if it closes, baseline credit X = 10 km/s (conservative interpretation)
#   - higher X (15, 20, 25) treated as outside reasonable single-pass envelope
# So the aerocapture conditional is:
#   p(X ≥ 10 | hybrid_closes) = 1.0 (assumption: if it closes at all, ≥10 is the
#                                    nominal target per matrix)
#   p(X ≥ 15) = 0.40 (stretch — beyond conservative hybrid skirt closure)
#   p(X ≥ 20) = 0.15 (further stretch)
#   p(X ≥ 25) = 0.05 (paper-study)
p_X_geq_given_hybrid_closes = {
    0.0: 1.0,   # always
    5.0: 0.90,
    10.0: 0.70,  # conservative hybrid closure envelope
    15.0: 0.30,
    20.0: 0.10,
    25.0: 0.03,
}

# The aerocapture round itself only matters if X > 0
# When evaluating X = 0 corner, hybrid round is not needed (no aerocapture credit)
# When evaluating X > 0 corner, must multiply by P_HYBRID_AEROCAP * p_X_geq

def joint_posterior(sp: float, X: float, L_str: str, prior: str, rendezvous_prior: float) -> dict[str, float]:
    p_orbit_500kWe = p_500kWe_orbit_by_2035[prior]
    p_sp = p_sp_geq_given_orbit_500kWe[sp]
    L_key = L_num(L_str) if L_str != "inf" else float("inf")
    p_L = p_L_geq_given_orbit_500kWe[L_key]
    if X > 0:
        p_aero = P_HYBRID_AEROCAP * p_X_geq_given_hybrid_closes[X]
    else:
        p_aero = 1.0  # no aerocapture conditional needed
    p_rend = rendezvous_prior
    # joint
    return {
        "p_reactor_with_sp_and_L_and_scope": p_orbit_500kWe * p_sp * p_L,
        "p_reactor_x_aerocap": p_orbit_500kWe * p_sp * p_L * p_aero,
        "p_full_conjunction": p_orbit_500kWe * p_sp * p_L * p_aero * p_rend,
    }


# Build the synthesis table — one row per minimum corner
synthesis_rows = []
for c in corners:
    X = c["X_km_s"]
    L = str(c["L_yr"]).replace(".0", ".0") if c["L_yr"] != "inf" else "inf"
    # Map back to dict key format
    if c["L_yr"] == "inf":
        L_key = "inf"
    elif c["L_yr"] == 5.0:
        L_key = "5.0"
    elif c["L_yr"] == 8.0:
        L_key = "8.0"
    elif c["L_yr"] == 10.0:
        L_key = "10.0"
    elif c["L_yr"] == 15.0:
        L_key = "15.0"
    else:
        L_key = str(c["L_yr"])
    sp = c["min_sp_w_per_kg"]

    row: dict[str, Any] = {
        "min_sp_w_per_kg": sp,
        "aerocapture_X_km_s": X,
        "lifetime_L_yr": c["L_yr"],
        "cell_count": c["cell_count_at_min"],
    }
    for prior in ("skeptical", "jeffreys", "uniform"):
        for rend_label, rend in (("rend_low", P_RENDEZVOUS_LOW), ("rend_hi", P_RENDEZVOUS_HI)):
            j = joint_posterior(sp, X, L_key, prior, rend)
            row[f"{prior}_{rend_label}_p_full"] = j["p_full_conjunction"]
            row[f"{prior}_{rend_label}_p_reactor_only"] = j["p_reactor_with_sp_and_L_and_scope"]
    synthesis_rows.append(row)


# ---------------------------------------------------------------------------
# 6. Capital-class thresholds
#
# Joint conjunction posteriors fall into program-class thresholds:
#   - corporate-growth / venture: requires ≥10%  (typical VC risk envelope)
#   - regulated-utility:          requires ≥50%  (utility procurement)
#   - sovereign-bond:             requires ≥80%  (sovereign-grade certainty)
#   - sovereign-grant / techdemo: any positive    (research-grade prior OK)
# ---------------------------------------------------------------------------

CAPITAL_CLASSES = [
    ("technology_demonstrator", 0.0),  # any positive posterior
    ("venture",                 0.10),
    ("corporate_growth",        0.30),
    ("regulated_utility",       0.50),
    ("sovereign_bond",          0.80),
]


def capital_class(p: float) -> str:
    last = "infeasible"
    for name, threshold in CAPITAL_CLASSES:
        if p >= threshold:
            last = name
    return last


# For each row, tag capital class under each (prior, rend) combination
for row in synthesis_rows:
    for prior in ("skeptical", "jeffreys", "uniform"):
        for rend_label in ("rend_low", "rend_hi"):
            p = row[f"{prior}_{rend_label}_p_full"]
            row[f"{prior}_{rend_label}_capital_class"] = capital_class(p)


# ---------------------------------------------------------------------------
# 7. Hypotheses adjudication
# ---------------------------------------------------------------------------

# H1: L0-05 strict min-point at sp≥8 AND L≥5 yr
# Closure verdict at L0-05 strict (close_20yr): all zero from sp_cliff (confirmed)
# → H1 FALSIFIED: L0-05 strict is unreachable within tested sp range up to 10 W/kg.

h1_verdict = {
    "hypothesis": "Min-point at L0-05 strict (close_20yr): sp≥8 AND L≥5 yr",
    "predicted_min_point": {"sp_w_per_kg": 8.0, "L_yr": 5.0},
    "measured": {
        "close_20yr_counts_by_sp": sp_cliff_strict_close_20yr,
        "any_closure_at_strict_in_tested_range": not l0_05_strict_unreachable,
    },
    "verdict": "FALSIFIED — but on the strict side: L0-05 strict unreachable up to sp=10 W/kg in tested grid. The hypothesis itself is misspecified — there is no min-point in tested range.",
}

# H2: min-point at L0-05 waiver + aerocap-10 km/s: sp≥5 AND L≥10 yr
# Measured at X=10, L=10: count = 0 at sp=5; count=1 at sp=6.
# Measured at X=10, L=15: count=3 at sp=5.
h2_count_X10_L10 = {sp: count_at(sp, 10.0, "10.0") for sp in sp_levels}
h2_count_X10_L15 = {sp: count_at(sp, 10.0, "15.0") for sp in sp_levels}
h2_verdict = {
    "hypothesis": "Min-point at L0-05 waiver + X=10 km/s aerocapture: sp≥5 AND L≥10 yr",
    "predicted_min_point": {"sp_w_per_kg": 5.0, "L_yr": 10.0, "X_km_s": 10.0},
    "measured": {
        "count_at_sp5_X10_L10": h2_count_X10_L10[5.0],
        "count_at_sp5_X10_L15": h2_count_X10_L15[5.0],
        "count_at_sp6_X10_L10": h2_count_X10_L10[6.0],
    },
    "verdict": "PARTIALLY-FALSIFIED: At sp=5, L=10 the count is 0; need L=15 (count=3) OR sp=6 at L=10 (count=1). One axis click higher than predicted.",
}

# H3: joint posterior of "any US fission program flies inside 2032-2035 with sp≥8 AND L≥5" ≤ 3 percent
# This decomposes as: p_fsp_orbit_by_2035 × p(scope ≥ 500 kWe | orbit) × p(sp ≥ 8 | orbit, 500 kWe) × p(L ≥ 5 | orbit)
# Use uniform (most-optimistic) prior to upper-bound
h3_p_strict = (
    p_500kWe_orbit_by_2035["uniform"]
    * p_sp_geq_given_orbit_500kWe[8.0]
    * p_L_geq_given_orbit_500kWe[5.0]
)
h3_verdict = {
    "hypothesis": "p(any US fission orbit in 2032-2035 delivering sp≥8 AND L≥5) ≤ 3 percent",
    "predicted_upper_bound": 0.03,
    "measured_upper_bound_uniform_prior": h3_p_strict,
    "verdict": "CONFIRMED" if h3_p_strict <= 0.03 else "FALSIFIED",
}

# H4: joint posterior of "any US fission program flies inside 2032-2035 with sp≥5 AND L≥10" ≤ 1 percent
h4_p_strict = (
    p_500kWe_orbit_by_2035["uniform"]
    * p_sp_geq_given_orbit_500kWe[5.0]
    * p_L_geq_given_orbit_500kWe[10.0]
)
h4_verdict = {
    "hypothesis": "p(any US fission orbit in 2032-2035 delivering sp≥5 AND L≥10) ≤ 1 percent",
    "predicted_upper_bound": 0.01,
    "measured_upper_bound_uniform_prior": h4_p_strict,
    "verdict": "CONFIRMED" if h4_p_strict <= 0.01 else "FALSIFIED",
}

# H5: full conjunction posterior (reactor + hybrid-aerocap + rendezvous-surv) ≤ 1% optimistic, ≤ 0.1% conservative
# Pick the best-feasible-corner under each prior
def best_corner_p(prior: str, rend: float, x_floor: float = 0.0) -> tuple[float, dict]:
    best_p = 0.0
    best_row = None
    for row in synthesis_rows:
        if row["aerocapture_X_km_s"] < x_floor:
            continue
        # use stored
        key = f"{prior}_{'rend_low' if rend == P_RENDEZVOUS_LOW else 'rend_hi'}_p_full"
        p = row[key]
        if p > best_p:
            best_p = p
            best_row = row
    return best_p, best_row

h5_optimistic_best, _ = best_corner_p("uniform", P_RENDEZVOUS_HI)
h5_conservative_best, _ = best_corner_p("skeptical", P_RENDEZVOUS_LOW)
h5_verdict = {
    "hypothesis": "Full-conjunction max posterior ≤ 1% optimistic / ≤ 0.1% conservative",
    "predicted_upper_bound_optimistic": 0.01,
    "predicted_upper_bound_conservative": 0.001,
    "measured_max_optimistic_uniform_x_rend_hi": h5_optimistic_best,
    "measured_max_conservative_skeptical_x_rend_low": h5_conservative_best,
    "verdict_optimistic": "CONFIRMED" if h5_optimistic_best <= 0.01 else "FALSIFIED",
    "verdict_conservative": "CONFIRMED" if h5_conservative_best <= 0.001 else "FALSIFIED",
}

# H6: reading-level conclusion = technology-demonstrator-only
# Compute fraction of (corner × prior × rend) cells that clear the venture (≥10%) threshold
total_cells = 0
venture_cells = 0
corp_growth_cells = 0
for row in synthesis_rows:
    for prior in ("skeptical", "jeffreys", "uniform"):
        for rend_label in ("rend_low", "rend_hi"):
            total_cells += 1
            cls = row[f"{prior}_{rend_label}_capital_class"]
            if cls in {"venture", "corporate_growth", "regulated_utility", "sovereign_bond"}:
                venture_cells += 1
            if cls in {"corporate_growth", "regulated_utility", "sovereign_bond"}:
                corp_growth_cells += 1

h6_verdict = {
    "hypothesis": "Reading-level: technology-demonstrator-only program class is the honest reading under conservative anchors",
    "total_capital_class_cells_evaluated": total_cells,
    "n_clearing_venture_10pct": venture_cells,
    "n_clearing_corporate_growth_30pct": corp_growth_cells,
    "verdict": "CONFIRMED — no candidate corner-prior-rendezvous combination clears even the venture-risk threshold of 10 percent" if venture_cells == 0 else f"FALSIFIED — {venture_cells} of {total_cells} cells clear venture threshold",
}


# ---------------------------------------------------------------------------
# 8. Write results
# ---------------------------------------------------------------------------

out = {
    "round": "R-reactor-specific-power-program-targets",
    "author": "iapetus",
    "date": "2026-05-15",
    "pre_registration": "STUDY.md (H1-H6)",
    "scope_anchor_rounds": [
        "R-arch-E-specific-power-flown-anchored",
        "R-specific-power-cliff",
        "R-aerocapture-cliff-shift",
        "R-reactor-lifetime-vs-burn-time",
        "R-power-bayesian-update",
    ],
    "l0_05_strict_close_20yr_by_sp": sp_cliff_strict_close_20yr,
    "l0_05_strict_unreachable_in_tested_sp_range": l0_05_strict_unreachable,
    "min_corner_table": corners,
    "subjective_priors": {
        "p_sp_geq_given_orbit_500kWe": p_sp_geq_given_orbit_500kWe,
        "p_L_geq_given_orbit_500kWe": {str(k): v for k, v in p_L_geq_given_orbit_500kWe.items()},
        "P_HYBRID_AEROCAP": P_HYBRID_AEROCAP,
        "P_RENDEZVOUS_LOW": P_RENDEZVOUS_LOW,
        "P_RENDEZVOUS_HI": P_RENDEZVOUS_HI,
        "p_X_geq_given_hybrid_closes": p_X_geq_given_hybrid_closes,
    },
    "p_500kWe_orbit_by_2035_by_prior": p_500kWe_orbit_by_2035,
    "synthesis_table": synthesis_rows,
    "capital_class_thresholds": [
        {"name": name, "min_p_full_conjunction": threshold}
        for name, threshold in CAPITAL_CLASSES
    ],
    "hypotheses": {
        "H1": h1_verdict,
        "H2": h2_verdict,
        "H3": h3_verdict,
        "H4": h4_verdict,
        "H5": h5_verdict,
        "H6": h6_verdict,
    },
}

out_path = RESULTS / "reactor_program_targets.json"
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

# ---------------------------------------------------------------------------
# 9. Console summary
# ---------------------------------------------------------------------------

print(f"Wrote {out_path}")
print()
print("=== L0-05 strict (close_20yr) closure counts by specific power ===")
for sp, n in sp_cliff_strict_close_20yr.items():
    print(f"  sp = {sp} W/kg : {n} cells close at close_20yr")
print(f"  → L0-05 strict UNREACHABLE up to sp=10 W/kg : {l0_05_strict_unreachable}")
print()
print("=== L0-05 ≥25-yr waiver: minimum (sp) per (X, L) corner ===")
print(f"  {'X km/s':>8} {'L yr':>8} {'min sp':>10} {'count':>6}")
for c in corners:
    L_str = "inf" if c["L_yr"] == "inf" else f"{c['L_yr']:.1f}"
    print(f"  {c['X_km_s']:>8.1f} {L_str:>8s} {c['min_sp_w_per_kg']:>10.1f} {c['cell_count_at_min']:>6d}")
print()
print("=== Joint posterior at most-optimistic corner (uniform prior, rend_hi) ===")
best_p_opt, best_row_opt = best_corner_p("uniform", P_RENDEZVOUS_HI)
print(f"  best full-conjunction posterior = {best_p_opt:.4%}")
if best_row_opt:
    print(f"  at sp={best_row_opt['min_sp_w_per_kg']} W/kg, X={best_row_opt['aerocapture_X_km_s']} km/s, L={best_row_opt['lifetime_L_yr']} yr")
    print(f"  capital class = {best_row_opt['uniform_rend_hi_capital_class']}")
print()
print("=== Hypotheses verdicts ===")
for h, v in out["hypotheses"].items():
    verdict_keys = [k for k in v if "verdict" in k]
    for vk in verdict_keys:
        print(f"  {h} [{vk}]: {v[vk]}")
print()
print("=== H6 capital class roll-up ===")
print(f"  total (corner × prior × rendezvous-prior) cells: {total_cells}")
print(f"  clearing venture-class (≥10%): {venture_cells}")
print(f"  clearing corporate-growth-class (≥30%): {corp_growth_cells}")
