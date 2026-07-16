# R-demonstrator-mission-concept — what does the demonstrator retire?

**Worker:** hyperion. **Date:** 2026-05-22. **Status:** complete.
**Round type:** synthesis (concept-of-operations + risk-retirement sequencing + staged-options re-gating). Consumes this session's three bet-audits + iapetus staged-options.
**SCOPE:** Saturn-authored 2026-05-21 (`030cb5e`), **before** the three bet-audits ran. This round populates the SCOPE's skeleton with the audited numbers and corrects one placeholder (the bet-2 thruster).

---

## Why this round

The SCOPE asked: what is the smallest mission that retires all three engineering bets? It proposed a concept-of-operations but used pre-audit placeholders (notably "water-MET ≥700 s … IS bet 2's experiment"). This session's three bet-audits (R-A14 `fd6fab0`, R-water-electrothermal `cd8d753`, R-kilopower `3529984`) now supply the real numbers and one structural correction. This round synthesizes them into a demonstrator concept-of-operations, a risk-retirement priority order, and a mapping to the re-gated tranche-1.

---

## Pre-registered hypotheses (worker-authored, applying lesson 18 — condition on the right structural variables)

| # | Hypothesis | Measured | Grade |
|---|---|---|---|
| H1 | By lesson 16: bet #1 is the highest-leverage gate (cheap Earth-orbit proxy lifts A14 0.53→0.69), bet #2 is the dominant-kill gate (lowest readiness, un-retirable except by the full mission), bet #3 is deferred off the critical path. | dominant-kill = bet #2 (0.48); highest-leverage = bet #1 | **HELD** |
| H2 | The demonstrator must fly the COMMERCIAL thruster architecture (RF-ion 2000 s + bag filtration on dirty water), not a power-appropriate MET, or it fails to retire commercial bet #2. | confirmed by bet-2 audit (MET 0–0.5% closure; cells run 2000 s RF-ion) | **HELD** (corrects SCOPE) |
| H3 | Demonstrator-conditional program-readiness (bets #1 × #2; bet #3 deferred) is 0.25–0.35 — a ~1-in-3 shot, arguing for the Earth-orbit proxy first. | 0.254 (cruise at baseline) → 0.331 (proxy first) | **HELD** |
| H4 (load-bearing) | The demonstrator operationalizes the re-gated tranche-1: an internal demonstrator gate (bets #1+#2) replacing the external FSP-2 gate, at materially higher controllable pass probability, with bet #3 deferred. | new T1 pass ~0.33 vs FSP-2 0.023 (~14×) | **HELD** |

All four held.

---

## Method

`run.py`, deterministic, no new physics — it composes the prior rounds' outputs. (1) Gate classification per lesson 16. (2) Demonstrator-conditional program-readiness as the product of on-path bet readiness, in two sequencing scenarios. (3) Tranche-1 re-gating vs iapetus R7 (T1=FSP-2 award, p≈0.023, E[loss]≈$80M, total program ≈$1.15B). Concept-of-operations in `results/conops_sketch.md`; priority order in `results/risk_retirement_priority.md`.

---

## Results

**Gate classification (lesson 16):** dominant-kill = bet #2 water-electrothermal (0.48, lowest on-path, un-retirable except by months of flight); highest-leverage = bet #1 chunk capture (cheap Earth-orbit proxy lifts A14 0.53→0.69).

**Recommended sequence:** (1) Earth-orbit catch-and-contain proxy first (cheap, pre-cruise) → lift bet #1 to 0.69 before committing the cruise; (2) continuous-months RF-ion run on chunk water during the Saturn cruise (the long pole); (3) reactor deferred off critical path (fly non-nuclear).

**Demonstrator-conditional program-readiness:** 0.254 (commit cruise at baseline bet #1) → **0.331** (Earth-orbit proxy first). A ~1-in-3 shot at retiring both on-path bets in one mission, dominated by bet #2's 0.48.

**Tranche-1 re-gating:** new internal demonstrator gate pass ≈ 0.33 vs the external FSP-2 award 0.023 — **~14×**, ICEBERG-controllable, with the dominant external kill-gate removed from the critical path. Demonstrator cost-class $150M–$1.5B (Hayabusa2 to OSIRIS-REx range; non-nuclear below the reactor-bundled path).

**Thruster-mismatch correction (H2):** a small low-power demonstrator would naturally fly MET (~543 s power-optimal per R6), but to retire *commercial* bet #2 it must fly the commercial RF-ion + bag-filtration stack on dirty chunk water. A MET demonstrator would prove water-electrothermal in deep space but not retire the contamination-sensitive RF-ion-continuous bet the matrix rests on.

---

## Reading (load-bearing, per H4)

**The demonstrator is the instrument that re-gates ICEBERG from an external-event bet to an internal-experiment bet — and that is the single biggest improvement to the program's risk story this session produces.** iapetus R7 priced tranche-1 on the Fission-Surface-Power-Phase-2 award: a gate ICEBERG does not control, with a ~2.3% pass probability, that kills the program early (E[loss]≈$80M) >95% of the time. By deferring the reactor (bet #3, ≤1.5% delivery, off critical path) and flying a non-nuclear demonstrator that retires the two ICEBERG-controllable bets (#1 chunk capture, #2 water-electrothermal), the tranche-1 gate becomes an internal experiment at ~14× the pass probability.

But the demonstrator is not a sure thing, and the honest number matters: **even with the cheap Earth-orbit proxy retiring bet #1 first, the demonstrator is a ~1-in-3 shot (0.33) at retiring both on-path bets in a single mission**, dominated by bet #2's 0.48 continuous-months flight-readiness. The sequencing is what makes this defensible: bet #1 is cheaply liftable (Earth-orbit proxy, pre-cruise) and should be retired before the 12–15-year cruise is committed; bet #2 is the dominant-kill long pole and is only retired by the mission itself. Spending the cheap option-value first (proxy) and treating the cruise as the bet #2 test article is the correct staged-options structure.

The thruster-mismatch finding (H2) is the demonstrator's most consequential design decision: it must fly the contamination-sensitive commercial RF-ion + bag-filtration stack, not the simpler power-appropriate MET, or the mission proves the wrong thing.

---

## Revisit (mandatory)

All four hypotheses held. This is the fourth clean round of the session and the second consecutive worker-authored SCOPE (after bet #2) that graded clean — both pre-registered the conditioning structure (lesson 18): gate-role classification (H1), thruster architecture branch (H2), sequencing scenario (H3). The synthesis introduced no new physics, so the grades reflect the prior rounds' correctness as much as this one's.

**This round corrects the SCOPE, per lesson 9 (anchor on primary text, not a prior summary).** The SCOPE's "water-MET ≥700 s IS bet 2's experiment" was a pre-audit placeholder; the bet-2 audit showed MET does not reach matrix-closing Isp and the cells run 2000 s RF-ion. A worker who took the SCOPE at face value would have specified the wrong demonstrator thruster. The correction is the value-add of running the synthesis *after* the bet-audits rather than before.

**Where I could be wrong.** (1) The demonstrator-confirmed bet #2 readiness (0.85, used only illustratively) is not load-bearing here — the program-readiness uses bet #2's *baseline* 0.48, which is the conservative anchor. (2) The ~14× tranche-1 improvement compares a controllable experiment's pass probability to an external award probability; they are not the same kind of object (one is "will our experiment succeed," the other "will a third party award a contract") — the comparison is about *what the program is betting on*, not a like-for-like probability. I flag this rather than overclaim. (3) Cost-class is an order-of-magnitude analogy (Hayabusa2/OSIRIS-REx), not a costed estimate.

---

## Cross-learning

- **Consumes and closes the three-bets audit set into an actionable artifact.** Bets #1/#2/#3 (this session) → demonstrator concept-of-operations + risk-retirement priority + tranche-1 re-gating. This is the technical-reviewer-facing deliverable the SCOPE called HIGH priority.
- **Corrects the Saturn SCOPE's bet-2 thruster** (MET → commercial RF-ion + bag filtration); feeds design-axis 03 (inbound propulsion) and the conops document (axis 16).
- **Operationalizes the iapetus staged-options re-gating** (from R-A14's `iapetus_staged_options_re_gating.md`): the demonstrator IS the re-gated tranche-1; iapetus R7's E[loss] should be recomputed against the internal demonstrator gate rather than the FSP-2 award. Feeds matrix decision #13 (pitch staged-options reframe).
- **Demonstrator sequencing applies lesson 16** (dominant-kill = bet #2; highest-leverage = bet #1): retire the cheap high-leverage gate (Earth-orbit proxy) before committing the cruise; the dominant-kill gate (bet #2) is the cruise itself.

---

## Files

- `SCOPE.md` (Saturn, pre-audit), `run.py`, `results/summary.json`, `results/conops_sketch.md`, `results/risk_retirement_priority.md`, `READING.md`.
