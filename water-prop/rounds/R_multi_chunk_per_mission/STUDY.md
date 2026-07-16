# R-multi-chunk-per-mission — does capturing N chunks per mission unlock corporate-growth-class returns?

**Author:** Titan (re-spawn)
**Status:** pre-registered.
**Branch:** `iceberg-titan-2`.
**Date:** 2026-05-16.
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessor this session:** R-launch-cost-sensitivity (commit `8c29cdd`).

---

## Motivation

R-launch-cost-sensitivity established three findings that converge on a single open question:

1. The 10 percent corporate-growth hurdle at 200 tonnes per ship is structurally unreachable under any cost-side optimisation. Theoretical max internal-rate-of-return at zero fixed costs is 9.78 percent.
2. The 15 percent venture-class hurdle is unreachable at the B-ring physical single-chunk cap (482 tonnes per ship) even with all three levers fully pulled (free launch + 2× reuse + max delivery). Maximum achievable internal-rate-of-return is 14.65 percent.
3. The only remaining unexplored economic-uplift mechanism in the campaign is multi-chunk-per-mission — capturing N chunks rather than 1, with total captured mass exceeding the 482-tonne single-chunk physical cap.

R-delivery-irr-curve's hurdle crossovers map per-ship delivered mass to internal-rate-of-return: 220 tonnes for sovereign-bond, 460 tonnes for regulated-utility, 700 tonnes for corporate-growth, ~1200 tonnes for venture-class extrapolated. Multi-chunk is the only mechanism that can push delivered mass above the 482-tonne single-chunk cap.

This round tests whether multi-chunk-per-mission is technically feasible in the surviving Variant B architecture (500-kilowatt-electric all-electric inbound, chunk-fed propulsion) and what the marginal-internal-rate-of-return curve looks like as a function of (N chunks, mass per chunk).

## The assumptions being questioned

Three assumptions baked into the campaign's mass accounting:

1. **Single-chunk-per-mission is taken as the default architecture.** No round has explicitly modelled multi-chunk capture. R-bag-capture-efficiency-revisit assumed one bag, one chunk. R-delivery-irr-curve swept delivered-mass as a free parameter without specifying how mass above 482 tonnes was achieved.

2. **The 17-percent delivered-fraction from rhea-2 round 3 is treated as a constant.** Under chunk-fed propulsion, delivered fraction is *not* constant — it rises with captured mass because the vehicle's dry mass becomes a smaller fraction of total. R-chemical-trim-vs-all-electric-earth-arrival anchored the 17-percent number at a 50-tonne chunk reference; scaling to larger captured masses changes the fraction non-linearly.

3. **Ring-traversal delta-velocity between captures is small enough to ignore.** True for chunks in close proximity in the same B-ring annulus, but if N=5 chunks at 482-tonne class need to be sourced from spatially-separated ring regions, traversal cost may be material.

## Pre-registered hypotheses (H-mc)

**Aggregate (H-mc-agg):** Under chunk-fed Tsiolkovsky scaling with the empirical 24.4 km/s inbound delta-velocity from rhea-2 round 3, multi-chunk capture provides super-linear delivered-mass scaling because dry-mass overhead is amortised. Capturing N=3 chunks of 482 tonnes each (1446 tonnes total captured) delivers approximately 500–600 tonnes — above the regulated-utility hurdle (460 tonnes) but below the corporate-growth hurdle (700 tonnes). Capturing N=5 chunks of 482 tonnes (2410 tonnes captured) delivers approximately 850–1000 tonnes — crosses corporate-growth. **However, the B-ring particle-size distribution makes finding 5 near-cap-mass chunks in a single mission unlikely** (Tiscareno 2010 power-law slope on B-ring size distribution: number density of >5m-diameter chunks is sparse). The effective ceiling on multi-chunk under realistic chunk-availability is N=2 to 3 large chunks plus a tail of small chunks — total captured 800–1500 tonnes, total delivered 280–550 tonnes. **Corporate-growth hurdle is reachable but only at the upper end of the credible multi-chunk envelope.**

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-mc-a | Delivered fraction at 482 tonnes captured (single-chunk B-ring physical cap) | 28–34 percent | outside [25%, 38%] |
| H-mc-b | Delivered fraction at 1446 tonnes captured (3 chunks of 482) | 35–42 percent | outside [30%, 47%] |
| H-mc-c | Delivered fraction at 2410 tonnes captured (5 chunks of 482) | 38–45 percent | outside [33%, 50%] |
| H-mc-d | Delivered tonnes at N=3 × 482 tonnes captured | 500–600 t | outside [430, 680] t |
| H-mc-e | Delivered tonnes at N=5 × 482 tonnes captured | 850–1000 t | outside [800, 1200] t |
| H-mc-f | Marginal internal-rate-of-return uplift from N=1 (single 482 t, ~150 t delivered) to N=3 (3 × 482 t, ~550 t delivered) at current $290M launch baseline | +2 to +4 percentage points | outside [+1, +5] pp |
| H-mc-g | Marginal internal-rate-of-return at N=5 × 482 (above corporate-growth crossover) under $50M Starship launch | 14–18 percent | outside [12, 20] percent |
| H-mc-h | Mission-success probability under N independent captures with per-capture p=0.85 (R-mission-success-probability anchor): probability of full-N success at N=3 vs N=5 | 0.61 at N=3, 0.44 at N=5 | both held within ±0.05 |

**Aggregate grading rule:**

- If H-mc-d holds, multi-chunk is the path out of regulated-utility-class even without R-chunk-as-heat-shield-revisit (the 482-tonne single-chunk-cap regime applies only to N=1). N=3 large-chunk operations get you into corporate-growth-class territory without aerocapture.
- If H-mc-g holds, multi-chunk under Starship-class launch is the credible venture-class path. Combined with R-chunk-as-heat-shield-revisit it becomes the lead architecture.
- If H-mc-h holds, the expected-value calculation under independent-capture probability is sharply penalising for high N. Expected delivered mass at N=5 with p=0.85 per capture and binary all-success-or-zero accounting is 0.44 × full-N-delivered, ~440 tonnes — below corporate-growth. **Multi-chunk is sensitive to capture-reliability, and partial-capture-credited accounting (deliver what you got, drop the rest) becomes critical.**

## Method

### Chunk-fed Tsiolkovsky model

Vehicle starts inbound burn with total mass = N × M_each + m_dry. Vehicle ends inbound with total mass = (delivered chunk) + m_dry. Rocket equation:

    m_initial / m_final = exp(Δv / v_e)
    let R = exp(Δv / v_e)
    delivered = (N × M_each + m_dry) / R - m_dry

Parameters anchored to rhea-2 round 3 Scenario B (all-electric inbound, 50-tonne chunk delivering 17.0 percent):

- Δv_inbound = 24.4 km/s (rhea-2 Scenario B total)
- v_e = 19.62 km/s (specific impulse 2000 s, water electric thruster)
- R = exp(24.4/19.62) = 3.488
- m_dry calibrated so that at N=1 × M_each=50, delivered = 8.51 t → m_dry = 8.27 t. Held flat for multi-chunk extrapolation.

Validity caveat: the 8.27-tonne m_dry is implausibly low for a deep-space vehicle at megawatt-class power. The rhea-2 number likely folds outbound-leg losses into "delivered fraction" or uses a different mass-bookkeeping convention. **The model below explicitly notes this discrepancy and reports results under two anchors: (a) rhea-2 face-value (m_dry = 8.27 t) and (b) a structural anchor (m_dry = 50 t, plausible for a 500-kilowatt-electric vehicle without chunk).** Both anchors are reported; the load-bearing conclusions are checked against both.

### Ring-traversal delta-velocity

For N captures spaced over the B-ring's 25,500-km radial width, inter-chunk traversal Δv is bounded by Hohmann between two circular orbits at the ring's inner and outer edges:

    v_inner = sqrt(GM_saturn / 92,000 km) ≈ 19.9 km/s
    v_outer = sqrt(GM_saturn / 117,500 km) ≈ 17.6 km/s
    Hohmann Δv across the ring ≈ 0.3 km/s round-trip

For traversal within a single ring annulus (separation < 1000 km), Δv is < 50 m/s per inter-chunk transit. Assumed below as 100 m/s per inter-chunk transit (conservative midpoint). N captures → (N-1) × 100 m/s = (N-1)×0.1 km/s added to inbound burn budget. Folded into total Δv when computing chunk-fed Tsiolkovsky.

### Sweep axes

- N ∈ {1, 2, 3, 5, 8, 10}
- M_each ∈ {100, 200, 482} tonnes (chunk per-chunk mass)
- m_dry anchor ∈ {8.27 (rhea-2 face-value), 50 (structural plausible)} tonnes
- Reuse scenario: single-use baseline only (multi-chunk effect is orthogonal to reuse)
- Launch cost: $290M (current) and $50M (Starship)

### Probabilistic accounting

For each (N, p_capture):

- All-N success probability = p_capture^N
- Expected delivered (binary all-or-zero) = p_capture^N × full-N-delivered
- Expected delivered (partial credit, captures are independent Bernoulli) = N × p_capture × M_each_delivered_at_that_N (approximation; treats captured-mass as accumulating)

p_capture sweep: {0.85, 0.95}. Anchor 0.85 from R-mission-success-probability per-subsystem assumption; 0.95 from optimistic-redundancy R-redundancy-budget-cost projection.

### Internal-rate-of-return computation

For each (delivered_t) value computed, plug into R-conops-phase12-reuse's cashflow framework (which extends R-reactor-roadmap's). Compute IRR at $290M and $50M launch costs.

### Validity caveats

1. The m_dry calibration discrepancy noted above is unresolved by this round. Both anchors are reported; load-bearing conclusions are checked against the more pessimistic (m_dry = 50) anchor.

2. B-ring particle-size distribution as a constraint on chunk availability is not modelled quantitatively in this round. Tiscareno 2010 indicates a power-law slope of approximately -3 on particle diameter, with maximum diameter ~10 m corresponding to 482-tonne mass. Number density of 10-m chunks per cubic kilometre of ring is sparse (~one per several cubic km). A multi-chunk mission must either traverse a wide ring region to find N near-cap-mass chunks, or accept a mixed chunk-size distribution where mean M_each is well below 482. The model treats M_each as a free parameter; the project owner should interpret M_each = 482 as the upper limit (requires finding the largest available chunks).

3. Capture-mechanism mass scaling with N is not modelled. If each chunk requires its own bag and grappler, capture-mechanism dry mass scales linearly with N — increasing m_dry for higher-N missions and partially offsetting the multi-chunk delivered-mass advantage. Quantitative treatment is a follow-on round (R-bag-multichunk-mass).

4. The mission-timeline budget for phase 5 (capture mechanism deployment) and phase 6 (capture) is not modelled. N captures take longer than 1 capture; if each capture requires N days for rendezvous + grappling + stowing, N=5 missions spend 5× longer in the ring system, which may affect reliability (radiation dose, micrometeorite exposure) and propellant for station-keeping.

### Revisit clause

Per-claim grading vs H-mc-a..h. Cross-learning identifies whether multi-chunk promotes to the lead architecture, becomes a conditional upside, or falsifies.

## Result

**Delivered mass and internal-rate-of-return at M_each = 482 tonnes (B-ring single-chunk physical cap), structural dry-mass anchor (m_dry = 50 t):**

| N chunks | Captured (t) | Delivered (t) | Delivered fraction | Hurdle class | IRR @ $290M launch | IRR @ $50M launch |
|---:|---:|---:|---:|---|---:|---:|
| 1 | 482 | 103 | 21.5% | below sovereign-bond | 0.36% | 2.59% |
| 2 | 964 | 241 | 25.0% | sovereign-bond | 6.74% | 8.77% |
| 3 | 1446 | 377 | 26.1% | sovereign-bond | 9.99% | 11.95% |
| 5 | 2410 | 645 | 26.8% | regulated-utility (8%) | 13.90% | **15.76%** |
| 8 | 3856 | 1037 | 26.9% | corporate-growth (10%) | 17.40% | **19.19%** |
| 10 | 4820 | 1291 | 26.8% | venture-class (15%) | 19.04% | **20.82%** |

**Same sweep at M_each = 200 tonnes (more realistic per-chunk mass under B-ring chunk availability):**

| N chunks | Captured (t) | Delivered (t) | Hurdle class |
|---:|---:|---:|---|
| 1 | 200 | 22 | below sovereign-bond |
| 3 | 600 | 136 | below sovereign-bond |
| 5 | 1000 | 247 | sovereign-bond |
| 10 | 2000 | 515 | regulated-utility |

At 200-tonne per-chunk class, even N=10 captures (2000 t total) only delivers 515 t — regulated-utility but **not** corporate-growth.

**Probabilistic accounting at M_each = 482 t (structural anchor), all-N-success required:**

| N | p_capture | P(all-N success) | All-success delivered | Expected delivered (binary all-or-zero) |
|---:|---:|---:|---:|---:|
| 3 | 0.85 | 0.61 | 377 t | 232 t |
| 3 | 0.95 | 0.86 | 377 t | 323 t |
| 5 | 0.85 | 0.44 | 645 t | 286 t |
| 5 | 0.95 | 0.77 | 645 t | 499 t |
| 8 | 0.85 | 0.27 | 1037 t | 283 t |
| 8 | 0.95 | 0.66 | 1037 t | 688 t |
| 10 | 0.85 | 0.20 | 1291 t | 254 t |
| 10 | 0.95 | 0.60 | 1291 t | 773 t |

Under R-mission-success-probability's anchor of 0.85 per capture and binary all-or-zero accounting, the **expected** delivered mass at N=5 drops from 645 t to 286 t — well below corporate-growth. Reliability per capture is critical.

**Pre-registration grading:**

| Sub-claim | Predicted | Observed | Verdict |
|---|---|---|---|
| H-mc-a (delivered fraction N=1, 482 t, structural ∈ [28, 34]%) | [28, 34] | 21.5% | **wrong-and-load-bearing** |
| H-mc-b (delivered fraction N=3, 482 t, structural ∈ [35, 42]%) | [35, 42] | 26.1% | **wrong-and-load-bearing** |
| H-mc-c (delivered fraction N=5, 482 t, structural ∈ [38, 45]%) | [38, 45] | 26.8% | **wrong-and-load-bearing** |
| H-mc-d (delivered tonnes N=3 × 482 ∈ [500, 600]) | [500, 600] | 377 t | **wrong-and-load-bearing** |
| H-mc-e (delivered tonnes N=5 × 482 ∈ [850, 1000]) | [850, 1000] | 645 t | **wrong-and-load-bearing** |
| H-mc-f (IRR uplift N=1→N=3 at $290M ∈ [+2, +4] pp) | [2, 4] | +9.63 pp | **wrong-and-load-bearing** (uplift much larger because N=1 fails to close at structural dry) |
| H-mc-g (IRR at N=5 × 482, structural, $50M launch ∈ [14, 18]%) | [14, 18] | 15.76% | held |
| H-mc-h (P(all-success): N=3 ≈ 0.61, N=5 ≈ 0.44) | held | 0.6141 / 0.4437 | held |

Six of eight sub-hypotheses falsified, two held. **The methodology lesson recurs for the seventh consecutive time:** my predicted delivered fractions were anchored on the wrong dry-mass figure (I implicitly mixed rhea-2's face-value calibration into a structural-anchor prediction).

## Reading

**The structural finding is binary and load-bearing:**

**Multi-chunk-per-mission opens the door to corporate-growth-class and venture-class returns, but only under three simultaneous conditions:**

1. **N ≥ 5 captures of near-B-ring-cap chunks (≥ 482 t each).** N=5 × 482 t delivers 645 t — just into regulated-utility class; N=8 reaches corporate-growth; N=10 reaches venture-class.
2. **Per-capture reliability ≥ 0.95.** At 0.85 (R-mission-success-probability anchor), expected delivered mass under all-N-success accounting collapses by 50 to 70 percent. Multi-chunk is reliability-multiplicative; the program needs ≥ 0.95 per capture to support N ≥ 5 missions.
3. **Starship-class launch ($50M+).** At current $290M Falcon-Heavy + Vulcan-kick, N=5 × 482 t delivers 13.9% (regulated-utility-class) under all-success. Starship lifts it to 15.76% (just venture-class).

**The asymptotic delivered fraction is approximately 27 percent**, set by the 24.4 km/s inbound delta-velocity and the 19.62 km/s exhaust velocity. This is a structural ceiling: bigger captures don't materially increase delivered fraction past 27%. The economic-leverage effect of multi-chunk comes from absolute delivered mass crossing the hurdle thresholds, not from improved efficiency.

**The corporate-growth hurdle (10% IRR) requires delivered ≥ 700 t.** Under structural dry-anchor + Falcon Heavy launch, this requires **N = 8 captures of 482-tonne chunks (3856 t captured)**. Under Starship launch, it relaxes to **N = 5 captures**. Under face-value dry-anchor (implausibly optimistic), it relaxes further to N = 4-5.

**The venture-class hurdle (15% IRR) requires delivered ≥ 1200 t (extrapolated from R-delivery-irr-curve).** Under structural anchor + Starship, this requires **N = 8 captures**. Under current launch, N = 10 captures barely clears at 19% IRR — but the reliability constraint at N = 10 makes this implausible (P(all-success) = 0.20 at p = 0.85).

**Why this round's results conflict with R-launch-cost-sensitivity's conclusion:**

R-launch-cost-sensitivity said venture-class is structurally unreachable under any cost-side optimisation. This round shows venture-class IS reachable — but the lever is *delivered mass*, not *cost*. **Delivered mass at N = 10 × 482 t (1291 t) clears the venture-class threshold of 1200 t.** R-launch-cost-sensitivity bounded delivery at 482 t (single-chunk physical cap); this round relaxes that bound by accepting multi-chunk operations.

**The N = 5 to 8 regime is the credible "stretch" architecture.** Below that, multi-chunk doesn't add enough delivered mass to cross meaningful hurdles. Above N = 8, ring-search and capture-mechanism complexity become severe. The sweet spot is N = 5 to 8 large chunks per mission — a non-trivial but bounded engineering problem.

## Revisit

The seventh-consecutive methodology lesson lands with a refinement: **not just "compute the product of central estimates first," but specifically "compute the product under the most pessimistic credible anchor first."** I knew the rhea-2 face-value dry-mass anchor was implausibly low (8.27 t for a 500-kilowatt-electric vehicle is not credible) but I anchored my predicted ranges on the face-value number anyway because it was the empirical calibration point. The structural anchor (50 t) is the correct planning number, and my predictions should have been built on it. The face-value anchor remains a useful debugging cross-check but is not the planning-anchor.

The 21.5% delivered fraction at N = 1, 482 t (structural anchor) is the right number to feed into ARCHITECTURE-DECISION-MATRIX for single-chunk Variant B operations. The current matrix carries 17 percent from rhea-2's 50-tonne-chunk run; **this round suggests the matrix should be updated to ~22 percent at 482-tonne-chunk-class, accounting for the dry-mass amortisation as captured mass grows**. This is a candidate orchestrator-pass note rather than a worker edit.

## Cross-learning

Three downstream directions:

1. **R-capture-reliability-per-event is now the binding round.** Multi-chunk N = 5 to 8 requires per-capture reliability ≥ 0.95. R-mission-success-probability projected 0.85 per major subsystem under single-string; reaching 0.95 likely requires the 2-of-3 redundancy overlay from R-redundancy-budget-cost (at $565M to $710M per vehicle). The economic case for multi-chunk thus circles back to the L0-10 Option B-vs-A discussion: **multi-chunk multi-capture missions push capture reliability requirements above the current L0-10 = 0.80 baseline.** This may require revisiting the project-owner-locked Option B.

2. **R-bag-multichunk-mass is the second downstream round.** Multi-chunk requires either a larger single bag (mass scales with volume, roughly N^(2/3) for spherical packing) or multiple bags (mass scales linearly with N). At N = 5, bag-mass overhead may be 5× single-chunk; this propagates into m_dry. If m_dry rises to 100-150 t for a multi-chunk vehicle, delivered fraction drops further. The structural anchor in this round (50 t) is single-chunk-class; multi-chunk-class dry mass is likely higher.

3. **B-ring chunk availability at near-cap-mass needs a quick literature pass.** Tiscareno 2010 power-law slope on B-ring particle size distribution. If the number density of 10-m-diameter (482-tonne) chunks is so low that finding 5+ in a single ring traversal is implausible, the M_each = 482 column collapses to a more realistic M_each ≈ 200 to 300 mean — and N = 5 at M_each = 200 only delivers 247 t (sovereign-bond, not corporate-growth). **B-ring chunk-size statistics are the binding ground-truth on the multi-chunk envelope.**

The conops augmentations status update (R-conops-skeleton's queue):
- A-ph11-dv: closed (R-delivery-architecture covered)
- A-ph7-regime: closed
- A-ph6.5-mass: closed (low-leverage)
- A-ph12-reuse: closed (bounded uplift, this session)
- A-ph4-orbit: still queued, moderate
- A-c1-contingency: still queued, moderate

**New downstream queue (in priority order):**

1. R-capture-reliability-per-event (binding for multi-chunk economics)
2. R-bag-multichunk-mass (binding for multi-chunk feasibility)
3. R-bring-chunk-size-distribution (binding for multi-chunk ground truth)
4. R-chunk-as-heat-shield-revisit (Iapetus running, dominant single-chunk lever)
5. ICEBERG-pitch rewrite incorporating both regulated-utility-baseline AND multi-chunk-venture-stretch postures

This round's recommendation for the project owner: **multi-chunk is the credible venture-class path, but it has three new binding contingencies (capture reliability, bag scaling, chunk-size availability) that are individually less expensive to test than R-chunk-as-heat-shield-revisit. Worth pursuing all three in parallel before re-committing to a single-architecture stance.**
