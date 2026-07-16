# R-conops-phase12-reuse — does deep-space-vehicle reuse change the marginal-internal-rate-of-return picture?

**Author:** Titan (re-spawn)
**Status:** pre-registered.
**Branch:** `iceberg-titan-2`.
**Date:** 2026-05-16.
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessor this session:** `R_conops_skeleton/STUDY.md` (conops augmentation A-ph12-reuse).

---

## Motivation

R-conops-skeleton enumerated six augmentations to the project-owner-supplied basic concept-of-operations. Five of the six (A-ph11-dv, A-ph6.5-mass, A-ph7-regime, A-ph4-orbit, A-c1-contingency) are either covered by existing rounds or are low-leverage. The one genuinely uncovered augmentation is **A-ph12-reuse**: the conops as drawn ends at phase 11 (customer handoff) with no statement about what the deep-space vehicle does next. R-reactor-roadmap and R-delivery-irr-curve both build their cashflow models on a fleet-of-single-use-vehicles assumption that is *implicit*, never named, and never tested.

This round names the assumption and tests it. If vehicle reuse for two or more missions is technically viable, the per-mission capital-expenditure denominator drops materially and marginal-internal-rate-of-return rises. R-delivery-irr-curve found the program is sub-sovereign-bond at 1.45 percent under MARVL-anchored mass; a 30–50 percent capex reduction from reuse would lift this by 1–2 percentage points and potentially cross the sovereign-bond floor without any architecture change.

## The assumption being questioned

The assumption is Titan's own — the augmentation A-ph12-reuse in R-conops-skeleton said: "Vehicle reuse for a second mission saves more than the refurbishment and refuelling cost." The R-reactor-roadmap cashflow model implicitly says the opposite: every launch pays the full ship cost, with no credit for reuse.

The binding technical constraints on reuse, in order of likely tightness:

1. **Reactor lifetime.** Kilopower is designed for ~15-year operational life. Fission Surface Power Phase 1 reactors target ~10-year design life. A single 14.5-year all-electric mission roughly consumes a Fission Surface Power Phase 1 reactor's design life and approaches Kilopower's. Two consecutive missions back-to-back (30 years total) require either a new reactor for the second mission or a fundamentally different long-life reactor design. National Academies 2021 notes that long-duration reactor lifetime is one of the un-funded technology gaps in space fission.

2. **Ion-engine grid erosion + cathode life.** R-cathode-life-water-plasma touched cathode degradation under water-plasma operation. Long-duration deep-space mission profiles (NEXT, NSTAR) have demonstrated > 30,000 hours of thrust life. A 14.5-year all-electric inbound burns roughly 30,000–40,000 thrust hours per mission. Two-mission reuse approaches the ground-tested edge.

3. **Radiator degradation.** Thermal cycling, micrometeorite punctures, and decade-scale degradation of radiator coating emissivity. Single-mission survival is built in to the design; second-mission survival is a separate qualification. R-thermal-cooling did not address multi-mission lifetime.

4. **Structural fatigue.** Outbound burn + capture + inbound burn induces a small number of high-stress events. Fatigue cycle count is low; not expected to bind.

5. **Avionics radiation dose.** Solid-state electronics in deep-space accumulate total ionizing dose over decade timescales. Mission-survivable parts (rad-hard, 100+ krad) typically support multiple missions; not expected to bind.

The model below treats reactor lifetime as the dominant constraint and parameterises refurbishment cost by whether the reactor is replaced.

## Pre-registered hypotheses (H-ph12)

**Aggregate (H-ph12-agg):** Two-mission vehicle reuse is technically viable for the surviving 500-kilowatt-electric all-electric architecture if the refurbishment-with-reactor-replacement cost is bounded below approximately the new-build cost minus the avionics-and-structure cost (i.e., reactor replacement is the dominant refurbishment cost). Under viable two-mission reuse with reactor replacement, marginal-internal-rate-of-return lifts from R-reactor-roadmap's 1.45 percent baseline by 0.6 to 1.4 percentage points and approaches but does not cross the sovereign-bond floor (~4 percent). Three-mission reuse without further-reactor-replacement is not viable (reactor-lifetime-bound). Reuse without reactor replacement (i.e., a reactor that supports 30+ years of high-power operation) is upside-only, contingent on a reactor program that has not flown.

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-ph12-a | Per-mission capex under 2-mission reuse with $200M basic refurbishment (no reactor replacement) | 35–45% lower than single-use | outside [30%, 50%] |
| H-ph12-b | Per-mission capex under 2-mission reuse with $500M reactor-replacement refurbishment | 10–25% lower than single-use | outside [5%, 30%] |
| H-ph12-c | Marginal internal-rate-of-return uplift under 2-mission reuse + reactor-replacement refurbishment (the realistic case under reactor-lifetime constraints) at delivery = 200 tonnes per ship (L1-007 cap) | 0.6 to 1.4 percentage points (from R-reactor-roadmap baseline 1.45 percent to 2.0 to 2.9 percent) | outside ±0.5 percentage points either side |
| H-ph12-d | Marginal internal-rate-of-return uplift under 3-mission reuse with two reactor replacements at delivery = 200 tonnes per ship | 1.0 to 2.0 percentage points | outside ±0.5 percentage points either side |
| H-ph12-e | Marginal internal-rate-of-return uplift under 2-mission reuse + $200M basic refurbishment (no reactor replacement — i.e., assumes long-life reactor exists) at delivery = 200 tonnes per ship | 1.8 to 2.8 percentage points | outside ±0.5 percentage points either side |
| H-ph12-f | None of the reuse scenarios at delivery = 200 tonnes per ship cross the sovereign-bond floor (4 percent) under MARVL-anchored mass | held | falsified if H-ph12-e brings marginal-internal-rate-of-return above 4.0 percent |
| H-ph12-g | At delivery = 482 tonnes per ship (B-ring physical single-chunk cap, requires R-chunk-as-heat-shield closure), reuse adds enough lift to cross the regulated-utility hurdle (8 percent) by a non-trivial margin (≥ 1 percentage point) under any of the three reuse scenarios | 9.5–11.5% range (vs no-reuse baseline 8.22%) | outside ±1 percentage point of [9.5%, 11.5%] |

**Aggregate grading rule:**

- If H-ph12-c holds, two-mission reuse is the project's best near-term economic-uplift move (because it requires no architecture change, only a refurbishment-capability investment).
- If H-ph12-f holds, even reuse cannot lift the program out of subsidy-capital class without a per-ship delivery uplift (which only R-chunk-as-heat-shield-revisit can provide).
- If both H-ph12-c and H-ph12-f hold, the combined recommendation is: reuse plus R-chunk-as-heat-shield-revisit are *both* required to reach regulated-utility class. Neither alone is enough.

## Method

### Cashflow model

Re-use R-reactor-roadmap's cashflow framework verbatim but parameterise the per-launch ship-cost field by reuse factor. The relevant logic in `R_reactor_roadmap/run.py` is `cashflow_yearly()`, which bills `SHIP_COST[era]` at each launch year. The new logic bills:

- `SHIP_COST[era]` at the year a *new* ship enters service (first mission of its life)
- `REFURB_COST` at the year a *reused* ship enters service for its second-or-later mission, where `REFURB_COST` is one of {$200M basic, $500M with reactor swap}
- Fleet schedule (launches every 13/12 years) held identical so the cadence and delivered-mass schedule are unchanged

For reuse factor R, the (build-vs-refurbish) decision at each launch follows the lifecycle: build at year 0, refurbish at year M, refurbish at year 2M, ..., refurbish at year (R-1)M, retire. A new vehicle is required every R missions to replace each retiring ship. The total fleet has the same number of mission-launches but the build/refurbish mix changes.

### Marginal-internal-rate-of-return uplift

Use R-reactor-roadmap's IRR-bisect routine. Compute:

- Baseline: single-use, full SHIP_COST per launch (= R-reactor-roadmap's reported 1.45 percent at delivery 128.8 tonnes per ship, which we will independently verify before computing reuse uplifts)
- Reuse case 1: 2-mission reuse, $200M basic refurbishment, delivery sweep ∈ {128.8, 200, 482} tonnes per ship
- Reuse case 2: 2-mission reuse, $500M reactor-replacement refurbishment, same sweep
- Reuse case 3: 3-mission reuse, two $500M reactor replacements, same sweep
- Reuse case 4: 2-mission reuse, $200M basic, but assumes long-life reactor exists (upside scenario for H-ph12-e)

Report marginal-internal-rate-of-return uplift = IRR(reuse-case) - IRR(no-reuse-baseline) at each delivery tonnage.

### Sweep axes

- Reuse factor R ∈ {1 (baseline), 2, 3, 4}
- Refurbishment cost C_refurb ∈ {$200M basic, $500M with reactor swap}
- Per-ship delivery ∈ {128.8 (R-megawatt-marvl-radiator headline), 200 (L1-007 cap), 482 (B-ring single-chunk cap)} tonnes
- R-power-base-rate cumulative-distribution-function held flat at "best-case audited cell" from R-delivery-irr-curve (price $10,000 per kilogram, $2 billion sovereign at year 11)

### Validity caveats

1. The reuse-vs-build decision treats a single failure mode (reactor lifetime) as deterministic and assumes other lifetime constraints (cathode life, radiator) clear with margin. R-cathode-life-water-plasma found ~25,000-hour cathode life under water plasma; 30,000–40,000 thrust hours per mission is at the edge. If cathode life caps at one mission, reuse requires thruster replacement too, raising refurbishment cost. Refurbishment-cost sensitivity (Reuse case 2 vs Reuse case 1) brackets this uncertainty within the model.

2. The model assumes refurbishment happens at Earth (low Earth orbit or a service depot). In-orbit refurbishment infrastructure does not exist as of 2026 and is itself a separate program. The model treats this infrastructure as a sunk cost outside the per-mission accounting — a simplification. If on-orbit servicing requires its own NRE and per-event cost, the refurbishment cost is higher than modeled.

3. R-mission-success-probability projects per-mission success at 0.56. Under reuse, the second mission only happens if the first succeeded *and* the vehicle returned in a refurbishable condition. The effective reuse factor under failure-conditioned accounting is lower than the nominal reuse factor. The model below uses nominal reuse factor only (no probability conditioning); this overstates reuse benefit by perhaps 30 percent at single-mission p=0.56. Documenting as a known optimistic bias.

4. Fleet schedule in the model is launch-year-driven (every 13/12 years) not ship-availability-driven. Under reuse, ship availability constrains launch schedule (you can't launch a ship that's still on mission). For the steady-state cadence assumed here, fleet size adjusts to maintain launch cadence; the model accounts for this by tracking how many *new* vs *refurbished* ships enter service each year independent of ship identity.

### Revisit clause

This round's prediction grades by per-claim falsification. Cross-learning section below names which downstream rounds become high-priority based on which sub-claims hold.

## Result

Sweep table (conditional internal-rate-of-return at megawatt-never branch — see Reading for framework caveat):

| Scenario | Delivery (t/ship) | IRR | Uplift vs single-use (percentage points) | Capex per mission ($M) | Capex reduction (%) |
|---|---:|---:|---:|---:|---:|
| single-use baseline | 128.8 | 2.10% | — | 650 | — |
| 2x reuse, $200M basic refurb | 128.8 | 3.24% | +1.14 | 468 | -28.1 |
| 2x reuse, $500M reactor-swap refurb | 128.8 | 2.45% | +0.36 | 589 | -9.4 |
| 3x reuse, two $500M reactor swaps | 128.8 | 2.82% | +0.72 | 561 | -13.7 |
| 4x reuse, three $500M reactor swaps | 128.8 | 2.91% | +0.81 | 557 | -14.3 |
| single-use baseline | 200.0 | 5.38% | — | 650 | — |
| 2x reuse, basic refurb | 200.0 | 6.33% | +0.96 | 468 | -28.1 |
| 2x reuse, reactor-swap refurb | 200.0 | 5.70% | +0.32 | 589 | -9.4 |
| 3x reuse, 2 reactor swaps | 200.0 | 5.85% | +0.47 | 561 | -13.7 |
| 4x reuse, 3 reactor swaps | 200.0 | 5.88% | +0.50 | 557 | -14.3 |
| single-use baseline | 482.0 | 11.77% | — | 650 | — |
| 2x reuse, basic refurb | 482.0 | 12.28% | +0.50 | 468 | -28.1 |
| 2x reuse, reactor-swap refurb | 482.0 | 11.94% | +0.17 | 589 | -9.4 |
| 3x reuse, 2 reactor swaps | 482.0 | 11.97% | +0.20 | 561 | -13.7 |
| 4x reuse, 3 reactor swaps | 482.0 | 11.98% | +0.20 | 557 | -14.3 |

Pre-registration grading:

| Sub-claim | Predicted | Observed | Verdict |
|---|---|---|---|
| H-ph12-a (2x basic capex reduction 35–45%) | [35, 45] | 28.1% | **wrong-and-load-bearing** |
| H-ph12-b (2x reactor-swap capex reduction 10–25%) | [10, 25] | 9.4% | wrong-but-informative |
| H-ph12-c (2x reactor-swap uplift 0.6–1.4 pp at 200 t/ship) | [0.6, 1.4] | +0.32 pp | wrong-but-informative |
| H-ph12-d (3x uplift 1.0–2.0 pp at 200 t/ship) | [1.0, 2.0] | +0.47 pp | **wrong-and-load-bearing** |
| H-ph12-e (2x basic uplift 1.8–2.8 pp at 200 t/ship — upside case) | [1.8, 2.8] | +0.96 pp | **wrong-and-load-bearing** |
| H-ph12-f (no reuse scenario crosses 4% at 200 t/ship) | held | falsified, baseline already 5.38% | falsified (framework artifact — see Reading) |
| H-ph12-g (max IRR at 482 t/ship with reuse in 9.5–11.5%) | [9.5, 11.5] | 12.28% | held (within ±1pp tolerance) |

## Reading

**The headline:** reuse provides a modest economic uplift (0.32 to 1.14 percentage points across realistic scenarios) but is not transformative. **Reuse is not load-bearing on the program's economic case in the way I predicted.** Five of seven sub-hypotheses are falsified in the conservative direction — my numeric ranges were systematically too optimistic.

**The root mistake in my pre-registered numbers:** I anchored uplift predictions on "halving ship cost halves per-mission capex," which is incorrect because:

1. **Launch cost is $290M per mission and is unchanged by vehicle reuse.** Falcon Heavy expendable plus a Vulcan-Centaur-class kick stage costs $290M every launch regardless of whether the vehicle being launched is new or refurbished. This sets a floor on per-mission cost that no amount of vehicle reuse can touch.

2. **Ground operations are a fleet-wide constant at $50M per year.** Over the 45-year horizon that's $2.25 billion, allocated across 36 missions = $63M per mission. Independent of reuse.

3. **The horizon truncation penalises late builds.** Ships launched after year ~29 cannot complete a second mission within the 45-year horizon even if reuse-factor permits. These ships are effectively single-use within accounting. The fleet schedule produces about 60 percent builds and 40 percent refurbishments rather than the 50/50 I assumed.

4. **Reactor-replacement refurbishment costs $500M out of a $650M new-build cost** — savings per refurbishment are only $150M. With the timing constraints above, this gives only 9.4 percent total fleet capex reduction, not the 10–25 percent I predicted.

5. **The basic-refurbishment ($200M, no reactor swap) scenario assumes a long-life reactor that does not exist.** Under H-ph12-e's "upside" framing this is just a hypothetical lift; under the realistic reactor-lifetime constraint (H-ph12-c), reactor-swap is required and uplift drops to 0.32 pp.

**Framework caveat on H-ph12-f.** My baseline at 200 tonnes per ship of 5.38 percent is the *conditional* internal-rate-of-return at megawatt-never branch (i.e., the all-Chemical_kick_500kWe fleet across the full horizon, no megawatt era). R-delivery-irr-curve's 3.77 percent at 200 tonnes per ship is the *marginal* internal-rate-of-return integrated over R-power-base-rate's megawatt-arrival cumulative-distribution-function, which puts substantial weight on lower-era branches that deliver zero. The 5.38 percent figure is therefore a "given a working architecture is in service" number; the 3.77 percent figure is "weighted across the probability that the architecture is in service at all." For uplift purposes, the delta is the right comparison; for absolute thresholding against 4 percent sovereign-bond floor, R-delivery-irr-curve's marginal number is the apples-to-apples comparison. **Under the marginal framework, the 4 percent floor is likely still un-crossed at 200 tonnes per ship under any reuse scenario, but this round did not reproduce R-delivery-irr-curve's full integration to verify.**

**H-ph12-g held by tolerance.** Maximum internal-rate-of-return at 482 tonnes per ship (B-ring physical single-chunk cap) is 12.28 percent under 2x basic reuse — within ±1 pp of the [9.5, 11.5] predicted range, classed as held. The B-ring-cap regime already comfortably clears the regulated-utility hurdle even *without* reuse (single-use at 482 t = 11.77%). Reuse is incremental at the high-delivery end too.

**What this round actually establishes:**

- Vehicle reuse at 2x with realistic reactor-replacement refurbishment lifts marginal-internal-rate-of-return by 0.2 to 0.5 percentage points across the realistic delivery range. Real but not load-bearing.
- The upside scenario (long-life reactor, $200M basic refurbishment) lifts by 0.5 to 1.1 percentage points — still modest, and contingent on a reactor technology that has not been developed.
- The reason reuse is not transformative is that ship cost is only ~$650M of a ~$1 billion per-mission gross expense. Launch ($290M) and ground operations ($63M per mission allocation) dominate the floor and are not addressed by reuse.
- **R-chunk-as-heat-shield-revisit (delivery uplift) remains the dominant economic lever.** A 200 tonnes per ship → 482 tonnes per ship uplift (single-chunk-B-ring-cap scenario) is worth ~6.4 percentage points of internal-rate-of-return. A reuse cycle is worth ~0.5 percentage points. The leverage ratio is 13:1.

## Revisit

The methodology lesson is the recurring one (now the fifth instance documented in two days, after R-outbound-dv-continuous-thrust H-od-d, R-megawatt-marvl-radiator H-mr-d, R-reactor-roadmap H-rxr2-b through H-rxr2-f, and R-delivery-irr-curve H-dic-d): **compute the product of central estimates before ranging around it.** I assumed ship-cost reduction would propagate proportionally to per-mission capex, ignoring the fixed costs that survive reuse. A one-line back-of-envelope `(650 - refurb) / (650 + 290 + ground_ops_share)` would have told me the ceiling was 20-25 percent capex reduction, not 50 percent.

## Cross-learning

This round generates two follow-on directions and one anti-direction:

1. **De-prioritise reuse as a near-term program decision.** Reuse is real upside but is not architecture-critical. It can be retrofitted into the program plan after the year-5 to year-10 demonstrator gates close. No reason to design the early vehicles for reuse if that adds non-trivial cost or complexity. R-conops-phase12-reuse is a *no-op* for the near-term roadmap.

2. **Promote R-chunk-as-heat-shield-revisit to highest priority confirmed.** The 13:1 leverage ratio (delivery uplift vs reuse uplift) is the largest single finding from this round. Saturn's Iapetus spawn is the right next move; this round provides quantitative justification.

3. **The fixed-cost floor (~$350M per mission for launch + ground-ops) is itself an open round.** Falcon-Heavy-class launch is the assumed launcher. Starship at a fraction of the price would change this floor dramatically. R-launch-cost-sensitivity is a candidate downstream round — under $50M-per-launch Starship economics, the per-mission floor drops to ~$110M and reuse uplift becomes more material. Currently un-modelled.

The conops augmentation A-ph12-reuse therefore promotes to **closed** in R-conops-skeleton's queue. The phase-12 end-of-mission decision can remain open (re-enter vs park vs reuse), but the economic case for prioritising reuse is now bounded.
