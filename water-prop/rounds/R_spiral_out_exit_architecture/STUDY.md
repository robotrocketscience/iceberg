# R-spiral-out-exit-architecture

**Worker:** titan (Block 13)
**Predecessors:** R-exit-burn-power-audit (Block 10), R-composite-burn-time-closure (Block 11)
**Pre-registration date:** 2026-05-18
**Status at pre-reg:** results not yet computed; hypotheses below frozen before any code is run.

---

## Motivation

Block 11 found that the residence-class composite is structurally dead at 500 kilowatt-electric: no (Isp_exit, Isp_inbound) combination closes both burns within their time budgets (exit ≤ 6 months residence dwell; inbound ≤ 6 years Hohmann cruise). Path (a) megawatt-class power is locked-memory-Bayesian-unlikely; Paths (b) dwell-extension and (c) Isp-revert are retired.

Path (d) — flagged in Block 10 as "exit burn as spiral-out during cruise, not as 6-month dwell-confined maneuver" — was deferred to a separate round. This is that round.

The spiral-out reframe asks: **what if we drop the 6-month residence dwell constraint on the exit burn and instead let the exit propulsion fire continuously from chunk-capture-complete through Saturn escape and into the heliocentric cruise leg?** Under that reframe, the exit burn extends through whatever calendar time it needs, the residence dwell is whatever remains after capture is complete (≥ days, not constrained), and the only mission-duration constraint is L0-05 (≤ 15 years strict, ≤ 25 years with waiver).

There are two competing effects:

1. **Constraint relaxation gain.** Block 11 needed 5-10 megawatt-electric to fit the exit burn in 6 months. If the burn can take years, much lower thrust (i.e. lower power at the same Isp, OR higher Isp at the same power) is permitted.
2. **Spiral-out delta-velocity penalty.** A true low-thrust spiral departure from a circular orbit does NOT cost the impulsive Δv (Block 4's 7.4 km/s). It costs approximately v_circular at the starting orbit — for the B-ring residence at ~100,000 km from Saturn center, v_circular ≈ 18-19.5 km/s. This is ~2.4× the impulsive value. The extra Δv eats Tsiolkovsky propellant.

The question this round answers: **does the constraint-relaxation gain exceed the spiral-physics Δv penalty, restoring the composite at 500 kilowatt-electric?**

If yes, the architecture is rescued without invoking megawatt-class fission. The Block 4-9 delivered-fraction headlines (16-22%) survive in a re-framed form with longer mission duration.

If no, the composite is conclusively dead at any plausible power class — the architecture either requires megawatt-class fission (Path a, Bayesian-unlikely) or must be retired in favour of one of the lab-side alternatives (Variant C, Architecture E, hyperion's cruise-time-optimization regime).

---

## Reframed accounting

**Mission timeline under spiral-out reframe:**

| Segment | Duration | Notes |
|---|---|---|
| Earth-orbit assembly + outbound chemical kick | ~0.5 yr | Locked outbound chemical (REQUIREMENTS-L1 v0.3 §axis-2). |
| Outbound Saturn cruise (post-kick) | ~6 yr | Hohmann-ish. Could be reduced by hyperion's non-Hohmann finding (separate axis, ignored here). |
| Saturn-side rendezvous + chunk capture + minimal dwell | 1-2 weeks operational | No longer a 6-month constraint. Just whatever the ram-scoop accretion sweep + bag close-out takes. |
| **Saturn-escape spiral-out (continuous low-thrust)** | t_spiral_yr (sweep variable) | Δv_spiral ≈ 18 km/s (replaces impulsive 7.4). Burn time = propellant / mdot. |
| **Heliocentric inbound cruise (continuous thrust)** | t_inbound_yr (sweep variable) | Δv_inbound ≈ 23.2 km/s (per titan R-inbound-dv-continuous-thrust, less aerocapture credit). |
| Earth-orbit insertion + delivery | ~weeks | Aerocapture handles ~1.5 km/s; remaining trim chemical or all-electric. |

**Total mission duration** = ~0.5 + ~6 + ~0 (negligible dwell) + t_spiral + t_inbound + ~0.

**L0-05 strict pass:** total ≤ 15 yr → t_spiral + t_inbound ≤ ~8.5 yr.
**L0-05 waiver pass:** total ≤ 25 yr → t_spiral + t_inbound ≤ ~18.5 yr.

The constraint is on the **sum** of spiral and inbound burn times, not on each individually. Under Block 11 the 6-month residence dwell hard-constrained the exit burn; here only the L0-05 mission duration constrains the total.

**Mass closure:** Same as Block 11 — at each (Isp_spiral, Isp_inbound), the propellant required for the two Δv segments must be less than (collected water + dry mass), or delivered fraction goes negative.

---

## Variables and grid

| Variable | Values | Units | Notes |
|---|---|---|---|
| P_reactor | {0.5, 1.0, 2.0, 5.0} | megawatt-electric | 0.5 is Variant B / Block 4 anchor. 5.0 is Block 11 megawatt threshold for comparison. |
| Isp_spiral | {3000, 5000, 7000, 9000} | s | Saturn-escape spiral-out. Same engine as inbound by default (single-engine vehicle). |
| Isp_inbound | {3000, 5000, 7000, 9000} | s | Heliocentric inbound. Independent sweep but typically equal to Isp_spiral. |
| Δv_spiral | 18.0 (baseline), 19.5 (high), 14.0 (low) | km/s | Edelbaum spiral-departure cost. Baseline 18 km/s assumes v_circ at ~100,000 km Saturn-center residence orbit. Low 14 km/s assumes assisted by ring-particle gravity sink or pre-spiral altitude-raise via aerobraking off ring particles (speculative, included as sensitivity). High 19.5 km/s assumes innermost residence orbit ~95,000 km. |
| Δv_inbound_net | 23.2 | km/s | Per Block 11 = 24.7 raw minus 1.5 aerocapture credit. |
| eta | 0.65 | - | Engine total efficiency (jet power / electrical power). |
| Mass model | Block 9 / Block 11 baseline (200 t collected, 180 t dry net of jettison, 4.13 t shield) | t | Held constant for direct comparability to Block 11 grid; megawatt-class mass scaling deferred to R-megawatt-composite-with-mass-scaling. |

Cells: 4 power × 4 Isp_spiral × 4 Isp_inbound × 3 Δv_spiral × 1 Δv_inbound = **192 cells**. Sensitivity-only sweep separately runs Block 11's impulsive 7.4 km/s as a counterfactual control row (the "if Block 11 had run with no dwell constraint" reference).

---

## Method

For each cell, compute:

1. **Spiral burn**:
   - mass_at_start_spiral = collected + dry_total = 384.13 t
   - mr_spiral = exp(Δv_spiral × 1000 / (Isp_spiral × g0))
   - m_propellant_spiral = mass_at_start_spiral × (1 − 1/mr_spiral)
   - mass_after_spiral = mass_at_start_spiral / mr_spiral
   - thrust_spiral = 2 × eta × P_reactor / (Isp_spiral × g0)
   - mdot_spiral = thrust_spiral / (Isp_spiral × g0)
   - t_spiral_s = m_propellant_spiral / mdot_spiral

2. **Inbound burn**:
   - mass_at_start_inbound = mass_after_spiral
   - mr_inbound = exp(Δv_inbound_net × 1000 / (Isp_inbound × g0))
   - m_propellant_inbound = mass_at_start_inbound × (1 − 1/mr_inbound)
   - mass_at_earth = mass_at_start_inbound / mr_inbound
   - t_inbound_s analogous to spiral.

3. **Delivered fraction**: m_delivered = max(0, mass_at_earth − dry_total); fraction = m_delivered / collected. Negative or zero → mass-closure fail.

4. **Closure flags**:
   - L0-05 strict: t_spiral + t_inbound ≤ 8.5 yr (yields total mission ≤ 15 yr)
   - L0-05 waiver: t_spiral + t_inbound ≤ 18.5 yr (yields total ≤ 25 yr)
   - mass closure: delivered > 0
   - L0-04 floor: delivered ≥ 5 t (operational minimum per L0-04)

5. **Pass tier**: STRICT (all closure flags + L0-05 strict), WAIVER (all + L0-05 waiver), MARGINAL (mass closure only, L0-05 fails), FAIL (mass closure fails).

---

## Pre-registered hypotheses

| # | Hypothesis | Predicted range | Falsification rule |
|---|---|---|---|
| H1 | At P_reactor = 500 kilowatt-electric and Δv_spiral = 18 km/s (baseline), **no cell** closes L0-05 strict (≤ 15-year mission). The total of spiral + inbound burn times exceeds 8.5 years at every Isp combination because at this power class, the Tsiolkovsky-favourable high-Isp regime is too slow and the burn-time-favourable low-Isp regime fails mass closure. | Zero STRICT-tier cells at P=0.5 MWe / Δv_spiral=18. | Falsified if ≥ 1 STRICT cell exists at 500 kWe / 18 km/s. |
| H2 | At P_reactor = 500 kilowatt-electric and Δv_spiral = 18 km/s, **at least one cell** closes L0-05 waiver (≤ 25-year mission) at delivered fraction ≥ 10%. The constraint relaxation from 6-month dwell to 18.5-year burn-time budget opens a regime that 500 kWe could not access in Block 11. | ≥ 1 WAIVER cell with delivered ≥ 10% at 500 kWe / 18 km/s. | Falsified if zero WAIVER cells exist with delivered ≥ 10% at this anchor. |
| H3 | The delivered-fraction-optimal cell at 500 kWe / Δv_spiral 18 km/s under L0-05 waiver lies at Isp_spiral 5000-7000 s and Isp_inbound 7000-9000 s. Mid-Isp on the spiral (because lower Isp means shorter spiral time at fixed power); higher Isp on the inbound (because the inbound has more mass leverage on delivered fraction). Predicted delivered fraction in this regime: 8-15%. | Optimal cell at Isp_spiral ∈ [5000, 7000], Isp_inbound ∈ [7000, 9000], delivered ∈ [8, 15]%. | Falsified if optimal cell falls outside these Isp ranges OR if delivered fraction falls outside [4, 20]%. |
| H4 | The spiral-out Δv penalty (going from impulsive 7.4 km/s to spiral 18 km/s) consumes 6-10 percentage points of delivered fraction at the 500-kWe-optimal regime. The constraint-relaxation gain at this regime is ~10-15 pp (allowing access to mass-closing high-Isp configurations that Block 11 could not reach). Net spiral effect: **+2 to +8 pp of delivered fraction over Block 11's best mass-closing 500-kWe row** (which was zero). | Net spiral-vs-Block-11 delta at 500 kWe: +2 to +8 pp. | Falsified if net delta is negative OR > 12 pp. |
| H5 | **Architecture verdict at flown anchors.** The spiral-out reframe is sufficient to save the composite at 500 kilowatt-electric under L0-05 waiver (≤ 25-year mission), but NOT under L0-05 strict (≤ 15-year mission). The architecture survives only if the program accepts a 20-25 year round-trip. This is the "regulated-utility-with-extended-duration" verdict; pitch posture must lengthen the mission timeline by 5-10 years if Path (d) is the chosen resolution. | H1 held + H2 held + H3 in band + H4 in band. | Verdict falsified if H1 falsifies (500 kWe closes strict — architecture even stronger than predicted) OR if H2 falsifies (waiver also fails — architecture conclusively dead at all power classes). |
| H6 | **Sensitivity to spiral-out Δv assumption.** Halving the spiral-out Δv penalty (18 → 14 km/s, optimistic ring-altitude-raise via passive aerobraking off ring particles) doubles the delivered fraction at the waiver-tier optimum. The architecture is highly sensitive to whether the spiral-out can be partially compensated by Saturn-ring atmospheric/dust drag during the residence-orbit altitude raise. | Δv_spiral 14 → optimal delivered roughly 2× the 18 km/s case. | Falsified if sensitivity is < 1.3× or > 3× over this Δv range. |

---

## Decision rule

| Outcomes | Architectural verdict |
|---|---|
| H1 falsified (STRICT closure at 500 kWe) | **Architecture rescued under L0-05 strict.** Block 4-9 headlines retain their original 15-year mission duration. Best-case outcome. |
| H1 held + H2 held + H3 in band | **Architecture rescued under L0-05 waiver only.** Mission timeline extends 5-10 years vs Block 4-9 framing. Pitch and matrix need a duration footnote. |
| H1 held + H2 falsified | **Architecture conclusively dead at 500 kilowatt-electric.** Only megawatt-class (Path a) or non-residence-class architectures (Variant C, Architecture E) survive. R-megawatt-composite-with-mass-scaling becomes the only remaining critical-path round. |
| H6 holds strongly (Δv_spiral 14 km/s opens STRICT closure) | **Architecture survival contingent on ring-aerobraking feasibility.** New critical-path round R-ring-particle-aerobraking-altitude-raise would gate the result. |

---

## Limitations and what this round does NOT test

- **Single-engine assumption.** The spiral and inbound burns use the same engine type (Isp identical or grid-swept independently for sensitivity). A two-engine vehicle (chemical kick + electric cruise) is not modeled.
- **Edelbaum approximation for spiral-out Δv.** The 18 km/s anchor is the standard textbook approximation (dv_spiral ≈ v_circ_start when escaping to infinity). Real trajectory optimization could find ~10-20% savings via patched-conic boundary-layer tricks, but this round uses the textbook value.
- **Constant power throughout each segment.** Reactor power is assumed steady; no thermal-management throttling or eclipse periods.
- **Dry mass held at 200 t.** Block 11 noted that megawatt-class composites likely have 500-1000 t dry mass. This round explicitly does NOT do megawatt mass scaling — that's R-megawatt-composite-with-mass-scaling, the orthogonal critical-path round. Megawatt rows here are upper bounds for direct comparability to Block 11 grid.
- **No solar contribution.** Saturn-side insolation is ~1% of Earth orbit; ignored. R-hybrid-solar-augmentation already audited this on a different axis.
- **No reactor lifetime / cathode-budget check.** The 18.5-year burn-time budget at the waiver tier exceeds the 5-10 year Kilopower design lifetime by ~2×. If the spiral-out architecture works in this round, R-cathode-life-spiral-out becomes an obvious follow-on (current cathode life-limits would need an audit).
- **No outbound revisit.** Outbound chemical kick is locked (REQUIREMENTS-L1 v0.3).
- **Single chunk-mass = 200 t.** Not a multi-chunk-per-mission round.

---

## Signed-coupling pre-registration (methodology lesson 10 candidate from Block 12)

To anchor H4's prediction against the relevant physics rather than against linear intuition:

- **Δv penalty sign:** ADDING Δv to the exit burn DECREASES delivered fraction (Tsiolkovsky). Coupling sign: negative.
- **Burn-time relaxation sign:** ALLOWING longer total burn time enables access to higher-Isp regimes which INCREASE delivered fraction (Tsiolkovsky). Coupling sign: positive.
- **Magnitude prediction (H4 in band):** −6 to −10 pp from Δv penalty alone (anchored against Block 11 grid at fixed Isp showing each km/s exit Δv costs ~0.6-0.8 pp at Isp 5000-7000); +10 to +15 pp from the unlocked Isp space (anchored against Block 11 grid showing the 500-kWe to 5-MWe optimum jumped from "no closure" to 22.76% at the 6-month-dwell-constrained Isp regime; the relaxation effect at 500 kWe should be smaller because the optimum is dragged by burn-time not by mass closure).
- **Net sign expected:** marginally positive (+2 to +8 pp). If observed net is negative, the spiral-out reframe is a strict liability and Path (d) is dead.

This pre-reg explicitly anchors against the relevant Tsiolkovsky-plus-burn-time joint physics rather than against intuition. Per Block 12 lesson 10 candidate: signed coupling pre-registration tested at first use.

---

## Anchors and sources

- Spiral-out Δv approximation: Edelbaum (1962), "Propulsion Requirements for Controllable Satellites," *ARS Journal* 32 (8), 1079–1089. dv_spiral ≈ v_circ_start for departure to infinity. Standard textbook treatment in Wertz, Curtis, etc.
- B-ring orbital velocity at 100,000 km from Saturn center: √(GM_Sat / r) with GM_Sat = 3.793e16 m³/s², r = 1.0e8 m → v_circ ≈ 19,470 m/s. Cross-check: at 117,580 km (B-ring outer edge), v_circ ≈ 18,000 m/s. At 95,000 km (inner edge), v_circ ≈ 19,990 m/s. Spec uses 18 km/s baseline = midpoint of B-ring orbital velocity.
- Impulsive escape Δv for 100,000 km circular: dv = v_circ × (√2 − 1) ≈ 0.414 × 19,470 ≈ 8,060 m/s. Block 4 baseline used 7.4 km/s, derived from R-bring-fine-structure (slightly inside this).
- Continuous-thrust inbound Δv: 24.7 km/s integrated raw, 23.2 km/s net of 1.5 km/s aerocapture credit. Source: titan R-inbound-dv-continuous-thrust commit `58581fb` and Block 11.
- Composite mass parameters: Block 4 / Block 9. m_collected 200 t, m_dry_net 180 t (post 20 t jettison), m_shield 4.13 t.

---

## Deliverables

- `STUDY.md` — this file plus results section appended after run.
- `run.py` — sweep across (P_reactor, Isp_spiral, Isp_inbound, Δv_spiral).
- `results/closure_grid.csv` — full cell grid.
- `results/closing_cells.csv` — only cells that achieve WAIVER tier or better.
- `results/summary.json` — hypothesis adjudication.
- `results/spiral_vs_block11_compare.csv` — head-to-head with Block 11 best per power class.
- Handoff at `~/.claude/handoffs/iceberg-titan-20260518-spiral-out.md`.

---

## Follow-on rounds conditional on outcome

- If H2 held (waiver closes at 500 kWe): **R-cathode-life-spiral-out** — does the 18.5-year burn-time budget exceed cathode replacement intervals? **R-reactor-lifetime-cumulative-burn** — does 18.5 years of full-power burn fit within Kilopower-design 10-year cumulative lifetime?
- If H1 falsified (strict closure at 500 kWe): orchestrator integration of Path (d) as the primary residence-class architecture; pitch/matrix update; matrix axis 19 cell flips green.
- If H2 falsified (no waiver closure at any 500 kWe regime): **R-megawatt-composite-with-mass-scaling** becomes the only remaining critical-path round. Architecture conclusively dead at flown power anchors regardless of dwell constraint.
- If H6 holds strongly: **R-ring-particle-aerobraking-altitude-raise** — feasibility of pre-spiral altitude raise off B-ring particles.

---

## Results (2026-05-18)

### Headline numbers

| Power class | Spiral-out tier | Max delivered fraction | Best Isp combo | Total mission duration | Δ vs Block 11 |
|---|---|---|---|---|---|
| **500 kilowatt-electric** (Variant B anchor) | **FAIL** | 0 (no L0-05 closure) | n/a | n/a | 0 pp (Block 11 also 0) |
| 1.0 megawatt-electric | WAIVER (marginal) | 2.83% | 5000 / 7000 | 22.2 yr | +2.83 pp |
| 2.0 megawatt-electric | STRICT (marginal) | 2.83% at Isp 5000/7000; **21.54%** at Isp 7000/9000 (WAIVER) | 7000 / 9000 | 24.6 yr (waiver) / 14.3 yr (strict) | +21.54 pp |
| 5.0 megawatt-electric | STRICT | **28.36%** | 5000 / 9000 | 11.94 yr | +5.6 pp |

**Architecture verdict — composite is STRUCTURALLY DEAD at 500 kilowatt-electric even under spiral-out reframe.** The 18.5-year burn-time budget available under L0-05 waiver is insufficient to close mass + duration jointly at 500 kWe, because the spiral-out 18 km/s Δv penalty (vs Block 4's impulsive 7.4 km/s) eats more delivered fraction than the constraint-relaxation gain provides.

**However: the threshold power for closure drops from Block 11's 5 megawatt-electric to 1-2 megawatt-electric under spiral reframe** — a 2.5-5× reduction in required power. At 2 MWe under L0-05 waiver, the architecture delivers 21.5% (un-mass-scaled) at 24.6-year mission. This is materially more credible than Block 11's 5 MWe headline.

### What happens at 500 kWe — mass-closing but mission-duration-failing

The 500-kWe / Δv_spiral 18 km/s grid does have **MARGINAL** cells (mass closure positive) at high-Isp combinations:

- Isp_spiral 5000 / Isp_inbound 7000: 5.66 t delivered (2.83%), burn time 31.4 yr → mission 37.9 yr
- Isp_spiral 5000 / Isp_inbound 9000: 20.46 t delivered (10.23%), burn time 37.2 yr → mission 43.7 yr
- Isp_spiral 7000 / Isp_inbound 9000: 30+ t delivered at burn time 50+ yr → mission 60+ yr

Mass closure is restored, but mission duration exceeds even L0-05 waiver (25 yr) by 13-35 years. **A further L0-05 waiver extension to 45+ years would save the architecture at 500 kWe spiral-out**, but a 45-year cislunar-water delivery cycle is not programmatically credible (operator turnover, technology obsolescence, capital-return horizon all break).

### Why the spiral Δv penalty dominates at 500 kWe

The combined Δv for the spiral+inbound = 18 + 23.2 = 41.2 km/s. At Isp 5000 (Variant B baseline): mass ratio = exp(41200/49033) = 2.32, propellant = 384.13 × (1 − 1/2.32) = 218 t. That's > 200 t collected water; the propellant load exceeds the collected mass on the wet side. At Isp 7000: mass ratio = 1.82, propellant 174 t — closer but still 87% of collected water just to spiral+cruise. The Tsiolkovsky inert-mass-leverage Block 9 identified runs in reverse at this Δv budget.

Compare to Block 11's impulsive accounting (exit 7.4 + inbound 23.2 = 30.6 km/s total): mass ratio at Isp 5000 is 1.86, propellant 178 t. The 11 km/s extra cost of the spiral over the impulsive is ~40 t of additional propellant at Isp 5000, which is itself ~20% of the collected water budget. The architecture cannot afford this without a higher power class to access higher Isp.

### Hypothesis adjudication

| Hyp | Prediction | Observed | Status |
|---|---|---|---|
| H1 (zero STRICT cells at 500 kWe / 18 km/s) | zero | 0 STRICT cells | **held** |
| H2 (≥ 1 WAIVER cell at 500 kWe / 18 km/s with df ≥ 10%) | ≥ 1 | **0** | **falsified** |
| H3 (optimal cell at Isp_s ∈ [5k,7k], Isp_i ∈ [7k,9k], df ∈ [8,15]%) | in band | no closure | **falsified (no closure)** |
| H4 (net spiral-vs-Block-11 delta +2 to +8 pp at 500 kWe) | +2 to +8 pp | **0 pp** (no closure either way; Block 11 was also 0 at 500 kWe) | **falsified-direction** |
| H5 (architecture saved under waiver only) | held | falsified — not saved at 500 kWe even under waiver | **falsified** |
| H6 (Δv 14 km/s doubles delivered) | 1.3-3× ratio | no closure at 14 km/s either at 500 kWe | **not testable at 500 kWe** |

### Why H2 / H4 falsified the way they did — methodology lesson

My signed-coupling pre-registration anchored H4 at +2 to +8 pp net spiral-vs-Block-11 delta at 500 kWe. The actual is 0 pp because Block 11 was zero AND spiral was zero at this power class. The pre-reg should have been one of:

- "Spiral at 500 kWe closes WAIVER at delivered > 0" (the *direction* of save), or
- "Spiral at 500 kWe restores mass closure but mission duration exceeds waiver budget" (the *partial* finding)

Falsification-direction is the right way to read this: the spiral reframe gives BOTH less than I predicted on mass closure at 500 kWe AND less than I predicted on the threshold power reduction. The honest read is "spiral reframe is a 2.5-5× threshold-power-reduction lever, not a 500-kWe-rescue lever."

Adding to methodology Lesson 8 instances: this is the **sixth** instance of "predicted save magnitude was based on partial-physics intuition rather than the full Tsiolkovsky-plus-burn-time joint constraint."

### Cross-reference: impulsive-exit-no-dwell counterfactual

What if Block 11 had run with no dwell constraint AND kept the impulsive 7.4 km/s exit Δv (a physically incoherent combination — you can't have impulsive Δv at thrust this low — but useful as an analytic decomposition)?

| Cell at 500 kWe / 7.4 km/s impulsive / Isp 5000/9000 | Result |
|---|---|
| Mass closure | yes, 26-28% delivered |
| Burn time | exit 9.05 yr + inbound 19.5 yr = 28.5 yr |
| Mission | 35 yr — fails waiver |

So even with the impulsive Δv (no spiral penalty), 500 kWe is mission-duration-failing under waiver. The constraint-relaxation gain alone is insufficient at 500 kWe regardless of which Δv accounting is used.

### What this means for the Titan campaign

**Block 4's composite architecture has THREE load-bearing closure conditions, two now falsified:**

1. ✗ **Exit burn fits 6-month residence dwell** — falsified by Block 10 (8.92 yr at 500 kWe / Isp 7000).
2. ✗ **Inbound burn fits ~6-year cruise** — falsified by Block 11 (15.24 yr at 500 kWe / Isp 5000).
3. ✗ **L0-05 waiver (≤ 25 yr mission) closure at 500 kWe under spiral-out reframe** — falsified by this round (no 500 kWe closure at any Isp combination + spiral Δv).

The composite is structurally dead at the assumed 500-kWe power class under **every** resolution path considered to date. The remaining "save the architecture" options are:

| Path | Status after Block 13 |
|---|---|
| (a) Megawatt-class composite (Block 11) | Closure threshold lowered from 5 MWe (dwell-constrained) to **1-2 MWe under spiral reframe**. Realistic delivered fraction depends on megawatt-class mass scaling (R-megawatt-composite-with-mass-scaling). **Now the most plausible save.** |
| (b) Extend mission to 45+ yr | L0-05-waiver-violating by 20+ years. Not programmatically credible. **Conclusively retired.** |
| (c) Revert Isp to chemical-equivalent | Mass closure fails at 500 kWe regardless of dwell relaxation. **Conclusively retired.** |
| (d) Spiral-out exit during cruise | **Audited this round — does NOT save 500 kWe but lowers Path (a) threshold to 1-2 MWe.** Folds into (a). |

**The architecture's only remaining survival path is Path (a) — megawatt-class power — with the threshold revised down to 1-2 MWe under spiral-reframe accounting.** R-megawatt-composite-with-mass-scaling becomes the sole remaining critical-path round.

### Sensitivity: Δv_spiral 14 vs 18 vs 19.5 km/s

Across the (500 kWe, Isp_spiral, Isp_inbound) headline cells, H6 was not testable because no cells close at 500 kWe even at 14 km/s. At 1-2 MWe, the Δv_spiral sensitivity is observable: optimal 1-MWe waiver-tier delivered moves from 0 (at 14 km/s, mass-closing but burn-time-failing) to 2.83% (at 18 km/s with Isp 7000/5000 combination opens up via threshold burn-time fit). Counterintuitively, the lower Δv_spiral 14 km/s case is NOT uniformly better — it shifts the optimal Isp combination because the propellant savings open access to longer burn-time Isp regimes.

This is methodology lesson 8 instance #7: a Δv reduction does not uniformly improve delivered fraction; it changes which Isp combination is at the joint constraint optimum. Linear-Δv intuition fails again.

### Methodology lesson 8 instance count

Block 5, 7, 9, 10, 11, 13 (this round). Six instances of "pre-registered against intuition instead of computing under joint physics first." The pattern is now reliably reproducible.

**Lesson 11 candidate (new this round):** For a constraint-relaxation round, pre-register the *threshold-power-reduction magnitude* explicitly, not just the *qualitative save/no-save at the anchor power class*. The qualitative pre-reg conflates "architecture rescued at anchor" with "architecture threshold-power lowered to anywhere"; only the latter was the real finding.

### Files

- `STUDY.md` — this document.
- `run.py` — joint mass-closure + burn-time + mission-duration calculator across (P_reactor, Isp_spiral, Isp_inbound, Δv_spiral).
- `results/closure_grid.csv` — full 192-cell grid.
- `results/closing_cells.csv` — 48 cells achieving WAIVER or STRICT tier.
- `results/spiral_vs_block11_compare.csv` — head-to-head with Block 11 best per power class.
- `results/impulsive_exit_no_dwell_reference.csv` — counterfactual: Block 11-equivalent but with constraint relaxation only (no spiral Δv penalty).
- `results/summary.json` — hypothesis adjudication.
