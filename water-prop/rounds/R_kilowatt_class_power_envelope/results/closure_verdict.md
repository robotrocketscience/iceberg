# R-kilowatt-class-power-envelope — closure verdict

---

## CORRECTION (2026-05-19 same-day follow-on)

**The headline "ICEBERG is architecturally empty at flyable power" is too strong and is partially retracted.**

This round computed inbound burn time assuming **pure continuous-thrust electric** at 25 kilometres-per-second Δv. That assumption already builds the gravity-loss penalty into the inbound segment. Under that assumption, 0 of 36 cells close at 1–10 kilowatt-electric, which is the result this round reports correctly.

What the round did NOT consider is **chemical-electric hybrid leapfrog architecture**: reactor power split between continuous electric thrust and continuous water electrolysis; stored hydrolox burned impulsively at Saturn periapsis on each orbit pass; cycle time set by tank capacity rather than mission duration. Under that architecture, the Saturn-departure leg becomes near-impulsive (avoiding the gravity-loss penalty), and the trans-Earth coast Δv drops from "25 kilometre-per-second continuous-thrust" to roughly "5.5 kilometre-per-second impulsive + 0.3 kilometre-per-second electric trim".

The corrected delivered-mass arithmetic, on a 220-tonne vehicle at Saturn departure (200-tonne chunk + 20-tonne dry stack):

| Architecture | Δv allocation | Propellant | Delivered |
|---|---|---|---|
| Hybrid leapfrog with Earth aerocapture | 5.5 km/s chemical + 0.3 km/s electric + 0 km/s aerocapture | 158 t | **42 t** |
| Hybrid leapfrog with chemical Earth capture | 5.5 km/s chemical + 0.3 km/s electric + 3.5 km/s chemical | 192 t | **8 t** |
| Pure continuous-thrust electric at specific impulse 2000 seconds | 25 km/s continuous-thrust | 158 t | **42 t** |

Delivered mass at flyable power is ~42 tonnes (above the L0-09 commercial floor of 30 tonnes) IF Earth aerocapture closes. Without aerocapture, the chemical Earth-capture burn eats the chunk down to 8 tonnes.

**The binding constraint at flyable power is Earth aerocapture, not reactor power.** Phoebe's 0/1920 aerocapture-aerobraking verdict is the load-bearing physics; the structural leg is single-axis flippable to higher ice tensile strength, but the aerobraking-timescale and sublimation legs remain bound by orders of magnitude.

**What this round still says correctly.** Pure continuous-thrust electric inbound at flyable power has a 193-year burn-time wall — that result stands. The architectural conclusion shifts: pure continuous-thrust is not the only propulsion architecture available, and the hybrid leapfrog rescues the burn-time wall (at the cost of needing aerocapture to close).

**Follow-on round.** `R-chemical-electric-leapfrog` (titan-3, same branch) sweeps reactor power, tank capacity, chemical-electric Δv split, and aerocapture-conditional scenario to lay out the closing envelope cleanly.

---

**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`)
**Date:** 2026-05-19
**Predecessor:** R-bus-mass-anchor-adjudication (this branch, commits `7b6a492` + `acdbdc1`)
**Trigger:** project-owner directive 2026-05-19 — 500-kilowatt-electric reactor out-of-bounds.

---

## Headline

At the actually-flyable power envelope (1–10 kilowatt-electric, Kilopower-heritage, specific power 2.4–5.3 watts-per-kilogram), **0 of 36 architecturally-relevant cells close L0-05 strict + L0-09 commercial floor**. 0 cells close under the L0-05 waiver (25-year round-trip), all at chunk masses below the commercial floor.

Anchor cell: 10 kilowatt-electric / Isp 2000 / 200-tonne chunk / Kilopower specific power 2.4 watts-per-kilogram → **inbound burn time 193 years**, which is **24× over the 8-year inbound-burn budget**. Round-trip 200 years total (vs L0-05 strict 15 years).

**Reading.** ICEBERG inbound delivery at the flyable power envelope is unphysical by an order of magnitude on burn time alone. Higher specific impulse makes it worse (energy scales as v_e²). Smaller chunk reduces burn time linearly, but the chunk size that closes the burn-time budget at 10 kilowatt-electric / Isp 2000 / Kilopower-class is below the L0-09 commercial floor by an order of magnitude. The drop-and-go architecture (deliver to Saturn-system orbit only) is the only surviving cell and requires an L0-04 waiver that has no existing commercial-demand model.

---

## Hypothesis verdicts

| H | Predicted | Measured | Verdict |
|---|---|---|---|
| H-kw-1 | burn time at 10 kWe / Isp 2000 / chunk 200 / sp 2.4 ∈ [150, 250] yr | 193.0 yr | HELD |
| H-kw-2 | Isp 5000 burn time > Isp 2000 burn time at same (P, chunk, sp) | Isp 5000 = 669 yr vs Isp 2000 = 193 yr | HELD |
| H-kw-3 | no chunk ≥ 30 t closes L0-05 strict at 10 kWe / Isp 2000 | no chunk closes at any size | HELD |
| H-kw-5 | 0 of 36 cells close L0-05 strict AND L0-09 commercial | 0 of 36 close strict; 0 close waiver | HELD |

---

## What this means for the matrix

1. **Axis 02 (Surviving cell) is now load-bearing on power envelope alone.** Bus mass, aerocapture closure, ring crossing, reactor program — all become second-order. The first-order kill is that ICEBERG cannot deliver chunks to Earth orbit at any flyable power class under continuous-thrust accounting.

2. **Every prior round that headlined 'N cells close at 500 kilowatt-electric' inherits an implicit retraction.** Listed in the handoff. The architecture-decision-matrix top-section needs orchestrator-level revision: every '500 kilowatt-electric' or 'megawatt-electric' surviving-cell row should be marked fantasy under the project-owner directive.

3. **The campaign's pivot-survey 31/31 DEAD reading from phoebe is now unconditional.** F6 (reactor program / specific-power availability) was the most-common kill criterion; the directive moves F6 from probabilistic (posterior 0.07–0.20 per iapetus) to binary FAIL for any cell requiring > ~10 kilowatt-electric. Under that move, even the 7 F6-conditional WORTH-DEEP-DIVE candidates from phoebe's audit collapse to DEAD.

4. **The only surviving cell is drop-and-go architecture** (deliver to Saturn-system orbit, do not bring water to Earth). This requires L0-04 waiver (deliver-to-Earth-orbit is the foundational product requirement). Whether the program can close on Saturn-system water depot revenue is a project-owner question, not a worker round.

---

## Critical follow-ons (project-owner direction required)

- **Is L0-04 (deliver water to Earth orbit) strict, or is Saturn-system water depot a valid product?** This is the program's only surviving architecture under the directive. Without an L0-04 waiver, there is no flyable ICEBERG.
- **Does a commercial cislunar water-tug program (kilowatt-class water-electric MET, ESPA-Grande-class vehicle) become the primary thesis?** That program does close at flyable power and has named customers. ICEBERG's surviving role in this case is as long-tail option attached to the tug roadmap, not as the load-bearing program.
- **The matrix and design-axes documents need orchestrator-level revision.** Multiple prior axes (02 surviving cell, 11 Earth-arrival mode, 13 capital structure, 19 capture architecture) carry 500-kilowatt-electric anchors that the directive retires. This is not a worker-round task.

---

## Audit / cross-check

Hand-verifying H-kw-1 anchor:
- Vehicle wet mass at start of inbound burn: 200 (chunk) + 5.5 (bus) + 10 (bag) + 4.17 (reactor at 2.4 W/kg) + 0.1 (thrusters) = 219.77 t.
- v_e = 2000 × 9.80665 = 19,613 m/s.
- Mass ratio = exp(25,000 / 19,613) = exp(1.2747) = 3.577.
- Propellant = 219.77 × (1 − 1/3.577) = 158.34 t.
- Jet kinetic energy = 0.5 × 158335 kg × 19613² = 3.05e+13 J.
- Electrical energy = 3.05e+13 / 0.5 = 6.09e+13 J.
- Burn time at 10 kilowatt-electric = 6.09e+13 / 10,000 = 6.09e+09 s = 193.0 years.
