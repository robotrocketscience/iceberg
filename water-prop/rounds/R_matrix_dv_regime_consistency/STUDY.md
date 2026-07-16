# R-matrix-dv-regime-consistency — does the matrix's "Arch E falsified, Variant B Active" verdict survive consistent dv-regime treatment?

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 15).

## Question

R14 surfaced an undocumented dv-regime asymmetry in the architecture decision matrix:

- **Variant B (Active):** matrix uses inbound dv 6.42 km/s (impulsive). Round-trip 14.5 yr reproduces at this dv.
- **Arch E (Falsified per rhea):** matrix uses continuous-thrust inbound dv 24.7–40.2 km/s (per titan's R-inbound-dv-continuous-thrust). Round-trip 23.6 yr at CT-low 24.7 km/s.

Electric thrusters are physically continuous-thrust. Impulsive dv 6.42 km/s for Variant B's electric inbound is **physically inconsistent with electric propulsion** unless one of three things is true:
- (a) Variant B has an undocumented chemical inbound braking phase.
- (b) Variant B uses gravity-assist trajectory shaping that yields an effective dv of 6.42 km/s after assist credits (lunar GA, Earth-Mars-Jupiter, or similar).
- (c) The matrix carries a stale impulsive number from a pre-titan, pre-continuous-thrust framework.

If (a) is true, the matrix needs to document the chemical inbound phase and mass-budget it. If (b), the matrix needs to document the GA sequence and cite the trajectory study. If (c), Variant B should be re-evaluated under continuous-thrust dv — and may be L0-05-non-compliant just like Arch E.

**Primary question:** if Arch E is rerun at the same impulsive dv framework the matrix uses for Variant B (inbound 6.42 km/s, outbound at matrix's pre-continuous-thrust 9 km/s), does Arch E become L0-05-marginal (round-trip near 15 yr) instead of catastrophically non-compliant (rhea's 23.6 yr)?

**Secondary question:** what is the L0-05-compliance verdict for each (architecture × inbound dv regime) combination at 500 kWe / 200-t chunk?

## What this round is and is NOT

**Is:** a 2×2 (architecture: Variant B, Arch E_500) × (inbound dv regime: impulsive 6.42 km/s, continuous-thrust 24.7 km/s) sweep at matched 500 kWe / 200-t chunk, with paired outbound dv (impulsive 9 km/s for Variant B chemical-outbound or Arch E impulsive-test; continuous-thrust 29.56 km/s for Arch E continuous-thrust).

**Is NOT:** a trajectory re-derivation (does not solve the GA optimization problem; treats both dv values as bracketing exogenous inputs).

## Component-level arithmetic

### Reference cell W — Arch E at impulsive (matrix's pre-continuous-thrust framework)

Arch E_500 at 500 kWe / ISP 2934 s / chunk 200 t / impulsive dv:
- v_e = 28,773 m/s, thrust = 24.33 N, mdot = 8.456×10⁻⁴ kg/s
- m_dry (bundled 10 W/kg) = 3 + 50 = 53 t

**Outbound dv = 9 km/s impulsive (pre-rhea matrix value):**
- MR = exp(9000/28773) = exp(0.3128) = 1.367
- m_prop (from-dry-end) = 53 × (1.367 - 1) = 19.5 t
- burn time = 19,500 / 8.456e-4 = 2.305 × 10⁷ s = **0.731 yr**

**Inbound dv = 6.42 km/s impulsive:**
- MR = exp(6420/28773) = exp(0.2231) = 1.2499
- m_prop (from-wet, chunk-fed) = (53+200) × (1 - 1/1.2499) = 253 × 0.1999 = **50.6 t**
- burn time = 50,600 / 8.456e-4 = 5.984 × 10⁷ s = **1.897 yr**
- delivered = 200 - 50.6 = **149.4 t**

**Total:**
- Cumulative reactor burn = 0.731 + 1.897 = **2.63 yr** (well under 10-yr Kilopower target)
- Round-trip = 0.731 + 6.083 + 0.5 + 1.897 + 6.083 = **15.29 yr** (0.29 yr / 1.9% over L0-05's 15-yr ceiling)

This is **marginally non-compliant** under L0-05, vs rhea's 23.6-yr catastrophically-non-compliant verdict. The 8-yr difference between rhea's 23.6 yr and my 15.3 yr is entirely the dv-regime shift.

### Reference cell X — Variant B at continuous-thrust (titan's framework applied symmetrically)

Variant B at 500 kWe / ISP 2000 s / chunk 200 t / continuous-thrust inbound dv:
- v_e = 19,613 m/s, thrust = 35.69 N (already computed in R14)
- m_dry = 53 t

**Outbound: chemical-kick (zero reactor burn for propulsion).**

**Inbound dv = 24.7 km/s continuous-thrust:**
- MR = exp(24,700/19,613) = exp(1.2594) = 3.523
- m_prop = (53+200) × (1 - 1/3.523) = 253 × 0.7163 = 181.2 t
- delivered = 200 - 181.2 = **18.8 t** (vs matrix's claimed 80 t)
- burn time = 181,200 / 1.820e-3 = 9.956 × 10⁷ s = **3.16 yr**

**Total:**
- Cumulative reactor burn = 0 + 3.16 = **3.16 yr** (still well under 10-yr Kilopower target — Variant B's reactor-life advantage survives continuous-thrust)
- Round-trip = 0 + 6.083 + 0.5 + 3.16 + 6.083 = **15.83 yr** (0.83 yr / 5.5% over L0-05 ceiling)

So Variant B under continuous-thrust is L0-05 non-compliant by 5.5%, delivering only 18.8 t — well below the matrix's 80-t target and L0-09's per-mission floor.

## Pre-registered hypotheses

| Hypothesis | Predicted | Falsification |
|---|---|---|
| H-mdvc-a — Arch E_500 round-trip at impulsive 6.42/9 km/s is L0-05 marginal (14.5–16.0 yr) | 14.5 ≤ RT ≤ 16.0 yr | outside band |
| H-mdvc-b — Arch E_500 round-trip at impulsive is at LEAST 5 years SHORTER than rhea's continuous-thrust 23.6 yr at matched 500 kWe / 200-t cell | RT_impulsive ≤ 18.6 yr | RT_impulsive > 18.6 yr |
| H-mdvc-c — Arch E_500 cumulative burn at impulsive is well under 10-yr Kilopower target | cumulative burn ≤ 4 yr | > 4 yr |
| H-mdvc-d — Arch E_500 at impulsive delivers more mass than the matrix's R7 stated 50 t | delivered > 60 t | ≤ 60 t |
| H-mdvc-e — Variant B at continuous-thrust 24.7 km/s round-trip is L0-05 non-compliant by 0.5–1.5 yr | RT in [15.5, 16.5] yr | outside band |
| H-mdvc-f — Variant B at continuous-thrust 24.7 km/s delivers ≤ 25 t (matrix's 80-t value falsified) | delivered ≤ 25 t | > 25 t |
| H-mdvc-g — Variant B's reactor-life advantage over Arch E survives the dv-regime swap: Variant B cumulative burn at CT ≤ 0.45 × Arch E cumulative burn at CT | ratio ≤ 0.45 | > 0.45 |
| H-mdvc-h — At consistent continuous-thrust dv applied to both architectures, neither at 200-t chunk closes L0-05 (Variant B 15.83, Arch E 22.58) | both round-trip > 15.0 yr at CT | at least one ≤ 15.0 |
| H-mdvc-i — At consistent impulsive dv applied to both architectures (rare for electric), Variant B at 14.0 yr is L0-05 compliant; Arch E at 15.3 yr is marginally non-compliant — only Variant B closes | exactly one of two cells closes | neither or both close |
| H-mdvc-j — The matrix's "Arch E falsified" verdict is dv-regime-dependent: Arch E goes from -8.6 yr below 15-yr ceiling (impulsive) to -8.6 yr ABOVE (continuous-thrust). The 8-yr swing is entirely the dv framework. | round-trip difference between regimes ≥ 5 yr | < 5 yr |
| H-mdvc-k — No (architecture, dv regime) cell at 500 kWe / 200-t chunk is L0-05-compliant when delivered mass is required to be ≥ 50 t per L0-09 | no cell satisfies both | at least one satisfies both |
| H-mdvc-l — Variant B at impulsive 6.42 km/s inbound implicitly requires a chemical inbound braking stage; if mass-budgeted at ISP 450 s with no propellant carried (chunk-fed chemical inbound), required propellant mass exceeds the 200-t chunk | required chemical inbound m_prop > 200 t | ≤ 200 t |

## Method

For each combination in the 2×2 grid:
- (Variant B, impulsive 6.42 km/s inbound, chemical 9 km/s impulsive outbound)
- (Variant B, continuous-thrust 24.7 km/s inbound, chemical outbound)
- (Arch E, impulsive 6.42 km/s inbound, impulsive 9 km/s outbound)
- (Arch E, continuous-thrust 24.7 km/s inbound, continuous-thrust 29.56 km/s outbound)

Compute:
- Outbound burn time, m_prop (for electric outbound) or 0 (chemical outbound)
- Inbound burn time, m_prop, delivered mass
- Cumulative reactor burn (outbound + inbound; chemical outbound = 0)
- Round-trip = outbound burn + Hohmann cruise + Saturn ops + inbound burn + Hohmann cruise
- L0-05 compliance flag (round-trip ≤ 15 yr)
- L0-09 mass flag (delivered ≥ 50 t)
- Reactor-life flag (cumulative burn ≤ 10 yr Kilopower target)
- Three-axis viability flag (all three above)

Hypothesis scoring: standard.

For H-mdvc-l: compute the propellant required for a 6.42 km/s impulsive chemical inbound braking phase at ISP 450 s (hydrolox) with initial wet mass = m_ship + chunk = 253 t. Required m_prop = 253 × (1 - 1/exp(6420/4413.0)) where 4413 m/s is hydrolox ISP × g0.

## Caveats

- "Impulsive" for electric thrusters is non-physical; treated here as an as-if dv calc to expose the matrix's framework asymmetry, not as a propulsion design.
- ETA_THR = 0.70 used throughout (R-electric-outbound-rerun default).
- Bundled 10 W/kg mass model gives m_dry = 53 t at 500 kWe; MARVL-anchored may be 60–70 t.
- Hohmann cruise used for both legs; gravity-assist effective dv changes are not modeled in transit time (only in dv).

## Decision matrix consequence

If H-mdvc-a, b, and j hold, the matrix's "Arch E falsified" verdict is **dv-regime-dependent**, not a robust falsification. Either the matrix needs to:

- (i) **Justify the impulsive 6.42-km/s inbound dv for Variant B** by documenting either a chemical inbound braking phase (H-mdvc-l tests its mass feasibility) or a gravity-assist sequence yielding effective dv of 6.42 km/s. Without this, Variant B should be re-evaluated under continuous-thrust dv and likely loses its Active status.
- (ii) **Apply continuous-thrust dv uniformly** to both architectures. Then Arch E rhea-falsification stands AND Variant B at 200-t chunk is also L0-05-non-compliant (15.83 yr) and delivers only 18.8 t (far below L0-09's per-mission floor). The matrix's "sole defensible cell" becomes "NO defensible cell at 500 kWe / 200-t chunk under continuous-thrust framework."

If H-mdvc-k holds (no cell closes both L0-05 AND L0-09 ≥ 50 t at 500 kWe / 200-t chunk), the matrix needs either a different chunk size, a different reactor power, or to officially accept L0-05 + L0-09 waivers across the board.

This round does not pick between the resolutions; it forces the matrix to choose one.
