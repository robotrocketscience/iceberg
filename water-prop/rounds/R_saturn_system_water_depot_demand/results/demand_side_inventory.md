# Saturn-system water-depot demand-side inventory

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Public-source desk study. Scores are this worker's judgments from the cited evidence; every external claim is linked or marked "no source".

Scoring keys:
- **Commitment:** confirmed (funded, in build) / selected (theme or target chosen, not yet funded to build) / studied (concept study) / proposed / aspirational.
- **Water demand from an ICEBERG depot:** none / hypothetical / nonzero.
- **P(materialises by 2050):** rough Bayesian judgment anchored on agency follow-through base rates and locked finding 2 (US space-fission 0-of-6 generalised to outer-system flagship follow-through).

---

## Source 1 — Agency Saturn-system / outer-system missions through 2050

| Mission | Agency | Destination | Commitment | Launch / arrive | Power + propellant | Water demand from ICEBERG depot | P(materialises) |
|---|---|---|---|---|---|---|---|
| **Dragonfly** | NASA (New Frontiers 4) | **Titan (Saturn system)** | **confirmed** — $3.35B life-cycle, in construction (began 10 Mar 2026) | launch July 2028 / arrive 2034 | RTG (Multi-Mission RTG); rotorcraft flies on Titan atmosphere; carries own hydrazine for entry/landing | **none** — arrives fully provisioned; no in-space refueling in conops | ~1.0 (in build) |
| **Enceladus Orbilander** | NASA | **Enceladus (Saturn system)** | studied — Decadal 2023 #2 flagship; not yet a funded build | arrive "no earlier than early 2050s" | own (RTG/solar TBD); own propellant | **none** — science orbiter+lander, self-provisioned | ~0.3–0.5 by 2050 (flagship cadence + budget) |
| **ESA L4 "Enceladus"** | ESA (Voyage 2050) | **Enceladus (Saturn system)** | selected — "Moons of the Giant Planets" theme; Enceladus chosen as L4 target 25 Mar 2024; not yet adopted/built | launch ~2040s / arrive ~2050s | own; own propellant | **none** — self-provisioned science mission | ~0.4 by 2050 (ESA L-class follow-through) |
| **Uranus Orbiter and Probe** | NASA | **Uranus** (via Jupiter gravity-assist) | studied — Decadal 2023 **#1 flagship**, $4.2B | launch early 2030s / arrive ~13 yr later | own; own propellant | **none — does not transit the Saturn system** (Jupiter GA route to Uranus) | ~0.4–0.6 (top flagship priority) |
| Neptune Odyssey / Trident-class | NASA | Neptune / Triton | proposed | aspirational | own | **none — Jupiter GA route, not via Saturn** | low |
| JAXA outer-system | JAXA | — | none with a Saturn-system architecture and a date | — | — | none | — |

**Source-1 reading:** there are **three live Saturn-*destination* missions** (Dragonfly confirmed; two Enceladus flagships studied/selected for ~2050s arrival). **Every one is a self-provisioned science mission that arrives with its own power and propellant.** None has an in-space refueling step in its concept of operations; none is a customer for depot water. The one top-priority outer-system flagship (Uranus) does not even pass through the Saturn system. There is no agency mission, at any commitment level, that demands water at Saturn.

Sources: [NASA confirms Dragonfly / $3.35B / July 2028 (JHU APL)](https://www.jhuapl.edu/news/news-releases/240417-nasa-confirms-apl-led-dragonfly-mission-to-saturn-moon-titan); [Dragonfly construction began Mar 2026 (Wikipedia)](https://en.wikipedia.org/wiki/Dragonfly_(Titan_space_probe)); [Decadal 2023 priorities — Uranus #1, Enceladus Orbilander #2 (SpaceNews)](https://spacenews.com/planetary-science-decadal-endorses-mars-sample-return-outer-planets-missions/); [Uranus $4.2B, Jupiter GA, early-2030s launch (Universe Today)](https://www.universetoday.com/articles/planetary-decadal-survey-says-its-time-for-a-mission-to-uranus-and-enceladus-too-1); [ESA selects Enceladus as Voyage 2050 L4 target, 25 Mar 2024 (European Spaceflight)](https://europeanspaceflight.com/saturns-moon-enceladus-identified-as-primary-target-for-esa/); [ESA Voyage 2050 themes (ESA)](https://www.esa.int/Science_Exploration/Space_Science/Voyage_2050_sets_sail_ESA_chooses_future_science_mission_themes).

---

## Source 2 — Commercial Saturn-system entrants

| Actor | Architecture | Capitalisation | Saturn-system presence | Verdict |
|---|---|---|---|---|
| Orbit Fab | In-space propellant depots + RAFTI refueling port | venture-funded | **none** — LEO/GEO/cislunar only; first operational GEO refuel (with Astroscale) targeted June 2026, xenon | not a Saturn actor |
| Astroscale (US) | Life-extension / refueling servicers (LEXI) | public/venture | none — GEO | not a Saturn actor |
| ispace + Orbit Fab | **Lunar** water/regolith ISRU propellant | venture | none — lunar | **competing supply** for ICEBERG's Earth-orbit market, not a Saturn customer |
| (any other) | — | — | **none found** | empty set |

**Source-2 reading:** **the commercial Saturn-system entrant set is empty.** Every commercial in-space-propellant actor operates in the Earth-orbit/cislunar regime. The nearest-adjacent activity (ispace-Orbit Fab lunar water ISRU) is on the *supply* side of ICEBERG's own Earth-orbit market — it competes with ICEBERG, it does not buy from a Saturn depot. No company has any stated Saturn-system architecture, customer base, or regulatory filing.

Sources: [Orbit Fab — LEO/GEO/cislunar scope; Tanker-001 Tenzing (Factories in Space)](https://www.factoriesinspace.com/orbit-fab); [Astroscale–Orbit Fab first on-orbit fuel-sale agreement, GEO June 2026, xenon (Orbit Fab)](https://www.orbitfab.com/news/astroscale-fuel-sale/); [ispace–Orbit Fab lunar-resource propellant partnership (ispace)](https://ispace-inc.com/news-en/?p=5037).

---

## Source 3 — Logistics-customer demand model (H3)

**Claim under test:** a mission passing the Saturn system could refuel at an ICEBERG depot to reduce its launched propellant mass.

**Forward pipeline of outer-system missions, 2026–2076 (by Δv route):**
- Uranus Orbiter and Probe — **Jupiter** GA → Uranus. Does not enter Saturn's sphere of influence.
- Neptune / Triton concepts — Jupiter GA → Neptune. Not via Saturn.
- Enceladus flagships (NASA, ESA) — Saturn *destination*, arrive provisioned for their own science ops.

**The Δv arithmetic kills the refuel-stop (corrected vis-viva anchors, titan-3 R-dv-anchor-audit):**

To *use* a Saturn depot, a passing mission must (a) capture into a bound Saturn orbit at the depot, then (b) re-depart. From the dv-audit geometry (v∞ at Saturn ≈ 6.21 km/s; Oberth periapsis at 60,000 km):

- Capture burn (hyperbolic → elliptical B-ring parking) ≈ **7.7 km/s**.
- Re-departure burn (elliptical → hyperbolic escape) ≈ **7.7 km/s**.
- **Total Δv to use the depot ≈ 15.4 km/s.**

No flyby mission spends 15.4 km/s to stop for fuel it could instead launch from Earth; a 15.4 km/s capture-and-redepart dwarfs any plausible post-Saturn maneuver savings. And a Saturn-*destination* mission is already capturing, but it arrives with its science propellant and has no large post-arrival Δv to refuel for. **The refuel-stop economics are Δv-inverted: reaching the depot costs more than the depot can save.**

**Source-3 reading:** the logistics market is **≈ 0 missions/decade** with a *net-positive* reason to use the depot. Even the 0–2 missions/decade that physically pass through or arrive at Saturn (the Enceladus flagships) bring their own propellant and gain nothing from refueling. H3 is not a thin market; it is a **Δv-inverted non-market**.

---

## Source 4 — ICEBERG-internal-relay back-of-envelope (H4)

**Concept:** split ICEBERG into (i) a **filler** — one-way Saturn vehicle, single-kWe, fills the depot, never returns; and (ii) a **relay** — fast Earth→Saturn→Earth shipper that picks up depot water and delivers to Earth.

**Why the SCOPE expected this to be the one non-empty reading:** removing the Earth-return leg from the *filler* removes the two framework killers (the 14–16-yr cumulative-burn reactor-lifetime kill and the 50-t small-vehicle mass-floor kill, titan-4 `0eb11a7`) *from the filler*.

**The back-of-envelope problem:** the loaded Earth-return leg does not disappear — it moves to the **relay**. The relay must fly the loaded inbound leg (Saturn departure ~7.7 km/s impulsive / ~27.6 km/s continuous-thrust + cruise braking + Earth capture), which is **the exact leg that killed the one-vehicle architecture.** So:

| Killer | One-vehicle | Two-vehicle filler | Two-vehicle relay |
|---|---|---|---|
| Reactor-lifetime (loaded inbound cumulative burn) | **binds** | removed (no loaded return) | **re-imported** — relay flies the loaded inbound |
| Small-vehicle mass-floor (carry reactor) | **binds** | softens (one-way, no return propellant) | binds if electric; relay needs its own powerplant |
| Propellant mass for inbound Δv | electric, ~ok | n/a | if relay is chemical, Tsiolkovsky at vₑ≈4.4 km/s makes 7.7+ km/s inbound prohibitively propellant-heavy |

**Reading:** the depot decoupling helps **only the filler**. The relay re-imports the binding kill, because *something* must fly the loaded inbound leg and that leg is the wall. Making the relay reusable (many trips) makes the *cumulative* reactor burn **worse**, not better. The two-vehicle architecture therefore does **not** obviously escape the binding constraint; it relocates it.

**The only way H4 escapes the kill** is a relay propulsion mode that the one-vehicle architecture lacked on its inbound leg — candidates: (a) a **depot-water-fed high-thrust relay** that trades the reactor-lifetime burn for a short high-power sprint, or (b) **Earth aerocapture on the relay** to delete the Earth-side capture burn (campaign finding: aerocapture is necessary-but-not-sufficient; it removes Earth capture but not Saturn departure + cruise braking). Neither is demonstrated to clear the loaded-inbound wall.

**Source-4 reading:** the two-vehicle relay is **not a clear escape** on the binding axis. A dedicated R-iceberg-two-vehicle-relay round is **lower priority than the SCOPE anticipated** — it is worth standing up *only if* a relay-propulsion concept that escapes the loaded-inbound kill is identified first. Absent that, H4 does not rescue option (b).
