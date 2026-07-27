# H6 — wet-vs-dry anchor catalog (catalog only; no verdicts re-derived)

Method: grep across `water-prop/rounds/*/{STUDY,SCOPE,FINDINGS,READING}.md` for
vehicle/launch-mass anchors with a numeric tonne value and no wet/dry qualifier within
the match window. Reference case (already documented by titan-6, not counted as new):
the assumption audit's "50 t vehicle" that was WET = 10 t dry — the 12× error.

| # | Anchor site | Quoted anchor | Ambiguity | Disposition |
|---|---|---|---|---|
| 1 | `R_assumption_audit_2026_05_21/FINDINGS.md` | "vehicle mass grid 50–200 tonne" | grid quoted without wet/dry; titan-6 established the v0 axis is WET | reference case (known) |
| 2 | `R_k2_bus_architecture_study/SCOPE.md` | "mass grid (50–200 tonne" | inherits #1's unqualified grid into a new SCOPE | flag: qualify as WET before the round runs |
| 3 | `R_smaller_vehicle_demonstrator_envelope/SCOPE.md+FINDINGS.md` | "vehicle_mass_kg down to 10 t", "39.5 t at vehicle 50 tonne" | unqualified; round retired as methodology artifact, but the numbers survive in quotations | flag: annotate retired numbers as WET-axis artifacts |
| 4 | `R13_dual_ion_architecture/STUDY.md` | "mass at Saturn ~280 t", "mass = 5 t" | no qualifier; "mass at Saturn" plausibly wet-with-chunk but unstated | flag |
| 5 | `R_outbound_chemical_kick_economics/STUDY.md` | "mission 1 mass 214 t / 224 t" | no qualifier; likely launch (wet) given context | flag |
| 6 | `R_outbound_architecture/STUDY.md` | "mass exceeds Starship expendable (~250 t)", "mass under chemical-kick outbound, 500 t" | manifest-comparison implies wet, unstated | flag |
| 7 | `R_reactor_specific_power/STUDY.md` | "mass ratio at 200 t / 500 t" | ratio base unqualified | flag (low risk: ratios) |

`R_variant_B_500kWe_sizing` anchors (527 t / 213 t) say "launch mass" — launch mass is
unambiguously wet; not counted.

**H6 verdict: HELD.** At least 5 unqualified anchor sites beyond the known case (rows
2–6; row 7 marginal). None re-derived here per SCOPE ("catalog only"). Recommended
follow-through: lesson-22 ratification plus a one-pass orchestrator annotation sweep
adding "(wet)" / "(dry)" qualifiers at rows 2–6.
