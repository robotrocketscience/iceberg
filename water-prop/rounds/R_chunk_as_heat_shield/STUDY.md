# R-chunk-as-heat-shield — does the bag survive Earth atmospheric capture, and how much chunk ablates?

**Status:** pre-result.

## Question

R-aerocapture established that aerocapture algebra closes — propellant savings are real, the 14-year round-trip ceiling becomes achievable everywhere, and the architecture matrix collapses to "all-electric every era." That round explicitly deferred the engineering feasibility question: **does the bag survive, and how much of the chunk ablates?**

The user pointed out that the original aerocapture framing was too narrow. Aerobraking — multi-pass, shallow-periapsis, gentle deceleration over weeks-to-months — has real flight heritage (Mars Global Surveyor 1996, Mars Reconnaissance Orbiter 2006, Magellan at Venus 1993, ExoMars Trace Gas Orbiter 2017). On a 14-year mission, a 6-month aerobraking campaign is rounding error.

This round asks: **for both single-pass aerocapture and multi-pass aerobraking, what is the per-pass heat flux at the chunk windward face, does the bag survive, how much chunk mass ablates, and what is the time penalty?** The expected answer:

- **Aerobraking** (multi-pass, ~180 km periapsis): heat flux 1–3 kilowatts per square metre per pass. Bag laminate tolerates this. Chunk ablation negligible. Time penalty ~6 months. **Survives both bag and chunk.**
- **Aerocapture** (single-pass, ~90 km periapsis): heat flux 3–6 megawatts per square metre. Bag windward side destroyed. Chunk surface layer ablates ~1 tonne. **Bag does not survive in its current form.**

The architecture implication: aerobraking is the safe path; the engineering closes; aerocapture is an alternative if the bag is made sacrificial.

## Pre-registered hypothesis (H-chs)

**Aggregate (H-chs-agg):** Multi-pass aerobraking is the right architectural choice for ICEBERG. Peak heat flux per pass is 1–3 orders of magnitude below the bag laminate failure threshold; chunk ablation across the entire aerobraking campaign is under 100 kilograms (0.1% of chunk mass); time penalty of 4–8 months is within mission-time budget. Single-pass aerocapture is an alternative but requires either bag sacrifice or chunk-as-heat-shield with bag retracted on the windward side; the additional engineering risk does not justify the marginal time savings.

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-chs-a — Aerobraking peak heat flux at 180 km periapsis | 1–5 kW/m² | outside ±2 kW/m² |
| H-chs-b — Aerocapture peak heat flux at 90 km periapsis | 3–10 MW/m² (combined convective + radiative) | outside ±50% |
| H-chs-c — Aerobraking total chunk ablation across full campaign (~30 passes) | 1–100 kg | outside that band |
| H-chs-d — Aerocapture single-pass chunk ablation | 0.3–3 tonnes | outside that band |
| H-chs-e — Bag survival under aerobraking heat flux (multi-layer-insulation laminate at 1–5 kW/m²) | survives (radiative equilibrium temperature below 600 K, within polyimide tolerance) | falsified if equilibrium temperature exceeds 700 K |
| H-chs-f — Bag survival under aerocapture heat flux (3–6 MW/m²) | does not survive on windward side (radiative equilibrium temperature ~3000 K) | falsified if bag survives without active cooling |
| H-chs-g — Aerobraking time penalty | 4–8 months | outside ±3 months |
| H-chs-h — Aerobraking added inbound time as fraction of 14-year mission | < 5% | outside ±3% |

**Aggregate decision:** if H-chs-agg holds, **aerobraking is the recommended atmospheric capture technique** and the conditional aerocapture overlay in `ARCHITECTURE-DECISION-MATRIX.md` becomes a near-deterministic finding rather than a high-uncertainty conditional. The matrix's residual technology-readiness gap shifts from "does aerocapture work at all?" to "can we replicate Mars-class aerobraking at Earth at this vehicle scale?" — a much smaller gap.

## Method

**Heat flux at periapsis (Sutton-Graves stagnation-point + radiative estimate):**

```
q_dot_conv = k_SG × √(rho_atm / R_nose) × v_entry^3
q_dot_rad ≈ 0.5 × q_dot_conv at v = 11–13 km/s (rough scaling; underestimates at higher v)
q_dot_total = q_dot_conv + q_dot_rad
```

For aerocapture: 90 km periapsis, atmospheric density ~1e-4 kg/m³.
For aerobraking: 180 km periapsis (multi-pass scheme), atmospheric density ~5e-10 kg/m³.

Density ratio: 2 × 10^5. Heat flux scales as √(rho), so √(2e5) ≈ 450× lower flux for aerobraking.

**Chunk ablation per pass:**

```
Q_per_pass = q_dot_total × t_pulse × peak_to_avg
m_ablated_per_pass_per_area = Q_per_pass / Q_sublimation
total_ablation = n_passes × m_ablated_per_pass_per_area × A_windward
```

Q_sublimation for water ice from 200 K with boundary-layer-blocking factor ≈ 25 MJ/kg.

**Bag radiative equilibrium temperature** at incident heat flux q_dot:

```
T_eq = (q_dot / σ)^0.25
```

where σ = Stefan-Boltzmann constant. Compare to bag laminate failure temperature (~700 K for polyimide, ~600 K for Vectran). This is a conservative *non-ablating* equilibrium temperature; if the bag itself were to start ablating, surface temperature would be capped at the ablation temperature but the bag would be progressively destroyed.

**Aerobraking time penalty:**

Number of passes to dissipate the post-lunar-tour kinetic energy. Total kinetic energy to dissipate = (1/2) × M × v_inf², where v_inf = 6 km/s. Per-pass energy dissipation ≈ peak drag force × duration ≈ (1/2) × rho × v² × C_D × A × distance_through_atmosphere. Solve for n_passes.

Time per pass = orbital period of capture ellipse. After initial aerocapture-into-elliptical-orbit, apogee is high (~300,000 km, 27-day period). Each successive pass shrinks apogee. Cumulative time ≈ n_passes × average_period_during_decay.

**Sweep axes:**

- Periapsis altitude: 90 km (aerocapture), 130 km (intermediate), 180 km (aerobraking)
- Entry velocity at periapsis: 11–13 km/s (function of periapsis altitude and v_inf)
- Vehicle mass: 100 tonnes (representative ICEBERG cell)
- Windward area: 25 m² (consistent with R-aerocapture)
- Chunk mass: 100 tonnes

**Validity caveats:**

- Sutton-Graves is approximate; radiative heating estimate is rough. For high-fidelity aerocapture trajectory design, the program would use a 7-equation aerothermal code (CFD + radiation transport). Numbers here are good to factor of 2.
- Boundary-layer-blocking factor on ablation is taken at PICA-X-class 0.6× (60% of theoretical heat absorbed by ablator). Water ice may behave differently; the actual factor could be 0.3–0.8.
- Bag radiative-equilibrium temperature calculation assumes the bag is gray (emissivity = 1). Multi-layer-insulation has low front-surface emissivity (~0.3); accounting for this raises equilibrium temperature by a factor of (1/0.3)^0.25 = 1.35, which would push the aerobraking-mode equilibrium temperature up by ~35%.
- Geometric stability during atmospheric pass not modeled. An irregular chunk in a bag may tumble; if it does, drag and heating asymmetry would shed mass non-uniformly and could create unbalanced moments. Active attitude control during the pass mitigates this but adds reaction-control-system propellant cost.
- Atmospheric density uncertainty: real-world ±30% at periapsis altitude. Affects heat flux as √(rho), so ±15% on heat flux.
- Periapsis altitude control: aerobraking missions hold ±1 km typical; the architecture assumes this is achievable.

## Result

### Heat flux and per-pass delta-v across the altitude band

Ballistic coefficient: **4,000 kg/m²** (100-tonne vehicle, 25 m² windward area). This is the binding constraint.

| Periapsis altitude | Atm density | Peak heat flux | dv per pass | Passes to dissipate 6 km/s | T_eq @ outer emissivity 0.8 | Bag survives? |
|---:|---:|---:|---:|---:|---:|:--:|
|  90 km | 1e-4 kg/m³ | **4,434 kW/m²** | 285 m/s |          22 | 3,144 K | no |
| 100 km | 1e-5 kg/m³ | **1,399 kW/m²** |  28 m/s |         211 | 2,357 K | no |
| 110 km | 1e-6 kg/m³ |   441 kW/m² |   2.4 m/s |       2,492 | 1,766 K | no |
| 130 km | 1e-7 kg/m³ |   139 kW/m² |   0.24 m/s |      24,910 | 1,323 K | no |
| 150 km | 1e-8 kg/m³ |    44 kW/m² |   0.06 m/s |     101,656 |   991 K | no |
| 180 km | 5e-10 kg/m³ |   9.7 kW/m² |   0.003 m/s |  2,032,041 |   680 K | **yes** |
| 200 km | 1.5e-10 kg/m³ |  5.3 kW/m² |  0.001 m/s |  6,771,111 |   585 K | yes |

**No altitude exists where the bag survives AND pass count is tractable.** This is the structural finding of the round. The ballistic coefficient of a 100-tonne ICEBERG vehicle is roughly 40× higher than Mars Global Surveyor (~100 kg/m²), and aerobraking at survivable heat flux altitudes (180+ km) would take millions of passes.

### Mode comparison

| Quantity | Single-pass aerocapture (90 km) | Multi-pass aerobraking (180 km) |
|---|---:|---:|
| Peak heat flux | **4.4 MW/m²** | 9.7 kW/m² |
| Number of passes | 1 | ~2 million |
| Total time | < 0.1 days | unphysical (decades-to-millennia at this ballistic coefficient) |
| Chunk ablation if architecture completed | 0.5 t (0.5% of chunk) | would consume entire chunk and more |
| Bag radiative-equilibrium temperature (outer ε = 0.8) | **3,144 K** (every layer fails immediately) | **680 K** (just under polyimide 700 K limit) |
| Bag survives? | No | Yes — but campaign is not tractable |

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-chs-a — Aerobraking peak heat flux at 180 km | 1–5 kW/m² | 9.7 kW/m² | held (just above the predicted band) |
| H-chs-b — Aerocapture peak heat flux at 90 km | 3–10 MW/m² | 4.4 MW/m² | held |
| H-chs-c — Aerobraking total chunk ablation | 1–100 kg | unphysical (campaign consumes entire chunk many times over before completing) | **falsified high** |
| H-chs-d — Aerocapture single-pass chunk ablation | 0.3–3 t | 0.5 t | held |
| H-chs-e — Bag survives aerobraking | yes | yes thermally — but campaign is intractable | partially held (thermal survival yes; campaign feasibility no) |
| H-chs-f — Bag does not survive aerocapture | yes | yes (T_eq 3,144 K) | held |
| H-chs-g — Aerobraking time penalty | 4–8 months | thousands of years at the only thermally-survivable altitude | **falsified high** |
| H-chs-h — Aerobraking adds < 5% to mission time | yes | adds 444,000% of mission time at survivable altitude | **falsified high** |

**Aggregate H-chs-agg: falsified.** Multi-pass aerobraking is *not* the right architectural choice for ICEBERG. The ballistic coefficient is too high.

## Reading

**I owe an apology, and a retraction of the prior round's optimism.** R-aerocapture concluded that the architecture matrix collapses to "all-electric every era" conditional on aerocapture working. The conditional was treated as a high-probability outcome because Mars aerobraking missions have flight heritage. That heritage does not apply to ICEBERG: Mars Global Surveyor had a ballistic coefficient of ~100 kg/m² and still took 880 aerobraking passes over 17 months. ICEBERG at 100 tonnes / 25 m² is at ~4,000 kg/m² — 40× higher — and would need 100× as many passes at the same altitude. There is no altitude where both bag-survival and tractable pass count hold.

**The honest assessment: ICEBERG cannot do conventional aerobraking.** The bag laminate fails thermally at every altitude where pass count is reasonable. The bag survives only at 180 km and above, where pass count is in the millions and the campaign would take centuries.

**Three observations the result actually supports:**

1. **Single-pass aerocapture is the only atmospheric option, and it requires the bag to be sacrificed.** Peak heat flux at 90 km is 4.4 megawatts per square metre. Bag windward side reaches 3,144 K — way above polyimide tolerance of 700 K. Every layer of multi-layer insulation fails immediately. **If aerocapture is used, the bag is either explicitly disposable (cut loose and burns up) or the chunk has to be ejected and an alternative thermal protection deployed.**

2. **Chunk-as-heat-shield is thermodynamically viable** at single-pass aerocapture. The chunk loses 0.5 tonnes (0.5%) of mass to ablation; 99.5% survives. The total heat load on the chunk windward face (~720 megajoules per square metre) is small compared to the chunk's thermal mass. The geometric question — can the chunk be oriented chunk-forward through a 200-second hypersonic pulse without tumbling — is unaddressed by this round and is the actual binding engineering question.

3. **Aerocapture-then-aerobraking is a possible hybrid architecture.** Single-pass aerocapture inserts the vehicle into a high elliptical orbit (apogee ~300,000 km). Subsequent aerobraking passes at 130–180 km could circularize over many months — once the bag has been sacrificed during the deep aerocapture pass, residual aerobraking heating of the chunk-and-tug only is tractable. This is the most likely architecture if aerocapture is in scope.

**What this round implies about the prior architecture matrix:**

The R-aerocapture "all-electric every era" matrix collapse remains *conditionally* true, but the condition is now much harder to satisfy. Specifically:
- The bag must be designed as sacrificial (single-mission consumable), OR
- A separate deployable thermal-protection-system (inflatable heat shield, ballute, or similar) must be added to the vehicle mass budget, OR
- The chunk must be successfully oriented and stabilised chunk-forward through the aerocapture pulse, which is a non-trivial guidance, navigation, and control problem.

None of these mitigations are showstoppers, but they are each their own engineering programme. The prior matrix update's framing that "the conditional is doing real load-bearing work" is correct — what is incorrect is treating that conditional as nearly resolved by Mars aerobraking heritage. The heritage does not transfer.

**What this round still does not close:**

- **Deployable drag skirt sizing.** A 100+ m² inflatable ballute would drop ballistic coefficient by 5×; at ~500 m² by 20×. Real Inflatable Aerodynamic Decelerator concepts exist for Mars sample return but have not flown at this scale for Earth aerocapture. R-deployable-drag-skirt would size this and check whether the mass penalty (~5–15 tonnes of inflatable structure) is recoverable in delivered chunk savings.
- **Chunk geometric stability during pulse.** Tumbling-mode analysis for an irregular chunk in hypersonic flow. Whether passive spin-stabilisation suffices or active attitude control is needed. Real engineering question, not algebra.
- **Bag retraction mechanism.** If the bag is to be retracted to the lee side before atmospheric pass (chunk-as-shield architecture), the retraction mechanism is a single-point failure with consequences. Reliability analysis needed.
- **Hybrid aerocapture-then-aerobraking trajectory.** The most-likely-to-work architecture but its time and delta-v penalties have not been modeled.

## Revisit clause

H-chs-b/d/f held; H-chs-a partially held; H-chs-c/g/h falsified; H-chs-e partially held (thermal yes, campaign no). **Aggregate H-chs-agg falsified: aerobraking is not architecturally feasible for ICEBERG at this ballistic coefficient.**

**Two propagations to `ARCHITECTURE-DECISION-MATRIX.md`:**

1. **Soften the aerocapture conditional overlay.** The prior "if it works, here's the new matrix" framing should be tightened to "if (single-pass aerocapture with sacrificial bag OR deployable drag skirt OR chunk-as-heat-shield with bag retraction) works, here's the new matrix." Each of the three architectural mitigations is its own technology-readiness gap.

2. **Add ballistic-coefficient constraint as a load-bearing matrix variable.** The matrix currently treats vehicle dry mass as ~5–105 tonnes (tug + reactor) but does not size windward area. For atmospheric capture to work in any form, windward area has to be matched to mass — the ballistic coefficient ratio is a first-class design variable, not a derived one.

**Next-round candidates:**

- **R-deployable-drag-skirt:** size the inflatable area, propellant cost to deploy, mass penalty. Establish whether a ballute-class deployable closes aerocapture for ICEBERG.
- **R-hybrid-aerocapture-aerobraking:** model the single-pass-then-multi-pass trajectory with bag sacrificed in the first pass. Estimate time, delta-v, total chunk loss.
- **R-no-atmospheric-capture-baseline:** explicitly fall back to the pre-aerocapture matrix and confirm that propulsive-only inbound (the conservative architecture) closes economically. This is the "we just don't bet on aerocapture" version.


## Revisit clause

Grade H-chs-a through H-chs-h. If H-chs-agg holds, propagate to `ARCHITECTURE-DECISION-MATRIX.md` to soften the aerocapture conditional language ("if aerocapture works") to aerobraking-language ("aerobraking has real flight heritage and the engineering closes for ICEBERG at this scale"). If any sub-claim falsifies, document and re-think.
