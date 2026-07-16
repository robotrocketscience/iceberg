# R-matrix-dv-regime-consistency — summary

## The 2×2 grid

| Case | out_burn (yr) | in_burn (yr) | RT (yr) | delivered (t) | cum_burn (yr) | L0-05 | L0-09 | R-life |
|---|---:|---:|---:|---:|---:|:-:|:-:|:-:|
| VariantB_impulsive | 0.00 | 1.33 | 14.01 | 128.8 | 1.33 | OK | OK | OK |
| VariantB_continuous_thrust | 0.00 | 3.42 | 16.10 | 17.4 | 3.42 | FAIL | FAIL | OK |
| ArchE_impulsive | 0.82 | 2.06 | 15.55 | 149.0 | 2.87 | FAIL | OK | OK |
| ArchE_continuous_thrust | 3.98 | 5.93 | 22.58 | 53.1 | 9.91 | FAIL | OK | OK |

## Chemical inbound braking sanity (H-mdvc-l)

Required hydrolox propellant for 6.42 km/s impulsive inbound = **837.3 t**.
Chunk available = 200 t. **Exceeds the chunk-as-chemical-prop capacity.**

## Scoring: 11 HELD / 1 FALSIFIED of 12

The one falsification (H-mdvc-k) is the most load-bearing finding: **Variant B at impulsive 6.42 km/s inbound dv passes ALL THREE viability axes** — L0-05 (round-trip 14.01 yr ≤ 15 yr ceiling), L0-09 (delivered 128.8 t ≥ 50 t floor), reactor lifetime (cumulative burn 1.33 yr ≤ 10-yr Kilopower target). The matrix's "sole defensible cell" survives, but only under the impulsive-dv framework.

See `hypothesis_scoring.md` for per-hypothesis verdicts.

## Discussion

### The dv-regime framework dispute is the matrix's most load-bearing open question

The 2×2 grid shows the matrix's "Arch E falsified, Variant B Active" verdict depends entirely on which dv regime is applied:

| | Variant B | Arch E_500 |
|---|---|---|
| **Impulsive (matrix's pre-rhea framework, applied to VB throughout)** | **All three axes PASS** (RT 14.01, del 128.8 t, burn 1.33 yr) | **L0-05 marginal** (RT 15.55, only 3.7% over) — but L0-09 and reactor life pass |
| **Continuous-thrust (titan/rhea framework, applied to E throughout)** | **L0-05 FAIL** (RT 16.10) and **L0-09 FAIL** (del 17.4 t) | **L0-05 FAIL** (RT 22.58) — rhea's "Arch E falsified" verdict |

Two possible resolutions:

**Resolution A — impulsive framework applies to both architectures.** Variant B at 14.01 yr is L0-05 compliant. Arch E at 15.55 yr is marginally non-compliant (3.7% over) — recoverable by a small chunk-size reduction, ISP adjustment, or L0-05 waiver. The matrix's "Arch E falsified" verdict is **wrong** under this resolution; Arch E should be re-evaluated as marginal-not-falsified.

**Resolution B — continuous-thrust framework applies to both architectures.** Variant B at 16.10 yr is L0-05 non-compliant by 7.3% AND L0-09 non-compliant by 65% (delivers 17.4 t, not 50 t). The matrix's "Variant B Active" verdict is **wrong** under this resolution; Variant B is L0-05 + L0-09 dual-non-compliant and the program has NO defensible cell at 500 kWe / 200-t chunk.

### Why the chemical-inbound-braking interpretation of Variant B's impulsive dv is infeasible

If one tried to interpret the matrix's 6.42-km/s impulsive inbound dv as a chemical inbound braking phase (the only way to get impulsive dv with reasonable burn time), the propellant mass required at hydrolox ISP 450 s is:

```
m_chem_required = (m_dry + chunk) × (exp(dv/v_e) - 1)
                = 255 × (exp(6420/4413) - 1)
                = 255 × (4.286 - 1)
                = 837.3 t
```

**Required hydrolox propellant: 837 t, which is 4.2× the 200-t chunk.** No reasonable depot or chunk-fed chemical mechanism can supply 837 t of hydrolox at Saturn. **Chemical inbound braking is structurally infeasible at the matrix's stated parameters.**

The matrix's 6.42-km/s impulsive inbound dv therefore must come from **gravity-assist trajectory shaping** (lunar gravity assist, Earth-Mars-Jupiter sequence, or equivalent) which is not currently documented. This is the highest-priority follow-up.

### Connection to R6 / R7 / R8 / R13 / R14

Every NPV cell in R7 / R8 / R13 assumed `Architecture("VariantB_500kWe", round_trip_yr=14.50, delivered_t=80.0, ...)`. R14 found the matrix's 7.5-yr inbound burn / 80-t delivered numbers don't reproduce; R15 confirms they don't reproduce at impulsive (RT does match, but burn time is 5.6× lower and delivered is 1.6× HIGHER than matrix-stated) NOR at continuous-thrust (where RT is also wrong). **The downstream NPV cells inherited stale Variant B numbers and need recomputation under whichever dv-regime resolution wins.**

If Resolution A wins (impulsive both), the corrected Variant B cell is:
- Round-trip 14.01 yr, delivered 128.8 t (not 80 t), cumulative burn 1.33 yr.
- 128.8 t / 80 t = 1.61× more mass delivered per mission. Revenue/mission goes up roughly proportionally. Variant B P(NPV+) probably recovers substantially above R13's 8.6%.
- Arch E_500 also becomes marginal-not-falsified; the matrix's whole "Arch E retired" framing falls.

If Resolution B wins (continuous-thrust both), the corrected Variant B cell delivers only 17.4 t, not 80 t — and is L0-05-non-compliant. Variant B is not a viable cell. **The program has no defensible architecture at 500 kWe / 200-t chunk.**

### The matrix needs a single, documented dv-regime choice. Currently it has two.

This round does not pick between the resolutions; it forces the matrix to choose one and document the trajectory framework. The cleanest follow-up is R-trajectory-shaping-feasibility — does a gravity-assist sequence exist that justifies 6.42-km/s effective inbound dv for an electric thruster at 500 kWe?
