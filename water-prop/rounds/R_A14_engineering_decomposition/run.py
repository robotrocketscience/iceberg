"""R-A14-engineering-decomposition — run.py

Replaces the Saturn-worker desk-study chunk-capture decomposition
(rendezvous 0.90 x deployment 0.95 x catch 0.80 x containment 0.70 x
survive 0.95 = 0.46 joint) with engineering-heritage-anchored sub-step
probabilities, each carrying a low/mid/high uncertainty bracket. Catch (3)
and containment (4) are closing-velocity-conditional; survive (5) is
cinch-redundancy-conditional.

Outputs:
  results/per_substep_probabilities.csv  — 5 sub-steps x low/mid/high (+ regime)
  results/joint_posterior_sensitivity.csv — joint over velocity x cinch x bracket
  results/summary.json                    — machine-readable digest

Anchors are documented in inputs/heritage_base_rates.csv,
inputs/catch_velocity_envelope.md, inputs/bag_cruise_duration_model.md.
Deterministic; no randomness.
"""

import csv
import json
import pathlib

HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Matrix closure context (titan-3 / Saturn-worker audit; inputs, not re-derived)
# ---------------------------------------------------------------------------
DESK_ANCHOR = 0.85                  # the 0.85 single-pass desk-study anchor A14
DOWNSTREAM_EFF = 0.277              # chunk-fed-spiral + Earth-arrival efficiency
CANONICAL_CHUNK_T = 200.0
L0_04_FLOOR_T = 25.0               # provisional commercial floor (REQUIREMENTS v0.13)
L0_09_FLOOR_T = 30.0               # service-availability floor used in audit table

# Absolute capture efficiency needed to deliver each floor from a 200 t chunk:
#   delivered = chunk * cap_eff * downstream_eff   ->   cap_eff = floor/(chunk*eff)
THRESH_25T = L0_04_FLOOR_T / (CANONICAL_CHUNK_T * DOWNSTREAM_EFF)   # ~0.451
THRESH_30T = L0_09_FLOOR_T / (CANONICAL_CHUNK_T * DOWNSTREAM_EFF)   # ~0.542

# ---------------------------------------------------------------------------
# Sub-step probability brackets (low, mid, high) — engineering-heritage anchored
# ---------------------------------------------------------------------------
# 1 rendezvous: OSIRIS-REx + Hayabusa2 + Hayabusa proximity-ops 3/3 success,
#   de-rated for Saturn light-time autonomy + non-cooperative tumbling target.
P_RENDEZVOUS = (0.88, 0.93, 0.97)
# 2 deployment: LOFTID + JWST sunshield deployable-hardware heritage; bag
#   mechanism complexity between the two.
P_DEPLOYMENT = (0.90, 0.94, 0.97)
# 3 catch + 4 containment: closing-velocity-conditional (see catch_velocity_envelope.md)
#   keyed by regime -> (low, mid, high) bracket each.
P_CATCH = {
    "mm_s":      (0.85, 0.88, 0.93),
    "low_m_s":   (0.72, 0.78, 0.84),
    "high_m_s":  (0.58, 0.65, 0.72),
}
P_CONTAINMENT = {
    "mm_s":      (0.74, 0.78, 0.84),
    "low_m_s":   (0.62, 0.68, 0.75),
    "high_m_s":  (0.50, 0.55, 0.62),
}
# 5 survive over 13 yr: cinch-redundancy-conditional (see bag_cruise_duration_model.md).
#   puncture ~0.98, sublimation ~0.995 (benign at cold cruise) dominate-free; cinch is the driver.
P_SURVIVE = {
    "single_cinch":   (0.78, 0.85, 0.90),
    "redundant_cinch":(0.80, 0.88, 0.93),
}

VELOCITY_REGIMES = ["mm_s", "low_m_s", "high_m_s"]
CINCH_DESIGNS = ["single_cinch", "redundant_cinch"]
BRACKETS = {"low": 0, "mid": 1, "high": 2}

# Saturn-worker placeholder, for side-by-side.
PLACEHOLDER = {"rendezvous": 0.90, "deployment": 0.95, "catch": 0.80,
               "containment": 0.70, "survive": 0.95}
PLACEHOLDER_JOINT = 1.0
for v in PLACEHOLDER.values():
    PLACEHOLDER_JOINT *= v


def joint(velocity, cinch, bracket):
    b = BRACKETS[bracket]
    r = P_RENDEZVOUS[b]
    d = P_DEPLOYMENT[b]
    c = P_CATCH[velocity][b]
    n = P_CONTAINMENT[velocity][b]
    s = P_SURVIVE[cinch][b]
    j = r * d * c * n * s
    return {"rendezvous": r, "deployment": d, "catch": c,
            "containment": n, "survive": s, "joint": j}


def closure(j):
    return {
        "capture_efficiency": round(j, 4),
        "multiplier_of_desk_0.85": round(j / DESK_ANCHOR, 3),
        "closes_25t_floor": j >= THRESH_25T,
        "closes_30t_floor": j >= THRESH_30T,
    }


# ---------------------------------------------------------------------------
# Demonstrator-retirement: which sub-steps each demonstrator profile retires.
# Retiring a sub-step lifts its probability to a demonstrator-confirmed value.
# ---------------------------------------------------------------------------
# Earth-orbit demonstrator (deployable target masses, mm/s closing): retires
#   deployment + catch + containment at mm/s -> confirmed ~0.95 each.
# Saturn small-chunk mission-1: retires rendezvous + short-duration survive.
# 13-yr survive: NOT retired until first full mission returns.
DEMO_CONFIRMED = 0.95   # a sub-step a demonstrator confirms is lifted to this cap


def demonstrator_conditional_joint():
    """Joint after Earth-orbit demonstrator (deployment, catch, containment at
    mm/s confirmed) AND Saturn small-chunk demonstrator (rendezvous confirmed),
    with 13-yr survive still un-retired at the redundant-cinch mid value."""
    r = DEMO_CONFIRMED          # rendezvous confirmed by Saturn small-chunk demo
    d = DEMO_CONFIRMED          # deployment confirmed by Earth-orbit demo
    c = DEMO_CONFIRMED          # catch confirmed at mm/s by Earth-orbit demo
    n = 0.92                    # containment confirmed at mm/s (capped below 0.95: hardest sub-step)
    s = P_SURVIVE["redundant_cinch"][1]   # 13-yr survive NOT retired -> stays at mid
    j = r * d * c * n * s
    return {"rendezvous": r, "deployment": d, "catch": c, "containment": n,
            "survive": s, "joint": j, **closure(j)}


def main():
    # --- per-substep CSV ---
    substep_rows = []
    for name, br in [("1_rendezvous", P_RENDEZVOUS), ("2_deployment", P_DEPLOYMENT)]:
        substep_rows.append({"substep": name, "regime": "velocity_independent",
                             "low": br[0], "mid": br[1], "high": br[2],
                             "placeholder": PLACEHOLDER[name.split("_")[1]]})
    for vel in VELOCITY_REGIMES:
        substep_rows.append({"substep": "3_catch", "regime": vel,
                             "low": P_CATCH[vel][0], "mid": P_CATCH[vel][1],
                             "high": P_CATCH[vel][2], "placeholder": PLACEHOLDER["catch"]})
    for vel in VELOCITY_REGIMES:
        substep_rows.append({"substep": "4_containment", "regime": vel,
                             "low": P_CONTAINMENT[vel][0], "mid": P_CONTAINMENT[vel][1],
                             "high": P_CONTAINMENT[vel][2], "placeholder": PLACEHOLDER["containment"]})
    for cinch in CINCH_DESIGNS:
        substep_rows.append({"substep": "5_survive", "regime": cinch,
                             "low": P_SURVIVE[cinch][0], "mid": P_SURVIVE[cinch][1],
                             "high": P_SURVIVE[cinch][2], "placeholder": PLACEHOLDER["survive"]})
    with open(RESULTS / "per_substep_probabilities.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["substep", "regime", "low", "mid", "high", "placeholder"])
        w.writeheader()
        w.writerows(substep_rows)

    # --- joint sensitivity CSV ---
    sens_rows = []
    for vel in VELOCITY_REGIMES:
        for cinch in CINCH_DESIGNS:
            for bracket in BRACKETS:
                j = joint(vel, cinch, bracket)
                cl = closure(j["joint"])
                sens_rows.append({
                    "velocity": vel, "cinch": cinch, "bracket": bracket,
                    "rendezvous": round(j["rendezvous"], 3),
                    "deployment": round(j["deployment"], 3),
                    "catch": round(j["catch"], 3),
                    "containment": round(j["containment"], 3),
                    "survive": round(j["survive"], 3),
                    "joint": round(j["joint"], 4),
                    "mult_of_0.85": cl["multiplier_of_desk_0.85"],
                    "closes_25t": cl["closes_25t_floor"],
                    "closes_30t": cl["closes_30t_floor"],
                })
    with open(RESULTS / "joint_posterior_sensitivity.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sens_rows[0].keys()))
        w.writeheader()
        w.writerows(sens_rows)

    demo = demonstrator_conditional_joint()

    summary = {
        "round": "R-A14-engineering-decomposition", "worker": "hyperion", "date": "2026-05-22",
        "context": {
            "desk_anchor": DESK_ANCHOR, "downstream_eff": DOWNSTREAM_EFF,
            "canonical_chunk_t": CANONICAL_CHUNK_T,
            "threshold_25t_floor": round(THRESH_25T, 4),
            "threshold_30t_floor": round(THRESH_30T, 4),
            "placeholder_joint": round(PLACEHOLDER_JOINT, 4),
        },
        "headline_joints": {
            "mm_s_redundant_mid": round(joint("mm_s", "redundant_cinch", "mid")["joint"], 4),
            "low_m_s_redundant_mid": round(joint("low_m_s", "redundant_cinch", "mid")["joint"], 4),
            "high_m_s_redundant_mid": round(joint("high_m_s", "redundant_cinch", "mid")["joint"], 4),
            "mm_s_redundant_low": round(joint("mm_s", "redundant_cinch", "low")["joint"], 4),
            "mm_s_redundant_high": round(joint("mm_s", "redundant_cinch", "high")["joint"], 4),
        },
        "demonstrator_conditional": {k: round(v, 4) if isinstance(v, float) else v
                                     for k, v in demo.items()},
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2))

    # --- console digest ---
    print("=" * 74)
    print("R-A14-engineering-decomposition")
    print("=" * 74)
    print(f"Placeholder joint (Saturn-worker desk): {PLACEHOLDER_JOINT:.3f}")
    print(f"Closure thresholds (200 t chunk, {DOWNSTREAM_EFF:.1%} downstream): "
          f"25 t floor -> cap_eff >= {THRESH_25T:.3f}; 30 t floor -> >= {THRESH_30T:.3f}")
    print()
    print(f"{'velocity':<10}{'cinch':<18}{'bracket':<8}{'joint':>8}{'x0.85':>7}"
          f"{'25t?':>6}{'30t?':>6}")
    for vel in VELOCITY_REGIMES:
        for cinch in CINCH_DESIGNS:
            for bracket in BRACKETS:
                j = joint(vel, cinch, bracket)["joint"]
                cl = closure(j)
                print(f"{vel:<10}{cinch:<18}{bracket:<8}{j:>8.3f}"
                      f"{cl['multiplier_of_desk_0.85']:>7.2f}"
                      f"{'Y' if cl['closes_25t_floor'] else 'n':>6}"
                      f"{'Y' if cl['closes_30t_floor'] else 'n':>6}")
    print()
    print(f"Demonstrator-conditional joint (Earth-orbit + Saturn small-chunk demos, "
          f"13-yr survive un-retired): {demo['joint']:.3f}  "
          f"(closes 25t={demo['closes_25t_floor']}, 30t={demo['closes_30t_floor']})")
    print(f"\nWrote {RESULTS}/per_substep_probabilities.csv, "
          f"joint_posterior_sensitivity.csv, summary.json")


if __name__ == "__main__":
    main()
