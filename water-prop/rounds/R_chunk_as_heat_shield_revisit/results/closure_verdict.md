# R-chunk-as-heat-shield-revisit — closure verdict

**Headline:** Single-pass chunk-as-heat-shield aerocapture is **structurally infeasible** across the full architecturally-relevant envelope. The matrix's aerocapture-conditional surviving cells should be reframed from "engineering-pending" to "single-pass-engineering-falsified, hybrid-engineering-pending."

---

## What this round actually found

Across an 8-chunk × 5-velocity-at-infinity × 2-tug-mass sweep (40 base cells + 8 sensitivity cells + 6 architectural intersection probes), **zero cells achieve single-pass aerocapture at periapsis ≥ 50 kilometres**. The binding constraint is **capture-feasibility itself**, not bag-thermal-survival or chunk-structural-survival as the SCOPE.md anticipated.

ICEBERG ballistic coefficients in the swept envelope (4,600–6,600 kilograms-per-square-metre) cannot dissipate the required Earth-arrival delta-velocity (3.8–7.9 kilometres-per-second) in a single atmospheric pass at any altitude that survives thermally. At the model's 40-kilometre periapsis floor, drag is sufficient — but periapsis ≤ 40 kilometres enters dense lower atmosphere where the trajectory is reentry, not aerocapture.

This is consistent with the original R-chunk-as-heat-shield's table: at periapsis 90 kilometres, single-pass delta-velocity dissipation was 285 metres-per-second — full capture would need 22 passes, not one. R-chunk-as-heat-shield was modelling multi-pass aerobraking; the "single-pass aerocapture is the only atmospheric option" sub-finding entered the matrix only via Saturn's R-chunk-as-heat-shield-revisit SCOPE.md cherry-pick.

---

## Cross-check against hyperion R-aerocapture-fast-cruise-envelope

Phoebe re-ran hyperion's Round-F STRICT no-LGA case (200-tonne chunk, 63.8-tonne tug, velocity-at-infinity 10.55 kilometres-per-second) using imported physics functions. Computed entry velocity 15.29 kilometres-per-second, ratio 1.000 to hyperion's anchor. STRICT pass = False, SACRIFICIAL_BAG pass = False. Physics agrees to four significant figures.

---

## Hypothesis grading

| Sub-claim | Pre-registered | Computed | Held |
|---|---|---|:---:|
| H-csa-a — STRICT closing region (predicted 0–2 of 40) | empty | 0 cells | YES |
| H-csa-b-chunk — SACRIFICIAL_BAG chunk upper bound (predicted 75–150 t) | undefined (region empty) | none | NO (vacuously, more pessimistic) |
| H-csa-b-vinf — SACRIFICIAL_BAG velocity upper bound (predicted 5–8 km/s) | undefined (region empty) | none | NO (vacuously, more pessimistic) |
| H-csa-c — Variant C STRICT closing cell intersection | False | False | YES |
| H-csa-d — Variant B chunk-200 intersection at any tested v_∞ | False | False | YES |
| H-csa-e — small-chunk (≤ 50 t) multi-mission flag | qualitative | none triggered | n/a |
| H-csa-f — orientation-stability conditional | not gradable iff antecedent false | antecedent false | not gradable |

**Aggregate H-csa-agg: HELD.** Three of three aggregate-relevant claims (a + c + d) all held; chunk-as-heat-shield single-pass is structurally infeasible across the architecturally-relevant envelope.

---

## Methodology lesson update

**Recurring-lesson #N (compute anchors before ranges):** Phoebe's pre-registration computed central back-of-envelope estimates for peak-g vs chunk mass, structural margin, and the bag thermal limit BEFORE writing range bands. The pre-reg was directionally correct (chunk-as-heat-shield doesn't close) but quantitatively *under-pessimistic* — the SACRIFICIAL_BAG region was predicted bounded; actually empty. The pattern continues: aerocapture-adjacent rounds in this campaign (now six in sequence: R-aerocapture, R-chunk-as-heat-shield, R-deployable-drag-skirt, R-aerocapture-fast-cruise-envelope, R-no-atmospheric-capture-baseline, R-chunk-as-heat-shield-revisit) have all falsified more pessimistically than their pre-registrations. Methodology lesson 5's two-bucket bias check holds: aerocapture is a domain where engineer-pessimism remains *insufficiently* pessimistic; pre-register MORE pessimistically than first instinct.

**Methodology-flag (carried forward):** Hyperion's `required_periapsis_altitude_km` returns the *deepest* viable periapsis (loop iterates 40→120 km, returns first hit). For aerocapture, the optimum is the *shallowest* viable periapsis (cooler heating). For hyperion's narrow Round-F sweep this didn't matter; for broader sweeps (low-β / low-velocity), the loop direction needs reversing. Phoebe's run.py uses a local override `shallowest_viable_periapsis_km`; identical result for this round (no cell captures at any altitude in [40, 120]) so the bug is latent. Recommend orchestrator add a docstring note to the upstream function.

**Methodology-flag (carried forward from phoebe's prior round):** Conditional-hypothesis grading distinguishes "not gradable" (antecedent false → no opinion expressible) from "not held vacuously" (the prediction was a bounded region, the actual region is empty — strictly more pessimistic, so falsified). Both used in this round.

---

## Implication for the matrix

The aerocapture-conditional architecture rows should be reframed. Specifically:

- **Variant C STRICT-closing cell** (faster cruise at aphelion 10.5–14 AU per Round F): doubly engineering-falsified — structural+thermal per hyperion R-aerocapture-fast-cruise-envelope, capture-feasibility per phoebe this round. Two independent failure modes.
- **Variant B chunk-200 cell** (the only L1-007-feasible Variant B per phoebe's prior R-variant-B-100t-resizing): no aerocapture-conditional rescue at any tested velocity-at-infinity. Combined with phoebe's prior round, Variant B is closed as a venture-class cell except via hybrid.
- **Year-twenty-plus megawatt all-electric end-to-end winner cell**: same chunk-as-heat-shield dependency; same falsification.

The matrix's "aerocapture-conditional" framing should become "hybrid-aerocapture-conditional, pending R-hybrid-aerocapture-aerobraking" for any cell that requires Earth aerocapture. Single-pass-conditional is closed.

---

## Open follow-ons

1. **R-hybrid-aerocapture-aerobraking** (SCOPE on main, not yet run) — single-deep-sacrificial-bag-pass + multi-pass-shallow-aerobraking. Now the only architecturally-credible aerocapture-adjacent candidate. Highest-leverage open round.
2. **R-program-class-reframe** (suggested) — given the surviving-cell list collapses to {Variant A acknowledged-collapse, Architecture-E with ≥25-year L0-05 waiver, hybrid-aerocapture-conditional}, the program may be L0-05-relaxation-required regardless of architectural choice. Worth a meta-round to surface this.
3. **Upstream physics-function fix** for hyperion's `required_periapsis_altitude_km`. Defer; not blocking.
