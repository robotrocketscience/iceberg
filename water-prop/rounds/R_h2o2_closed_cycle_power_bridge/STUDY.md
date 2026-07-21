# R-h2o2-closed-cycle-power-bridge — STUDY

**Round:** R-h2o2-closed-cycle-power-bridge. SCOPE pre-registered 2026-07-20 before `run.py` existed.
**Worker:** worktree-115637 session. Owner question: can a "recirculating" H2/O2 generator at 10+ kWe close the mission without a reactor?

## Hypotheses, tests, results

Computations in `run.py`; numbers in `results/findings.json`; figures `energy_wall.png`, `h2o2_bridge.png`.

### H1 — chemical energy cannot feed electric propulsion — **FALSIFIED at the margin, verdict intact**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| direct-burn ÷ via-electricity impulse per kg, worst grid point | ≥ 3.0 | **2.71** (at Isp 600 s) | **FALSIFIED** |
| same ratio at 800 s / 1000 s | — | 3.62 / 4.51 | — |

**Reading.** The registered "≥ 3× everywhere" bound was set from the 800 s central case and missed the 600 s corner — the same bound-setting error class as the two prior rounds, at a round where the convention was already standing. The architecture verdict is untouched: at every specific impulse on the grid, a kilogram of H2/O2 delivers **more impulse burned directly at 450 s than fed through a fuel cell into the water thruster** (ratio 2.7–4.5). Chemical-powered electric propulsion is energetically self-defeating; the predecessor rounds' 5,300–10,500 t hydrolox walls are the same physics seen from the mass side.

### H2 — the hotel-bridge niche — **FALSIFIED on the cap, corner held**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| net penalty, every grid point | < 6 t | **9.72 t** at 15 kWe × 6 months | **FALSIFIED** |
| net penalty at 5 kWe × 2 months | < 1.5 t | **1.11 t** | (condition held) |

**Reading.** The SCOPE's own reactant table carried an arithmetic slip at the big corner (21.5 t written where the declared parameters give 31.9 t), so the 6 t cap was unsatisfiable as registered. The corrected picture: net of the product-water credit, the bridge costs **1.1–3.4 t at duty points up to ~10 kWe × 2 months or 5 kWe × 4 months — inside or near the Kilopower-class reactor band (1.5–3 t)** — and grows to ~10 t at 15 kWe × 6 months. The niche is real but narrow: short-duty, hotel-scale.

### H3 — beats batteries — **HELD**

Worst advantage over 250 Wh/kg secondary batteries: **8.1×** (bound ≥ 6×). For multi-month discharge, chemical banking dominates electrochemical storage at every grid point.

### H4 — closure is untouched — **HELD**

Of **1,061 closing paths** across the audit sweep's cells at the 25 t floor, **zero** avoid electric-propulsion legs. Deleting propulsion-phase power (what removing the reactor does, per H1) closes nothing. The chemical bank can displace the reactor for hotel loads; it cannot displace it for the mission. The recorded non-fission escape remains L0-05 relaxation to 20–25 years (R_non_fission_baseline), unaffected by this round.

## Revisit (mandatory)

Two falsifications, both mine rather than the concept's: a central-case bound at H1 and an arithmetic slip inside the SCOPE's own table at H2. The worst-corner convention now has three rounds of teeth marks; the sharpened rule from R-harvest-draw-symmetrization ("propagate the worst corner through derived quantities") would have caught both, and this round wrote its bounds before that STUDY landed — no excuse next time, the rule is standing. Substantively: the owner's concept survives in scoped form. The plant is flight-proven (Apollo/Shuttle H2/O2 fuel cells: kW-class, ~100 W/kg, product water retained by design — the "closed system that keeps its mass" is literally how Shuttle made drinking water). What fails is the energy inventory for propulsion, by thermodynamic argument (H1) and by closure count (H4), consistent with all three predecessor rounds.

## Cross-learning

- **Scoped adoption:** H2/O2 fuel-cell energy bank is the recommended baseline for (a) **demonstrator-mission power** (Gates A/B fly at kW-scale for days-to-weeks with zero reactor dependence — directly strengthens the staged-gates story), and (b) **Saturn-ops hotel bridge** in any variant that idles or sheds the reactor during ring operations. Not adoptable as propulsion power at any scale.
- **Negative for** "maybe we can close the mission this way": closure remains gated by bet #3 (flight fission) or by L0-05 relaxation. Fourth independent confirmation.
- **Design note for the orchestrator:** the demonstrator power-system line in the campaign gantt (Gate A/B flights) can drop its unstated power assumption and name the fuel-cell bank explicitly; heritage citation is Shuttle PC17-C class.
- **Follow-on candidates:** regenerative variant (solar electrolysis at ≤ 3 AU recharging the bank) for the L0-05-relaxed solar architecture; peak-power shaving during capture ops (days-scale, where the bank's 8× battery advantage compounds).
