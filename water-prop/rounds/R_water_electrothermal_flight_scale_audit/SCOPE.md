# R-water-electrothermal-flight-scale-audit — bet #2: does continuous water-electrothermal at flight scale on Saturn-water purity close, and how does it fail?

**Status:** scope + study (worker-authored). Authored by **hyperion** (worker), 2026-05-22, immediately before execution. This SCOPE is worker-authored because no orchestrator SCOPE existed; locked finding 5 named bet #2 as the only one of the three engineering bets without a dedicated audit round, and the R-A14 + R-kilopower handoffs (`fd6fab0`, `3529984`, this session) flagged it as the highest-leverage un-audited bet.

**Anchoring discipline (lesson 9):** this round anchors on the PRIMARY-text findings of the campaign's existing electrothermal rounds (R0 frozen-flow, R6 power-optimal-Isp, R-silicate-contamination, R11 grid-life, R-MET-cathode-escape-hatch) and the user-locked A1 belief, not on downstream summaries.

---

## Why this round

Locked finding 5 (`5535179f`): the matrix reduces to three engineering bets. Bet #2 is *"continuous water-electrothermal on Saturn-water purity at flight scale — lab-confirmed 800 s in 50 s pulses; flight gap remains; Momentus Vigoride is the closest precedent."* Bets #1 (R-A14, chunk capture) and #3 (R-kilopower, reactor program) now have dedicated audits. Bet #2 has only the Saturn-worker A1 PLAUSIBLE-PROVISIONAL finding (locked `650938e3`).

**Three flight gaps the A1 finding names but did not quantify:**
1. **Ground → flight** at the operation profile.
2. **Pulse (50 s) → continuous (months).**
3. **Lab-clean water → Saturn-ring water** (~0.3–3% non-icy contaminants; resonant-cavity / grid erosion).

**Two cross-round tensions this round must resolve (surfaced during the heritage fetch):**
- **The 800 s A1 anchor exceeds the campaign's own continuous ceiling.** R0 frozen-flow found realistic continuous water-MET Isp is ~480–650 s, with an equilibrium ceiling ~700–750 s; 800 s is a ground/clean/short-pulse figure. The locked A1 belief and R0 are in numerical tension.
- **The closure cells do not run on 800 s MET.** titan-3 / mission_graph closure cells run Isp 2000 s (water radio-frequency ion, Pale Blue class), not 800 s MET. So "bet #2 = water-electrothermal at 800 s" is partly mis-specified relative to what actually closes the matrix. The audit must address BOTH the MET branch (contamination-tolerant, ~500–800 s, does it reach matrix-closing Isp?) and the RF-ion branch (Isp-sufficient at 2000 s, but contamination-SENSITIVE — does its continuous flight on Saturn water hold?).

---

## Question this round answers

For the inbound electric burn fed by bag-harvested Saturn-ring water over a multi-year continuous operation:

1. What is the defensible **continuous-flight effective Isp** for the contamination-tolerant architecture (water-MET), and what matrix closure rate does it produce (via the locked A1 closure sensitivity: 0% @600 s, 0.5% @700 s, 4% @800 s, 12% @900 s at the 30 t floor)?
2. For the Isp-sufficient architecture (water RF-ion, 2000 s), what is the **continuous-months flight-readiness** conjunction — does the bag's incidental silicate rejection hold for months, and does cathode/grid life cover the multi-year burn?
3. How large is the **flight gap** in cumulative operating time between the closest flown precedent (Vigoride-5: 35 pulse firings; AQUARIUS: deep-space resistojet at 91 s) and ICEBERG's continuous-months requirement?
4. **Does bet #2 fail, and if so, how differently from bets #1 and #3?**

---

## Pre-registered hypotheses (worker's honest predictions, frozen before computation)

| # | Hypothesis | Predicted | Falsification band |
|---|---|---|---|
| H1 | Realistic continuous-flight water-MET Isp on Saturn-purity water is 500–700 s — below the 800 s ground/pulse anchor (R0 frozen-flow ceiling + continuous-vs-pulse de-rate; contamination is lifetime not Isp risk for MET). | 500–700 s | >750 s or <450 s defensible continuous-flight |
| H2 | At realistic continuous MET Isp (500–700 s), matrix closure at the floor is <2% — the contamination-tolerant architecture does not reach matrix-closing Isp. | <2% closure | ≥4% at mid Isp |
| H3 | The Isp-sufficient architecture (RF-ion 2000 s) closes on Isp but its continuous-months flight-readiness on Saturn water is a conjunction of (bag silicate rejection holds) × (cathode/grid life ≥ burn) × (no anomaly), with joint flight-readiness 0.3–0.6 absent a demonstrator. | 0.3–0.6 joint | <0.15 or >0.8 |
| H4 | The cumulative-operating-time flight gap between Vigoride-5 (≈ tens of hours of pulses) and ICEBERG continuous-months (≈ thousands of hours continuous) is ≥2 orders of magnitude. | ≥100× | <30× |
| H5 (load-bearing) | Bet #2 fails DIFFERENTLY from bets #1/#3: not "the physics doesn't work" (Vigoride proved water electrothermal in space, in pulses), but "the matrix-closing Isp (2000 s) belongs to the contamination-SENSITIVE RF-ion architecture, whose continuous-months operation on Saturn water depends on the bag filtration holding — flight-unproven at ICEBERG duration." The matrix propulsion cell should be carried as **demonstrator-conditional on a continuous-months-on-chunk-water run**. | reading-level | falsified if MET reaches matrix-closing Isp at realistic continuous flight OR if RF-ion continuous-on-Saturn-water is already flight-demonstrated |

---

## Method

`run.py`, deterministic. (1) MET branch: continuous-flight effective-Isp bracket (anchored on R0) → matrix closure rate via piecewise-linear interpolation of the locked A1 closure sensitivity. (2) RF-ion branch: continuous-months flight-readiness conjunction from three reliability factors anchored on R11 (bag silicate rejection) + R-MET-cathode-escape-hatch (cathode/grid life). (3) Flight-gap: cumulative-operating-time ratio, ICEBERG-continuous vs flown precedent. Heritage in `inputs/flight_heritage.csv`.

## Out of scope
- Re-deriving R0 frozen-flow Isp ceiling (input, not re-derived).
- Re-deriving R11 silicate-rejection ratio or grid-wear (inputs).
- Reactor power class (R-kilopower, decision #14) and chunk capture (R-A14, bet #1) — companion audits.
- Demonstrator-mission specification (R-demonstrator-mission-concept consumes this round's demonstrator objective).
