# R-variant-B-burn-consistency — does the matrix's "sole defensible cell" hold up on first-principles burn time and propellant accounting, and where does it sit on R12's reactor-lifetime axis?

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 14).

## Question

The architecture decision matrix (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`) names a single Active deployment cell:

> **500-kWe chemical-kick + electric-inbound** (year 0–15, formerly "Variant B"). 500 kWe reactor, chunk ≤ 200 t, chemical Saturn-departure, electric inbound, ~7.5-year inbound burn, **~14.5-year round trip**, 80 t delivered. **Active — sole defensible cell.**

R13 priced this cell at $4.14B median first-unit bottoms-up. R12 added a reactor-lifetime viability axis but only ran the analysis on Architecture E cells (all-electric end-to-end). The matrix's stated numbers for Variant B (7.5-yr inbound burn, 14.5-yr round trip, 80-t delivered) have not been independently audited from first principles in any committed round on `iceberg-enceladus-r5`. R7's `Architecture("VariantB_500kWe", ...)` and the R7/R8 NPV math both consume these numbers as inputs; if they don't close, the entire R7/R8/R13 NPV chain is built on an unverified vehicle.

**Primary question:** running the matrix-asserted Variant B parameters (500 kWe reactor, ISP 2000 s, 200-t chunk, chemical Saturn-departure, electric chunk-fed inbound, MARVL-anchored ship dry mass) through first-principles burn-time and propellant arithmetic, do the matrix's stated 7.5-yr inbound burn / 14.5-yr round-trip / 80-t delivered numbers reproduce?

**Secondary question:** where does Variant B sit on R12's reactor-lifetime axis (cumulative full-power reactor burn vs Kilopower's 10-year design target)?

**Tertiary question:** if Variant B clears reactor lifetime but Arch E doesn't, does that change the matrix's Variant-B-vs-Arch-E comparison meaningfully?

## What this round is and is NOT

**Is:** a focused first-principles burn-time + propellant-accounting check on Variant B at the matrix-stated parameters, extending R12's reactor-lifetime analysis from Arch E to Variant B.

**Is NOT:** a re-derivation of inbound delta-velocity from trajectory physics; uses the matrix's stated dv values plus titan's continuous-thrust range as bracketing inputs.

## Component-level arithmetic (per-hypothesis, recurring-lesson-7 v4 protocol fix)

The R13 retrospective surfaced lesson-7 strike 8: pre-registration arithmetic was anchored on a different vehicle than the model used. This round reads the upstream `Architecture` dataclass directly:

```python
Architecture("VariantB_500kWe",
    reactor_kwe=500.0, chunk_t=200.0, isp_s=2000.0,
    round_trip_yr=14.50, delivered_t=80.0, first_unit_cost_M=500.0)
```

### Reference cell V — Variant B at matrix parameters

Constants:
- v_e = ISP × g0 = 2000 × 9.80665 = 19,613.3 m/s
- Jet efficiency η = 0.70 (matching R-electric-outbound-rerun's ETA_THR)
- Thrust at 500 kWe = 2 × η × P / v_e = 2 × 0.70 × 500,000 / 19,613.3 = **35.69 N**
- Mass flow rate = thrust / v_e = 35.69 / 19,613.3 = **1.820 × 10⁻³ kg/s**

Ship dry mass at 500 kWe under matrix-anchored MARVL model (per `R_electric_outbound_rerun/run.py:83-95` "bundled_10_W_per_kg": m_fixed = 3.0 t, specific_power = 10 W/kg):
- m_stack = 500 / 10 = 50 t
- m_dry (no propellant tank) = 3.0 + 50.0 = **53.0 t**

Inbound, chunk-fed (chunk water is propellant):
- Initial wet mass = m_dry + chunk = 53.0 + 200.0 = 253.0 t

Inbound delta-velocity has two candidates from upstream rounds:
- (a) Matrix impulsive 6.42 km/s (DV_INBOUND_MATRIX_KM_S in R-electric-outbound-rerun)
- (b) Titan continuous-thrust 24.7–40.2 km/s (R-inbound-dv-continuous-thrust)

**Compute burn time and propellant for case (a) — impulsive 6.42 km/s:**
- Mass ratio = exp(6420 / 19,613.3) = exp(0.3273) = 1.3873
- m_prop = m_initial × (1 - 1/MR) = 253.0 × (1 - 1/1.3873) = 253.0 × 0.2792 = **70.6 t**
- Burn time = m_prop / mass_flow_rate = 70,600 / 1.820 × 10⁻³ = 3.879 × 10⁷ s = **1.23 yr**
- Delivered = chunk - m_prop = 200 - 70.6 = **129.4 t**

**Compute burn time and propellant for case (b1) — titan low 24.7 km/s:**
- MR = exp(24,700 / 19,613.3) = exp(1.2594) = 3.524
- m_prop = 253.0 × (1 - 1/3.524) = 253.0 × 0.7162 = **181.2 t**
- m_prop exceeds chunk mass (200 t) marginally; remaining inbound propellant must come from outbound-carried reserve OR the cell does not close at 200-t chunk.
- Burn time = 181,200 / 1.820 × 10⁻³ = **3.16 yr**
- Delivered = chunk - m_prop = 200 - 181.2 = **18.8 t**

**Compute burn time and propellant for case (b2) — titan high 40.2 km/s:**
- MR = exp(40,200 / 19,613.3) = exp(2.0496) = 7.766
- m_prop = 253.0 × (1 - 1/7.766) = 253.0 × 0.8712 = **220.4 t**
- m_prop > chunk (200 t). Cell **does not close** at 200-t chunk; ship must carry inbound propellant from depot or shrink chunk.
- Hypothetical burn time = 220,400 / 1.820 × 10⁻³ = **3.84 yr**
- Delivered = 200 - 220.4 = **-20.4 t** (chunk insufficient)

**Compute round-trip total for case (a) — impulsive:**
- Outbound: chemical-kick from LEO depot; chemical burn is fast (~minutes). Cruise to Saturn = Hohmann half-period = π × √(a_h³ / GM_sun) where a_h = (a_earth + a_saturn)/2 ≈ 5.29 AU = 7.91 × 10¹¹ m.
- Hohmann cruise (each way) = π × √((7.91 × 10¹¹)³ / 1.327 × 10²⁰) = π × √(3.73 × 10¹³) = π × 6.11 × 10⁶ s = **6.083 yr**
- Saturn ops = SATURN_OPS_YR (per R7-rerun) = 0.5 yr
- Round-trip = ~0 (chemical) + 6.083 (outbound cruise) + 0.5 (ops) + 1.23 (inbound burn) + 6.083 (inbound cruise) = **13.90 yr**

This **matches** the matrix's 14.5-yr round-trip within 4%. ✓

But case (a) at 6.42 km/s gives 129 t delivered (not 80 t per matrix). And 1.23-yr inbound burn (not 7.5 yr per matrix).

**Hypothesis on the matrix's numbers:** the matrix's stated "7.5-yr inbound burn / 80-t delivered" for Variant B were carried from an earlier round under different parameters (perhaps Kilopower-class reactor at 10 kWe — burn time scales inversely with reactor power, so 1.23 yr at 500 kWe → ~61.5 yr at 10 kWe, which doesn't match either; OR perhaps under continuous-thrust dv 24.7 km/s, where burn is 3.16 yr and delivered is 18.8 t — also doesn't match). **The matrix may carry stale numbers from a pre-rhea Variant B configuration.**

The 14.5-yr round-trip survives my reproduction of case (a). The 7.5-yr inbound burn and 80-t delivered do not. **This is a falsifiable matrix audit.**

### Reference cell A — Arch E for cross-comparison

R12 ran the all-electric Arch E at 500 kWe / 200-t chunk / ISP 2934 s / round-trip 23.6 yr / delivered 50 t / cumulative burn 11.37 yr. I'll re-extract the burn-time decomposition to cross-check.

For Arch E_500kWe (electric outbound + electric inbound, both at 500 kWe):
- v_e = 2934 × 9.80665 = 28,773 m/s
- Thrust = 2 × 0.70 × 500,000 / 28,773 = **24.33 N**
- Mass flow rate = 24.33 / 28,773 = 8.456 × 10⁻⁴ kg/s
- m_dry (bundled 10 W/kg) = 3 + 50 = 53.0 t
- Outbound dv (continuous-thrust per rhea) = 29.56 km/s (high-elliptical Saturn departure)
- Outbound MR = exp(29,560 / 28,773) = exp(1.0274) = 2.794
- Outbound m_prop = 53.0 × (2.794 - 1) = 95.1 t (burn-from-dry-end)
- Outbound burn time = 95,100 / 8.456 × 10⁻⁴ = 1.125 × 10⁸ s = **3.56 yr**
- Inbound dv (continuous-thrust) = 24.7 km/s (titan low end)
- Inbound initial wet = 53.0 + 200.0 = 253.0 t
- Inbound MR = exp(24,700 / 28,773) = exp(0.8585) = 2.360
- Inbound m_prop = 253.0 × (1 - 1/2.360) = 253.0 × 0.5763 = 145.8 t
- Inbound burn time = 145,800 / 8.456 × 10⁻⁴ = 1.724 × 10⁸ s = **5.46 yr**
- Inbound delivered = 200 - 145.8 = 54.2 t (matches R12's stated 50 t within rounding)
- **Cumulative reactor burn (Arch E) = 3.56 + 5.46 = 9.02 yr.**

Hmm — that's 9.02 yr, not R12's 11.37 yr. Either R12 used different parameters, or I'm using different efficiency. Let me check by running.

Actually R12 said "11.37 yr cumulative — EXCEEDS Kilopower's 10-year design life by 14%." That's the cell `E_500kWe_200t` at round_trip 23.6 yr / delivered 50 t. R12's actual cumulative-burn formula will be replicated in this round's code.

## Pre-registered hypotheses

| Hypothesis | Predicted | Falsification |
|---|---|---|
| H-vbrc-a — Variant B at matrix params (500 kWe, ISP 2000 s, dv_in 6.42 km/s impulsive, chunk 200 t, MARVL mass) inbound burn time | 1.0–1.5 yr (per ref cell V above) | outside [1.0, 1.5] yr |
| H-vbrc-b — Variant B delivered at matrix params, dv_in 6.42 km/s impulsive | 120–135 t (per ref cell V above) | outside [120, 135] t |
| H-vbrc-c — Variant B at continuous-thrust 24.7 km/s inbound dv requires more propellant than the 200-t chunk supplies (chunk-fed model fails) | propellant ≥ 180 t at 24.7 km/s | propellant < 180 t |
| H-vbrc-d — Variant B at continuous-thrust 40.2 km/s inbound dv has negative delivered mass | delivered < 0 t at 40.2 km/s | delivered ≥ 0 t |
| H-vbrc-e — Matrix's stated "7.5-yr inbound burn" reproduces in NEITHER of impulsive 6.42 nor continuous 24.7 nor continuous 40.2 km/s cases at the stated 500-kWe / 200-t / ISP 2000 s parameters | matrix value is at least 2× different from every regime I test | matrix value reproduces (within ±20%) in at least one regime |
| H-vbrc-f — Matrix's stated "80-t delivered" reproduces in NEITHER of the three dv regimes | matrix value is at least 30% different from every regime tested | matrix value reproduces (within ±15%) in at least one regime |
| H-vbrc-g — Variant B round-trip at impulsive 6.42 km/s reproduces the matrix's stated 14.5-yr | round-trip in [13.5, 15.0] yr | outside band |
| H-vbrc-h — Variant B cumulative reactor burn (impulsive 6.42 km/s, all from inbound, chemical outbound has zero reactor burn) | 1.0–1.5 yr | outside band |
| H-vbrc-i — Variant B cumulative reactor burn is ≤ 1/5 of Arch E_500's cumulative burn at matched chunk + reactor power | ratio Variant B / Arch E ≤ 0.20 | ratio > 0.20 |
| H-vbrc-j — Variant B clears Kilopower's 10-year reactor-lifetime target with margin of at least 8 years | Variant B cumulative burn ≤ 2 yr | > 2 yr |
| H-vbrc-k — Arch E_500 cumulative burn reproduces R12's 11.37 yr within ±25% | between [8.5, 14.2] yr | outside band |
| H-vbrc-l — Under continuous-thrust inbound dv (24.7–40.2 km/s), Variant B's 200-t chunk does not yield a self-consistent chunk-fed cell (propellant exceeds chunk OR delivered ≤ 0) for ANY of the three dv values in {24.7, 32, 40.2 km/s} | no self-consistent cell exists in this dv range | at least one dv value yields delivered > 0 and propellant ≤ chunk |
| H-vbrc-m — The matrix's "sole defensible cell" relies on impulsive 6.42 km/s inbound dv (not continuous-thrust), implicitly assuming a chemical inbound phase that the matrix does not document | impulsive yields self-consistent cell; continuous-thrust does not | both yield self-consistent cells, or neither does |
| H-vbrc-n — If the matrix's Variant B uses continuous-thrust inbound dv consistent with titan, the cell does NOT close on propellant at 200-t chunk; required chunk for closure at 24.7 km/s is ≥ 250 t (exceeds L0-05 chunk cap of 200 t) | required chunk ≥ 250 t at 24.7 km/s for self-consistency | required chunk < 250 t |

## Method

### Step 1 — first-principles burn-time + propellant calc

For each of (impulsive 6.42, continuous 24.7, continuous 32.0, continuous 40.2) km/s inbound dv:
- Compute Variant B m_prop_inbound (chunk-fed, m_initial = m_dry + chunk)
- Compute burn time = m_prop × v_e / thrust
- Compute delivered = chunk - m_prop

### Step 2 — Variant B round-trip reconstruction

- Outbound: chemical kick (assume 0 yr reactor burn for propulsion, instantaneous burn)
- Outbound cruise: Hohmann half-period
- Saturn ops: 0.5 yr
- Inbound burn: per Step 1
- Inbound cruise: Hohmann half-period

### Step 3 — Arch E cumulative burn replication

Replicate R12's calculation (outbound burn + inbound burn) at 500 kWe / ISP 2934 / 200-t chunk / continuous-thrust outbound 29.56 + inbound 24.7 km/s.

### Step 4 — reactor-lifetime axis

For each architecture: compute (cumulative burn) / (10-yr Kilopower target) and (cumulative burn) / (15-yr FSP target).

### Step 5 — chunk-cap sensitivity

For Variant B at 24.7 km/s inbound dv: what chunk mass is needed for a self-consistent chunk-fed cell with delivered ≥ 30 t?

### Step 6 — hypothesis scoring

Standard table.

## Caveats

- Jet efficiency η = 0.70 is the R-electric-outbound-rerun default; real ion thrusters at 2000 s achieve 0.60–0.75. ±15% sensitivity on burn time.
- Mass model "bundled 10 W/kg" gives m_dry = 53 t at 500 kWe. R-power-wonder finding 4 (MARVL-anchored) suggests this is approximately right for the bundled formula at megawatt scale; at 500 kWe it may be optimistic by ~30%.
- Chemical-kick outbound burn time is treated as zero from a reactor-life standpoint, which is correct for propulsion but ignores housekeeping power draw over 6-yr outbound cruise. Housekeeping at ~5–20 kWe over 6 yr is 0.03–0.06 reactor-year-equivalents — negligible.
- Saturn ops time set to 0.5 yr per R-electric-outbound-rerun's SATURN_OPS_YR.
- This round does NOT re-derive trajectory physics; it consumes the matrix's stated dv values (impulsive 6.42; continuous 24.7–40.2 from titan).

## Decision matrix consequence

If H-vbrc-e and H-vbrc-f hold (matrix's 7.5-yr inbound / 80-t delivered don't reproduce at any of the four dv regimes), the matrix's "sole defensible cell" needs its stated parameters re-derived from the same source that produced R7's Architecture cell. Either Variant B is **better** than the matrix claims (impulsive case: 129-t delivered, 1.23-yr burn) or it's **worse** (continuous-thrust case: cell doesn't close on propellant at 200-t chunk).

If H-vbrc-i and H-vbrc-j hold (Variant B clears reactor lifetime by ≥8-year margin, while Arch E exceeds the 10-yr target), the reactor-program risk axis preferentially shifts toward Variant B. R13's strict-dominance finding (Variant B > Arch E on P(NPV+) under bottoms-up cost) gains a second independent axis of dominance (reactor lifetime). The "Architecture E might catch up via 8× credibility lift" story becomes harder to sustain.

If H-vbrc-l holds (no self-consistent Variant B cell at continuous-thrust inbound dv), the matrix needs to commit publicly to one of two readings:
- Variant B uses impulsive inbound dv ⇒ requires an inbound chemical phase the matrix doesn't document; OR
- Variant B is L0-05-non-compliant under realistic (continuous-thrust) inbound dv just like Arch E.

Either is a major matrix amendment.
