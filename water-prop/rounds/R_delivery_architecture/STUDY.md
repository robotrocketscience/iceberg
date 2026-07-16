# R-delivery-architecture — does the chunk have to come to low Earth orbit?

**Author:** rhea (worker session)
**Status:** pre-registered hypotheses below; run.py + results to follow.
**Branch:** `iceberg-rhea-2` (this worktree).
**Date:** 2026-05-15 (evening, post-four-worker integration).
**Protocol:** per `water-prop/PROTOCOL.md` (rounds-with-revisit; pre-
registered numeric ranges).

---

## Motivation

After four-worker integration, the architecture decision matrix has
converged to one defensible cell (500-kilowatt-electric chemical-kick
plus electric-inbound) contingent on a reactor program that has not been
awarded (Fission Surface Power Phase 2 at five-times current scope). The
year-twenty-plus cell is structurally falsified under conservative
assumptions. Saturn's nominated rescue path is aerocapture or
chunk-as-heat-shield, which requires a thermal-protection-system
breakthrough at Technology-Readiness-Level 3 or below.

This round questions an assumption upstream of that framing: **the
inbound vehicle must terminate at low Earth orbit.** L0-02 specifies
delivery between low Earth orbit and geosynchronous Earth orbit, but
nothing in L0-01 through L0-23 says the deep-space vehicle itself must
land the chunk at low Earth orbit. A two-leg architecture — chunk to a
high-cislunar staging orbit, then a separate cislunar tug shuttles water
to low Earth orbit at customer demand — satisfies L0-02 and may dissolve
the integrated-continuous-thrust delta-velocity problem that titan
exposed.

This is one of the proposals from rhea's assumption audit
(`.session/ASSUMPTION-AUDIT.md` per the previous rhea session, integrated
into the orchestrator handoff). The audit identified
R-delivery-architecture as the highest-leverage new round. This document
is that round.

---

## Background: why low Earth orbit arrival is structurally hard

From titan's R-inbound-delta-velocity-continuous-thrust: the
*integrated* continuous-thrust inbound delta-velocity at low Earth orbit
arrival is 24.7 to 40.2 kilometres per second, 3.8 to 6.3 times the
matrix's impulsive 6.42 kilometres per second. The reason is that the
Edelbaum spiral from high-elliptical to low Earth orbit accumulates
delta-velocity continuously at low thrust; the impulsive equivalent
substantially undercounts the propellant requirement. From rhea's
prior rounds, the same problem applies to the outbound segment, so the
matrix had been undercounting both legs of any all-electric mission.

The root cause is structural, not numerical: any electric-propulsion
vehicle that must terminate at low Earth orbit pays a multi-tens-of-
kilometres-per-second integrated penalty in the final spiral phase. No
amount of reactor specific-power improvement removes this penalty; it is
intrinsic to the destination orbit's altitude relative to where the
spacecraft arrives from interplanetary cruise.

If the destination is not low Earth orbit but a high-cislunar staging
orbit (lunar distant retrograde orbit, Earth-Moon Lagrange Point 2,
or similar), the Edelbaum penalty disappears because the spacecraft
inserts via a single lunar flyby plus a small propulsive maneuver,
closer to impulsive equivalent. The continuous-thrust penalty is paid by
a *separate* cislunar tug shuttling water from the staging orbit to low
Earth orbit, and that tug — being short-haul, high-thrust, smaller, and
not encumbered with a multi-hundred-tonne chunk — pays the penalty in a
smaller integrated form.

This is the parsimony argument from the audit, restated quantitatively.

---

## Architectures compared

### A: whole-chunk-to-low-Earth-orbit via lunar gravity assist (status quo)

The matrix's surviving year-zero-through-fifteen cell. Deep-space
vehicle hauls the chunk all the way to low Earth orbit. Lunar gravity
assist tour absorbs about three kilometres per second of arrival
velocity-infinity; remaining inbound delta-velocity is paid propulsively.

Per titan: integrated continuous-thrust inbound delta-velocity 24.7
kilometres per second at high-elliptical Saturn departure, rising to
40.2 kilometres per second at the B-ring departure case.

### B: chunk-to-lunar-distant-retrograde-orbit, cislunar tug shuttles to low Earth orbit

Deep-space vehicle delivers the chunk to lunar distant retrograde orbit
(or Earth-Moon Lagrange Point 2). Insertion via single lunar flyby plus
small propulsive maneuver, approximately impulsive at 0.5 to 1.0
kilometres per second. A separately-launched cislunar tug docks at the
staging orbit and shuttles water to low Earth orbit, sized for
single-flight cargo of 5 to 50 tonnes per shuttle round-trip, drawing
its propellant from the chunk it shuttles (water-microwave-
electrothermal-thruster or electrolysis-fed methalox).

### C: streaming delivery

Deep-space vehicle processes water during inbound cruise; dispatches
small parcels (5 to 10 tonnes each, ten or so per fifty-tonne chunk).
Each parcel carries its own avionics, thermal control, and propulsion;
each arrives at low Earth orbit on a slightly different trajectory.
Processing hardware (electrolyzer or freeze-and-dispatch unit) lives on
the deep-space vehicle; per-parcel bus overhead is the operating tax.

### D: aerocapture or chunk-as-heat-shield (Saturn's nominated rescue path)

Held in the round as a comparison cell. Per R-chunk-as-heat-shield:
ballistic coefficient four thousand kilograms per square metre is forty
times Mars Global Surveyor; thermal protection at 12.6 kilometres per
second hyperbolic entry exceeds Low-Earth-Orbit Flight Test of an
Inflatable Decelerator envelope. Conditional on a thermal-protection
breakthrough that does not currently exist. Round assumes the
breakthrough closes and quantifies what closure would buy.

---

## Pre-registered hypotheses

Hypotheses pre-registered before run.py is executed. Per the
methodology lesson recorded in the previous rhea session
(`.session/STATE.md`): numeric ranges pre-registered only after a
back-of-envelope arithmetic check. Each hypothesis below includes the
back-of-envelope sketch that informed the range.

### H-delivery-architecture-a (deep-space leg of B versus A)

**Prediction:** Architecture B's deep-space-vehicle delivered fraction
of Saturn-captured mass to lunar distant retrograde orbit is 60 to 85
percent. Architecture A's deep-space-vehicle delivered fraction of
Saturn-captured mass to low Earth orbit at integrated continuous-thrust
accounting is 20 to 35 percent. **B's deep-space leg out-delivers A by a
factor of 2 to 4.**

**Sketch:** A's inbound continuous-thrust integrated delta-velocity is
24.7 kilometres per second (titan); Tsiolkovsky at specific impulse 2000
seconds, exhaust velocity 19.6 kilometres per second, propellant
fraction equals 1 minus exponential of negative 24.7 over 19.6, equals
about 0.716; delivered about 0.284. B's inbound is dominated by a
lunar flyby with about 0.5 kilometres per second propulsive trim plus
the same Saturn-departure and inbound-cruise-braking budget (3.5
kilometres per second total), exhaust velocity 19.6 kilometres per
second, propellant fraction about 0.164, delivered about 0.836.

**Held / falsified:** numerical comparison of computed delivered
fractions.

### H-delivery-architecture-b (cislunar tug class for B)

**Prediction:** Architecture B's total system delivered fraction (deep-
space leg times cislunar-tug leg) is 25 to 70 percent depending on
cislunar-tug propulsion class. With hypergolic (specific impulse 320
seconds) the total is 25 to 35 percent (worse than A). With methalox
(specific impulse 380 seconds) the total is 30 to 40 percent
(comparable to A). With electric or water-microwave-electrothermal-
thruster (specific impulse 2000 seconds) the total is 60 to 75 percent
(materially better than A).

**Sketch:** cislunar-leg delta-velocity 3.5 kilometres per second from
lunar distant retrograde orbit to low Earth orbit. Tsiolkovsky at the
three specific-impulse classes gives delivered fractions about 0.328,
0.391, 0.837 respectively. Multiply by deep-space leg's 0.836 → totals
about 0.274, 0.327, 0.700.

**Held / falsified:** numerical comparison.

### H-delivery-architecture-c (streaming dominated)

**Prediction:** Architecture C delivers less than Architectures A and B
in absolute fraction terms when processing-hardware fixed mass and
per-parcel bus overhead are accounted for. Specifically, C's delivered
fraction is in the 45 to 65 percent range, below B with electric tug
(60 to 75 percent) and possibly below A under continuous-thrust
accounting (depending on parcel-class).

**Sketch:** processing hardware on the deep-space vehicle, 5 to 10
tonnes fixed; per-parcel bus overhead 10 percent of parcel mass; per-
parcel arrival delta-velocity about 2 kilometres per second at parcel-
class specific impulse 1500 seconds. For a fifty-tonne chunk split into
ten parcels: 50 minus 7.5 fixed minus 5 overhead minus 4.9 arrival-
propellant equals 32.6 tonnes, or 65.2 percent.

**Held / falsified:** numerical comparison.

### H-delivery-architecture-d (Architecture B versus aerocapture rescue)

**Prediction:** Architecture B closes the year-twenty-plus delivery
problem at Kilopower-era reactor power (10 to 40 kilowatts-electric),
where Architecture D (aerocapture rescue) requires both a thermal-
protection-system breakthrough and a reactor power class equal to or
greater than the surviving 500-kilowatt-electric cell. **B reaches the
fifteen-year ceiling at lower reactor power class than D.** Falsified if
B requires reactor power class equal to or greater than 200
kilowatts-electric to close at the L0-05 ceiling.

**Sketch:** B's deep-space chunk-fed inbound delta-velocity is 3.5 to 4
kilometres per second (close to impulsive). At specific impulse 2000
seconds and propellant fraction 0.164 the time-of-thrust is dominated
by Saturn-departure spiral not by the LDRO insertion; this is similar
to Variant B's chunk-fed chemical scaling. Kilopower 10 kilowatts-
electric at specific impulse 2000 seconds gives about 1 newton thrust;
acceleration on a 50-tonne loaded vehicle is two times ten-to-the-minus-five
metres per second squared; time to accumulate 4 kilometres per second
is about 6.3 years — within L0-05 envelope if outbound is comparable.

**Held / falsified:** numerical comparison plus a closure check at
Kilopower-era reactor power.

### H-delivery-architecture-e (Architecture B closes Kilopower demonstrator-class)

**Prediction:** Under demonstrator-class waivers (any non-zero delivered
mass, L0-05 not applied) Architecture B closes a Kilopower mission at
10 kilowatts-electric with a 50-tonne chunk, delivered mass greater
than 25 tonnes to low Earth orbit. Architecture A under continuous-
thrust accounting at the same Kilopower 10 kilowatts-electric specific
power does not close a 50-tonne chunk delivery to low Earth orbit
because integrated continuous-thrust delta-velocity exceeds chunk-fed
propellant available.

**Sketch:** A at 10 kilowatts-electric, 50-tonne chunk, integrated 24.7
kilometres per second inbound: chunk-fed propellant is the chunk itself
minus delivered mass; mass-ratio at specific impulse 2000 seconds for
24.7 kilometres per second is exp(1.259) = 3.52. So for a chunk that
must self-fuel its inbound, delivered mass equals 50 over 3.52 equals
14.2 tonnes. B at 10 kilowatts-electric, same 50-tonne chunk,
integrated 3.5 kilometres per second: mass-ratio exp(0.178) = 1.195;
delivered 50 over 1.195 equals 41.8 tonnes. After cislunar tug at
specific impulse 2000 seconds and 3.5 kilometres per second the
cislunar-leg mass-ratio is 1.195; final delivered to low Earth orbit
equals 41.8 over 1.195 equals 35.0 tonnes.

**Held / falsified:** numerical comparison.

### H-delivery-architecture-f (questioning the audit's own claim)

**Prediction (steelmanning the criticism of my own audit):** Architecture
B does *not* eliminate the deep-space hard problem; it relocates it.
Specifically, the cislunar tug must operate water-shuttle at the
50-tonne-cargo class, which is roughly two orders of magnitude beyond
the largest existing cislunar tug operating envelope (Northrop Mission
Extension Vehicle handles low-single-digit tonnes of propellant per
servicing event). Architecture B's "easier" framing therefore inherits
a *new* technology-readiness risk — a 50-tonne cislunar water-shuttle
operating between lunar distant retrograde orbit and low Earth orbit —
that is itself unflown.

**Held / falsified:** held if existing cislunar tug operating envelope
is less than or equal to 10 tonnes of single-flight cargo; falsified if
an existing or near-term (Technology-Readiness-Level greater than or
equal to 5) cislunar tug class already operates at 50 tonnes or above.

**Note:** this hypothesis is testing my own audit's framing, not
testing Architecture B's numerical performance. Either resolution is
informative: H-delivery-architecture-f-held says the audit's
"parsimony" argument is partially overstated; H-delivery-architecture-f-
falsified says the audit's argument is on stronger ground than I gave
it credit for.

---

## What the round does NOT decide

- This round does not propose changes to REQUIREMENTS.md (orchestrator-
  owned).
- This round does not propose changes to the architecture decision
  matrix (orchestrator-owned).
- This round does not commit to Architecture B as a recommended
  architecture. It produces numbers for Saturn to integrate, in
  comparison to Saturn's nominated aerocapture rescue.
- This round does not investigate cislunar-depot infrastructure costs
  in detail. Depot-build economics are downstream and out of scope
  here.

---

## Constants and assumptions (for run.py)

- Standard gravity g0 = 9.81 metres per second squared.
- Specific-impulse classes for deep-space vehicle: 2000 seconds
  (radio-frequency ion baseline); 5000 seconds (dual-ion stretch);
  1500 seconds (Hall-effect fallback).
- Specific-impulse classes for cislunar tug: 320 seconds (hypergolic);
  380 seconds (methalox); 2000 seconds (water-microwave-
  electrothermal-thruster or electric).
- Deep-space-vehicle inbound delta-velocity, Architecture A
  (continuous-thrust integrated): 24.7 kilometres per second per
  titan high-elliptical; 40.2 kilometres per second per titan B-ring;
  6.42 kilometres per second per matrix impulsive equivalent for
  comparison.
- Deep-space-vehicle inbound delta-velocity, Architecture B (close to
  impulsive): Saturn-departure 1.5 kilometres per second + inbound
  cruise braking 2.0 kilometres per second + lunar-flyby-plus-trim 0.5
  kilometres per second = 4.0 kilometres per second total chunk-fed.
- Cislunar-tug delta-velocity from lunar distant retrograde orbit to
  low Earth orbit: 3.5 kilometres per second impulsive.
- Streaming Architecture C: 7.5 tonnes fixed processing hardware on
  deep-space vehicle; 10 percent per-parcel bus overhead; 2 kilometres
  per second per-parcel arrival propellant at specific impulse 1500
  seconds.
- Chunk masses: 50 tonnes (Kilopower-class) baseline; 100, 200, 500
  tonnes for higher reactor classes.
- Saturn-captured-mass-to-delivered-mass conversion includes only
  inbound legs. Outbound mass tax and Saturn-side ops mass are
  identical across architectures and out of scope for this comparison.

---

## Sources

- `water-prop/rounds/R_inbound_dv_continuous_thrust/STUDY.md` (titan,
  the integrated continuous-thrust delta-velocity finding).
- `water-prop/rounds/R_outbound_dv_continuous_thrust/STUDY.md` (rhea,
  outbound-leg symmetric correction).
- `water-prop/rounds/R_megawatt_marvl_radiator/STUDY.md` (rhea,
  MARVL-anchored mass model).
- `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` evening 2026-05-15
  revision.
- `REQUIREMENTS.md` v0.5.
- `ICEBERG-pitch.md` section 1 step 5 (lunar gravity assist tour and
  low Earth orbit insertion).
- `.session/ASSUMPTION-AUDIT.md` from prior rhea session (the proposal
  this round operationalises).

---

## Result

Full machine-readable output: `results/results.json`. Tables in
`results/tables.md`. Headline numbers (50-tonne chunk, deep-space
specific impulse 2000 seconds, cislunar tug specific impulse 2000
seconds):

| Architecture | deep-space delta-velocity (km/s) | delivered to low Earth orbit (tonnes) | delivered fraction |
|---|---:|---:|---:|
| A continuous-thrust, high-elliptical | 24.7 | 14.2 | 28.4% |
| A continuous-thrust, B-ring direct | 40.2 | 6.4 | 12.9% |
| A impulsive equivalent (matrix legacy) | 6.4 | 36.0 | 72.1% |
| B lunar distant retrograde orbit + water-microwave-electrothermal-thruster tug | 4.0 | 34.1 | 68.2% |
| B lunar distant retrograde orbit + methalox tug | 4.0 | 15.9 | 31.9% |
| B lunar distant retrograde orbit + hypergolic tug | 4.0 | 13.4 | 26.7% |
| C streaming, 10 parcels | n/a | 33.4 | 66.8% |
| D aerocapture rescue, 3-percent heat shield | 0.5 | 47.3 | 94.6% |

Architecture B with water-microwave-electrothermal-thruster tug
out-delivers Architecture A under continuous-thrust accounting by a
factor of 2.40 to 5.33 (depending on Saturn-departure case). Architecture
C (streaming) is approximately tied with Architecture B-electric.
Architecture D, conditional on a thermal-protection-system breakthrough
that does not currently exist, dominates both at 94.6 percent delivered
fraction.

### Hypothesis grading

| Hypothesis | Prediction | Computed | Verdict |
|---|---|---|---|
| H-delivery-architecture-a | B/A ratio 2–4× | 2.87× (high-elliptical) | **held** |
| H-delivery-architecture-a | B deep-space fraction 60–85% | 81.6% | **held** |
| H-delivery-architecture-a | A continuous-thrust fraction 20–35% | 28.4% | **held** |
| H-delivery-architecture-b (hypergolic) | 25–35% | 26.7% | **held** |
| H-delivery-architecture-b (methalox) | 30–40% | 31.9% | **held** |
| H-delivery-architecture-b (electric) | 60–75% | 68.2% | **held** |
| H-delivery-architecture-c | C delivered 45–65% AND dominated by B | 66.8%, approximately tied with B | **falsified high on range, weakly held on dominance** |
| H-delivery-architecture-d | D requires reactor ≥ 500 kWe | D works at Kilopower (chunk-fed delta-v is only post-capture trim) | **falsified** |
| H-delivery-architecture-d | B closes at lower reactor class than D | Both close at Kilopower; D dominates if breakthrough closes | **falsified on direction; D > B if it works** |
| H-delivery-architecture-e | B at Kilopower 50-t chunk > 25 t delivered | 34.1 t | **held** |
| H-delivery-architecture-e | A at Kilopower 50-t chunk does not close | A delivers 14.2 t (closes weakly, not "fails") | **falsified on binary close/don't framing** |
| H-delivery-architecture-f | Existing cislunar tug envelope ≤ 10 t single-flight cargo | Largest near-term ~3 t (Blue Origin Blue Moon Mk2 class); existing operating ~1-2 t (Impulse Helios) and below | **held** |

Three falsifications (H-delivery-architecture-c on the predicted range,
H-delivery-architecture-d on direction, H-delivery-architecture-e on
binary close/don't framing) and one held-as-steelman
(H-delivery-architecture-f). The audit's parsimony argument for
Architecture B is partially overstated — it relocates a hard problem
rather than eliminating it.

---

## Reading

1. **Architecture A under continuous-thrust accounting is structurally
   inferior to all alternatives.** A's 28.4 percent delivered fraction
   in the high-elliptical Saturn departure case is the floor any
   alternative needs to beat. B-electric beats it by 2.4×. C-streaming
   beats it by 2.4× (essentially tied with B-electric). D-aerocapture, if
   it works, beats it by 3.3×.

2. **The matrix's "no year-twenty-plus closure" finding is conditional
   on Architecture A.** The matrix's surviving year-zero-through-fifteen
   cell at 500-kilowatt-electric is sized against Architecture A's
   integrated continuous-thrust delta-velocity. Under Architecture B,
   the reactor-power requirement drops because the deep-space chunk-fed
   delta-velocity is 4 kilometres per second (close to impulsive) rather
   than 24.7 to 40.2 kilometres per second (continuous-thrust integrated).
   A Kilopower-class deep-space vehicle reaches the L0-05 ceiling under
   Architecture B; under Architecture A, only the 500-kilowatt-electric
   reactor class does. **The reactor-program risk that dominates the
   matrix's current state is an artefact of the delivery-architecture
   choice.**

3. **Architecture B is not free.** It requires a 50-tonne cislunar water-
   shuttle operating between lunar distant retrograde orbit and low
   Earth orbit. The existing and announced cislunar tug fleet operates
   at the 1-to-3-tonne class. A 50-tonne tug is roughly one-and-a-half
   orders of magnitude beyond near-term. This is a new engineering
   programme. The audit's claim that B is "more parsimonious" than A
   is overstated; B *redistributes* the hard problem from the deep-space
   leg to the cislunar leg.

4. **Architecture D (aerocapture rescue), if it works, dominates both A
   and B.** D delivers 94.6 percent of chunk because chunk-fed propulsion
   is only used for the post-capture trim of 0.5 kilometres per second.
   D's barrier is thermal-protection at four-thousand-kilograms-per-
   square-metre ballistic coefficient and twelve-point-six-kilometres-
   per-second hyperbolic entry, currently at Technology-Readiness-Level
   2 to 3.

5. **Architecture C (streaming) is competitive on delivered mass and
   parcel-count-insensitive.** Per-parcel delivered fraction depends on
   per-parcel bus overhead and per-parcel arrival propellant fraction;
   it does not depend on parcel count. This is a structural property of
   the architecture, not a sweep result. Parcel count is free to be
   chosen for operational reasons (ground-segment capacity, customer
   pull pacing, single-loss exposure). Streaming has its own readiness
   barriers (in-cruise processing hardware at 5 to 10 tonnes operating
   for 7 years autonomously at deep space) that are not in this round.

6. **The matrix's "rescue path" framing is incomplete.** Saturn nominated
   aerocapture or chunk-as-heat-shield (Architecture D in this round) as
   the next round. This round shows that Architecture B is a *different*
   rescue path that requires no thermal-protection breakthrough and that
   reaches comparable delivered fraction. The matrix should treat B as
   a peer to D, not as an alternative to consider only if D fails.

---

## Revisit

Pre-registered hypotheses were largely held in direction, but three
falsified on binary framing or on predicted range. Two of those (H-c,
H-e) repeat the methodology lesson recorded in the previous rhea
session: binary close-or-don't-close framings tend to falsify in either
direction; comparative range framings hold. Recording for the third
time: **future rhea rounds should pre-register comparative ranges only,
not binary close/don't-close hypotheses.**

H-delivery-architecture-d falsified on the reactor-power direction:
aerocapture eliminates the chunk-fed continuous-thrust burden, so
reactor power requirement drops to Kilopower-class regardless of
chunk size. This is a real finding that the matrix should integrate.

The audit's "parsimony" framing for Architecture B (H-f) is partially
overstated: B relocates rather than eliminates the deep-space hard
problem. The 50-tonne cislunar water-shuttle is itself an unprecedented
engineering programme. Architecture B's actual value is **reducing the
continuous-thrust integrated delta-velocity penalty**, not "simplifying
the program." Reframing required.

---

## Cross-learning

**Forward:** open R-cislunar-tug-design as a follow-on round if Saturn
adopts Architecture B as a peer to A in the matrix. Specifically: design
envelope for a 50-tonne cislunar water-shuttle, propulsion class trade
(water-microwave-electrothermal-thruster versus methalox versus
electrolysis-fed hydrogen-oxygen), service-life trade (single-shot
versus reusable), interface trade (lunar distant retrograde orbit
versus Earth-Moon Lagrange Point 2).

**Forward:** R-chunk-as-heat-shield-revisit (Saturn's nominated next
round) should now compare Architecture D not just against status-quo
Architecture A but against this round's Architecture B baseline.
Specifically: D's "rescue" value is the *delivered-fraction premium*
over B, not just the survival of the matrix versus A's continuous-
thrust failure mode.

**Backward:** the matrix's L0-05 closure analysis at 500-kilowatt-
electric is conditional on Architecture A. Under Architecture B, the
L0-05 ceiling closes at much lower reactor power class. The matrix's
"reactor program risk" framing softens to "depending on delivery
architecture choice, reactor program risk varies by an order of
magnitude in power class."

**Backward:** rhea's assumption audit (`.session/ASSUMPTION-AUDIT.md`
in the prior rhea session, handoff
`~/.claude/handoffs/iceberg-rhea-20260515-audit.md`) proposal #3 (open
R-delivery-architecture) is now executed and the proposal is supported.
But the audit's framing of Architecture B as "parsimonious" should be
revised — it is *less power-intensive* and *more existing-cislunar-tug-
extending*, not more parsimonious in the engineering-readiness sense.

**Methodology:** binary close-or-don't-close hypotheses falsify in
either direction at this stage of campaign maturity; pre-register
comparative ranges only.
