---
axis: "Reactor lifetime"
status: open
confidence: high
last_revised: 2026-07-21 (latest+25)
related:
  - "[[05-reactor-power-floor]]"
  - "[[06-reactor-specific-power]]"
  - "[[02-surviving-cell]]"
  - "[[15-per-mission-reliability]]"
---

# Reactor lifetime

## Current

Every viable Architecture-E cell needs **8–12 years of cumulative reactor full-power burn time** (enceladus-r5 R-reactor-lifetime-vs-burn-time `c685c52`, post-processing the R11 grid by adding reactor lifetime ceiling L as a third viability axis alongside specific-power and aerocapture). Required burn-hours: 70,000–105,000 hours. KRUSTY 2018 flight-heritage is **28 hours**. The program's reactor heritage is **3–4 orders of magnitude short** of what any surviving cell needs.

Survival of close-25-yr cells under reactor lifetime ceiling L:

| L (years) | Heritage anchor | Surviving cells |
|---|---|---|
| 5 yr | Brayton flight-rated minimum | only 9–10 W/kg at X ≥ 20 km/s aerocapture-Δv-credit |
| 10 yr | Kilopower design target | ~80 percent of R11 grid survives |
| 15 yr | Effectively non-binding | all R11 close cells survive |
| KRUSTY 28-hr anchor | Sole flown datapoint | **zero** |

This is a third independent viability axis the matrix had not separately tracked. Specific power (axis 06) and aerocapture closure (axis 11) are the prior two; reactor lifetime is the third.

**2026-05-22 latest+18 — STRUCTURALLY ENFORCED IN MISSION_GRAPH FRAMEWORK (titan-4 R-framework-matrix-parity `0eb11a7`):** worker encoded `reactor_lifetime_years` as a first-class param-gated constraint in `water-prop/sims/mission_graph/missions/powerplant_constraints.py` along with the `electric_burn_hours` helper (uses thrust = 2P/v_e; ties burn time to power, not the framework's `electric_thrust_n` param — more physical; documented in code). The constraint computes cumulative full-power burn hours per mission's electric phases and trips when the total exceeds L. Constraint reproduces enceladus-r5 R-reactor-lifetime-vs-burn-time finding at megawatt scale (re-derived from first principles) and corroborates hyperion R-kilopower-scale-up-credibility at 30-kilowatt-electric scale (14-16 yr cumulative burn for 200-tonne chunk at 30 kilowatt-electric is over any plausible ceiling). H1 falls at every L ∈ {5, 10, 15, ∞}. With constraints-ON the 200-tonne closure cell collapses to 0 surviving cells at conservative anchors across the 1-55 kilowatt-electric flyable envelope. **Reactor lifetime is now enforced structurally in the framework rather than by per-round assertion.** 22 new tests pass in `test_reactor_lifetime_constraint.py` + `test_powerplant_mass_floor.py` + `test_visviva_capture.py`. Status held at open / high; the resolution is framework integration, not a numerical change to required-burn-hours.

**2026-07-21 latest+25 — full-power-years is the demonstrable currency (R184 `R_shuttle_reuse_fleet`), and disposal is a solved-in-principle end-of-life line (R190 `R_spent_reactor_disposal`).** R184 made the lifetime axis load-bearing for the *fleet* economics, not just single-mission viability: the reactor is ~60 percent of a fleet's recurring launch mass, and the "immortal reactor" fleet dream needs **L ≥ 40 full-power-years — 4× an unmeasured Kilopower target**. The demonstrable currency of bet #3 is therefore full-power-years, not peak kilowatts; every year of reactor life is directly monetizable in launch-mass terms. R190 closed the *other* end of the lifetime: end-of-life disposal of the activated core is **cheap and Cassini-precedented** (co-orbital deorbit into Saturn 2.78 km/s, or free via one Titan flyby from a staging orbit — note the R186 asymmetry: Titan lowers periapsis for disposal though it cannot raise v∞ for departure), and is **not a binding bet**. But it imposes three design constraints on the reactor subsystem: it must be **separable and independently disposable** (cannot depend on a mothership that may not return), the fleet must **reserve a Titan disposal flyby per spent core**, and — the sharp, unpriced one — the *monolithic* baseline's reactor **returns with the ship and is disposed in cislunar**, an activated fission core arriving in the delivery zone (a launch-licensing and re-entry-safety constraint the campaign has not analyzed). See [[15-per-mission-reliability]].

## Open question

What reactor-program profile (specific power + cumulative full-power lifetime + scope-megawatt-class) is required to restore any surviving cell to the matrix? Best current bound: ≥ 5 W/kg specific power + ≥ 10-year cumulative full-power burn lifetime. Neither in hand. Connects to axis 05 (reactor power floor) and axis 06 (specific power).

Follow-on round candidate: R-reactor-specific-power-program-targets — sweep (specific-power × lifetime) jointly and identify minimum reactor-program target that re-opens any surviving cell at conservative anchors. No SCOPE yet.

## Last touched by

- enceladus-r5 R-reactor-lifetime-vs-burn-time — `c685c52` (2026-05-15 latest+7)
- hyperion R-kilopower-scale-up-credibility — `3529984` (latest+17; lifetime axis independently corroborated at 30 kilowatt-electric)
- titan-4 R-framework-matrix-parity — `0eb11a7` (latest+18; lifetime constraint now first-class in mission_graph framework)

## HISTORY

### 2026-05-15 latest+7 — enceladus-r5 R-reactor-lifetime-vs-burn-time (`c685c52`) — axis created

Round post-processes the R11 grid to add reactor lifetime as a third independent viability axis alongside specific-power and aerocapture-Δv-credit. Computes cumulative full-power burn hours per mission for the surviving cells and grades them against KRUSTY heritage (28 hours), Brayton flight-rated minimum (5 yr), Kilopower design target (10 yr), and an effectively-non-binding ceiling (15 yr).

The KRUSTY result is the load-bearing finding: the only US space-fission reactor ever ground-tested has 28-hour heritage; ICEBERG's surviving Architecture-E cells need 70,000–105,000 hours; the gap is 3–4 orders of magnitude. This is independent of and orthogonal to the specific-power axis (which sits between 7-8 W/kg closure cliff per R-specific-power-cliff, and which KRUSTY also misses at 2.4 W/kg flown vs 7+ W/kg required). The two axes compound: KRUSTY misses both.

The matrix's prior R-power-base-rate framing (0-of-6 US space-fission programs reaching orbit within their originally-stated decade) is *necessary but not sufficient* — even if a US fission reactor does fly within the ICEBERG window, it still must hit 5+ W/kg specific power AND 10+ years cumulative full-power burn life to put any surviving cell in the matrix. That conjunction is a much stiffer bet than orbital flight alone.

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-22 latest+18 — titan-4 R-framework-matrix-parity (`0eb11a7`) — lifetime constraint becomes first-class in mission_graph framework

Worker encoded `reactor_lifetime_years` as a param-gated constraint in `water-prop/sims/mission_graph/missions/powerplant_constraints.py` along with the `electric_burn_hours` helper. The framework now structurally enforces what enceladus-r5 R-reactor-lifetime-vs-burn-time and hyperion R-kilopower-scale-up-credibility found by per-round assertion. With constraints-ON the 200-tonne closure cell collapses to 0 surviving cells at conservative anchors across the 1-55 kilowatt-electric flyable envelope. H1 (lifetime) falls at every L ∈ {5, 10, 15, ∞}. 22 new tests pass in the constraint test suite. Caveat from worker: `electric_burn_hours` uses thrust = 2P/v_e (ties burn time to power, not to the framework's `electric_thrust_n` param); more physical, but lifetime burn-hours are computed at a lower thrust than some phases' own time bookkeeping uses. Documented in `powerplant_constraints.py`. If the convention is changed, lifetime numbers shift but the qualitative collapse does not (mass floor alone kills the conservative-anchor cells).

Status held at open / high; the resolution is framework integration, not a numerical change. The locked-belief constraint now appears in code as well as in matrix prose; downstream rounds can call into the constraint rather than re-implement per-round.

### 2026-05-22 latest+17 — hyperion R-kilopower-scale-up-credibility (`3529984`) — lifetime axis independently corroborated at 30 kilowatt-electric

The kilopower audit on titan-3's 30 kilowatt-electric closure cell finds lifetime falsified independently of the mass and programmatic axes: KRUSTY 28-hour heritage versus ~6-8 year cumulative full-power burn required for the closure cell is 3-4 orders of magnitude short. The result corroborates enceladus-r5 R-reactor-lifetime-vs-burn-time finding at a different power class (the original axis-creation finding was at megawatt scale; this lands at 30 kilowatt-electric and the conclusion holds with the same magnitude gap). Reading: lifetime is an independent viability axis from mass and programmatic, AND it binds at the 30-kilowatt-electric closure cell, NOT only at megawatt. Matrix decision #14 amendment cites this finding as one of two independent reasons (programmatic + lifetime) for the option (b) hold-directive recommendation. No change to required-burn-hours number (still 70,000-105,000 hr / 8-12 yr at the matrix-relevant Architecture-E cells); the kilopower round reports the same gap with KRUSTY anchor reaffirmed.

### 2026-07-21 latest+25 — worktree-115637 R-shuttle-reuse-fleet (`7b9adf6`) + R-spent-reactor-disposal (`6f1ec6b`) — full-power-years as fleet fuel line; end-of-life disposal solved-in-principle with three constraints

R184 made lifetime load-bearing for fleet economics: the reactor is ~60 percent of a fleet's recurring launch mass, and the immortal-reactor fleet dream needs L ≥ 40 full-power-years (4× an unmeasured Kilopower target). Bet #3's demonstrable currency is full-power-years, not peak kilowatts. R190 priced end-of-life disposal of the activated core: cheap (co-orbital deorbit 2.78 km/s; free via one Titan flyby from a staging orbit) and Cassini-precedented — NOT a binding bet — but imposing three constraints: reactor separability + independent disposability; a reserved Titan disposal flyby per spent core (fleet); and the unpriced cislunar activated-reactor delivery constraint (monolithic reactor returns home). The R186 Titan asymmetry is recorded (lowers periapsis for disposal though it cannot raise v∞ for departure). Status held at open / high; required-burn-hours number unchanged, but the fleet framing (full-power-years as fuel) and the disposal constraint set are new. Both round hypotheses HELD.
