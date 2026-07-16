# R-framework-matrix-parity — STUDY (pre-registered)

**Worker:** titan (re-spawn 4, branch `iceberg-titan-4` off `origin/main`)
**Date frozen:** 2026-05-22
**SCOPE:** `water-prop/rounds/R_framework_matrix_parity/SCOPE.md` (Saturn, punch-list M-4 + S-1)
**Round type:** framework engineering + comparative cell-diff. No new architectural cells.

---

## Question

Once the `mission_graph` framework encodes the four constraints the matrix already
carries (reactor lifetime, MARVL bundled radiator mass, conservative bus-mass floor,
vis-viva-corrected delta-velocity anchors), do the framework's surviving cells reproduce
the matrix's surviving cells at conservative anchors? Where they diverge by > 30 percent,
does the bug live in the framework or in the matrix?

---

## Pre-study code reading (frozen before any encoding)

Reading the framework and the source rounds **before** touching code surfaced four facts
that revise the SCOPE's stated mechanisms. These are recorded here so the hypotheses below
are honest predictions against the actual code, not against the SCOPE's assumptions.

1. **The framework models reactor mass and radiator mass as ZERO.** Grep across
   `framework/` and `missions/` finds no `reactor_mass`, no `radiator`, no `specific_power`
   term. `VehicleState` carries `power_available_kwe` but nothing scales vehicle dry mass
   with it. A 1-kWe vehicle and a 30-kWe vehicle have identical dry mass in the framework.
   The SCOPE framed constraint 2 as "replace the decomposed model the framework inherits";
   in fact there is no powerplant-mass model at all. titan-3's source
   (`R_chunk_size_pareto/run.py:60-64`) explicitly subtracts
   `m_reactor = P_kw·1000 / sp_w_per_kg / 1000` (12.5 t at 30 kWe / 2.4 W/kg; 3 t at 10 W/kg)
   from delivered tonnage. **This is a missing term, not a wrong one — the larger of the
   four expected effects.**

2. **Phase 4 (Saturn departure) already encodes the corrected 7.7 km/s anchor**
   (`phase4_saturn_departure.py:56`, `CHEMICAL_TEI_DV_KM_S = 7.7`, citing titan-3 `42120cf`).
   Constraint 4 is therefore half-done; only the Phase 6 arrival side remains.

3. **Phase 6 (Earth arrival) capture-burn formula is too cheap.** The framework uses
   `direct_propulsive_capture_dv(v_inf) = 0.4·v_inf + 0.3` km/s, giving 0.7 km/s at
   v_inf = 1 and 4.3 km/s at v_inf = 10. The physically correct LEO-capture burn is
   `√(v_inf² + v_esc_LEO²) − v_circ_LEO` with v_esc_LEO ≈ 11.0, v_circ_LEO ≈ 7.78 km/s,
   which gives 3.2 km/s at v_inf = 1 and 7.3 km/s at v_inf = 10.3 — matching titan-3
   R-delta-velocity-anchor-audit's 7.3-direct / 4.2-post-LGA exactly. The framework
   understates the arrival burn by ~2.5–3 km/s, biggest in fractional terms at LOW v_inf
   (the chunk-fed-spiral path arrives at v_inf = 1, where the error is 0.7 vs 3.2).

4. **titan-3's closing architecture is pure-electric at Isp 2000 s, not water-MET 800 s.**
   `R_chunk_size_pareto/run.py` uses `ISP_ELECTRIC_S = 2000`, inbound residual Δv 4470 m/s
   after the R12 10-flyby lunar gravity assist, reactor mass subtracted, **no radiator term,
   and no reactor-lifetime ceiling** (the lifetime ceiling is enceladus-r5's later
   addition). The framework's canonical sweep uses `water_met_isp_s = 800` for chunk-fed
   departure and `electric_isp_s = 3000` for the low-thrust spiral — neither equals 2000.
   This is an architecture-parameterization difference, not a physics difference, and is a
   candidate root cause for any residual divergence.

## Pre-encoding baseline (frozen)

Canonical sweep `runs/20260522T193231Z` (regenerated; the saturn-audit `20260521T193329Z`
output was gitignored as a large file). 750 cells, `delivered_floor` ≥ 30 t:

- **1404 of 26852 closure-results close (5.2 %).**
- **Only chunk_mass_kg = 200,000 closes.** 25/50/100-t chunks: 0 %. 10-t chunk: 0 %.
- Closes only at power_kwe ∈ {30, 55} (the K30 and K30+S50 classes); 0 % at ≤ 20 kWe.
- Closes only at electric_thrust_n ≥ 5 N, and at vehicle_mass_kg ∈ {50, 63, 100 t}.
- This reproduces the saturn-audit "200-tonne-only" headline.

**Mechanism (frozen reading):** the framework rewards large chunks because (a) it charges
nothing for the reactor that must push them and (b) it undercharges the arrival capture
burn. Encoding constraints 1–4 removes both subsidies.

---

## Pre-registered hypotheses (honest predictions)

Adopted from SCOPE H1–H6, with predictions revised per the pre-study code reading above.
Falsification bands frozen.

| # | Hypothesis | Predicted | Falsified if |
|---|---|---|---|
| H1 | **Constraint 1 (reactor lifetime)** binds on cells whose cumulative full-power burn exceeds L·8760 h. titan-3's closing cells have inbound burn < 6.09 yr (round-trip 13.81 yr = 6 + 1 + 6.09 + 0.725), so they survive L = 10 yr but FAIL L = 5 yr. The framework's 200-t chunk-fed cell has a much longer burn and fails at L ≤ 10 yr. | 200-t framework cell collapses at L = 5 yr; transitional at L = 10; survives at L = 15. titan-3 4 cells survive L = 10. | mission_graph 200-t cell survives at L ≤ 5 yr AND sp = 2.4 W/kg. |
| H2 | **Constraint 2 (reactor + MARVL radiator mass)** is the load-bearing constraint, NOT a marginal shift. Because the framework currently charges ZERO for the powerplant, adding `m_reactor = P/sp` + `m_radiator = 5 t + 0.1 t·kWe` removes a large subsidy. At 30 kWe / 2.4 W/kg that is 12.5 + 8 = 20.5 t of dry mass that must now fit inside the launched vehicle and be hauled through every burn. | The 200-t cell at small vehicle mass (50–63 t) collapses because the powerplant no longer fits / no longer closes the floor; surviving cells shift toward higher vehicle mass or sp = 10 W/kg. | 200-t cell survives unchanged after powerplant mass is charged. |
| H3 | **Constraint 4 (Phase 6 vis-viva capture)** removes the arrival-burn subsidy and bites hardest on low-v_inf paths (chunk-fed spiral arrives at v_inf = 1). Direct propulsive capture becomes ~3.2 km/s instead of 0.7, consuming chemical propellant the chunk-fed path does not carry; surviving paths shift to lunar-GA or aerocapture arrival. | Chunk-fed-spiral + direct-capture cells lose closure; LGA / aerocapture arrival paths dominate the surviving set. | Phase 6 correction changes no surviving cell. |
| H4 | **Joint encoding (1+2+3+4) reproduces titan-3's 4 cells within ±20 % delivered mass and ±15 % round-trip** — IF the framework is run at titan-3's anchors (Isp 2000, lunar-GA arrival, sp ∈ {2.4, 10}). The chunk axis must include the 50/60-t band, and the framework must offer a non-chunk-burning electric inbound at Isp 2000. | The 4 titan-3 strict cells reproduce within tolerance once anchors are aligned. | Any titan-3 strict cell disagrees > 30 % on delivered mass OR > 25 % on round-trip after anchor alignment. |
| H5 | **enceladus-r5 reproducibility is a methodological parity check only** (500 kWe is retired). The 9 cells at Cassini bus + hybrid aero + 500 kWe reproduce within ±20 %; the 6/9 shielding subset reproduces within tolerance. Cells stay retired. | enceladus-r5 cells reproduce within ±20 % delivered mass. | enceladus-r5 cells disagree > 30 %. |
| H6 (load-bearing) | **After encoding 1–4 the framework becomes matrix-replay-trustworthy.** Either the 200-t cell survives (becoming a second surviving architecture distinct from titan-3) or it collapses and the matrix returns to titan-3's 40–80-t band as the sole surviving set. Either way, residual divergences reduce to documented anchor/parameterization choices, not unexplained physics. The framework can then replace per-round Python scripts as the canonical sweep substrate (closes mimas lesson-17). | Reading-level: framework matrix-replay-trustworthy; 75 %-chunk-tow delivery anchor (matrix M-3) gets a framework-derived replacement. | Cell-by-cell diff shows persistent > 30 % disagreement on any matrix surviving cell after constraint encoding AND anchor alignment, with no identifiable root cause. |

**Worker's honest prior (frozen):** I expect H2 to be the dominant effect (the framework
gives the powerplant away for free), H3 second, H1 third. I expect the framework's 200-t
cell to COLLAPSE under joint encoding — most likely on H2 (the 20.5-t powerplant will not
fit in a 50–63-t vehicle that is already 80 % propellant) reinforced by H3. I expect the
hardest part of H4 to be the architecture-parameterization mismatch (titan-3 is
chunk-mass-centric at Isp 2000 + lunar GA; the canonical sweep is launch-vehicle-mass-centric
at Isp 800/3000), which may force a titan-3-anchored sub-sweep rather than a re-read of the
canonical sweep. If that mismatch cannot be closed by anchor alignment alone, H6 is
falsified and the divergence is a matrix-vs-framework parameterization gap to document, not
a physics bug.

---

## Method

Atomic commits per constraint (Steps 1–4), then sweeps (Steps 5–6), then diff (Step 7).

1. **Constraint 1 — reactor lifetime.** Add `reactor_lifetime_years` and
   `cumulative_full_power_burn_hours` to `VehicleState`; accumulate burn time in every
   full-power electric phase (P1 low-thrust, P4 chunk-fed / electric leg, P6 low-thrust
   capture); precondition rejects an option if cumulative would exceed `L·8760`. Ground-truth
   against `R_reactor_lifetime_vs_burn_time`.
2. **Constraint 2 — powerplant mass.** Add `m_reactor = power_kwe / sp_w_per_kg` (t) and
   `m_radiator = 5 + 0.1·reactor_kwe` (t, MARVL bundled). Charge this as a dry-mass floor:
   reject any launch/assembly state whose dry mass cannot contain bus + reactor + radiator +
   thrusters for its power class. `sp_w_per_kg` is a sweep param (default 2.4; titan-3 also
   ran 10).
3. **Constraint 3 — bus-mass floor.** Precondition rejecting dry mass below the conservative
   2000 kg bus anchor (document Cassini ~600 kg heritage as comment).
4. **Constraint 4 — vis-viva arrival.** Replace `direct_propulsive_capture_dv` with
   `√(v_inf² + v_esc_LEO²) − v_circ_LEO`. Phase 4 already at 7.7 km/s (no change).
5. **Re-run canonical sweep** post-encoding → `results/canonical_sweep_post_encoding.json`;
   diff vs `20260522T193231Z` and titan-3's 4 + 30 cells.
6. **enceladus-r5 reproduction sub-sweep** → `results/enceladus_r5_reproduction.json`.
7. **`RESULTS.md`** cell-by-cell diff + root-cause of any > 30 % divergence.
   **`READING.md`** H6 verdict + 75 %-chunk-tow delivery-anchor replacement note.

## Out of scope (per SCOPE)

New architectural cells; resolving decision points #14/#15; editing matrix HISTORY or
surviving-cell readings; per-round migration onto `waterprop.propulsion` helper pair.
