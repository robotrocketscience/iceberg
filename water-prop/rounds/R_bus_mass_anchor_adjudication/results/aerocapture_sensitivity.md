# Sub-procedure 3 — single-axis sensitivity on phoebe's R-hybrid-aerocapture-aerobraking

Source: phoebe R-hybrid-aerocapture-aerobraking STUDY.md pre-registration anchor tables. Closed-form perturbation of three failure-mode anchors.

Anchors (chunk 200 t / tug 64 t / β=6022 kg/m² / v_entry 15.29 km/s, periapsis-1 40 km, periapsis-2 130 km):

- `chunk_t` = 200.0
- `tug_t` = 64.0
- `beta_kgm2` = 6022.0
- `v_entry_kms` = 15.29
- `periapsis1_km_for_dv` = 40.0
- `peak_g_at_p1_40km` = 40.0
- `chunk_radius_m` = 3.73
- `ice_tensile_MPa_anchor` = 1.0
- `stress_anchor_MPa` = 1.34
- `blbf_anchor` = 0.4
- `blbf_max_credible` = 0.7
- `sublimation_anchor_t_at_130km` = 1505.0
- `passes_anchor_at_130km` = 303000
- `period_hr` = 2.0
- `aerobraking_residual_dv_kms` = 3.0
- `teq_anchor_K_at_130km` = 702.0
- `sublimation_threshold_t` = 100.0
- `timescale_budget_yr` = 5.0

## H5-a — pass-1 chunk structural failure mode (ice tensile sensitivity)

Stress anchor: r × ρ_ice × g_peak × g_earth = 3.73 × 917 × 40 × 9.80665 = 1.34 MPa.

| ice tensile (MPa) | margin = tensile/stress | structural leg flips? |
|---|---|---|
| 1.00 | 0.75× | no |
| 1.25 | 0.93× | no |
| 1.50 | 1.12× | YES |
| 1.75 | 1.31× | YES |
| 2.00 | 1.49× | YES |

**H5-a verdict.** Single-axis relaxation of ice tensile from 1.0 MPa to 1.5 MPa (within phoebe's own 'laboratory-ice envelope' range) flips the structural leg. **H5-a FALSIFIED at 2.0 MPa** (and at 1.5 MPa).

## H5-b — aerobraking-leg sensitivity (boundary-layer-blocking-factor / drag-correction-factor)

**Interpretation 1: BLBF as sublimation rate factor.** Phoebe text: 'Real value 0.3–0.7'. Sublimation total scales as (1 − BLBF) / (1 − 0.4).

| BLBF | sublimation (t) at 130 km | leg flips (≤ 100 t)? |
|---|---|---|
| 0.40 | 1505 | no |
| 0.50 | 1254 | no |
| 0.60 | 1003 | no |
| 0.70 | 753 | no |

**Interpretation 2: K-factor scaling drag Δv-per-pass (King-Hele correction).** Δv-per-pass × K → pass count / K → timescale / K. Anchor: 9.9 mm/s per pass at 130 km, 3 km/s residual.

| K | Δv-per-pass (mm/s) | passes | years | leg flips (≤ 5 yr)? |
|---|---|---|---|---|
| 1.00 | 9.9 | 303030 | 69.1 | no |
| 1.25 | 12.4 | 242424 | 55.3 | no |
| 1.50 | 14.9 | 202020 | 46.1 | no |

**H5-b verdict.** Under BOTH interpretations of the SCOPE-named 'ballistic-correction-factor', single-axis relaxation 0.4 → 0.6 does NOT flip any leg. Sublimation drops from 1505 t to 1003 t (still ≥ 100 t threshold by an order of magnitude). Aerobraking timescale drops from 69 yr to 46 yr (still > 5 yr by an order of magnitude). **H5-b HELD**.

**Naming-conflation note.** The SCOPE called this parameter 'ballistic-correction-factor'. Phoebe's STUDY.md uses 'boundary-layer-blocking factor' for the 0.4 value (in the sublimation calculation). 'Ballistic coefficient' β = 6022 kg/m² is a separate, dimensional parameter. Both interpretations have been tested; neither flips a leg. Flagged as candidate methodology lesson 17 (naming-conflation across rounds).

## H5-c — atmosphere density sensitivity (aerobraking 130–200 km)

Drag-pass Δv scales linearly with ρ; pass count scales as 1/ρ; timescale scales as 1/ρ.

| ρ × | passes (130 km) | timescale (yr) | leg flips (≤ 5 yr)? |
|---|---|---|---|
| 1.0 | 303000 | 69.1 | no |
| 2.0 | 151500 | 34.6 | no |
| 3.0 | 101000 | 23.0 | no |

Chunk equilibrium temperature scales as ρ^0.25 (q ∝ ρ × v³; T_eq = (q/(ε σ))^(1/4)).

| ρ × | T_eq (K) at 130 km | direction |
|---|---|---|
| 1.0 | 702 | anchor |
| 2.0 | 835 | worse |
| 3.0 | 924 | worse |

**H5-c verdict.** Atmosphere density × 3 drops aerobraking timescale at 130 km from 69 yr to 23 yr — still > 5 yr by 4.6×. Chunk T_eq rises from 702 K to 925 K — worse, not better. **H5-c HELD**.

## H5 aggregate

- H5-a structural leg flips at tensile ≥ **1.5 MPa**.
- H5-b sublimation/timescale legs flip under single-axis BLBF/drag relaxation: **False**.
- H5-c aerobraking timescale leg flips under single-axis atmosphere-density relaxation: **False**.
- Number of legs flipping under any single-axis relaxation tested: **1 of 3**.
- Architecture closure requires all three legs to clear simultaneously (conjunctive): **True**.
- **Aggregate H5 verdict.** H5_agg: phoebe 0/1920 robust at the ARCHITECTURE level under any single-axis relaxation

**Reading.** Phoebe's 0/1920 verdict is robust by *conjunction* under single-axis relaxation. The structural leg can be flipped by adopting a more-generous ice-tensile anchor (2.0 MPa, within phoebe's own 'laboratory-ice envelope'), but the aerobraking-timescale and sublimation legs both remain bound by orders of magnitude at any single-axis relaxation tested. Two of three legs are robust-by-magnitude.

**Implication.** A follow-on round targeting H5-a alone would NOT reopen the architecture; it would shift the binding leg from structural to timescale. Reopening the architecture requires a *joint* relaxation across all three legs, which exceeds the scope of single-axis sensitivity. Joint-axis sweep is out-of-scope here and flagged as a candidate follow-on R-hybrid-aerocapture-joint-axis-sensitivity SCOPE only if the project owner directs further investigation.
