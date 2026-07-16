# R-chemical-electric-leapfrog — closure verdict

**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`)
**Date:** 2026-05-19
**Predecessors:** R-bus-mass-anchor-adjudication (`7b6a492` + `acdbdc1`); R-kilowatt-class-power-envelope (`5162735` + `10b77b7`)
**Trigger:** project-owner architectural proposal — continuous reactor power split between electric thrust and water electrolysis, periodic impulsive chemical burns at Saturn periapsis.

---

## Headline

**ICEBERG inbound delivery closes at flyable reactor power under the chemical-electric leapfrog architecture, IF AND ONLY IF Earth aerocapture closes.** At flyable power (≤ 30 kilowatts-electric, Kilopower-extrapolation):

- 0 cells close L0-05 strict (15-year round-trip) AND L0-09 commercial floor (30 tonnes delivered) under aerocapture-yes.
- 13 cells close L0-05 waiver (25-year round-trip) AND commercial floor under aerocapture-yes.
- 0 cells close commercial-strict under aerocapture-no.

**The binding constraint at flyable power is Earth aerocapture closure, not reactor power class.** Phoebe's 0-of-1920 hybrid-aerocapture-aerobraking verdict (commit `1623cca`) holds the load-bearing physics. R-bus-mass-anchor-adjudication's H5 sub-analysis (this branch, commit `7b6a492`) found phoebe's verdict robust by conjunction: single-axis relaxation of ice tensile strength flips the pass-1 structural leg, but the aerobraking-timescale and sublimation legs remain bound by orders of magnitude. The R-hybrid-aerocapture-joint-axis-sensitivity follow-on round (flagged in the prior round, project-owner direction required) is now the highest-leverage remaining engineering question for the entire program.

---

## Hypothesis verdicts

| H | Predicted | Measured | Verdict |
|---|---|---|---|
| H-lf-1a | anchor (P=15, T=150, aero=yes) round-trip = 13 yr (stockpile everything, no spiral) | 14.6 yr; spiral=1.57 yr | FALSIFIED |
| H-lf-1b | small-tank cell (P=10, T=1, aero=yes) round-trip ~21.9 yr (mostly spiral) | 21.9 yr; spiral=8.90 yr | HELD |
| H-lf-2a | anchor (P=15, T=10, aero=yes) delivered ~35 t, above L0-09 floor | delivered 37.4 t | HELD |
| H-lf-2b | aero=no at flyable power (P<=30): max delivered < 30 t | max delivered (aero=no, P<=30) = 6.6 t | HELD |
| H-lf-3 | aero=yes envelope non-empty; aero=no envelope empty at flyable power | aero=yes strict=0 cells, waiver=13 cells; aero=no strict=0, waiver=0 | FALSIFIED |
| H-lf-4 | ICEBERG closes at flyable power (P<=30) under aero=yes; empty under aero=no | flyable+aero=yes: strict=0 waiver=13; flyable+aero=no: strict=0 | HELD |

## Three-paragraph decision frame

**Architecturally.** The chemical-electric leapfrog rescues ICEBERG inbound delivery at flyable reactor power. The R-kilowatt-class-power-envelope round's headline that the architecture is empty at flyable power was an artefact of assuming pure continuous-thrust electric inbound; that round has been corrected (commit `10b77b7`). Under leapfrog, the Saturn-departure delta-velocity is delivered as many small Oberth-efficient periapsis burns rather than a single gravity-loss-laden continuous-thrust spiral. Chemical hydrogen-oxygen at exhaust velocity 4413 metres-per-second is ~4.8× more reactor-energy-efficient per delta-velocity than electric water-Microwave-Electrothermal-Thruster at 2000-second specific impulse. Reactor power can drop from the 240+ kilowatts-electric needed for pure-electric closure to ~15–30 kilowatts-electric for leapfrog closure — a flyable Kilopower-extrapolation rather than Fission Surface Power class.

**Conditionally.** The leapfrog architecture's delivered-mass result is gated entirely on Earth aerocapture closing. Without aerocapture, the chemical Earth-capture burn (3.5 kilometres-per-second on a 62-tonne mid-cruise vehicle) eats 34 tonnes of additional propellant and drops delivered mass below the L0-09 30-tonne commercial floor. Phoebe's 0-of-1920 verdict on hybrid-aerocapture-aerobraking is the binding physics, robust by conjunction across three failure modes (pass-1 chunk shatter, aerobraking timescale, sublimation). Single-axis ice-tensile relaxation flips only one leg.

**Decision-frame.** The program-level question collapses from 'what reactor power class do we need?' to 'does Earth aerocapture close under any defensible joint relaxation of phoebe's three anchors?' If yes, ICEBERG has a flyable cell at ~15–30 kilowatt-electric Kilopower-extrapolation, delivering ~30–42 tonnes per mission in 13–22 years round-trip. If no, the program is empty at any flyable power regardless of propulsion architecture, and the surviving cells reduce to (a) drop-and-go at Saturn (requires L0-04 waiver) or (b) wait for a power class that isn't built. The R-hybrid-aerocapture-joint-axis-sensitivity round is the load-bearing follow-on.

---

## Matrix amendments

1. **Axis 02 (Surviving cell) — un-collapse the kilowatt-class round's collapse.** The prior round's claim that axis 02 collapses to power envelope at flyable power is wrong under leapfrog architecture. Axis 02 splits back into two load-bearing axes: (a) Earth aerocapture closure, (b) propulsion architecture choice (continuous-thrust electric vs chemical-electric leapfrog). The aerocapture axis is the binding one.

2. **New sub-axis: propulsion architecture.** Pure continuous-thrust electric: empty at flyable power. Chemical-electric leapfrog: non-empty at flyable power if aerocapture closes. Matrix should carry both rows.

3. **Axis 11 (Earth-arrival mode) — the binding axis.** Phoebe's 0-of-1920 verdict stands as basis-of-record. R-hybrid-aerocapture-joint-axis-sensitivity is the highest-leverage follow-on.

4. **Phoebe pivot-survey 31/31 DEAD reading — narrow the audit.** Many of phoebe's kill criteria were F6 (reactor program). Under leapfrog architecture at 15–30 kilowatts-electric Kilopower-extrapolation, F6 binarised-FAIL is no longer the correct treatment; the relevant question becomes 'does Kilopower scale to 15–30 kilowatts-electric in the demonstrator window?'. That's a softer constraint than 'does Fission Surface Power Phase 2 deliver 100+ kilowatts-electric'. Pivot-survey re-run under the Kilopower-extrapolation framing might re-classify some candidates from DEAD to WORTH-DEEP-DIVE.

---

## Engineering risks not modelled (each is its own round)

- **Hydrogen leak rate** in pressurised gas tanks across week-class storage cycles. Hydrogen permeates standard tank wall materials; rate at 10-megapascal pressure across a 100-kilogram-class buffer tank may be significant fraction of stored propellant per week. Determines minimum reactor power that keeps electrolysis rate ahead of leak loss.
- **Chemical-engine throat erosion** across N periapsis burns. N may be 100–10,000 depending on cycle time. Conventional chemical engines are not designed for that many starts.
- **Reactor lifetime** at full power across 8+ years of continuous operation. Enceladus-r5 R-reactor-lifetime-vs-burn-time finding: KRUSTY 28-hour heritage is 3-4 orders of magnitude short of multi-year operation. This is orthogonal to the leapfrog architecture and remains binding.
- **Saturn aerocapture for arrival.** Assumed in this round; Saturn atmosphere is thicker than Earth's and Cassini-Huygens demonstrated entry. Independent verification round flagged.
- **Long-term cryogenic storage of liquid hydrogen / liquid oxygen.** Modelled as 30% mass-fraction pressurised gas storage; cryogenic at large tank sizes (T_tank ≥ 50 tonnes) has much worse mass and boiloff penalties.
- **Electrolyser longevity, plant balance-of-system, water-purity requirements.** All assumed nominal; each is a real engineering programme.

---

## Audit / cross-check

Hand-verifying anchor cell (P = 15 kilowatts-electric, T_tank = 10 t, aerocapture-yes):
- Reactor mass: 15,000 / 2.4 / 1000 = 6.25 t.
- Dry mass: 5.5 (bus) + 10 (bag) + 6.25 (reactor) + 0.15 (thrusters) + 1.0 (chemical engine) + 1.0 (electrolyser) + 3.0 (tank) = 26.90 t.
- Saturn departure propellant: 220 × (1 − exp(−5500/4413)) = 161.7 t.
- Outbound + Saturn-side stockpile: min(10, 7 × 1.76 × 15) = min(10, 184.8) = 10.0 t (tank-limited).
- Spiral electrolysis: (161.7 − 10.0) / (1.76 × 15) = 5.72 years.
- Round-trip: 6 + 1 + 5.72 + 6 = 18.7 years.
- Delivered: 220 × exp(−5500/4413) − 1 (trim) − 26.9 (dry) = 37.4 t.

---

## Critical follow-ons (project-owner direction required)

- **R-hybrid-aerocapture-joint-axis-sensitivity** (highest priority). Joint relaxation across {ice tensile strength, boundary-layer-blocking-factor, atmosphere density} at credible-upper-bounds. Determines whether phoebe's 0-of-1920 is robust under the most-generous-credible-anchor reading. The leapfrog architecture's viability depends entirely on this round's verdict.
- **R-leapfrog-tank-physics** (engineering). Hydrogen leak rate vs storage time at relevant pressures; chemical-engine restart life across N cycles; electrolyser balance-of-system mass and lifetime. Each could move the closing envelope by 1-2× in either direction.
- **R-pivot-survey-rerun-at-Kilopower-anchor** (lower priority). Re-test phoebe's 7 F6-conditional candidates under the softer 'Kilopower scales to 15-30 kilowatts-electric' constraint rather than the binarised 'Fission Surface Power Phase 2 delivers'.
