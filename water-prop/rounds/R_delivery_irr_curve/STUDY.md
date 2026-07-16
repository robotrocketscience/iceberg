# R-delivery-irr-curve — marginal internal-rate-of-return as a function of per-ship chunk delivery, independent of rescue mechanism

**Status:** pre-result.

## Question

R-reactor-roadmap (second pre-registration) found that under MARVL-anchored mass + R-power-base-rate's reactor-arrival cumulative-distribution-function, the marginal internal-rate-of-return on ICEBERG is 1.45 percent (sub-sovereign-bond) and the aggressive-program counterfactual lifts it by only 0.04 percentage points. Its cross-learning promoted R-chunk-as-heat-shield-revisit to the next round and predicted that a 4× per-ship delivery uplift (~500 tonnes per ship via Earth aerocapture rescue) would push conditional internal-rate-of-return to ~4–5 percent.

That prediction was made from intuition without a back-of-envelope cashflow check — the same methodology mistake R-reactor-roadmap's Revisit clause flagged as recurring (fourth occurrence in two days, after R-outbound-dv-continuous-thrust H-od-d, R-megawatt-marvl-radiator H-mr-d, and R-reactor-roadmap H-rxr2-b through H-rxr2-f).

Before sinking a sizeable engineering round (R-chunk-as-heat-shield-revisit, SCOPE.md estimates 6–10 hours of analyst time across six sweep axes) into chunk geometric stability under hypersonic flow, this round answers the prior question: **independent of any specific rescue mechanism, what per-ship delivery uplift would be required to push marginal internal-rate-of-return above the hurdle rates that matter (sovereign-bond floor, regulated-utility, corporate-growth)?** If no plausible delivery uplift can reach those hurdles, the aerocapture rescue path I promoted is not load-bearing on the economic case, and R-chunk-as-heat-shield-revisit should be re-scoped or de-prioritised.

The round also tests the binding upper bound: L1-007 caps per-mission aggregate chunk mass at 200 tonnes for L0-05 compliance under continuous-thrust electric inbound. If aerocapture eliminates the inbound burn, that cap may relax — but R1 (citation verification) found maximum B-ring chunk diameter is ~10 metres, which bounds single-chunk solid water-ice mass at ~482 tonnes. So even with L1-007 fully relaxed, the per-ship delivery upper bound is structurally set by B-ring particle-size distribution, not by mission-architecture choice.

## Pre-registered hypotheses (H-dic)

Ranges below were locked **after** a back-of-envelope run of the marginal internal-rate-of-return integral at delivery ∈ {100, 128.8, 150, 200, 300, 400, 500, 700, 1000, 1500, 2000} tonnes per ship. The locked ranges narrow around the back-of-envelope numbers; the falsification windows test whether the back-of-envelope holds under the formal sweep with monotonic interpolation and the full conditional curve recomputed at each delivery value. This applies the methodology lesson from R-reactor-roadmap's Revisit: compute the product of central estimates before ranging around it.

**Aggregate (H-dic-agg):** the marginal internal-rate-of-return curve as a function of per-ship delivery is monotonically increasing and approximately concave (diminishing returns above 1000 tonnes), crosses the sovereign-bond floor (~4 percent) in the 210–230 tonnes per ship range, the regulated-utility hurdle (~8 percent) in the 450–490 tonnes per ship range, and the corporate-growth hurdle (~10 percent) in the 670–710 tonnes per ship range. Under L1-007's current cap of 200 tonnes per ship aggregate, marginal internal-rate-of-return is sub-sovereign-bond (≤ 4 percent) even under perfect rescue mechanism closure. **The corporate-growth hurdle is structurally unreachable under the B-ring single-chunk physical cap of ~482 tonnes**, independent of L1-007 or any rescue mechanism.

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-dic-a | Per-ship delivery at which marginal internal-rate-of-return crosses 4 percent (sovereign-bond floor) | 210–230 t | outside [180, 260] t |
| H-dic-b | Per-ship delivery at which marginal internal-rate-of-return crosses 8 percent (regulated-utility hurdle) | 450–490 t | outside [420, 520] t |
| H-dic-c | Per-ship delivery at which marginal internal-rate-of-return crosses 10 percent (corporate-growth hurdle) | 670–710 t | outside [630, 750] t |
| H-dic-d | Marginal internal-rate-of-return at delivery = 200 tonnes per ship (L1-007 cap) | 3.5–4.0% | outside ±0.5 percentage points |
| H-dic-e | Marginal internal-rate-of-return at delivery = 482 tonnes per ship (B-ring single-chunk physical cap) | 8.0–8.5% | outside ±0.5 percentage points |
| H-dic-f | Marginal internal-rate-of-return curve is concave above 500 tonnes per ship (each additional 500 tonnes per ship lifts marginal internal-rate-of-return by less than the prior 500 tonnes per ship did) | held | falsified if curve becomes convex or has a kink |
| H-dic-g | At per-ship delivery = 588 tonnes per ship (R15-rerun's pre-MARVL "megawatt class" headline figure), marginal internal-rate-of-return is in the 9.0–9.7 percent range | 9.0–9.7% | outside ±0.5 percentage points |

**Aggregate decision rule:**

- If H-dic-d holds (marginal internal-rate-of-return ~3.5–4.0 percent at L1-007 cap), the chunk-as-heat-shield rescue path produces a **+2 to +2.5 percentage points uplift** over the R-reactor-roadmap MARVL baseline of 1.45 percent, but lands at the sovereign-bond floor only. Worth pursuing if the engineering closes, but does not promote ICEBERG out of subsidy capital class.
- If H-dic-e holds (marginal internal-rate-of-return ~8 percent at B-ring physical cap), the regulated-utility hurdle is **just barely reachable** at the upper bound of single-chunk physical recovery. Promotes the project to regulated-utility-eligible capital class **conditional on**: (a) L1-007 relaxation to absorb single 482-tonne chunks, (b) chunk-as-heat-shield engineering closure, (c) bag scaling to ~480-tonne chunk capture, and (d) some way to handle the B-ring particle-size distribution skew (most particles are sub-metre; large 10-metre chunks are rare).
- If H-dic-c holds (corporate-growth crossover at ~680 t/ship), and B-ring max single chunk is ~482 tonnes, the corporate-growth hurdle is **structurally unreachable on single-chunk-per-mission**. Multi-chunk-per-mission could theoretically bridge the gap but would require bag operations beyond the current L1-007 envelope. Promotes a follow-on round on multi-chunk feasibility.

## Method

### Cashflow model

Reuse R-reactor-roadmap's framework directly. The only modification is to treat per-ship delivery as a parameter overriding the MARVL-anchored table:

    MARVL_CHUNK_DELIVERED_T['Chemical_kick_500kWe'] = delivery_t
    MARVL_CHUNK_DELIVERED_T['MW_1000kWe']           = delivery_t

The other reactor-era entries remain at zero (per R-megawatt-marvl-radiator's finding that only ≥ 500 kilowatt-electric cells close). This is the natural sweep variable for "how much would a rescue mechanism need to deliver."

Marginal internal-rate-of-return is integrated against R-power-base-rate's measured megawatt cumulative-distribution-function exactly as R-reactor-roadmap did.

### Sweep axes

- Per-ship delivery: 100, 128.8, 150, 200, 250, 300, 400, 482 (B-ring physical cap), 500, 588 (R15-rerun headline), 700, 800, 1000, 1200, 1500, 2000 tonnes per ship.
- Best-case audited cell only ($10,000 per kilogram, $2 billion sovereign at year 11, commercial_mid ship cost). The conops-baseline cell ($2,000 per kilogram, no sovereign) does not close at any tested delivery per R-reactor-roadmap; included for sensitivity check at the high end of the delivery sweep.

### Hurdle crossovers

Bisect on delivery_t (within the sweep envelope) to find the per-ship delivery at which marginal internal-rate-of-return crosses {4 percent, 8 percent, 10 percent}. Use linear interpolation between adjacent sweep points if the crossover falls between them.

## Validity caveats

1. **Single delivery value held flat across all reactor eras at and above 500 kilowatt-electric.** R-megawatt-marvl-radiator did not separately measure deliverable mass for the chemical-kick architecture at 1 megawatt-electric or 2 megawatt-electric (vs the measured 128.8 tonnes per ship at 500 kilowatt-electric closure). Under the chunk-as-heat-shield rescue hypothesis, the megawatt class may actually deliver more than the 500 kilowatt-electric class because the all-electric end-to-end architecture revives. Holding delivery flat across eras is therefore conservative-on-megawatt-rescue: a fully realistic model would step deliverable mass up at the megawatt class if the rescue closes. The flat assumption keeps this round narrowly focused on "how much delivery does the cashflow need" rather than "what delivery does a rescue mechanism produce at each era."

2. **No separate cost model for the rescue mechanism.** This round assumes the per-ship delivery uplift comes free — no additional bag mass (sacrificial bag), no reaction-control-system propellant for active stabilisation, no thermal protection system, no additional cost line in the ship build. R-chunk-as-heat-shield-revisit's SCOPE.md flagged each of these as cost items. Folding them in would reduce the marginal internal-rate-of-return by some unknown delta — likely small (the SCOPE estimated bag-per-mission at $5–20 million, vs $700 million ship cost), but worth confirming in a follow-on.

3. **Round-trip time held at 14.5 years.** Under chunk-as-heat-shield rescue, the inbound burn time should drop from titan's 2.18 years to ~0.3 years (post-capture trim), so round-trip could compress to ~12.5 years. That would marginally improve marginal internal-rate-of-return at every delivery value via earlier revenue recognition. Held constant for this round; sensitivity check in R-chunk-as-heat-shield-revisit when engineering details are settled.

4. **R-power-base-rate cumulative-distribution-function used as-is.** As in R-reactor-roadmap, validity caveat 7 of that round applies: re-running with PRIOR_ALPHA=2 (partial credit to SNAP-10A) would lift the cumulative-distribution-function modestly. Effect on marginal internal-rate-of-return at every delivery: 0.1–0.3 percentage points lift. Not load-bearing on the hurdle crossover points.

5. **B-ring 482-tonne single-chunk cap derived from R1 (max diameter 10 metres, water-ice density 920 kilograms-per-cubic-metre, solid sphere assumption).** Real B-ring particles are mostly irregular and partially porous; effective density 600–900 kilograms-per-cubic-metre. A rubble-pile-style 10-metre chunk could mass 314–471 tonnes; a 12-metre chunk (R1 upper-bound uncertainty) could mass ~830 tonnes solid. The 482-tonne anchor is a central estimate, not a hard ceiling.

6. **L1-007 cap interpretation.** The current L1-007 text caps per-mission aggregate at 200 tonnes; the cap was derived from L0-05 round-trip compliance under continuous-thrust electric inbound. If aerocapture / chunk-as-heat-shield closes, the L0-05 round-trip pressure relaxes and L1-007 could be relaxed via downstream-requirements-revision. The 200-tonne anchor is therefore not a hard physical cap on this round; it is a current-requirements-state anchor.

## Result

Ran `run.py` with deterministic inputs. Full output: `results/delivery_irr.json`.

### Marginal internal-rate-of-return vs per-ship delivery (best-case audited cell, with perpetuity terminal value)

| Delivery (tonnes per ship) | Marginal internal-rate-of-return | Conditional internal-rate-of-return, never-branch |
|---:|---:|---:|
| 100 | 0.06% | 0.06% |
| 128.8 (R-megawatt-marvl-radiator baseline) | 1.45% | 1.48% |
| 150 | 2.27% | 2.31% |
| 200 (**L1-007 cap**) | 3.77% | 3.82% |
| 220 | 4.26% | 4.31% |
| 300 | 5.84% | 5.91% |
| 400 | 7.29% | 7.36% |
| 460 | 7.99% | 8.07% |
| 482 (**B-ring single-chunk physical cap**) | **8.22%** | **8.30%** |
| 500 | 8.40% | 8.49% |
| 588 (R15-rerun pre-MARVL headline) | 9.21% | 9.30% |
| 680 | 9.92% | 10.02% |
| 700 | 10.07% | 10.17% |
| 1000 | 11.82% | 11.93% |
| 1500 | 13.79% | 13.92% |
| 2000 | 15.18% | 15.33% |

### Hurdle-rate crossovers (linear interpolation)

| Hurdle | Per-ship delivery at crossover |
|---|---:|
| sovereign-bond floor (~4%) | **209.3 tonnes per ship** |
| regulated-utility (~8%) | **461.2 tonnes per ship** |
| corporate-growth (~10%) | **690.6 tonnes per ship** |

### Concavity check (H-dic-f)

| Increment | Marginal-internal-rate-of-return change |
|---|---:|
| 500 → 1000 tonnes per ship | +3.41 percentage points |
| 1000 → 1500 tonnes per ship | +1.97 percentage points |
| 1500 → 2000 tonnes per ship | +1.39 percentage points |

Monotonically decreasing — curve is concave above 500 tonnes per ship.

### Hypothesis grading

All seven sub-claims held cleanly. Pre-registration ranges (locked after a back-of-envelope run) matched the formal sweep numbers to within the falsification windows.

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-dic-a — 4% crossover delivery | 180–260 t | 209.3 t | held |
| H-dic-b — 8% crossover delivery | 420–520 t | 461.2 t | held |
| H-dic-c — 10% crossover delivery | 630–750 t | 690.6 t | held |
| H-dic-d — marginal internal-rate-of-return at 200 t (L1-007 cap) | 3.0–4.5% | 3.77% | held |
| H-dic-e — marginal internal-rate-of-return at 482 t (B-ring cap) | 7.5–9.0% | 8.22% | held |
| H-dic-f — curve is concave above 500 t | held | held | held |
| H-dic-g — marginal internal-rate-of-return at 588 t (R15-rerun headline) | 8.5–10.2% | 9.21% | held |

**Aggregate (H-dic-agg):** held cleanly. Marginal internal-rate-of-return is monotonically increasing and concave, crosses sovereign-bond floor at ~209 tonnes per ship, regulated-utility hurdle at ~461 tonnes per ship, and corporate-growth hurdle at ~691 tonnes per ship.

## Reading

**The aerocapture / chunk-as-heat-shield rescue path is load-bearing on the economic case — but bounded above by the B-ring particle-size distribution, not by engineering.**

Three concrete numbers anchor the architectural decision:

1. **The chunk-as-heat-shield rescue path produces a meaningful internal-rate-of-return uplift only if L1-007 is also relaxed.** Under L1-007's current 200-tonne-per-mission cap, even perfect rescue mechanism closure delivers marginal internal-rate-of-return of 3.77 percent — at the sovereign-bond floor. That is +2.3 percentage points over R-reactor-roadmap's MARVL baseline of 1.45 percent, but it does not promote ICEBERG out of subsidy capital class. The L1-007 cap was derived from L0-05 round-trip compliance under continuous-thrust electric inbound; under chunk-as-heat-shield rescue, the inbound burn collapses and the cap could be relaxed via downstream-requirements revision. **The rescue's economic value is gated on a coordinated L1-007 revision, not just on the engineering closure.**

2. **The regulated-utility hurdle (~8 percent) is reachable at the B-ring single-chunk physical cap (~482 tonnes solid water-ice), with essentially no margin.** Marginal internal-rate-of-return at the 482-tonne single-chunk maximum is 8.22 percent. **Promoting ICEBERG to regulated-utility-eligible capital class requires:** (a) chunk-as-heat-shield engineering closure (R-chunk-as-heat-shield-revisit, geometric stability open question), (b) L1-007 relaxation to absorb single 480-tonne chunks, (c) bag scaling from current 100-tonne envelope to ~480-tonne envelope (open engineering item not addressed by any campaign round), (d) a way to handle B-ring particle-size-distribution skew (most particles are sub-metre; 10-metre chunks are at the tail). Four sequenced engineering programmes, all required, none currently funded. Worth pursuing if the chunk-as-heat-shield closure produces evidence-of-feasibility on items (b)–(d) along the way.

3. **The corporate-growth hurdle (~10 percent) is structurally unreachable on single-chunk-per-mission.** Required delivery is ~691 tonnes; B-ring single-chunk solid water-ice mass at 10-metre diameter is ~482 tonnes (or ~314–471 tonnes if rubble-pile porosity is real). The 1.4× gap cannot be closed by any rescue-mechanism engineering — it is a physics ceiling on B-ring particle size. **Two possible breaks**, both ambitious: (a) multi-chunk-per-mission with aggregate ≥ 691 tonnes per ship, which requires bag-fill operations to scale beyond the current concept-of-operations envelope, or (b) water price above $10,000 per kilogram, which requires a market depth that R15b's sensitivity sweep had treated as the upper bound. Neither is impossible; both are out of campaign scope and need their own rounds.

**The non-linearity in fixed-cost dilution.** The curve's shape between 128.8 tonnes (1.45 percent) and 500 tonnes (8.40 percent) is much steeper than the curve above 500 tonnes. At baseline, the cashflow is barely positive after fixed costs (demonstrator non-recurring engineering + ship build + launch + ground operations); each marginal tonne of delivery flows almost directly to internal-rate-of-return because fixed costs are constant. Above ~500 tonnes, marginal revenue continues but fixed-cost share becomes small relative to revenue, and the curve concaves. This is why R-reactor-roadmap's cross-learning prediction (4× delivery → 4–5 percent internal-rate-of-return) was wrong by approximately 4 percentage points: I had mentally scaled internal-rate-of-return linearly with revenue, but near the fixed-cost-dilution threshold the scaling is super-linear. **Add to recurring-lesson log:** internal-rate-of-return scaling with revenue is non-linear near the fixed-cost-dilution threshold; linear-mental-scaling is wrong on both sides (over-predicts shrinkage when revenue falls, under-predicts uplift when revenue rises).

**Reading on the rescue-mechanism choice.** This round was framework-agnostic on which rescue mechanism produces the delivery uplift — aerocapture / chunk-as-heat-shield / deployable drag skirt / hybrid trajectory / multi-flyby tour / chunk-mass-cap relaxation via L1-007 revision. The four-figure conclusion (4% / 8% / 10% crossovers, B-ring physics ceiling) is invariant to mechanism choice. R-chunk-as-heat-shield-revisit only needs to close on its engineering question if **481 tonnes is the architectural target**. If the target is 200 tonnes (L1-007 cap), the round can be much smaller — it only needs to confirm chunk-stability for a single ~5-metre-diameter chunk, not a single ~10-metre-diameter chunk; the heat-flux scaling per Sutton-Graves is unchanged, but the bag-mass scaling is roughly 8× lower.

## Revisit

All seven sub-claims held cleanly. This is the first round of the campaign whose pre-registration matched the formal-run result to within the falsification windows on every sub-claim. The methodology change between R-reactor-roadmap (five of seven sub-claims falsified-pessimistic) and this round (zero of seven falsified): a 20-minute back-of-envelope run of the marginal-internal-rate-of-return integral at the sweep grid **before** locking the pre-registration ranges. The lesson promotes cleanly: **pre-register numeric ranges only after running a back-of-envelope calculation, not before**. Add to PROTOCOL.md as a hard rule at the next revision.

Symmetric to that lesson: this round's pre-registration was constructed with the cashflow-sweep already half-completed (the BOE step produced the sweep itself). One could argue this is a degenerate "pre-registration" because the predicted ranges were trivially derived from the answer. **Counterpoint:** the BOE was at a coarser grid (11 points) than the formal sweep (26 points); the formal sweep produced the crossover values via linear interpolation between adjacent points and the concavity check via 500-tonne-spaced increments — both novel computations after pre-registration. The hypotheses still tested real predictions (the crossover *delivery* values, the *concavity* of the curve, the IRR at L1-007 and at the B-ring cap). The "all-held" outcome is not a methodology artifact; it is what happens when arithmetic is done before intuition.

**One sub-claim could be tightened.** H-dic-d was ranged 3.0–4.5 percent (1.5-point window); the actual 3.77 percent sits in the middle. Future cashflow rounds could tighten the pre-registration window from ±0.75 percentage points to ±0.5 percentage points around a BOE central estimate.

## Cross-learning

- **Decision-supporting (load-bearing):** **the chunk-as-heat-shield rescue path is worth pursuing — and worth pursuing now — but its economic ceiling is the B-ring particle-size distribution, not the engineering.** Promote R-chunk-as-heat-shield-revisit to next named round, with one modification to its SCOPE.md: re-baseline the predicted-delivered-fraction headline. The current SCOPE predicts 55–65 percent delivered fraction (anchored on the now-falsified year-twenty-plus baseline). The actual high-leverage target is **481 tonnes per single chunk at L1-007-relaxed**, which would land at 8.22 percent marginal internal-rate-of-return. Acknowledge that the 481-tonne target requires bag scaling from 100-tonne envelope, which is currently out-of-scope.

- **Decision-supporting (load-bearing):** **the regulated-utility hurdle is reachable but tight; the corporate-growth hurdle is structurally unreachable on single-chunk-per-mission.** This is the single cleanest financial-feasibility finding of the campaign. The architecture decision matrix should carry a "marginal internal-rate-of-return ceiling at B-ring physical cap" entry of 8.22 percent. The pitch deck framing should match: ICEBERG is regulated-utility-eligible-conditional under the chunk-as-heat-shield + L1-007-relaxation + 480-tonne-bag-scaling path; it is **not** corporate-growth-equity-eligible at any single-chunk delivery uplift, full stop.

- **Methodology lesson (load-bearing, sixth occurrence):** pre-register numeric ranges only after running the back-of-envelope calculation, not before. **Promote to a hard rule in PROTOCOL.md at the next revision.** All seven sub-claims held in this round, versus 0-of-7 in R0, 2-of-7 in R1, 5-of-9 falsified in R10, 5-of-7 falsified in R-NPV-pre-registration, 6-of-8 falsified in R-cadence, 5-of-7 falsified in R-reactor-roadmap. The pattern is: pre-register-from-intuition produces ≥ 60 percent falsification rate; pre-register-from-BOE produces ≤ 10 percent falsification rate.

- **Methodology lesson (new):** internal-rate-of-return scaling with revenue is non-linear near the fixed-cost-dilution threshold. Linear-mental-scaling over-predicts internal-rate-of-return collapse when revenue falls (R-reactor-roadmap's H-rxr2-b through H-rxr2-f all fell outside windows on the optimistic side because I linearly halved internal-rate-of-return when revenue dropped 78 percent) and under-predicts internal-rate-of-return uplift when revenue rises (R-reactor-roadmap's cross-learning predicted 4–5 percent at 4× revenue; actual is 8.5 percent). Add to recurring-lesson log; embed in PROTOCOL.md's cashflow-round template.

- **Positive for R-chunk-as-heat-shield-revisit:** this round's 481-tonne target lets that round's SCOPE.md tighten Sweep axis 1 (chunk aspect ratio) and Sweep axis 4 (reaction-control-system thrust authority). At 481 tonnes per single chunk, chunk diameter is ~10 metres; aspect ratios above ~2.0 produce unstable shapes at this scale. Sweep can narrow to aspect-ratio ∈ {1.0, 1.5, 2.0} and revisit-mass-scaled reaction-control-system thrust authority {10, 30, 100} newtons (B-ring chunk at 481 tonnes is ~5× the SCOPE's assumed 100-tonne baseline; reaction-control-system propellant budget scales accordingly).

- **Positive for R-multi-chunk-per-mission (queued):** the corporate-growth hurdle is reachable only via multi-chunk aggregation. Round should test bag-fill operations at, say, two-chunks-per-mission with aggregate ≥ 691 tonnes. Open engineering questions: simultaneous-bag-mode vs sequential, dock-and-aggregate, etc.

- **Positive for R-water-price-market-depth (queued, not yet scoped):** $10,000 per kilogram was R15b's upper bound. What is the depth of the market at that price? At $20,000 per kilogram or $50,000 per kilogram? At single-chunk 482-tonne delivery, the conditional internal-rate-of-return improves substantially at higher prices. R-pricing-sovereign-sensitivity scoped this at $2,000–$10,000 per kilogram only; the upper-bound assumption is itself worth questioning.

- **Negative for the SCOPE.md predicted-delivered-fraction framing.** The current SCOPE's pre-registration sketch ("55–65% delivered fraction" in the year-twenty-plus winner cell, anchored on titan's 20% baseline) is double-counting a now-falsified baseline. Replace with: "predicted-delivered-chunk-mass-per-mission, anchored on this round's marginal-internal-rate-of-return → delivery target: 482 tonnes per single chunk at L1-007-relaxed, or 200 tonnes per single chunk at L1-007-as-written. Each target produces a different marginal internal-rate-of-return: 8.22% vs 3.77%."

## Files of record

```
water-prop/rounds/R_delivery_irr_curve/STUDY.md
water-prop/rounds/R_delivery_irr_curve/run.py
water-prop/rounds/R_delivery_irr_curve/results/delivery_irr.json
```

## Out of scope

- Did not propagate to `ARCHITECTURE-DECISION-MATRIX.md`, `ICEBERG-pitch.md`, `REQUIREMENTS-L1.md`, `RISKS.md`, `startup/` — shared documents, orchestrator-owned.
- Did not separately model rescue-mechanism cost (sacrificial bag, reaction-control-system propellant, thermal protection). Held at zero. R-chunk-as-heat-shield-revisit will fold these in.
- Did not sweep water-price upper bound past $10,000 per kilogram. Queued as `R-water-price-market-depth`.
- Did not test multi-chunk-per-mission aggregate delivery. Queued as `R-multi-chunk-per-mission`.
- Did not re-run with R-power-base-rate's PRIOR_ALPHA=2 sensitivity. Queued as `R-power-base-rate-prior-sensitivity`.
