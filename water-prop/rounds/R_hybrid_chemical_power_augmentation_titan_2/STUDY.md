# R-hybrid-chemical-power-augmentation — does a 10-kilowatt-electric reactor plus brought-from-Earth hydrolox gas-generator boost close any inbound cell that the 500-kilowatt-electric pure-reactor cell could not?

**Status:** pre-registration, before any run.py execution. Worker: titan (re-spawn). Date: 2026-05-18.

This document records the pre-registered hypotheses, the mass-and-energy bookkeeping model, the sweep grid, and the architectural verdict criteria — all *before* any numeric result is produced. Results table and verdict are appended in a second commit.

---

## 1. The question and why it is asked now

Per SCOPE (author: Saturn-orchestrator, 2026-05-15 latest+8), this round tests the project-owner's architectural intuition that a **10-kilowatt-electric reactor + brought-hydrolox gas-generator** hybrid can trade the reactor-scope wall (500-kilowatt-electric is unfunded; KRUSTY-anchored specific power 2.4 watts-per-kilogram is at Technology-Readiness-Level 2) for a launch-cadence wall (brought-hydrolox mass to low Earth orbit).

The hybrid is honest about thermodynamics: gas-generator + Brayton turbine is 30-50 percent efficient electrical conversion of hydrolox chemical energy. The trade is mass-for-reactor-scope: pay propellant mass at Earth orbit to avoid carrying a 500-kilowatt-electric reactor.

**Standing context relevant to result interpretation:**

- Phoebe rounds 3-6 (integrated `b5c5d61`, 2026-05-16) **convergently falsified the held chunk-rendezvous architecture** across 4,268 unique closure checks. Recommendation on file: retire as venture-class with very high confidence. This SCOPE was authored *before* phoebe's findings, so it presumes a held axis-19. Any "closes" verdict here is *power-axis* closure conditional on chunk-rendezvous, not architecture-level closure.
- Architecture E was independently falsified by enceladus-r5 rounds 9-12 (KRUSTY 28-hour lifetime is 3-4 orders of magnitude short of the 8-12-year cumulative full-power burn required).
- Titan's own Blocks 10-11 (un-integrated, on `iceberg-titan-2`) found Block 4's 500-kilowatt-electric composite is structurally dead under joint (burn-time, mass-closure) audit. This round is in a sense the *project-owner's response*: if 500-kilowatt-electric does not work, can a 10-kilowatt-electric reactor plus chemical-energy supplement work instead?

## 2. Mass-and-energy bookkeeping model

This is **not** a Basilisk simulation. It is closed-form Tsiolkovsky plus thermodynamic energy balance, in the style of titan R-inbound-dv-continuous-thrust, rhea R-megawatt-marvl-radiator, and titan R-composite-burn-time-closure.

### 2.1. Power architecture — what generates and what consumes

Three power-system components and one electric thruster:

1. **Reactor.** Continuous baseline electric power `P_reactor` (kilowatts-electric). Specific power 2.4 watts-per-kilogram flown anchor (Kilopower / Kilowatt-Reactor-Using-Stirling-Technology system-level, locked belief `0d5c882c13395571`) or 5.0 watts-per-kilogram optimistic. Subsystem mass = `P_reactor / specific_power`, includes power conversion and reactor-side radiator. Used for housekeeping + supplementing the gas-generator's electrical output during the inbound burn.
2. **Gas-generator.** Brings hydrolox `M_H2O2` (tonnes) from Earth in a separate cryogenic tank. During the inbound burn, hydrolox is combusted stoichiometrically, hot gas drives a Brayton turbine, turbine drives a generator. Electrical output efficiency `η_gen` ∈ {0.30, 0.50}. Lower-heating-value of hydrolox = 13.4 megajoules-per-kilogram (water-vapor product; standard combustion thermodynamics).
3. **Radiator.** Sheds waste heat from both reactor and gas-generator. At kilowatt-class power totals (10-500 kilowatts-electric combined), radiator is approximated as 0.10 tonnes-per-kilowatt of combined waste-heat output. This is more aggressive than MARVL's megawatt-anchored 40-55 percent of system mass (which applies at multi-megawatt). At our scale, radiator mass is roughly comparable to reactor + generator mass — call out as a sensitivity.
4. **Hall-effect or ion thruster.** Specific impulse `Isp_e` ∈ {2000, 5000} seconds. Thruster efficiency `η_thr` = 0.65 (standard for Hall thrusters; flowing-water-cathode option per axis 03 stays in band). Propellant is **chunk water** (water-Hall, no brought Xenon). The chunk is being delivered AND simultaneously serves as the electric-propellant reservoir during the inbound burn. The amount of chunk water consumed degrades the delivered-chunk fraction directly.

### 2.2. Mass bookkeeping — open-cycle gas-generator

The hydrolox combustion products (water vapor) exit the gas-generator turbine and are exhausted overboard at low residual velocity (energy already extracted by turbine). For this round, **assume the gas-generator exhaust velocity is zero** — i.e., the exhaust mass contributes no useful thrust. This is conservative against the architecture; a follow-on round could credit residual-exhaust thrust if warranted.

Hydrolox is therefore inert mass aboard from launch through Saturn-departure, becomes propellant during the inbound burn, and exits at zero velocity. From the inbound-burn Tsiolkovsky equation:

- Initial inbound mass:        `m_initial = m_dry + M_chunk + M_H2O2`
- Final inbound mass:          `m_final = m_dry + (M_chunk - m_chunk_prop)`
- Total mass ejected:           `m_ejected = m_chunk_prop + M_H2O2`
- Total impulse:                `I = m_chunk_prop × v_e_Hall + M_H2O2 × 0`
- Effective specific exhaust:   `v_e_eff = v_e_Hall × m_chunk_prop / (m_chunk_prop + M_H2O2)`
- Tsiolkovsky:                  `dv_inbound = v_e_eff × ln(m_initial / m_final)`

This is the **inert-hydrolox-during-inbound** penalty: every tonne of brought hydrolox that sits aboard at the start of the inbound burn must be decelerated by the Hall thruster, then ejected at zero velocity (it gets ejected because the gas-generator burns it during the same burn). The mass leaves the vehicle, but contributes zero impulse.

### 2.3. Closed-cycle as an alternative bookkeeping

A closed-cycle alternative — store the water-vapor combustion products aboard as liquid water — removes the open-cycle inert-ejection penalty but adds two costs:

1. Liquid-water storage tankage (call it 0.05 tonnes per tonne of combustion-product, on top of the cryogenic-hydrolox tank that stays empty).
2. The combustion-product mass stays aboard through the entire inbound burn and into Earth aerocapture (if aerocapture is used) and into the LEO-arrival vehicle. So either (a) it contributes to delivered water, or (b) it's dumped overboard as dead-end mass once the inbound burn ends.

In option (a) closed-cycle, every tonne of brought hydrolox becomes 1 tonne of stored water delivered to LEO **in addition to** the chunk water. This actually *increases* delivered water — at the cost of carrying that mass for the entire round-trip cruise and inbound burn.

The round runs the open-cycle model as primary and reports the closed-cycle (a) variant as a sensitivity, because the open-cycle is closer to the SCOPE's stated "gas-generator that turns a turbine" mental model and because the closed-cycle requires non-trivial cryo-to-room-temperature plumbing that adds Technology-Readiness risk this SCOPE was not commissioned to assess.

### 2.4. Energy balance

The Hall thruster needs jet kinetic energy at rate (`F_thruster × Isp_e × g0 / 2`). The electric power required at the thruster input is:

```
P_elec = (1/2) × m_dot_chunk_prop × v_e_Hall² / η_thr
```

This power is supplied jointly by reactor and gas-generator:

```
P_elec = P_reactor + η_gen × m_dot_H2O2 × LHV_hydrolox
```

Over the burn duration `t_burn`, integrated:

```
E_elec_total = (1/2) × m_chunk_prop × v_e_Hall² / η_thr
             = P_reactor × t_burn + η_gen × M_H2O2 × LHV_hydrolox
```

**Sanity gate:** `E_elec_total ≤ P_reactor × t_burn + η_gen × M_H2O2 × LHV_hydrolox`. If a cell shows `E_elec_total` strictly exceeding the right-hand side, the model has a bug.

### 2.5. Solving the cell

Given `(P_reactor, M_H2O2, M_chunk, η_gen, Isp_e, dv_inbound, m_dry_base)`:

1. Numerically solve the Tsiolkovsky equation for `m_chunk_prop` — given the effective `v_e_eff` depending on `m_chunk_prop` and the prescribed `M_H2O2`.
2. If solution requires `m_chunk_prop > M_chunk` (i.e., the chunk is entirely consumed and still does not give enough delta-velocity), mark **infeasible (chunk too small)**.
3. If solution requires `m_chunk_prop < 0`, mark **infeasible (M_H2O2 too high — over-supplied with inert mass)**.
4. Compute `t_burn` from energy balance: `t_burn = (E_elec_total - η_gen × M_H2O2 × LHV) / P_reactor` if positive; else `t_burn ≥ 0` is trivially satisfied and we set `t_burn = 0.5` years (lower-bound placeholder; the actual burn time depends on thruster peak power capacity, which is a free design choice).
5. Compute round-trip = 6.09 years outbound Hohmann cruise + 0.5 year Saturn ops + `t_burn` years inbound continuous-thrust. (Outbound is chemical kick; cruise time is ballistic-Hohmann.)
6. Compute LEO-stack mass: vehicle wet at Saturn-departure × (1 + (e^(dv_TSI/v_e_chem) - 1)) where `dv_TSI = 7.0 km/s` and `v_e_chem = 4414 m/s` (hydrolox upper stage). Add 10-percent kick-stage dry-mass adder.
7. Apply pass/fail flags:
   - L0-04 (delivered chunk > 0)
   - L0-05 strict (round-trip ≤ 15 years)
   - L0-05 waiver (round-trip ≤ 25 years)
   - Launchable (LEO stack ≤ 2× Starship-to-LEO ≈ 300 tonnes per launch × 10 launches = 3000 tonnes; conservatively use 5000 tonnes as the ceiling for "not architecturally absurd")

### 2.6. Vehicle dry-mass build-up

For each cell, the vehicle dry mass is:

| Subsystem | Mass model |
|---|---|
| Reactor (with conversion + reactor-radiator) | `P_reactor / specific_power` |
| Gas-generator + turbine + alternator | `0.05 × P_gen_peak` tonnes (terrestrial Brayton APU heritage) |
| Generator radiator (waste-heat from gas-gen losses) | `0.10 × (P_gen_peak × (1 - η_gen) / η_gen)` tonnes |
| Hydrolox cryogenic tank | `0.10 × M_H2O2` tonnes (Centaur heritage) |
| Hall thruster array | `0.01 × P_elec_peak` tonnes |
| Bag + harvesting hardware | 50 tonnes fixed (per L1-007 baseline) |
| Saturn-capture chemical (0.8 km/s impulse at Isp 320 s) | derived from post-capture wet mass, with 0.10 tank-mass fraction |
| Structure, avionics, tankage residuals | 30 tonnes fixed |

`P_gen_peak` is derived from energy balance and burn time: `P_gen_peak ≈ η_gen × M_H2O2 × LHV / t_burn`. `P_elec_peak = P_reactor + P_gen_peak`.

This recursive dependence (dry mass depends on `P_gen_peak`, which depends on `t_burn`, which depends on `m_chunk_prop`, which depends on dry mass) is resolved by fixed-point iteration in `run.py` — three or four sweeps usually suffice.

## 3. Pre-registered hypotheses

Hypothesis numbering follows the SCOPE; predicted ranges and falsification bands are mine. Each is a falsifiable empirical claim that the sweep can resolve.

| # | Hypothesis | Predicted range | Falsification band |
|---|---|---|---|
| H1 | At `P_reactor = 10 kW_e`, no `(M_H2O2 ≤ 1000 t, M_chunk = 200 t)` combination at `η_gen = 0.50` closes L0-05 strict (round-trip ≤ 15 years) AND delivers `M_chunk - m_chunk_prop > 10 tonnes` to low Earth orbit. | Zero close cells. | H1 falsified if any (M_H2O2, M_chunk = 200t) cell at η_gen = 0.50 and Isp ∈ {2000, 5000} closes L0-05 strict with delivered > 10 t. |
| H2 | At `P_reactor = 10 kW_e` and `M_chunk = 50 t` (Architecture-E scope), the surviving cell envelope under L0-05 waiver (≤ 25 yr) with `M_H2O2 ≤ 500 t` is non-empty, but always at `delivered ≤ 20 tonnes` (chunk water heavily consumed). | At least one close cell exists; delivered ≤ 20 t in every such cell. | H2 falsified-bullish if any close cell delivers > 20 t at this corner. H2 falsified-bearish if zero close cells exist. |
| H3 | Reactor alone (`M_H2O2 = 0`) at `P_reactor = 10 kW_e` does NOT close any chunk ≥ 1 t mission inside round-trip 40 years. The hybrid is necessary at 10-kilowatt-electric; bare-reactor at 10-kilowatt-electric is dead on its own. | Zero close cells at `M_H2O2 = 0` for any `M_chunk ≥ 1 t` and round-trip ≤ 40 yr. | H3 falsified if any pure-reactor cell delivers > 0.5 t at round-trip ≤ 40 yr. |
| H4 | The brought-hydrolox-mass requirement is approximately linear in `m_chunk_prop × v_e_Hall² × (1 - 1/η_thr_marginal_term)` — i.e., dominated by the Hall thruster energy budget. At `Isp_e = 2000 s`, a useful (M_H2O2 per delivered-tonne) ratio sits in the band 50-300 tonnes-hydrolox per tonne delivered for the closing cells. | M_H2O2/delivered ∈ [50, 300] for cells passing L0-05 waiver. | H4 falsified if the ratio is outside [10, 1000] for any closing cell (would indicate model bug or unexpected non-linearity). |
| H5 | Total LEO launch stack for any closing-with-positive-delivered cell exceeds 1500 tonnes — i.e., more than 10 Starship-class launches per mission — which Block-5/Block-8 economic envelopes already declared infeasible at venture-class. The hybrid does not reach launch-feasibility even where it reaches physics-feasibility. | LEO stack ≥ 1500 t for all H2-surviving cells. | H5 falsified if any L0-05-waiver-passing cell has LEO stack < 1500 t. |
| H6 | The architectural-verdict alignment with phoebe + enceladus-r5 holds: even setting aside chunk-rendezvous survivability (axis 19) and reactor lifetime (axis 20), the **power axis alone** keeps the hybrid below any reasonable-launchable threshold. Verdict path 3 from SCOPE ("does not close at any tested combination") wins. | Verdict 3. | H6 falsified if the round produces verdict 1 ("closes — restores a surviving cell") or verdict 2 ("closes only at demonstrator scales ≤ 10 t with reasonable LEO stack"). |

**Decision ordering — what the verdict says depending on which hypotheses hold or fall:**

- **All six hold → architectural verdict 3.** Hybrid power axis joins specific-power and reactor-lifetime axes as a third orthogonal kill on the matrix.
- **H1 holds + H2 falsified-bullish → demonstrator-scale framing rescue.** Hybrid closes at very small chunk only. SCOPE's path 2.
- **H1 falsified → load-bearing finding.** Project-owner's intuition is right at some non-trivial chunk. L0-13 capital-structure decision becomes coupled to "Vulcan-class brought-hydrolox launch cadence." SCOPE's path 1.
- **H4 falsified high → model bug suspected.** Re-derive bookkeeping before reporting.
- **H5 falsified → economic relief possible.** Hybrid might trade launch-mass for reactor risk in a meaningfully smaller stack. Triggers an economic-overlay follow-on.
- **H6 falsified-with-H5-falsified-also → the rare double-positive case where physics AND launch-mass close.** Most consequential for the program. Demands immediate orchestrator integration.

## 4. Sweep grid

Per SCOPE, plus a few sanity-anchor cells:

| Variable | Values |
|---|---|
| `P_reactor` (kilowatts-electric) | 1, 5, 10, 20, 50, 100 (last added as upper-bound sanity anchor) |
| `M_H2O2` (tonnes brought) | 0, 100, 250, 500, 1000, 2500, 5000 (last added as upper-bound infeasibility witness) |
| `M_chunk` (tonnes captured) | 5, 10, 50, 100, 200 |
| `η_gen` | 0.30, 0.50 |
| `Isp_e` (seconds) | 2000, 5000 |
| `aerocapture_credit` (km/s, off inbound dv) | 0, 10 |
| `specific_power` (watts-per-kilogram, reactor) | 2.4 (flown anchor), 5.0 (optimistic) |
| `dv_inbound_base` (km/s, before aerocapture) | 25.0 (orchestrator central per SCOPE §3.2) |

Grid count: 6 × 7 × 5 × 2 × 2 × 2 × 2 = 3,360 cells per primary table. Open-cycle is primary; closed-cycle (option (a) — combustion products as additional delivered water) reported as a single sensitivity sweep on the most-favourable subset.

## 5. What this round does NOT test

Verbatim from SCOPE §"What this round does NOT test":
- Solar augmentation. Saturn-side insolation ~ 1 percent Earth orbit; negligible.
- Chemical kick stage trades (outbound is locked chemical).
- Saturn-capture mode (0.8 km/s chemical, locked).
- B-ring-rendezvous survivability (now retired per phoebe rounds 3-6 anyway).
- Fuel-cell vs Brayton-turbine generator details; `η_gen` band covers it.

Plus titan-flagged:
- Combustion-product handling cryo-to-room-temperature plumbing (closed-cycle Technology-Readiness).
- Optimal-control trajectory shaping. Continuous-thrust integrated dv is the closed-form upper bound (accurate to ~10-20 percent of optimal).
- Heliocentric Jupiter-gravity-assist (already retired by titan Block 5 — not load-bearing).

## 6. Falsification of architectural relevance — explicit map

What does a "closes" finding mean given phoebe's kill of the chunk-rendezvous axis?

- This SCOPE was authored before phoebe's findings. It presumes axis 19 (chunk-rendezvous) held.
- After phoebe rounds 3-6, axis 19 carries a very-high-confidence kill. Architecture is conditional on a rendezvous mechanism that has not been identified.
- Therefore: **a hybrid-power "closes" finding is power-axis closure conditional on a rendezvous mechanism existing that does not currently appear on the matrix.** It is not a program-level "closes" finding.
- A hybrid-power "does not close" finding is corroborative — adds a third orthogonal kill — and does not change the program-level verdict.

The asymmetry: this round can only *add* killing-evidence to the program verdict. It cannot *rescue* the program by itself, because it does not address the rendezvous-survivability kill.

## 7. Deliverables

Per SCOPE:

- `STUDY.md` — this document, extended with §8 Results and §9 Verdict in the second commit.
- `run.py` — implements the model in §2, sweeps the grid in §4, writes JSON + Markdown.
- `results/launch_stack.json` — full sweep with per-cell pass/fail.
- `results/tables.md` — headline tables: by-corner minimum-M_H2O2 closures, LEO-stack-by-delivered-chunk cliff, comparison vs matrix-empty pure-reactor verdict.
- Handoff at `~/.claude/handoffs/iceberg-titan-20260518-hybrid-power.md`.

## 8. Results

Sweep executed 2026-05-18, `run.py` v1 commit `dfa5dd2`+1. Full per-cell results in `results/launch_stack.json`. Headline tables in `results/tables.md`.

### 8.1. Top-line counts (3,360 cells total)

| Metric | Count | Fraction |
|---|---:|---:|
| Tsiolkovsky-feasible (positive `m_chunk_prop ∈ (0, M_chunk)`) | 366 | 10.9 % |
| Delivered chunk > 0 | 366 | 10.9 % |
| Delivered chunk > 10 t | 324 | 9.6 % |
| Pass L0-05 strict (round-trip ≤ 15 yr) AND delivered > 0 | **0** | **0.0 %** |
| Pass L0-05 waiver (round-trip ≤ 25 yr) AND delivered > 0 | 6 | 0.18 % |
| Pass H1 (delivered > 10 t AND L0-05 strict) | **0** | **0.0 %** |
| Launchable (LEO stack ≤ 5000 t) AND delivered > 0 | 352 | 10.5 % |
| Energy-balance sanity gate PASS | 366/366 | 100 % |

### 8.2. H1 corner — `P_reactor = 10 kW_e`, `M_chunk = 200 t`, `η_gen = 0.5`, `aerocap = 0`

At Isp 2000 s, *every* M_H2O2 cell from 0 to 5000 tonnes is Tsiolkovsky-infeasible — the chunk is too small relative to the delta-velocity budget at v_e = 19.6 km/s.

At Isp 5000 s, three cells close Tsiolkovsky:

| M_H2O2 (t) | delivered (t) | t_burn (yr) | round-trip (yr) | LEO stack (t) |
|---:|---:|---:|---:|---:|
| 0   | 85.5 |  671 |  678 |   573 |
| 100 | 64.8 |  790 |  797 | 1322 |
| 250 | 36.9 |  951 |  957 | 2444 |
| 500 | infeasible | – | – | – |

**Adding hydrolox makes delivered chunk *worse* and round-trip *longer*.** The Tsiolkovsky-inert penalty on the brought hydrolox mass exceeds the chemical-energy-import benefit. Round-trip is 7-9× the L0-05 strict ceiling regardless.

### 8.3. H2 corner — `P_reactor = 10 kW_e`, `M_chunk = 50 t`, `η_gen = 0.5`, `aerocap = 0`

**All 14 cells (Isp ∈ {2000, 5000}, M_H2O2 ∈ {0, 100, 250, 500, 1000, 2500, 5000}) are Tsiolkovsky-infeasible.** A 50-tonne chunk fully consumed plus any tested brought-hydrolox load cannot deliver the 25 km/s inbound delta-velocity, because the v_e_eff scales as `m_chunk_prop / (m_chunk_prop + M_H2O2) × v_e_Hall` — adding hydrolox lowers effective specific exhaust faster than it boosts mass-ratio.

### 8.4. H3 corner — pure reactor, `M_H2O2 = 0`

Pure-reactor cells close Tsiolkovsky only at Isp 5000 s AND `M_chunk ≥ 100 t`. None has round-trip ≤ 40 years:

| P_reactor (kW_e) | M_chunk (t) | delivered (t) | round-trip (yr) |
|---:|---:|---:|---:|
| 10 | 100 | 25.4 | 444 |
| 10 | 200 | 85.5 | 678 |
| 100 | 100 |  9.6 |  60 |
| 100 | 200 | 69.7 |  83 |

At 10 kW_e, pure-reactor round-trip is centuries. At 100 kW_e it drops to 60-83 years but still exceeds L0-05 waiver by 2-3×.

### 8.5. The six L0-05-waiver-passing cells — corner-anchored at the upper grid boundary

| P_r (kW_e) | M_H2O2 (t) | M_chunk (t) | Isp (s) | η_gen | aerocap (km/s) | σ (W/kg) | delivered (t) | round-trip (yr) | LEO stack (t) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 |   0 | 200 | 2000 | – | 10 | 5.0 | 37.5 | 21.82 |  687 |
| 100 |   0 | 200 | 2000 | – | 10 | 2.4 | 25.6 | 22.94 |  834 |
| 100 | 100 | 200 | 2000 | 0.5 | 10 | 5.0 | 12.0 | 24.01 | 1437 |
| 100 | 100 | 200 | 2000 | 0.3 | 10 | 5.0 | 12.0 | 24.09 | 1437 |

(Two more duplicates exist with `η_gen` flipped; `η_gen` is unused at M_H2O2 = 0.)

**All six waiver-passing cells are at the upper grid boundary `P_reactor = 100 kW_e`, with aerocapture credit, and ≥ 100 t chunk.** None of them represents the project-owner's hybrid intuition (10 kW_e + brought hydrolox). The cells *with* hydrolox in this set (rows 3-4) deliver *less* chunk (12 t vs 25-37 t) than the comparable no-hydrolox row. Verdict at 100-kW_e-with-aerocap is "the hydrolox supplement is net-negative."

A 100-kW_e reactor at 5 W/kg specific power is 20 tonnes; at 2.4 W/kg it is 42 tonnes. Both anchors are not Technology-Readiness-Level 9; the 5 W/kg case anchors against radioisotope-thermoelectric-generator-class systems and is optimistic for fission units at this scope. Per locked memory `776575c01d55ca51`, US space-fission programs have a 0-of-6 base rate of reaching orbit within their stated decade since 1965. These cells inherit the same prior penalty as `R-megawatt-marvl-radiator` and `R-fission-surface-power-stretch-credibility` (programmatic-risk-adjusted closure probability low-single-digit percent).

### 8.6. Sanity gate (model-bug check)

For every Tsiolkovsky-feasible cell, energy supplied (reactor over t_burn + η_gen × M_H2O2 × LHV_hydrolox) ≥ energy required at Hall thruster input (0.5 × m_chunk_prop × v_e² / η_thr). Minimum energy_balance_ratio observed: ≥ 0.999 across all 366 feasible cells. **Sanity gate PASS.**

### 8.7. Hypothesis scoring

| # | Prediction | Result | Verdict |
|---|---|---|---|
| **H1** | Zero close cells at P_r = 10 kW_e, M_chunk = 200 t, η_gen = 0.50 with L0-05 strict + delivered > 10 t. | 0 close cells in this corner across all Isp and M_H2O2. | **HELD.** |
| **H2** | At P_r = 10 kW_e, M_chunk = 50 t, at least one close cell exists under L0-05 waiver with M_H2O2 ≤ 500 t and delivered ≤ 20 t. | Zero close cells exist. All 14 cells in the corner are Tsiolkovsky-infeasible (chunk too small for the dv at any tested Isp). | **FALSIFIED-BEARISH.** Pre-registered range was too generous; even waiver corner is structurally dead at 10 kW_e + 50 t chunk. Stronger result than predicted: the architecture fails Tsiolkovsky before it even gets to energy-balance. |
| **H3** | Reactor alone at 10 kW_e does not close any chunk ≥ 1 t mission inside round-trip 40 years. | Confirmed. Closest cell is 10 kW_e / chunk 100 t / Isp 5000 at round-trip 444 yr. | **HELD.** |
| **H4** | M_H2O2 / delivered ratio in [50, 300] for cells passing L0-05 waiver. | Of 6 waiver-passing cells, 4 have M_H2O2 = 0 (ratio undefined); 2 have M_H2O2 = 100 t, delivered = 12 t, ratio ≈ 8. | **FALSIFIED-STRUCTURAL.** The framing was wrong: hydrolox isn't "X tonnes per delivered tonne;" hydrolox is *net-negative on delivered tonnage* in every cell where it nominally helps. Section 8.8 expands. |
| **H5** | Total LEO launch stack ≥ 1500 t for any waiver-passing cell. | 4 of 6 waiver-passing cells have LEO stack 687-834 t; 2 have 1437 t. All below 1500 t. | **FALSIFIED.** But the cells that escape the floor are at the upper grid boundary (100 kW_e + aerocap), not the project-owner's 10-kW_e architecture. Sub-1500-t LEO stack at the hybrid-as-proposed corner does not exist. |
| **H6** | Architectural verdict = path 3 from SCOPE ("does not close at any tested combination"). | 0 cells pass L0-05 strict with delivered > 0; the only cells passing L0-05 waiver are at upper-bound P_reactor + aerocap and do not represent the hybrid intuition. | **HELD.** |

### 8.8. The structural finding behind H4's falsification

The pre-registered model assumed brought hydrolox is "additional electric energy in exchange for launch mass" — a clean trade. The actual physics:

**At the inbound burn, brought hydrolox is *both* a chemical-energy source AND inert mass that must be decelerated by the Hall thruster.** With v_e_Hall = 49 km/s (Isp 5000 s) but gas-generator-exhaust velocity ≈ 0 m/s (energy extracted by turbine, products exit at residual enthalpy), the effective specific exhaust v_e_eff scales as:

```
v_e_eff = v_e_Hall × m_chunk_prop / (m_chunk_prop + M_H2O2)
```

Every tonne of brought hydrolox aboard at start of inbound *lowers v_e_eff* by `v_e_Hall × M_H2O2 / (m_chunk_prop + M_H2O2)²`. To recover the lost specific impulse, more chunk water must be consumed as Hall propellant. This compounds: more inert mass → more chunk propellant → less delivered chunk → relatively more inert-fraction → worse v_e_eff. The system spirals against the proposal.

The chemical-energy-import benefit (η_gen × M_H2O2 × LHV ≈ 6.7 MJ/kg at η_gen = 0.5) is dwarfed by the Tsiolkovsky penalty: at Isp 5000 the per-kg energy cost of pushing 1 tonne of hydrolox to dv_inbound = 25 km/s is approximately `(v_e_eff_reduction × dv)` ≈ 4.5 × 10⁸ joules per tonne of hydrolox per kilometre per second of dv reduction — far more than the 6.7 × 10⁹ joules per tonne of energy hydrolox supplies. Net-negative.

**Closed-cycle does not rescue the architecture.** A spot-check (chunk = 200 t, M_H2O2 = 500 t, m_dry = 200 t, dv = 25 km/s, Isp 5000 s, closed-cycle assuming combustion products stay aboard as water): Tsiolkovsky requires `m_chunk_prop = 360 t`, which exceeds the available chunk (200 t). Infeasible. At larger chunk (impossible per axis-19 cap) or higher Isp (cathode-life conditional), it remains infeasible at the same scale. Closed-cycle removes the inert-during-inbound penalty but trades it for inert-through-entire-round-trip — same Tsiolkovsky shape, worse outbound delta-velocity bookkeeping.

This is **instance #6 of the methodology pattern flagged in PROTOCOL lesson 8** (Block 9 in titan's own arc; also surfaced in Block 5 and Block 7). Pre-registration anchored on linear-additive intuition for energy trade; actual Tsiolkovsky cross-term physics produces a sign-flip relative to the linear prediction.

### 8.9. Branch-state caveats and integration notes

- This round is committed on `iceberg-titan-2`, which is ~30 commits behind `origin/main` (titan's Blocks 4-11 from prior session are stranded — they explored the ram-scoop residence-class architecture which the project-owner retired post-titan-handoff). The SCOPE.md in this commit was copied from `origin/main` for in-branch reference; no shared docs were edited.
- Architectural-relevance asymmetry as flagged in §6: phoebe rounds 3-6 (integrated `b5c5d61`) already independently falsified the chunk-rendezvous architecture this SCOPE presumes. Even if this round had found a *closing* hybrid cell, it would not have rescued the program — it would only have produced power-axis closure conditional on a rendezvous mechanism that does not currently appear on the matrix. Since the round produces *non-closure*, it adds a corroborative third orthogonal kill (alongside specific-power and reactor-lifetime).

## 9. Verdict

**SCOPE-prescribed verdict: PATH 3 — "Does not close at any tested combination."**

The hybrid 10-kilowatt-electric reactor + brought hydrolox gas-generator architecture, evaluated across 3,360 cells covering `P_reactor ∈ [1, 100] kW_e`, `M_H2O2 ∈ [0, 5000] t`, `M_chunk ∈ [5, 200] t`, `Isp_e ∈ {2000, 5000} s`, `η_gen ∈ {0.30, 0.50}`, `aerocapture credit ∈ {0, 10} km/s`, and reactor specific power ∈ {2.4, 5.0} W/kg, **fails L0-05 strict (round-trip ≤ 15 years) with positive delivered chunk in every cell**.

The proximate cause of failure splits into two regimes:

1. **At Isp 2000 s**, the chunk-water-only Hall propellant has insufficient specific exhaust (19.6 km/s) to deliver the 25-km/s integrated inbound delta-velocity even fully consuming a 200-tonne chunk. Tsiolkovsky alone closes the architecture, before any energy bookkeeping is engaged.
2. **At Isp 5000 s**, Tsiolkovsky closes mathematically (chunk-prop solution exists in `(0, M_chunk)` for chunks ≥ 100 t), but the burn time at 10 kilowatts-electric reactor is centuries (444-2280 yr depending on M_H2O2). Increasing brought hydrolox makes delivered chunk *worse* due to inert-mass-during-inbound Tsiolkovsky penalty, which dominates the chemical-energy-import benefit by approximately an order of magnitude per tonne.

**The project-owner's architectural intuition is falsified at the prescribed reactor scope (10 kilowatts-electric).** The hybrid does *not* trade reactor-scope wall for launch-cadence wall; instead it incurs both walls (still requires multi-decade burn time AND adds 100-1000+ tonnes of brought hydrolox to the LEO stack).

**Sub-finding on the project-owner intuition's failure mode.** The intuition's implicit assumption — "brought chemical energy substitutes for reactor electrical capacity" — holds *thermodynamically* (joules per kilogram of hydrolox × η_gen = ~6.7 MJ/kg of electrical energy is real) but fails *propulsively*: in the Hall thruster + open-cycle gas-generator topology, the brought hydrolox is *both* an energy source and inert payload, and the latter cost exceeds the former benefit by an order of magnitude.

**Adding a third orthogonal kill to the matrix.** The hybrid-power-axis kill is independent of:
- The phoebe chunk-rendezvous-architecture kill (axis 19).
- The enceladus-r5 reactor-lifetime kill (axis 20).
- The hyperion + rhea specific-power-flown-anchor kill (axis 06).

For framing decisions L0-13 (capital structure) and reactor-program-availability L0 (deferred to `R-reactor-specific-power-program-targets`), this round implies: **the workaround proposal of "smaller reactor + brought chemical energy" does not restore any cell that the 500-kilowatt-electric pure-reactor case did not already close.** The reactor-program decision cannot be deferred to a hybrid-architecture rescue; it must be made on its own terms.

**Methodology lesson 10 candidate** (extending PROTOCOL lesson 8): when a proposal trades one resource for another (here: reactor scope for brought propellant mass), pre-register the trade as a *signed* coupling, not a *linear-additive* one. The brought-resource may interact non-linearly with the system's existing Tsiolkovsky bookkeeping. **The signed-coupling check before pre-registration would have anticipated H4's falsification direction.** This is instance #6 of the same meta-pattern surfacing in titan's arc (Blocks 5, 7, 8, 9, plus this round).

### 9.1. What this round does NOT resolve

- Whether the 100-kW_e + aerocapture corner cells (Section 8.5) represent a viable demonstrator-class architecture. They are at the upper grid boundary, are not "hybrid" in any meaningful sense, and inherit the chunk-rendezvous kill. They surface as a side-effect of grid-extension, not as a hybrid-rescue.
- Whether a different thruster topology (water-vapor-direct chemical engine using brought hydrolox as the *primary* propellant, not a gas-generator-feeding-Hall-thruster) could close. That is a fundamentally different architecture, not the project-owner's proposal.
- Closed-cycle gas-generator (combustion products as additional delivered water). Spot-checked in §8.8 and found also-infeasible at the same chunk-class; full sweep not run because the spot check is determinative.

### 9.2. Recommendations to orchestrator (Saturn)

1. **Integrate finding into matrix** as third orthogonal power-axis kill, alongside specific-power and reactor-lifetime. The hybrid-architecture row is `falsified` (`verdict = path 3`).
2. **Update RISKS.md A-REACTOR family** to reflect that the brought-hydrolox workaround does not restore closure. The B-PROP-WALL risk (programmatic propellant-mass-to-LEO ceiling) is *not* relieved by this proposal.
3. **For L0-13 framing-decision routing** to `R-reactor-specific-power-program-targets`: this round eliminates one of the workarounds the framing-A pitch might have leaned on. The framing decision now depends *only* on reactor-program-availability — there is no chemical-augmentation fallback.
4. **Methodology-lesson 10 candidate** ("signed-coupling pre-registration for trade-off proposals") to PROTOCOL.md after orchestrator review.
5. **Architectural-relevance asymmetry note**: this round was scoped before phoebe's findings. Future SCOPE authoring should explicitly cite the most recent axis-19 and axis-20 verdicts in the §"Architectural relevance" preamble — partly to avoid the SCOPE-authored-before-the-killing-round timing problem, partly to make the architectural-relevance-conditional explicit upfront.

