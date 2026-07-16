# R-chemical-trim-vs-all-electric-earth-arrival — what propulsion does the matrix's surviving cell actually require?

**Author:** rhea (worker session, re-spawn)
**Status:** pre-registered.
**Branch:** `iceberg-rhea-2`.
**Date:** 2026-05-15 (late).
**Protocol:** per `water-prop/PROTOCOL.md`.
**Predecessors this session:** R-delivery-architecture (commit `e2fc68e`), R-delivery-destination-altitude (commit `c3ec48f`).

---

## Motivation

R-delivery-destination-altitude (the prior round) closed by naming this
round as the next move. STATE.md framed the question crisply:

> The matrix's surviving Variant B cell is contingent on a propulsion
> choice the matrix has not made explicit: does Variant B's electric
> Earth-arrival admit a chemical-trim burn at Earth capture, or is it
> pure-electric end-to-end?
>
> - If chemical-trim is admitted, the matrix's 6.42 km/s impulsive-
>   equivalent is the right number, the surviving cell closes under
>   consistent accounting, and delivered fraction is ~70 percent at
>   Kilopower-class power.
> - If pure-electric is required, titan's 24.7–40.2 km/s integrated
>   continuous-thrust applies and Variant B falsifies along with the
>   all-electric cell that rhea's prior three rounds already killed.

What the matrix (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`)
actually says for the surviving cell:

> **500-kWe chemical-kick + electric-inbound** (year 0–15, formerly
> "Variant B"). 500 kWe reactor (under MARVL-anchored mass), chunk-fed
> chemical Saturn-departure, electric inbound, ≤ 200 t chunk.

Literal reading: **electric inbound**. That is, post-Saturn-departure
all propulsion is electric continuous-thrust. Under titan's correction
this implies the inbound integrated delta-velocity is 24.7–40.2 km/s,
not the matrix's stated 6.42 km/s.

The matrix's 6.42 km/s figure is therefore one of three things:

1. **Wrong** — titan's number applies and the matrix has a silent
   accounting inconsistency.
2. **Implicit chemical-trim** — the matrix silently assumes a chemical
   Earth-capture burn, contradicting its own "electric inbound" cell
   label.
3. **Mixed regime** — the matrix admits chemical for impulsive capture
   only, with electric for everything continuous (cruise braking,
   final circularisation).

This round arithmetises all three and asks which one closes L0-05.

## Delta-velocity decomposition (per titan, high-elliptical Saturn-departure case)

From titan's `R_inbound_dv_continuous_thrust/STUDY.md`. The inbound
integrated delta-velocity decomposes into five segments. Numbers are
the matrix's high-elliptical case (titan's middle column):

| Segment | Delta-velocity (km/s) | Continuous-thrust amenable? |
|---|---:|---|
| (1) Saturn-departure (high-elliptical departure orbit) | 3.0 (matrix Variant B chemical-kick; titan computed 3.3 electric or 2.0 impulsive) | Currently chemical in matrix |
| (2) Heliocentric Saturn-to-Hohmann-aphelion decel | 5.44 | Yes (cruise phase, 6 yr available) |
| (3) Ballistic Hohmann cruise | 0 (time only) | N/A |
| (4) Heliocentric Earth-side decel (Hohmann-perihelion → Earth orbital speed) | 10.30 minus ≤ 2.0 lunar gravity assist credit = 8.30 | Yes (cruise phase) |
| (5a) Earth capture from velocity-infinity to bound elliptical | 2.42 (impulsive) or part of 7.67 (Edelbaum) | Either; chemical impulsive much more propellant-efficient at this delta-velocity since electric pays integrated cost |
| (5b) Edelbaum circularisation from elliptical to low Earth orbit | 1.18 (small enough that impulsive ≈ integrated) | Either |

**Note on segment (1):** Matrix uses 3.0 km/s chemical at high-
elliptical-departure. Titan separately computed 2.0 km/s impulsive (with
Oberth) or 3.3 km/s integrated continuous-thrust. The matrix's 3.0 km/s
sits between, consistent with a chunk-fed chemical kick from the high-
elliptical orbit. I hold segment (1) at 3.0 km/s chemical across all
scenarios this round, since the matrix's "chemical Saturn-departure" is
not the variable under test.

**Sum, if all of (2)+(4)+(5) is electric continuous-thrust:** 5.44 +
8.30 + 7.67 = **21.41 km/s electric inbound**. (Titan's reported 27.56
for the high-elliptical case is 3.3 km/s segment (1) electric + this
sum; I am subtracting (1) since (1) is chemical in matrix Variant B.)

**Sum, if Earth-capture (5a) is chemical and rest electric:** (2) 5.44
electric + (4) 8.30 electric + (5a) 2.42 chemical + (5b) 1.18 electric
= **14.92 km/s electric + 2.42 km/s chemical**.

**Sum, if all heliocentric is treated as "Hohmann-free" (matrix
impulsive accounting):** (2) + (4) treated as zero (Hohmann is free under
impulsive); (5a) 2.42 chemical + (5b) 1.18 electric or chemical = 3.60
km/s impulsive. Plus segment (1) Saturn-departure 3.0 km/s chemical.
Total propulsive 6.60 km/s, of which 6.60 = 5.42 chemical + 1.18
electric. **Matches the matrix's 6.42 km/s within 3 percent.**

So the matrix's 6.42 km/s is consistent with **chemical-Earth-capture
plus Hohmann-free heliocentric**. That is, scenario (3) above — implicit
chemical-trim — and additionally the matrix is treating the heliocentric
phase as free (which under continuous-thrust electric is wrong: titan
established (2)+(4) costs 13.74 km/s of integrated electric burn).

## What scenarios this round tests

Each scenario starts with a 50-tonne chunk grappled at Saturn, with
segment (1) Saturn-departure 3.0 km/s chemical at specific impulse 450
seconds. Variations are on segments (2), (4), (5a), (5b).

| Scenario | (2) heliocentric Saturn | (4) heliocentric Earth | (5a) Earth capture | (5b) Edelbaum |
|---|---|---|---|---|
| **A — Matrix literal "6.42"** | free (impulsive Hohmann) | free (impulsive Hohmann) | chemical | electric |
| **B — All-electric inbound (matrix-cell-as-written)** | electric integrated | electric integrated | electric integrated (part of 7.67) | electric integrated (part of 7.67) |
| **C — Chemical-trim at Earth-capture only** | electric integrated | electric integrated | chemical impulsive | electric integrated |
| **D — Full chemical Earth-arrival** | electric integrated | electric integrated | chemical impulsive | chemical impulsive |
| **E — Pure chemical inbound (worst case)** | chemical (with 5.44 chemical at high specific impulse) | chemical | chemical | chemical |

E is for bracketing only; the surviving cell would never pay segments
(2) and (4) as chemical because chemical exhaust velocity (4.41 km/s)
is 4.4× worse than electric (19.6 km/s) for delta-velocity costs above
the chemical exhaust-velocity threshold.

## Constants

- Chemical specific impulse: 450 s (hydrolox, chunk-fed).
- Electric specific impulse: 2000 s (matrix default; titan and rhea
  R&D both anchor here).
- Standard gravity: 9.81 m/s² → chemical exhaust velocity 4.41 km/s,
  electric 19.62 km/s.
- Saturn-departure (1): 3.0 km/s chemical.
- Heliocentric Saturn (2): 5.44 km/s.
- Heliocentric Earth (4): 10.30 km/s, minus 2.0 km/s lunar gravity
  assist credit = 8.30 km/s.
- Earth-capture impulsive (5a): 2.42 km/s.
- Earth-Edelbaum impulsive equivalent (5b): 1.18 km/s.
- Earth full Edelbaum spiral (combined 5a+5b electric): 7.67 km/s.
- Chunk size base case: 50 tonnes.

## Pre-registered hypotheses (comparative ranges only, per the methodology lesson)

### H-chem-a (Scenario A reproduces matrix 6.42)

**Prediction:** Scenario A total propulsive delta-velocity is in the
range 6.0 to 7.5 km/s, matching the matrix's stated 6.42 km/s within
20 percent. **Falsified if** scenario A is below 5 km/s (matrix
overstates) or above 8 km/s (matrix understates).

### H-chem-b (Scenario B falsifies under continuous-thrust)

**Prediction:** Scenario B (all-electric inbound, matrix cell as
labelled) delivers less than 15 percent of chunk mass at 50-tonne
chunk, electric specific impulse 2000 s, 500-kWe reactor irrelevant
to the closure question. **Falsified high** if delivered fraction is
above 20 percent (the cell would marginally close under continuous-
thrust). **Held** if delivered fraction is below 15 percent.

### H-chem-c (Scenario C — chemical-capture-only — recovers most of the matrix's claim)

**Prediction:** Scenario C delivered fraction is in the range 25 to 35
percent of chunk mass. Above scenario B (which has no chemical at
Earth) but below scenario A (which has no electric continuous-thrust
heliocentric penalty). **Falsified high** if Scenario C ≥ scenario A
delivered fraction. **Falsified low** if Scenario C ≤ scenario B
delivered fraction.

### H-chem-d (Scenario D — full chemical Earth-arrival — is worse than Scenario C)

**Prediction:** Scenario D delivered fraction is less than Scenario C
by 2 to 5 percentage points. Chemical Edelbaum circularisation (1.18
km/s at 4.41 km/s exhaust) is more propellant-expensive than electric
Edelbaum at 19.62 km/s exhaust. **Held** if Scenario D < Scenario C.
**Falsified** if Scenario D ≥ Scenario C.

### H-chem-e (load-bearing: the matrix's surviving cell's true inbound delta-velocity)

**Prediction:** Under consistent continuous-thrust accounting (which
the matrix has *not* used), the matrix's "500-kWe chemical-kick +
electric-inbound" cell with chemical-trim-at-Earth admitted (Scenario
C) has total chunk-fed propulsive delta-velocity in the range 15 to 18
km/s — roughly 2.5× the matrix's stated 6.42 km/s. The cell still
closes (delivered fraction > 25 percent) but at a substantially worse
operating point than the matrix advertises. **Falsified high** if the
true inbound is below 12 km/s (matrix is right) or above 22 km/s (cell
falsifies even with chemical-trim).

### H-chem-f (steelman: chemical storage problem)

**Prediction:** The chemical propellant for Earth-capture (segment 5a,
2.42 km/s) must be either (a) cryogenic hydrolox stored from Saturn-
departure for the 6+ year inbound cruise, (b) re-electrolysed near
Earth from a portion of the chunk water, or (c) carried-from-Earth at
outbound launch with the 6.9× launch-mass multiplier from R-outbound-
architecture. Held if at least one of (a), (b), (c) has a clear
Technology-Readiness-Level ≥ 5 path within the demonstrator window
2032–2035. **Falsified** if all three require new technology
development. This is a qualitative claim graded against literature.

### H-chem-g (sensitivity: does scenario C close at smaller chunk?)

**Prediction:** Scenario C delivered mass crosses zero between 100-
tonne and 200-tonne chunks (delivered fraction stays roughly constant
because Tsiolkovsky is mass-ratio not mass-difference, so delivered
mass scales with chunk mass). **Held** if delivered fraction at 100 t,
50 t, and 25 t are all within 1 percentage point of each other.
**Falsified** if delivered fraction depends strongly on chunk size.

## Methodology lesson check (per session log)

Pre-registering comparative ranges with arithmetic backing. The
delta-velocity decomposition is taken directly from titan's published
numbers; the chemical/electric Tsiolkovsky split is a textbook
calculation. All hypothesis ranges have at least one number from
back-of-envelope arithmetic *before* writing.

## What this round does NOT decide

- Does not propose changes to the matrix or REQUIREMENTS. The matrix's
  inconsistency, if found, is a Saturn (orchestrator) integration call.
- Does not commit to one scenario as the correct architecture. The
  point is to make the propulsion-choice ambiguity in the matrix
  explicit so Saturn can resolve it.
- Does not address the L0-09 / L0-10 reliability dimensions
  (enceladus's domain).
- Does not address the cryogenic-storage engineering question beyond
  flagging it. Detailed thermal analysis is its own engineering round.

---

## Result

Run output in `results/results.json` and `results/tables.md`. Base
case: 50-tonne chunk, chemical specific impulse 450 seconds (hydrolox,
chunk-fed), electric specific impulse 2000 seconds, lunar-gravity-
assist credit 2.0 km/s.

| Scenario | dv chemical (km/s) | dv electric (km/s) | dv total (km/s) | delivered (t) | delivered fraction |
|---|---:|---:|---:|---:|---:|
| A — matrix literal (impulsive Hohmann + chemical capture) | 5.42 | 1.18 | 6.60 | 13.79 | **27.6%** |
| B — all-electric inbound (matrix cell as labelled) | 3.00 | 21.41 | 24.41 | 8.51 | **17.0%** |
| C — chemical-trim Earth-capture + electric elsewhere | 5.42 | 14.92 | 20.34 | 6.85 | **13.7%** |
| D — full chemical Earth-arrival | 6.60 | 13.74 | 20.34 | 5.57 | **11.1%** |
| E — pure chemical inbound (bracketing only) | 20.34 | 0.00 | 20.34 | 0.50 | **1.0%** |

Delivered fraction is Tsiolkovsky-invariant in chunk mass (confirmed
in `tables.md`: identical to four significant figures at 25, 50, 100,
200-tonne chunks). H-chem-g held.

### Hypothesis grading

| Hypothesis | Prediction | Computed | Verdict |
|---|---|---|---|
| H-chem-a | Scenario A total dv in 6.0–7.5 km/s range matching matrix's 6.42 km/s within 20% | 6.60 km/s (+2.8% vs matrix) | **held** |
| H-chem-b | Scenario B delivered fraction < 15% | 17.0% | **falsified high** (marginal — 17% is above the 15% threshold but the qualitative picture, "cell does not deliver the matrix's claimed fraction", holds) |
| H-chem-c | Scenario C delivered fraction 25–35%, above B, below A | 13.7%, **below** B (17.0%) | **falsified low and direction-wrong** |
| H-chem-d | Scenario D < Scenario C by 2 to 5 percentage points | D 11.1% vs C 13.7% (delta 2.6 ppt) | **held** |
| H-chem-e | Scenario C "true inbound" 15–18 km/s, cell still closes (delivered fraction > 25%) | inbound 17.34 km/s (held on the dv); delivered 13.7% (cell does NOT close at 25%) | **mixed: held on dv, falsified on closure** |
| H-chem-f | At least one of (a) cryogenic storage, (b) re-electrolyse-at-Earth, (c) carried-from-Earth has TRL ≥ 5 path | Qualitative, see Reading | **partial — carried-from-Earth is TRL 9 but incurs R-outbound penalty; cryogenic multi-year storage is TRL 3–4; re-electrolyse-at-Earth is TRL 2** |
| H-chem-g | Delivered fraction Tsiolkovsky-invariant in chunk mass | Identical across 25/50/100/200 t | **held** |

Three falsifications, three holds, one partial-mixed. The **direction
of H-chem-c was wrong**: I expected chemical-trim to *recover* mass
that all-electric inbound was losing. The arithmetic says the opposite.

---

## Reading

The result that matters and that I did not predict:

**Adding a chemical-trim burn at Earth-capture makes the matrix's
surviving cell deliver LESS, not more, than pure-electric inbound
under continuous-thrust accounting.**

Why. Electric exhaust velocity at specific impulse 2000 seconds is
19.62 km/s. Chemical exhaust velocity at specific impulse 450 seconds
is 4.41 km/s — 4.45× lower. Tsiolkovsky propellant penalty per unit
delta-velocity is proportional to one-over-exhaust-velocity. So
replacing 6.49 km/s of electric inbound burn (the full Earth-side
Edelbaum capture spiral 7.67 km/s minus the small final spiral 1.18
km/s) with 2.42 km/s of chemical-impulsive Earth-capture:

- Mass-ratio for the electric burn it replaces: exp(6.49 / 19.62) =
  1.391
- Mass-ratio for the chemical burn that replaces it: exp(2.42 / 4.41)
  = 1.731

**The chemical burn is more propellant-expensive than the electric
burn it replaces, even though its delta-velocity is 2.7× smaller.**
The chemical-trim intuition is wrong for any burn segment small enough
that electric continuous-thrust integrated delta-velocity is below
(chemical_exhaust_velocity) × (chemical_burn_delta_velocity) /
(electric_exhaust_velocity_minus_chemical_exhaust_velocity). At this
configuration, that crossover is at ~3.8 km/s of integrated electric
delta-velocity. Earth-side Edelbaum at 7.67 km/s is well above the
crossover, so chemical loses.

**Implications for the matrix:**

1. **The matrix's 6.42 km/s figure (Scenario A at 6.60 km/s, 27.6%
   delivered) is reproduced only by treating segments (2) and (4)
   heliocentric as Hohmann-free.** Under impulsive accounting that is
   conventional: a Hohmann transfer is the natural cruise trajectory
   and consumes no propellant once placed on it. Under continuous-
   thrust electric, segments (2) and (4) require 13.74 km/s of
   integrated burn (5.44 + 8.30 with lunar-gravity-assist credit).
   That cost is real and the matrix's accounting elides it.

2. **The matrix's cell label "500-kWe chemical-kick + electric-inbound"
   is structurally inconsistent with the matrix's 6.42 km/s figure.**
   Either the cell is impulsive Earth-arrival (in which case the
   propulsion is chemical at Earth, not electric, and the label is
   wrong), or the cell is electric inbound and the 6.42 km/s figure
   is wrong by 3.8× (titan's continuous-thrust ratio).

3. **Best continuous-thrust scenario for the matrix's surviving cell
   is Scenario B (all-electric inbound) at 17.0% delivered fraction
   — 38% degradation from the matrix's 27.6% Scenario A claim.** At
   200-tonne chunk this delivers 34.0 tonnes of water versus the
   matrix's 55.2-tonne claim under Scenario A accounting. The surviving
   cell still has positive delivered mass; the cell does not falsify.
   It is materially worse than the matrix advertises.

4. **Chemical-trim cannot rescue the cell.** Scenarios C and D both
   underperform Scenario B. The matrix's option to "add chemical-trim
   at Earth" *is not an option that improves things*. It is a
   downgrade. The chemical-trim path is only useful if it removes a
   continuous-thrust segment large enough that the crossover threshold
   is crossed — which Earth-side capture (segments 5a+5b at 7.67 km/s
   continuous-thrust integrated, vs 2.42+1.18 = 3.60 km/s chemical-
   impulsive-or-near-impulsive) does not, because electric is more
   propellant-efficient even at the larger delta-velocity.

5. **The cells's true degradation is not 38% from the matrix figure
   but ~50% from the matrix figure if customers expected the matrix's
   Scenario-A-style 27.6% delivered fraction.** Scenario A is what the
   matrix has carried; Scenario B is the physical truth. Saturn needs
   to decide whether the matrix should be amended to either (i) state
   Scenario B as the surviving cell's delivered fraction (17%, with
   honest continuous-thrust accounting), or (ii) re-label the cell as
   "chemical Earth-capture" (Scenario A at 27.6%, but admitting that
   chemical propellant must be either stored cryogenically for 6+
   years or carried from Earth), or (iii) acknowledge that the cell
   does not close at the matrix's stated economics.

### Chemical storage steelman (H-chem-f)

If Saturn chooses (ii) — Scenario A is the operating point — the
chemical propellant problem becomes load-bearing.

- **Cryogenic hydrolox storage for 6+ years:** The chemical must be
  produced at Saturn (chunk-fed electrolysis) and stored for the
  6.1-year inbound cruise plus the 1-year Saturn operations phase.
  Long-duration cryogenic storage of hydrogen at 20 kelvin is **TRL
  3–4** (laboratory and short-duration on-orbit demonstrations
  exist; multi-year storage in deep-space thermal environment has no
  flight heritage). Active cryocoolers add mass and power.
- **Re-electrolyse-at-Earth-approach:** Carry a portion of chunk water
  separately, run electrolysis with reactor power near Earth.
  Requires a parallel electrolysis facility designed for short-burst
  operation; mass model unsolved. **TRL 2** at integrated-vehicle
  level.
- **Carried-from-Earth chemical-trim kit:** Launch a sealed
  storable-hypergolic or hydrolox stage with the outbound vehicle.
  Storable hypergolics (MMH/NTO, MON-3 NTO) at specific impulse 320–
  340 seconds are TRL 9 (decades of flight heritage). Multi-year
  cryogenic hydrolox is TRL 5 only for in-space depots, and the
  R-outbound-architecture 6.9× launch-mass multiplier applies to
  every kilogram of carried chemical. At Scenario A's 35 tonnes of
  chemical propellant burned, the launch-mass cost is 241 tonnes,
  which is more than the matrix's full Variant B vehicle dry mass.

**Honest assessment of the steelman:** The matrix's 27.6%-delivered-
fraction Scenario A operating point requires either a TRL-3-or-below
multi-year cryogenic storage technology, or a TRL-2 in-space
electrolysis-at-Earth-approach, or a carried-from-Earth chemical
penalty that erases more mass than the chemical saves. **None of the
three is currently a feasible engineering path within the demonstrator
window 2032–2035.** Saturn's three options reduce to: accept
Scenario B (17% delivered, electric inbound, honest about continuous-
thrust cost), or develop one of the three chemical-storage paths as a
parallel R&D programme, or retire the cell.

The Scenario A operating point — the one the matrix currently
implicitly assumes — is not free. It is contingent on a chemical-
storage technology programme that the matrix has not surfaced.

---

## Revisit

Round 3 in this session, three more hypothesis falsifications.

**Methodology lesson, fifth occurrence:** Pre-registering numeric
ranges with arithmetic backing is not enough; I also need to verify
*direction-of-effect* against arithmetic before pre-registering.
H-chem-c was wrong in direction — I assumed chemical-trim helps. The
two-minute calculation (Tsiolkovsky mass-ratio comparison) would have
caught the direction-error.

Strengthened lesson: **before pre-registering whether scenario X is
better or worse than scenario Y, compute mass-ratios for both. If the
mass-ratio comparison contradicts the intuition, trust the arithmetic.**

The methodology lesson at this point has been recorded five times
across two sessions of rhea, in increasingly specific forms:

1. Pre-register numeric ranges only after back-of-envelope arithmetic
2. Pre-registered ranges should be comparative, not binary
3. (Repeat of 1+2)
4. Verify delta-velocity accounting regime is identical across arms
   before comparing
5. (This round) Verify direction-of-effect against arithmetic before
   pre-registering "scenario X better than scenario Y" claims

The pattern is: I keep pre-registering hypotheses that arithmetic
would have falsified before the run. The fix at each step is to spend
more time at the back-of-envelope stage. Recording this as itself a
load-bearing finding for the campaign: **pre-registered hypotheses
that survive the run are useful; pre-registered hypotheses that fail
because the arithmetic was already against them are wasted rounds.**
The corrective is in the rhea-personal process, not in the project's
data.

---

## Cross-learning

**Backward — closes the chain from R-delivery-architecture (commit `e2fc68e`) and R-delivery-destination-altitude (commit `c3ec48f`):**

R-delivery-architecture compared two architectures under inconsistent
accounting. R-delivery-destination-altitude established that under
chemical-trim-at-Earth accounting (impulsive Hohmann), the two
architectures are tied. This round establishes that **chemical-trim-
at-Earth accounting is itself the matrix's implicit assumption** —
specifically the Hohmann-free part of segments (2) and (4) — and that
**this implicit assumption is not free under continuous-thrust electric
propulsion**. The two prior rounds asked the right question (which
architecture?) but at the wrong level. The actual leverage is one
level up: **does the matrix admit continuous-thrust accounting for
the heliocentric phase, or does it stay impulsive?**

**Forward — matrix-amendment options for Saturn:**

The matrix's "500-kWe chemical-kick + electric-inbound" cell, as
currently labelled and quantified, is internally inconsistent. Three
amendment paths Saturn can pick from:

| Path | Cell label | Stated dv | Delivered fraction at 50 t | Honest accounting? |
|---|---|---|---|---|
| Amendment A | "500-kWe all-electric inbound" | 21.41 km/s electric + 3.0 chemical Saturn-departure | 17.0% | yes (continuous-thrust) |
| Amendment B | "500-kWe chemical Earth-capture + electric heliocentric" | 5.42 chemical + 1.18 electric (matrix-current 6.42) | 27.6% but contingent on TRL-3-or-below cryogenic storage tech | partial (chemical is impulsive but heliocentric still electric) |
| Amendment C | "Cell retired" | n/a | n/a | yes |

Amendment A is the most honest engineering reading. Amendment B
preserves the matrix's numbers but adds a TRL-3 propellant-storage
programme as a new explicit dependency. Amendment C retires the only
surviving cell and forces a search for a non-fission baseline or for
the aerocapture-with-chunk-as-heat-shield rescue path.

**Forward — propellant-storage R&D as a load-bearing dependency:**

If Saturn chooses Amendment B, the matrix gains a new top-level
dependency (alongside reactor program risk) on multi-year cryogenic
hydrolox storage or carried-from-Earth chemical with the 6.9×
multiplier. This is its own R&D round candidate:
**R-cryogenic-hydrolox-multi-year-storage** — what is the TRL path to
multi-year deep-space cryogenic hydrolox storage, and is it in scope
for the demonstrator window?

**Forward — chunk-as-heat-shield is back on the critical path:**

If the matrix-surviving cell delivers only 17% under honest accounting
(Amendment A), the aerocapture path (R-chunk-as-heat-shield-revisit)
becomes higher leverage than previously rated. Earth-side aerocapture
collapses segments (4) and (5) — 8.30 + 7.67 = 15.97 km/s of electric
continuous-thrust inbound — to aerodynamic dissipation. At ~50%
propellant savings, the cell's delivered fraction could rise back
toward 35-40%, restoring something close to the matrix's claimed
operating point but via a different physical mechanism than chemical-
trim.

**Methodology:** Verify direction-of-effect before pre-registering.

**Honest assessment of this round:** The headline finding is real
and load-bearing. The chemical-trim intuition that the matrix
implicitly relies on (and that I implicitly endorsed in pre-
registration) is *backward* — adding chemical at Earth-capture makes
things worse under continuous-thrust accounting. The matrix's
surviving cell has approximately half the delivered fraction the
matrix advertises, and the path to recovering the matrix's claim
requires propellant-storage technology at TRL 3 or below. Saturn now
has a concrete three-option amendment proposal to choose from.

**Net session contribution (three rounds):** One real finding
(continuous-thrust accounting is the matrix's hidden propulsion-
choice variable, and chemical-trim cannot rescue the cell), one
overstated finding (R-delivery-architecture's 2.4× headline) that
this round and the prior corrected, and one extension finding
(destination-altitude is not load-bearing). Net: the matrix's
surviving cell needs amendment.

