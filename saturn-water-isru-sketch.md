# Towed Ice-Block ISRU Concept — Back-of-Envelope, Sourced

> **Update [2026-05-01]:** Original ΔV numbers were wrong — partly double-counted, partly didn't account for the low-thrust spiral penalty, partly ignored the solar-power problem at Saturn distance. Corrected numbers come from `saturn_isru_boe.py` (Edelbaum + Tsiolkovsky in this directory). The corrections actually **strengthen** the pitch: the Saturn round-trip doesn't close on water MET alone (it needs chemical or fission-electric for trans-Saturn injection), but **the same architecture pattern closes cleanly for water-bearing near-Earth asteroids**, with **75% delivered-mass fraction** instead of the 36% in the original sketch. The headline finding: "the pattern is right, the first target is an NEA, the Saturn version is a 2040s+ fission-electric upgrade." That's a trade study, not a missed number.

**Purpose:** Upstream back-of-envelope sketch of the architecture: rendezvous with a large icy body, secure it, tow it home, and feed the propulsion system off the cargo itself via a sublimation-capture shroud. Numbers are back-of-envelope but every claim is sourced.

**Why this version is stronger than "harvest at Enceladus":** the earlier framing is a planetary science mission. This framing is **a cislunar-tug-class product, scaled up**. A water-MET in-space tug class building rendezvous, grapple, and orbital tug capability has "tow a chunk of ice home" as a *direct extension* of that capability, not a new mission class.

---

## 1. Concept

1. Small tug (~1 t dry + grapple/tether system) launches from cislunar / LEO with a one-way water-MET propellant load.
2. Cruises to a water-rich target — preferably **a hydrated near-Earth asteroid**, **a periodic short-period comet near aphelion**, or (long-horizon) **a Saturn ring fragment / shepherded Enceladus plume capture**.
3. Rendezvous, characterize, and **secure a multi-tonne to multi-hundred-tonne chunk of ice**. Tether, net, harpoon, or cage — open trade. (A commercial in-space-tug capability is the right starting point; RPO with uncooperative objects is in that lane.)
4. Wrap the chunk in a **multi-layer thermal shroud** that:
   - Blocks direct solar flux during the inbound leg (chunk would otherwise sublimate uncontrolled — *desirable* sublimation is metered).
   - Has an **internal cold surface** (radiator-cooled to <150 K) that captures sublimated H₂O vapor by re-deposition.
   - Feeds metered water from the shroud's collection volume into the MET on demand.
5. Cruise back to LEO / cislunar burning **water shaved off the cargo** — the chunk is simultaneously the propellant tank and the cargo. Aerocapture at Earth.
6. Deliver residual ice to a depot. Drop spacecraft into a parking orbit for the next mission.

---

## 2. Why the bag-as-cold-trap inverts the architecture

The conventional ISRU plan ("land, mine, melt, pump, store, lift") is a TRL stack of separate disciplines, each with its own hardware, each unproven. **Sublimation-capture in a flexible bag turns ISRU into a thermal-management problem instead of a mining problem.**

### Three architectural simplifications stacked

1. **Phase change is sublimation, not melting.** In vacuum, water ice sublimates directly to vapor — no liquid phase. **No melting reservoir, no liquid plumbing in microgravity, no bubble management.** The vapor pressure curve does the work for you:
   - 150 K → ~10⁻⁹ Pa (effectively zero)
   - 200 K → ~0.16 Pa
   - 250 K → ~76 Pa
   - 273 K (triple point) → 611 Pa

   Heat the chunk a little and water vapor flows. **Liquid water in microgravity is a feed-system nightmare; vapor-only is a feed-system dream.** This is one of the major reasons ice ISRU is architecturally simpler than mineral-bound water (NEAs require a heated regolith-extraction process to liberate water from clay).

2. **Enclosure is a flexible bag, not a rigid shroud.** Multi-layer film (MLI heritage, 60+ years of flight history) at <1 kg/m² conforms to the irregular chunk geometry, deploys by unfurling around the cargo after grapple, and weighs ~50 kg for a 100 t chunk vs. 500+ kg for a rigid shroud sized at design time.

3. **Vapor transport is a thermal gradient (passive), not pumping.** Heat-pipe physics: hot side sublimates, cold side condenses, pressure gradient drives mass flow without any moving parts.

### How the bag actually works (heat-pipe topology)

- **Sun-facing side of bag:** lets in some solar IR. Chunk surface here heats to ~200–230 K. Sublimation rate is high.
- **Anti-sun side of bag:** radiator-cooled to <150 K. Bag inner wall acts as a cryopump — vapor re-deposits as frost on it. Sticking coefficient near unity at these temperatures.
- **Pressure differential** between hot side (high vapor pressure) and cold side (essentially zero) drives **natural mass flow** from chunk surface to cold wall. The bag is a giant heat pipe with the chunk as the hot reservoir and the cold-side wall as the condenser.
- **Harvest port** at the cold-side wall: a small heated zone where frost is locally re-sublimated and routed to the MET feed. The MET runs on metered vapor.

### Why this physics is well-understood

- **Comet coma formation:** ice sublimates from the nucleus surface under solar flux; coma grows as the comet approaches the Sun. Whipple's icy-conglomerate model (Whipple 1950, ApJ 111:375)¹ is the foundational reference. Sublimation rate governed by surface energy balance.
- **Lunar polar volatile cold-trapping:** water vapor migrates across the lunar surface and condenses in permanently shadowed regions because the cold trap is below ~110 K (Watson, Murray, & Brown 1961, JGR 66:3033)². Same physics in our bag.
- **Cryopump physics:** standard vacuum-system technology. Surfaces below water's local saturation temperature trap water vapor with near-unity sticking coefficient. (O'Hanlon, *A User's Guide to Vacuum Technology*)¹⁷.
- **Heat pipes:** a closed two-phase loop where vapor migrates from a hot evaporator to a cold condenser under its own pressure gradient. Standard spacecraft thermal control hardware since the 1970s. The bag is conceptually a heat pipe at very large scale.

### Common misconception worth flagging — thrust does *not* "settle" vapor

It is tempting to think that low spacecraft acceleration would push vapor toward the rear of the bag. **It does not, by six orders of magnitude.** Water-MET acceleration is ~10⁻⁴ m/s² for a 5–15 t system. Water vapor thermal velocity at 200 K is ~600 m/s. Thermal motion dominates by ~10⁶. Vapor distribution is governed by **temperature gradients alone**, not by thrust direction.

The same physics is why orbital propellant slosh is hard — once you're at <1 g, fluid distribution is governed by surface tension, capillary action, and thermal gradients, not "down."

### Bag tightness

The bag does not have to be vapor-tight in the "zero leak" sense — only **low-permeability**, in the same way a thermos flask is "low-leak." Acceptable leakage is small compared to the controlled flow from hot wall to cold wall. MLI and multi-layer polymer films routinely achieve permeability adequate for this duty.

Failure modes are graceful: a small puncture leaks some vapor to space but the cold trap still pulls most of it toward the radiator. Total bag failure means rapid cargo loss, but pressure/temperature telemetry would give plenty of warning.

### Mass and architectural advantages over a rigid shroud

- **Mass:** ~50 kg of bag film for a 100 t chunk vs. 500+ kg rigid shroud
- **Deployment:** unfurl-and-cinch operation; no precision rigid-body assembly in deep space
- **Geometry:** conforms to whatever shape the chunk turns out to be
- **Mechanism:** entirely passive vapor transport; only active element is the harvest-port heater that meters vapor into the MET
- **Scales with chunk:** bigger chunk → unfurl more bag

The bag is essentially a deep-space cryopump wrapped around a slowly-evaporating cargo, using the chunk itself as the hot reservoir and the radiator-cooled bag wall as the cold trap. The novelty is *what* it's pumping (a propellant supply you brought home with you), not *how*.

---

## 3. Target tractability ranking

Listed from "could plausibly be demonstrated in <10 years" to "this is the Saturn version":

### 3.1 Hydrated near-Earth asteroid (NEA — most tractable)
*NEA = Near-Earth Asteroid. Asteroid with perihelion < 1.3 AU. NASA tracks ~36,000. The water-bearing subset are C-type carbonaceous chondrites; OSIRIS-REx (Bennu) and Hayabusa2 (Ryugu) both confirmed hydrated minerals at 10–20% by mass.*
- **Water content:** CI/CM carbonaceous chondrite analogues hold up to **~10–20% water by mass**, bound in hydrated phyllosilicates (Rivkin et al. 2002, *Asteroids III*)³.
- **Round-trip ΔV:** comparable to lunar missions (~5–7 km/s) for the most accessible NEAs (Brophy et al. 2012, **KISS Asteroid Retrieval Feasibility Study**)⁴ — that study is *exactly the architectural pattern* you're proposing, just sized for a ~7 m / ~500 t boulder rather than ring ice.
- **Heritage:** Hayabusa2, OSIRIS-REx have demonstrated the rendezvous + sample-acquisition portion. A commercial in-space-tug grapple capability is the missing piece.
- **Catch:** the water is in mineral form, not free ice. Sublimation-capture only works after the regolith is heated; you'd want a heated harvest port rather than passive shroud collection.

### 3.2 Short-period comet, captured near aphelion (medium tractability)
- **Water content:** comet nuclei are roughly **half water ice by mass** (A'Hearn et al. 2011, *Science* 332:1396 on Tempel 1)⁵ — though "rubble pile" structure varies. Rosetta/67P showed surface dust covers most of the nucleus (Sierks et al. 2015, *Science* 347:aaa1044)⁶.
- **ΔV:** larger than NEA missions but tractable for some Jupiter-family comets at aphelion.
- **Catch:** dust contamination of the propellant feed. Filter design becomes a primary system.

### 3.3 Saturn ring fragment (long-horizon)
- **Water content:** **B-ring is ~90–95% water ice by mass** (Cuzzi et al. 2010, *Science* 327:1470, "An Evolving View of Saturn's Dynamic Rings")⁷.
- **Particle sizes:** range from cm-scale to ~10 m boulders in the densest parts; embedded "propellers" suggest larger 100+ m bodies (Tiscareno et al. 2010, ApJ Letters)⁸.
- **ΔV:** ~10–12 km/s outbound (Cassini-class trajectory; Cassini total chemical ΔV ~2.3 km/s after gravity assists, but cruise ~6.7 yrs)⁹.
- **Catch:** it's the romantic target, not the cheap one. NEA demo first; rings as the long-horizon vision.

### 3.4 Enceladus — *not* the right target
Worth noting and dismissing: Enceladus orbits at ~4 R_S, deep inside Saturn's magnetosphere and radiation environment. Saturn's radiation belts are not Jupiter-class but they are not benign — multi-month dwell at 4 R_S exposes spacecraft electronics and crew (if any) to a cumulative dose problem (Roussos et al. 2018, *Icarus* 300:47, on Saturn's MeV proton belts)¹⁰. **Drop Enceladus.** B-ring fragments at ~1.5–2 R_S (outside the densest belts) and outer-ring or shepherded chunks are the better targets within the Saturn system.

---

## 4. ΔV math — corrected, with low-thrust penalty

### Assumptions
- Water MET in plasma mode: **Isp ≈ 700 s, v_e ≈ 6.87 km/s**.
  - **Important caveat:** No commercial water-MET vendor has publicly disclosed Isp, thrust, mass flow, or other performance numbers in a verifiable form. The 700 s figure is a **proxy** drawn from (a) Momentus Vigoride public performance claims via SEC 10-K filings¹³, and (b) Penn State Micci-group MET literature on water and water/methane mixtures (Sullivan & Micci 1994 et seq.)¹². Vendor-actual numbers may differ in either direction. **Do not cite "Isp = 700 s" as any vendor's number** — it is the closest defensible open-literature proxy. Calibrate against vendor-actual hardware specs as soon as they're disclosed.
- Aerocapture at Earth: trim ΔV ~0.5 km/s. TRL 4–5 (Hall et al. 2005)¹⁴.
- Tug dry mass: 1 t including grapple, shroud, MET, avionics.
- Edelbaum coplanar low-thrust transfer formula for spiral phases³⁶.

### 4a. Saturn case — impulsive baseline (full chemical, just to bound the problem)

| Leg | ΔV (km/s) |
|---|---|
| LEO → Earth-departure to V_∞ = 10.30 km/s | 7.29 |
| Saturn capture into highly elliptical at 1.5 R_S (just below escape) | 0.61 |
| Saturn departure (mirror) | 0.61 |
| Earth arrival, propulsive insertion to LEO | 7.29 |
| **Total impulsive, full propulsive** | **15.79** |
| Earth arrival, aerocapture trim only | 0.50 |
| **Total impulsive, with aerocapture** | **9.00** |

Cruise time: ~6.1 yr each way; round trip ~13–14 yr including grapple/secure.

### 4b. Saturn case — low-thrust (Edelbaum)

For continuous-spiral water-MET propulsion, ΔV is much higher:

| Leg | ΔV (km/s) |
|---|---|
| LEO escape spiral (ΔV ≈ V_circ_LEO) | 7.67 |
| Heliocentric Edelbaum, Earth → Saturn (\|v_E − v_S\| heliocentric) | 20.16 |
| Saturn arrival shaping | 1.00 |
| Saturn departure shaping | 1.00 |
| Heliocentric return spiral, Saturn → Earth | 20.16 |
| Earth arrival, aerocapture trim | 0.50 |
| **Total low-thrust, with aerocapture** | **50.49** |

That's a **5.6× penalty** over the impulsive case.

### 4c. The Saturn case **does not close** on water MET

At Isp = 700 s, the outbound-only ΔV of ~25 km/s gives a mass ratio of **39.6** — propellant fraction **97.5%**. The vehicle is essentially all tank.

**This concept needs one of:**
- **Chemical** trans-Saturn injection (~7 km/s impulsive at Isp 450 s) plus low-thrust everywhere else — hybrid architecture.
- **Higher-Isp electric:** Hall (Isp ~1800 s) drops the prop fraction to ~76%; ion (Isp ~3500 s) to ~52%. Workable but the operator's current production stack is MET, not Hall/ion.
- **Nuclear-electric power:** because solar at 9.58 AU gives only **55 W per 5 kW** of Earth-orbit array (1.1% of Earth flux), a Saturn water-tug **must** carry RTG or fission-electric power. Cassini used 880 W BOL of RTG. A water-MET tug needs single- to multi-kW class fission electric — that's the 2040s, not the 2030s.

**Honest assessment: Saturn is the long-horizon vision, not the near-term target.** The architecture pattern (rendezvous, grapple, tow, shroud-collect, aerocapture, depot delivery) is right. The propulsion stack to make it work at Saturn distance is one to two technology generations beyond what commercial water-MET tugs fly today.

### 4d. The **NEA case closes cleanly** — and this is the real pitch

For a representative water-bearing NEA at ~1.05 AU heliocentric:

| Leg | ΔV (km/s) |
|---|---|
| LEO → Earth-departure to V_∞ = 0.36 km/s | 3.20 |
| NEA arrival match (V_∞ ~1.5 km/s typical) | 1.50 |
| Departure from NEA | 1.50 |
| Earth arrival, aerocapture trim | 0.50 |
| **Total round-trip with aerocapture** | **~6.68** |

Trip time: ~6 months one-way for Hohmann. Round-trip ~1.5 yr including loiter at NEA for grapple.

#### Mass ratios (NEA round-trip)
| Propulsion | Isp (s) | Mass ratio | Prop fraction |
|---|---|---|---|
| Water MET, plasma | 700 | 2.65 | 62% |
| Water MET, optimistic | 900 | 2.13 | 53% |
| Hall thruster | 1800 | 1.46 | 31% |

Closes cleanly on water MET. **No exotic power or propulsion required — this is what the current cislunar-tug vehicle class can already do.**

#### **The headline number — chunk-tow return leg only**

Outbound is small-tug; the leverage is on the *return* leg, where the chunk-as-propellant inversion shows up. Return-leg ΔV (depart NEA + Earth aerocapture trim) ≈ **2.0 km/s.**

At Isp = 700 s, mass ratio = 1.34. **Delivered fraction = 75% of grappled chunk mass.**

| Grappled chunk | Delivered to LEO depot |
|---|---|
| 100 t | **75 t** |
| 500 t | **374 t** |
| 1000 t | **747 t** |

### Why the leverage is real
You are not paying tankage mass on the return leg. The chunk's own mass is its own structural envelope. Every kg of MET propellant you burn comes out of the cargo, but you started with so much cargo that the leverage ratio inverts compared to a conventional fuel-and-cargo split.

**Compared to the original sketch's 36% delivery fraction (which had an inflated return ΔV), the corrected NEA case at 75% is roughly 2× better.** The architecture works *better* than the back-of-envelope first suggested — once you target the right body.

### Net economics, single NEA flight
Outbound investment: ~1.6 t water (62% prop fraction × ~2.6 t wet mass) + 1 t hardware + launch cost.
Single-flight return (corrected): **75 t to 747 t** of water delivered to LEO depot per 100 t / 1000 t grappled.
**Mass leverage: 50× to 500× water delivered per kg of Earth-launched water for the NEA case.** Roughly an order of magnitude better than the Saturn version because the gravity well is essentially flat.

### What that water is *worth* in LEO
The leverage number above is interesting in the abstract. It becomes existential when you price it.

**Cost-per-kg to LEO (2024–2025 figures):**
- Falcon 9 dedicated: ~$2,800/kg (SpaceX published price ÷ payload mass)²⁰
- Falcon Heavy: ~$1,400/kg²⁰
- ISS commercial resupply (CRS) effective price: **~$20,000–$50,000/kg of cargo** depending on mission and accounting (NASA OIG 2018, IG-18-016)²¹
- Starship target (eventual, not yet achieved): ~$100–$200/kg²²

**What fraction of LEO mass is water-derived?** For a representative crewed-LEO operation (ISS or successor station):
- **Crew water consumption:** ~3–4 kg/person-day (drinking + hygiene) → for a 7-person station, **~10–14 t/year**²³
- **Crew oxygen consumption:** ~0.84 kg/person-day → **~2.1 t/year** for 7 crew²³
- **Stationkeeping propellant:** ISS uses **~7 t/year** of propellant for reboost (mostly imported via Progress)²⁴
- **Water for ECLSS make-up, EVA cooling, experiment use:** several additional tonnes/year

**Of every kg launched to ISS, roughly 30–50% is water, oxygen, or propellant** that could in principle be sourced from delivered water (electrolyze for O₂ + H₂; use directly for drinking/hygiene; use water-MET propellant for stationkeeping).

**Direct displacement value of a 75 t NEA water delivery (one shroud-tow of a 100 t chunk):**
- Falcon 9 baseline: **~$210M** in launch displacement.
- ISS-CRS baseline: **~$1.5–3.75B**.
- Starship floor: ~$15M (still attractive given on-orbit, no-launch-slip-risk premium).

**Direct displacement value of a 5 t delivery (small first chunk):**
- At Falcon 9 launch cost: **~$14M** in displaced launches.
- At ISS-CRS effective cost: **~$100–250M** in displaced resupply.
- At Starship target: ~$1M (this is the floor — and even at this floor, the science / non-fungible value is dominant; see §5b).

**Direct displacement value of a 750 t NEA delivery (1000 t chunk grappled):**
- Falcon 9 baseline: **~$2.1B** in launch displacement.
- ISS-CRS baseline: **~$15–37B**.
- Starship floor: ~$150M (still the size of a Discovery-class mission award).

**Direct displacement value of a hypothetical 100 t Saturnian delivery (long-horizon):**
- Falcon 9 baseline: **~$280M** in launch displacement.
- ISS-CRS baseline: **~$2–5B**.
- Starship floor: ~$20M.

Even at Starship-floor launch costs, the operator doesn't have to compete with the floor — it has to compete with **whatever NASA / ESA / JAXA / commercial-station-operator is willing to pay for *on-orbit, no-launch-required, beyond-Earth-sourced* water.** That price is set by mission architecture, not by lift cost.

### 4b. The science / non-fungible value (the part NASA writes blank checks for)

The cost-per-kg displacement above is the **logistics** revenue. There is a parallel **science** revenue stream that is not subject to launch-cost competition at all:

- **Cassini cost NASA + ESA ~$3.9B** to *measure* Saturn-system material remotely²⁵. The mission did not return any sample. There has never been a Saturn-system sample-return mission proposed at any cost; the ΔV budget makes it prohibitive for a conventional sampler.
- A by-product of the towed-chunk architecture is that **you are returning macroscopic, kilogram-scale Saturnian-ring material to Earth orbit.** That is, by accident of mission design, the most valuable planetary science sample-return mission ever attempted.
- NASA's New Frontiers and Discovery class missions are budgeted at **~$1B and ~$500M respectively**²⁶. A sample-return mission *to the Saturn system* would, conservatively, be a Flagship-class line item (~$3B+).
- ESA, JAXA, and the new Chinese CNSA Tianwen sample-return programs each have analogous lines.
- Even **0.1% of the towed chunk** allocated to science partners — pristine, sealed, returned to LEO — is a mission worth on its own terms. The operator gets paid by the agency consortium for delivery; the bulk water is *additional* revenue from the depot/logistics market.

This is the dual-revenue argument: **the same flight closes both an economic (depot) thesis and a scientific (sample-return) thesis.** Either alone is hard to fund. Together they make a compelling case to multiple funding sources who don't otherwise overlap.

---

## 5. Bag thermodynamics — sketch

The bag is the architectural innovation. Three jobs:

### 5.1 Control solar flux into the bag
At 1 AU, solar flux is **1361 W/m²** (NASA SORCE TIM measurements)¹⁵. Bare water ice at 1 AU equilibrates near 200 K and sublimates at **~10⁻⁵ to 10⁻⁴ kg/m²/s** (Whipple-type calculation; see Delsemme & Miller 1971, Planet. Space Sci. 19:1229)¹⁶. A 100 t chunk with ~50 m² surface area would lose **~50 g/s ≈ 1.5 t/year** uncontrolled — significant on a multi-year cruise.

The bag's sun-facing side is a partially-transparent or absorber layer that admits a designed amount of IR — enough to drive sublimation at the rate the MET wants to consume vapor. The anti-sun side is high-emissivity radiator. Heat balance is the design knob.

### 5.2 Cold collection surface (cryopump physics)
Anti-sun-side bag inner wall radiator-cooled to **<150 K**. Saturation pressure of water at 150 K is ~10⁻⁹ Pa — well below any vapor pressure the chunk will produce. Sticking coefficient on a clean cold surface is near unity (O'Hanlon, *A User's Guide to Vacuum Technology*, Wiley)¹⁷. Sublimated water from the chunk re-deposits as frost on the cold-wall.

### 5.3 Meter water from cold-wall frost into MET feed
Periodic localized heating of a "harvest port" on the cold-wall inner surface re-sublimates frost at controlled rate; vapor flows through a heated line into the MET feed. The MET runs on vapor; phase-change happens **inside the bag**, not in the thruster feed system, which avoids two-phase flow problems in plumbing — **a known pain point for water-prop systems** (Brinkert et al. 2022, npj Microgravity)¹⁸.

### 5.4 Why the heat-pipe topology is the key insight
The chunk + bag system is **a giant heat pipe at scale.** The chunk is the evaporator, the cold-wall is the condenser, the pressure gradient between them drives mass flow with no mechanical pumping. Heat pipes have flown on every spacecraft thermal control system since Skylab; this is just one at large scale. The mass flow rate is set by the heat balance, which we control via the absorber/radiator design.

### 5.5 Why this is harder than I'm making it sound
- **Active radiator at <150 K** with realistic spacecraft heat loads is non-trivial. Loop heat pipes / pulse tubes scale poorly with radiator area; passive radiation may be sufficient at outer-solar-system distances but at 1 AU you need active rejection.
- **Center of mass walks** as the chunk sublimates and frost grows on the cold-wall. GNC + attitude control with a slowly-deforming cargo is its own dissertation.
- **Bag puncture / tear** by chunk shifting, micrometeoroid, or thermal cycling. Failure is graceful (slow leak) but mission-ending if catastrophic.
- **Dust contamination** if the target is anything but pure ring ice. The bag's harvest port becomes a filter problem.
- **Tether / capture dynamics** with a several-hundred-tonne uncooperative cargo. NASA's TSS-1R taught everyone that tethers in space are gnarlier than simulation suggests (NASA TSS-1R post-flight analysis, 1996)¹⁹.

### 5.6 Common misconception — thrust does not "settle" vapor

It is tempting to think low spacecraft acceleration pushes vapor toward the rear of the bag. **It does not, by six orders of magnitude.** Water-MET acceleration is ~10⁻⁴ m/s² for a 5–15 t system; water vapor thermal velocity at 200 K is ~600 m/s. Thermal motion dominates by ~10⁶. **Vapor distribution is governed by temperature gradients alone**, not thrust direction. (Same physics as why orbital propellant slosh is hard — at <1 g, fluid distribution is governed by surface tension, capillary action, and thermal gradients, not "down.")

### 5.7 Bag tightness requirement

The bag does **not** have to be vapor-tight in the "zero leak" sense — only **low-permeability**, in the same way a thermos flask is "low-leak." Acceptable leakage is small compared to the controlled hot-wall-to-cold-wall mass flow. MLI and polymer films routinely achieve permeability adequate for this duty. Some passive sublimation loss is treated as a budgeted η_c reduction (see §5b-bis).

---

## 5b-bis. Mission phase architecture (hybrid Saturn version)

The pure-water-MET architecture doesn't close at Saturn distance (§4c). The version that does close is **hybrid: chemical for the impulsive heavy lifts, water MET for everything else**. Most of the chemical hardware is bought, not built — the operator's product is the proprietary tow/shroud/MET stack.

### Phases

| # | Phase | Propulsion | Provider | Duration |
|---|---|---|---|---|
| 1 | LEO insertion | Falcon 9 / FH / Starship | Bought (rideshare or dedicated) | minutes |
| 2 | Trans-Saturnian injection (~7.3 km/s) | Chemical kick stage, Isp ~450 s | Bought (Impulse Helios, Centaur V, Star-class solid) or built | minutes |
| 3 | Heliocentric coast outbound | Coast (water MET trim only) | Operator | ~6–7 years |
| 4 | Saturn capture (~0.6 km/s impulsive at periapsis) | Storable hypergolic (MMH/N₂O₄, Isp ~310 s) | Operator | minutes |
| 5 | Ring chunk rendezvous & loiter | Water MET (low-thrust, plenty of time) | Operator | weeks–months |
| 6 | Grapple, secure, deploy shroud | Cold gas / mechanisms | Operator | hours–days |
| 7 | Saturn departure (~0.6 km/s impulsive) | Hypergolic + water MET (chunk-fed) | Operator | minutes for impulsive, then continuous |
| 8 | Heliocentric coast inbound | Water MET trim, fed from chunk | Operator | ~6–7 years |
| 9 | Earth aerocapture | Aerodynamic + small trim burn | Operator | minutes |
| 10 | LEO depot delivery / orbit phasing | Water MET, chunk-fed | Operator | days–weeks |

### Why this stack works
- **Phase 2 (TSI) is bought, not built.** Impulse Helios is being designed for exactly this mission class; Centaur V is procurable. The operator doesn't have to develop a deep-space chemical kick stage. Major de-risking move — the operator focuses engineering on what's proprietary, buys what's commodity.
- **Phase 4 (Saturn capture) uses storable hypergolics, not cryo.** MMH/N₂O₄ has 60+ years of flight heritage, doesn't boil off over a 7-year cruise. Lower Isp than LH2/LOX, but you only need ~0.6 km/s, so propellant mass is small.
- **Phase 5 onward is the proprietary stack.** Water MET, rendezvous, grapple, tow, shroud — all the in-house pieces that justify a water-MET tug operator's existence.
- **Phases 7–10 are chunk-fed.** The architectural inversion: once the shroud is deployed, the water MET runs off harvested water for the entire return leg. No tankage carried home.

### Indicative mass budget (mission delivering ~10 t to LEO)

| Element | Mass | Notes |
|---|---|---|
| TSI kick stage (Helios-class, jettisoned post-burn) | ~30–50 t | bought; Isp 450 s; ΔV 7.3 km/s |
| Hypergolic capture/depart system + propellant | ~3–4 t | for two ~0.6 km/s impulsive burns |
| Water MET tug dry mass (avionics, GNC, MET, grapple, shroud, radiators) | ~1–2 t | proprietary |
| Outbound water for cruise trim | ~0.5 t | small |
| **Vehicle stack at LEO (pre-TSI)** | **~35–60 t** | Within Falcon Heavy expendable capability (~64 t to LEO) |
| Chunk grappled at Saturn | **12–15 t** | per §4d math — to deliver 10 t |
| Chunk delivered to LEO depot | **10 t** | the product |

### Tow-leg ΔV sensitivity — chunk size for delivered mass

For the water-MET tow leg (post-chemical-TSI), with $m_\text{dry} = 1$ t and Isp = 700 s (v_e = 6.87 km/s):

$$M_0 = (m_\text{dry} + m_d) \cdot e^{\Delta V/(\eta_c v_e)} - m_\text{dry}$$

**Perfect shroud capture (η_c = 1.0):**

| Tow-leg ΔV | 5 t delivered | 10 t delivered |
|---|---|---|
| 1 km/s (chemical does Saturn capture+depart; MET trims only) | 5.95 t | 11.74 t |
| 2 km/s (chemical TSI+capture; MET departs Saturn) | 7.02 t | 13.71 t |
| 5 km/s (chemical TSI only; MET does most Saturn-side) | 11.45 t | 21.83 t |
| 10 km/s (water MET does most Saturn-side maneuvering) | 24.8 t | 46.3 t |

**Realistic shroud capture (η_c = 0.8 → effective Isp = 560 s, v_e = 5.49 km/s):**

| Tow-leg ΔV | 5 t delivered | 10 t delivered |
|---|---|---|
| 1 km/s | 6.20 t | 12.21 t |
| 2 km/s | 7.65 t | 14.94 t |
| 5 km/s | 13.93 t | 26.51 t |
| 10 km/s | 38.4 t | 71.8 t |

**Headline:** in the realistic Saturn-hybrid case where chemical handles TSI and the impulsive Saturn capture/depart, **the water-MET tow leg sees ~1–2 km/s of ΔV**. **A 6–8 t chunk gets you 5 t to LEO; a 12–15 t chunk gets you 10 t.** Both are well within the size range of B-ring particles or shepherded F-ring fragments.

### The Tsiolkovsky correction for sublimation losses

Vanilla Tsiolkovsky already handles non-constant $\dot{m}$ — that's what the integration does. The non-Tsiolkovsky term in this concept is **uncaptured sublimation**: mass that leaves the chunk without producing thrust because the shroud isn't a perfect cold-trap. Define $\eta_c$ = fraction of sublimated mass captured and routed to the MET. Then:

$$\Delta V = \eta_c v_e \ln\frac{m_0}{m_f}$$

Equivalently: **effective Isp = $\eta_c \times$ Isp_nominal.** This is the real architectural sensitivity number — the shroud thermal design lives or dies on $\eta_c$. The η_c = 0.8 row above is the realistic engineering target; η_c < 0.5 means the architecture doesn't close.

### The summary, plainly

The mission stack is mostly bought — Falcon Heavy or Starship for the lift, an Impulse-Helios-class kick stage for TSI, hypergolics for Saturn capture and depart. The operator's product is the water MET tug, the rendezvous, the grapple, the shroud, the chunk-fed propulsion. Most of the de-risking is moving as much of the mission as possible onto bought hardware so the focus stays on what's actually novel. Headline math: tow leg sees about 1–2 km/s for the water MET, so a 12–15 tonne chunk gets you 10 tonnes to a LEO depot. Sensitivity that drives the design is shroud capture efficiency.

---

## 5c. Vehicle cost, loss probability, and risk economics

### Vehicle cost — real analogs (don't anchor on Cassini)

Cassini's $3.9B is the wrong anchor. Cassini was a flagship science platform with a multi-instrument suite, RTG, and a foreign-built lander. A water-MET tug is **commercial single-purpose hardware** — completely different cost class.

Right cost analogs:

| Vehicle class | Cost (rough, public) |
|---|---|
| Commercial GEO commsat (Maxar/Lockheed bus) | $200–400M including launch²⁷ |
| Lockheed A2100 bus alone | $100–150M²⁷ |
| **Momentus Vigoride** (water-MET tug) | est. $10–20M per vehicle²⁸ |
| **D-Orbit ION** | est. $5–10M per vehicle²⁸ |
| **Impulse Mira / Helios** | low-tens of $M (Helios more) |
| Hayabusa2 (small sample-return craft, JAXA) | ~$150M total mission²⁹ |
| OSIRIS-REx (NASA Discovery sample-return) | ~$800M total mission³⁰ |
| Lucy (Trojan flyby) | ~$981M³¹ |
| Psyche | ~$1B³² |

**Saturn-capable tug — realistic estimates:**
- **First-of-kind:** $150–300M (hardware + R&D amortization + integration + launch). Most is non-recurring engineering.
- **Nth-of-kind, in production:** **$50–100M per vehicle including launch.** Heritage from a commercial short-range water-tug fleet drives unit cost down. By the time the operator flies Saturn missions, it should have built and flown 10+ short-range tugs already.
- **NEA demo mission (the realistic first step in this architecture):** **~$50–150M.** This is the right number to anchor on — not the Saturn flagship cost.

### Loss probability — historical baseline

| Mission class | Approximate loss rate |
|---|---|
| Pre-2000 Mars + outer-planet | ~30–40% (MCO, MPL, Beagle 2, Phobos 1/2, etc.)³³ |
| Post-2000 outer-planet | ~10–15% (biased toward landers / aerobraking events) |
| Cruise-only deep-space (Cassini, Voyager 1/2, New Horizons, Juno, OSIRIS-REx outbound) | ~5% per mission |

**Hardware wants to keep working in deep space; it's the *events* that kill missions.**

### Failure-probability stack — towed-chunk architecture, first-of-kind

| Phase | TRL | Realistic P(fail) |
|---|---|---|
| Launch (Falcon Heavy class) | 9 | 2–4%³⁴ |
| Cruise outbound (7 yr) | 8 (Cassini heritage) | 5–8% (radiation + MTBF) |
| RPO with uncooperative target | 7–8 (Hayabusa2, OSIRIS-REx) | ~5% |
| **Grapple of multi-tonne ice chunk** | **3–4 (no flight heritage)** | **10–20% — biggest single risk** |
| **Sublimation-shroud thermal control** | **3 (paper concept)** | **5–10% — second biggest** |
| Cruise inbound with ablating tethered cargo | 2–3 | 10–15% (tether dynamics, CoM walk, GNC under deformation) |
| **Aerocapture at Earth** | **4–5 (never flown operationally)** | **10–25% on first attempt** |
| Final disposal / depot delivery | 7 | ~2% |

**Combined first-of-kind P(success): ~40–60%.** That's bad for a science flagship; **excellent for a commercial venture** if the success-case payoff is right.

### Drivers of those numbers

1. **Total ionizing dose over 14-yr mission.** Shielding mass, part selection (rad-hard vs. rad-tolerant COTS), trajectory choices that minimize Jupiter-belt dwell.
2. **MTBF on rotating machinery.** Every moving part is a wear-out clock. Architecture choice (control moment gyros vs. reaction wheels vs. magnetic + thruster only) is a ~10× reliability lever.
3. **Software fault tolerance.** Round-trip light time at Saturn ~80 minutes. The vehicle handles every fault autonomously for an hour-plus before the ground can react. **End-to-end simulation problem.**
4. **Aerocapture corridor design.** Margin between skipout and demise. Sim + GNC + thermal all have to close together. Currently the riskiest never-flown element.
5. **Tether dynamics with deforming cargo.** TSS-1R taught us real tethers behave nothing like sim¹⁹. With a multi-hundred-tonne uncooperative ablating cargo, this is the highest-novelty subsystem.
6. **Cargo securing geometry.** Net vs. tether vs. cage vs. harpoon — different failure modes, different mass penalties. Open trade.

### Worst-case write-down

Complete mission loss:
- Hardware + launch: **$100–250M** (first-of-kind to nth-of-kind)
- Mission ops to date of failure (~$10–20M/yr × 7 yr cruise to halfway point): **$70–140M**
- **Total sunk: ~$200–400M for a complete loss.**

Compare to:
- Cassini: $3.9B with 0% revenue on success
- Webb: ~$10B with 0% revenue on success
- Mars Polar Lander: ~$165M lost (1999) ≈ $300M today, zero return³⁵

**A $200–400M failure with a $360M+ upside per successful flight is a better risk profile than every flagship NASA has flown.**

### The risk-mitigation framing, plainly

The honest expected-value math: first-of-kind P(success) is probably 40–60% — not great by flagship standards, very good by commercial standards. Worst-case write-down is $200–400M. Best-case single-flight return is $360M+ on logistics, plus science-program-budget money on top. The EV closes even at coin-flip odds, *and* every failure informs the next vehicle. NEA demo first proves the grapple, shroud, and aerocapture for two orders of magnitude less money. By the time the operator flies the Saturn version, it's flown a dozen short-range chunks already and the unit P(success) is in the high 80s.

This isn't a moonshot science gamble; it's a **learning-curve investment program with revenue at every step.**

---

## 6. The honest caveats

1. **Cruise time = many years.** Cassini took **6.7 years one-way** to Saturn⁹ (with Venus-Venus-Earth-Jupiter gravity assists). A round-trip towed-chunk mission to the Saturn system is therefore **~13–15 years** including outbound cruise, ~6–12 months for grapple/secure/depart, and inbound cruise. Power degradation, MTBF on rotating machinery, software / ground-system continuity over a 15-year mission — all real engineering programs in their own right. Voyager has flown 47+ years, so it's not unprecedented; but it shapes the architecture (high reliability, deep autonomy, generous redundancy). The NEA-first demo (§3.1) is the tractable starting point precisely *because* it skips the multi-decade timeline.
2. **Aerocapture TRL is low.** No mission has done it operationally¹⁴. The math doesn't close without it.
3. **Shroud design is novel.** Cryopumps are mature on the ground; making one work at scale on a tethered, ablating, slowly-deforming cargo is new engineering.
4. **GNC with massive ablating cargo** is non-trivial.
5. **NEA demo first.** A hydrated near-Earth asteroid mission is the architecturally honest first step. The Saturn mission is the long-horizon picture this enables.
6. **None of this is publicly demonstrated.** Both the towed-cargo architecture and the shroud-collection mechanism are paper concepts. The math closes; the hardware doesn't exist.

---

## 7. Honest closure on Saturn vs NEA

Saturn doesn't close on water-MET alone — heliocentric Edelbaum penalty plus the solar-power problem at 9.58 AU pushes prop fraction past 97%. Fission-electric is required, which is a 2040s vehicle class. **But** — the same architecture closes cleanly on near-Earth asteroid water at current MET Isp. NEA round-trip is about 6.7 km/s with aerocapture, prop fraction ~62%, and the chunk-tow return leg delivers about 75% of grappled chunk mass to LEO. A 100 t chunk delivers 75 t; a 1000 t chunk delivers 747 t. NEA is the version to build first.

The gating items: aerocapture TRL, the shroud thermal architecture, and tether dynamics on an uncooperative ablating cargo. Those are the cross-discipline closure questions a simulation-and-mission-systems function owns.

It's a dual-revenue mission. The bulk water is logistics revenue against LEO launch displacement — at Falcon 9 prices, even a 100 t delivery is hundreds of millions in displaced launch. The *same* flight is also the most valuable planetary-sample-return mission ever attempted. NASA spent ~$4B on Cassini just to *measure* Saturn material; nobody's ever returned a kilogram. A consortium-funded science allocation off the same towed chunk is a separate revenue stream that's not subject to launch-cost competition at all.

---

## 8. Connection to a generic water-MET roadmap

- **Commercial short-range water tugs (now):** LEO → GEO with water MET. Validates propulsion class.
- **Next:** cislunar transfers, lunar surface delivery.
- **Long horizon:** lunar / asteroid water → orbital depot.
- **This concept:** the architectural pattern that turns "lunar water" into "any water in the inner solar system." Same vehicle class. Same propulsion. Just a longer leash and a smarter shroud.

The deeper connection isn't "a cool idea about Saturn." It's that the same architectural frame — water as the propellant, tugs as the vehicle class — extends without modification from today's commercial roadmaps to any water source in the inner solar system.

---

## References

1. Whipple, F. L. (1950). "A comet model. I. The acceleration of Comet Encke." *Astrophysical Journal* 111:375. <https://doi.org/10.1086/145272>
2. Watson, K., Murray, B. C., & Brown, H. (1961). "The behavior of volatiles on the lunar surface." *Journal of Geophysical Research* 66(9):3033–3045. <https://doi.org/10.1029/JZ066i009p03033>
3. Rivkin, A. S., Howell, E. S., Vilas, F., & Lebofsky, L. A. (2002). "Hydrated minerals on asteroids: the astronomical record." In *Asteroids III* (Bottke et al., eds.), University of Arizona Press, pp. 235–253. <https://www.lpi.usra.edu/books/AsteroidsIII/pdf/3036.pdf>
4. Brophy, J., et al. (2012). "Asteroid Retrieval Feasibility Study." Keck Institute for Space Studies / NASA JPL. <https://kiss.caltech.edu/final_reports/Asteroid_Retrieval_final_report.pdf>
5. A'Hearn, M. F., et al. (2011). "EPOXI at Comet Hartley 2." *Science* 332(6036):1396–1400. <https://doi.org/10.1126/science.1204054>
6. Sierks, H., et al. (2015). "On the nucleus structure and activity of comet 67P/Churyumov-Gerasimenko." *Science* 347(6220):aaa1044. <https://doi.org/10.1126/science.aaa1044>
7. Cuzzi, J. N., et al. (2010). "An Evolving View of Saturn's Dynamic Rings." *Science* 327(5972):1470–1475. <https://doi.org/10.1126/science.1179118>
8. Tiscareno, M. S., et al. (2010). "Physical characteristics and non-Keplerian orbital motion of 'propeller' moons embedded in Saturn's rings." *Astrophysical Journal Letters* 718:L92. <https://doi.org/10.1088/2041-8205/718/2/L92>
9. NASA / JPL Cassini mission record: launch 15 October 1997, Saturn orbit insertion 1 July 2004 (~6.7 yr cruise). <https://solarsystem.nasa.gov/missions/cassini/overview/>
10. Roussos, E., et al. (2018). "A radiation belt of energetic protons located between Saturn and its rings." *Science* 362(6410):aat1962 (and related work in *Icarus* 300:47, 2018, on Saturn MeV proton belts). <https://doi.org/10.1126/science.aat1962>
12. Sullivan, D. J., & Micci, M. M. (1994). "Performance testing and exhaust plume characterization of a microwave arcjet thruster." *AIAA-94-3127*. (Penn State MET program; multiple follow-on papers through ~2010.) Citation form per AIAA Joint Propulsion Conference proceedings.
13. Momentus Inc. — public statements on Vigoride MET performance. Investor presentations and 10-K filings (SEC EDGAR, ticker MNTS). <https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=MNTS>
14. Hall, J. L., Noca, M. A., & Bailey, R. W. (2005). "Cost-benefit analysis of the aerocapture mission set." *Journal of Spacecraft and Rockets* 42(2):309–320. <https://doi.org/10.2514/1.4118>
15. NASA SORCE TIM solar irradiance baseline ≈ 1361 W/m² at 1 AU. <https://lasp.colorado.edu/home/sorce/data/tsi-data/>
16. Delsemme, A. H., & Miller, D. C. (1971). "Physico-chemical phenomena in comets — III. The continuum of Comet Burnham (1960 II)." *Planetary and Space Science* 19(10):1229–1257. <https://doi.org/10.1016/0032-0633(71)90180-2>
17. O'Hanlon, J. F. (2003). *A User's Guide to Vacuum Technology* (3rd ed.). Wiley-Interscience. ISBN 978-0471270522. (Standard reference on cryopump operation; sticking-coefficient and saturation-pressure tables.)
18. Brinkert, K., et al. (2022). "Fundamentals and future applications of electrochemical energy conversion in space." *npj Microgravity* 8:52. <https://doi.org/10.1038/s41526-022-00239-y>
19. NASA (1996). TSS-1R post-flight investigation. Kennedy Space Center / Marshall reports on tethered satellite dynamics and tether failure modes. <https://ntrs.nasa.gov/citations/19990017542>
20. SpaceX published prices: <https://www.spacex.com/media/Capabilities&Services.pdf> (Falcon 9, Falcon Heavy capacity & price). Cost-per-kg back-calculated from advertised LEO mass.
21. NASA Office of Inspector General (2018). "NASA's Management of the International Space Station and Efforts to Commercialize Low Earth Orbit." Report IG-18-021 / IG-18-016 series; CRS effective per-kg cost analysis. <https://oig.nasa.gov/docs/IG-18-021.pdf>
22. Musk, E. — public statements on Starship long-run cost target ($100–$200/kg). Multiple presentations 2017–2024. Treat as forward-looking; not yet realized.
23. Anderson, M. S., et al. (2018). "Life Support Baseline Values and Assumptions Document." NASA/TP-2015-218570 Rev. 1. <https://ntrs.nasa.gov/citations/20180001338> — crew metabolic rates for water, O₂, food.
24. NASA ISS reboost statistics, Roscosmos Progress / Northrop Cygnus reboost reports. Approx. 7 t/yr propellant for ISS station-keeping — varies year to year. <https://www.nasa.gov/international-space-station/>
25. Cassini-Huygens mission cost: NASA + ESA + ASI total ~$3.26B in then-year dollars, ~$3.9B inflation-adjusted to 2017 launch end-of-mission accounting. NASA mission overview: <https://science.nasa.gov/mission/cassini/>
26. NASA Discovery and New Frontiers cost caps: Discovery ~$500M (FY15); New Frontiers ~$1B (FY15), excluding launch and operations. NASA SMD program documentation: <https://science.nasa.gov/planetary-science/programs/>
27. Maxar / Lockheed A2100 / Boeing 702 commercial GEO bus prices: aggregated from public satellite procurement filings, FCC Form 312 disclosures, and analyst reports (Northern Sky Research, Euroconsult). Order-of-magnitude figures only.
28. Momentus and D-Orbit per-vehicle costs: estimated from public 10-K filings (Momentus, ticker MNTS) and D-Orbit press disclosures around their Series C. Not directly published; inferred from program totals divided by vehicle count.
29. Hayabusa2 program cost: JAXA published total mission cost ~16.4B JPY ≈ $150M USD. <https://global.jaxa.jp/projects/sas/hayabusa2/>
30. OSIRIS-REx mission cost: ~$800M lifecycle per NASA. <https://www.nasa.gov/osiris-rex>
31. Lucy mission cost: ~$981M per NASA Discovery Program documentation. <https://science.nasa.gov/mission/lucy/>
32. Psyche mission cost: ~$1.0B per NASA Discovery Program. <https://science.nasa.gov/mission/psyche/>
33. Pre-2000 Mars/outer-planet loss rate: aggregated from Mars Climate Orbiter (1999), Mars Polar Lander (1999), Mars Observer (1993), Phobos 1 (1988), Phobos 2 (1989), Mars 96 (1996), and successful counter-cases. See NASA NSSDCA mission archive: <https://nssdc.gsfc.nasa.gov/planetary/>
34. Falcon Heavy reliability: 11/11 successful launches as of late 2025; Falcon 9 family ~99% success since 2017. SpaceX launch manifest: <https://www.spacex.com/launches/>
35. Mars Polar Lander loss: ~$165M mission cost (1999 dollars). NASA failure investigation report: <https://ntrs.nasa.gov/citations/20000033568>
36. Edelbaum, T. N. (1961). "Propulsion requirements for controllable satellites." *ARS Journal* 31(8):1079–1089. <https://doi.org/10.2514/8.5723> — foundational closed-form result for low-thrust circle-to-circle transfers, including coplanar special case ΔV = \|v₁ − v₂\|. Implementation in `saturn_isru_boe.py` in this directory.

---

*Note on sources: I am confident of refs 1–4, 6–11, 14–18 — these are well-known, citation-stable papers and reports. Refs 5, 12, 13, 19 I am citing from memory of the literature; verify the exact volume/page before quoting them.*
