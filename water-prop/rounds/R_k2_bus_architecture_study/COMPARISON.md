# K2 vs clean-sheet vs hybrid — vehicle-architecture comparison

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Public-source; ROM (rough-order-of-magnitude) cost/schedule.

## K2 Space facts (verified 2026-05-26)

- **Funding:** $250M Series C at **$3B valuation**, December 2025, led by Redpoint (+ T. Rowe Price, Hedosophia, Altimeter, Lightspeed, Alpine Space Ventures). [SpaceNews](https://spacenews.com/k2-space-raises-250-million-to-scale-high-power-satellite-line/)
- **Mega class (flown):** 20 kW power, ~2 t wet mass (Gravitas), ~1 t payload, 3×3 m deck, ~40 m solar array tip-to-tip. Multi-orbit (LEO/MEO/GEO/cislunar). [Via Satellite](https://www.satellitetoday.com/manufacturing/2024/12/20/k2-space-to-build-mega-satellite-for-2026-mission-to-meo/) · [DCD](https://www.datacenterdynamics.com/en/news/k2-space-to-launch-gravitas-satellite-later-this-month/)
- **Gravitas mission:** launched February 2026, SpaceX rideshare; demoed a 20 kW Hall-effect thruster (most powerful flown) raising LEO→MEO; $60M STRATFI contract. [Military Embedded](https://militaryembedded.com/comms/satellites/satellite-for-meo-mission-will-launch-in-february-2026)
- **Stacking:** up to 10 Mega per launch vehicle → **200 kW per launch**. [K2 site](https://www.k2space.com/satellites)
- **Giga class (announced, not built):** **100 kW**, sized for Starship / New Glenn bays; 2027 mission announced. [K2 PR](https://www.prnewswire.com/news-releases/k2-space-announces-details-of-groundbreaking-2027-mission-302583289.html)

## Specific power (H1)

| Source | Specific power (system) | Status |
|---|---|---|
| KRUSTY fission | ~2.4 W/kg | ground-test (locked belief) |
| Flown RTG (GPHS) | ~5.3 W/kg | flown |
| **K2 Mega (solar)** | **~10 W/kg** (20 kW / 2 t wet); ~20 W/kg if 1 t dry-bus basis | **flown Feb 2026** |
| K2 Giga (projected) | ~30 W/kg (SCOPE projection) | announced |
| MW-NEP aspiration | 40 W/kg | TRL 2 (locked belief; upside-only) |

**H1 HELD.** Mega is 10–20 W/kg on a defensible basis — 4–8× KRUSTY fission, ~2–4× flown RTG, and the first *flown* hardware in that band. This is the same physical fact that made NEA close the closed-loop mass loop: solar at ~1 AU is the light-powerplant path, and K2 has now flown it as a product.

## Architecture comparison

| Axis | ICEBERG clean-sheet bus | K2 Giga stack (N×100 kW) | Hybrid (K2 bus + grafted reactor) |
|---|---|---|---|
| Power regime served | any (if reactor) | **solar only → inner-system / NEA (~1 AU)** | reactor at Saturn-arrival |
| Power at Saturn (9 AU) | reactor: full | **~1% of 1-AU rating → dead** (200 kW→~2 kW) | reactor: full; solar dead |
| Specific power | depends on power source | ~10–30 W/kg (solar, flown/near-term) | dominated by reactor (2.4 W/kg) |
| Mass to 40 kWe (inner-system) | clean-sheet ~2–3 t power-bus | **~1.3 t (single Giga fraction) — flown, mass-produced** | n/a (reactor overkill at 1 AU) |
| Deep-space heritage | must build | **LEO/MEO/GEO/cislunar only; 7-yr cruise unproven** | inherits K2's heritage gap + reactor heritage gap |
| Cost (ROM) | high NRE, slow | **low marginal (mass-produced; $60M-class units)** | K2 cost + reactor program cost |
| Schedule | slow (clean-sheet qual) | **fast (flying now)** | gated by reactor program (L0-24) |
| Supply-chain risk | single-program | mass-produced line, $3B-backed | reactor is the binding constraint |

## Closed-loop mass cross-check (H3)

The NEA closed-loop model (`nea_mass_demands.py`, this session) used an array-only solar specific power (150 W/kg) giving a ~0.8 t powerplant at 40 kWe, inside a ~45 t self-consistent dry mass. K2's *whole-bus* system specific power (~10–20 W/kg) is a stricter, real-hardware number: a 40-kWe K2-derived power-bus is ~2–3 t. **Still ~15× lighter than Saturn's fission stack (~21–26 t), and a small fraction of the ~45 t NEA dry mass.** So K2-anchored, flown numbers **corroborate the NEA mass-loop closure** rather than threatening it. **H3 HELD.**

For Saturn the cross-check is moot in the other direction: no solar bus delivers kilowatts at 9 AU, so K2 cannot serve Saturn at all (**H2 HELD — fundamental physics, not a contracting gap**).

## Stack arithmetic (SCOPE sub-question 1)

- 10× Giga = 1 MW — but megawatt-class is fantasy-conditioned per locked beliefs (40 W/kg is TRL 2; MW-NEP retired by project-owner directive). The megawatt stack is not a live ICEBERG cell.
- The *live* inner-system need is 40–100 kWe — **one Giga (100 kW) covers it directly**, no large stack, no on-orbit assembly required. The stack story is only relevant to the retired megawatt dream.
