# R-mid — Mid-Campaign Assumption Audit

**Purpose:** systematically check every load-bearing assumption in R5-R15b against sources. Identify assumptions that are: (a) sourced and correct, (b) sourced but possibly applied wrong, (c) unsourced placeholder numbers, (d) inherited from prior rounds without independent verification.

---

## 1. Trajectory assumptions

| Quantity | Value used | Source / verification | Status |
|---|---|---|---|
| Outbound Hohmann time-of-flight | 6.09 yr | R9 sun-centered two-body conic, vis-viva | **verified** |
| Saturn dwell | 1.0 yr | Conops baseline | **verified** |
| Inbound Hohmann coast | 6.09 yr | R9 vis-viva (same as outbound) | **verified** |
| Inbound delta-velocity after 10-flyby tour | 4.47 km/s | R12 result from R9 `lunar_flyby` module | **verified by sim** |
| Inbound delta-velocity after 3-flyby tour | 8.87 km/s | R9 result | **verified by sim** |
| Hohmann v_∞ at Earth arrival | 10.30 km/s | R9 vis-viva | **verified** |
| Lunar synodic phasing per flyby | 29.5 days | Lunar synodic period (canonical) | **verified** |
| 10-flyby tour phasing time | 0.73 yr | (10-1) × 29.5 d / 365.25 | **verified** but implicitly assumes lunar resonance availability |
| Round-trip time = outbound + dwell + max(inbound coast, braking) + phasing | by construction | R12 model | **verified** |

**Trajectory model assumption: constant thrust, midpoint mass, no gravity/steering losses.** Documented in R13 STUDY.md. Estimated ±10-20% optimistic on cruise time relative to a real low-thrust optimizer. **Status: ACKNOWLEDGED LIMITATION**.

---

## 2. Vehicle / propulsion assumptions

| Quantity | Value used | Source / verification | Status |
|---|---|---|---|
| Operator-side dry mass (post trans-Saturn-injection) | 5 t | Conops mass budget (pitch §2 fig 06) | **verified** |
| Reactor specific power (Kilopower demonstrated) | 5 W/kg | NASA Kilopower-1 ground test 2018 (~30 W from ~6 kg core; specific power including conversion ~5 W/kg per published estimates) | **sourced** |
| Reactor specific power (Fission Surface Power target) | 10 W/kg | NASA Fission Surface Power Phase 1 contract target (2022) | **sourced** |
| Reactor specific power (megawatt class) | 10 W/kg assumed | speculative, no funded program | **UNSOURCED** |
| Water-MET specific impulse | 700 s | R1 verified open-literature water microwave electrothermal | **sourced** |
| Water-MET efficiency η | 0.30 | R10 assumption | **sourced (R0 / R1 results)** |
| Water radio-frequency ion specific impulse | 2000 s | Pale Blue published number (R1) | **sourced** |
| Water radio-frequency ion η | 0.65 | R1 / R10 assumption | **sourced** |
| Water Hall specific impulse | 1500 s | Generic water-Hall assumption | **unverified for chunk-water purity** |
| Water Hall η | 0.55 | Generic Hall efficiency | **unverified** |
| Water dual-ion specific impulse | 5000 s nominal, swept 3000-12000 s | R3i / R10 exploratory | **TRL 1-2 speculative** |
| Water dual-ion η | 0.55 | guess | **UNSOURCED** |
| Bag capture efficiency η_c | 0.8 | Conops bag-engineering.md §6.2 design point | **sourced** |
| η_c application: multiplier on effective specific impulse | yes | Conops bag-engineering.md §6 convention | **convention-following** |
| **Duty cycle** | **0.5** | **inherited from R5; not justified** | **UNSOURCED — likely conservative** |
| Hohmann floor on inbound TOF | 6.09 yr | structural minimum | **verified** |
| Lunar gravity assist single-flyby ∆v at v_∞=10.3 | 0.46 km/s | `lunar_flyby.py` patched-conic | **verified by sim** |

**Duty cycle is the most likely-to-be-wrong assumption.** Justifications:
- Dawn ion-engine mission: ~70% over 11-yr mission
- BepiColombo ion engine: 60-80% during cruise
- Voyager RTG-driven instruments: continuous (100%)
- Pale Blue commercial GEO servicing: 30-50% (limited by thermal)
- ICEBERG would be a custom design for continuous deep-space operation; 50% is conservative, 70% is mid-realistic, 80%+ requires not-yet-demonstrated thermal continuous operation

**Action: recompute R12, R14, R15 with duty cycle 0.7 sensitivity to see if findings change qualitatively.**

---

## 3. Cost assumptions

| Quantity | Value used | Source / verification | Status |
|---|---|---|---|
| Launch (Falcon Heavy expendable) | $150M | SpaceX commercial pricing | **sourced** |
| Trans-Saturn-injection chemical kick stage (Vulcan-Centaur class) | $140M | Conops pitch (Vulcan-Centaur baseline) | **sourced** |
| Total launch + boost per ship | $290M | sum | **sourced** |
| Ship build cost — conops optimistic | $150-400M | conops saturn-water-isru-sketch.md (first-of-kind $150-300M) | **sourced (concept-paper-grade)** |
| Ship build cost — commercial mid | $250-700M | Northrop Grumman MEV, Boeing 702SP, DARPA RSGS reference points | **sourced reference class** |
| Ship build cost — commercial high | $400-1200M | conservative scaling | **estimated, not sourced** |
| Demonstrator NRE | $500M | guess | **UNSOURCED** |
| Ground operations per year (fleet-wide) | $50M | guess | **UNSOURCED** |
| Price per kilogram baseline | $2,000 | Conops Tier 2 mid-point | **sourced** |
| Price per kilogram premium (strategic reserve) | $20,000 | speculative sovereign-strategic pricing | **UNSOURCED extrapolation** |

**Cost assumptions are concept-paper-grade and not load-bearing for engineering findings.** They're load-bearing for R15/R15b break-even calculations. **Action: tag R15/R15b conclusions explicitly as "concept-paper-grade scenario sketches, not financial model."**

---

## 4. Conops compatibility checks

| Claim | Conops value | My R-rounds value | Status |
|---|---|---|---|
| Round trip headline | 13-13.5 yr | 14 yr (closer to honest) | **R-rounds use 14 yr ceiling, slightly more conservative** |
| Outbound Hohmann time | "~6.1 yr each way" (pitch §1) | 6.09 yr | **agrees** |
| Saturn dwell | "~6 months at Saturn-loiter" or "~1 yr" depending on doc | 1.0 yr | **conservative version** |
| Trans-Saturn-injection burn | 7.3 km/s | 7.3 km/s (R-rounds don't compute this; baked into launch+kick-stage cost) | **agrees** |
| Inbound chunk-fed water delta-velocity | "~4.2 km/s" (Saturn departure 1.5 + cruise braking 2.0 + Earth trim 0.5 + RCS 0.2) | 4.47 km/s (R12 from R9-derived lunar tour residual) | **R-rounds use ~6% higher; within model uncertainty** |
| Lunar gravity assist contribution | "2-3 flybys, ~2.5-3.5 km/s" | R9 simulation: 3-flyby tour sheds 1.43 km/s, 10-flyby tour sheds 5.83 km/s | **R-rounds say conops is ~2x optimistic at 3-flyby** |
| Bag η_c design point | 0.8 (bag-engineering.md §6.2) | 0.8 | **agrees** |
| η_c application | "design at η_c = 0.80 → 46% delivered" (bag-eng §6.2) | apply as Isp multiplier (effective specific impulse = 0.8 × thruster Isp) | **convention-following; bag-engineering doc uses this exact convention** |
| Chunk per ship (Kilopower era) | "~50 t delivered" (pitch §2 table) | 5 t at 14-yr ceiling and 3-flyby tour | **R14 finding: ~10x optimism** |
| Chunk per ship (Fission Surface Power era) | "100-200 t" | 14 t at 14-yr ceiling | **R14 finding: ~7-14x optimism** |
| Chunk per ship (megawatt era) | "500-1000 t" | 233 t at 14-yr ceiling and 3-flyby tour, 608 t at 10-flyby tour | **roughly 1-1.5x optimism — closer** |
| Year-11 cash-positive | yes (via sovereign forward sale) | R15: requires $5B sovereign at year 11 for break-even at year 11 | **R-rounds find conops claim is too aggressive** |
| Steady-state revenue at perpetuity | $1B+/year | R15 R14-corrected gives $0.47B/year at year 36-40 | **R-rounds 2-3x lower than conops claim** |

**Three places where R-rounds diverge from conops:**
1. **Lunar gravity assist ~2x optimism in conops** at 3-flyby tour
2. **Chunk-per-ship 7-14x optimism in conops** at Kilopower / Fission Surface Power tiers
3. **Steady-state revenue 2-3x optimism in conops** under corrected scaling

All three are documented in R14 / R15. Audit confirms these findings are not spurious.

---

## 5. The big assumption to retest: duty cycle

Recomputed key cells at duty cycles 0.5 (R-rounds default), 0.7 (Dawn / BepiColombo heritage), 0.85 (continuous-operation aspiration), and at round-trip ceilings 14/15/16/18/20 yr.

### Headline finding: assumption mix dominates the result

| Assumption mix | 40 kilowatt-electric Fission Surface Power delivers | vs conops 100-200 t |
|---|---:|---:|
| R14 baseline (3-flyby, duty 0.5, 14-yr ceiling) | 14 t | conops 7-14x optimistic |
| Realistic-1 (3-flyby, duty 0.7, 14-yr) | 23 t | conops 4-9x optimistic |
| Realistic-2 (10-flyby, duty 0.7, 14-yr) | 65 t | conops 1.5-3x optimistic |
| Realistic-3 (3-flyby, duty 0.7, 18-yr) | 42 t | conops 2-5x optimistic |
| Optimistic (10-flyby, duty 0.7, 18-yr) | 113 t | **conops claim consistent** |
| Aspiration (10-flyby, duty 0.85, 18-yr) | 139 t | **conops claim consistent** |

**R14's "10x optimism" finding holds under STRICT assumption mix (3-flyby tour, duty 0.5, 14-yr ceiling). Under realistic-to-optimistic mix, the conops scaling claims are roughly right.**

### Duty cycle reference class

| Mission | Duty cycle | Notes |
|---|---:|---|
| Pale Blue commercial cislunar (GEO tug) | 0.3-0.5 | Thermally limited by satellite radiators |
| Dawn (Vesta / Ceres, 11-yr) | ~0.7 | Mission-long average during cruise |
| BepiColombo (Mercury cruise) | 0.6-0.8 | Solar electric propulsion |
| Voyager (continuous instruments) | 1.0 | RTG, not thruster — reference only |
| **ICEBERG custom (assumed)** | **0.7 realistic, 0.85 aspirational** | **bespoke thermal mgmt + continuous reactor** |

Pale Blue's commercial 0.5 is not the right reference class — those are short GEO maneuvers limited by satellite radiator area, not deep-space cruise with bespoke thermal management. R-rounds 5-15b inherited the 0.5 duty cycle without justification; **0.7 is the better default**.

### Round-trip ceiling sensitivity

Doubling-time approximately: every 4-year extension of round-trip ceiling approximately doubles deliverable chunk per ship at fixed power class.

| Power | 14-yr (3-flyby, duty 0.7) | 18-yr (3-flyby, duty 0.7) | 20-yr (3-flyby, duty 0.7) |
|---:|---:|---:|---:|
| 10 kWe | 2 t | 7 t | 9 t |
| 40 kWe | 23 t | 42 t | 52 t |
| 100 kWe | 66 t | 114 t | 138 t |
| 500 kWe | 349 t | 588 t | 708 t |

**The 14-yr ceiling was my arbitrary user-imposed constraint.** Actual conops headline is 13.5 yr (which doesn't close at all under any assumption mix). Going to 18 yr (4.5 years past conops headline) gives roughly conops claims at conservative duty cycle.

### Thruster ranking under audit

| Mix | Best thruster at 40 kWe |
|---|---|
| 3-flyby, duty 0.5, 14-yr | water radio-frequency ion (Pale Blue) — 14 t |
| 10-flyby, duty 0.7, 14-yr | water Hall — 65 t (water RFI 61 t, within 6%) |
| Any cell at 500 kWe with duty 0.7+ | water Hall by ~5%; water radio-frequency ion close second |
| Dual-ion at all cells | dominated, sometimes by 5-10x |

**Water radio-frequency ion (Pale Blue) remains the right flight-ready choice — within 5-10% of theoretical-best water Hall, but with TRL 7-8 heritage vs water Hall's TRL 2-3 at chunk-water purity.**

**Dual-ion is dominated at every cell under realistic constraints.** R13's "dual-ion wins" was an artifact of cherry-picking small chunks against overpowered reactors. Confirmed in R10b. Re-confirmed here.

### Audit conclusion

**The campaign's "conops is 10x optimistic" headline (R14, R15, R15b) is conditional on the strict assumption mix.** A more honest statement:

| Honest statement of conops scaling validity |
|---|
| Conops chunk-per-ship table is approximately right *if* we assume: (a) 10-flyby lunar gravity assist tour (operationally aggressive), (b) duty cycle 0.7+ (deep-space heritage, not Pale Blue commercial), (c) round-trip ceiling relaxed to 18+ years (4.5 yr past conops headline), and (d) Fission Surface Power program achieves its 10 W/kg specific power target. Drop any of (a)-(d) and the conops claim becomes 2-10x optimistic. |

This is the honest reframe of R14-R15b. The deck should:
- Acknowledge the conops claims are achievable under realistic (not conservative) assumption mix
- Flag duty cycle and lunar flyby count as the load-bearing operational unknowns
- Note that round-trip extension to 18-20 years (vs conops 13.5) is the cheapest cost-free lever to recover the conops chunk delivery numbers

### What this audit corrects in prior rounds

| Round | Original claim | Audited claim |
|---|---|---|
| R9 | Conops 13-yr round trip "off by 10+ yr" | True at conservative assumption mix; conops 13.5-yr never closes at any mix, but 14-yr closes at high power + relaxed assumptions |
| R9b | "No power class closes 13-yr + 50% delivery" | True at conservative mix; at duty 0.7 + 10-flyby tour, Fission Surface Power 40 kWe closes 14-yr at 60%+ delivery |
| R12 | "10-flyby tour + 15 kWe = 14 yr / 70%" | Still correct |
| R13 | "Dual-ion 200 kWe / 5000 s wins at 89%" | Artifact of asymmetric comparison; confirmed dominated by Hall/RFI in apples-to-apples |
| R10b | "Hall wins by 0-2 pp" | Holds across audit |
| R14 | "Conops 10x optimistic" | Conditional on strict mix; under realistic mix (duty 0.7), conops is ~2-5x optimistic; under optimistic mix (duty 0.7 + 10-flyby + 18-yr), conops is roughly right |
| R15 / R15b | "Financials don't close within 40 yr" | True at R14 strict-mix scaling. Under realistic-mix scaling, R15 cashflow improves materially; needs re-run. |

### Next round candidate

**R15-audit-rerun:** Re-run R15 / R15b with audited assumptions (duty 0.7, realistic ship cost basis, conops fleet cadence) and see whether the "financials don't close" finding survives. My guess: break-even moves from "never" to "year 30-35" under realistic mix — still infrastructure-scale but not catastrophic.

