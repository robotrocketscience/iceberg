# Market anchors for LEO water clearing price, 2030s

Research compiled 2026-05-15 by enceladus-r5 via web research agent. Original
research-agent transcript notes preserved below with verbatim citations.

## Anchor table

| # | Anchor | Year | Quoted $/kg | 2026-USD $/kg* | Source | Interpretation |
|---|--------|------|-------------|----------------|--------|----------------|
| 1 | Orbit Fab hydrazine in GEO ($20M / 100 kg) | 2022 | $200,000 | ~$220,000 | https://payloadspace.com/orbit-fab-announces-in-space-refueling-prices/ ; https://spacenews.com/orbit-fab-announces-in-space-hydrazine-refueling-service/ | Hard ceiling for "any liquid in hard-to-reach orbit." GEO not LEO; hydrazine not water. Willingness-to-pay anchor for life-extending propellant. |
| 2 | Orbit Fab LEO water/propellant | 2022-2026 | Not published | — | https://www.orbitfab.com/news/hydrazine-fuel-price/ | Orbit Fab explicitly states LEO pricing is "custom" — public LEO $/kg does not exist. Itself a data point. |
| 3 | NASA CRS-2 cargo to ISS (total contract) | 2018 | ~$71,800/kg | ~$87,000 | https://oig.nasa.gov/wp-content/uploads/2024/02/IG-18-016.pdf ; https://spacenews.com/nasa-will-pay-more-for-less-iss-cargo-under-new-commercial-contracts/ | What NASA pays today for crew-rated logistics to LEO. Crew-rated premium is large. |
| 4 | Falcon 9 Dragon ISS cargo (mission-cost basis) | ~2020 | ~$23,300/kg | ~$26,800 | https://en.wikipedia.org/wiki/Falcon_9 | Non-crew-rated full-up mission cost. Includes launch + capsule, not just water. |
| 5 | Saturn V → LEO (Apollo era) | 1969 | $8,250/kg | ~$10,000 | https://www.planetary.org/space-policy/cost-of-apollo | Historical anchor. Apollo-era LEO delivery in 2026 dollars is cheaper than CRS-2 cargo today. |
| 6 | Starship to LEO bulk propellant tanker (target) | 2024-2025 | $100-1,600/kg (range); aspirational $10-20/kg | $100-$1,600 | https://www.nextbigfuture.com/2025/01/spacex-starship-roadmap-to-100-times-lower-cost-launch.html ; https://spacenexus.us/guide/space-launch-cost-comparison | **Load-bearing competing supply curve.** If Starship hits mid-case, Earth-launched water clears at $200-2,000/kg LEO in 2030s. |
| 7 | Starship HLS tanker campaign per Artemis mission | 2024 | 1,200-1,500 t propellant per HLS; 10-20 tankers | — | https://www.nextbigfuture.com/2023/12/nasa-says-up-to-20-spacex-starship-refueling-launches-per-moon-mission.html ; https://www.gao.gov/assets/d24106256.pdf | NASA-validated propellant demand >1,000 t per Artemis mission. Largest plausible customer at 2-3 missions/yr through 2035. |
| 8 | ULA Cislunar 1000 (Bruno) economy projection | 2016-2018 | $2.7T/yr by ~2046; 20 Bt lunar ice resource | — | https://spacenews.com/ulas-tory-bruno-argues-for-u-s-investments-in-the-production-of-fuel-in-space/ ; https://www.nasaspaceflight.com/2018/03/ula-laying-foundations-econosphere-cislunar-space/ | Aspirational total addressable market. Narrative anchor; not defensible as clearing price. |
| 9 | TransAstra asteroid water valuation | 2020-2022 | $10,000/kg | ~$11,500 | https://www.asapdrew.com/p/asteroid-mining-2026 | Asteroid-mining business case assumes water in space clears at ~$10k/kg. Value-of-product, not transacted price. |
| 10 | Karman+ staged cost-down roadmap | 2025 | Phase 1 $10k/kg → Phase 2 $1k/kg → Phase 3 $100/kg | same | https://www.karmanplus.com/karman-masterplan/ ; https://techcrunch.com/2025/02/19/karman-digs-up-20m-to-build-an-asteroid-mining-autonomous-spacecraft/ | Most explicit asteroid-water cost curve. Phase 3 aspirational and undated. Phase 1 $10k/kg matches TransAstra — soft industry consensus on first-transactable price for delivered space water. |
| 11 | Xenon terrestrial commodity (not in LEO) | 2023 | $10,000/kg terrestrial | ~$10,500 | https://www.linkedin.com/posts/phase-four_innovation-spacepropulsion-satellite-activity-7142620723755270145-Jyac ; https://www.giesepp.com/wp-content/uploads/2019/11/A831-Mission-Cost-for-Gridded-Ion-Engines-using-Alternative-Propellants.pdf | $10k/kg is what electric-propulsion industry pays on ground for propellant. Add launch → xenon-in-LEO at $12-30k/kg in satellite hardware. Real, transacted comparable. |
| 12 | NASA ISRU breakeven analysis (NTRS 20205007564) | 2020 | "Low thousands $/kg to LEO" breakeven (paper exists, PDF not text-extracted) | — | https://ntrs.nasa.gov/api/citations/20205007564/downloads/ISRU-Paper3-Final.pdf | **Flag: extrapolation.** Research agent could not extract the precise number. Should be retrieved before external citation. |

\* Inflation: ~2.5%/yr compounded to 2026 dollars. Rounded.

## Honesty flags from the research agent

- **No published LEO water clearing price exists.** Every figure above is either different orbit, different commodity, different cost structure, or unrealized target.
- **Bryce / Euroconsult / NSR reports paywalled.** Defensible 2030s sizing requires $5-15k report purchases not done here.
- **Anchor 12 PDF was binary-only via WebFetch.** A human should pull the breakeven figures before external citation.

## Elasticity model (per research agent synthesis)

Demand for water-in-LEO is **bimodal**, not smooth, with two distinct customer classes:

1. **Satellite life-extension / station-keeping** (Orbit Fab customer): elastic, price-sensitive, max ~$50-100k/kg even with strong willingness-to-pay because underlying satellite has finite remaining life. Total addressable demand: few hundred t/yr at most even in optimistic case.

2. **Propellant aggregation for beyond-LEO missions** (HLS / Artemis / DoD cislunar customer): inelastic up to ~$20-50k/kg because alternative is "do not fly the mission" — but capped on quantity by mission cadence (Artemis = >1,000 t demand but cadence 1-2/yr). Highly sensitive to Starship tanker $/kg. If Starship hits $200/kg, Earth-launched water wins and this market collapses to $300-800/kg with asteroid/Saturn water priced out. If Starship stalls at $1-2k/kg, in-space water at $5-15k/kg has a real window.

**The load-bearing variable is Starship economics, not water-mining economics.** ICEBERG's defensible business case requires either (a) Starship to underperform its targets, or (b) a niche Starship cannot compete in (delivering pre-positioned water to high-energy orbits where Earth-launched water needs additional in-space transport).

## Research agent's recommended planning range

| Tier | $/kg in LEO | Annual demand at this price |
|---|---|---|
| Pessimistic | $2,000-5,000 | ~50-200 t/yr |
| Likely | $10,000-20,000 | ~500-2,000 t/yr |
| Optimistic | $50,000-200,000 | ~100-500 t/yr early |

**Central planning number: $10,000/kg** (consistent with TransAstra, Karman+ Phase 1, xenon-as-comparable). Explicit sensitivity to Starship at $500/kg downside and GEO-hydrazine $200k/kg upside.

**Do NOT cite Cislunar 1000 $2.7T TAM as defensible — it is narrative, not modelable.**
