# R-kilopower-scale-up-credibility — is 30 kilowatt-electric defensibly Kilopower-extrapolation, or does it quietly re-import the retired 500 kilowatt-electric fantasy?

**Status:** scope, pre-study. Authored by Saturn (orchestrator), 2026-05-19 latest+13, after titan-3's R-chunk-size-pareto closure cell surfaced at P = 30 kilowatt-electric Kilopower-extrapolation and the project-owner directive retired the 500 kilowatt-electric power class as fantasy-conditioned.

---

## Why this round

titan-3's R-chunk-size-pareto (`1997a51`) found a non-empty closure cell at 40-80 tonne chunks + 30 kilowatt-electric reactor power + R12 lunar-gravity-assist Earth-arrival. Strict L0-05 closures sit at P=30 kilowatt-electric (none at P=10 or 15). This is **3× outside titan-3's own 1-10 kilowatt-electric "flyable Kilopower-extrapolation" envelope** defined in R-kilowatt-class-power-envelope (`5162735`) earlier the same day, and **outside the locked-memory directive** ("Kilopower-class single-kilowatt fission at best"; feedback memory `feedback_no_large_fission.md`).

This round is the load-bearing engineering audit on matrix decision point #14. **The titan-3 closure cell does not become a state-of-record finding for the matrix until this round either survives or kills the 30 kilowatt-electric assumption.** If the round kills it, ICEBERG has no flyable-power closure cell and the campaign moves to decision #15 (L0-04 strict + accept campaign termination at flyable power, or waive to Saturn-system depot). If the round survives it, the closure cell becomes real and decision #14 resolves toward option (a) (soften directive to admit 30 kilowatt-electric Kilopower-extrapolation).

**Round type:** primary-sources research + Bayesian conjunction synthesis. NOT a closed-form physics round. The worker fetches primary documents (NASA Glenn / Los Alamos / Sandia reports on KRUSTY, Department of Energy + NASA Fission Surface Power Phase 1 awards, August 4 2025 Duffy directive text if accessible, National Academies 2021 Space Nuclear Propulsion report, post-mortem references on cancelled programs SP-100 / Project Timberwind / Prometheus / DRACO) and composes the evidence into a defensible probability bracket on 30 kilowatt-electric Kilopower-extrapolation in the ICEBERG demonstrator window 2032-2035.

---

## The four locked external findings this round must respect

These are user-locked beliefs from R-power-wonder, May 2026. The round MUST anchor against them, not litigate them:

1. **The 40 watts-per-kilogram specific-power assumption is paper-aspirational at Technology-Readiness-Level 2**, not extrapolated from Kilopower Reactor Using Stirling Technology ground-test data. Flown radioisotope thermoelectric generators top at ~5.3 W/kg; KRUSTY measured ~2.4 W/kg system-level.
2. **United States space-fission programs have a 0-of-6 base rate** of reaching orbit within their originally-stated decade since 1965. SNAP-10A (1965) is the only United States fission reactor ever orbited. ~$1.7B spent post-SNAP with zero orbital outcomes.
3. **NASA Fission Surface Power Phase 2 has NOT been awarded as of May 2026.** Phase 1 awards June 2022; contracts extended January 2025 rather than rolled into Phase 2. August 4 2025 Duffy directive raised scope to 100 kilowatt-electric with "Q1 FY2030 deployment intent" (policy direction, not a contract). Draft Announcement for Partnership Proposals issued August 29 2025; final release anticipated early 2026. Same Fiscal Year 2026 budget request zeroed NASA nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines entirely. DARPA DRACO cancelled May 30 2025.
4. **At megawatt-electric scale, radiator subsystem is 40-55 percent of system mass**, not the reactor core. Modular Assembled Radiators for Very Large systems studies anchor this. The 40 W/kg target bets on deployable ultra-low-areal-density radiators that have not flown.

These four findings together say: the United States space-fission landscape is a known cancellation graveyard with one orbital success in sixty years. Any specific-power or scope claim above flown anchors needs an extraordinary-evidence threshold to be load-bearing.

---

## The question this round answers

**For each candidate path from KRUSTY's flown anchor (1 kilowatt-electric, 28-hour ground test, 2.4 watts-per-kilogram system-level, 2018) to titan-3's required design point (30 kilowatt-electric, ~10-year cumulative full-power burn life, 2032-2035 demonstrator-window delivery), what is the credibility of that path?** Three candidate paths:

- **Path A (single-unit scale-up):** Build a single fission reactor that is 30× the Kilopower core scale at comparable specific power. Closest precedent: Fission Surface Power Phase 1 design point (40 kilowatt-electric scope, three competing designs in 2022 awards). 30 kilowatt-electric sits just below Phase 1 scope; Phase 1 design heritage transfers if Phase 2 awards and delivers.
- **Path B (parallel modules):** Build 30× 1-kilowatt-electric Kilopower modules and run them in parallel as a power plant. Each module is single-unit Kilopower-class per the locked-memory directive. Mass penalty: 30× the reactor cores, shields, controls — though the per-core mass at small scale may be more favourable than the linear extrapolation suggests.
- **Path C (intermediate scale-up + intermediate count):** Build N reactors of scope k kilowatt-electric each, where N × k = 30. Trade-space across (N, k) ∈ {(1,30), (2,15), (3,10), (6,5), (10,3), (30,1)}. Path A is N=1; Path B is N=30.

For each path, audit:
1. **Technical credibility:** what existing reactor programs / design heritage support this path? What is the engineering gap between flown anchors and the design point?
2. **Programmatic credibility:** what is the probability that a United States or allied space-fission program delivers this path inside the 2032-2035 window? Anchor on the 0-of-6 base rate + Fission Surface Power Phase 2 status + Defense Advanced Research Projects Agency Demonstration Rocket for Agile Cislunar Operations cancellation pattern.
3. **Lifetime credibility:** KRUSTY's 28-hour ground-test heritage is 3-4 orders of magnitude short of the 8-12 year cumulative burn (per enceladus-r5 R-reactor-lifetime-vs-burn-time `c685c52`). What program profile would bring lifetime in range, and what is its probability inside the window?

The round's deliverable is a **synthesis table for the project owner**: rows are candidate paths A / B / C; columns are technical credibility / programmatic credibility / lifetime credibility / joint conjunction posterior / "is this defensibly Kilopower-extrapolation under the locked-memory directive?" (yes / no / project-owner-call).

---

## Pre-registered hypotheses (worker's honest predictions)

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | Path A (single 30-kilowatt-electric reactor) is NOT defensibly Kilopower-extrapolation — it is FSP-Phase-1-extrapolation. The closest design heritage is the 40-kilowatt-electric Fission Surface Power Phase 1 awards (Lockheed Martin / Westinghouse / IX joint venture), not Kilopower. Re-framing it as Kilopower-extrapolation is the same fantasy-conditioned move the project-owner directive retired. | Path A: NOT Kilopower-extrapolation; requires Fission Surface Power Phase 2 award. | H1 falsified if there is documented engineering work mapping Kilopower's Stirling-conversion architecture to 30 kilowatt-electric without a step change in thermal-conversion technology. |
| H2 | Path B (30× parallel 1-kilowatt-electric Kilopower modules) is technically defensible as Kilopower-extrapolation but pays a severe specific-power penalty. Mass-per-unit-power for 30 parallel units is meaningfully worse than 30 kilowatt-electric in a single unit, because shield mass, controls, and structure don't scale favorably with parallel-module count. Effective specific power < 1 watts-per-kilogram (vs KRUSTY's 2.4 single-unit). | Path B effective system specific power: < 1 W/kg system-level. | H2 falsified if a credible engineering argument puts parallel-module effective specific power at ≥ 2 W/kg system-level. |
| H3 | Path B mass penalty falsifies titan-3's R-chunk-size-pareto closure cell. The closure-cell reactor mass budget at P=30 kilowatt-electric and sp=2.4 W/kg was 12.5 tonnes. If Path-B effective specific power is <1 W/kg, reactor mass exceeds 30 tonnes — larger than the 40-80 tonne chunk budget can absorb. | Path B implies reactor mass > chunk budget; closure cell collapses. | H3 falsified if titan-3's closure cell survives at Path-B effective specific power. |
| H4 | Path C (intermediate (N, k) combinations) has no committed United States program at any N × k = 30 design point inside the 2032-2035 demonstrator window. Posterior probability of any United States or allied program delivering ≥ 30 kilowatt-electric AND ≥ 5 year cumulative full-power lifetime AND ≥ 5 W/kg specific power inside 2032-2035 is ≤ 1 percent under the 0-of-6 base rate prior. | Joint posterior ≤ 1 percent. | H4 falsified if a credible argument puts the joint posterior > 5 percent. |
| H5 | The honest answer to decision point #14 is option (b) (hold the locked-memory directive at strict single-kilowatt Kilopower-class) OR option (c) (require a Kilowatt-scale-up-credibility audit — i.e., this round). Option (a) (soften directive to admit 30 kilowatt-electric Kilopower-extrapolation) is structurally indefensible because there is no Kilopower-extrapolation path to 30 kilowatt-electric that is consistent with the locked-memory directive. | Reading-level: option (b) or (c) is the honest answer; (a) is not. | H5 falsified if H1 + H2 + H3 + H4 jointly admit a path to 30 kilowatt-electric that survives the locked-memory directive. |
| H6 (project-owner-facing) | The titan-3 R-chunk-size-pareto closure cell, taken seriously, requires either Fission Surface Power Phase 2 + Phase 2 delivery within ICEBERG's 2032-2035 demonstrator window (joint posterior ≤ 1 percent per H4 + locked finding 3) OR a Path-B parallel-module mass penalty that collapses the cell on its own propellant accounting. Therefore: **the closure cell is fantasy-conditioned in the same sense as the prior 500 kilowatt-electric cells, just with a softer-sounding power class name.** The matrix should not carry it as state-of-record. | Reading-level: the closure cell is NOT load-bearing; ICEBERG has no surviving cell at flyable power. | H6 falsified if H5 falsifies. |

If H6 holds, the campaign returns to the iapetus tech-demonstrator-only framing as the honest reading and decision point #15 becomes the only live ICEBERG architectural question. If H6 falsifies, the closure cell becomes real and the matrix re-anchors.

---

## Method (worker drafts the actual research + computation)

**Step 1 — Primary-sources fetch.** Workers should pull and cite primary documents, not Wikipedia or speculation. Required sources at minimum:

- KRUSTY: NASA Glenn / Los Alamos National Laboratory 2018 ground-test report (Gibson, McClure, et al.). System-level specific power, test duration, thermal-conversion architecture (Stirling), and Technology Readiness Level at end of test.
- Kilopower design family: design-point papers for 1, 3, 5, 10 kilowatt-electric Kilopower variants. Mass breakdowns. None of these flew; they are all paper studies above 1 kilowatt-electric.
- NASA Fission Surface Power Phase 1: June 2022 awards (Lockheed Martin, Westinghouse, IX joint venture, $5M each, 40 kilowatt-electric design point). January 2025 extensions. August 4 2025 Duffy directive (100 kilowatt-electric scope, Q1 Fiscal Year 2030 deployment intent). August 29 2025 Draft Announcement for Partnership Proposals.
- Cancelled-program post-mortems: SP-100 (~$400M spent, cancelled 1994), Project Timberwind (~$340M, 1993), Prometheus / Jupiter Icy Moons Orbiter (~$464M, 2006), Defense Advanced Research Projects Agency Demonstration Rocket for Agile Cislunar Operations (~$499M ceiling, cancelled May 2025). What technical milestone did each program hit before cancellation, and how far below 30 kilowatt-electric flown power?
- National Academies 2021 Space Nuclear Propulsion report — specific text on "very little advancement in nuclear-electric-propulsion in the past decade."

**Step 2 — Technical-credibility assessment for each path A / B / C.** For Path A, identify the Fission Surface Power Phase 1 design heritage and the engineering gap between Phase 1 (40 kilowatt-electric, surface-deployed, no flight heritage) and titan-3's design point (30 kilowatt-electric, spaceflight). For Path B, compute mass breakdown for 30 parallel 1-kilowatt-electric Kilopower modules including shields, controls, structure, thermal interfaces. For Path C, evaluate the intermediate (N, k) points using interpolation between Path A and Path B mass breakdowns.

**Step 3 — Programmatic-credibility Bayesian posterior.** Apply hyperion R-power-bayesian-update three-prior bracket (2.9-8.9 percent posterior on any United States fission orbit by 2035) as the unconditional prior. Condition on "delivers ≥ 30 kilowatt-electric" and "delivers ≥ 5 year lifetime" and "delivers ≥ 5 W/kg specific power" — these conditionals can be bounded from known program scope and cancellation post-mortems. For each candidate path, compute the joint posterior probability of delivery inside ICEBERG demonstrator window 2032-2035.

**Step 4 — Mass-budget feedback into titan-3's closure cell.** Take the effective system specific power from Step 2 for each path and re-run titan-3 R-chunk-size-pareto's reactor mass calculation for P=30 kilowatt-electric. If reactor mass exceeds the 40-80 tonne chunk budget, the closure cell collapses on physics grounds independent of programmatic credibility.

**Step 5 — Decision-frame synthesis.** Produce a synthesis table (rows: paths A / B / C; columns: technical credibility / programmatic posterior / mass-budget feedback verdict / locked-memory-directive compliance / overall verdict). The reading-level recommendation to project-owner is the answer to decision point #14: which of (a) / (b) / (c) is the honest choice given the audit?

---

## Anchor cell and audit handles

Anchor cell for hand-verification: titan-3 R-chunk-size-pareto's anchor at P=30 kilowatt-electric, sp=2.4 W/kg, chunk=60 tonnes. Reactor mass at sp=2.4 is 12.5 tonnes (= 30,000 / 2.4 / 1000). Dry mass + chunk = 60 + bus + electrolysis + thruster + reactor. If Path-B effective specific power drops to 1 W/kg, reactor mass becomes 30 tonnes — half the chunk. The closure cell's propellant accounting (Tsiolkovsky on residual Δv) needs to be re-run at the new dry mass to see if the cell survives.

Cross-check against enceladus-r5 R-arch-E-specific-power-flown-anchored (`62f7079`) which already found that at 2.4 W/kg (KRUSTY), 0 of 60 cells close at 25-year ceiling under Architecture E (no Saturn-side electrolysis, 200-tonne chunk). titan-3's closure cell is at 40-80 tonne chunks, not 200, so the cell sizes are different — but the underlying reactor mass calculation is the same and the worker should reconcile.

---

## Out-of-scope guards

- Do NOT re-litigate the locked-memory findings 1-4. They are user-locked beliefs; this round anchors against them.
- Do NOT re-derive titan-3's R-chunk-size-pareto closure tables. Use them as input.
- Do NOT propose new architectural alternatives (e.g., a different propulsion class). This round is narrow: is 30 kilowatt-electric defensibly Kilopower-extrapolation? Yes / no / project-owner-call.
- Do NOT edit shared docs (matrix, REQUIREMENTS, design-axes, SESSION-LOG, active-sessions). Produce findings; orchestrator integrates.

---

## Expected deliverables

- `STUDY.md` with pre-registered hypotheses (above), method, results, hypothesis grades, reading-level recommendation.
- `run.py` (or `analysis.py`) for the Bayesian conjunction synthesis and mass-budget feedback.
- `results/` directory with synthesis table, primary-source citation index, audit cross-check against enceladus-r5 R-arch-E-specific-power-flown-anchored.
- Worker handoff at `~/.claude/handoffs/iceberg-NAME-YYYYMMDD-kilopower-scale-up.md`.

---

## What this round does NOT resolve

- Decision point #15 (L0-04 strict deliver-to-Earth-orbit). Orthogonal to this round.
- R-lunar-gravity-assist-risk-budget (titan-3's 10-flyby tour risk audit). Independent failure mode; needs its own round.
- R-saturn-aerocapture-feasibility (Saturn arrival via aerocapture was assumed by titan-3). Independent failure mode.
- R-rhea-heterogeneous-cadence-refresh-at-40-80t-chunks (economic verdict on the new chunk band). Downstream of this round closing positive.

If this round closes negative (H6 holds), most of the downstream candidates become moot — the closure cell does not exist and the audit cycle moves to decision #15.

---

## Suggested worker

Any moon. The round is research-heavy + light Bayesian synthesis; favours a worker with appetite for primary-source pulls. Iapetus has demonstrated this pattern (R-reactor-specific-power-program-targets, R-T1-sensitivity-and-breakeven). Hyperion has the R-power-base-rate prior already in heritage. Either fits.

---

## Connection to matrix decision points

- Decision #14 (reactor power class for closure cell): **this round produces the audit input.**
- Decision #5 (reactor program path): the round refines the 30 kilowatt-electric option that decision #5 currently flags.
- Decision #1 (program class) and decision #13 (pitch staged-options reframe): downstream — if this round closes negative, the iapetus tech-demonstrator framing is reinforced; pitch revision should not yet assume the titan-3 closure cell is real until this round runs.
