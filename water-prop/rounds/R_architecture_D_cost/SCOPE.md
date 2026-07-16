# R-architecture-D-cost — scope

**Owner session:** rhea (re-spawn, fifth re-entry)
**Branch:** `iceberg-rhea-2`
**Source:** worker-authored from `.planning/round-queue.md` parallel-work row (enceladus-r5 handoff).

## Question

Costs Architecture D-fission and D-solar-thermal vehicle plus mission opex and outputs marginal-internal-rate-of-return per Architecture-D variant. Architecture D is the **chemical-propulsion-end-to-end** family with a small Saturn-side power plant used purely for inbound electrolysis (never propulsion):

- **D-fission:** Saturn-side fission reactor at the Fission-Surface-Power Phase-1 stretch specific-power target (10 watts-per-kilogram system-level), 150-300 kilowatts-electric class.
- **D-solar-thermal:** Saturn-side solar-thermal-concentrator + solid-oxide-electrolyzer stack at Saturn-Sun L1 halo or high-eccentric Saturn orbit, 150-300 kilowatts-electric useful.

Both variants share the same chemical propulsion stack, vehicle dry mass, and chunk-fed inbound chemistry (specific-impulse 450 seconds, mass-ratio 4.27).

## Why this round is load-bearing

Architecture D is currently priced as a paper hedge in the matrix. Enceladus-r5 round 5 (`R-fission-surface-power-stretch-credibility`) collapsed both D variant posteriors below five percent unconditional — D-fission posterior median 0.78 percent, D-solar-thermal posterior median 2.03 percent. The matrix needs to record whether either D variant clears the sovereign-bond, regulated-utility, or corporate-growth hurdle on per-mission economics, and which D variant dominates on programmatic-risk-adjusted basis.

This round is not "does D close at fission" — that question was resolved by R-chemical-plus-small-reactor (yes, at Fission-Surface-Power-Phase-1-stretch reactor specific-power) and R-fission-surface-power-stretch-credibility (no, the bet has 0.78-percent credibility). This round is the **economic dual** to those engineering closures: assuming D closes engineering, does it clear any commercial-finance hurdle?

## Cross-references

- `R_chemical_plus_small_reactor` — Architecture D delivered-mass-per-mission and round-trip-yr (the 10 closing scenarios — `architecture_D.json`).
- `R_saturn_side_solar_thermal` — D-solar-thermal stack mass at 150-200 kilowatts-electric useful.
- `R_fission_surface_power_stretch_credibility` — D-fission posterior 0.78 percent, D-solar-thermal posterior 2.03 percent (cascade-Monte-Carlo posteriors). Authoritative posteriors for the programmatic-risk overlay.
- `R_reactor_roadmap` — cashflow framework, BEST_CELL and CONOPS_BASE price anchors, ship-cost ladder.
- `R_delivery_irr_curve` — hurdle table (sovereign-bond 4 percent, regulated-utility 8 percent, corporate-growth 10 percent).
- `R_launch_cost_sensitivity` — Starship lifts marginal-internal-rate-of-return by ~2 percentage points.
- `R_variant_B_recovery_paths_economic` (rhea Round 5, this branch) — Variant B per-mission cashflow positive at 32 t delivered, 4 path options for the matrix.

## Deliverables

1. `STUDY.md` — pre-registered numeric predictions for D-fission and D-solar-thermal CapEx, OpEx, per-mission cashflow, marginal-internal-rate-of-return, and programmatic-risk-adjusted expected delivered mass.
2. `run.py` — sweep across launch-cost anchors {Falcon Heavy + assembly, Starship-optimistic, Starship-central, mixed} × water-price anchors {BEST_CELL $10K/kg, CONOPS_BASE $2K/kg} × posterior {D-fission, D-solar-thermal} × stack-mass anchors {optimistic 20 tonnes, central 30 tonnes, pessimistic 50 tonnes}.
3. `results/` — JSON + tables.md.
4. Post-run grading of all sub-claims.
5. Handoff to Saturn at `~/.claude/handoffs/iceberg-rhea-20260515-arch-d-cost.md`.
