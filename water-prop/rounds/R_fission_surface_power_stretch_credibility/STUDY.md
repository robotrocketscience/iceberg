# R-fission-surface-power-stretch-credibility

**Owner session:** enceladus-r5 (resumed 2026-05-15)
**Branch:** iceberg-enceladus-r5
**Status:** PRE-REGISTERED (hypothesis frozen before run)
**Builds on:** R-saturn-side-solar-thermal (commit `0fcab42`), R-saturn-shadow-and-station-location (commit `b39e7a5`), and the initial-pass enceladus-r5 cascade in R-chemical-plus-small-reactor (commit `1d48cb2`).

---

## Motivation

Round-2 of this resumed pass reframed the prior verdict to *"Saturn-side-Technology-Readiness-Level-bet-limited, fission-stretch and solar-thermal in same credibility band."* The credibility-band claim has two halves:

1. Solar-thermal-with-solid-oxide-electrolyzer at low mirror areal density is a Technology-Readiness-Level-2-to-3 bet.
2. Fission-Surface-Power at 10-watts-per-kilogram stretch specific power is also a Technology-Readiness-Level-2-to-3 bet.

Round 1 established (1). This round tests (2) quantitatively. If the fission-stretch posterior collapses to substantially below the solar-thermal posterior (e.g. 0.5–1 percent vs 4–10 percent), the same-credibility-band claim is wrong in the *opposite* direction from the prior enceladus-r5 verdict: D-fission would be *less* credible than D-solar-thermal, and the matrix annotation should reflect that.

The initial-pass enceladus-r5 cascade in R-chemical-plus-small-reactor placed Architecture-D unconditional posterior at 0.07–0.15. That cascade was program × specific-power × per-mission-completion. This round re-derives the cascade with explicit prior elicitation from the locked beliefs and policy evidence as of May 2026, using Monte Carlo over plausible parameter ranges rather than point estimates.

## Cited evidence (from locked beliefs and project-level context)

- **National Academies 2021 Space Nuclear Propulsion report.** Notes "very little advancement" in nuclear-electric-propulsion in the past decade. The 40-watts-per-kilogram megawatt-class figure is paper-study, Technology-Readiness-Level 2. (Locked belief 1.)
- **Kilowatt Reactor Using Stirling Technology demonstrated 2018.** System-level 2.4 watts-per-kilogram. (Locked belief 1.)
- **Flown radioisotope thermoelectric generators top out at ~5.3 watts-per-kilogram** (General Purpose Heat Source). (Locked belief 1.)
- **US space-fission base rate: 0-of-6 reached orbit within the originally-stated decade since 1965.** SNAP-10A (1965) is the only US fission reactor ever orbited; SP-100, Project Timberwind, Prometheus/JIMO, DARPA DRACO, Kilopower flight, Fission-Surface-Power Phase 2 all failed or remain unfunded as of May 2026. ~$1.7B spent post-SNAP with zero orbital outcomes. (Locked belief 2.)
- **Fission-Surface-Power Phase 1** awarded June 2022, $5M each to Lockheed Martin, Westinghouse, and Intuitive Machines / X-energy joint venture. Contracted to 40-kilowatt-electric class at 5-watts-per-kilogram specific power. Phase 1 contracts extended January 2025. (Locked belief 3.)
- **August 4 2025 Duffy directive** raised scope to 100 kilowatts-electric with "Q1 FY2030 deployment intent." Policy direction, not a contract. (Locked belief 3.)
- **Draft Announcement for Partnership Proposals** issued August 29 2025; final release anticipated early 2026. As of May 2026, Phase 2 has NOT been awarded. (Locked belief 3.)
- **FY2026 budget request zeroed NASA nuclear-electric-propulsion and nuclear-thermal-propulsion technology lines.** DARPA DRACO cancelled May 30 2025. (Locked belief 3.)
- **Pattern: scope grew (40 to 100 kilowatts-electric) while schedule held.** Historically precedes either large funding ask or quiet de-scope. (Locked belief 3.)

I have no live web access in this session and cannot link primary sources directly. All citations are by name and date from the locked-belief evidence above. The reader who wants primary documents should retrieve them by those names.

## Hypothesis (H-fission-stretch-credibility)

**Pre-registered numeric prediction.**

Decompose the question *"Is Architecture-D-fission's Saturn-side reactor at 10-watts-per-kilogram specific power delivered to Saturn orbit by ICEBERG launch (2035 nominal)?"* into a Bayesian cascade. Per-stage prior ranges (pre-registered before Monte Carlo):

| Stage | Probability range | Anchor |
|---|---|---|
| 1. Fission-Surface-Power Phase 2 awarded by end of fiscal year 2027 | 0.30–0.65 | Draft Announcement issued August 2025; final release anticipated early 2026; FY26 budget zeroed NEP/NTP lines is hostile context; Phase 1 extension Jan 2025 rather than rolling into Phase 2 suggests delay; recent Duffy directive intent is supportive |
| 2. Phase 2 commits to 10-watts-per-kilogram stretch (not Phase-1-baseline 5-watts-per-kilogram) given awarded | 0.35–0.70 | Scope raise from 40 to 100 kilowatts-electric makes mass more binding, supporting stretch target; but Phase-1 contracted 5 W/kg and Phase-2 RFP language not yet public |
| 3. 10-watts-per-kilogram achieved on ground/flight demonstrator by 2032 given committed | 0.10–0.35 | KRUSTY achieved 2.4 W/kg at 1 kWe scale; National Academies "very little advancement"; 4× specific-power scale-up plus 100× power scale-up; some uplift for industry capability |
| 4. Flight demonstrator launched and operating in space by 2035 given ground-qualified | 0.15–0.40 | 0-of-6 historical base rate gives Jeffreys-prior P~0.125; SpaceX-era launch capacity uplift ×1.5–2; Q1 FY2030 deployment intent supportive but historically schedules slip |
| 5. ICEBERG can integrate Phase-2 demonstrator design at 200–300 kilowatts-electric Saturn-orbit role given flight success | 0.40–0.75 | Phase-2 is 100 kWe; ICEBERG-D-fission target is 200–300 kWe; scaling 2–3× from a qualified demonstrator generally easier than building from zero, but not free; IP and contracting questions left aside |

**Predicted point estimates** (multiplying midpoints):
- Pessimistic (lower-end of each range): 0.30 × 0.35 × 0.10 × 0.15 × 0.40 = **0.00063** (≈ 0.06 percent)
- Mid (midpoint of each range): 0.475 × 0.525 × 0.225 × 0.275 × 0.575 = **0.0090** (≈ 0.9 percent)
- Optimistic (upper-end of each range): 0.65 × 0.70 × 0.35 × 0.40 × 0.75 = **0.0478** (≈ 4.8 percent)

**Falsification rule (pre-registered):**

The hypothesis *"D-fission is in the same credibility band as D-solar-thermal at 4–10 percent unconditional posterior"* is **upheld** if the Monte-Carlo 50th-percentile (median) lands in [0.03, 0.10] — i.e. the credibility-band overlap holds at one standard deviation.

The hypothesis is **falsified** if:
- Median < 0.02 — D-fission is meaningfully less credible than D-solar-thermal (the round-1-2 same-band claim is wrong in the conservative direction).
- Median > 0.15 — D-fission is meaningfully more credible (the prior enceladus-r5 cascade was right; round-2's same-band reframe was wrong in the generous direction).

## Flight-heritage survey

| Component | Heritage status (as of May 2026) |
|---|---|
| Fission reactor in low-Earth orbit | SNAP-10A 1965 (one flight, 43 days). HERITAGE-AVAILABLE for the *concept*; HERITAGE-NONE for modern specific-power targets. |
| Kilopower-class reactor (1–10 kWe, ~2.4 W/kg system-level) | KRUSTY ground demonstrator 2018. HERITAGE-NONE for space. |
| 40-kWe-class reactor at 5 W/kg | Fission-Surface-Power Phase 1 contracted design. HERITAGE-NONE — no flight, no full-scale ground test as of 2026. |
| 100-kWe-class reactor at 10 W/kg | Fission-Surface-Power Phase 2 stretch target. HERITAGE-NONE — Phase 2 not awarded; no demonstrator. |
| 200–300-kWe-class reactor (ICEBERG D-fission target) | HERITAGE-NONE. No funded program. |

All five stages of the cascade transit Technology-Readiness-Level boundaries with no flight heritage above SNAP-10A. The base rate is the right anchor.

## Test

`run.py` runs 100,000-sample Monte Carlo over the five-stage cascade using uniform priors over the pre-registered ranges. Outputs the posterior distribution, percentile summary, and credibility-band comparison against the solar-thermal posterior 0.04–0.10 from rounds 1–2.

Output to `results/cascade_montecarlo.json` and `results/tables.md`.

## Result

100,000-sample Monte Carlo, seed 20260515.

| Statistic | D-fission posterior | D-solar-thermal posterior |
|---|---|---|
| Mean | 0.0089 (0.9%) | 0.0242 (2.4%) |
| Median | 0.0078 (0.78%) | 0.0203 (2.0%) |
| 5th percentile | 0.0029 | 0.0055 |
| 25th percentile | 0.0052 | 0.0120 |
| 75th percentile | 0.0114 | 0.0330 |
| 95th percentile | 0.0187 (1.87%) | 0.0555 (5.55%) |
| P(posterior > 0.02) | 0.036 | 0.509 |
| P(posterior > 0.05) | 0.000 | 0.078 |
| P(posterior > 0.10) | 0.000 | 0.000 |

**Pre-registered classification:** `FALSIFIES_REFRAME_lower_than_solar_thermal`. D-fission median 0.78 percent is below the 2-percent threshold for the same-credibility-band claim from round 2.

## Reading

**Round 2's same-credibility-band claim is wrong in the generous direction (toward fission).** Under the locked-belief evidence and the pre-registered conditional ranges, D-fission posterior median is 0.78 percent (95th percentile 1.87 percent) — about 2.6× lower than D-solar-thermal median 2.0 percent (95th percentile 5.6 percent). The P(D-fission posterior > 5 percent) is zero across 100,000 samples; the P(D-solar-thermal posterior > 5 percent) is 7.8 percent.

**The corrected ordering is D-solar-thermal > D-fission, with both well below the 5 percent threshold of any meaningful confidence.** The matrix annotation should not be "same credibility band" but rather "both Saturn-side power paths have credibility below 5 percent unconditional; solar-thermal is structurally less program-risk-bound than fission."

**Why fission posterior collapses below the prior enceladus-r5 0.07-0.15.** The initial-pass cascade in R-chemical-plus-small-reactor used three stages (program × specific-power × per-mission completion) at point-midpoint values that implicitly assigned P(program) ≈ 0.5-0.8 and P(completion) ≈ 0.5-0.85. My five-stage cascade with locked-belief-anchored ranges gives P(Phase 2 awarded) × P(commits 10 W/kg) ≈ 0.475 × 0.525 = 0.25, and P(flight) × P(integration) ≈ 0.275 × 0.575 = 0.158. The initial-pass cascade was approximately 3× too generous at "program" and 4× too generous at "completion." The added context that justifies tighter ranges:
- 0-of-6 historical base rate (locked belief 2) — not previously priced in.
- FY2026 budget request zeroing NEP/NTP technology lines (locked belief 3) — hostile context.
- August 2025 Duffy directive is policy direction, not a contract.
- Draft Announcement issued August 2025; no final Announcement or award as of May 2026.
- Phase 1 extension in January 2025 *instead of* rolling into Phase 2.

**Structural advantage of solar-thermal that the cascade does not fully capture.** My solar-thermal cascade has four stages (mirror qualification × solid-oxide-electrolyzer qualification × Saturn-orbit conops × per-mission completion) with no "program funded" stage gating the technology development. This is defensible because:
- Inflatable concentrator development has multiple funding paths (commercial space, solar-sail follow-ons like NEA Scout, defense satellite-segment work). No single program gates it.
- Solid-oxide-water-electrolyzer development is funded by the terrestrial hydrogen economy (Department of Energy Hydrogen Shot, Inflation Reduction Act 2022 hydrogen-production tax credit of approximately $3 per kilogram, multi-billion-dollar industry investment). Space adaptation is marginal cost on a mature commercial technology.
- Fission has no commercial parallel funding equivalent for spaceflight applications. Every U.S. space-fission program has been government-funded through NASA or DARPA.

This is a structural credibility advantage for solar-thermal that is *worth* its lower stage count, not an artifact of my decomposition.

**Three caveats on the magnitude of the gap.**

1. *I had no live web access for this round.* All cited evidence is from the locked beliefs. A reader retrieving primary documents (Phase 2 Draft Announcement, FY2026 budget testimony, Duffy directive memo) might find context that shifts individual stage probabilities by ±10 percentage points. The directional finding (D-solar-thermal > D-fission) is robust to that level of perturbation; the magnitude (2.6× factor) is less robust.

2. *Sensitivity to stage decomposition.* If I bundled Phase-2-awarded and commits-to-stretch into one stage at the midpoint of 0.475 × 0.525 = 0.25 with the same range, the cascade collapses by one factor. But splitting them is correct: a Phase 2 contract could be awarded at the Phase-1 5-watts-per-kilogram specification without stretching to 10 watts-per-kilogram. These are distinct events.

3. *Uniform priors are conservative-but-defensible.* I used uniform over the elicited ranges. A reasonable alternative would be triangular or beta priors weighted toward the elicited midpoints; this would tighten posteriors but not shift the medians meaningfully.

**Implication for the architecture matrix.** Both D-fission and D-solar-thermal have unconditional posteriors below 5 percent. Neither is a credible 2035-baseline. The matrix should pursue a third architecture or relax L0-05 (mission timeline) to admit non-Saturn-side-electrolysis approaches. Possibilities:
- Architecture B (all-chemical, chunk-fed Saturn-departure) under a relaxed L0-05 of 25–30 years.
- Architecture E (no Saturn-side electrolysis at all; both legs chunk-fed; cadence × 2 to compensate).
- Hybrid solar-electric outbound with no Saturn-side electrolysis.

The prior enceladus-r5 verdict *"either accept the fission bet, relax L0-05, or abandon"* should be sharpened to *"accept a sub-5-percent-posterior credibility bet (either path), or relax L0-05 to 25–30 years, or abandon."*

## Revisit

**Pre-registered prediction vs measured:**

| Statistic | Predicted (midpoint multiplication) | Measured (Monte Carlo median) | Held? |
|---|---|---|---|
| D-fission point estimate (pessimistic) | 0.00063 | n/a (Monte Carlo p05 = 0.0029) | held loosely; range overlaps |
| D-fission point estimate (mid) | 0.0090 | 0.0078 | held |
| D-fission point estimate (optimistic) | 0.0478 | 0.0187 (p95) | not held — Monte Carlo p95 is lower than my point-multiplication upper bound by 2.5× |

**Why the optimistic point estimate missed.** Multiplying the upper-end of each range (0.65 × 0.70 × 0.35 × 0.40 × 0.75 = 0.0478) implicitly assumes perfect positive correlation across stages. The Monte Carlo with independent uniform draws gives the 95th percentile at 0.0187 because each stage's upper-end is rarely sampled simultaneously. This is a *correct* mathematical behavior of the Monte Carlo — independent draws of bounded uniforms have a tighter joint distribution than the product of endpoints. The pre-registered point estimates were therefore overstating uncertainty width; the Monte Carlo is the right answer.

**Falsification verdict.** Hypothesis (D-fission and D-solar-thermal same credibility band) **falsified** at the lower-than-solar-thermal direction. Median 0.78 percent < pre-registered 2 percent floor. Solar-thermal median 2.0 percent > 2.5× fission median.

**Recurring-lesson-seven check.** Did I avoid the methodology bug from rounds 1 and 2 (anchoring on one regime, extrapolating without arithmetic)? Yes — I explicitly multiplied midpoints in the pre-registration and the Monte Carlo confirmed the calculation. The miss on the optimistic point estimate is a Monte-Carlo-vs-point-multiplication issue, not an arithmetic-skipped issue. Lesson appears genuinely internalized; protocol update from round 2 helped.

## Cross-learning

**Backward references:**

- **R-saturn-side-solar-thermal (round 1, commit `0fcab42`):** the round-1 finding "solar-thermal optimistic case ties Fission-Surface-Power stretch at 101 kg/kW" was a *technical* same-band claim (hardware mass parity at aggressive technology assumptions). This round shows that even when the hardware is parity, the credibility of *achieving* the aggressive technology assumptions differs — solar-thermal is more credible because of program-funding diversification. Hardware parity does not imply program-risk parity.
- **R-saturn-shadow-and-station-location (round 2, commit `b39e7a5`):** the "same credibility band" reframe is qualified: solar-thermal is structurally higher-credibility than fission because of commercial-tech funding leverage. The right matrix annotation is *"both paths below 5 percent unconditional; solar-thermal preferred for credibility but only in Saturn orbit; fission location-agnostic but lower credibility."*
- **R-chemical-plus-small-reactor (initial-pass enceladus-r5, commit `1d48cb2`):** the initial-pass cascade was approximately 3× too generous at the program stage and 4× too generous at the completion stage. The 0.07–0.15 unconditional posterior should be revised downward to 0.005–0.020 under locked-belief-anchored priors.
- **Locked beliefs 1–4:** all four power findings now have direct posterior consequences. The 0-of-6 base rate (belief 2) and FY2026 budget context (belief 3) are the largest single drivers of the lower D-fission posterior; the radiator-mass MARVL correction (belief 4) drove rounds 1–2; the 40-watts-per-kilogram-is-Technology-Readiness-Level-2 finding (belief 1) drove stage-3 probability range.

**Forward references / spawned threads:**

- **R-architecture-E-no-saturn-side-electrolysis:** if both D-fission and D-solar-thermal are below 5 percent unconditional, the most-credible non-fission path may be Architecture E (no Saturn-side electrolysis at all). Both legs chunk-fed, no inbound process power. Cadence × 2 to compensate for half the propellant. Mass and delta-velocity closure to compute.
- **R-architecture-B-with-L0-05-relaxation:** explicit posterior calculation for Architecture B under relaxed timeline (25–30 years). Plausible non-fission, non-process-power baseline?
- **R-program-funding-diversification-credit:** more rigorous accounting for the structural credibility advantage of dual-use commercial technologies (solid-oxide-electrolyzer, inflatable structures, photovoltaics) over single-program-gated technologies (fission). Could the matrix annotation include a "funding-path multiplicity factor" by default?
- **Matrix update (orchestrator):** D-fission cell unconditional posterior should drop from 0.07–0.15 to 0.005–0.020 (Monte-Carlo p05–p95). D-solar-thermal cell should be added at 0.005–0.055 (Monte-Carlo p05–p95). Annotation: both below 5 percent; solar-thermal structurally less program-risk-bound; both require relaxed L0-05 or strong-bet acceptance to baseline ICEBERG launch by 2035.

**Methodology note:** this round used Monte Carlo for a Bayesian cascade for the first time in this session. The Monte Carlo correctly tightened the joint distribution relative to point-endpoint multiplication. Future rounds with cascades of 4+ stages should default to Monte Carlo rather than point estimates. Pre-registration of point estimates remains useful as a sanity check on the Monte Carlo midpoint.

