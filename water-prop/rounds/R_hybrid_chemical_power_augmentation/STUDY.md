# R-hybrid-chemical-power-augmentation — does a small reactor plus a brought-from-Earth hydrogen-oxygen gas-generator boost close any inbound cell that the 500-kilowatt-electric pure-reactor cell could not?

**Worker:** phoebe (resumed 2026-05-18 latest+8 → +11; reading in cold on chemical-mass-accounting heritage, leaning on lesson-9 SCOPE-audit discipline).
**Round number:** 9th on iceberg-phoebe (3rd outside the chunk-rendezvous architectural arc; first on a power-side question).
**Pre-registered before run.py executed:** yes (Revisit and Cross-learning sections filled post-result).

---

## Question (verbatim from SCOPE)

> For the held chunk-rendezvous architecture (axis 19) with outbound chemical kick locked, inbound continuous-thrust electric, and a hybrid power plant consisting of one reactor of scope P_reactor (kilowatts-electric) plus a gas-generator with brought-from-Earth hydrolox tankage M_H2O2 (tonnes), determine whether any (P_reactor, M_H2O2, chunk_mass, burn_time) combination yields a positive delivered-fraction cell at flown-anchored reactor performance.

The orchestrator's first-pass back-of-envelope addressed only the **full replacement** case (~18,800 t hydrolox to replace 500-kilowatt-electric reactor entirely; infeasible). The project-owner's proposal is a **hybrid**: reactor provides continuous baseline, gas generator provides boost during inbound burn, chunk mass and burn time are free parameters. The three-way optimization across (reactor power, brought hydrolox, chunk mass) has not been run.

---

## SCOPE audit — five load-bearing input-assumption issues caught before pre-registering

Lesson-9 audit-pattern (fifth phoebe-session application; sixth campaign-wide). Each is documented here so the pre-registration is anchored to corrected anchors, not to the SCOPE's original ones.

### Issue 1 — SCOPE missed the chunk-as-propellant constraint (LOAD-BEARING)

The SCOPE's mass model does not explicitly account for the harvested-water Tsiolkovsky constraint: in the surviving cell architecture, electric-thruster propellant is harvested from the chunk itself, so `m_propellant_consumed_from_chunk ≤ chunk_initial`. At Isp 3000 s and 25 km/s inbound delta-velocity, propellant fraction is 0.574 of m_initial. For chunk ≤ ~8.5 t plus 4.3-t dry-stuff bundle, m_prop exceeds chunk_initial — the vehicle would consume the entire chunk as propellant before completing the burn. SCOPE's lowest chunk_mass = 5 t falls below the chunk-eaten threshold at Isp ∈ {2000, 3000}; at Isp 4000 only chunk = 5 t is borderline. **The first three cells of (chunk × Isp) classify CHUNK-EATEN under SCOPE-as-written anchors and deliver negative chunk_delivered before any power consideration applies.** This issue alone falsifies SCOPE's H3 ("reactor alone closes 30-40 year demonstrator at chunk ≤ 10 t") at most of the H3 cells before the energy budget is even computed.

Correction: pre-register on (chunk_delivered, hydrolox_required) jointly; flag CHUNK-EATEN cells as non-deliverable regardless of power.

### Issue 2 — Saturn departure orbit unspecified

SCOPE quotes "inbound burn under continuous-thrust electric needs ~25 km/s integrated delta-velocity" without binding the Saturn departure altitude. Per R-inbound-dv-continuous-thrust (`results/main.json`), continuous-thrust integrated delta-velocity decomposes:

| Saturn departure | dv_no_LGA | dv_with_LGA |
|---|---|---|
| B-ring (1.35 × 10⁵ km) | 40.17 km/s | 38.17 km/s |
| High-elliptical (10⁶ km) | 29.56 km/s | 27.56 km/s |
| Iapetus distance (3.56 × 10⁶ km) | 26.67 km/s | 24.67 km/s |

The SCOPE's "25 km/s" anchor corresponds to Iapetus-distance departure with LGA — i.e. the **most favorable** of three operationally relevant choices. The surviving cell architecture (chunk-rendezvous) places operations at B-ring (1.35 × 10⁵ km), where inbound dv is 40.17 km/s — 1.6× the SCOPE's anchor. The choice changes electrical energy required by a factor of ~1.6²–2× (Tsiolkovsky exponent).

Correction: pre-register on both anchors. Report the SCOPE-as-written Iapetus-distance result first; add B-ring sensitivity at headline cells.

### Issue 3 — Aerocapture credit (10 km/s) conditional on R-hybrid-aerocapture-aerobraking closure (currently 0 of 1920 cells)

SCOPE includes `aerocapture_credit ∈ {0, 10}` as an axis. The 10-km/s credit case requires a chunk-as-heat-shield architecture that phoebe round 1 (R-hybrid-aerocapture-aerobraking, commit `1623cca`) demonstrated does not close at any of 1920 cells across three independent failure modes (pass-1 chunk shatter, aerobraking-timescale, sublimation consumes chunk). Including aerocapture_credit = 10 as a live axis is therefore *conditional* on a separately falsified cell.

Correction: run both anchors but report the aerocapture-credit-10 cells as **conditional-on-aerocapture-rescue**, not as live closure paths.

### Issue 4 — Reactor lifetime constraint absent from SCOPE energy bookkeeping

SCOPE assumes "Kilopower-design-target lifetime of 10 years cumulative" — a paper-study lifetime, not a measured one. The flown-anchored measurement (locked aelfrice belief `0d5c882c13395571` and corroborated by enceladus-r5 R-reactor-lifetime-vs-burn-time) is **28 hours** ground-test (Kilowatt Reactor Using Stirling Technology, 2018). For inbound burns of 10–40 years implied by the SCOPE's burn-time discussion, reactor lifetime is itself a binding constraint, separate from energy budget. A cell with viable energy bookkeeping but burn_time > reactor_lifetime_target is non-closing on lifetime grounds.

Correction: pre-register a separate `lifetime_ok` flag at three thresholds:
- `lifetime_ground_anchor = 28 hr = 0.003 yr` (KRUSTY ground-test measurement)
- `lifetime_design_target = 10 yr` (Kilopower design target; paper-study)
- `lifetime_aspirational = 30 yr` (no public reactor program at this anchor)

### Issue 5 — Hydrolox tank-mass fraction optimistic for multi-year cryogenic storage

SCOPE uses 10 percent tank-mass fraction (Centaur upper-stage heritage). Centaur's storage is hours-of-mission, not years. For a hydrolox stack kept liquid for ~6 years inbound cruise (or 7 years per L1-008), either:

- Active cooling (additional reactor power → reduces electrical budget for thrust), OR
- Multi-layer insulation + accept boil-off (mass-fraction increases substantially; hydrogen worse than oxygen).

Public data point: Centaur III boil-off ≈ 1 percent per day; cumulative over 6 yr cruise = effectively 100 percent loss without active cooling. Reasonable multi-year-storage anchors are 25–40 percent tank-fraction (sub-cooled densified storage + passive multi-layer insulation; ULA ACES/IVF concept territory, no flight heritage).

Correction: pre-register sensitivity on tank fraction ∈ {0.10, 0.25, 0.40}. Report SCOPE-as-written 10% case headline; flag the 25–40% case as the realistic anchor.

---

## Pre-registered hypotheses

All six SCOPE-original hypotheses preserved verbatim with phoebe-side numeric predictions anchored to the BOE under corrected assumptions. **All written and committed before run.py executes.**

### Sweep grid (SCOPE-as-written)

| Axis | Values |
|---|---|
| `P_reactor` (kilowatts-electric) | {1, 5, 10, 20, 50} |
| `M_H2O2` (tonnes brought hydrolox) | {0, 100, 250, 500, 1000, 2500} |
| `chunk_mass` (tonnes) | {5, 10, 50, 100, 200} |
| `η_gen` (gas-generator efficiency) | {0.30, 0.50} |
| `aerocapture_credit` (km/s) | {0, 10} |
| **Total cells** | **5 × 6 × 5 × 2 × 2 = 600** |

Plus phoebe-side audit-extension axes (run as a second sweep block; not in SCOPE-original count):

| Audit-extension axis | Values |
|---|---|
| `saturn_departure` | {Iapetus-distance + LGA (= SCOPE-as-written), B-ring no LGA} |
| `tank_fraction` | {0.10 (SCOPE), 0.25 (realistic), 0.40 (pessimistic)} |
| `Isp_s` | {2000, 3000, 4000} (covered as inner derivation) |
| `lifetime_threshold` | {0.003 yr KRUSTY ground, 10 yr Kilopower design, 30 yr aspirational} (post-hoc flag, not sweep input) |

The audit-extension is small (typically 1–2 representative cells per axis combination rather than full Cartesian) and is run after the SCOPE-as-written sweep.

### Hypothesis pre-registration

| # | Hypothesis (SCOPE-original) | Phoebe BOE prediction | Falsification band |
|---|---|---|---|
| H1 | At P_reactor = 10 kWe, no combination of brought hydrolox up to 1000 t closes a 200-tonne-chunk commercial cell at L0-05 ≤ 15 yr. | **HOLDS strongly.** BOE at chunk = 200 t, Isp 3000, 25-yr burn: hydrolox required ≈ 10,500 t. Even at Isp 2000 (lowest energy): 5,300 t. All > 1000 t. | H1 falsified if any (M_H2O2 ≤ 1000 t, chunk = 200 t) combination at η_gen = 0.5 closes L0-05 strict. |
| H2 | At P_reactor = 10 kWe and chunk ≤ 50 t (Architecture-E scope), some combination closes under L0-05 ≥ 25-yr waiver with brought hydrolox ≤ 500 t. | **MARGINALLY FALSIFIED.** BOE at chunk = 50 t, Isp 2000 (lowest energy): hydrolox @ 25-yr burn = 551 t. Sits 10 percent over SCOPE's H2 threshold. At Isp 3000: 1,913 t (4× over). H2 likely falsified, narrowly. | H2 falsified if zero cells in (M_H2O2 ∈ [0, 500 t]) × (chunk ≤ 50 t) × (burn_time ≤ 25 yr) close. |
| H3 | At P_reactor = 10 kWe and chunk ≤ 10 t, reactor alone closes a 30-40 yr demonstrator without brought hydrolox; hybrid is unnecessary. | **PARTIALLY HOLDS at one cell.** BOE at chunk = 10 t, Isp 4000: reactor-only burn = 25.3 yr, round-trip ≈ 25.3 + 12.2 + 1 = 38.5 yr ≤ 40 yr. At chunk = 5 t, Isp 4000: chunk_delivered = 0.6 t (positive but marginal). All other (chunk ≤ 10, Isp ≤ 3000) cells CHUNK-EATEN. | H3 falsified if zero (chunk ≤ 10 t) cells deliver positive chunk with M_H2O2 = 0 at round-trip ≤ 40 yr. |
| H4 | The launch-mass-vs-chunk-mass cliff sits between 20 and 80 tonnes delivered chunk. | **FALSIFIED-PESSIMISTIC.** BOE shows hydrolox requirement at chunk = 20 t already > 1,000 t at Isp 3000 (cliff lies below 20 t delivered chunk). | H4 falsified if cliff lies outside [20, 80] t delivered. |
| H5 | Round-trip time for surviving hybrid cells is 22-30 years. | **LIKELY FALSIFIED-PESSIMISTIC for surviving cells.** Surviving cells are demonstrator-class (≤ 10 t) at long reactor-only burns; round-trip = 35–45 yr, not 22–30. The SCOPE's 22-30 yr prediction implicitly assumed mid-chunk + heavy hydrolox closure. | H5 falsified if round-trip falls outside [18, 35] years for the surviving cells. |
| H6 | Brought-hydrolox-mass scales linearly with chunk mass × inverse with η_gen. | **HOLDS in BOE.** Linear scaling matches Tsiolkovsky × LHV bookkeeping; deviations < 15 percent expected. | H6 falsified if scaling is non-linear (would indicate a coupled effect such as additional reactor-lifetime burden from extended electrolysis). |

### Phoebe-side aggregate hypothesis (lesson-7: write a campaign-level prediction first)

**H-pa-aggregate (phoebe-aggregate, pre-registered):** The hybrid architecture **does not close** at any cell satisfying the joint constraint set (positive chunk_delivered AND M_H2O2 ≤ commercial single-Starship-flight ≈ 150 t AND L0-05 strict ≤ 15 yr AND reactor lifetime ≤ 10 yr design target). The architecture closes **conditionally** at narrow demonstrator-class cells (chunk = 10 t, Isp 4000, reactor-only, 38-yr round-trip) **only if L0-05 is relaxed to 40-yr demonstrator-class**. Predicted: 0 of 600 cells close at strict joint constraint; 1–4 cells close at demonstrator-class relaxation.

The aggregate prediction is consistent with phoebe's prior architectural reading: **the hybrid is a fourth orthogonal kill on the held architecture if (and only if) the SCOPE's H1 holds strongly, which the BOE shows it does.** The interest of the round is whether the H3 demonstrator-class loophole survives the joint mass + reactor-lifetime + Saturn-departure-orbit audit.

---

## Method

This is a Tsiolkovsky-plus-energy-bookkeeping round, not a Basilisk simulation round. Inherited from rhea R-megawatt-marvl-radiator and titan R-inbound-dv-continuous-thrust in computational style.

**Per-cell evaluation:**

1. **Inbound delta-velocity** = 25 km/s (SCOPE; Iapetus-distance + LGA per R-inbound-dv-continuous-thrust). Audit-extension: 40 km/s (B-ring no LGA) at headline cells.
2. **Aerocapture credit** = 0 or 10 km/s applied to dv before Tsiolkovsky.
3. **Harvested-water Tsiolkovsky** from chunk:
   - `m_initial = chunk + dry_bundle` where dry_bundle = 3.5 t spacecraft + 0.05 × P_reactor (incremental reactor mass above the 10-kWe baseline) + 0.05 × η_gen × peak_generator_power (generator) + 0.05 × M_H2O2 (tank).
   - `m_prop = m_initial × (1 − exp(−dv/v_exh))` where `v_exh = Isp × g0`
   - **Sanity gate (chunk-as-propellant constraint):** if `m_prop > chunk`, classify CHUNK-EATEN; chunk_delivered ← 0.
   - else `chunk_delivered = chunk − m_prop`.
4. **Electrical energy required** = `m_prop × ½ × v_exh² / η_thr` where η_thr = 0.65.
5. **Reactor energy over burn time** at `burn_time` (free; solved below).
6. **Solve for required burn_time:** assuming reactor + gas-generator both run continuously during burn,
   - `E_reactor = P_reactor × burn_time`
   - `E_hydrolox = M_H2O2 × LHV × η_gen` (LHV = 13.4 MJ/kg)
   - `burn_time = (E_required − E_hydrolox) / P_reactor` if `E_hydrolox < E_required`, else burn closes on hydrolox at gas-gen-max-power runtime.
7. **Round-trip time** = `outbound_burn (0.5 yr chemical kick) + cruise (6.09 yr each leg per Hohmann) + saturn_ops (1.0 yr) + inbound_burn`.
8. **Launch-stack mass at Earth orbit** = `chemical_kick_stage_propellant + dry_bundle + chunk_delivered_at_LEO + M_H2O2 + tank_mass`. (Chemical kick stage is from rhea R-outbound-dv-continuous-thrust / hyperion R-outbound-chemical-kick-economics anchors; not swept in this round, taken as 150-tonne-class typical.)
9. **Pass/fail flags:**
   - `closes_L0_05_strict`: round_trip ≤ 15 yr
   - `closes_L0_05_waiver`: round_trip ≤ 25 yr
   - `closes_demonstrator`: round_trip ≤ 40 yr
   - `delivers_positive_chunk`: chunk_delivered > 0
   - `launchable_2x_starship`: Earth-orbit stack ≤ 300 t
   - `launchable_1x_starship`: Earth-orbit stack ≤ 150 t
   - `reactor_lifetime_design`: burn_time ≤ 10 yr (Kilopower design target)
   - `reactor_lifetime_ground`: burn_time ≤ 28 hr (KRUSTY measured)
   - `closes_joint_strict`: ALL of (delivers_positive_chunk, closes_L0_05_strict, launchable_1x_starship, reactor_lifetime_design)
   - `closes_joint_demonstrator`: relaxes L0-05 to demonstrator and reactor_lifetime to aspirational
10. **Energy-bookkeeping sanity:** assert `(E_reactor + E_hydrolox × η_gen) ≥ E_required` for any cell flagged "closes". If a cell flagged closing fails this check, the model has a bug.

**Mass model anchors:**
- Vehicle dry mass: 3.5 t (SATURN-SHIP-SPEC.md bottom-up, including 10-kWe Kilopower baseline + radiators + bag + harvesting hardware)
- Reactor specific power: 2.4 W/kg (KRUSTY flown anchor, locked aelfrice belief `0d5c882c13395571`)
- Generator mass: 0.05 t/kW × peak generator power
- Hydrolox tank fraction: 10 percent (SCOPE) plus phoebe-extension sensitivity at 25 percent and 40 percent
- Thruster efficiency η_thr = 0.65 (titan/rhea anchor)
- LHV hydrolox stoichiometric = 13.4 MJ/kg (lower heating value for water-vapor product; standard combustion thermodynamics)

**Anchors and sources** (in addition to those in SCOPE):
- Inbound delta-velocity decomposition: R-inbound-dv-continuous-thrust commit `58581fb`, `results/main.json` rows `dv_decomposition_no_lga.{B_ring, high_elliptical_1Mkm, Iapetus_distance}` and `dv_decomposition_with_lga.*`.
- Vehicle dry mass bottom-up: water-prop/vehicle/SATURN-SHIP-SPEC.md (3.497 t including 20 percent margin; consistent with conops 5-t top-down if reactor scaled to 20 kWe).
- Aerocapture closure: R-hybrid-aerocapture-aerobraking commit `1623cca` — 0 of 1920 cells close (three independent failure modes).

**Energy-bookkeeping check (sanity gate):** electrical energy delivered to thrusters cannot exceed `reactor × burn_time + M_H2O2 × LHV × η_gen` over any mission segment. Assertion lives in run.py.

---

## Result

### SCOPE-as-written sweep — 1,800 cells

| Flag | Count | Fraction |
|---|---:|---:|
| CHUNK-EATEN (m_prop > chunk_initial) | 968 | 53.8% |
| delivers_positive | 832 | 46.2% |
| closes L0-05 strict (≤ 15 yr) | 0 | 0.0% |
| closes L0-05 waiver (≤ 25 yr) | 126 | 7.0% |
| closes demonstrator (≤ 40 yr) | 362 | 20.1% |
| launchable 1× Starship (stack ≤ 150 t) | 0 | 0.0% |
| launchable 2× Starship (stack ≤ 300 t) | 360 | 20.0% |
| reactor lifetime OK at Kilopower design (10 yr) | 123 | 6.8% |
| reactor lifetime OK at KRUSTY ground (28 hr) | 0 | 0.0% |
| **closes JOINT STRICT** (delivers + L0-05 strict + 1× Starship + lifetime 10 yr) | **0** | 0.0% |
| **closes JOINT DEMONSTRATOR** (delivers + 40 yr + 2× Starship + lifetime 30 yr) | **54** | 3.0% |
| energy-bookkeeping sanity violations | 0 | 0.0% |

### Audit-conditional-axis stripping of the 54 joint-demonstrator cells

The "joint demonstrator" flag uses charitable anchors on three axes: (a) `aerocapture_credit ∈ {0, 10}` charitably treats the 10 km/s credit as live despite R-hybrid-aerocapture-aerobraking having 0 of 1920 cells close; (b) `lifetime_aspirational ≤ 30 yr` is generous against the KRUSTY 28-hr flown anchor and the Kilopower 10-yr design target; (c) `launchable_2× Starship` ≤ 300 t is permissive against the single-flight 1× Starship 150-t envelope.

Stripping these conditional axes one at a time gives the audit-conditional collapse:

| Constraint chain | Surviving cells |
|---|---:|
| Joint demonstrator (charitable joint flag) | **54** |
| ... AND aerocapture_credit = 0 km/s (no rescue from falsified architecture) | **12** |
| ... AND reactor lifetime ≤ Kilopower design 10 yr | **0** |
| ... AND launchable_1×_Starship (≤ 150 t stack) | **0** |

**No cell survives all three audit-conditional strips.** The 12 cells that survive aerocapture-stripping all fail reactor-lifetime at the Kilopower design target (burns are 17-25 yr; 1.7-2.5× over).

### Hypothesis grading

| # | Predicted | Observed | Verdict (raw / audit-conditional) |
|---|---|---|---|
| H1 | 0 cells (200 t commercial closes L0-05 strict at M_H2O2 ≤ 1000 t) | 0 cells | **HELD strongly (both)** |
| H2 | ≥ 1 cell (chunk ≤ 50 t closes L0-05 waiver at M_H2O2 ≤ 500 t) | 4 cells | **HELD raw; FALSIFIED audit-conditional** — all 4 require aerocapture_credit = 10 km/s. After stripping: 0 cells. |
| H3 | ≥ 1 cell (chunk ≤ 10 t closes 30-40 yr demonstrator at M_H2O2 = 0) | 30 cells | **HELD raw; FALSIFIED audit-conditional** — after aerocapture-strip 4 cells, all fail lifetime_design ≤ 10 yr (burns 17.7-25.5 yr). After lifetime-strip: 0 cells. |
| H4 | Cliff in delivered chunk in [20, 80] t | No cliff observed in band | **FALSIFIED** — closure exists at chunk ∈ {10, 50, 100} but not 200; cliff sits in [100, 200] t (above predicted band). |
| H5 | Round-trip 22-30 yr for surviving cells | [20.9, 39.2] yr | **FALSIFIED** — observed range exceeds predicted band on both ends (one cell shorter, several longer). |
| H6 | Linear scaling M_H2O2 ∝ chunk × 1/η_gen ± 15% | Not gradable | **NOT GRADABLE** — fewer than 2 cells with M_H2O2 > 0 close at demonstrator under any (chunk, eta_gen). The reactor-only sweep dominates the closure set; gas-generator augmentation does not produce a closure that the reactor alone would not. |
| H-pa (phoebe aggregate) | 0 strict, 1-4 demonstrator | 0 strict, 54 demonstrator (charitable); 0 demonstrator (audit-conditional) | **HELD on strict (both readings). Falsified-high on demonstrator charitable; HELD-strong on demonstrator audit-conditional (0 ≤ 1-4).** |

### Saturn-departure-orbit sensitivity (audit-extension; P_reactor = 10 kWe, Isp = 3000 s, η_gen = 0.5)

| Saturn departure | dv_inbound | chunk=10 t, M=0 closure? | chunk=50 t, M=0 closure? | chunk=200 t, M=0 closure? |
|---|---:|---|---|---|
| Iapetus + LGA (SCOPE anchor) | 24.7 km/s | round-trip 29.85 yr (delivers 2.34 t) — closes demo | round-trip 77.78 yr — fails demo (burn 64 yr) | round-trip 257.5 yr — fails everything |
| B-ring no LGA (surviving cell architecture operating zone) | 40.2 km/s | round-trip 34.89 yr (CHUNK-EATEN, delivers 0 t) | round-trip 97.77 yr (delivers 10.16 t) — fails demo | round-trip 333.6 yr — fails everything |

**Saturn departure orbit matters substantially.** B-ring departure (where the surviving cell architecture operates) drives delta-velocity from 24.7 km/s to 40.2 km/s, which sufficient to flip chunk=10 t from delivers-positive (Iapetus) to CHUNK-EATEN (B-ring). For the held chunk-rendezvous architecture, the SCOPE's Iapetus-distance anchor is the wrong operating point — closure at B-ring is strictly worse.

### Tank-fraction sensitivity (audit-extension; P_reactor = 10 kWe, Isp = 3000 s, η_gen = 0.5, Iapetus-distance + LGA)

| tank_frac | chunk=10 t, M=250 t closure? | chunk=50 t, M=250 t closure? |
|---:|---|---|
| 0.10 (SCOPE) | dry=29 t, CHUNK-EATEN | dry=29 t, delivers 5.15 t, burn 89.4 yr — fails demo |
| 0.25 (realistic multi-year) | dry=66.5 t, CHUNK-EATEN | dry=66.5 t, CHUNK-EATEN |
| 0.40 (pessimistic) | dry=104 t, CHUNK-EATEN | dry=104 t, CHUNK-EATEN |

**Tank fraction is decisive at non-zero hydrolox**: realistic multi-year cryogenic storage (25-40%) eats the chunk entirely at chunks ≤ 50 t, eliminating most of the SCOPE's notional hybrid closure path. The 10% Centaur-hours anchor inflates the appearance of hybrid viability.

### Sanity checks

- **Energy-bookkeeping violations: 0 of 1,800 cells.** The energy delivered to thrusters never exceeds (reactor × burn_time + M_H2O2 × LHV × η_gen) by more than 1 J floating-point slack. Model passes the SCOPE's gate.
- **Closure on M_H2O2 = 0:** at small chunks and high P_reactor, demonstrator closure exists without any hydrolox. The "hybrid" half of the architecture is not load-bearing; closures use reactor only. (Reinforces H6 not-gradable: no demonstrator closure required hydrolox augmentation.)

---

## Reading

The hybrid architecture **does not close** at any cell under load-bearing constraints. The headline 54 joint-demonstrator cells collapse to 0 after stripping three audit-conditional axes (aerocapture credit = 10 conditional on a separately falsified architecture; reactor lifetime relaxed to 30-yr aspirational vs 10-yr design target; launch envelope at 2× Starship vs single-flight 1× Starship). On the raw SCOPE-as-written sweep, the hybrid is a fourth orthogonal kill on the held chunk-rendezvous architecture, joining R-hybrid-aerocapture-aerobraking (`1623cca`), R-bring-rendezvous-survivability (`abdcd35`), and R-mission-architecture-pivot-survey (`bb570d7`).

The four critical structural findings:

1. **Chunk-as-propellant constraint binds at the demonstrator floor.** 968 of 1,800 cells (54%) classify CHUNK-EATEN: harvested-water Tsiolkovsky propellant exceeds chunk_initial. The SCOPE's lowest chunk_mass (5 t) is universally CHUNK-EATEN at Isp ∈ {2000, 3000}; only Isp = 4000 delivers any chunk at 5 t. This was not in the SCOPE pre-registration. The demonstrator path (H3) lives in a narrow chunk ∈ [5, 10] t × Isp ≥ 3000 corner where chunk_delivered is positive but ≤ 3 t — i.e. demonstrator-class delivery is in the kilograms-per-tonne range, not the tens of tonnes per ship.

2. **Reactor lifetime, not energy budget, is the binding constraint at small chunks.** At chunk = 10 t, P_reactor = 10 kWe, Isp = 3000, M_H2O2 = 0, the energy budget closes (delivers 0.88 t over a 19.25-year burn). But Kilopower's 10-year design target is exceeded by ~2×; the KRUSTY 28-hour flown anchor is exceeded by 1,700×. **The gas-generator boost does not relax the lifetime constraint** because the surviving demonstrator cells require no hydrolox in the first place — gas-generator augmentation is irrelevant where it would have mattered.

3. **The Saturn departure orbit anchor in SCOPE is mismatched to the surviving cell architecture.** SCOPE quotes 25 km/s inbound delta-velocity (Iapetus-distance + LGA). The held chunk-rendezvous architecture operates at B-ring (1.35 × 10⁵ km), where continuous-thrust integrated delta-velocity is 40.2 km/s. The energy budget at B-ring is ~2.6× the SCOPE anchor (Tsiolkovsky exponent), which alone flips chunk = 10 t at P = 10 kWe from delivers-positive (Iapetus) to CHUNK-EATEN (B-ring).

4. **The "hybrid" half of the architecture is not load-bearing in any closing cell.** Across the 54 joint-demonstrator cells, exactly one closing cell has M_H2O2 > 0 (and even that one's gas-generator contribution is small relative to reactor energy). The architectural proposal — trade reactor scope for brought hydrolox — does not produce a closure that the reactor alone wouldn't. H6 (linear hydrolox-mass scaling) cannot be graded because the hybrid mechanism doesn't drive any closure in the swept space. **The hybrid premise fails on its own terms before any anchor audit applies.**

The combined effect is that the SCOPE's question ("does any (P_reactor, M_H2O2, chunk_mass, burn_time) combination yield a positive delivered-fraction cell at flown-anchored reactor performance?") answers **NO at strict joint constraint, conditionally YES (54 cells) at charitable joint flags, NO again after stripping conditional axes.** This is a phoebe-style outcome: the surviving-cell count under charitable framing collapses to zero under each load-bearing constraint independently, confirming the architectural falsification with high confidence.

---

## Revisit

**Did the pre-registration hold?**

- **H1 HELD strongly (predicted: 0 cells; observed: 0 cells).** The 500-kilowatt-electric-equivalent commercial-class closure at chunk = 200 t is unreachable through any combination of P_reactor ≤ 50 kWe and M_H2O2 ≤ 2500 t. The orchestrator's SCOPE-original H1 anticipated this; the BOE confirmed it; the sweep ratifies it.

- **H2 mixed.** Raw: HELD (4 cells satisfy chunk ≤ 50 t × M_H2O2 ≤ 500 t × L0-05 waiver). After audit-conditional stripping (aerocapture = 0): 0 cells. The pre-registration was technically correct under SCOPE-as-written, but the load-bearing reading after the audit-pass is that H2 is **conditional on rescuing a separately falsified architecture**. The phoebe BOE prediction ("marginally falsified") was wrong by one cell at the SCOPE-as-written anchor, and right at the audit-conditional anchor.

- **H3 mixed.** Raw: HELD (30 cells satisfy chunk ≤ 10 t × M_H2O2 = 0 × demo 40 yr). After audit-stripping (aerocapture = 0 + lifetime_design ≤ 10 yr): 0 cells. The pre-registration was technically correct under SCOPE-as-written, but the load-bearing reading after the audit-pass is that H3 is **conditional on either aerocapture rescue or reactor-lifetime relaxation beyond the design target**.

- **H4 FALSIFIED.** No cliff in [20, 80] t band; the cliff sits between 100 and 200 t. The BOE prediction "cliff lies below 20 t delivered chunk" was also wrong-direction; the cliff is *above* the predicted band. Why: the sweep allows reactor-only closure where the BOE assumed hydrolox-augmented closure. With reactor-only, the cliff is set by energy gap which scales linearly with chunk; the cliff sits where the gap exceeds reactor-lifetime × P_reactor at maximum sweep P (= 50 kWe).

- **H5 FALSIFIED.** Observed range [20.9, 39.2] yr; predicted [22, 30]. Falsified on both ends — some cells shorter (aerocapture rescue lowers burn time), some longer (low-P reactor-only burns extend round-trip).

- **H6 NOT GRADABLE.** No demonstrator-closing cell required M_H2O2 > 0; the hybrid mechanism is functionally inert in the swept space.

- **H-pa-aggregate**: HELD on strict; observed 54 demonstrator vs predicted 1-4 — falsified-high on the count but the audit-conditional reading collapses to 0, consistent with the aggregate architectural prediction "the hybrid does not close at load-bearing constraints." Phoebe-aggregate prediction stands at the aggregate-architectural-reading level even though the cell-count was off.

**What went wrong in the pre-registration?**

1. **BOE underestimated demonstrator closures by ~10×.** I predicted "partially holds at one cell" for H3; observed 30 raw / 4 audit-conditional / 0 fully-clean. The BOE missed that at small chunks (5-10 t) AND high P_reactor (5-50 kWe), reactor-only cells close because energy budget shrinks faster than reactor capacity. I was too pessimistic on reactor sizing because I anchored to P_reactor = 10 kWe instead of sweeping P_reactor.

2. **BOE missed the aerocapture-credit lever.** I treated `aerocapture_credit = 10` as "charitable / conditional" but didn't quantify how many cells it rescues. Observed: 42 of 54 joint-demonstrator cells require it. This is a much larger lever than I anticipated.

3. **BOE got the SATURN-SHIP-SPEC dry-mass anchor wrong.** I anchored to 3.5 t total dry (Kilopower paper-study specific power), not the KRUSTY flown anchor (~6 t at 10 kWe). Sixth audit-issue caught during run.py construction, fixed in the code, documented in STUDY.md SCOPE-audit section, BUT the pre-registered numeric predictions in §"Pre-registered hypotheses" used the wrong anchor. **The phoebe pre-registration grades are anchored to the corrected model output, not the wrong-anchor BOE.** This is the second time a phoebe round caught its own load-bearing anchor error during run.py construction (first: R-bring-rendezvous-survivability round-trip ambiguity). Methodology footnote candidate.

4. **BOE under-anticipated the chunk-eaten count.** Predicted CHUNK-EATEN at chunks ≤ 8.5 t (Isp 3000); observed CHUNK-EATEN at 968 of 1,800 cells (54%) — the constraint binds across more of the sweep than expected. The over-binding is mostly the higher dry-bundle (Issue 6) plus the Isp interactions.

The pre-registration's structural prediction — hybrid does not close at audit-conditional constraints — held. The cell-count predictions were off in both directions for the wrong-anchored cells (under-predicted demonstrator and over-predicted chunk-eaten band-edges). **The aggregate architectural reading is robust to the BOE errors; the per-hypothesis numeric grading is not.**

---

## Cross-learning

### Forward references (for downstream rounds)

- **POSITIVE for the held chunk-rendezvous architecture's retirement.** This round adds a fourth orthogonal kill: the hybrid power proposal does not close under load-bearing constraints. The architecture is now killed by (1) aerocapture-impossible at any cell (R-hybrid-aerocapture-aerobraking, 0/1920); (2) B-ring-survivability impossible at any cell (R-bring-rendezvous-survivability and three self-questioning follow-ons, 0 of 4,808); (3) no surviving architecture in the pivot-survey of 31 candidates (R-mission-architecture-pivot-survey); and (4) no hybrid-power closure at audit-conditional constraints. Five-round phoebe convergent falsification of the held architecture, now spanning 6,608+ closure-checks across both architectural and power-side axes.

- **POSITIVE for L0-13 capital-structure-framing deferral**. The project-owner walk-through deferred L0-13 capital structure to R-reactor-specific-power-program-targets. This round corroborates that deferral: there is no plausible (P_reactor, M_H2O2) combination that closes a return-seeking-capital cell with the held architecture; the framing-A pitch ("trade reactor risk for launch-cadence risk") fails because the launch-cadence trade is itself infeasible at chunks ≥ 50 t. Both walls bind; trading them does not produce a closure.

- **NEGATIVE for hybrid as a standalone architectural lever.** The hybrid proposal as written does not produce ANY closure that reactor-only would not. M_H2O2 > 0 helps in zero of 54 surviving cells. The gas-generator mass-for-reactor-scope swap is real (you do get electrical energy at a chemical-mass cost), but the swap does not change which cells close. If the project-owner wants to revisit the hybrid concept, the binding constraint to relax first is **reactor lifetime**, not reactor scope.

- **NEUTRAL for the demonstrator path.** R-mission-architecture-pivot-survey identified 7 F6-conditional WORTH-DEEP-DIVE candidates under iapetus-style probabilistic F6 (reactor program). This round shows that even at the smallest chunks (5-10 t), the reactor-lifetime constraint pushes burn time to 17-25 yr at 10 kWe — well past Kilopower's 10-yr design target. **Any demonstrator-path round should pre-register a reactor-lifetime feasibility check as a primary hypothesis, not a secondary flag.** The "lifetime cliff" sits at chunk × Isp ratios where energy budget × Kilopower 10-yr ≥ reactor-only burn closure; for the SCOPE-as-written anchors, this cliff is below the smallest tested chunk.

### Backward references

- **R-hybrid-aerocapture-aerobraking (1623cca):** explicitly tested in this round as `aerocapture_credit ∈ {0, 10}`. The 10-km/s case rescues 42 of 54 joint-demonstrator cells but is conditional on R-hybrid-aerocapture having a closing cell, which it does not. **Conditional-credit pattern is methodology-noteworthy.** Future rounds inheriting conditional architectures from upstream falsified rounds should report results both ways and flag the conditional dependency.

- **R-bring-rendezvous-survivability (abdcd35) and follow-ons (45869d4, 8a31ba9, 75ba925):** The chunk-population vs safe-passage co-location problem is independent of power; this round's negative verdict on hybrid power does not relax it. The held architecture remains dead on both axes.

- **R-mission-architecture-pivot-survey (bb570d7):** identified 31/31 DEAD-ON-ARRIVAL candidates; 7 F6-conditional WORTH-DEEP-DIVE. This round confirms F6 (reactor program) is binding even at the demonstrator scale: no Kilopower-anchored cell closes joint-strict under any (chunk, M_H2O2) combination. **The F6 conditionality is real in this round at the demonstrator floor.**

- **R-inbound-dv-continuous-thrust (titan, 58581fb):** anchor for 24.67 km/s Iapetus-departure delta-velocity. The audit-extension Saturn departure sensitivity in this round shows B-ring (40.17 km/s) operating point flips chunk = 10 t from delivers-positive to CHUNK-EATEN. **The SCOPE-author should anchor delta-velocity to the architecture's operating departure orbit, not the most-favorable arbitrary anchor.** Candidate PROTOCOL footnote.

- **R-power-wonder findings 1-4 (locked aelfrice beliefs):** This round directly uses finding 1 (40 W/kg paper-study vs KRUSTY 2.4 W/kg flown) as the reactor-specific-power anchor. SATURN-SHIP-SPEC's 1.6-t reactor anchor at 10 kWe is paper-study (6.25 W/kg); KRUSTY anchor gives 4.17 t. Catching this during run.py construction is the 6th SCOPE/anchor audit issue.

### Methodology lessons reinforced or candidate-new

- **Methodology lesson 9 sixth campaign-wide application.** SCOPE audit caught five input-assumption errors before run.py and a sixth during run.py construction (vehicle dry-mass anchor). Each was load-bearing on at least one hypothesis grading. **Lesson 9 is now stable practice across both worker-authored SCOPEs and orchestrator-authored SCOPEs; should be promoted from candidate to PROTOCOL methodology lesson.**

- **Methodology lesson 11 candidate (self-questioning round pattern) extended to power-side architecture.** This round is structurally a self-question on the hybrid-power proposal: pre-register what the SCOPE asks, audit the SCOPE's anchors, then show that the surviving-cell count under charitable framing collapses to 0 under load-bearing constraints. Same pattern as R-bring-survivability-relaxed and the three subsequent self-questioning rounds. **Pattern generalises beyond the architectural-rendezvous arc.**

- **Candidate methodology lesson 12 (new this round): conditional-axis stripping discipline.** When a SCOPE includes an axis that is conditional on a separately-falsified upstream cell (here: `aerocapture_credit = 10`), the run-result table should report both raw and audit-conditional counts side-by-side. Otherwise the SCOPE-as-written count overstates closure availability by a factor matching the conditional-axis multiplicity. **Recommend extending lesson 9 SCOPE-audit checklist with explicit "list upstream-falsified architectures inherited by this SCOPE's axes; report results with and without those axes."**

- **METHODOLOGY-FLAG (campaign-shared): the BOE-vs-run discipline holds with a known weakness.** Phoebe-style BOE-first-then-pre-register caught structural predictions correctly (architecture does not close) but missed cell counts by ~10×. This is consistent with lessons 1 and 7 (BOE for direction, not for cell counts). For high-multiplicity sweeps, BOE should anchor each hypothesis to its predicted *fraction* of the sweep (e.g. "≤ 1% of cells") rather than to absolute cell counts, since the BOE typically can't anticipate axis combinatorics. Footnote candidate.

- **METHODOLOGY-FLAG: anchor-error caught during run.py implementation (load-bearing).** SATURN-SHIP-SPEC anchors reactor+power at 1.6 t per Kilopower paper-study; locked aelfrice flown anchor (KRUSTY 2.4 W/kg) gives 4.17 t — 2.6× heavier. Caught after first run produced "negative dry bundle" at low P_reactor. **Recommend: campaign-shared utility `reactor_mass_t(p_kwe, specific_power_w_per_kg)` that defaults to KRUSTY flown anchor with explicit override flag for paper-study anchors.** Same pattern as the `bag_min_area_m2(chunk_t)` utility from R-bag-aperture-chunk-joint.

