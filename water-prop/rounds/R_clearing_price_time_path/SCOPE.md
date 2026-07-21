# R-clearing-price-time-path — anchoring R183's open price-decay parameter to the launch experience curve

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside. **This round introduces external data** (the launch-cost experience curve) — the first round this session to anchor on non-campaign sources; every external number is cited below and carried as a band, not a point.
**Worker:** worktree-115637 session. R183's Revisit: *"the price-decay path has NO campaign anchor (scenario swept openly — a clearing-price-vs-launch-cost-decline round would anchor it)."* This is that round. Post-R187 the relay-vs-monolithic question is settled (monolithic reactor baseline is state-of-record), so the live economic question is no longer *which* architecture but *whether the delivered-water clearing price the mission can charge survives its own multi-decade timeline.*

## The load-bearing claim

ICEBERG sells water at a destination. At any **Earth-accessible** destination (LEO / cislunar), the clearing price is bounded above by the cheapest substitute — **Earth-launched propellant** — whose price rides the launch-cost experience curve. That curve is falling steeply. So the price ICEBERG can charge **decays on the launch curve**, over the mission's own decision-to-delivery timeline (~13 yr round trip; 23.5 yr full paper timeline per R183). This is exactly R183's swept "water-price decay," now anchored.

## External anchors (cited)

- **LEO clearing price, 2025:** Earth launch to LEO ≈ **$3,868/kg** ([PNAS Nexus experience-curve study](https://academic.oup.com/pnasnexus/article/5/7/pgag217/8732400); [Starlust](https://starlust.org/from-thousands-of-dollars-to-less-than-300-per-kgspace-launch-costs-could-plunge-by-2040/)); propellant delivered to LEO ≈ **$4,000/kg**, lunar propellant valued at a 25% discount ≈ **$3,000/kg in LEO** ([Commercial Lunar Propellant Architecture study](https://www.linkedin.com/pulse/commercial-lunar-propellant-architecture-study-business-robert)). Band **$3,000–4,000/kg**, central **$3,500**.
- **Decline rate:** LEO launch **$3,868 (2025) → ~$273/kg (2040)** median; conservative **−45% by 2030 / −75% by 2040**; Citi bull **~$30/kg by 2040** ([Starlust](https://starlust.org/from-thousands-of-dollars-to-less-than-300-per-kgspace-launch-costs-could-plunge-by-2040/); [AEI, "Moore's Law Meet Musk's Law"](https://www.aei.org/articles/moores-law-meet-musks-law-the-underappreciated-story-of-spacex-and-the-stunning-decline-in-launch-costs/)).
- **R183 kill threshold:** 3%/yr price decay alone sinks even the paper-κ relay at the 8% utility hurdle (campaign, `R_waiver_value_consolidation`).

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (the LEO anchor).** The 2025 LEO water/propellant clearing price is **$3,000–4,000/kg** (central $3,500); the independent ISRU-discount cross-check (25% off the $3,868 launch figure) lands at **$2,901 ≈ the band floor**. Falsified if the external anchors are mutually inconsistent by > 2× or fall outside the band.

**H2 [S] (the decline rate, anchored).** The launch-cost experience curve gives a delivered-water price decline of **9–18 %/yr** (scripted: conservative 9.2, median 17.7, geometric-central 12.8; bull 32.4 as an upper outlier) — **3–6× R183's 3%/yr kill threshold** (scripted 3.1–5.9×). Falsified if the anchored rate lands below 6%/yr (≤ 2× the kill threshold) or the bull case is treated as central.

**H3 [S] (the timeline multiplier and the effective rate).** Over the mission's own timeline the substitute price falls by **3.3× (13 yr, conservative) to 63× (23.5 yr, median)**; at the central rate the price at delivery is **5–19 % of its decision-time value**. The **decline rate alone (12.8 %/yr) exceeds both campaign hurdles (8 %, 10 %)**, so the combined effective revenue discount (hurdle + decline ≈ 21–23 %/yr) drives the 23.5-yr revenue discount factor **below 1 %** (scripted 0.76 % at 8 %, 0.47 % at 10 %). Falsified if the combined-rate discount factor exceeds 2 % or the decline alone falls under either hurdle.

**H4 [W] (the surviving niche, and the dilemma).** The only clearing-price regime that does *not* track the collapsing LEO cost is water sold at a **deep-space** destination, where Earth launch carries the full rocket-equation delivery penalty: at Δv {10, 15, 20} km/s (chemical Isp 450 s) the substitute is **9.6× / 29.9× / 93× LEO** (scripted; ~$34 k / $105 k / $325 k per kg). But that market requires outer-system demand absent in the 2032–2050 window and itself gated on cheap launch. **Registered dilemma:** ICEBERG's water is either sold **cheap** (LEO, racing substitute) or **dear** (deep space, no customers) — an economics bet that sits *beneath* the three engineering bets, not beside them. This does **not** falsify the engineering (the locked matrix verdict brackets economics by construction); it prices the market bet. Held if the multipliers land in band and the dilemma's two horns are both quantified.

## Sweep (run.py)

Price-path curves P(T) over rate ∈ [0.03, 0.32] × T ∈ [10, 23.5]; effective-rate discount surface (hurdle ∈ {8, 10 %} × decline); deep-space substitute vs Δv ∈ [10, 20] km/s; the R183-anchor overlay (mark where 3%/yr sits vs the empirical band). Grids span the pre-script's.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/clearing_price.png`), `results/findings.json`, `STUDY.md` with Revisit; orchestrator notes: R183's open parameter is now anchored (design-axes L0-05 / economics axis gains the experience-curve decline band and the "decline > hurdle" finding); the **economics/market bet** is surfaced as a named fourth bet-adjacent risk under the three engineering bets, with the cheap-vs-dear dilemma; a full-cashflow follow-on (R15-rerun lineage) is named, not run. **This round's numbers are externally anchored desk estimates, not a market study** — the bands are the claim.
