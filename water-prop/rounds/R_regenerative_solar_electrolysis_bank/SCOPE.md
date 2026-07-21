# R-regenerative-solar-electrolysis-bank — charge the H2/O2 bank from the sun on the way out

**Status:** SCOPE pre-registered 2026-07-20, before `run.py` was written or executed.
**Worker:** worktree-115637 session. Follow-on named in R-h2o2-closed-cycle-power-bridge's cross-learning; owner-directed.
**Predecessors:** R_h2o2_closed_cycle_power_bridge (bank scoped-adopted for hotel/demonstrator power; launched-reactant variant); R_hybrid_solar_augmentation (solar augment adopted at ≤ 3 AU); R_non_fission_baseline (Saturn-side power is the binding non-fission gap); derivation-thermal-isp-ceilings (multi-year H2 storage flagged as killer — this round prices that flag).

## Concept

Launch water, not reactants. During the outbound leg inside ~3 AU (about 1.25 years of the Hohmann transfer), solar arrays drive an electrolyzer that splits water into H2/O2, banking chemical energy for Saturn operations where solar flux is 1.1 percent of Earth's. At Saturn the fuel cell discharges the bank; product water returns to the propellant inventory. Fully regenerative in the only sense thermodynamics allows: the energy is harvested sunlight, the mass cycles water → gases → water → thrust.

The suspected load-bearing element is not the array or the electrolyzer — it is **keeping liquid hydrogen liquid for the ~4.9 years of cruise beyond 3 AU**. Zero-boil-off cryocooling costs continuous electric power precisely when the sun is fading; a poorly insulated bank could consume itself before arrival.

## Pre-registered hypotheses (worst corners propagated through derived quantities)

Duty grid as round 171 (5/10/15 kWe × 2/4/6 months Saturn-side); burst grid (50/100 kWe × 1/3 days). Chain: array 120 W/kg at 1 AU; electrolyzer η 0.66 (charge), 1 kW/kg; fuel cell η 0.55, 100 W/kg; tanks 20 percent of reactant mass; Hohmann r(t) by Kepler solve (a = 5.27 astronomical units, e = 0.810).

**H1 (harvest is cheap).** The worst duty corner (15 kWe × 6 months → 642 GJ charge energy) is collected inside 3 AU by an array rated ≤ **60 kW at 1 AU** with array + electrolyzer mass ≤ **1.0 t**. Falsified if either is exceeded.

**H2a (warm-tier cryo self-consumption kills the bank).** At warm-tier insulation (10 W of heat leak per tonne of liquid hydrogen; 150 W of cryocooler input per W lifted at 20 K), the cruise-integrated zero-boil-off electric demand is at least **1.5× the bank's entire chemical inventory** at every grid point — the bank eats itself. Falsified if the ratio drops below 1.5 anywhere.

**H2b (cold-tier design closes, and the charge array carries it).** At cold-tier insulation (sunshield + deep multilayer blanket, 1.5 W per tonne, 80 W per W lifted from a 40 K precooled stage), the already-sized charge array supplies the cryocooler all the way to Saturn arrival, and bank self-drain is ≤ **5 percent** of chemical inventory at every grid point. Falsified if drain exceeds 5 percent anywhere.

**H3 (mass ranking).** Total regenerative system mass (tanks + plants + array + cooler; cycled water credited as propellant per round 171):
  (a) beats a direct-Saturn solar array (120 W/kg at 1 AU scaled by 1/90 flux and a 1.5× low-intensity-low-temperature derate) by ≥ **2×** at every continuous duty point, and
  (b) sits at or below the Kilopower-class band (≤ 3 t) for discharge energies ≤ 100 GJ, exceeding 3 t above 140 GJ.
Falsified by any grid point violating (a) or the (b) thresholds.

**H4 (burst niche).** For capture-ops burst loads (50/100 kWe × 1/3 days), the bank beats a 250 Wh/kg battery bank by ≥ **5×** and direct-Saturn solar by ≥ **10×** on mass at every burst point. Falsified below either factor anywhere.

**H5 (closure, by citation).** Round 171 H4 stands: no propulsion-leg power, no closure change. This round adds no closure re-test; its adoption target is the L0-05-relaxed non-fission variant and the reactor-carrying baseline's Saturn-ops resilience.

## Deliverables

1. `run.py` (Kepler harvest integral, ZBO ledger both tiers, mass rollup, comparators), `results/regen_bank_mass.png`, `results/zbo_ledger.png`, `results/findings.json`.
2. `STUDY.md` with Revisit; adoption recommendation for the orchestrator.
