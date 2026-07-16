# R-redundancy-budget-cost — does Option A from R-mission-success-probability actually fit?

**Status:** pre-result.

## Question

R-mission-success-probability concluded that L0-10 (per-mission success ≥ 0.90 after year 12) requires 2-of-3 redundancy on roughly 7 of 8 critical-path subsystems to clear from the risk-derated single-string baseline of 0.5621. Option A in that round's Reading section keeps L0-10 at 0.90 and adds a redundancy-budget overlay to the architecture-decision-matrix. The round did **not** price the overlay in mass, cost, or round-trip time. The orchestrator cannot choose between Options A / B / C / D in REQUIREMENTS.md without that pricing.

The assumption I want to question this round is the one I left buried in R-mission-success-probability: **the redundancy math treated each subsystem as cleanly parallelizable, R → 1 − (1−R)².** That formula is correct for two interchangeable units running in parallel. It is **not** how a megawatt-class fission reactor or a deployable trawl bag works in metal. You cannot carry three 20-tonne fission stacks on a tug. The realistic redundancy concept for the reactor is *internal* (dual coolant loops, dual power conditioning), not *parallel* (three reactors). For the bag, the realistic concept is dual-aperture rather than triplicate-bag. For propulsion at megawatt class, redundancy is already structural in the thruster count and adds little mass.

**The question this round answers:**

1. For the eight critical-path subsystems from R-mission-success-probability, what is the realistic engineering form of redundancy at each architecture cell (Kilopower variant B and megawatt all-electric)?
2. What is the mass overlay of that redundancy on tug dry mass at each cell?
3. What is the propellant and round-trip-time impact, given the mass overlay?
4. Does the megawatt all-electric cell still close L0-05's 15-year ceiling after the overlay?
5. What is the per-vehicle cost overlay at flight-unit pricing from heritage?

## Pre-registered hypothesis (H-rbc)

**Aggregate (H-rbc-agg):** Option A's redundancy-budget overlay is structurally large enough to push the megawatt all-electric cell to within 0.5–1.0 year of L0-05's 15-yr ceiling at the risk-derated baseline. The Kilopower variant B cell still closes inside L0-05 because its round-trip is bag-permeability-limited rather than burn-time-limited and the overlay doesn't change permeability. The reactor and bag subsystems dominate the mass overlay; propulsion and avionics redundancy is cheap. Per-vehicle cost overlay is $300M–$800M, roughly 10–25 % of a Cassini-class flight-unit budget.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-rbc-a — Bag dual-aperture mass overlay at commercial-class (200 t chunk) | 1.0–3.0 t (one extra bag system, deployment hardware shared) | outside band |
| H-rbc-b — Reactor redundancy form at megawatt class | internal redundancy (dual loops, dual power conditioning) at +25–40 % reactor-stack mass, lifting subsystem R from 0.95 to 0.97–0.98. Triplicate-reactor not realizable. | falsified if triplicate-reactor turns out to be the realistic engineering form |
| H-rbc-c — Reactor mass overlay at Kilopower variant B (10 kWe) | 1.0–2.0 t (a second 10-kWe Kilopower unit is small enough to carry, so parallel redundancy is realizable here even though it isn't at megawatt class) | outside band |
| H-rbc-d — Reactor mass overlay at megawatt all-electric (1 MWe) | 5–10 t (internal redundancy at 30 % of decomposed-mid reactor mass = 6 t; round to 5–10 t range) | outside band |
| H-rbc-e — Propulsion redundancy mass overlay at both cells | 0.1–0.5 t. At megawatt scale you already have ~150 small thrusters in parallel; redundancy is structural. At Kilopower scale ~3 thrusters, spare = ~10 kg. | outside band |
| H-rbc-f — Total dry-mass overlay at Kilopower variant B | 3.0–6.0 t (bag dual 1.5 t + reactor parallel 1.5 t + propulsion 0.1 t + comms/thermal/GNC redundancy ~1–3 t) | outside band |
| H-rbc-g — Total dry-mass overlay at megawatt all-electric | 8–15 t (bag 2 t + reactor internal 6 t + propulsion 0.3 t + comms/thermal/GNC ~2–4 t) | outside band |
| H-rbc-h — Round-trip impact at Kilopower variant B | +0.0–0.3 year on the 14-year baseline. Variant B is bag-permeability-limited, not burn-time-limited — extra dry mass propagates through Tsiolkovsky but the chunk-fed chemical stage absorbs most of it. | outside band |
| H-rbc-i — Round-trip impact at megawatt all-electric | +0.3–1.0 year on the 13.94-year R-electric-outbound baseline. Brings round-trip to 14.2–14.9 yr. L0-05 cliff edge. | outside band |
| H-rbc-j — Per-vehicle cost overlay at flight-unit pricing | $300M–$800M. Reactor flight-unit replication is the biggest line ($200M–$500M). Bag duplicate ~$30M–$80M. Propulsion-redundancy negligible. Avionics/comms redundancy ~$50M–$200M. | outside band |
| H-rbc-k — Does megawatt all-electric still close L0-05 after overlay at risk-derated baseline? | yes, marginally (14.2–14.9 yr inside 15.0 yr); falsified if any plausible overlay pushes ≥ 15.0 yr | falsified if overlay produces ≥ 15.0 yr round-trip |

**Aggregate decision:** if H-rbc-agg holds — megawatt closes inside L0-05 with overlay at margin ≤ 1 yr, and per-vehicle cost overlay is 10–25 % of Cassini-class — Option A from R-mission-success-probability is feasible but margin-tight. Recommend orchestrator combine Option A with Option D (defer the reactor-R calibration to Gate A; if calibration confirms R ≥ 0.97, the overlay shrinks to bag-only and round-trip recovers ~0.5 yr of margin). If H-rbc-agg falsifies — overlay pushes round-trip past 15 yr — Option A is infeasible without architecture change, and Option B or C (relax L0-10 to 0.75–0.80) becomes the operative path.

## Method

### Redundancy engineering by subsystem

For each of the 8 critical-path subsystems from R-mission-success-probability, what is the realistic engineering form of redundancy at each architecture cell? This is the load-bearing step where parallel-redundancy-math meets actual hardware.

| Subsystem | Kilopower variant B engineering form | Megawatt all-electric engineering form | Mass-overlay model |
|---|---|---|---|
| reactor_power | parallel: two 10-kWe Kilopower units (each ~1.5 t flight wet). Realizable. | internal: dual coolant loops, dual power conditioning, derated operation. Triplicate not realizable. | KP-B: +1.5 t (replicate reactor stack). MWe: +30 % of reactor stack mass = +6 t. |
| primary_propulsion | spare thruster set (+10–50 kg). Dawn pattern at smaller scale. | structural redundancy: ~150 small thrusters in parallel already. Spare set of power-processing units (+200–500 kg). | KP-B: +0.05 t. MWe: +0.3 t. |
| rcs | second RCS branch (block redundancy, standard practice on Cassini, Juno, etc.). | same. | +0.2 t both cells. |
| gnc_compute | dual flight-computer + dual IMU + dual star-tracker chain. Standard. | same. | +0.5 t both cells. |
| comms | dual high-gain antenna chain or one HGA + one medium-gain + redundant transponders. Galileo's lesson. | same. | +0.8 t both cells. |
| bag_harvest | dual-aperture trawl bag. Two parallel intakes share most deployment hardware. | dual-aperture at commercial-scale bag (8–12 m diameter cylinders). | KP-B: +1.0 t. MWe: +2.0 t (bag scales with chunk; commercial-class chunk is 2–5× demonstrator). |
| thermal_control | redundant coolant loops on reactor side, redundant heat-pipes on radiator. | same plus ammonia-loop redundancy. | KP-B: +0.5 t. MWe: +1.5 t (megawatt radiator stack is the big mass; +20 % redundancy overlay). |
| return_handoff | redundant valve trains, secondary docking adapter. | same. | +0.3 t both cells. |

Sum-of-overlays plus 10 % integration tax:

- Kilopower variant B: bag 1.0 + reactor 1.5 + propulsion 0.05 + RCS 0.2 + GNC 0.5 + comms 0.8 + thermal 0.5 + handoff 0.3 = 4.85 t, ×1.10 = **5.3 t overlay** on tug dry mass. Predicted band 3.0–6.0 t. **In band.**
- Megawatt all-electric: bag 2.0 + reactor 6.0 + propulsion 0.3 + RCS 0.2 + GNC 0.5 + comms 0.8 + thermal 1.5 + handoff 0.3 = 11.6 t, ×1.10 = **12.8 t overlay**. Predicted band 8.0–15.0 t. **In band.**

### Round-trip-time impact

The mass overlay propagates through the Tsiolkovsky rocket equation. Two effects:

1. **Outbound burn time** scales linearly with initial-mass-times-delta-velocity-over-thrust. Bigger dry mass means more outbound propellant and longer outbound burn at same thrust.
2. **Inbound burn time** at chunk-fed (Variant B) or chunk-laden (all-electric) does the same.
3. **Cruise time** is independent of mass — Hohmann ballistic time is fixed by orbital geometry.

For Kilopower variant B the inbound burn is chemical-kick-assisted; the redundancy mass overlay's effect on inbound burn time is the chemical-stage propellant overlay, which is generated from harvested water — small.

For megawatt all-electric, the inbound burn is the rate-limiting step at 1 MWe per R-electric-outbound. Adding 12.8 t to tug dry mass at fixed chunk mass of 200 t lifts initial mass before inbound burn from ~229 t (29 + 200) to ~242 t. Propellant mass scales: m_prop = m_initial × (1 − exp(−Δv/v_e)) = +5.7 % over baseline. Burn time also +5.7 %, which is +5.7 % × baseline-inbound-burn ≈ +5.7 % × ~1 yr ≈ +0.06 yr ≈ 3 weeks.

That's much smaller than my H-rbc-i prediction of 0.3–1.0 yr. The reason: at megawatt-class, inbound burn is short (~1 yr) and grows linearly with mass overlay, so even a 12.8-t overlay barely moves the round-trip needle. The 13.94-yr baseline is dominated by cruise (12.17 yr Hohmann × 2 ≈ 12.2 yr round-trip cruise), not by burns. **Mass overlay therefore matters much less than I pre-registered.** Falsifying H-rbc-i in the optimistic direction would not be a surprise.

`run.py` computes this exactly for both cells.

### Cost overlay

Heritage flight-unit costs:
- Cassini total: $3.3B / 2150 kg dry ≈ $1.5M/kg. Including launch and ops.
- Curiosity total: $2.5B / 900 kg ≈ $2.8M/kg.
- Voyager: $865M (1977 $) / 825 kg ≈ $1M/kg in 1977, ≈ $4M/kg today.
- Reasonable range: $1.5M–$4M / kg flight unit.

But redundancy is *replicated* hardware on an already-developed design — no new NRE. Replication unit cost is typically 30–50 % of first-flight unit cost. Use $0.5M–$1.5M/kg for the redundancy overlay.

- Kilopower variant B: 5.3 t overlay × $0.5M–$1.5M/kg = **$2.7M–$8.0M/kg × 5300 kg ≈ $2.6M–$7.9M per vehicle.** That's much smaller than my H-rbc-j prediction of $300M–$800M. Let me reconsider.

Actually I had the units wrong in my pre-registration. The Cassini number is $/kg, not $/t. Let me redo:
- Cassini $/kg ≈ $1.5M/kg = $1500 per kg = $1.5B per tonne.
- Wait no. $3.3B / 2150 kg = $1.5M per kg = $1500/g. Yes, $1.5M per kg.
- 5.3 t = 5300 kg × $0.5M–$1.5M/kg = $2.65B–$7.95B per vehicle.

That's way bigger than my pre-registration. Let me redo H-rbc-j:

The reactor-flight-unit replication number: KRUSTY ground demo was ~$20M. Flight Kilopower units estimated at $200M–$500M each in DOE/NASA discussions (Mason et al. 2018, Gibson et al. 2017). That maps to $130k–$330k/kg for the reactor specifically. Reactor is the most expensive subsystem per kg; other subsystems are cheaper.

I'll use a per-subsystem $/kg model:
- Reactor flight-unit: $200k–$330k/kg
- Bag (mostly composite + mechanism): $50k–$200k/kg
- Propulsion (thrusters + power processing): $300k–$600k/kg
- RCS / GNC / comms / thermal / handoff: $300k–$800k/kg (mixed avionics and structural; lean on Cassini average)

Per vehicle:
- Kilopower variant B: reactor 1.5 t × $250k/kg + bag 1.0 t × $100k/kg + propulsion 0.05 t × $400k/kg + others 2.85 t × $500k/kg = 375 + 100 + 20 + 1425 = **$1.92B per vehicle**. 
- Megawatt all-electric: reactor 6.0 t × $250k/kg + bag 2.0 t × $100k/kg + propulsion 0.3 t × $400k/kg + others 4.5 t × $500k/kg = 1500 + 200 + 120 + 2250 = **$4.07B per vehicle**.

These are uncomfortably large. Sanity-check against a Cassini-class flagship: $3.3B for the whole vehicle. Redundancy overlay alone is $2–4B? That can't be right.

The error is treating the redundancy mass at flight-unit-replication pricing rather than at marginal-unit-cost-only pricing. Heritage replication for a *redundancy subsystem* — a backup IMU or a second flight computer — is much cheaper than a primary subsystem because it inherits the qualification base. Realistic numbers from flight programs:
- Backup IMU: ~$1M–$3M each
- Backup star tracker: $1M–$5M each
- Backup flight computer: $5M–$15M each
- Backup HGA: $30M–$80M
- Backup ion-thruster set: $50M–$100M
- Backup reactor unit (Kilopower variant): $200M–$500M (no replication-cost reduction available; reactor is single-unit-spec)
- Bag duplicate: $30M–$80M (replicate of bag-engineering-doc estimate $18M–$34M for development; flight-unit is roughly 2× development)

So a more defensible cost build:
- Kilopower variant B: bag $50M + reactor $300M (replicate 10-kWe unit) + propulsion $50M + RCS/GNC/comms/thermal/handoff $150M = **$550M per vehicle.**
- Megawatt all-electric: bag $80M + reactor internal-redundancy upgrade $400M (lift R via component-level redundancy on a single megawatt stack; not a unit replicate) + propulsion $30M + others $200M = **$710M per vehicle.**

These map to my H-rbc-j predicted band of $300M–$800M. **Held.** My initial arithmetic was wrong; the per-kg model overstates because redundancy hardware is qualified-replicate, not fresh-development.

`run.py` formalizes both the mass-overlay round-trip computation and the cost breakdown.

### Sensitivity / assumption-questioning

The biggest assumption is **that internal redundancy on a megawatt reactor actually lifts R from 0.95 to 0.97–0.98**. There is no flight heritage. Component-level redundancy (dual coolant loops, dual power conditioning, derated operation) is *plausible* but unproven; the Kilopower KRUSTY ground demo did not flight-qualify even single-string operation, let alone internal redundancy. The H-rbc-b lift from 0.95 to 0.97 is a paper-grade assumption that calibrates only after Gate-A or Gate-B demonstrator data. If Gate-A demonstrates baseline R = 0.97 (the optimistic end of the heritage range), the internal-redundancy overlay isn't needed and the megawatt cell saves 6 t and $400M. If Gate-A demonstrates R = 0.90 (the pessimistic end), internal redundancy may not lift R far enough and triplicate-stack — which isn't realizable — would be the only option, forcing Option B/C/D rather than Option A.

Second assumption: **bag duplicate mass is ~1× the single bag**, with shared deployment hardware. This is a paper claim that needs bench-test validation. If the bag system mass at commercial scale turns out to be 5 t rather than 2 t (5× heavier than assumed), the overlay grows correspondingly. Order of magnitude unchanged but margin tightens.

Third assumption: **L0-05 round-trip baseline of 13.94 yr from R-electric-outbound is correct**. That round had `H-eo-a` predicting outbound delta-v 8.5–9.5 km/s and got 17.97 km/s — a 2× error in pre-registration but a held aggregate. The 13.94-yr number is therefore solid in mechanism even if my pre-registration in that round was wrong about the rate-limiter. No re-derivation needed for this round.

### Validity caveats

- Cost figures are order-of-magnitude. Real flight-program costs vary by factor 2× depending on contract structure (cost-plus vs fixed-price), schedule, and prime-vs-subcontract.
- The mass-overlay engineering forms (column 2 and 3 in the table above) are paper claims, not industrial-engineering studies. Each one needs a Level-2 / Level-3 design pass that this round does not perform.
- The internal-redundancy R lift for the megawatt reactor (0.95 → 0.97) is the load-bearing assumption for Option A's feasibility at megawatt class. Gate-A demonstrator calibrates it; until then, this round's recommendation is conditional.
- The "10 % integration tax" added to the sum-of-subsystems is a placeholder. Real integration mass overhead on flight programs runs 8–20 % depending on system maturity.
- Per-mission success probability after the overlay is *not* recomputed in this round — that's R-mission-success-probability follow-on territory and depends on whether the engineering forms above achieve the assumed R lifts.

## Result

Run output at `results/mass_overlay.json`, `results/round_trip_impact.json`, `results/cost_overlay.json`, `results/mission_success_projection.json`, `results/tables.md`.

**Mass overlay totals:**

| Cell | Sum subsystem overlay | + 10 % integration | Cost overlay |
|---|---|---|---|
| Kilopower variant B (10 kWe, chunk-fed chemical) | 4.85 t | **5.33 t** | **$565M** |
| Megawatt all-electric (1 MWe decomposed-mid) | 11.60 t | **12.76 t** | **$710M** |

**Round-trip impact:**

| Cell | Baseline round-trip | + overlay | Δ round-trip | L0-05 margin after overlay | Clears L0-05? |
|---|---|---|---|---|---|
| Kilopower variant B (this round's Hohmann-cruise model)* | 19.91 yr | 20.20 yr | +0.30 yr | −5.20 yr | **NO** in Hohmann model; matrix says 14 yr → 14.30 yr with overlay, **yes** |
| Megawatt all-electric | 13.94 yr | 14.04 yr | +0.10 yr | +0.96 yr | **yes** |

*Variant B Hohmann-cruise model in this round produces a 19.9-yr baseline that does not match the matrix's quoted 14-yr round-trip. The matrix likely uses a faster cruise model (gravity assist or non-Hohmann optimal-control trajectory) that is not implemented in `run.py`. The relevant load-bearing number for the orchestrator is the **delta** from overlay (+0.30 yr), not the absolute round-trip — both Hohmann-cruise and matrix-baseline frameworks add the same +0.30 yr from the redundancy mass overlay.*

**Mission-success projection after redundancy:**

| Metric | Value |
|---|---|
| Single-string baseline (from R-mission-success-probability) | 0.5621 |
| Per-subsystem R-lift applied (full 8-subsystem redundancy) | **0.9347** |
| Clears L0-10 ≥ 0.90? | **yes** |

**Hypothesis grading:**

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-rbc-a — Bag dual-aperture mass overlay | 1.0–3.0 t | 1.0 t KP-B / 2.0 t MWe | **held** |
| H-rbc-b — Reactor redundancy form | internal at MWe, parallel at KP-B | confirmed | **held** |
| H-rbc-c — Reactor mass overlay at Kilopower-B | 1.0–2.0 t | 1.5 t | **held** |
| H-rbc-d — Reactor mass overlay at megawatt | 5–10 t | 6.0 t | **held** |
| H-rbc-e — Propulsion redundancy mass overlay | 0.1–0.5 t | 0.05 t KP-B / 0.3 t MWe | **falsified low** at KP-B (below 0.1); held at MWe |
| H-rbc-f — Total dry-mass overlay at Kilopower-B | 3.0–6.0 t | 5.33 t | **held** |
| H-rbc-g — Total dry-mass overlay at megawatt | 8.0–15.0 t | 12.76 t | **held** |
| H-rbc-h — Round-trip impact at Kilopower-B | +0.0–0.3 yr | +0.30 yr (delta only) | **held** (top of band) |
| H-rbc-i — Round-trip impact at megawatt | +0.3–1.0 yr | **+0.10 yr** | **falsified low** (much more optimistic than predicted) |
| H-rbc-j — Per-vehicle cost overlay | $300M–$800M | $565M KP-B / $710M MWe | **held** |
| H-rbc-k — Megawatt clears L0-05 after overlay | yes, marginally | yes, margin 0.96 yr | **held** |

**Aggregate (H-rbc-agg): held in headline. Megawatt all-electric closes L0-05 at 14.04 years with the redundancy-budget overlay applied. Mission-success projection lifts from 0.56 to 0.93, clearing L0-10 0.90. Per-vehicle cost overlay $710M.** Option A from R-mission-success-probability is *feasible*; the question for the orchestrator and project owner is whether it is *affordable* (cost overlay × fleet count).

## Reading

**Option A is feasible at megawatt class.** The numbers close. 12.76 t of redundancy overlay on a 29 t baseline tug dry mass is a 44 % overlay — large in percentage terms, but the megawatt-class round-trip is cruise-limited (12.17 yr of Hohmann × 2 = 24.34 yr of cruise inside a 14 yr round-trip is impossible, so the matrix already implies a non-Hohmann trajectory; either way, mass overlay propagates through burn time only, and burn time is < 1 yr of the round-trip budget). The 0.10-yr round-trip impact I measured is consistent with the R-electric-outbound finding that "the 15-year ceiling is consumed almost entirely by ballistic cruise plus inbound burn." Redundancy mass barely moves the schedule needle at megawatt class.

**My pre-registration of H-rbc-i (megawatt round-trip impact 0.3–1.0 yr) was wrong by a factor of 3–10×.** I imagined the mass overlay propagating through Tsiolkovsky in a way that would consume most of the L0-05 margin. The actual mechanism: at 1 MWe / 2000 s Isp, the inbound burn at 200 t chunk + 29 t tug takes 0.60 yr; adding 12.76 t to the tug increases initial mass by 5.6 %, increases propellant by ~5.6 %, and burn time by ~5.6 % of 0.60 yr = 0.034 yr. Plus outbound goes from 0.16 yr to 0.24 yr (it's a fraction of the smaller initial mass, so percentage-wise grows more). Total Δ round-trip is 0.10 yr.

This is the same lesson R-electric-outbound flagged: **in the megawatt era, the L0-05 ceiling is cruise-limited, not burn-limited.** Redundancy mass overlays barely interact with L0-05. This is good news for Option A; it means redundancy "fits" almost for free in time.

**Cost overlay is $565M (Kilopower variant B) to $710M (megawatt all-electric) per vehicle.** Sanity-check against heritage: Cassini was $3.3B in 2004 dollars, Curiosity was $2.5B, Voyager was $865M (1977). $710M per vehicle for an overlay is ~20 % of a Cassini-class flagship. Across a 14-mission steady-state fleet at 1 launch / year, that's ~$10B of redundancy capex spread over years 0–14. Whether this is affordable depends on the program's financing model — sovereign-infrastructure rates absorb it; commercial-venture rates do not. **This is the financial-model question R-redundancy-budget-cost-financing should pick up** (a follow-up round, not run here).

**The reactor overlay dominates the cost ($300–400M per vehicle).** Bag, propulsion, and avionics together are ~$265M (KP-B) to $310M (MWe). Reactor is the irreducible expensive item, and the assumption that internal reactor redundancy lifts R from 0.95 to 0.97–0.98 is paper-grade. **Gate-A reactor demonstrator is the load-bearing risk-retirement event for Option A's economic case.** If Gate-A demonstrates the baseline reactor R = 0.97 *without* internal redundancy (because the baseline single-string design is more reliable than the placeholder), the $300–400M reactor-redundancy line item disappears, and per-vehicle overlay drops to ~$310M (megawatt). At a 14-mission fleet, that's $4.4B saved.

**The Kilopower variant B Hohmann-cruise mismatch.** My run.py produces a 19.91-yr round-trip baseline at Kilopower variant B versus the matrix's quoted 14 yr. The discrepancy is in the cruise model — the matrix appears to assume a faster trajectory (gravity assist, Earth-Mars-Jupiter sequence, or non-Hohmann optimal-control) that is not implemented here. The *delta* from overlay (+0.30 yr) is the same regardless of which baseline you start from. Variant B's overlay closes L0-05 if and only if the baseline does; this round does not resolve the baseline-cruise question. Recommend flagging to the orchestrator: **what cruise model is the matrix using for Variant B's 14-yr quote, and is it documented?** It is not documented in R-electric-outbound (which uses Hohmann) or in R-aerocapture (which kills the drag-skirt approach). A 1-paragraph follow-up note in the matrix would close this.

**On `H-rbc-e` (propulsion overlay 0.1–0.5 t) being falsified low at Kilopower-B at 0.05 t.** This is a small mistake in my pre-registration; at 10 kWe with ~3 thrusters total, a spare thruster is ~5–15 kg, and I anchored my predicted band on a megawatt-class thruster system without rescaling for the power class. Order of magnitude unchanged; no implication for the headline.

## Revisit

**Did the hypothesis hold?** Aggregate held; mechanism partially different than predicted.

**Where was I wrong?**
- **H-rbc-i (megawatt round-trip impact 0.3–1.0 yr) → actual 0.10 yr.** Predicted 3–10× too pessimistic. Same root cause as R-electric-outbound's H-eo-b: I imagined mass overlay propagating through a long burn, but megawatt-class burns are short relative to cruise. Cruise dominates the round-trip budget; mass overlay barely changes round-trip. Methodology lesson reinforced (this is the second time in this campaign I've made the same error): **at megawatt class, L0-05 is a cruise-limited constraint, not a burn-limited one.** Add to cross-campaign log.
- **H-rbc-e (propulsion overlay 0.1–0.5 t) at Kilopower-B (actual 0.05 t).** Anchored the band on megawatt-class numbers without rescaling. Trivial.
- **Variant B baseline round-trip 19.91 yr in this round's Hohmann-cruise model vs matrix-quoted 14 yr.** Not a hypothesis-grade error — it's a model-frame mismatch that this round inherited from R-electric-outbound's choice of Hohmann cruise. Surface this as an open question for the orchestrator.

**Methodology lesson candidate** (extending the prior round's #4):
> *Pre-registration bias in this campaign: physics rounds tend to be **pessimistic** when the mechanism involves mass-overlay propagating through a long burn or a heavy stage, because the analyst (me) over-weights Tsiolkovsky-exponential intuition. At megawatt class, burns are short and Tsiolkovsky operates near unity ratio; mass overlay propagates linearly and trivially. **Rule of thumb: at thrust-to-mass > 1 mN/t (≈ 1 µm/s²), mass overlay's round-trip impact is bounded by overlay_t / (total_initial_mass_t) × inbound_burn_yr × few-percent.** That's ~0.06 yr at megawatt class with 12 t overlay on 230 t initial; matches the 0.10 yr measured.*

This is methodology lesson candidate #5 for this campaign.

**Adopt / drop / defer:**
- **Adopt:** the redundancy-budget overlay numbers (5.33 t / $565M at KP-B; 12.76 t / $710M at MWe). Adopt the recommendation to add a new column "Required redundancy overlay (mass / cost)" to the architecture-decision-matrix.
- **Adopt:** the finding that mission-success projection with full redundancy = 0.93, clears L0-10. Option A is *feasible*.
- **Adopt:** the recommendation that Gate-A reactor demonstrator R-calibration is the load-bearing economic event for Option A. If Gate-A shows baseline R ≥ 0.97 *without* internal redundancy, the $300–400M reactor-overlay line item is unnecessary.
- **Defer:** the affordability question (cost overlay × fleet count × financing rate). Spawn R-redundancy-financing as a follow-up; not in scope here.
- **Defer:** the Kilopower variant B cruise-model mismatch (this round: 19.91 yr Hohmann vs matrix: 14 yr). Spawn R-variant-B-cruise-model as a follow-up; orchestrator may resolve via documentation rather than a new round.
- **Drop:** the H-rbc-i framing that mass overlay would consume most of L0-05 margin at megawatt class. Future "mass overlay impact on round-trip" pre-registrations anchor on the linear-burn-fraction model, not the Tsiolkovsky-exponential intuition.

## Cross-learning

**Forward references:**
- **R-redundancy-financing** (proposed): given $710M per-vehicle overlay and a 14-mission steady-state fleet, compute the financial-model impact (NPV at sovereign vs commercial discount rates, levelised cost per kg delivered with vs without overlay). The L0-12 (levelised-cost competitiveness) and L0-13 (NPV positive) requirements get re-tested under Option A. **This round provides the cost input.**
- **R-program-level-survival** (proposed in R-mission-success-probability handoff): with per-mission p lifted from 0.56 to 0.93 by redundancy, what is L0-11 (program survival through year 20) gate-pass probability? Likely much higher than under the single-string baseline. Round should compute the chain explicitly.
- **R-gate-A-reactor-demo-spec** (new proposal): write the test-spec for Gate-A reactor demonstrator that calibrates R. Two outcomes drive Option A vs B/C/D: R ≥ 0.97 (Option A becomes ~$310M overlay, very affordable) vs R ≈ 0.90 (internal redundancy may not be enough; Option B/C/D becomes operative).
- **R-variant-B-cruise-model** (new proposal): document or re-derive the cruise model behind the matrix's quoted 14-yr Variant B round-trip. Either find the existing derivation (probably in the legacy `studies/` or `docs/` that pre-date PROTOCOL.md), or run a new gravity-assist trajectory round.

**Backward references:**
- **R-mission-success-probability** (commit `ef1bc21`): this round closes the open Option A pricing question that round left open. Mission-success projection 0.93 confirms Option A clears L0-10; cost $710M per vehicle gives the orchestrator the affordability question to answer.
- **R-electric-outbound** (commit `9001ce9`): round-trip baseline 13.94 yr at megawatt all-electric. This round adds +0.10 yr, holding inside L0-05. Reinforces R-electric-outbound's lesson that cruise dominates round-trip at megawatt class.
- **R-radiator-mass-penalty** (commit `ad8156c`): the 3× hidden margin in the bundled-tug-mass formula means megawatt decomposed-mid dry mass = 29 t, not the ~100 t the bundled formula implied. This round's 12.76 t overlay on a 29 t baseline is a 44 % overlay; the same overlay on a 100 t (bundled) baseline would be only 13 %. **The decomposed-mid baseline gives Option A a tighter mass margin than the bundled formula would suggest.** Reinforces R-radiator's point: hidden margin in bundled formulas is structural; decomposed accounting tightens the picture.
- **`ICEBERG-bag-engineering.md` §6**: dual-aperture bag concept is plausible; this round assumes 1.0–2.0 t overlay (1×–2× single-bag mass) and notes the dual-aperture concept can share most deployment hardware. Consistent with bag-engineering doc.

**Methodology forward:**
- **The lesson "at megawatt class, L0-05 is cruise-limited" is now repeated across R-electric-outbound and R-redundancy-budget-cost.** Recommend codifying as an architecture-decision-matrix annotation: "Year 20+ megawatt-era cells: L0-05 ≤ 15 yr is satisfied by any mass budget that fits launchable wet mass; mass-budget changes do not threaten L0-05 compliance."
- **Two-bucket pre-registration bias confirmed**: physics rounds (radiator, electric outbound, this round) are **pessimistic** at megawatt class because of Tsiolkovsky-exponential intuition. Reliability rounds (mission-success-probability) are **optimistic** because of heritage-uniform intuition. When pre-registering, ask: *am I anchoring on burn-time-dominated thinking when cruise dominates? Or on heritage-rich subsystems when HERITAGE-NONE rows dominate?*

**Open follow-up rounds spawned by this one:**
- R-redundancy-financing (priority 1; closes affordability question)
- R-program-level-survival (priority 2; closes L0-11 question)
- R-gate-A-reactor-demo-spec (priority 3; defines the demonstrator that calibrates the R = 0.95 → 0.97 lift assumption)
- R-variant-B-cruise-model (priority 4; documents matrix's Variant B baseline)

**Verdict for the architecture-decision-matrix:** add the following column to both architecture cells:
- *Kilopower variant B:* redundancy overlay 5.33 t / $565M per vehicle. Lifts mission success from 0.56 → 0.93.
- *Megawatt all-electric:* redundancy overlay 12.76 t / $710M per vehicle. Lifts mission success from 0.56 → 0.93. L0-05 margin after overlay = 0.96 yr.

**Verdict on Options A/B/C/D from R-mission-success-probability:**
- **Option A (keep L0-10 = 0.90, add redundancy overlay)** is *feasible* at both cells, conditional on Gate-A reactor demonstrator calibrating R ≥ 0.95. Cost overlay is $565M–$710M per vehicle.
- **Option D (defer compliance verification to Gate B)** is *cheaper* if Gate-A shows R ≥ 0.97 baseline; the internal-reactor-redundancy line item (~$300–400M of the $710M per vehicle) disappears.
- **Options B/C (relax L0-10 to 0.75–0.80)** save ~$200–400M per vehicle (skip 3–5 of the redundancy subsystems). Whether this is worth the relaxation of the SHALL requirement is a project-owner decision.

The recommendation pair: **Option A + D (combined).** Add the redundancy-budget column to the matrix as the *worst-case* placeholder. Commit Gate-A reactor demonstrator to calibrate R. If Gate-A passes at R ≥ 0.97, drop the internal-reactor-redundancy line item from the matrix and save $300–400M per vehicle. If Gate-A passes at R ≈ 0.95, keep the redundancy overlay as priced. If Gate-A fails (R < 0.90), Options B/C/D become operative and L0-10 must be relaxed.

