# R-h2o2-closed-cycle-power-bridge — chemical energy banking as the no-fission power leg

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed.
**Worker:** worktree-115637 session. Project-owner-directed: "recirculating hydrogen/oxygen burning generator for 10 kW or more — maybe we can close the mission this way."
**Predecessors:** R_hybrid_chemical_power_augmentation (hydrolox-for-propulsion killed at 5,300–10,500 t); R_hybrid_power_generator_exhaust_revisit (zero-hydrolox dominates every corner even with 10× exhaust credit); R_non_fission_baseline (no non-fission architecture closes L0-05 + L0-12; Saturn-side power is the binding gap).

## Framing the concept honestly

A fully closed loop — recirculating the H2 and O2 themselves — is excluded by the second law: combustion consumes the reactants, and electrolyzing the product water back costs more energy than the burn released. The chargeable version of the owner's concept: a **closed-cycle generator** (the working fluid recirculates; the reactants are consumed) whose **product water is retained and joins the propellant budget** — on a water-propelled ship the reactants are pre-paid propellant, not waste. Two plant options: a Rankine turbogenerator (η ≈ 0.25–0.35), or the flown option — **Apollo/Shuttle-class H2/O2 fuel cells** (12 kW flown, ~100 W/kg, η ≈ 0.5–0.6, product water retained by design). The fuel cell IS this concept with flight heritage. The open question is the energy inventory, not the plant.

## Pre-registered hypotheses (bounds at worst grid corners)

**H1 (energetic dominance — chemical energy cannot feed electric propulsion).** For a water thruster at Isp 600–1000 s, total impulse per kilogram of launched H2/O2 delivered via fuel-cell electricity (η_fc 0.6, thruster η 0.6) is at least **3× less** than burning the same kilogram directly in a 450 s chemical engine. Falsified if the direct/via-electricity impulse ratio drops below 3 anywhere on the Isp grid. (Consequence if held: no chemical energy bank powers the spiral or inbound electric legs — the propulsion wall from the predecessor rounds is thermodynamic, not architectural.)

**H2 (bridge sizing — the hotel niche).** For a Saturn-operations bridge carrying hotel + trawl-ops loads only (grid: 5/10/15 kWe × 2/4/6 months), fuel-cell reactant mass runs **2.4–21.5 t**; after crediting product water to the inbound propellant budget, the *net* mass penalty (cryo tankage 20 percent of reactants + plant at 100 W/kg + boil-off 10 percent over the 6-year outbound) lands **under 6 t at every grid point** and under 1.5 t at the 5 kWe × 2 month corner. Falsified if any grid point exceeds 6 t net.

**H3 (storage dominance over batteries).** For discharge durations ≥ 2 months, the H2/O2 bank beats 250 Wh/kg secondary batteries on storage mass by at least **6×** at every grid point. Falsified below 6× anywhere.

**H4 (closure — the honest test).** In the audit sweep, removing reactor power (which the electric-propulsion phases require) leaves **0 closing cells** at the 25 t floor regardless of the bridge — every feasible path in the sweep's closing set uses low-thrust electric legs whose energy a chemical bank cannot supply (per H1). Falsified if any closing path survives with propulsion-phase power deleted. (The known non-fission escape remains L0-05 relaxation to 20–25 years per R_non_fission_baseline — out of scope here, cited for the record.)

If H1–H4 hold: the concept's verdict is a **scoped adoption, not a kill** — the fuel-cell bank is the right answer for a specific job (multi-month Saturn-side hotel power in any low-fission variant, and a demonstrator-mission power system with zero reactor dependence), while mission closure keeps hinging on bet #3 for the propulsion legs.

## Method

Closed form, deterministic. LHV stoichiometric H2/O2 = 13.3 MJ/kg of mix; fuel cell η 0.55 (0.6 for H1's bound), turbine variant η 0.30 reported alongside; plant 100 W/kg (Shuttle PC17-C anchor); cryo tankage 20 percent; boil-off 10 percent of inventory over the outbound. Battery comparator 250 Wh/kg. H4 reprocesses the audit cells (leaf_state.payload_kg) with propulsion-phase power availability zeroed.

## Deliverables

1. `run.py`, `results/h2o2_bridge.png` (bridge net-mass vs duty grid, reactor band overlaid), `results/energy_wall.png` (impulse-per-kg comparison), `results/findings.json`.
2. `STUDY.md` with Revisit and the scoped-adoption recommendation for the orchestrator.
