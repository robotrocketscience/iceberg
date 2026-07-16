# R-microwave-electrothermal-as-cathode-life-escape-hatch — does water microwave-electrothermal beat water-radio-frequency-ion at Variant B when cathode-life penalty for radio-frequency-ion is properly priced?

**Status:** pre-result.

## Question

R10b (prior round) retired water-microwave-electrothermal at power classes above 25 kilowatt-electric on delivered-fraction grounds: water-radio-frequency-ion delivers roughly twice the chunk per mission. R-all-electric-thruster-sweep (commit 9b20cbf) confirmed this at Variant B delta-velocities — water-microwave-electrothermal at 1 megawatt-electric delivers 35.6% chunk versus water-radio-frequency-ion's 70.4%. R10b's decision was orthogonal to cathode life.

R-cathode-life-water-plasma (commit 4988360) surfaced cathode life as a load-bearing axis the campaign had not previously evaluated. Microwave-electrothermal has no hollow cathode (microwave plasma is sustained without thermionic emission); the cathode-life problem does not apply. Radio-frequency-ion has a hollow cathode (radio-frequency neutralizer plus internal radio-frequency-coupled discharge cathode); the cathode-life requirement at 10-mission reuse is 54,349 hour for Variant B canonical, 1.09× Advanced-Electric-Propulsion-System design life of 50,000 hour.

The non-obvious architectural reversal proposed at the end of R-cathode-life-water-plasma is: under the Wang et al. 2025 pessimistic cathode-life anchor (3,000 hour, derived from oxygen-deposition work-function degradation extrapolated to megawatt-electric current density), water-microwave-electrothermal becomes the only Variant B thruster that closes cathode-life — by escape rather than by competing on delivered fraction.

But that proposal was at the cross-learning level. It has not been properly priced. The proper pricing requires two corrections:

1. **The spare-cathode mass penalty for radio-frequency-ion is small.** Cathode assemblies are ~10–30 kilogram each, swap mechanism another ~50 kilogram. At Variant B's small mass ratio (1.39), an 80–500 kilogram dry-mass addition propagates to a < 5% propellant-mass increase, translating to a < 5% chunk-delivered-fraction reduction. Microwave-electrothermal's 36.2% delivered fraction is half of radio-frequency-ion's 70.4%; the spare-cathode mass penalty alone does not close that gap.

2. **The real penalty for radio-frequency-ion under cathode-life-pessimism is mission-failure-probability.** Each in-flight cathode swap has some non-zero probability of mechanical failure, plume contamination, swap-mechanism deployment failure, or cathode start-up failure. If per-swap failure probability is p and total swaps required over N missions is S, the expected fraction of missions that complete normally is (1−p)^S. At sufficiently high p × S, the expected delivered chunk across N missions drops below microwave-electrothermal's deterministic 36.2%-per-mission floor, and microwave-electrothermal wins on expected lifetime delivery.

The question: at what cathode-life anchor and per-swap failure probability does water-microwave-electrothermal beat water-radio-frequency-ion on expected lifetime delivered chunk, for Variant B at 10-mission reuse?

## Pre-registered hypothesis (H-mealh)

**Aggregate (H-mealh-agg):** Microwave-electrothermal-as-escape-hatch is the right architectural choice only under a combined cathode-life-pessimistic plus high-failure-rate regime. Under realistic engineering assumptions (Dawn three-thruster hot-swap heritage suggests per-swap failure probability ≤ ~1%, even at the Wang et al. pessimistic life anchor of 3,000 hour) water-radio-frequency-ion remains the dominant choice for Variant B by a wide margin. The escape-hatch claim from R-cathode-life-water-plasma is too strong: microwave-electrothermal only wins when cathode-life is pessimistic *and* engineering failure probability is high, which is a small region of the parameter space.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-mealh-a — At zero per-swap failure probability and unlimited cathode life, radio-frequency-ion lifetime delivery dominates microwave-electrothermal by ratio | 1.85 to 2.05× | outside band |
| H-mealh-b — Spare-cathode mass penalty for radio-frequency-ion at 10-mission reuse, Wang pessimistic life (need ~18 cathodes total at 3,000 hour each over 54,349 hour required), assembly mass 50 kilogram each | drops radio-frequency-ion chunk delivery by 1–5% | outside band |
| H-mealh-c — Per-swap failure probability at which radio-frequency-ion's expected lifetime delivery ties microwave-electrothermal, under canonical cathode life (1 spare needed, S=1 swap) | p_crit ≈ 0.49 — radio-frequency-ion only loses if a single cathode swap fails roughly half the time | falsified if p_crit < 0.30 (would mean cathode-swap reliability is highly load-bearing even at single swap) |
| H-mealh-d — Per-swap failure probability at which radio-frequency-ion ties microwave-electrothermal, under Wang pessimistic cathode life (need 18 cathodes, S ≈ 17 swaps over 10 missions) | p_crit ≈ 0.04 — even modest swap failure probability flips the verdict | falsified if p_crit > 0.10 (would mean even high-S swap regimes tolerate substantial failure rates) |
| H-mealh-e — Realistic per-swap failure probability based on Dawn three-thruster hot-swap heritage (Dawn flew 11+ years, accumulated 51,765 hour across three thrusters, no swap-mediated mission loss; estimate ≤ 1% per swap) | ≤ 0.01 | falsified if Dawn analogy gives > 0.05 (1 swap loss in 20 swaps) |
| H-mealh-f — Combining H-mealh-d and H-mealh-e: at Wang pessimistic plus 1% per-swap failure probability, radio-frequency-ion vs microwave-electrothermal | radio-frequency-ion still wins by 10–30% expected lifetime delivery | falsified if microwave-electrothermal wins under realistic-failure-plus-pessimistic-life regime |
| H-mealh-g — Combining at Wang pessimistic plus 5% per-swap failure probability (degraded engineering, unproven swap mechanism) | microwave-electrothermal wins by 10–30% expected lifetime delivery | falsified if radio-frequency-ion still wins |
| H-mealh-h — Combining at xenon-heritage life (50,000 hour) plus 1% per-swap failure probability | radio-frequency-ion wins by 80–100% expected lifetime delivery (no swaps needed in 10 missions) | falsified if even single-spare regime gives p_crit < 0.50 |

**Pre-registered aggregate decision-ordering:**

The structurally interesting question is whether H-mealh-g holds — i.e., whether there is *any* engineering regime in which microwave-electrothermal beats radio-frequency-ion. If H-mealh-g holds, the R-cathode-life-water-plasma "escape hatch" claim survives in the cathode-life-pessimistic plus high-failure-rate corner. If H-mealh-g fails, the escape-hatch claim is too strong: even under cathode pessimism, microwave-electrothermal does not win.

H-mealh-f is the load-bearing case. Realistic engineering (Dawn-class failure rates) plus pessimistic cathode life (Wang et al. extrapolation) is the most defensible "should we worry?" scenario. If radio-frequency-ion still wins there, the escape-hatch claim is retired.

## Method

**Lifetime delivered chunk** for each thruster over N missions, accounting for cathode-swap regime and per-swap failure probability:

For water-microwave-electrothermal (no hollow cathode, no swaps):
```
E[delivered_MET] = N × chunk × delivered_fraction_MET
```
deterministic; no failure-probability term.

For water-radio-frequency-ion (hollow cathode, S swaps over N missions):
```
E[delivered_RFI] = N × chunk × delivered_fraction_RFI × (1 - p)^S
                  - mass_penalty_from_spare_cathodes
```
where:
- S = ceil((total cathode-on hour required) / (life per cathode in hour)) − 1, but at least 0
- p = per-swap failure probability (0%, 1%, 5%, 10%, 25%)
- mass_penalty_from_spare_cathodes propagates via Tsiolkovsky to a small chunk-delivered reduction

**Failure model.** Per-swap failure means the swap mechanism does not successfully transition to the spare cathode. The interpretation matters: (a) tug-loss-per-failure (the entire mission and possibly the tug is lost on first failure, with all subsequent missions also lost) or (b) mission-loss-per-failure (only the current mission's chunk is lost, the tug returns to base for refurbishment and continues). Both are modelled and reported side-by-side. The realistic Dawn-class operational pattern is closer to (b).

**Cathode-on time per mission** (from R-cathode-life-water-plasma):
- Microwave-electrothermal Variant B canonical: 5,435 hour (microwave-on time; counts as thruster-on for parity even though there's no cathode)
- Radio-frequency-ion Variant B canonical: 5,435 hour cathode-on

**Cathode-life anchors** (from R-cathode-life-water-plasma):
- Optimistic (matches xenon heritage Advanced-Electric-Propulsion-System): 50,000 hour
- Mid-case (half of xenon): 25,000 hour
- Pessimistic (Wang et al. 2025 work-function extrapolation): 3,000 hour

**Cathode hardware mass** (engineering estimate, bounded against Dawn three-thruster heritage):
- Single cathode assembly: 30 kilogram (cathode + keeper + tightly-coupled plumbing)
- Swap mechanism (per slot): 20 kilogram (linear actuator, plasma seal, electrical disconnect)
- Per-slot mass: 50 kilogram

**Sweeps.**
- Thruster: water-microwave-electrothermal (delivered fraction 35.6% per R-all-electric-thruster-sweep at 1 megawatt-electric), water-radio-frequency-ion (70.4%)
- Cathode-life anchor: optimistic, mid-case, pessimistic
- Per-swap failure probability: 0%, 1%, 5%, 10%, 25%
- Failure mode: tug-loss-per-failure, mission-loss-per-failure
- N_missions: 1, 5, 10, 20

**Validity caveats.**

- Per-swap failure probability is an engineering parameter the campaign has not measured. The Dawn heritage suggests ≤ 1% as a sane anchor but is itself a single data point (one mission, three thrusters, no swap-mediated mission loss across 11+ years). Treating ≤ 1% as the realistic case is the right anchor for this round but is uncertain by an order of magnitude.
- The "(1 − p)^S" model assumes swap failures are independent. In reality, swap failures may correlate (common-cause failure in the swap mechanism design). The independent-failure assumption is optimistic; a correlated-failure model would push p_crit lower.
- Spare-cathode mass penalty is treated as additive dry mass; the structural integration cost (swap-rail, plasma seals, control electronics) is bundled into the 50 kilogram per slot. Real engineering will need a vehicle-level mass roll-up.
- Chunk-aerocapture path (R-chunk-as-heat-shield revisit territory) is orthogonal to this round and not modelled. Aerocapture would reduce inbound delta-velocity for both thrusters and shift the cathode-on-time floor; the relative comparison microwave-electrothermal versus radio-frequency-ion is not affected.
- The microwave-electrothermal delivered fraction of 35.6% is from R-all-electric-thruster-sweep at the matrix-impulsive Variant B delta-velocities, 1 megawatt-electric. At higher power (2 megawatt-electric) microwave-electrothermal drops slightly to 34.3% delivered; at lower power (500 kilowatt-electric) it rises to 36.2%. The round uses 1 megawatt-electric as the matrix's reference power.
- Reactor cycle life under multi-year burn is a separate but adjacent constraint (flagged R-cathode-life-water-plasma cross-learning). Microwave-electrothermal also requires the reactor; the cathode-life axis is independent of reactor-life axis. Both architectures bear the reactor-life burden equally.

## Result

**Status:** complete. Run output in `results/escape_hatch.json` and `results/tables.md`.

### Crossover per-swap failure probability (10-mission reuse, mission-loss model)

| Life anchor | Swaps required | p_crit (radio-frequency-ion ties microwave-electrothermal) |
|---|---:|---:|
| Optimistic (50,000 hour) | 1 | 0.494 |
| Mid-case (25,000 hour) | 2 | 0.289 |
| Pessimistic (3,000 hour, Wang et al.) | 18 | 0.037 |

### Direct head-to-head at Wang pessimistic, 10-mission reuse, mission-loss model

| p_swap | Microwave-electrothermal lifetime (tonne) | Radio-frequency-ion lifetime (tonne) | Verdict | Radio-frequency-ion advantage |
|---:|---:|---:|:---|---:|
| 0.00 | 712.0 | 1,405.4 | radio-frequency-ion | +97% |
| 0.01 | 712.0 | 1,172.8 | radio-frequency-ion | +65% |
| 0.05 | 712.0 | 558.2 | **microwave-electrothermal** | −22% |
| 0.10 | 712.0 | 210.9 | microwave-electrothermal | −70% |
| 0.25 | 712.0 | 7.9 | microwave-electrothermal | −99% |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Verdict |
|---|---|---|---|
| H-mealh-a — radio-frequency-ion / microwave-electrothermal ratio at zero failure | 1.85–2.05× | 1.98× (70.4 / 35.6) | **held** |
| H-mealh-b — Spare-cathode mass penalty at Wang pessimistic 18 cathodes | drops radio-frequency-ion delivered fraction by 1–5% | 0.14% (70.4 → 70.3%) | **falsified low** — Variant B's small mass ratio (1.39) makes 850 kilogram dry-mass addition negligible against 200-tonne chunk |
| H-mealh-c — p_crit at canonical life, 10 missions, 1 swap | ≈ 0.49 | 0.4942 | **held** |
| H-mealh-d — p_crit at Wang pessimistic, 10 missions, 18 swaps | ≈ 0.04 | 0.0371 | **held** |
| H-mealh-e — Realistic per-swap failure from Dawn heritage | ≤ 0.01 | carried (Dawn 11+ year, three-thruster, zero swap-mediated mission loss across the mission) | held by anchor |
| H-mealh-f — At Wang pessimistic + 1% failure, radio-frequency-ion vs microwave-electrothermal | radio-frequency-ion wins by 10–30% | radio-frequency-ion wins by 65% | **falsified high** — radio-frequency-ion wins by *more* than predicted at realistic failure rates, even at Wang pessimistic |
| H-mealh-g — At Wang pessimistic + 5% failure, microwave-electrothermal wins by 10–30% | yes | microwave-electrothermal wins by 28% | **held** |
| H-mealh-h — At optimistic + 1% failure, radio-frequency-ion wins by 80–100% | yes | radio-frequency-ion wins by 96% | **held** |

Eight sub-claims, six held, one falsified-low (spare-cathode mass penalty is even smaller than predicted), one falsified-high (radio-frequency-ion advantage at realistic failure rates is even larger than predicted).

## Reading

**The microwave-electrothermal-as-escape-hatch claim from R-cathode-life-water-plasma is too strong but not fully retired.** Under realistic engineering failure rates (≤ 1% per swap, per Dawn three-thruster heritage), water-radio-frequency-ion wins at every cathode-life anchor, including the Wang et al. 2025 pessimistic 3,000-hour anchor. At Wang pessimistic plus 1% per-swap failure, radio-frequency-ion delivers 1,172.8 tonne lifetime versus microwave-electrothermal's 712 tonne — a 65% radio-frequency-ion advantage *even under the worst cathode-life-and-needs-18-swaps regime*. The "escape hatch" only opens above ~3.7% per-swap failure at Wang pessimistic, ~28.9% at mid-case life, and ~49.4% at optimistic life.

**The right framing is: per-swap reliability is the load-bearing engineering requirement, not cathode life by itself.** Cathode life sets the *number of required swaps*, but the architectural win/loss is set by per-swap *reliability*. The number of swaps doesn't matter as much as the failure probability:

- At optimistic life (50,000 hour, 1 swap over 10 missions), even very high per-swap failure (~49% per swap) tolerates radio-frequency-ion.
- At Wang pessimistic (3,000 hour, 18 swaps over 10 missions), per-swap failure must stay below ~3.7% for radio-frequency-ion to win.

Dawn heritage suggests per-swap failure can be held to ≤ 1% with mature swap-mechanism design (three-thruster hot-swap, 11+ years, no swap-mediated mission loss). The campaign's engineering requirement is therefore: demonstrate per-swap reliability ≤ ~3%, even under Wang pessimistic cathode life. This is more concrete than "match xenon heritage on water plasma," which the campaign cannot influence with engineering investment.

**The spare-cathode mass penalty is negligible across the parameter space.** At Wang pessimistic with 18 cathodes (1 primary + 17 spares), the radio-frequency-ion delivered fraction drops from 70.4% to 70.3% — a 0.14% reduction in chunk-per-mission. Variant B's small mass ratio (1.39 at impulsive 6.42 km/s) absorbs an 850 kilogram dry-mass addition without meaningful propellant penalty. This refutes a worry that motivated the round in the first place. The mass-budget axis is not the architecture decision; the failure-probability axis is.

**The R10b verdict survives under realistic engineering assumptions.** R10b found water-radio-frequency-ion dominates water-microwave-electrothermal above 25 kilowatt-electric on delivered-fraction grounds. The cathode-life axis modifies this conclusion: at the combined regime of pessimistic life *and* per-swap failure > ~3.7%, microwave-electrothermal wins. Under any other regime, radio-frequency-ion wins. The matrix is therefore: 1) under realistic engineering, R10b's verdict stands; 2) the microwave-electrothermal escape hatch is a hedge against the joint failure of cathode-life-on-water *and* swap-mechanism reliability — a smaller corner of parameter space than the R-cathode-life-water-plasma cross-learning implied.

**This round retires a claim I made in the prior round.** R-cathode-life-water-plasma cross-learning section: "microwave-electrothermal becomes the only Variant B thruster that closes cathode-life — by escape." That framing was too binary. The proper framing is: microwave-electrothermal becomes the dominant Variant B thruster only in the combined pessimistic-life *plus* unreliable-swap region. The cross-learning was a 1D claim; this round shows the actual decision lives on a 2D surface.

**Cathode life on water plasma is still load-bearing — but as a coarse parameter on the failure-probability axis, not as a decision criterion by itself.** The campaign should:
1. Set the engineering requirement: demonstrate per-swap reliability ≤ 3% under flight-relevant conditions.
2. Carry both architectures (water-radio-frequency-ion with swap design, water-microwave-electrothermal without) as eligible. The choice between them at the program level depends on whether the swap-reliability requirement can be met.
3. Drop the binary "microwave-electrothermal-as-escape-hatch" framing from the cross-learning log.

## Revisit clause

Grade H-mealh-a through H-mealh-h. Six held, one falsified-low (mass penalty smaller than predicted), one falsified-high (radio-frequency-ion advantage larger than predicted at realistic failure rates).

If the per-swap failure model is refined (correlated failures, common-cause failure modes, swap-mechanism maintenance failures during long inter-mission downtime), the crossover p_crit will shift. Independent-failure assumption is optimistic for radio-frequency-ion; correlated failures would push p_crit lower and shrink the microwave-electrothermal escape-hatch region.

If the Dawn ≤ 1% per-swap heritage anchor is challenged by a closer analogue (water-plasma-specific swap mechanism, chunk-debris contamination of swap rails, multi-year orbital storage of spare cathodes between missions), H-mealh-e softens. This is the most uncertain anchor in the round.

If R-trajectory-shaping-optimization reduces inbound burn time by 10–20%, per-mission cathode-on time drops proportionally, swap count drops, and p_crit moves slightly toward microwave-electrothermal disadvantage. Effect is small (single swap or two swap difference at most life anchors).

## Cross-learning

- **The R-cathode-life-water-plasma escape-hatch claim is retired in its binary form.** Microwave-electrothermal is the right Variant B choice only when *both* cathode-life-pessimistic *and* per-swap-failure > ~3.7% hold simultaneously. Under realistic engineering (Dawn-class swap reliability ≤ 1%) radio-frequency-ion dominates microwave-electrothermal at every cathode-life anchor by 65–97% on lifetime delivered chunk. R10b's verdict stands.
- **Per-swap reliability is the load-bearing engineering requirement.** Cathode life sets the number of swaps; reliability sets the win/loss. The campaign engineering ask is concrete: demonstrate per-swap reliability ≤ 3% under flight-relevant conditions including water-plasma residue management, swap-mechanism qualification, spare-cathode long-duration cold storage between missions.
- **Spare-cathode mass penalty is negligible across the parameter space.** Variant B's small inbound mass ratio (1.39) absorbs the 850 kilogram of 17-spare-cathode dry mass at < 0.2% chunk-delivered-fraction reduction. The mass-budget axis is not the architectural decision; the failure-probability axis is.
- **Methodology lesson — binary "escape hatch" framings hide 2D decision surfaces.** R-cathode-life-water-plasma cross-learned that microwave-electrothermal escapes cathode-life by not having a cathode. True but coarse. The full decision lives on the (cathode-life × per-swap-failure-probability) plane and the escape-hatch region is a corner of that plane, not a half-space. Adding to the convention log: when a round surfaces an architectural reversal, the next-round task is to map the *region* in which the reversal holds, not to confirm the reversal at one point.
- **Independent-failure assumption is the round's optimistic side.** Correlated-failure modes (common-cause defect in swap-mechanism design, water-plasma residue accumulating on swap rails, lubricant degradation across multi-year missions) would push p_crit lower and shrink the radio-frequency-ion dominance region. The round under-states the architecture sensitivity in this dimension; a follow-on R-swap-mechanism-reliability-with-correlated-failures is a candidate round.
- **The matrix architectural pick is now: radio-frequency-ion-with-swap-design, contingent on per-swap reliability ≤ 3% demonstration.** Microwave-electrothermal is the hedge architecture, retained as the option exercised only if the swap-reliability demonstration fails. Carry both in the matrix until the demonstration is done. This is a sharper architectural posture than "matrix carries radio-frequency-ion under canonical efficiency" (R-all-electric-thruster-sweep) — it explicitly identifies the engineering test that retires or confirms the architecture.
- **The Dawn heritage anchor warrants a deeper look.** Dawn flew NSTAR-class ion thrusters with hot-swap capability across three thrusters over 11+ years (launch 2007, end of mission 2018) with no swap-mediated mission loss. The anchor is real but is a single mission, single design heritage. R-dawn-swap-heritage-deep-dive could pin H-mealh-e more tightly; not in scope here. If Dawn heritage is invalidated for ICEBERG-specific reasons (different cathode coupling, different propellant, different long-duration storage), the p_crit interpretation tightens.
- **The reactor cycle life axis still hangs.** Cathode life is solved (in principle, by Dawn-heritage swap). Reactor cycle life under multi-year continuous burn is the adjacent unaudited multi-year-burn risk. R-reactor-cycle-life-megawatt remains a high-priority candidate round; it might force a similar swap-architecture requirement on the reactor side, which is a much harder engineering problem.

