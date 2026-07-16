# Citation index — R-kilopower-scale-up-credibility

Per SCOPE out-of-scope guard #1 ("Do NOT re-litigate the locked-memory findings 1–4"), this round anchors against user-locked beliefs and prior campaign rounds rather than independently re-fetching primary documents. The evidence chain:

## User-locked beliefs (R-power-wonder, May 2026) — primary sources attributed within each belief
1. **40 W/kg is paper-aspirational at TRL 2; flown RTGs ~5.3 W/kg; KRUSTY ~2.4 W/kg system-level.** Primary: NASA Glenn / Los Alamos KRUSTY 2018 ground test (Gibson, McClure et al.); National Academies 2021 Space Nuclear Propulsion report.
2. **0-of-6 base rate of United States space-fission programs reaching orbit since SNAP-10A (1965).** SP-100, Project Timberwind, Prometheus/JIMO, DARPA DRACO, Kilopower-flight, Fission Surface Power. ~$1.7B post-SNAP, zero orbital outcomes.
3. **Fission Surface Power Phase 2 NOT awarded as of May 2026.** Phase-1 awards June 2022 (Lockheed Martin, Westinghouse, IX JV, $5M each, 40 kWe); contracts extended Jan 2025; Aug 4 2025 Duffy directive (100 kWe, Q1 FY2030 intent); Aug 29 2025 draft Announcement for Partnership Proposals; FY2026 budget zeroed NEP/NTP lines; DARPA DRACO cancelled May 30 2025.
4. **At megawatt scale radiators are 40–55% of system mass.** National Academies 2021; NASA MARVL studies. (Not load-bearing here — 30 kWe radiator mass is small.)

## Prior campaign rounds used as input
- **titan-3 R-chunk-size-pareto (`1997a51`)** — closure cell + `m_dry`/`evaluate` formulas (copied verbatim into this round's `run.py`).
- **hyperion R-power-bayesian-update** — three-prior bracket P(United States fission orbit by 2035): uniform 8.9%, Jeffreys 4.9%, skeptical 2.9%. Used as the unconditional programmatic prior.
- **enceladus-r5 R-arch-E-specific-power-flown-anchored (`62f7079`)** — 0/60 cells close at 2.4 W/kg under Architecture E (500–1000 kWe). Cross-checked: no contradiction; reactor mass differs 17× by power class.
- **enceladus-r5 R-reactor-lifetime-vs-burn-time (`c685c52`)** — KRUSTY 28-hr flown vs ~6–12-yr cumulative-burn need; Kilopower 10-yr life is a target. Anchors the `p_life = 0.40` conditional.

## Methodology lessons applied
- Lesson 1 / 5 (pessimistic-default; two-bucket bias): H2/H3 pre-registered pessimistic, came back less-pessimistic.
- Lesson 7 (inverted): conditional factors set charitably (upper-bound) to show even the generous case is sub-threshold.
- Lesson 11 (robustness-by-magnitude): decision-#14 verdict robust because the programmatic floor is far below threshold, not by cancellation.
- Lesson 12 (prospective vs historical scope distribution): `p_power = 0.60` anchored on prospective funded-program scope.
