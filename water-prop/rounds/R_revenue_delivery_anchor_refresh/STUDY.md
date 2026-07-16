# R-revenue-delivery-anchor-refresh — STUDY (pre-registration frozen before re-runs)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. **Status:** pre-registration frozen; re-runs pending.
**Round type:** parameter-refresh + sensitivity band-sweep over three existing revenue rounds, with one new joint constraint (delivered-tonnes capped by chunk-mass-cap × corrected delivery fraction). Pure-stdlib Python re-runs of existing `run.py` harnesses with a swept `delivered_t` input.

**Anchors:**
- R-pitch-arithmetic-audit (`f9f7fc2`): honest delivered fraction at surviving cells is **17–28%**, not the pitch §2 **54%**; same root error as the retired 75% (impulsive ΔV frame + indefensible 1.5 km/s Saturn departure).
- R-framework-matrix-parity (titan-4, integrated latest+18 — **the upstream dependency the SCOPE flagged as BLOCKED has since landed**): framework full-round-trip delivery ratio is **~20% of nominal chunk (39.5 t / 200 t) constraints-OFF**, and **0% constraints-ON (conservative)** — no cell delivers ≥ 30 t. The 17–28% band is the physics-only (constraints-off) reading; the matrix-faithful conservative reading is harder still.
- REQUIREMENTS L1-007 chunk-mass cap = 200 t (captured); L0-04 commercial-class floor = 25 t provisional (locked belief `c95626970c29aeef`).

---

## Question (from SCOPE)

The pitch §4 era table claims 50 t delivered per mission at a 54% delivery fraction. The honest fraction is 17–28%. Punch-list M-3 feared this invalidates the revenue rounds (R-LEO-water-demand-curve, R-clearing-price-tail-integration, R-pricing-anchor-revisit). **Does correcting the delivery anchor flip any revenue-round verdict — or is the pitch §4 table the optimistic outlier while the revenue rounds already sit at (or near) the honest band?**

The binding interaction is **delivered-tonnes = delivery-fraction × captured-tonnes**, with captured-tonnes capped at 200 t (L1-007). At the cap, the honest delivered-per-mission band is **200 t × 17–28% = 34–56 t** (centered ~44 t). The clearing-price round already uses 42 t. The framework constraints-off point (39.5 t) lands inside this band.

---

## What the upstream pin changes vs the SCOPE-as-written

The SCOPE was authored 2026-05-22 with R-framework-matrix-parity still open, so it specified a band-sweep with no pinned point. The parity round has since landed and pins:
- **constraints-OFF: 39.5 t / 200 t ≈ 19.75%** — inside the 17–28% band, low end. The sweep grid {34, 42, 50, 56} t brackets it (34 ≈ 17%, 42 ≈ 21%, 50 = 25%, 56 = 28%).
- **constraints-ON (conservative): 0 t** — no closing cell. This is a *new, sharper* reading the SCOPE did not have: under the matrix-faithful conservative constraints there is no delivery at all, so the revenue rounds are trivially NPV-negative (zero revenue). I therefore add **point 0 t** to the sweep as the conservative-reading anchor, alongside the SCOPE's {34, 42, 50, 56}.

This does not change any pre-registered hypothesis; it sharpens the verdict envelope (the conservative end is 0 t, not 34 t).

---

## Pre-registered hypotheses (frozen; worker's honest predictions before re-runs)

| # | Hypothesis | Predicted | Falsification band |
|---|---|---|---|
| H1 | At the 200 t cap, the corrected band (34–56 t) overlaps the `delivered_t` the revenue rounds already use, for ≥2 of 3 rounds. | ≥2 of 3 rounds' `delivered_t` ∈ [34, 56] t | Falsified if ≥2 of 3 rounds use `delivered_t` outside 34–56 t. |
| H2 | Re-running R-LEO-water-demand-curve across the band shifts P(any architecture NPV-positive) by < 15 pp vs its current verdict. | ΔP(NPV+) < 15 pp across the 34–56 t sweep | Falsified if ΔP(NPV+) ≥ 15 pp anywhere in 34–56 t. |
| H3 | R-clearing-price break-even $/t scales inversely with delivered tonnes and stays within [\$6M, \$13M] across 34–56 t. | break-even $/t ∈ [6, 13] M/t across band | Falsified if break-even $/t exits [6, 13] M/t at any swept point. |
| H4 | R-pricing-anchor-revisit's H7 verdict is invariant to the delivery correction (the round is purely \$/kg-based; it takes no delivered-tonnage input). | H7 verdict unchanged | Falsified if the corrected anchor changes R-pricing-anchor-revisit's H7 reading. |
| H5 | The pitch §4 table (50 t at 54%) is the only artifact that materially misstates revenue from the delivery error; the revenue *rounds* do not. | pitch table is the outlier; rounds robust | Falsified if any revenue round's headline verdict moves materially under the correction. |
| **H6 (load-bearing)** | The program-class financial verdict (sub-sovereign-bond / technology-demonstrator at conservative anchors) **does NOT flip anywhere in the 17–28% band** (nor at the 0 t conservative point). The delivery correction sharpens per-mission tonnage but is not the binding constraint — reactor-program availability (L0-24) and the chunk-mass cap bind first. | program-class verdict invariant across {0, 34, 42, 50, 56} t | Falsified if the program-class verdict crosses the sovereign-bond IRR hurdle (flips toward viable) at any delivered tonnage in the band. |

### Directional note (honest prior, recorded before re-runs)

Revenue per mission = clearing-price × delivered_t (monotone increasing in delivered_t). The revenue rounds currently use delivered_t ∈ {30, 42, 50, 80} t. Three of these (E_200 at 30 t below band; VariantB at 80 t far above band) are *not* in the corrected band; only E_500 at 50 t and clearing at 42 t are. **So I expect H1 to be FALSIFIED or split** — the demand-curve round in particular carries VariantB at 80 t, which at 17–28% retention requires capturing 286–470 t, a hard L1-007 cap violation. That is the M-3 fear partially realized for one architecture. But because reducing delivered_t can only *lower* P(NPV+), no "ruled out" verdict can flip toward viable; H6 should hold robustly even where H1 fails. The interesting output is therefore *which* rounds carried an above-cap optimistic anchor (H1/H5), not whether the verdict flips (H6 — predicted invariant).

A second-order note: the three demand-curve architectures (E_500kWe_200t, E_200kWe_100t, VariantB_500kWe) are all at power classes (200–500 kWe) the project owner retired as fantasy-conditioned (2026-05-19 directive). This round does not re-open that; it takes the rounds' `delivered_t` as the object of correction. Flagged for the reading.

---

## Method

1. **Anchor reconciliation.** Extract the per-mission `delivered_t` each of the three revenue rounds uses. Tabulate vs the corrected band (34–56 t) and the framework points (39.5 t constraints-off, 0 t constraints-on). Output: `results/anchor_reconciliation.csv`.
2. **Band sweep.** Re-run R-LEO-water-demand-curve and R-clearing-price-tail-integration with `delivered_t` swept over {0, 34, 42, 50, 56} t (corrected band + pitch headline 50 t reference + conservative 0 t). Capture each round's headline verdict metric (P(NPV+), P(any arch NPV+), break-even $/t) at each point. The demand round's MC clearing distribution is independent of delivered_t, so only the revenue→break-even comparison re-evaluates; the clearing round re-derives break-even $/t = cost / delivered_t. Output: per-round sweep JSON in `results/`.
3. **Chunk-cap interaction check.** For each delivered point, back out required captured tonnes = delivered / fraction at fractions {17%, 20%, 25%, 28%}; flag any (delivered, fraction) pair requiring > 200 t captured. Output rows in the sweep JSON.
4. **Verdict-flip detection.** For each round, determine whether the headline verdict flips anywhere in {0, 34, 42, 50, 56} t. Load-bearing H6 output: the program-class verdict across the band.
5. **R-pricing-anchor-revisit (H4) — structural, no re-run.** Confirm by inspection that `run.py` / `inverse_risk_check.py` take only `price_per_kg` and never delivered tonnage; the H7 verdict cannot move under a delivered-tonnage correction.
6. **Pitch-table reconciliation.** Produce the corrected §4 era-table delivered-tonnage column as a drop-in for the pitch rewrite (feeds R-pitch-arithmetic-audit C20/C26/C28 + PROPOSED-PITCH-DIFF). Output: `corrected_era_table.md`.
7. **Reading.** `READING.md` with H6 verdict + whether the delivery correction is financially load-bearing or merely a pitch-honesty fix.

---

## Out of scope

- Pinning the exact delivery fraction beyond what the parity round already provides. This round sweeps the band; the parity point (39.5 t / 0 t) is consumed as context, not re-derived.
- Re-deriving the delivery fraction itself (R-pitch-arithmetic-audit + R-framework-matrix-parity job).
- Re-opening L1-007 (200 t cap) or the retired 200–500 kWe power classes.
- Reactor-program availability / L0-24 (iapetus territory; orthogonal).
- Applying the pitch diff (`corrected_era_table.md` is a drop-in; orchestrator applies after project-owner ratification).

---

## Deliverables (commit order)

1. `STUDY.md` — this file (pre-registration frozen). [exp commit 1]
2. `run.py` + `results/anchor_reconciliation.csv` + per-round sweep JSON. [exp commit 2]
3. `corrected_era_table.md`. [exp commit 3]
4. `RESULTS.md` — verdict-flip table + H1–H6 scoring. [exp commit 4]
5. `READING.md` — H6 load-bearing reading. [exp commit 5]
6. Handoff to orchestrator (`~/.claude/handoffs/`).

---

## Where I could be wrong (pre-registered)

1. If a revenue round computes revenue from a *fraction* rather than a fixed `delivered_t`, the sweep semantics differ; I will read each harness before swapping inputs (verified for demand + clearing rounds: both use fixed `delivered_t`).
2. The framework's 0 t conservative reading makes the rounds trivially NPV-negative; if the project owner reads the program at the constraints-OFF physics envelope (~20%) rather than the matrix-faithful conservative one, the operative band is 34–56 t and the H6 verdict rests on the revenue/break-even margin, not on zero revenue. I report both readings explicitly.
3. The demand round's break-even table is anchored to retired power classes (R-fleet-ramp-NPV round-7). The break-even $M/mission values are taken as given; if those are themselves stale, the P(NPV+) levels shift — but the *direction* of the delivery correction (lower delivered_t → lower P(NPV+)) is robust to that.
