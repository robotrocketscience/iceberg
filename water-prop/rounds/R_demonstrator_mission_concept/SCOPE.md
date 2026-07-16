# R-demonstrator-mission-concept — what does the demonstrator retire?

**Status:** scope, pre-study. Authored by Saturn (worker), 2026-05-21.

## Premise

The 2026-05-21 assumption audit reduced the matrix verdict from "ICEBERG closes (with caveats)" to a structured claim: closure is gated by three engineering bets, each independently testable. The corresponding question for the demonstrator class (per REQUIREMENTS.md §7.5) is: what's the smallest mission that retires all three bets?

Section 7.5 defines demonstrator-class as "first mission, or first 1-2 missions. Retire technical risk on the harvest, return, and delivery loop. Prove the architecture works at any scale. L0-04 mass floor relaxed to any non-zero mass delivered. L0-05, L0-06, L0-07, L0-08, L0-09 do not apply." So the demonstrator is licensed to be small.

## The three engineering bets the demonstrator must retire

### Bet 1 — Active chunk capture at scale (A14)

**Claim:** ICEBERG can actively capture a multi-tonne Saturn-ring particle with >= 70 percent joint success probability across rendezvous, deployment, catch, containment, and structural survival.

**Why it's a bet:** the framework's 85 percent capture-efficiency anchor has no engineering decomposition and no flight precedent. Bottoms-up gives ~46 percent. Below 50 percent, the matrix collapses at the L0-04 provisional 25-tonne floor (audit finding A14, locked 31a13abb).

**What retires it:** an active-chunk-capture experiment. Two reasonable demonstrator scopes:
- (a) **Earth-orbit proxy.** Deploy a target mass (10 tonnes of structural mass, possibly inflatable, or a co-launched dummy) and demonstrate the trawl-and-contain mechanism in low-Earth-orbit ahead of the Saturn cruise. This retires the mechanism in cheap-to-iterate conditions.
- (b) **In-situ small-chunk at Saturn.** During or after Saturn arrival, attempt capture of a 1-10 tonne ring particle with full telemetry on success / fragmentation / containment / structural survival.

(b) is more risky and more informative; (a) is cheaper and lower-fidelity. A two-step plan (a then b) retires the bet incrementally.

### Bet 2 — Continuous water-electrothermal on Saturn-water purity (A1)

**Claim:** Water-microwave-electrothermal thrust delivers >= 700 seconds specific impulse continuously for months on chunk-water purity (~99 percent water, ~0.3 percent silicate inclusions per Cassini).

**Why it's a bet:** ground tests confirm 700-900 seconds in 50-second pulses with distilled water (audit finding A1, locked 650938e3). Momentus Vigoride flew the technology in space but the continuous-months-on-dirty-water profile is unvalidated. Real chunk water has trace contaminants that could erode the resonant cavity over the mission timeline.

**What retires it:** an extended-duration water-electrothermal flight test on water with ICEBERG-relevant contaminants:
- 30+ days of continuous operation
- Specific-impulse telemetry throughout
- Post-test inspection of resonant cavity erosion (could be conducted at Earth return)
- Builds on Momentus Vigoride heritage

This experiment can be co-resident with bet 1's chunk capture: the demonstrator's chunk-fed propulsion IS the test article.

### Bet 3 — Kilopower-class reactor program delivers (L0-24)

**Claim:** A flight-qualified ~30 kilowatt-electric fission reactor is on contract by the demonstrator's launch window.

**Why it's a bet:** locked findings 2 and 3: 0-of-6 US space-fission programs since 1965 reached orbit on schedule; NASA Fission Surface Power Phase 2 not yet awarded as of May 2026. L0-24 hard-conditions commercial-class commitment on a flight reactor being on contract; demonstrator-class is exempt per REQUIREMENTS §7.5.

**What retires it:** the demonstrator can pre-empt this bet two ways:
- (a) **Fly without nuclear.** Demonstrator uses solar power (small mission) or radioisotope thermoelectric generators. Validates the chunk-capture + water-electrothermal architecture without requiring nuclear. Disadvantage: solar at Saturn is 1 percent of Earth, so the demonstrator would have to operate at very low power outbound or use a hybrid solar (inner-system) + radioisotope thermoelectric (Saturn) power stack.
- (b) **Fly the reactor.** Bundle a Kilopower-class fission demonstration into the same mission. Higher cost, retires more risk, but tightly couples to Fission Surface Power Phase 2 award timing.

(a) is the recommended path: demonstrator de-risks bets 1 and 2 without requiring a reactor. Bet 3 is retired in a separate mission (or by NASA's Fission Surface Power program) before commercial-class commitment.

## Proposed demonstrator architecture

Following the audit's best-architecture report (vehicle 50 tonnes, single Falcon Heavy expended or Starship, low-thrust spiral outbound, chunk-fed spiral departure, direct propulsive or hybrid aerocapture return) but scaled down for demonstrator class:

| Element | Demonstrator-class value | Commercial-class value (for context) |
|---|---:|---:|
| Vehicle dry mass | 4-6 tonnes | 10-15 tonnes |
| Launch manifest at low-Earth orbit | 15-30 tonnes (one Falcon Heavy partial reuse) | 50 tonnes (single Falcon Heavy expended) |
| Target chunk mass at Saturn | 5-10 tonnes (proves capture at scale) | 200 tonnes |
| Delivered mass at low-Earth orbit | 1-3 tonnes (any non-zero per §7.5) | 25+ tonnes (L0-04) |
| Round-trip time | 12-15 years (L0-05 strict relaxed for demonstrator but worth honoring as proof) | 12 years (per best-architecture report) |
| Power source | Radioisotope thermoelectric (~1-3 kilowatts) or solar-thermal inner-system + radioisotope at Saturn | Kilopower-class 30 kilowatts-electric (subject to bet 3 retirement) |
| Propulsion | Water-electrothermal (this IS bet 2's experiment) | Same |
| Chunk capture | Single-pass trawl with full telemetry (this IS bet 1's experiment) | Same |

## Open questions

1. **Solar vs radioisotope-thermoelectric for the demonstrator.** Radioisotope-thermoelectric flight heritage is strong (Cassini, Mars rovers, etc.) but mass-inefficient. Solar at Saturn is impossible at meaningful power, but a hybrid (large solar array inner-system + small radioisotope-thermoelectric outer-system) could work. Captured in `R_solar_thermal_hybrid_power/SCOPE.md`.

2. **Earth-orbit dress rehearsal of chunk capture (bet 1 step a) — cost effective?** A pre-cruise low-Earth-orbit chunk-capture experiment retires the mechanism cheaply but adds mission complexity. Trade study needed.

3. **Demonstrator launch window.** Earth-Saturn synodic period is 378 days; demonstrator launch window is annual. Demonstrator targeting Saturn arrival in the 2032-2035 window per locked finding 2 means launch in ~2026-2029. Tight against Fission Surface Power Phase 2 award timing if going the "fly with reactor" path.

4. **Cost / budget.** Demonstrator-class missions in this class historically run $500M-$1.5B (Cassini was $3.26B all-in but included Huygens probe; OSIRIS-REx $1B; Hayabusa-2 $150M-$300M). ICEBERG demonstrator would land in this range; iapetus R7 four-tranche staged-options structure already prices this.

## Deliverables of THIS round

1. This SCOPE document (you're reading it).
2. A demonstrator concept-of-operations sketch matching the three bets.
3. Risk-retirement priority order: capture-mechanism (Earth-orbit proxy) first, then continuous water-electrothermal in deep space, then reactor in a separate mission once Fission Surface Power Phase 2 lands.
4. Cost-class estimate compared to iapetus staged-options framework.

## Out of scope

- Detailed bus design (defer to follow-on rounds).
- Customer-acceptance protocols for demonstrator water (per L0-04 demonstrator-class waiver: "any non-zero mass delivered" — no customer needed).
- Lunar-orbit-processing sub-mission (Phase 7 is commercial-class; demonstrator delivers small enough chunk to fit aerocapture or direct propulsive directly).

## Predecessor work

- Locked beliefs: `31a13abb` (A14 capture efficiency), `c646b3c6` (A4 water content confirmed), `650938e3` (A1 plausible-provisional), `c9562697` (L0-04 = 25 t provisional), `5535179f` (three engineering bets framing).
- REQUIREMENTS.md v0.13 (L0-04 set; L0-24 commercial-class gate on reactor contract; §7.5 mission classes).
- `water-prop/rounds/R_assumption_audit_2026_05_21/FINDINGS.md`.
- `water-prop/rounds/R_assumption_audit_2026_05_21/BEST_ARCHITECTURES_25T.md` — the architecture pattern the demonstrator should scale down.
- `water-prop/sims/mission_graph/` framework — used to size the demonstrator architecture against the L0-04 demonstrator-class waiver.

## Priority

**HIGH.** This is the artifact a technical reviewer would actually engage with. It names the bets the project is making, proposes how to retire them, and grounds the cost / schedule story in the iapetus staged-options framework.
