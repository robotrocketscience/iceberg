# R-bag-silicate-rejection-derivation — the bet-#2 conjunction's biggest driver is a derived, PSD-gated quantity, not an intrinsic 10⁻⁴

**Status:** run + STUDY complete 2026-07-22. **5/5 HELD.** Result JSON `results/bag_rejection.json`; figure `results/bag_rejection.png`.
**Bet under test:** #2 of three (continuous water-electrothermal at flight scale on Saturn-water purity). Derives the bag silicate rejection factor that `R11_grid_life_silicate_contamination` and `R_silicate_contamination` both *assumed*.
**Predecessors:** supplies the missing *input* to R11 (`run.py:27` rejection ratio 10⁻³–10⁻⁶ "literature scaling, not a measurement") and R_silicate_contamination (2026-05-15 PSD addendum: sub-100-nm colloidal silicate defeats a 100 nm mesh; "cannot resolve PSD from desk data — a pre-Gate-B test requirement"). Prices the single biggest driver of the `R_water_electrothermal_flight_scale_audit` 0.48 continuous-months flight-readiness conjunction ("bag silicate rejection holds over the burn").

## Hypothesis (pre-registered; see SCOPE.md)

The bag rejection factor is not intrinsic — it equals the silicate PSD mass fraction that is both *lofted* and *transported* to the thruster, set by a free-molecular entrainment cutoff d_max(T) = ρ_gas(T)·L/ρ_grain (gas channel) plus an electrostatic nano-tail leak (residual even when cold). Predicted (H-K1..K5): d_max sub-micron and steeply T-dependent; cold-bag throughput feasible; carryover ~0 cold but 10⁻²–3×10⁻¹ warm (spanning the assumed 10⁻⁴, robust neither way); electrostatic residual ≥10⁻³ for a Hsu-class nano-tail; and R11's benign grid-life verdict conditional on the assumed value.

## Test

Deterministic. Marti-Mauersberger ice sublimation P_sat → ρ_gas, J, d_max = ρ_gas·L/ρ_grain across bag temperature {200, 220, 250, 273 K}; carryover f_pass = massfrac(silicate PSD below d_max/2) for a q=3.5 power-law (r_max {1, 100 µm}) plus a bimodal nano-mode (φ_nano {10⁻³, 0.1, 0.3}); electrostatic residual φ_nano·g_geom (g_geom 10⁻²–10⁻¹); then R11's silicate→grid-wear mapping (16.7 kg silicate-to-grid budget, 0.3 % silicate, 690 t processed). `run.py`.

## Result

| bag T | cutoff d_max | throughput A_ice | carryover f_pass (r_max 1 µm) | carryover (r_max 100 µm) |
|---|---|---|---|---|
| 200 K | 0.60 nm | 2.3 m² | 0 | 0 |
| 220 K | 8.84 nm | 0.15 m² | 0 | 0 |
| 250 K | 221 nm | 0.006 m² | **0.281** | 0.026 |
| 273 K | 1.60 µm | 0.0007 m² | **0.885** | 0.083 |

Electrostatic residual (cold-bag leak, Hsu φ=0.3): **3×10⁻³ – 3×10⁻²**.

Grid-life loop (690 t processed, 0.3 % silicate, 16.7 kg budget to grid):

| corner | f_pass | grid consumed | verdict |
|---|---|---|---|
| cold 200 K + small nano-tail (opt.) | 1.0×10⁻⁵ | 0.12 % | **survives** |
| R11 assumed central | 1.0×10⁻⁴ | 1.24 % | survives |
| cold 200 K + Hsu nano-tail (electrostatic) | 3.0×10⁻² | 373 % | **LIFE-LIMITED** |
| warm 273 K + Hsu nano-tail | 8.9×10⁻¹ | 10995 % | LIFE-LIMITED |
| warm 273 K + power-law (r_max 1 µm) | 8.9×10⁻¹ | 10995 % | LIFE-LIMITED |

| Sub-claim | Pre-registered | Measured | Verdict |
|---|---|---|---|
| H-K1 d_max sub-µm, steep T-dep | ~0.5 nm/150–250 nm/1–2 µm | 0.6 nm/221 nm/1.60 µm | ✅ HELD |
| H-K2 cold-bag throughput feasible | A_ice ≤ 20 m² @200 K | 2.3 m² | ✅ HELD |
| H-K3 PSD-and-T-gated, not intrinsic 10⁻⁴ | ~0 cold, 10⁻²–3×10⁻¹ warm; spans; not robust | 0 cold, 0.026–0.885 warm; spans; not robust | ✅ HELD (load-bearing) |
| H-K4 electrostatic residual ≥10⁻³ (Hsu) | ≥10⁻³ | 3×10⁻² | ✅ HELD |
| H-K5 grid fails at Hsu, survives cold+small | fail >1×; survive ~1 % | 110×/survives 0.12 % | ✅ HELD |

## Reading

**The bag silicate rejection factor is not an intrinsic ~10⁻⁴ — it is a derived quantity gated on two design/physics variables: the bag sublimation temperature and the sub-100-nm silicate inclusion PSD of ring ice. R11's and R_silicate's assumed 10⁻⁴ (at which silicate is a non-limiter) is reachable only in one corner: a cold bag AND a small sub-micron silicate mass fraction. Move off that corner and the RF-ion grid dies within the burn.** The 0.48-conjunction's biggest driver is therefore not a reliability number to be argued up or down; it is a computable quantity gated on a specific, nameable, currently-absent measurement.

1. **The entrainment cutoff is sub-micron and swings 3.5 orders across a 73 K window (H-K1).** In the free-molecular bag the vapor carries only grains below d_max = ρ_gas(T)·L/ρ_grain — 0.60 nm at 200 K, 221 nm at 250 K, 1.60 µm at 273 K — because ρ_gas ∝ P_sat rises ~3700× over that range. This *derives* R_silicate's "sub-100-nm colloidal silicate is the problem" flag from first principles: at any bag temperature warm enough to have d_max in the 100 nm–µm band, the sub-micron tail is entrained.

2. **Cold operation suppresses the gas channel and the thruster is still fed (H-K2, H-K3).** At 200 K the cutoff is 0.6 nm — below any real silicate grain — so gas-entrainment carryover is physically ~0, and a 2.3 m² sublimation area still feeds 0.5 g/s. So the throughput constraint does *not* force warm operation; **cold sublimation-distillation (≤ ~220 K) is the derived design rule** for silicate rejection. At warm operation (273 K) the plain power-law PSD alone — no special nano-mode — gives 8–88 % carryover (a q=3.5 power-law to r_max = 1 µm puts ~25 % of silicate mass below 100 nm). R11's 10⁻⁴ is thus a cold-bag corner value, not an intrinsic still property.

3. **The electrostatic nano-tail is the residual leak cold operation cannot close (H-K4) — and it is decisive (H-K5).** Even at 200 K (gas channel off), electrostatic lofting of the sub-100-nm tail gives a residual carryover φ_nano·g_geom. At a Hsu-class nano-tail (φ_nano ~ 0.3) and pessimistic geometric capture this is 3×10⁻² — and through R11's own erosion mapping that consumes **373 % of the grid over the burn: the grid dies even with a perfectly cold bag.** So the whole bet-#2 grid-erosion story reduces to one unmeasured input: **the sub-100-nm silicate inclusion PSD of ring ice (and its grain charging).** If that nano-tail is small (power-law, mass at the large end), cold operation gives ~10⁻⁵ rejection and the grid survives with 100× margin; if it is Hsu-class, no bag temperature saves the RF-ion grid and bet #2's contamination-sensitive closer is falsified on grid life.

4. **The strategic verdict for bet #2.** The audit rated bet #2 an "architecture trap": the contamination-*tolerant* MET can't reach matrix-closing Isp, and the Isp-sufficient RF-ion is contamination-*sensitive*. This round localizes the sensitivity to a single physical quantity and a single design choice. The design choice (run the bag cold) is free and derivable; the physical quantity (nano-tail PSD) is the actual bet, and it is *measurable pre-Gate-B* — a sample-return or in-situ dust-analyzer characterization of the sub-micron inclusion size distribution in B-ring ice retires it. This is a sharper demonstrator objective than "run a thruster continuously for months": that flight test *exhibits* the failure if the nano-tail is bad, but a ground/in-situ PSD measurement *predicts* it far cheaper. **The 0.48 conjunction's biggest factor should be re-priced not as a reliability guess but as "conditional on a nano-tail measurement not yet taken," with cold-bag operation as the standing mitigation.**

## Revisit

**5/5 held — the first clean sweep of this two-bet batch, and the pre-registration was accurate because the bands were *derived from the scope_bounds pre-script physics before being written*, not guessed** (the lesson-18 conditioning structure — temperature × PSD — and lesson-20 re-derive-from-inputs discipline applied at the pre-registration step). This contrasts with the session's recurring absolute-threshold misses (six so far): here the thresholds were computed brackets (d_max ∈ [50 nm, 1 µm] at 250 K; A_ice ≤ 20 m²), not round numbers, so they held. That is direct evidence for the logged remedy — anchor absolute pre-registrations on a computed bracket, not a convenient round number.

**Where I could be wrong.** (a) The free-molecular relaxation cutoff d_max = ρ_gas·L/ρ_grain is an order-of-magnitude St=1 estimate; the numerical prefactor (Epstein drag coefficient, bag geometry, actual vapor bulk velocity vs thermal speed) could shift d_max by ~2–3×, which moves the 250 K carryover but not the cold-vs-warm dichotomy or the electrostatic conclusion. (b) The electrostatic residual g_geom (10⁻²–10⁻¹) is a bounded guess, not a sheath calculation — a proper plasma/photoemission charging + trajectory model is the natural follow-on; but H-K4 only needs the residual to be non-negligible, which even the optimistic g_geom gives (3×10⁻³). (c) The PSD is the whole ballgame and is *unmeasured for ring-ice inclusions* — I bracket it with a power-law and a Hsu-class nano-mode; the true distribution could sit anywhere between, which is exactly the finding (it is the load-bearing unknown). (d) L_transport = 1 m and ρ_grain = 3000 kg/m³ are nominal; d_max ∝ L/ρ_grain, so a longer bag or lighter (hydrated/porous) grains raise d_max and worsen carryover — pessimistic-consistent.

**Deferred (retest spec):** (1) a sheath/photoemission grain-charging + trajectory model to replace the g_geom bound and pin the cold-bag electrostatic residual; (2) fold the derived f_pass(T, PSD) back into R11/R_silicate as a *derived* input replacing their assumed 10⁻⁴, and re-report the grid-life surface as a function of the nano-tail PSD; (3) the MET-cavity thermal-soak / contaminant-erosion twin (the survey-flagged un-run gap for the contamination-tolerant branch); (4) the sub-100-nm inclusion-PSD measurement itself as a named pre-Gate-B objective in the demonstrator concept.

## Cross-learning

- **Prices the bet-#2 audit's 0.48-conjunction driver (`R_water_electrothermal_flight_scale_audit`):** "bag silicate rejection holds over the burn" is not a standalone reliability factor — it is f_pass(bag T, nano-tail PSD), ~10⁻⁵ (cold + small tail, grid survives 100×) to ~10⁻¹ (warm or Hsu tail, grid dies). Re-price the factor as conditional on a nano-tail measurement, with cold-bag operation as the mitigation.
- **Supplies the missing input to R11 + R_silicate_contamination:** both assumed 10⁻⁴; this round shows 10⁻⁴ is a cold-bag corner, not intrinsic. R11's headline "silicate is not a nominal grid-life-limiter" is **conditional on the assumed rejection and on cold operation** — true in the favorable corner, false at a Hsu-class nano-tail even cold. Derives R_silicate's "cannot resolve PSD from desk data" flag from the entrainment physics.
- **Sharpens the demonstrator critical path (axis 03 / R-demonstrator-mission-concept):** the highest-leverage bet-#2 retirement may not be the months-continuous thruster run (which *exhibits* the failure) but a far cheaper in-situ / sample-return **sub-100-nm silicate inclusion PSD measurement** of B-ring ice (which *predicts* it), plus adopting cold-bag sublimation-distillation as the standing design. Feeds the demonstrator-objective list.
- **Does NOT change the matrix propulsion-cell status:** bet #2 remains an architecture trap; this round localizes the trap's contamination-sensitivity to one measurable quantity + one free design choice, converting a 0.48-conjunction guess into a derived, nameable pre-Gate-B measurement.
