"""R-demonstrator-mission-concept — run.py

Synthesis round. Consumes the three bet-audit rounds from this session and the
iapetus staged-options framework to produce: (1) a bet-retirement sequencing
under lesson 16 (dominant-kill vs highest-leverage gate); (2) a demonstrator-
conditional program-readiness conjunction; (3) a mapping of the demonstrator to
the re-gated tranche-1 (internal demonstrator gate replacing the external
Fission-Surface-Power-Phase-2 gate).

Inputs (not re-derived — outputs of prior rounds this session + iapetus):
  bet #1 (R-A14, fd6fab0):     A14 joint 0.53 (mm/s undemonstrated) ->
                               0.69 (demonstrator-confirmed). Earth-orbit proxy
                               retires deployment+catch+containment.
  bet #2 (R-water-electro, cd8d753): continuous-months flight-readiness ~0.48;
                               MET ~500-700 s (0-0.5% closure) vs RF-ion 2000 s
                               (closes, contamination-sensitive).
  bet #3 (R-kilopower, 3529984): reactor delivery <=1.5%; OFF critical path
                               (demonstrator flies non-nuclear per SCOPE path a).
  iapetus R7 (staged-options): T1=FSP-2 award p~0.023; E[loss]~$80M (kills early);
                               total program cost ~$1.15B; breakeven T1=0.25 @ $24B.

Deterministic. No randomness.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# The three bets as the demonstrator sees them (from this session's audits)
# ---------------------------------------------------------------------------
BETS = {
    "bet1_chunk_capture": {
        "label": "Active chunk capture (A14)",
        "baseline_readiness": 0.53,          # mm/s undemonstrated joint (R-A14)
        "demonstrator_confirmed": 0.69,      # after Earth-orbit + Saturn small-chunk demos
        "retired_by": "Earth-orbit catch-and-contain proxy (deployment+catch+containment) + Saturn small-chunk (rendezvous)",
        "retirement_cost_class": "low (Earth-orbit proxy is pre-cruise, cheap-to-iterate)",
        "on_demonstrator_critical_path": True,
    },
    "bet2_water_electrothermal": {
        "label": "Continuous water-electrothermal on Saturn-water purity (A1)",
        "baseline_readiness": 0.48,          # continuous-months flight-readiness (R-water-electro)
        "demonstrator_confirmed": 0.85,      # a successful months-long flight run lifts it, but only the mission retires it
        "retired_by": "the demonstrator's own continuous-months water-thruster run on bag-filtered chunk water (IS the test article)",
        "retirement_cost_class": "high (requires the full Saturn cruise + months of operation; no shortcut)",
        "on_demonstrator_critical_path": True,
    },
    "bet3_reactor": {
        "label": "Kilopower-class reactor program (L0-24)",
        "baseline_readiness": 0.015,         # delivery <=1.5% by 2035 (R-kilopower)
        "demonstrator_confirmed": None,      # not retired by the demonstrator
        "retired_by": "DEFERRED — demonstrator flies non-nuclear (RTG/solar-hybrid); reactor retired in a separate mission / by NASA FSP",
        "retirement_cost_class": "off the demonstrator critical path",
        "on_demonstrator_critical_path": False,
    },
}

# ---------------------------------------------------------------------------
# Lesson-16 gate classification: dominant-kill (lowest readiness, drives kill)
# vs highest-leverage (cheapest unit-readiness lift per dollar / per mission risk)
# ---------------------------------------------------------------------------
def gate_classification():
    on_path = {k: v for k, v in BETS.items() if v["on_demonstrator_critical_path"]}
    # dominant-kill = lowest readiness among on-path bets
    dominant_kill = min(on_path, key=lambda k: on_path[k]["baseline_readiness"])
    # highest-leverage = largest cheap lift: bet1's Earth-orbit proxy is cheap AND
    # lifts 0.53->0.69; bet2 only lifts via the full mission (expensive). So highest
    # leverage per unit cost is bet1.
    highest_leverage = "bet1_chunk_capture"
    return {
        "dominant_kill_gate": dominant_kill,
        "dominant_kill_readiness": on_path[dominant_kill]["baseline_readiness"],
        "highest_leverage_gate": highest_leverage,
        "highest_leverage_rationale": (
            "bet1 Earth-orbit proxy is cheap, pre-cruise, and lifts A14 0.53->0.69 by "
            "retiring 3 of 5 sub-steps; bet2 only lifts via the full multi-month Saturn run. "
            "Per unit cost/mission-risk, bet1 buys the most readiness."),
        "recommended_sequence": [
            "1. bet1 Earth-orbit catch-and-contain proxy (cheap, pre-cruise) -> lift A14 to ~0.69 BEFORE committing the cruise",
            "2. bet2 continuous-months water-thruster run during the Saturn demonstrator cruise (the long pole; dominant-kill)",
            "3. bet3 reactor DEFERRED off critical path (fly non-nuclear)",
        ],
    }

# ---------------------------------------------------------------------------
# Demonstrator-conditional program-readiness: product of the on-path bets the
# demonstrator must clear (bet3 excluded — deferred).
# Two scenarios: (A) commit cruise at baseline bet1 (0.53); (B) retire bet1 via
# Earth-orbit proxy first (->0.69) THEN commit cruise.
# ---------------------------------------------------------------------------
def program_readiness():
    b1_base = BETS["bet1_chunk_capture"]["baseline_readiness"]
    b1_demo = BETS["bet1_chunk_capture"]["demonstrator_confirmed"]
    b2 = BETS["bet2_water_electrothermal"]["baseline_readiness"]
    return {
        "scenarioA_cruise_at_baseline_bet1": round(b1_base * b2, 3),
        "scenarioB_earth_orbit_proxy_first": round(b1_demo * b2, 3),
        "interpretation": (
            "Scenario A (commit the Saturn cruise without the Earth-orbit proxy) is a "
            f"{round(b1_base*b2*100)}% joint shot at retiring both on-path bets in one mission. "
            "Scenario B (Earth-orbit proxy first, lifting bet1 to 0.69) raises that to "
            f"{round(b1_demo*b2*100)}%. The proxy is the cheap option-value purchase."),
    }

# ---------------------------------------------------------------------------
# Tranche mapping: re-gated tranche-1 (internal demonstrator) vs iapetus R7
# (external FSP-2). The demonstrator's controllable pass-probability replaces the
# 0.023 FSP-2 award.
# ---------------------------------------------------------------------------
IAPETUS = {
    "old_T1_gate": "Fission-Surface-Power-Phase-2 award (external)",
    "old_T1_pass_prob": 0.023,
    "old_E_loss_usd_M": 80,
    "total_program_cost_usd_B": 1.15,
    "breakeven_T1_at_24B": 0.25,
}

def tranche_mapping():
    prB = BETS["bet1_chunk_capture"]["demonstrator_confirmed"] * BETS["bet2_water_electrothermal"]["baseline_readiness"]
    return {
        "old_tranche1": IAPETUS,
        "new_tranche1_gate": "internal demonstrator: Earth-orbit catch-and-contain (bet1) + continuous-months water-thruster on chunk water (bet2)",
        "new_tranche1_pass_prob_scenarioB": round(prB, 3),
        "reactor_status": "bet3 deferred off critical path (demonstrator non-nuclear)",
        "reading": (
            f"The re-gated tranche-1 pass probability (~{round(prB*100)}% under Earth-orbit-proxy-first) "
            f"is ~{round(prB/IAPETUS['old_T1_pass_prob'])}x the external FSP-2 award probability ({IAPETUS['old_T1_pass_prob']}). "
            "The program now spends its tranche-1 budget on an experiment it CONTROLS, with a materially "
            "higher pass probability, and the dominant external kill-gate (FSP-2) is removed from the critical path."),
        "cost_class_usd_M": "150-1500 (Hayabusa2 ~150-300M to OSIRIS-REx ~1B class; non-nuclear demonstrator below the reactor-bundled path)",
    }

def main():
    gc = gate_classification()
    pr = program_readiness()
    tm = tranche_mapping()
    summary = {
        "round": "R-demonstrator-mission-concept", "worker": "hyperion", "date": "2026-05-22",
        "bets": BETS, "gate_classification": gc, "program_readiness": pr, "tranche_mapping": tm,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2))

    print("=" * 74)
    print("R-demonstrator-mission-concept — what does the demonstrator retire?")
    print("=" * 74)
    print("\nBet retirement (lesson 16 gate classification):")
    print(f"  dominant-kill gate    : {gc['dominant_kill_gate']} (readiness {gc['dominant_kill_readiness']})")
    print(f"  highest-leverage gate : {gc['highest_leverage_gate']}")
    for s in gc["recommended_sequence"]:
        print(f"    {s}")
    print("\nDemonstrator-conditional program-readiness (on-path bets only; bet3 deferred):")
    print(f"  Scenario A (cruise at baseline bet1=0.53): {pr['scenarioA_cruise_at_baseline_bet1']}")
    print(f"  Scenario B (Earth-orbit proxy first ->0.69): {pr['scenarioB_earth_orbit_proxy_first']}")
    print("\nTranche-1 re-gating vs iapetus R7:")
    print(f"  old T1 (FSP-2 award): pass {IAPETUS['old_T1_pass_prob']}, E[loss] ${IAPETUS['old_E_loss_usd_M']}M")
    print(f"  new T1 (internal demonstrator): pass {tm['new_tranche1_pass_prob_scenarioB']} "
          f"(~{round(tm['new_tranche1_pass_prob_scenarioB']/IAPETUS['old_T1_pass_prob'])}x)")
    print(f"\nWrote {RESULTS}/summary.json")


if __name__ == "__main__":
    main()
