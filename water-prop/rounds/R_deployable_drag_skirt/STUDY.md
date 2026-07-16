# R-deployable-drag-skirt — can an inflatable ballute rescue Earth aerocapture for ICEBERG?

**Status:** complete.

## Question

R-chunk-as-heat-shield (commit c330fe2) established that ICEBERG's bare-chunk ballistic
coefficient of beta = mass / area ≈ 4,000 kg/m² (50 t chunk + 5 t tug + bag, ~12.5 m²
frontal area) makes Earth atmospheric capture infeasible at every altitude: no
periapsis exists where the bag survives thermally AND the pass count is tractable.
The reason is geometric. ICEBERG has 40× the ballistic coefficient of Mars Global
Surveyor.

The obvious counter-move is to grow the drag area on demand. Inflatable
decelerators (Hypersonic Inflatable Aerodynamic Decelerators (HIADs), ballutes,
mechanically deployed ribs) have real flight heritage: LOFTID (Low-Earth Orbit
Flight Test of an Inflatable Decelerator) flew a 6 m article in 2022 with beta ≈ 42
kg/m² through Mach 25 reentry; HIAD-2 ground-test articles target ~500 kW/m² peak
heat flux tolerance; IRDT (Inflatable Reentry and Descent Technology, Russian
flights 2000-2005) demonstrated the concept at 2.3 m.

**The question this round answers:** can a deployable drag skirt size up to drop
ICEBERG's effective ballistic coefficient by enough to clear the aerocapture
corridor (beta ≈ 200-500 kg/m²) or even the aerobraking corridor (beta ≈ 100
kg/m²)? And if it can geometrically, does the thermal protection on the skirt
itself stand up to interplanetary-return entry velocities (~12.6 km/s, much higher
than LOFTID's ~7.6 km/s)?

The honest result is partly counter-intuitive: the **mass closure is easy** but the
**thermal closure is the binding constraint**, because v³ scaling on Sutton-Graves
heating from v = 7.6 to v = 12.6 km/s multiplies peak heat flux by ~4.6×, which
overwhelms the 1/sqrt(R_nose) benefit of a bigger skirt.

## Pre-registered hypothesis (H-dds)

**Aggregate (H-dds-agg):** A deployable drag skirt rescues aerocapture for ICEBERG.
Mass closure is straightforward (skirt sizes to ~250-500 m² at ~5-15 kg/m² areal
density = 1.5-7.5 t, fits within the 5 t tug allocation or its growth margin).
Thermal closure is plausible because a wider deployed envelope gives a larger
effective nose radius (R_nose ≈ 5-15 m), pulling stagnation heat flux back
into the LOFTID / HIAD-2 demonstrated capability envelope (~300-500 kW/m²).

**Pre-registered sub-claims:**

| Sub-claim | Predicted | Falsification |
|---|---|---|
| H-dds-a — Area needed for beta = 200 kg/m² at 55 t vehicle mass | 250-300 m² (16-20 m diameter) | outside ±25% |
| H-dds-b — Area needed for beta = 100 kg/m² at 55 t vehicle mass | 500-600 m² (25-28 m diameter) | outside ±25% |
| H-dds-c — Skirt mass at HIAD/LOFTID areal density (5-15 kg/m²), beta = 200 kg/m² | 1.5-4 t | outside ±50% |
| H-dds-d — Skirt mass at HIAD/LOFTID areal density (5-15 kg/m²), beta = 100 kg/m² | 3-9 t | outside ±50% |
| H-dds-e — Mass budget closure | skirt fits within 5 t tug budget OR within 10 t growth budget for at least one of the (beta, areal density) cells | falsified if no (beta, areal density) cell fits 10 t |
| H-dds-f — Peak heat flux on skirt at 90 km, v_inf = 6 km/s, beta = 200 kg/m² | 300-800 kW/m² (R_nose ~ 10 m pulls flux down) | outside ±50% |
| H-dds-g — Thermal capability margin: peak flux fits inside HIAD-2 design tolerance (~500 kW/m²) for at least one (beta, areal density) cell | yes | falsified if every cell exceeds HIAD-2 design |
| H-dds-h — State B (aerocapture) rescue verdict | partial rescue (aerocapture-class beta = 200-500 closes with margin; aerobraking-class beta = 100 marginal) | falsified if neither aerocapture nor aerobraking closes |

**Aggregate decision rule:**

- If H-dds-agg holds (mass + thermal both close): State B is **rescued**.
  Architecture matrix collapses to all-electric every era as in R-aerocapture, but
  with the deployable skirt added as a new line item in the tug mass budget.
- If only mass closes but thermal does not: State B is **partially rescued** at
  aerobraking velocities (lower v) but not aerocapture from a hyperbolic
  interplanetary return.
- If neither closes: State B is **killed**. The architecture defaults to the
  no-atmospheric-capture matrix (R-outbound-architecture baseline).

## Method

**Skirt sizing (geometric):** for a target beta and vehicle bare mass M_bare = 55 t,
the skirt sizes by fixed-point iteration so the deployed area A satisfies

  A × beta_target = M_bare + sigma × A    =>    A = M_bare / (beta_target - sigma)

where sigma is the skirt's areal density (kg/m²). This iterates because the skirt
adds mass which then raises the area requirement. Below sigma >= beta_target, no
solution exists — the skirt would need to be infinitely large.

**Skirt thermal (Sutton-Graves):** the skirt is modeled as a blunt aerodynamic
decelerator with effective stagnation-point nose radius R_nose_eff = 0.5 × D_skirt
(conservative — sharper than a hemisphere, blunter than a flat disc). At 90 km
periapsis, atmospheric density 1e-4 kg/m³, v_inf = 6 km/s:

  v_entry = sqrt(v_inf² + 2 × GM_Earth / r_periapsis) ≈ 12.6 km/s

  q_conv = K_SG × sqrt(rho / R_nose) × v_entry³
  q_rad ≈ 0.5 × q_conv × max(1, (v_entry / 12) ²)
  q_total = q_conv + q_rad

The 1/sqrt(R_nose) factor means a 28 m skirt with R_nose = 14 m has peak flux
sqrt(14/2) ≈ 2.6× lower than a 2 m bare chunk at the same conditions.

**Heritage anchors:**

| Mission | Year | Diameter | Vehicle mass | Beta | Peak flux |
|---|---:|---:|---:|---:|---:|
| LOFTID | 2022 | 6 m | 1.2 t | 42 kg/m² | ~350 kW/m² measured |
| HIAD-2 (ground test) | ongoing | 6 m | n/a | n/a | ~500 kW/m² design |
| IRDT | 2000-2005 | 2.3 m | 110 kg | 90 kg/m² | ~200 kW/m² |
| Mars Global Surveyor | 1996-1999 | n/a | 1,030 kg | ~100 kg/m² | ~3 kW/m² (aerobraking) |

**Areal density bands:** 5 kg/m² (optimistic), 10 kg/m² (baseline), 15 kg/m²
(conservative). LOFTID's public-literature inflatable + thermal protection layer is
in this range; the full LOFTID vehicle including bus reads heavier but that
includes elements ICEBERG would not need to duplicate (the IAD is the skirt; the
chunk and tug are the bus).

**Validity caveats:**

- Sutton-Graves is approximate. Radiative-heating estimate is rough. Real entry
  trajectory design needs CFD + radiation transport. Numbers good to factor of ~2.
- R_nose_eff = 0.5 × D_skirt is a modeling choice. For a truncated-cone IAD the
  effective stagnation radius can be smaller (depending on the angle of the
  forward-facing surface and where the bow shock attaches). If the real R_nose is
  half of this assumption, heat flux goes up by sqrt(2) = 1.4×.
- Hyperbolic entry velocity from interplanetary return (~12.6 km/s) is well above
  LOFTID's LEO-reentry regime (~7.6 km/s). Linear extrapolation of heritage
  thermal capability is not rigorous. **The v³ scaling makes this the binding
  question of the round.**
- Areal density 5-15 kg/m² for hypersonic-rated inflatable thermal protection
  is from public literature on LOFTID and HIAD-2; for an entry environment 2-5×
  more aggressive than LOFTID, the areal density required is plausibly higher
  (the thermal protection has to be thicker / heavier per area). This round does
  not iterate on that — it takes LOFTID-class areal density and asks whether
  the thermal closure even holds before worrying about the corrected mass.
- The skirt is assumed to deploy successfully and remain aero-stable. Deployment
  and tumbling-mode stability are separate engineering programmes not modeled
  here.

## Result

### Bare ICEBERG reference

- Bare vehicle: 55 t over 12.5 m² → **beta = 4,400 kg/m²** (consistent with the
  4,000 kg/m² stated in R-chunk-as-heat-shield within rounding).
- Bare-chunk peak heat flux at 90 km, v_inf = 6 km/s, R_nose ≈ 2 m:
  **~3,800 kW/m²** (R-chunk-as-heat-shield mode A reported 4,434 kW/m² with a slightly
  different nose-radius assumption — same order, factor-of-2 model uncertainty
  documented in both rounds).

### Mass closure — required area, diameter, and skirt mass

| Target beta | Areal density | Skirt area (m²) | Skirt diameter (m) | Skirt mass (t) | Vehicle total (t) | Actual beta |
|---:|---:|---:|---:|---:|---:|---:|
| 500 | 5 | 111 | 11.9 | 0.56 | 55.6 | 500 |
| 500 | 10 | 112 | 12.0 | 1.12 | 56.1 | 500 |
| 500 | 15 | 113 | 12.0 | 1.70 | 56.7 | 500 |
| 200 | 5 | 282 | 18.9 | 1.41 | 56.4 | 200 |
| 200 | 10 | 289 | 19.2 | 2.89 | 57.9 | 200 |
| 200 | 15 | 297 | 19.4 | 4.46 | 59.5 | 200 |
| 100 | 5 | 579 | 27.1 | 2.89 | 57.9 | 100 |
| 100 | 10 | 611 | 27.9 | 6.11 | 61.1 | 100 |
| 100 | 15 | 647 | 28.7 | 9.71 | 64.7 | 100 |

**Mass closure holds.** At baseline 10 kg/m² areal density:
- aerocapture-aggressive (beta = 500): ~1.1 t skirt → fits inside 5 t tug budget.
- aerocapture-nominal (beta = 200): ~2.9 t skirt → fits inside 5 t tug budget.
- aerobraking-class (beta = 100): ~6.1 t skirt → does NOT fit inside 5 t tug, but
  fits inside a 10 t growth budget. Pushes the inbound vehicle dry-mass column of
  the architecture matrix by ~10% per cell.

### Thermal closure — peak heat flux on the skirt at 90 km, v_inf = 6 km/s

| Target beta | Areal density | D_skirt (m) | R_nose (m) | Peak q (kW/m²) | T_eq @ eps=0.8 (K) | LOFTID demo (≤350)? | HIAD-2 design (≤500)? |
|---:|---:|---:|---:|---:|---:|:--:|:--:|
| 500 | 5 | 11.9 | 6.0 | 2,224 | 2,634 | NO | NO |
| 500 | 10 | 12.0 | 6.0 | 2,221 | 2,633 | NO | NO |
| 500 | 15 | 12.0 | 6.0 | 2,217 | 2,633 | NO | NO |
| 200 | 5 | 18.9 | 9.5 | 1,769 | 2,492 | NO | NO |
| 200 | 10 | 19.2 | 9.6 | 1,753 | 2,486 | NO | NO |
| 200 | 15 | 19.4 | 9.7 | 1,738 | 2,481 | NO | NO |
| 100 | 5 | 27.1 | 13.6 | 1,479 | 2,378 | NO | NO |
| 100 | 10 | 27.9 | 13.9 | 1,454 | 2,368 | NO | NO |
| 100 | 15 | 28.7 | 14.4 | 1,431 | 2,358 | NO | NO |

**Thermal closure fails in every cell.** Best case (beta = 100, 15 kg/m², R_nose
= 14.4 m) is ~1,430 kW/m² — still **~4× the LOFTID 2022 demonstrated flux** and
**~3× the HIAD-2 design tolerance**. Radiative equilibrium temperature on the
skirt is ~2,400 K in the best case, far above the polyimide / Vectran / Mylar
laminate stack's continuous-use limit (~700 K).

The reason heritage doesn't close it: ICEBERG re-enters from a hyperbolic
interplanetary trajectory at v_entry ≈ 12.6 km/s. LOFTID flew an orbital reentry
at ~7.6 km/s. The Sutton-Graves convective term scales as v³, so the velocity
delta alone multiplies flux by (12.6/7.6)³ ≈ 4.6×. The R_nose benefit
(sqrt(R_nose_skirt / R_nose_loftid) ≈ sqrt(14 / 0.4) ≈ 6) helps in nose-radius
terms, but LOFTID had a 6 m diameter and effective R_nose ~ 3 m, not 0.4 m, so the
nose-radius gain over LOFTID is only ~sqrt(14/3) ≈ 2.2× heat-flux reduction. Net:
4.6× from velocity ÷ 2.2× from nose radius ≈ 2× the LOFTID demonstrated flux,
which is what the numbers show.

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-dds-a — area for beta = 200 | 250-300 m² | 282-297 m² | held |
| H-dds-b — area for beta = 100 | 500-600 m² | 579-647 m² | held (just above band) |
| H-dds-c — skirt mass at beta = 200 | 1.5-4 t | 1.4-4.5 t | held |
| H-dds-d — skirt mass at beta = 100 | 3-9 t | 2.9-9.7 t | held |
| H-dds-e — mass budget closure | at least one cell fits | every cell fits 10 t; most fit 5 t | held |
| H-dds-f — peak flux on skirt at beta = 200 | 300-800 kW/m² | 1,738-1,769 kW/m² | **falsified high** by ~2-6× |
| H-dds-g — at least one cell fits HIAD-2 design (≤500 kW/m²) | yes | no — every cell exceeds it by ≥3× | **falsified** |
| H-dds-h — State B verdict: partial rescue | partial | no rescue at v_inf = 6 km/s hyperbolic entry | **falsified — full kill** |

**Aggregate H-dds-agg: falsified.** Mass closure holds (H-dds-a through H-dds-e
all held), but thermal closure on the skirt fails at every (beta, areal density)
cell explored (H-dds-f, H-dds-g, H-dds-h all falsified). The v³ scaling from
interplanetary return velocity overwhelms the R_nose benefit of a larger
deployed envelope.

## Reading

**State B (aerocapture) is killed for ICEBERG at the v_inf = 6 km/s post-lunar-tour
hyperbolic entry condition with current-heritage inflatable thermal protection.**
This is the headline finding.

The result was not obvious going in. The pre-registered hypothesis was the
honest engineering intuition: LOFTID flew, HIAD-2 is in active development for
exactly this kind of mission, areal density is well-characterised, and a 25-30 m
inflatable is within the same order of magnitude as articles already flown. The
mass closure works out cleanly. What the pre-registered hypothesis missed is
that LOFTID's heat flux envelope is set by its **velocity regime**, not its
**diameter**, and ICEBERG's interplanetary return is ~1.7× faster than LOFTID's
LEO reentry. Sutton-Graves is v³, so 1.7× faster is ~5× more heat flux.

Three observations the result actually supports:

1. **The heritage doesn't transfer.** LOFTID is a tested article and gives a
   real performance envelope, but that envelope was demonstrated at LEO reentry
   velocity. Extending the same areal density and stagnation heating model to
   12.6 km/s entry puts the skirt thermal load 3-6× above demonstrated
   capability. This is a thermal-protection-research question, not a
   sizing-and-deployment-mechanism question.

2. **Slower entry would change the verdict.** If v_inf at Earth could be
   reduced from 6 km/s to ~3 km/s (via a longer outbound/inbound trajectory or
   additional lunar-tour passes), v_entry at 90 km drops from 12.6 to ~11.4 km/s.
   That's only ~25% off in v, but the v³ factor pulls flux down by ~30%. Best
   case (beta = 100, 15 kg/m²) would still be ~1,000 kW/m² — still 2-3× LOFTID.
   To get inside LOFTID-demonstrated capability, v_inf would need to drop near
   0, i.e. propulsive matching to near-LEO before atmospheric entry. At that
   point the propulsive delta-v already approaches the all-propulsive
   architecture's inbound budget, and the atmospheric capture is no longer
   saving meaningful delta-v.

3. **The architecture decision matrix should treat aerocapture as off-table
   absent a thermal-protection breakthrough.** Specifically: a next-generation
   IAD class capable of ~2 MW/m² peak flux (a 4× advance over HIAD-2 design
   tolerance) would bring beta = 100 inside its envelope. NASA's HIAD next-gen
   research targets are in this range, but no flight article exists. The
   architecture matrix should not assume this rescue.

**What this round closes:**

- The "what if we add an inflatable ballute?" question that R-chunk-as-heat-shield
  left open. The answer is: it doesn't rescue aerocapture at this entry velocity
  with current thermal-protection technology.
- The mass-budget question: skirt mass is manageable (1-10 t depending on
  ambition), so if a thermal-protection breakthrough did arrive, the rest of the
  architecture could absorb it without restructuring.

**What this round still does not close:**

- **Sub-hyperbolic entry trajectory.** If the inbound propulsion stage burns
  down to v_inf < 2 km/s before the atmospheric pass, v_entry drops to ~11 km/s
  and Sutton-Graves drops by ~35%. Combined with a 30 m skirt, that may cross
  into the HIAD next-gen research envelope (~2 MW/m²). The propulsive delta-v
  cost of doing this and the trip-time penalty are not modeled here.
- **Magnetic / plasma-assisted decelerators.** Magnetoshell aerocapture, plasma
  parachute, etc. — concepts that decelerate without a physical wetted
  surface, in principle removing the thermal-protection constraint. Pre-flight,
  none of these have flown. R-magnetoshell-aerocapture would size that.
- **Mass-margin propagation.** If the architecture matrix is built assuming a
  6-10 t skirt anyway (as future-proofing for the possibility that thermal
  protection improves), every inbound-vehicle cell grows by ~10-15%. That
  ripples into reactor sizing and trajectory closure. Not done here.

## Revisit clause

H-dds-a through H-dds-e held (mass closure works as predicted). H-dds-f, H-dds-g,
H-dds-h falsified (thermal closure fails by 3-6×). **Aggregate H-dds-agg
falsified: deployable drag skirt does not rescue State B at v_inf = 6 km/s with
LOFTID / HIAD-2 class thermal protection.**

**Propagations to `ARCHITECTURE-DECISION-MATRIX.md`:**

1. **State B (aerocapture) is now closed.** The R-aerocapture conditional
   ("all-electric every era *if* aerocapture works") had three rescue paths after
   R-chunk-as-heat-shield: sacrificial bag, chunk-as-heat-shield with bag
   retraction, or deployable drag skirt. The deployable drag skirt path is
   eliminated by this round. The remaining two paths are (sacrificial bag, which
   abandons reuse) and (chunk-as-heat-shield, which still has unresolved
   geometric stability and orientation questions). Both are research-level
   open, not engineering-level closed.

2. **Architecture matrix defaults back to no-atmospheric-capture baseline.**
   Until a thermal-protection breakthrough or sub-hyperbolic entry trajectory is
   demonstrated, the matrix should use the R-outbound-architecture / R-inbound
   propulsive-only architecture as the load-bearing reference. The "all-electric
   every era" matrix overlay is an upside scenario, not the default.

**Next-round candidates:**

- **R-sub-hyperbolic-entry:** what is the inbound propulsive delta-v cost of
  burning down v_inf to ~2 km/s before the atmospheric pass? Does the trip-time
  penalty fit inside the 14-year ceiling?
- **R-magnetoshell-aerocapture:** can a magnetic decelerator avoid the
  thermal-protection bottleneck entirely? This is research-grade physics; the
  round would size the magnet, power requirement, and entry corridor without
  pretending the technology is flight-ready.
- **R-no-atmospheric-capture-confirm:** explicitly re-derive the architecture
  matrix assuming State B is off the table. Cross-check that the propulsive-only
  inbound architecture still closes economically (R-financing-capital-stack
  built its model on State A, so this should already be the load-bearing
  scenario, but it's worth a confirmation pass).
