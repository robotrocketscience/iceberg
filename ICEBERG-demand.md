# ICEBERG — Demand-side hardening (WTP curve)

**Companion to `ICEBERG-pitch.md` §4 (economics) and §9 #7 (customer WTP open question).** The pitch prices ICEBERG against an **alternative-cost ceiling** (Earth-launch displacement, with lunar-ISRU as the actual planning ceiling per §3.4). It does not yet commit to a *demand-side* model — i.e. who actually buys, how much, and at what stated WTP. This document is the bottoms-up build that pitch §9 names as the §7-converging deliverable: a price-elasticity curve at three supply tiers, anchored to named buyers and their alternative-cost stacks.

Written without access to actual customer conversations. Every number below is built from published per-buyer demand drivers and published alternative costs. **The single output that would change every line of this document is one round of stated-WTP interviews with the five buyers in §3.** This is the gap pitch §7 calls out and the work that converts §4 from a sketch to a forecast.

---

## 0. Methodology and confidence levels

Each buyer demand estimate carries one of three confidence labels:

| Label | Meaning | Example |
|---|---|---|
| **Anchored** | Built from published per-unit consumption × published fleet/crew size | ISS water demand (NASA TP-2015-218570 × 7 crew) |
| **Inferred** | Built from architecture analogs that have not yet flown at the scale assumed | GEO-servicing fleet propellant if water-MET adopted |
| **Speculative** | Built on a program / market that does not yet exist or has not committed to water-derived consumables | Mars-architecture refueling at scale |

The aggregated demand curve in §5 explicitly separates anchored from inferred-plus-speculative tonnage so the reader can see which bucket each tier depends on.

---

## 1. Buyer enumeration

Six buyer classes, ranked by combined (volume × likelihood) for the 2040–2050 ICEBERG delivery window. Pitch §7 names the five-conversation discovery list; this document expands it to six because the operator's own water-MET fleet is itself a load-bearing internal customer.

| # | Buyer class | Confidence | Anchor reference |
|---|---|---|---|
| 1 | Crewed LEO stations (ISS + commercial successors) | Anchored | NASA TP-2015-218570 (life-support baseline values) |
| 2 | Lunar surface / Gateway operations | Inferred | Artemis architecture (NASA HEOMD); largely lunar-ISRU-served |
| 3 | GEO satellite servicing fleets | Inferred | Northrop SpaceLogistics MEV-1/MEV-2 public ops |
| 4 | DoD strategic-resilience reserve | Speculative | DoD Space Strategy 2020 (no specific water program) |
| 5 | Mars-architecture propellant | Speculative | SpaceX Starship Mars architecture (public claims only) |
| 6 | Operator-internal tug fleet | Anchored | Plausible cislunar-tug-operator fleet roadmap intent; razor-and-blades reasoning per pitch §6 stream 2 |

---

## 2. Per-buyer demand build

### 2.1 Crewed LEO stations — *Anchored*

**Per-person consumption (NASA TP-2015-218570, "Life Support Baseline Values and Assumptions Document," 2018 Rev. 1):**

| Item | kg/person/day | Notes |
|---|---|---|
| Drinking water | 2.0 | ECLSS recovery currently ~93% on ISS WPA |
| Hygiene water | 1.6 | EVA cooling + hygiene |
| Food prep / rehydration | 0.8 | Some shipped wet, some dry |
| **Total water mass throughput** | **~4.4** | Pre-recycling |
| Oxygen consumption | 0.84 | Sourced from electrolyzed water on ISS |

**Net make-up water per person (after ~80% effective recycling)**: ~1 kg/person/day.

**Plus stationkeeping propellant**: ISS reboost is ~7 t/yr (Progress + Cygnus, NASA ISS overview). For commercial stations of similar mass class, scale linearly with mass.

**2030–2050 station population scenarios:**

| Scenario | Stations operational | Total crew | Anchored water demand (t/yr) | Anchored prop demand (t/yr) |
|---|---|---|---|---|
| **Conservative** | ISS-class only (ISS or one direct successor) | 7 | ~3 (make-up only) | ~7 |
| **Base case** | 2–3 commercial stations (Axiom, Vast Haven-1, Starlab) | 20–30 | ~10–15 | ~20–30 |
| **Optimistic** | 5–7 stations across multiple operators | 50–70 | ~25–35 | ~50–70 |

**Net anchored total, base case: ~30–45 t/yr in the 2040 timeframe.** Anchored to NASA's own per-person consumption numbers and currently-funded commercial-station programs.

### 2.2 Lunar surface / Gateway — *Inferred (and largely served by lunar ISRU)*

**Crewed lunar surface (Artemis steady state):**
- 4-person base, periodic occupancy → ~6 t water make-up + ~3 t O₂/yr (per-person × occupancy fraction)
- Surface mobility / EVA prop: ~5–10 t/yr

**HLS ascent propellant:** SpaceX HLS variant uses LOX/CH4. Not directly water-served.
- Blue Moon Mk2 uses LH2/LOX. Hydrogen-side could in principle be water-electrolysis-sourced, but lunar ISRU at the pole is the natural supplier.

**Gateway stationkeeping:** NRHO, ~125 kg/yr xenon for ion propulsion (Gateway PPE). Not water-MET.

**Net for ICEBERG in this segment: ~0 t/yr direct demand** in the base case. Lunar ISRU has the gravity-well advantage for surface-and-near-Moon delivery (pitch §3.4 reasons 1–2). ICEBERG only competes here if a future user chooses to source LEO-staged water for a lunar mission and finds ICEBERG cheaper than launching from Earth — possible at scale, not load-bearing for the demand model.

### 2.3 GEO satellite servicing — *Inferred*

**Existing operations (2026):**
- Northrop SpaceLogistics MEV-1 (docked Intelsat 901, 2020) and MEV-2 (Intelsat 10-02, 2021). Hydrazine-class propellant.
- Astroscale ELSA-d (debris demo). No bulk-prop business yet.
- Starfish Space Otter (announced commercial servicing).

**Next-gen architecture (2030s):**
- Northrop's Mission Robotic Vehicle (MRV) + Mission Extension Pods (MEP) — refueling vs. life-extension trade. If refueling becomes commercial product, per-customer prop demand: ~50–200 kg/yr.
- Fleet of 50–100 MEPs by 2040 → ~5–20 t/yr of *delivered* propellant in the GEO operations volume.

**The water-MET adoption question.** Today's servicing fleet runs on hypergolics (MMH/N₂O₄ or hydrazine). For ICEBERG to sell into this segment, customers must convert to water-MET — the razor-and-blades anchor per pitch §6 stream 2. Realistic conversion rate: low single digits in 2040, growing.

**Net inferred: ~5–15 t/yr by 2040, dependent on water-MET adoption rate.** Could grow to 50+ t/yr by 2050 if water-MET wins ~50% of the new-fleet servicing market.

### 2.4 DoD strategic-resilience reserve — *Speculative*

Per pitch §3 and §6 stream 4, the DoD/SDA strategic angle is that off-Earth water becomes a resilience asset (analog: petroleum strategic reserve). No current DoD program funds this; the closest authority is general "space domain awareness" and depot-anchor procurement under SDA.

**Speculative demand:** if a 100-tonne strategic reserve is established at LEO depot in the 2040s, that's a one-shot 100 t buy + ~5–10 t/yr maintenance. Could repeat for a NRHO reserve.

**Net: 100–250 t one-shot, 10–25 t/yr ongoing.** Not load-bearing for the floor case but premium-priced if the program materializes. **No DoD conversation has happened to validate this** — pitch §9 #11 calls this out explicitly.

### 2.5 Mars-architecture propellant — *Speculative*

**SpaceX architecture:** Starship Mars-bound vehicle requires ~1,200 t LEO propellant per outbound ship. SpaceX intends to refuel via tanker Starships from Earth, not from in-space ISRU. ICEBERG doesn't directly compete with SpaceX's stated plan.

**The water-derivation pivot:** if any Mars program decides to electrolyze + Sabatier in-LEO instead of launching prop tankers, ICEBERG-delivered water becomes input. Per ship: ~1200 t propellant requires ~600 t water if methane is sourced separately, or ~1000+ t water if both methane and oxygen come from water-derived stack. **This is a multi-launch-window architectural choice that does not exist today and may never.**

**NASA HEO Mars architecture:** decades from materializing if at all. Not a planning anchor.

**Net speculative: 0 t/yr in 2040, possibly 200–500 t/yr post-2045 if a Mars program adopts a water-source architecture.** Pitch §4 induced-demand row (b) lives here.

### 2.6 Operator-internal tug fleet — *Anchored* (if an operator stands up a cislunar fleet)

If the same operator running ICEBERG also operates a cislunar tug fleet by 2040, it's the largest captive customer for ICEBERG-delivered water. Each tug carrying ~1 t prop per mission, executing ~10 missions/year at fleet scale of 20–50 vehicles → **~200–500 t/yr of internal water demand**.

This is the captive-customer effect (the operator drinks its own champagne) and probably the most robust single demand component, because the operator has unilateral control over both supply and demand. Internal transfer pricing applies (i.e. it doesn't show up at the external $/kg ceiling).

**Net anchored: 200–500 t/yr by 2040 if the operator's tug fleet reaches the size cislunar-tug roadmaps currently project.** This number depends entirely on the operator's commercial trajectory, not on external customer adoption.

---

## 3. Per-buyer alternative-cost stacks (the WTP ceiling)

Each buyer's WTP is bounded above by the cost of their next-best alternative. Below those ceilings, ICEBERG's actual price is set by competition (lunar ISRU at scale) and by what the operator decides to leave on the table.

**Reference launch costs (2024–2026):**
- Falcon 9 dedicated: ~$2,800/kg (SpaceX published)
- Falcon Heavy: ~$1,400/kg (SpaceX published)
- ISS commercial resupply (CRS) effective per-kg: ~$25,000–50,000/kg (NASA OIG IG-18-021)
- Starship target: ~$200/kg (SpaceX projection, not yet operational)

**Reference lunar-ISRU delivered cost (planning band):**
- Sanders et al. 2019, NASA Glenn / KSC ISRU economic analyses: $1,000–3,000/kg delivered to NRHO at mid-scale; ~$2,000–5,000/kg to LEO when factoring lunar-surface gravity-well
- **Mid-2030s planning band: $1,500–3,000/kg to LEO.** Drops as fleet scales.

| Buyer | Alternative-cost stack | WTP ceiling | WTP floor (post-competition) |
|---|---|---|---|
| Crewed LEO stations | CRS at $25–50k/kg, OR commercial cargo at $5–20k/kg projected | $5,000–10,000/kg | $1,000–2,000/kg (set by lunar-ISRU at scale) |
| Lunar surface | Lunar ISRU (gravity-well advantage) | $1,500/kg lunar floor | ICEBERG not competitive |
| GEO servicing | Earth-launched hypergolics + tug delivery to GEO; ~$30,000/kg effective at GEO | $5,000–15,000/kg | $2,000–5,000/kg |
| DoD strategic reserve | No commercial alternative; mission-essential pricing | $10,000–50,000/kg (premium) | $5,000–10,000/kg |
| Mars-architecture water | Earth-launched + in-LEO Sabatier vs. Starship LEO refill | $500–2,000/kg | $200–500/kg (volume-bound) |
| Operator-internal | Earth-launched water-MET propellant via Falcon Heavy share | $1,400/kg | Internal transfer (TBD) |

**Two-line summary of the ceiling.** The crewed-station + GEO-servicing + DoD segments support **$3,000–10,000/kg** in the 100 t/yr supply tier. As supply grows, lunar ISRU's $1,500–3,000/kg planning band caps the bulk-water price at roughly $1,000–2,000/kg in the 1,000 t/yr tier. At 10,000 t/yr, Mars-architecture induced demand is the load-bearing buyer — and that buyer is **price-sensitive in the $200–500/kg band** because it competes with Starship tanker refills at Starship-cost-floor pricing.

---

## 4. Stated-WTP estimates — what each buyer would actually say

These are estimates of what a single discovery conversation would surface, marked with confidence. **None of these have been validated by an actual conversation.**

### 4.1 Orbit Fab (depot operator)

- **Self-described mission:** in-space propellant logistics; closest to a paying buyer for ICEBERG water.
- **Stated WTP estimate:** $2,000–5,000/kg in the 2030–2040 window for water that arrives at an LEO depot orbit. Above CRS-substitution pricing because Orbit Fab can re-monetize at higher per-customer pricing.
- **Confidence: medium.** Orbit Fab's actual published numbers focus on hydrazine-class propellants, not water; their water program is less developed.
- **What would change this:** their actual depot-economics teardown — what's their target margin, their per-kg dispense price, and their throughput assumption.

### 4.2 Starfish Space (servicing fleet)

- **Self-described mission:** satellite servicing using SpaceX-rideshare-deliverable Otter vehicles.
- **Stated WTP estimate:** $3,000–8,000/kg if and only if Otter converts to water-MET propulsion, which it currently doesn't. **Conversion cost is the real friction.**
- **Confidence: low.** Starfish hasn't published a roadmap for water-MET adoption.
- **What would change this:** vendor MET-spec disclosure + a customer-engineering workshop to size the conversion cost.

### 4.3 Northrop SpaceLogistics (existing GEO-servicing operator)

- **Self-described mission:** life-extension and refueling for GEO commsats.
- **Stated WTP estimate:** $5,000–15,000/kg at GEO, **but ICEBERG delivers to LEO**. The cost to move water LEO→GEO via tug roughly halves the deliverable WTP. Net: $2,500–7,500/kg ICEBERG floor pricing.
- **Confidence: medium.** Northrop's existing fleet runs on hydrazine; conversion would be a multi-year program decision.
- **What would change this:** a Northrop-internal trade study on hydrazine vs water-MET for the next-generation MRV/MEP fleet.

### 4.4 DoD-SDA (strategic resilience customer)

- **Self-described mission:** space-domain resilience; potential anchor depot customer.
- **Stated WTP estimate:** $10,000–25,000/kg for the strategic reserve (one-shot) at premium pricing. $5,000–8,000/kg for ongoing maintenance volume.
- **Confidence: very low.** No program funds this today. Pitch §6 stream 4 names a national-security business-development bridge as the relationship vector but no conversation has happened.
- **What would change this:** the §7 90-day DoD-SDA conversation in pitch §7.

### 4.5 SpaceX / NASA HEO (Mars architecture)

- **Self-described mission:** human Mars exploration.
- **Stated WTP estimate:** $200–500/kg, only at very high volume (10⁴ t/yr+) and only if architecture pivots to water-derived propellant.
- **Confidence: very low.** SpaceX has publicly committed to Earth-launched tanker-Starship refilling; no in-space ISRU dependency in current architecture.
- **What would change this:** a Starship tanker reuse-rate failure forcing architectural revisit, or NASA HEO going its own way with a different propellant stack.

---

## 5. Aggregated WTP curve at three supply tiers

The headline output of this document. **Tonnage at each tier breaks out by anchored / inferred / speculative.**

### 5.1 Demand-stack table

| Buyer | 100 t/yr tier | 1,000 t/yr tier | 10,000 t/yr tier | Confidence |
|---|---|---|---|---|
| Crewed LEO stations | 30 t/yr @ $5,000–10,000/kg | 50 t/yr @ $2,000–5,000/kg | 80 t/yr @ $1,000–2,000/kg | Anchored |
| Operator-internal tug fleet | 50 t/yr @ internal | 300 t/yr @ internal | 800 t/yr @ internal | Anchored |
| GEO servicing | 10 t/yr @ $3,000–7,500/kg | 50 t/yr @ $2,000–5,000/kg | 150 t/yr @ $1,500–3,000/kg | Inferred |
| DoD strategic reserve | 10 t/yr @ $10,000–25,000/kg (one-shot during ramp) | 50 t/yr @ $5,000–10,000/kg | 100 t/yr @ $3,000–5,000/kg | Speculative |
| Lunar surface (LEO-staged only) | 0 | 50 t/yr @ $1,500–2,000/kg | 200 t/yr @ $1,000–1,500/kg | Inferred (lunar-ISRU competitive) |
| Mars-architecture | 0 | 0 | 8,000 t/yr @ $200–500/kg | Speculative |
| **Total demand at tier** | **100 t/yr** | **500 t/yr** | **9,330 t/yr** | mixed |

### 5.2 Tier-by-tier reading

**Tier 1 — 100 t/yr supply (entry / Kilopower era):**
- Demand exists with high confidence (mostly anchored to stations + operator-internal).
- Pricing power is high: limited supply meets premium-paying buyers.
- **Realized blended price: ~$3,000–5,000/kg.** Closer to ISS-CRS displacement than Falcon-Heavy displacement, because the buyers in this tier are mission-essential and on-orbit-convenience-paying.
- **Annual revenue at blended midpoint: ~$300–500M/yr.** This corresponds to pitch §4 floor-row "Kilopower" annual run-rate ($370M/yr at single-ship cadence) — and is consistent with the multi-ship-cadence path's $1.0–1.2B at the same chunk-size assumption, because that path delivers more than 100 t/yr.

**Tier 2 — 1,000 t/yr supply (FSP era):**
- Demand still mostly anchored + inferred. Mars hasn't kicked in.
- Lunar ISRU is now a credible competitor at $1,500–3,000/kg planning band.
- **Realized blended price: ~$1,500–3,000/kg** — pricing converges to lunar-ISRU floor for bulk segments, premium retained for DoD + GEO segments.
- **Annual revenue at blended midpoint: ~$1.0–2.5B/yr.** Consistent with pitch §4 mid-program row ($550M/yr at the FSP-era chunk size with 1 ship/window cadence; multi-ship cadence gets to the upper band).

**Tier 3 — 10,000 t/yr supply (sub-MW / MW era + Mars):**
- Volume requires Mars-architecture induced demand to clear.
- Mars buyer dominates volume but is price-sensitive ($200–500/kg).
- Premium segments still pay $1,500–3,000/kg but they're now <15% of total volume.
- **Realized blended price: ~$300–800/kg** (volume-weighted toward Mars).
- **Annual revenue at blended midpoint: ~$3–8B/yr.** Consistent with pitch §4 steady-state row's upside band ($1.2–2.1B/yr) extended to 10× the assumed delivered tonnage.

### 5.3 Confidence-stratified version

If we discount speculative demand (Mars + DoD) entirely:

| Tier | Anchored + inferred-only volume | Anchored + inferred-only blended price | Conservative revenue |
|---|---|---|---|
| 100 t/yr supply | 90 t/yr clears | $4,000/kg | ~$360M/yr |
| 1,000 t/yr supply | 450 t/yr clears (50% supply unused) | $2,000/kg | ~$900M/yr |
| 10,000 t/yr supply | 1,330 t/yr clears (87% supply unused) | $1,500/kg | ~$2B/yr |

**The conservative reading: thesis closes at the floor and FSP tiers without ever needing Mars-architecture demand.** Pitch §2's multi-ship-cadence floor case ($1.0–1.2B/yr at Kilopower) is consistent with the 1,000 t/yr conservative line above; the upside columns in pitch §4 require Mars-architecture-class induced demand to absorb the 10,000 t/yr supply tier.

### 5.4 What's load-bearing vs. upside

| If you remove… | Floor case still closes? | Steady-state run-rate |
|---|---|---|
| Mars-architecture demand | Yes | Drops $5–7B/yr in Tier 3 — still ~$2B/yr conservative |
| DoD strategic reserve | Yes | Drops $0.5–1B/yr in Tier 3 — modest |
| Operator-internal tug fleet | Yes (loses captive demand, loses internal transfer revenue but recovers external) | Drops ~$0.3–1B/yr depending on tier |
| Crewed station demand | Yes (anchored but small) | Drops ~$0.1–0.4B/yr |
| Lunar-LEO-staged segment | Yes | Drops ~$0.1–0.3B/yr |
| **GEO servicing + Operator-internal + Stations all simultaneously** | **No** | Floor case drops below $200M/yr; thesis breaks |

**The thesis breaks if all three of (anchored + operator-captive + GEO-inferred) fail.** Two of the three failing is recoverable. **Pitch §9 #7 (customer WTP) is the actual decision-class question because it determines whether GEO-servicing converts to water-MET — which is the only one of the three that has real market-adoption risk.**

---

## 6. Lunar-ISRU vs ICEBERG crossover model

Pitch §3.4 asserts ICEBERG's marginal cost beats lunar ISRU at scale. This section is the two-curve model that backs the assertion.

### 6.1 Cost structures

**Lunar ISRU delivered to LEO:**
- Mining + extraction capex: amortizes over decade; ~$200–500/kg at full lunar-fleet scale (NASA Glenn ISRU economic analyses; Kornuta et al. 2018; Sowers 2018)
- Lunar surface → NRHO / EML: ~3 km/s ΔV out of lunar gravity well. Per-kg propellant penalty even with reusable lunar lander.
- NRHO → LEO: another ~4 km/s on whatever vehicle handles the leg.
- **Net at scale: ~$1,500–3,000/kg in LEO** per published analyses. Floor possibly $1,000/kg if all stages reach reuse maturity.
- **Marginal cost dominated by:** lunar surface power (always-on extraction during 14-day day cycle), lander reuse rate, NRHO→LEO transport.

**ICEBERG delivered to LEO:**
- Per-flight cost (nth-of-kind, pitch §5): ~$265M including launch + ops + amortized R&D
- Per-flight delivered chunk: 50 t (Kilopower) → 200 t (FSP) → 500–1000 t (MW)
- Per-kg cost: $5,300/kg (Kilopower era) → $1,300/kg (FSP era) → **$265/kg (MW era)**
- **Marginal cost dominated by:** TSI launch cost (single chemical burn), sustaining ops budget, reactor amortization

### 6.2 Crossover curve

| Tier | Lunar ISRU $/kg | ICEBERG $/kg | Crossover |
|---|---|---|---|
| 100 t/yr | $2,000–3,000 | $5,300 | **Lunar wins** |
| 1,000 t/yr | $1,500–2,000 | $1,300 | **ICEBERG wins, narrowly** |
| 10,000 t/yr | $1,000–1,500 | $265–500 | **ICEBERG wins by 3–6×** |

**Crossover sits between Tier 1 and Tier 2** — i.e. the FSP-era chunk size (~200 t delivered per ship at multi-ship cadence). This matches pitch §3.4's assertion qualitatively but sharpens the timing: lunar ISRU wins the first decade of LEO supply (Tier 1 tonnage); ICEBERG wins from Tier 2 onward. **They genuinely coexist by serving different markets** rather than competing on the same curve.

### 6.3 Failure mode for the model

**If lunar ISRU drops to $500/kg.** Some advocacy-grade lunar-ISRU analyses (Spudis & Lavoie 2011; ULA-aligned Cislunar-1000 model) project $200–500/kg at very-large-scale lunar mining. If that materializes, ICEBERG's crossover slides out to Tier 3, and the thesis depends much harder on Mars-architecture induced demand to absorb supply.

**Mitigation:** the moat (pitch §3) is set by orbital mechanics, not by $/kg. Even at parity, ICEBERG's positional advantage is preserved through the depot-standard lock-in argument (pitch §3, Case A). Lunar ISRU at $500/kg + ICEBERG at $700/kg in the same LEO market is a price war ICEBERG loses on bulk but wins on premium segments and on the first-mover depot interface standards.

---

## 7. What would shift the curve

Sensitivity ranking (largest first):

1. **Mars-architecture water-derived adoption.** $5–7B/yr swing in Tier 3 between adoption and non-adoption. This is the single largest upside lever and the single largest source of induced-demand uncertainty.
2. **GEO-servicing water-MET conversion rate.** Each 10% of the next-gen servicing fleet that adopts water-MET adds ~$50–150M/yr to the demand curve in Tier 2.
3. **DoD strategic-reserve program funding.** $0.5–1.5B one-shot revenue + ~$50–100M/yr maintenance if any single program funds it.
4. **Lunar ISRU realized cost.** Each $500/kg drop in lunar floor pricing pulls the crossover up one tier and shifts more of ICEBERG's defensible market into the premium-segment-only band.
5. **Commercial LEO station population.** Each additional 10-person station adds ~$10–50M/yr in anchored demand.
6. **Starship per-kg lift cost.** Each $500/kg drop in Starship operational $/kg compresses the entire WTP ceiling proportionally; ICEBERG's premium-segment-only revenue stays intact, bulk thins.

---

## 8. What this document does **not** close (deferred to actual conversations)

Pitch §7 names five customer-discovery conversations; this document substitutes per-buyer analysis for those conversations and is therefore necessarily one shell less rigorous. The five gaps that only conversations can close:

1. **Stated** WTP from each buyer at each tier (vs. estimated from alternative-cost stacks here).
2. **Adoption-rate decisions** for water-MET conversion (Starfish, Northrop, future MRV/MEP customers).
3. **Program funding pathway** for DoD strategic reserve (does any FY27+ DoD program have a line item that could absorb this?).
4. **SpaceX architecture commitment** on whether tanker-Starship refill stays the only Mars approach or whether a water-derivative pivot is even on the table.
5. **Orbit Fab depot-economics teardown** so the actual margin structure between supplier (ICEBERG) and dispenser (depot operator) can be modeled rather than assumed.

The 90-day pressure-test described in pitch §7 is the next concrete deliverable. **Until those five conversations happen, every number in §5 carries the uncertainty band stated in §0.**

---

## 9. Updated open-questions (delta to pitch §9)

| § | Item | Status before this doc | Status after |
|---|---|---|---|
| #7 | Customer WTP at 100/1k/10k t/yr | "five customer-discovery conversations" | **Estimated** with per-buyer alternative-cost stacks. Stated-WTP from actual conversations still required for forecast-grade. |
| #8 | Lunar-ISRU price floor in 2040s | "track Artemis-adjacent programs" | **Modeled** crossover at Tier 1→2 boundary. Sensitivity to $500/kg lunar floor surfaced. |
| #9 | Induced-demand growth assumption | "$50–200B requires 5–20× growth" | **Decomposed** by buyer and confidence. Conservative reading drops Mars-architecture and still closes the floor case at Tier 1. Speculative reading underwrites pitch §4 upside. |
| (new) | Thesis-break sensitivity test | not in pitch | **Identified**: thesis breaks only if anchored + operator-captive + GEO-inferred demand all fail simultaneously. Two-of-three failures are recoverable. |
| (new) | Model failure mode if lunar ISRU drops to $500/kg | not in pitch | **Surfaced**: depot-standard lock-in is the moat residual; ICEBERG retains premium segments under price-war scenario. |

---

## 10. References

Sources cited above; full citation list follows pitch.md/conops.md format.

- NASA Anderson et al. (2018). "Life Support Baseline Values and Assumptions Document." NASA/TP-2015-218570 Rev. 1. <https://ntrs.nasa.gov/citations/20180001338>
- NASA Office of Inspector General (2018). "NASA's Management of the International Space Station and Efforts to Commercialize Low Earth Orbit." Report IG-18-021. <https://oig.nasa.gov/docs/IG-18-021.pdf>
- Sanders, G. B., et al. (2019). "ISRU Technology Development for U.S. Lunar and Mars Exploration." NASA Glenn Research Center technical reports. (Multiple papers; representative: Linne et al. 2018, ASCE Earth and Space conference.)
- Kornuta, D., et al. (2018). "Commercial Lunar Propellant Architecture: A Collaborative Study of Lunar Propellant Production." (United Launch Alliance / Colorado School of Mines.) <https://www.csmspace.com/research/lunar/CommercialLunarPropellantArchitectureWhitePaperReleased.pdf>
- Sowers, G. F. (2018). "A Cislunar Transportation System Fueled by Lunar Resources." *Space Policy* 37:103–109. <https://doi.org/10.1016/j.spacepol.2016.07.004>
- Spudis, P. D., & Lavoie, A. R. (2011). "Using the resources of the Moon to create a permanent cislunar space faring system." AIAA Space 2011 Conference paper.
- SpaceX published prices: <https://www.spacex.com/media/Capabilities&Services.pdf>
- Northrop SpaceLogistics MEV-1/MEV-2 mission summaries: <https://www.northropgrumman.com/space/space-logistics-services/>
- Starfish Space, Otter mission profiles: <https://www.starfishspace.com/>
- Brophy, J., et al. (2012). "Asteroid Retrieval Feasibility Study." Keck Institute for Space Studies / NASA JPL. <https://kiss.caltech.edu/final_reports/Asteroid_Retrieval_final_report.pdf>

---

*Methodology: bottoms-up demand built per-buyer from published per-unit consumption × published or projected fleet/crew sizes. Alternative-cost stacks built from published launch costs and lunar-ISRU economic analyses. Confidence labeling per §0. Five remaining open items per §8 require actual customer-discovery conversations to close.*
