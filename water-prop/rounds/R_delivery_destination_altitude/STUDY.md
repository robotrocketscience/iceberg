# R-delivery-destination-altitude — is titan's continuous-thrust penalty destination-conditional?

**Author:** rhea (worker session)
**Status:** pre-registered.
**Branch:** `iceberg-rhea-2`.
**Date:** 2026-05-15 (evening).
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessor in this session:** R-delivery-architecture (commit `e2fc68e`).

---

## Motivation and the assumption being questioned

R-delivery-architecture (just committed) established that Architecture B
(chunk to lunar distant retrograde orbit plus cislunar tug) out-delivers
Architecture A (whole chunk to low Earth orbit) by 2.4 times under
titan's continuous-thrust integrated delta-velocity accounting. The
mechanism that drives B's advantage is **avoiding the low-Earth-orbit
Edelbaum spiral.**

This round asks the same question one level upstream: **does L0-02
actually require low-Earth-orbit delivery?**

Reading the literal text: "L0-02. Project ICEBERG SHALL deliver
harvested water to customers in low Earth orbit or medium Earth orbit.
... altitude between 250 kilometres (low Earth orbit floor) and 35,786
kilometres (geostationary altitude, medium Earth orbit ceiling)."

The requirement admits any altitude up to geostationary. The matrix and
titan's continuous-thrust round both implicitly assumed *low* Earth
orbit as the delivery destination. If the delivery is instead to a
geostationary or near-geostationary orbit, the continuous-thrust
Edelbaum spiral terminates at much higher altitude where circular
velocity is much lower, and the integrated delta-velocity is
correspondingly smaller.

If this works, it is a parsimony win over the previous round:
Architecture A's framework is preserved, no new cislunar tug class is
needed, and the continuous-thrust integrated penalty drops by a factor
of two to four. The chunk arrives at geostationary, the customer
either operates there or pays for the geostationary-to-low-Earth-orbit
transfer themselves (per L0-02's "if a cislunar customer later emerges,
they are responsible for the transfer from delivery orbit to their
location" framing).

---

## The continuous-thrust scaling

The Edelbaum approximation for continuous-thrust circular-to-circular
transfers gives integrated delta-velocity equal to the absolute
difference in circular orbital velocity at the two altitudes:

  delta-velocity_Edelbaum = | v_circular_initial − v_circular_final |

Where v_circular = square-root of (Earth-gravitational-parameter divided
by orbital-radius), in metres per second.

For a spacecraft arriving from interplanetary cruise via lunar-gravity-
assist with residual velocity-infinity of 3 kilometres per second,
captured into a high-elliptical Earth orbit with apoapsis near the
destination altitude, the additional spiral delta-velocity from
apoapsis-circular to the final circular destination is approximately
the same Edelbaum form. Capture from velocity-infinity to high-
elliptical at the destination altitude is approximately impulsive and
costs the hyperbolic-velocity-difference at that altitude.

The key insight: **circular velocity falls with the square-root of
altitude.** At geostationary altitude circular velocity is 3.07
kilometres per second; at low-Earth-orbit altitude it is 7.73 kilometres
per second. The Edelbaum spiral from interplanetary-arrival altitude
*down to* low Earth orbit must pay the full velocity gap; the spiral
*down to* geostationary pays only a small fraction.

Titan's continuous-thrust integration of 24.7 to 40.2 kilometres per
second was anchored on the low-Earth-orbit destination. If the
destination is geostationary the same integrated form yields a much
smaller number.

---

## Constants

- Earth gravitational parameter: 3.986 × 10⁵ cubic kilometres per
  second squared.
- Earth equatorial radius: 6378 kilometres.
- Low Earth orbit, 300-kilometre altitude reference: orbital radius
  6678 kilometres; circular velocity 7.73 kilometres per second.
- Medium Earth orbit, 8000-kilometre altitude reference: orbital
  radius 14378 kilometres; circular velocity 5.27 kilometres per
  second.
- Geosynchronous orbit, 35786-kilometre altitude: orbital radius
  42164 kilometres; circular velocity 3.07 kilometres per second.
- Lunar distant retrograde orbit reference: approximate orbital radius
  450,000 kilometres from Earth; circular velocity (Earth-centred,
  approximate) 0.94 kilometres per second.
- Residual velocity-infinity after lunar-gravity-assist tour: 3
  kilometres per second (per matrix convention).
- Outbound chunk-fed inbound delta-velocity components shared across
  destinations: Saturn-departure 1.5 + cruise braking 2.0 = 3.5
  kilometres per second. The destination-dependent components are
  capture and final spiral.

## Pre-registered hypotheses (comparative ranges only, per the methodology lesson)

### H-altitude-a (continuous-thrust delta-velocity scales with destination)

**Prediction:** integrated continuous-thrust inbound delta-velocity to a
geostationary destination is at least three times smaller than to a
low-Earth-orbit destination, for the same Saturn-departure case. At
geostationary, total chunk-fed inbound delta-velocity is in the range
4.5 to 7.5 kilometres per second; at low Earth orbit it is in the range
20 to 30 kilometres per second.

### H-altitude-b (geostationary delivery delivered fraction)

**Prediction:** at 50-tonne chunk, specific impulse 2000 seconds,
geostationary delivery delivers in the range 50 to 70 percent of chunk
mass (versus 28 percent at low Earth orbit per the previous round).
Lower bound of geostationary holds Architecture A's framework with no
cislunar tug; upper bound matches Architecture B with the cislunar tug
removed.

### H-altitude-c (geostationary vs Architecture B)

**Prediction:** geostationary delivery within Architecture A's
framework delivers within 10 percentage points of Architecture B's
68.2-percent delivered fraction (water-microwave-electrothermal-thruster
cislunar tug case). If the prediction holds, the geostationary-
destination choice is comparable to Architecture B on delivered
fraction *without* introducing the 50-tonne cislunar water-shuttle
that Architecture B requires. Falsified if geostationary delivery is
materially worse (below 55 percent) or materially better (above 80
percent).

### H-altitude-d (matrix-internal consistency)

**Prediction:** the matrix's impulsive-equivalent delta-velocity of 6.42
kilometres per second (which the matrix's surviving 500-kilowatt-
electric Variant B cell uses) actually maps to a destination *above*
low Earth orbit. Specifically: 6.42 kilometres per second is consistent
with capture-to-geostationary plus modest trim. If held, **the matrix's
6.42 number is not "an impulsive-equivalent approximation of the
continuous-thrust 24.7"; it is a different operating point
altogether**, namely geostationary delivery. Falsified if the 6.42
number lines up arithmetically with the low-Earth-orbit destination
under any reasonable assumption.

### H-altitude-e (steelman: there are reasons not to deliver to geostationary)

**Prediction:** the largest currently-anchored demand for in-space water
is at low Earth orbit (per `ICEBERG-demand.md`: crewed stations,
operator-internal cislunar tug fleet). Geostationary demand is
predominantly satellite-servicing propellant which is inferred or
speculative. So even if the engineering closes at geostationary, the
business case at geostationary alone is materially weaker than at low
Earth orbit. Held if geostationary anchored demand is less than 20
percent of low-Earth-orbit anchored demand at base case in 2040.

**Note:** H-altitude-e is the demand-side question. It does not block
H-altitude-a through d as engineering findings; it qualifies how the
finding flows back to the architecture decision.

---

## What this round does NOT decide

- Does not propose changes to L0-02. The text already admits the range
  of altitudes; this round tests whether moving to the upper end
  changes the architecture-cell economics.
- Does not commit to geostationary as the delivery destination. The
  trade between geostationary-delivery (engineering-easier, demand-
  weaker) and low-Earth-orbit-delivery (engineering-harder, demand-
  stronger) is a Saturn-and-project-owner decision.
- Does not investigate the geostationary-to-low-Earth-orbit transfer
  cost on the customer side. That is the customer's problem per
  L0-02's framing, but it does affect pricing.

---

## Result

Run output in `results/results.json` and `results/tables.md`. Base case,
50-tonne chunk, specific impulse 2000 seconds, residual velocity-
infinity 3 kilometres per second after lunar-gravity-assist tour, with
impulsive capture into a captured elliptical orbit (eccentricity 0.33)
plus continuous-thrust Edelbaum circularisation:

| Destination | total chunk-fed delta-velocity (km/s) | delivered (tonnes) | delivered fraction |
|---|---:|---:|---:|
| Low Earth orbit (300 km) | 7.10 | 34.8 | 69.6% |
| Medium Earth orbit (8000 km) | 6.26 | 36.3 | 72.7% |
| Medium Earth orbit (20000 km) | 5.88 | 37.1 | 74.1% |
| Geostationary (35786 km) | 5.71 | 37.4 | 74.8% |

The destination scaling under this accounting is much smaller than I
predicted. Geostationary saves 1.39 kilometres per second relative to
low Earth orbit (a 19.6 percent reduction), translating to 5.2
percentage points more delivered fraction.

### Hypothesis grading

| Hypothesis | Prediction | Computed | Verdict |
|---|---|---|---|
| H-altitude-a | geostationary delta-velocity ≥ 3× smaller than low Earth orbit | 1.24× smaller | **falsified** |
| H-altitude-a | geostationary total chunk-fed delta-velocity 4.5–7.5 km/s | 5.71 km/s | **held** |
| H-altitude-a | low Earth orbit total chunk-fed delta-velocity 20–30 km/s | 7.10 km/s | **falsified — far lower** |
| H-altitude-b | geostationary delivered fraction 50–70% | 74.8% | **falsified high** |
| H-altitude-c | geostationary within 10 percentage points of Architecture B's 68.2% | 74.8% (+6.6 ppt) | **held** |
| H-altitude-d | matrix's 6.42 km/s maps to geostationary-like destination | matrix 6.42 km/s maps cleanly to low Earth orbit under chemical-trim accounting (computed 7.10 km/s); not geostationary | **falsified** |
| H-altitude-e | geostationary anchored demand < 20% of low-Earth-orbit anchored demand | per `ICEBERG-demand.md`: geostationary servicing 5–15 tonnes per year inferred, low-Earth-orbit 30–45 tonnes per year anchored → geostationary at 33% of low-Earth-orbit at base case | **falsified on the 20-percent threshold but held in direction** |

Four falsifications. This is the round telling me my mental model was
wrong.

---

## Reading

This round's *measured* result — that destination altitude under
chemical-trim-at-Earth accounting changes delivered fraction by only 5
percentage points — is uninteresting on its own.

The *real* finding sits one level up: **R-delivery-architecture (the
previous round, commit `e2fc68e`) compared Architecture A under
titan's pure-continuous-thrust integrated delta-velocity (24.7
kilometres per second) against Architecture B under impulsive-
equivalent-with-lunar-flyby-trim (4 kilometres per second). The two
sides of that comparison used different propulsive-regime assumptions
about the Earth-arrival burn. That comparison was apples-to-oranges.**

Under consistent accounting — chemical-trim-at-Earth-with-lunar-
gravity-assist, which is what the matrix's surviving Variant B cell
actually uses — Architecture A delivers 34.8 tonnes of a 50-tonne
chunk to low Earth orbit, identical (within 0.7 tonne) to
Architecture B's 34.1 tonnes. **Architecture B's 2.4× advantage from
R-delivery-architecture disappears under consistent accounting.**

Two things follow from this:

1. **The matrix's Variant B cell delta-velocity budget is consistent.**
   The matrix's 6.42 kilometres per second impulsive-equivalent matches
   my low-Earth-orbit chemical-trim computation of 7.10 kilometres per
   second to within 10 percent. The matrix has not been silently using
   titan's continuous-thrust number for Variant B; it has been using
   the chemical-trim number all along.

2. **Titan's continuous-thrust integrated delta-velocity of 24.7
   kilometres per second applies to all-electric Earth approach
   *without* chemical-trim and *without* lunar-gravity-assist credit.**
   That is the all-electric end-to-end scenario, which rhea's three
   prior rounds already established is structurally falsified. So
   titan's number does the work of *killing the all-electric cell* and
   does *not* do the work of *killing the Variant B cell*. The two
   accounting regimes are distinct and apply to distinct
   architectures.

3. **R-delivery-architecture's headline finding overstated
   Architecture B's value.** The 2.4× number is real for an
   all-electric-end-to-end mission that does not exist (and was killed
   by rhea's prior rounds). For the matrix's surviving Variant B
   architecture, Architecture B and A deliver approximately the same
   fraction to low Earth orbit. Architecture B's value over A is small
   under consistent accounting and may be outweighed by the cost of
   introducing a 50-tonne cislunar water-shuttle.

This is a real correction. The previous round's conclusion needs to be
amended.

---

## Revisit

Round 2 in this session, four falsifications. The pattern is the same
as previous rhea rounds: numeric ranges pre-registered without enough
back-of-envelope checking falsify in either direction. But this round's
falsifications point at something specific — **the previous round
(R-delivery-architecture) compared two architectures under different
delta-velocity accounting regimes**, and the apparent 2.4× advantage of
Architecture B was an artifact of that inconsistency.

Recording the methodology lesson, fourth occurrence: **before
comparing two architectures, verify that the delta-velocity accounting
regime is identical on both sides of the comparison.** This is a
stronger version of "pre-register numeric ranges only after back-of-
envelope arithmetic" — it requires arithmetic *consistency* across
arms, not just within each arm.

The previous round (`water-prop/rounds/R_delivery_architecture/`)
remains in the repository as a committed audit-trail artefact. Its
hypothesis-grading is honest (it pre-registered the assumptions that
turn out to be inconsistent); its Reading section needs amendment.
Documenting that the previous round's Architecture-A column should be
re-run under chemical-trim accounting before the comparison flows back
to the matrix. The two rounds together remain useful — the previous
round established the parametric envelope; this round established that
the headline comparison was overstated.

---

## Cross-learning

**Backward:** R-delivery-architecture's 2.4× Architecture-B-over-A
headline needs correction. Under consistent chemical-trim-at-Earth
accounting, B and A are approximately tied at the 34-tonne-per-50-
tonne-chunk operating point. Architecture B's actual value is *not*
delivered-fraction; it is *operational decoupling* (deep-space vehicle
doesn't need to operate at low Earth orbit) and *avoidance of low-
Earth-orbit Edelbaum spiral if you reject chemical-trim at Earth*.

**Forward:** R-chemical-trim-vs-all-electric-earth-arrival is a real
round candidate. Specifically: is the matrix's Variant B cell allowed
to use a chemical-trim burn at Earth capture? The pitch describes the
inbound as "low-thrust trim to low Earth orbit" (chunk-fed water-
microwave-electrothermal-thruster, no chemical). If Variant B is pure-
electric Earth arrival, titan's continuous-thrust integrated delta-
velocity 24.7 kilometres per second applies and Variant B falsifies.
If Variant B admits chemical trim at Earth, the matrix's 6.42 km/s
number stands and Variant B closes. **The matrix's surviving cell is
contingent on a propulsion choice the matrix has not made explicit.**

**Forward:** R-delivery-destination-altitude (this round) extends to a
geostationary-versus-low-Earth-orbit comparison under *consistent*
accounting. The 5-percentage-point delivered-fraction win for
geostationary is not zero and is paid for at delivery-orbit choice
rather than at architecture choice. Worth recording as an operational
preference; not load-bearing.

**Methodology:** before comparing two architectures, verify accounting
consistency across arms.

**Honest assessment of two-round session:** R-delivery-architecture
overstated a result; R-delivery-destination-altitude corrected it.
The session produced one real finding (the matrix's Variant B
delta-velocity budget is internally consistent; titan's number applies
to all-electric not Variant B; the chemical-trim-at-Earth question is
the next round to run) and one mis-stated finding (R-delivery-
architecture's 2.4× advantage). Net contribution is one new sub-
question for the matrix and one methodology lesson recorded a fourth
time. **Not what I hoped for going in. Recording honestly.**
