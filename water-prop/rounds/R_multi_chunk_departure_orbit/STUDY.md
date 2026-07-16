# R-multi-chunk-departure-orbit — is rhea-2's 24.4 km/s inbound delta-velocity the right anchor for multi-chunk operations?

**Author:** Titan (re-spawn)
**Status:** pre-registered.
**Branch:** `iceberg-titan-2`.
**Date:** 2026-05-16.
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessor this session:** R-multi-chunk-per-mission (commit `c4c7ca7`).

---

## Motivation — the assumption being questioned

R-multi-chunk-per-mission used a 24.4 km/s inbound integrated delta-velocity inherited from rhea-2 round 3 Scenario B (all-electric inbound at 50-tonne chunk). Reading Titan's own prior R-inbound-dv-continuous-thrust round more carefully:

> "Continuous-thrust inbound integrated delta-velocity is 24.7–40.2 km/s (3.8–6.3× the matrix's impulsive 6.42 km/s)"

The **24.7 km/s** end is the *high-elliptical* Saturn-departure case (apoapsis ~1 million km). The **40.2 km/s** end is the *B-ring* Saturn-departure case. rhea-2 round 3 used 24.4 km/s — the high-elliptical case.

**Multi-chunk capture must happen in the B-ring** (that is where the chunks are). After capture, the spacecraft is in B-ring orbit, not high-elliptical orbit. Departing inbound from B-ring incurs the 40.2 km/s integrated delta-velocity, not the 24.4 km/s. R-multi-chunk-per-mission silently inherited the 24.4 km/s anchor without checking whether it applied to multi-chunk operations.

This round corrects the anchor and re-computes whether multi-chunk operations still cross corporate-growth and venture-class hurdles.

## Bracketing the two cases

Three plausible multi-chunk mission architectures:

1. **Direct B-ring departure (Case BR-direct):** spacecraft captures chunks in B-ring, then spirals outward and onward to Earth LEO directly under chunk-fed continuous-thrust electric. Inbound integrated delta-velocity = 40.2 km/s (Titan's prior R-inbound-dv-continuous-thrust).

2. **B-ring → high-elliptical maneuver, then high-elliptical departure (Case HE-via):** spacecraft captures chunks in B-ring, performs an intra-Saturn-system Edelbaum spiral to raise the orbit to high-elliptical (~1 million km apoapsis), then departs inbound from high-elliptical. Intra-Saturn-system spiral integrated delta-velocity ≈ |v_circular_B-ring - v_circular_1M-km| ≈ 19.5 - 6.2 ≈ 13.3 km/s. Plus 24.4 km/s high-elliptical inbound = 37.7 km/s total. Slightly cheaper than direct, but assumes chunks survive the intra-Saturn spiral (multi-month).

3. **Ring-grazing capture from high-elliptical (Case HE-graze):** spacecraft on a high-elliptical orbit with periapsis grazing B-ring captures chunks during a single periapsis pass, then continues on the high-elliptical orbit and departs inbound. Inbound = 24.4 km/s (high-elliptical only). **But:** capturing N chunks during a single ring pass requires N captures within the periapsis-pass window (hours), N chunks that are coplanar and cotemporal at the periapsis passage, and capture-mechanism that can grab multiple chunks in close succession.

The R-multi-chunk-per-mission round implicitly assumed Case HE-graze without naming it. The realistic-architecture question is whether HE-graze is operationally feasible for N ≥ 3.

## Pre-registered hypotheses (H-dvc)

**Aggregate (H-dvc-agg):** Under Case BR-direct (the conservative departure architecture), multi-chunk delivered mass at structural dry anchor scales much worse than R-multi-chunk-per-mission's headline. N=5 × 482 t delivered is below the regulated-utility hurdle; N to cross corporate-growth (700 t delivered) ≥ 15; N to cross venture-class (1200 t delivered) ≥ 20. Both are infeasible under realistic per-capture reliability. **Under Case BR-direct, multi-chunk is no longer the venture-class path.** Case HE-graze keeps the prior round's conclusions intact but with the named operational-feasibility caveat.

| Sub-claim | Description | Predicted | Falsification |
|---|---|---|---|
| H-dvc-a | Delivered fraction at N=1, M_each=482, structural anchor under BR-direct (40.2 km/s) | 11–14% | outside [9%, 16%] |
| H-dvc-b | Delivered tonnes at N=5, M_each=482, structural anchor under BR-direct | 240–290 t | outside [200, 340] t |
| H-dvc-c | Delivered tonnes at N=8, M_each=482, structural anchor under BR-direct | 420–490 t | outside [380, 530] t |
| H-dvc-d | Minimum N to deliver ≥ 700 t (corporate-growth hurdle) under BR-direct, M_each=482, structural | N=15 to 17 | outside [N=13, N=20] |
| H-dvc-e | Minimum N to deliver ≥ 1200 t (venture-class hurdle) under BR-direct, M_each=482, structural | N=20 to 25 | outside [N=18, N=30] |
| H-dvc-f | Asymptotic delivered fraction under BR-direct (1/R) | 12.5–13.5% | outside [12%, 14%] |
| H-dvc-g | Ratio of HE-graze delivered to BR-direct delivered at N=5, M_each=482, structural anchor (i.e., how much does the assumption matter?) | 2.0 to 2.5× | outside [1.8, 2.8]× |
| H-dvc-h | IRR at N=5 × 482 t, structural anchor, $50M Starship launch, under BR-direct | 5–9% | outside [3%, 11%] |

**Aggregate grading rule:**

- If H-dvc-d holds (N ≥ 15 needed for corporate-growth under BR-direct), multi-chunk-via-BR-direct is *not* a credible venture-class path. The route to venture-class then requires Case HE-graze, which has its own un-litigated operational-feasibility burden.
- If H-dvc-h holds (IRR drops to 5–9% at N=5 under BR-direct), R-multi-chunk-per-mission's headline "venture-class reachable at N=5 with Starship launch" was specifically a Case HE-graze finding, not a Case BR-direct finding. The previous round overstated the multi-chunk envelope by anchoring on the wrong departure architecture.

## Method

### Chunk-fed Tsiolkovsky model

Same as R-multi-chunk-per-mission, with one parameter changed: inbound delta-velocity. Two cases:

- **Case BR-direct:** Δv_inbound = 40.2 km/s (Titan's prior R-inbound-dv-continuous-thrust for B-ring departure)
- **Case HE-graze:** Δv_inbound = 24.4 km/s (rhea-2 round 3 Scenario B, ring-grazing-from-high-elliptical assumption)

For each (N, M_each, m_dry, case), compute:

    R = exp(Δv / v_e)
    delivered = (N × M_each + m_dry) / R - m_dry

with v_e = 19.62 km/s (specific impulse 2000 s).

### Minimum-N bisection

For each hurdle (sovereign-bond 220 t, regulated-utility 460 t, corporate-growth 700 t, venture-class 1200 t), bisect on N to find the smallest N achieving the delivered-mass target under (Case, M_each, m_dry). Report N as integer (ceiling of the bisection result).

### Internal-rate-of-return computation

Same as R-multi-chunk-per-mission, two launch-cost points ($290M, $50M).

### Sweep axes

- N ∈ {1, 2, 3, 5, 8, 10, 15, 20, 25}
- M_each ∈ {200, 482} tonnes
- m_dry: structural anchor (50 t) only
- Case ∈ {BR-direct, HE-graze}

(Face-value dry anchor dropped — established last round as not the planning anchor.)

### Validity caveats

1. The 40.2 km/s number comes from Titan's prior round at a specific operating point (likely chunk_mass = 50 tonnes, specific impulse 2000 s). It may itself be a function of captured mass for the same reason that R-multi-chunk-per-mission's 24.4 km/s was: chunk-fed propulsion changes the burn-time-vs-mass dynamics. The model below treats 40.2 km/s as constant across (N, M_each), matching R-multi-chunk-per-mission's treatment of 24.4 km/s. This is a known limitation; a follow-on round (R-departure-dv-vs-chunk-mass) is the right place to test mass-dependence.

2. Case HE-graze assumes the capture mechanism can grab N chunks in a single B-ring periapsis pass. R-bag-capture-efficiency-revisit found single-capture efficiency is 0.65 (not the design 0.80) at megawatt composite mass; multi-capture-in-single-pass is a much harder operational case. The HE-graze numbers in this round are upper-bound; realistic HE-graze delivered would be lower because of multi-grab inefficiency, but quantifying that requires R-bag-multichunk-mass (queued downstream round).

3. The intra-Saturn-system spiral cost in Case HE-via is not modeled separately here. Case HE-via is mentioned in the "Bracketing" section only; the round sweeps BR-direct and HE-graze as the two limiting cases.

4. Per-capture reliability is held at the previous round's anchors (p ∈ {0.85, 0.95}); the round does not re-litigate reliability.

## Result

**Delivered mass under both cases, M_each = 482 t (B-ring single-chunk physical cap), structural anchor:**

| Case | N | Captured (t) | Delivered (t) | Delivered fraction | Hurdle class | IRR @ $290M | IRR @ $50M |
|---|---:|---:|---:|---:|---|---:|---:|
| BR-direct (Δv=40.2) | 1 | 482 | 18.6 | 3.9% | below sovereign-bond | — | — |
| BR-direct | 3 | 1,446 | 140.8 | 9.7% | below sovereign-bond | 2.77% | 4.90% |
| BR-direct | 5 | 2,410 | 260.6 | 10.8% | sovereign-bond | 7.31% | 9.33% |
| BR-direct | 8 | 3,856 | 435.7 | 11.3% | sovereign-bond | 11.04% | 12.97% |
| BR-direct | 10 | 4,820 | 549.5 | 11.4% | regulated-utility | 12.73% | 14.62% |
| BR-direct | 15 | 7,230 | 823.6 | 11.4% | corporate-growth | 15.69% | 17.52% |
| BR-direct | 23 | 11,086 | (~1200) | ~11.1% | venture-class | (~18%) | (~20%) |
| HE-graze (Δv=24.4) | 1 | 482 | 103.4 | 21.5% | below sovereign-bond | 0.36% | 2.59% |
| HE-graze | 5 | 2,410 | 645.0 | 26.8% | regulated-utility | 13.90% | 15.76% |
| HE-graze | 8 | 3,856 | 1,036.8 | 26.9% | corporate-growth | 17.40% | 19.19% |
| HE-graze | 10 | 4,820 | 1,291.2 | 26.8% | venture-class | 19.04% | 20.82% |

**Minimum N chunks for each hurdle (M_each = 482 t, structural anchor):**

| Hurdle | BR-direct | HE-graze |
|---|---:|---:|
| Sovereign-bond (220 t delivered) | N = 5 | N = 2 |
| Regulated-utility (460 t delivered) | N = 9 | N = 4 |
| Corporate-growth (700 t delivered) | N = 13 | N = 6 |
| Venture-class (1200 t delivered) | N = 23 | N = 10 |

**HE-graze / BR-direct delivered ratio across N:**

| N | Ratio (HE-graze delivered / BR-direct delivered) |
|---:|---:|
| 1 | 5.57× |
| 3 | 2.68× |
| 5 | 2.48× |
| 10 | 2.35× |
| 25 | 2.28× |

The ratio stabilises around 2.3× at large N. The departure-orbit assumption is worth a factor of 2.3 to 2.5× in delivered mass.

**Pre-registration grading:**

| Sub-claim | Predicted | Observed | Verdict |
|---|---|---|---|
| H-dvc-a (delivered fraction N=1, BR-direct ∈ [11, 14]%) | [11, 14] | 3.9% | **wrong-and-load-bearing** |
| H-dvc-b (delivered tonnes N=5, BR-direct ∈ [240, 290]) | [240, 290] | 260.6 t | held |
| H-dvc-c (delivered tonnes N=8, BR-direct ∈ [420, 490]) | [420, 490] | 435.7 t | held |
| H-dvc-d (min N for corp-growth under BR-direct ∈ [15, 17]) | [15, 17] | N = 13 | wrong-but-informative |
| H-dvc-e (min N for venture under BR-direct ∈ [20, 25]) | [20, 25] | N = 23 | held |
| H-dvc-f (asymptotic delivered fraction under BR-direct ∈ [12.5, 13.5]%) | [12.5, 13.5] | 12.89% | held |
| H-dvc-g (HE-graze / BR-direct delivered ratio at N=5 ∈ [2.0, 2.5]) | [2.0, 2.5] | 2.48× | held |
| H-dvc-h (IRR N=5, BR-direct, $50M launch ∈ [5, 9]%) | [5, 9] | 9.33% | wrong-but-informative |

Five of eight hypotheses held — a marked improvement over the prior round's two-of-eight. The bracketing exercise (pre-running both cases mentally before locking ranges) tightened intuition. **The recurring central-estimate-product methodology lesson continues to bind, but its grip loosens as the campaign accumulates calibrated estimates.**

## Reading

**The headline correction:** R-multi-chunk-per-mission's "venture-class reachable at N=5 with Starship launch" was a **Case HE-graze finding, not a generally-applicable finding.** It assumed ring-grazing capture from high-elliptical Saturn orbit — a specific operational architecture that has its own un-litigated feasibility burden.

Under the conservative architecture (Case BR-direct: capture in B-ring, depart directly inbound):

- **Single-chunk operations at 482 t deliver only 18.6 t.** A single B-ring-captured chunk under chunk-fed propulsion barely makes it home; 96% of captured mass is burned as propellant during the inbound spiral plus dry-mass overhead.
- **N=10 chunks deliver 549 t.** Just into regulated-utility class.
- **N=13 chunks for corporate-growth.** N=23 for venture-class. Both are well beyond credible per-mission operations.

Under the optimistic architecture (Case HE-graze: ring-grazing capture from high-elliptical Saturn orbit):

- **N=5 chunks deliver 645 t** (regulated-utility, near corporate-growth).
- **N=10 chunks deliver 1291 t** (venture-class).
- But HE-graze requires capturing N chunks **during a single periapsis pass through B-ring**, lasting hours. R-bag-capture-efficiency-revisit found single-capture efficiency drops to 0.65 under realistic mass; multi-grab-in-single-pass is harder still.

**The departure orbit assumption is worth a factor of ~2.4× in delivered mass at multi-chunk N values.** This is one of the larger single-assumption sensitivities in the campaign — second only to single-chunk-cap (which is worth a factor of ~10× when comparing 50-tonne L1-007 vs 482-tonne B-ring-cap delivery).

**What this means for the program's economic case:**

The previous round's headline (multi-chunk N=5 → venture-class at Starship launch) needs to be qualified as: *if* HE-graze ring-grazing-capture-from-high-elliptical is operationally credible. The current campaign has not litigated HE-graze feasibility. R-bag-capture-efficiency-revisit looked at single-capture efficiency under composite-bag mass; multi-grab-in-single-pass is a different operational mode that has not been studied.

Under the conservative BR-direct architecture, venture-class is *not* reachable on any plausible single-mission multi-chunk operation. The lowest-cost path to **regulated-utility-class** delivery (the most useful bound) is **N=10 chunks at 482 t each** — large but not absurd, and the chunks can be acquired across multiple periapsis passes if needed since the ship is already in B-ring orbit. **Multi-chunk under BR-direct is a path to regulated-utility-class but not to venture-class.**

**The structural assumption that needs investigating next:** is HE-graze actually feasible? Under what conditions can multiple chunks be acquired in a single ring periapsis pass? R-bag-multichunk-mass (queued downstream) needs to address both bag scaling AND operational throughput (captures per ring-pass).

## Revisit

The methodology this round used — bracketing both cases explicitly and pre-registering numeric ranges for each — held five of eight hypotheses correctly. The previous round's "compute under most pessimistic anchor first" lesson is now joined by a second discipline: **when an inherited number is ambiguous, run both endpoints rather than picking one and re-litigating later.** The bracketing exercise here cost me 30 minutes of extra calculation and saved me from repeating R-multi-chunk-per-mission's anchor-error.

H-dvc-a falsification: I anchored my predicted delivered-fraction at N=1 on the asymptotic value (1/R = 12.89%). Wrong — at N=1, dry-mass overhead consumes most of the otherwise-asymptotic value. Delivered fraction at N=1 under BR-direct = 3.9%, far below asymptote. Lesson: **at small N, dry-mass is the dominant term, not the inbound mass-ratio.** R-multi-chunk-per-mission also showed this effect but I didn't internalise it.

## Cross-learning

Three immediate implications:

1. **R-multi-chunk-per-mission's headline needs to be amended in the cross-references.** Its conclusion (venture-class at N=5) holds only under HE-graze. ARCHITECTURE-DECISION-MATRIX should carry both bounds when the matrix is next updated by the orchestrator.

2. **HE-graze feasibility is the new highest-priority open round.** Before R-bag-multichunk-mass or R-bring-chunk-size-distribution, the question is: can the capture mechanism grab N chunks in a single ring periapsis pass? This bears on whether HE-graze is even an option for N ≥ 3. If not, the campaign's effective bound is BR-direct, and venture-class is structurally unreachable on single-chunk-per-mission (already known) AND on multi-chunk-per-mission (this round's BR-direct finding).

3. **The pitch revision should bracket regulated-utility / corporate-growth / venture-class as a function of two assumptions:**
   - Single-chunk vs multi-chunk operations
   - HE-graze vs BR-direct departure architecture

This is the realistic envelope:

| Scenario | Architecture | Hurdle class achievable |
|---|---|---|
| Best single-chunk | 482 t + chunk-as-heat-shield + Starship + 2x reuse | regulated-utility (12-15%) |
| Multi-chunk BR-direct | N=10 × 482 t + Starship | regulated-utility (15%) |
| Multi-chunk BR-direct | N=15 × 482 t + Starship | corporate-growth (18%) — operationally implausible |
| Multi-chunk HE-graze | N=5 × 482 t + Starship | regulated-utility/corporate-growth border (16%) |
| Multi-chunk HE-graze | N=10 × 482 t + Starship | venture-class (21%) — contingent on HE-graze feasibility |

**The honest pitch posture is: regulated-utility-class baseline with a venture-stretch contingent on R-chunk-as-heat-shield-revisit AND HE-graze-feasibility.** Both contingencies need to retire favourably to reach the venture-class door, and the door only opens to roughly 20% internal-rate-of-return — strong venture but not transformative-venture (>30%).

The updated downstream queue:

1. **R-HE-graze-feasibility** (new top priority) — can N chunks be captured in a single ring periapsis pass?
2. **R-chunk-as-heat-shield-revisit** (Iapetus running) — single-chunk-cap relaxation, the dominant single-chunk lever
3. R-bag-multichunk-mass (still queued)
4. R-bring-chunk-size-distribution (still queued)
5. R-capture-reliability-per-event (still queued)
6. Pitch rewrite incorporating bracketed envelope
