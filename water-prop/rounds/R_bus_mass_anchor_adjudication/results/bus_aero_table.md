# Sub-procedure 1 — bus mass × aerocapture commercial-strict closure table

Source: enceladus-r5 R-bus-mass-anchor-sweep, results.json, linear-bag rows only.
Definition: cell passes if feasible AND L0-05 strict AND L0-09 commercial AND reactor-life AND launchable.

## Commercial-strict count by (m_bus, aerocapture credit)

| m_bus (t) | aero = 0 km/s | aero = 10 km/s |
|---|---|---|
| 2.0 | 0 | 9 |
| 5.0 | 0 | 6 |
| 10.0 | 0 | 6 |
| 15.0 | 0 | 4 |

**Reading.**
- aero=0 column is uniformly **zero** across all four bus anchors. The Tsiolkovsky-implied propellant fraction at 25-kilometre-per-second continuous-thrust Δv with 19.6-kilometre-per-second exhaust velocity is 0.72 of total mass; at 200-tonne chunk the propellant required exceeds the chunk's mass at all bus values. Aerocapture is the binding axis. H4 HELD-strong (more pessimistic than the SCOPE's per-Cassini-only prediction).
- At Europa-Clipper-proxy bus (m_bus = 5 t in the existing grid, closest to the 5.5 t basis-of-record): **6 commercial-strict cells at aerocapture credit 10 km/s, 0 at aerocapture credit 0**. H2 anchor 6 cells (from enceladus-r5 shielding sensitivity at Europa-Clipper-medium-shield) is consistent with the 5-t-grid count of 6 within margin.
- Cassini (2 t) gives 9 cells at aerocapture=10; m_bus = 15 t gives 0. The bus-mass axis contributes a 0–9 cell delta at aerocapture=10. The aerocapture-credit axis contributes the entire 9–0 cell delta at any fixed bus. **Aerocapture is dominantly load-bearing**.

## Shielding-sensitivity anchor reproduced from enceladus-r5 §137-143

| Scenario | Commercial-strict cells (of 9 Cassini-anchor cells) |
|---|---|
| cassini_only | 9 |
| cassini_light_shield | 7 |
| cassini_medium_shield | 7 |
| cassini_heavy_shield | 6 |
| europa_clipper_light | 6 |
| europa_clipper_medium | 6 |

**H2 verdict.** At Europa-Clipper-with-shielding (medium shielding) 6 cells survive. Predicted range [5, 9]; observed 6. **H2 HELD**.

**H1 verdict.** Basis-of-record bus mass: **5.5 t** (Europa-Clipper-with-medium-shielding). Brackets: 2 t (Cassini, no shielding — upside) and 15 t (predecessor stale anchor — far-conservative). Project-owner may override; absent override, adopt 5.5 t. **H1 ADOPTED**.
