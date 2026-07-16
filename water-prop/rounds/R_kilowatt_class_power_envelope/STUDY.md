# R-kilowatt-class-power-envelope — STUDY

---

## CORRECTION (2026-05-19 same-day follow-on)

The "ICEBERG architecturally empty at flyable power" framing is partially retracted. This round computed pure-continuous-thrust electric inbound, which carries a gravity-loss penalty (25 km/s continuous-thrust Δv anchor). Under a chemical-electric hybrid leapfrog architecture — reactor power split between continuous electric and continuous water electrolysis, with stored hydrolox burned impulsively at Saturn periapsis — the burn-time wall relaxes substantially. With Earth aerocapture closing, delivered mass is ~42 tonnes (above L0-09 floor). The binding constraint at flyable power shifts from reactor power to Earth aerocapture closure (phoebe 0/1920). See `results/closure_verdict.md` CORRECTION block. Follow-on round `R-chemical-electric-leapfrog` runs the architecture properly.

---



**Worker:** titan (re-spawn 3, branch `iceberg-titan-3`, 2026-05-19 latest+12 follow-on).
**Round type:** analytical-bound round. No new physics; closed-form Tsiolkovsky + thrust-power-energy bookkeeping at the project-owner-specified flyable power class.
**Predecessor:** R-bus-mass-anchor-adjudication (this branch), commits `7b6a492` (round) and `acdbdc1` (retraction).

---

## Why this round exists

Project-owner directive 2026-05-19: "A 500 kilowatt reactor is not going to happen. Stop accounting for it, stop talking about it." The four user-locked ICEBERG power findings already say: zero-of-six US space-fission base rate since 1965; NASA Fission Surface Power Phase 2 not awarded; 40 watts-per-kilogram is paper-only at technology-readiness-level 2; megawatt radiator stack is 40–55 percent of system mass.

The entire campaign's matrix has been generating "X cells survive AT 500 kilowatt-electric reactor" headlines that absorb back as if the reactor were credible. The previous round (R-bus-mass-anchor-adjudication) is the most recent instance — its "6 surviving cells at Europa-Clipper-bus" headline presupposed a 500-kilowatt-electric vehicle. The directive retires that pretense.

This round answers the one remaining quantitative question: **at the actually-flyable power envelope (single-digit to low-double-digit kilowatt-electric, Kilopower-heritage), where does the architecture sit on the burn-time wall?** I expect the answer is "off the wall by 1–4 orders of magnitude," but the round computes the bound explicitly so the matrix can carry a numerical reading rather than a project-owner directive.

---

## Flyable power envelope (anchor)

Per user-locked ICEBERG power findings 1 and 2:

| Power source | Specific power (system-level) | Demonstrated scale | Anchor |
|---|---|---|---|
| Radioisotope thermoelectric generator (heritage Cassini/MSL/Mars 2020) | ~5.3 watts-per-kilogram | ~110 watts each, clustered to ~1 kilowatt-electric | flown |
| Kilopower (Kilowatt Reactor Using Stirling Technology, KRUSTY) | 2.4 watts-per-kilogram | 1 kilowatt-electric ground demonstration 2018 | technology-readiness-level 5 (ground) |
| Hypothetical 10-kilowatt-electric scaled Kilopower | 2.4 watts-per-kilogram | not built | technology-readiness-level 3 |
| Solar photovoltaic at Saturn (9.5 AU) | irrelevant — flux 1/90 of Earth-level | < 1 kilowatt-electric per 1000 square metres array | not viable for propulsion |

**Anchor power grid:** `P_reactor ∈ {1, 5, 10}` kilowatt-electric. Specific power `sp ∈ {2.4, 5.3}` watts-per-kilogram (KRUSTY-measured floor, radioisotope-thermoelectric-generator-flown ceiling). No 50-kilowatt-electric point — that was already a half-order-of-magnitude reach above any flown anchor.

---

## Question this round answers

**Q1.** At kilowatt-class power, what is the inbound burn time to dump 25 kilometres-per-second continuous-thrust Δv for a 200-tonne chunk + 5.5-tonne bus + 10-tonne bag vehicle? Compare against the L0-05 strict ceiling (15 years cumulative round-trip, of which 7 years are non-burn outbound + Saturn-side).

**Q2.** Does any specific-impulse choice rescue closure? Higher exhaust velocity reduces propellant mass but raises kinetic energy per kilogram, so energy-cost-per-Δv is approximately invariant; burn time scales as v_e² × (1 - exp(-Δv/v_e)).

**Q3.** Does any chunk-mass choice rescue closure? Smaller chunk reduces total energy linearly but the L0-09 commercial floor (30 tonnes delivered) constrains how small.

**Q4.** Stripping the inbound burn entirely (drop-and-go architecture: deliver chunk to Saturn-system orbit and don't bring anything to Earth) — does ANY power envelope close even one of the existing matrix axes?

---

## Pre-registered hypotheses (central anchor computed BEFORE range)

### H-kw-1: inbound burn time anchor

At P = 10 kilowatt-electric, Isp = 2000 seconds, vehicle wet mass at exit = 215.5 tonnes (200 chunk + 5.5 bus + 10 bag), Δv = 25 kilometres-per-second, thruster efficiency 0.5:

- Exhaust velocity v_e = 2000 × 9.80665 = 19,613 metres-per-second
- Mass ratio m_0/m_f = exp(25,000 / 19,613) = 3.58
- Propellant m_w = m_0 × (1 − 1/3.58) = 215.5 × 0.721 = 155.4 tonnes
- Jet kinetic energy = 0.5 × 155,400 × 19,613² = 2.99 × 10¹³ joules
- Electrical energy = 2.99 × 10¹³ / 0.5 = 5.98 × 10¹³ joules
- Burn time at 10 kilowatt-electric = 5.98 × 10¹³ / 10,000 = 5.98 × 10⁹ seconds = **189.5 years**

**Anchor:** burn time at 10 kilowatt-electric / Isp 2000 / 200-tonne chunk = **190 years**. L0-05 strict allows ≤ 8 years of inbound burn. Margin: **0.04× of budget — short by 24×**.

Predicted range [150, 250] years. Falsified if burn time ≤ 50 years (closure within stretch waiver) or ≥ 500 years (anchor mis-computed).

### H-kw-2: higher specific-impulse does not rescue

At Isp = 5000 seconds, v_e = 49,033 metres-per-second:
- Mass ratio = exp(25,000 / 49,033) = 1.668
- Propellant = 215.5 × 0.4 = 86.2 tonnes
- Jet energy = 0.5 × 86,200 × 49,033² = 1.036 × 10¹⁴ joules (3.5× higher than Isp 2000)
- Burn time at 10 kilowatt-electric = 1.036 × 10¹⁴ / (10,000 × 0.5)... = electrical 2.07 × 10¹⁴ joules → 6,569 years

Wait — at higher Isp the jet energy goes UP (energy scales as v_e², propellant only as 1 − exp(-Δv/v_e)), so burn time gets WORSE.

**Anchor:** Isp 5000 burn time = **6,570 years** at 10 kilowatt-electric (35× worse than Isp 2000). The Isp lever is anti-rescue at fixed Δv.

Predicted: monotonic — higher Isp = longer burn at fixed power. Falsified if anchor cell at Isp 5000 produces burn time < Isp 2000 anchor.

### H-kw-3: smaller chunk does not rescue closure

At chunk = 10 tonnes (smallest commercial-floor-relevant; L0-09 floor is 30 tonnes delivered, so chunk must be ≥ 30 tonnes pre-burn — but 10 tonnes is the demonstrator-class anchor enceladus-r5 grid used):
- m_0 = 10 + 5.5 + 10 = 25.5 tonnes
- m_w at Isp 2000 = 25.5 × 0.721 = 18.4 tonnes
- E_jet = 0.5 × 18,400 × 19,613² = 3.54 × 10¹² joules
- E_elec = 7.07 × 10¹²
- Burn time at 10 kilowatt-electric = 7.07 × 10¹² / 10,000 = **22.4 years**

Still > 8-year inbound budget by 2.8×.

**Anchor:** chunk = 10 tonnes / Isp 2000 / 10 kilowatt-electric burn time = **22 years**. Smaller-chunk lever reduces burn time linearly (since energy scales linearly with propellant mass which scales linearly with m_0 which scales linearly with chunk mass). To close the 8-year budget at 10 kilowatt-electric / Isp 2000, chunk must be ≤ 3.6 tonnes delivered — well below L0-09 commercial floor.

Predicted: NO chunk choice satisfies BOTH L0-05 strict and L0-09 commercial at 10 kilowatt-electric. Falsified if any (chunk ≥ 30 tonnes) cell closes burn time ≤ 8 years.

### H-kw-4: drop-and-go architecture (no inbound burn)

Strip the inbound delivery entirely. Deliver chunk to Saturn-system orbit only. Then the in-space architecture only needs to handle outbound (6 years) + Saturn-side processing (1 year) — no inbound burn. The "delivered fraction" is zero by definition; product becomes "Saturn-system water depot" not "Earth-orbital water delivery."

**Anchor:** under L0-04 (deliver water to Earth orbit, the foundational product requirement), drop-and-go is L0-strict-non-compliant. Under an L0-04 waiver (deliver water to ANY orbital destination, including Saturn-system depot), the architecture closes trivially because the binding leg is removed. Whether that closes a viable program depends on L0-13 (commercial customer demand for Saturn-system water depot), which has zero existing demand model.

Predicted: drop-and-go is the only architecture that closes under kilowatt-class power, AND it requires L0-04 waiver, AND L0-04 waiver requires a non-existent commercial demand framework. Falsified if any cell closes inbound delivery without an L0-04 waiver.

### H-kw-5 (aggregate)

**Under the project-owner directive that 500-kilowatt-electric reactors are out-of-bounds, ICEBERG's actual flyable architecture is empty at the inbound-delivery level by 3–24×.** No combination of chunk mass, specific impulse, or bus mass closes the 8-year inbound-burn budget at 1–10 kilowatt-electric. The only closure that exists is drop-and-go, which requires an L0-04 waiver that has no existing commercial-demand basis.

Predicted: 0 of the architecturally-relevant cells close. Falsified if ≥ 1 cell closes both L0-05 strict (8-year inbound burn) AND L0-09 commercial floor (30 tonnes delivered) at any (P, chunk, Isp) ∈ {1, 5, 10} × {30, 100, 200} × {2000, 5000} kilowatt-electric × tonnes × seconds.

---

## Method

`run.py` computes inbound burn time analytically for the (P, chunk, Isp) grid above, plus margin against the 8-year inbound-burn budget. Closed-form Tsiolkovsky; no integration; no numerical sweep beyond ~36 cells. Reports:

- Burn-time grid with closure flags
- Closing chunk size (if any) per (P, Isp) cell
- Margin distribution: how far off the budget is each cell?
- Drop-and-go cell as a separate readout (L0-04 waiver required)

The round produces `results/burn_time_grid.md` and `results/closure_verdict.md`.

---

## Out-of-scope

- Solar photovoltaic. At Saturn (9.5 astronomical units), solar flux is 1/90 Earth-level. Even a 1000-square-metre array delivers under 1 kilowatt. The directive's "Kilopower-heritage" framing assumes solar is not on the table for this orbital regime.
- Beamed-power architectures. Outside any existing flight-program envelope.
- Multi-vehicle / orbital tug staging (chunk passed between multiple smaller tugs). Folded into the "drop-and-go" cell.
- Project-pivot questions (what L0 requirements would have to change for ICEBERG to close at this power class). Out of scope for the round; raised in the closure verdict for project-owner direction.

---

## What this round does and does not address

**Addresses.** The numerical bound on architecture closure under the project-owner-specified power envelope. The retraction of the prior round's headlines is justified by this round's numbers, not by the directive alone.

**Does not address.** Whether the ICEBERG program can be reframed around the surviving cells (drop-and-go, or a non-water-delivery product). That is project-owner-level work, not a worker round.

The handoff after this round should flag two follow-on questions for project-owner direction: (a) is L0-04 a strict requirement or is "Saturn-system water depot" a valid product, (b) what demand model exists for the surviving cells if any.
