# R-saturn-water-v2-electrolysis-departure — FINDINGS

**Worker:** worktree-172651, 2026-07-26. Pre-registration: `STUDY.md`. Artifacts:
`missions/phase4_electrolysis.py`, `missions/saturn_water_v2.py`,
`saturn_mass_demands.py` extension (all defaults inert — v1 baseline and 179-test
suite unchanged), `run.py`, `results/v2_closure_results.json`,
`results/v2_isp_boundary.json`.

## Headline

**The H₂/O₂ electrolysis departure stage is FALSIFIED at closed-loop fidelity —
within hydrogen/oxygen chemistry it closes nothing, at any power (to 300 kWe),
any harvest mass (to 1,000 t), any launcher (to ×16), in either physics arm.**
The 8.51 km/s Oberth burn at Isp 450 s demands a departure-stack propellant
fraction of 0.854 (mass ratio 6.87), while the self-consistent vehicle's
chunk-scaled hardware (capture + structure + margin + cryo tankage, even with
harpoon capture, path-conditional TPS removed, and 33 W/kg power) caps the
achievable fraction at ~0.83 asymptotically — and ~0.75 at record settings.
Quantified at the best probed cell: the burn needs 527 t of water; a 500-t chunk
at 0.85 capture efficiency supplies 425 t. **This retires the analytic round's
closure claim** (R-electrolysis-departure-stage's 146–437 kWe softening): that
round did not charge the chunk-scaled hardware self-consistently and implicitly
assumed harvested water beyond the 482-t single-chunk cap — the same
open-loop-optimism error class the wet-vs-dry audit chain has caught before.

**The architecture revives at Isp ≥ ~750 s on the impulsive stage** — i.e.,
electrolysis feeding a hydrogen nuclear-thermal (~900 s) or LANTR-class
oxygen-augmented (~750 s) engine instead of an H₂/O₂ combustion chamber:

- At 900 s: **closes the 30-t commercial floor in BOTH arms — including honest
  physics — delivering up to 89.6 t** (200 kWe, 33 W/kg, harpoon, no-TPS,
  1,000-t harvest, ×16 launcher). 0 strict-15-yr paths; 511 waiver-25-yr paths.
- At 750 s: 63 t. At 700 s and below (all H₂/O₂ chemistry): zero.
- The impulsive burn's independence from the electric-spiral penalty makes this
  the ONLY departure mode found anywhere in the campaign that closes the 30-t
  floor under the honest arm without a 3,000-s electric thruster.

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H-V1 | v2 restores ≥1 arrival under Arm B at ≤200 kWe, ≤×8 | **FALSIFIED** | 0 everywhere at 450 s; the analytic band does not survive self-consistent mass |
| H-V2 | Electrolysis beats electric spiral at matched cells | **MOOT at 450 s; HELD at ≥750 s** | v1 matched grid all-zero; v2-at-900-s is the only closing departure |
| H-V3 | Modal failure shifts P4 → P6 (hot arrival) | **FALSIFIED** | P4 remains modal — chemistry never survives departure to expose the arrival wall; at 900 s arrivals pass P6 via LGA tour + chemical trim on leftover propellant |
| H-V4 | 30-t floor closes at 450 s + chunk ≥200 t + ≥100 kWe (launch elastic) | **FALSIFIED as posed; HELD in modified form** | requires Isp ≥750–900 s (beyond H₂/O₂ chemistry), harvest 500–1,000 t (beyond single-chunk cap), harpoon + path-conditional TPS, ≥33 W/kg, ×16 launch |
| H-V5 | 3-yr dwell gate kills Kilopower-class | **HELD** | 30 kWe: 8.7-yr production for a 342-t load (unit test); 200 kWe: ~2.7 yr for ~700 t — fits |

## What this adds to the closure boundary (amends the inversion round's List 2)

A SECOND closing corridor under honest physics, alternative to the 3,000-s
electric path:

| Lever | Value required |
|---|---|
| Impulsive-stage Isp on water-derived propellant | **≥750 s (LANTR-class) / 900 s (H₂-NTP)** — electrolysis + liquefaction feeding nuclear-thermal; H₂/O₂ combustion (≤465 s) categorically insufficient |
| Harvested water per mission | **500–1,000 t** — beyond the 482-t B-ring single-chunk cap ⇒ **multi-chunk harvesting is load-bearing** (R-multi-chunk-per-mission: never run) |
| Power | ≥150–200 kWe (dwell ≤3 yr; production ~2.7 yr at 200 kWe) — "not Kilopower" re-confirmed |
| Specific power | ≥33 W/kg |
| Capture architecture | harpoon-class mass (0.05 kg/kg) + path-conditional TPS (fidelity-H4 fix, jettison/no-carry on propulsive-arrival paths) |
| Launcher | ×16 record (≈1,000-t class assembled) at f = 0.80 — largely an artifact of the frozen fraction; per-phase accounting would cut it substantially (un-run fidelity round) |
| Round-trip | 25-yr waiver only; no strict-15-yr path exists in this corridor |

TRL note: nuclear-thermal propulsion is TRL 3–4 (DRACO cancelled May 2025;
0-of-6 US space-fission base rate applies), and an electrolysis-fed NTP with
in-situ liquefaction has never been studied as an integrated system — TRL 2.
This corridor trades the nonexistent 3,000-s water-compatible electric thruster
for a nonexistent water-to-hydrogen NTP chain; it widens the option space
without raising its floor.

## Residuals

1. Tank jettison, boiloff, and shadow-shield placement excluded (STUDY) — all
   flatter the stage; verdict-safe for the falsification, but the 750–900 s
   corridor should carry them before being quoted as more than an existence
   proof.
2. The liquefaction power adder (~44 kWe floor at scale, DOE band) is inside the
   6.7 kWh/kg energy figure only approximately; vendor-anchoring remains the
   named follow-on from the analytic round.
3. Arm A and Arm B produce identical v2 numbers at the probed cells (the
   impulsive path is untouched by the spiral anchor and lifetime toggles at
   these dwells) — the corridor is posture-robust, which is its main virtue.
4. Multi-chunk harvesting (2–5 captures per mission) is now the binding
   capture-side requirement and has no round; its GNC/containment implications
   at 500–1,000 t aggregate are unstudied.

## Addendum (latest+29c, lesson-25 ledger walk + consistency probes)

The ratified lesson-25 ledger walk (`R_closure_boundary_inversion/ledger_walk.py`)
exposed an inconsistency in the corridor cell as first quoted: the closing path
used hybrid aerocapture at Earth arrival while the vehicle was configured with
`plans_aerocapture=False` (no TPS mass). Probes
(`results/v2_tps_consistency_probe.json`,
`results/v2_selfconsistent_nonaero_grid.json`):

- With TPS charged (consistent with an aerocapture arrival): the corridor
  collapses to 5.7 t — the 89.6 t figure does not survive.
- **Self-consistent corridor (no TPS, propulsive/lunar-gravity-assist arrival —
  no aerocapture anywhere on the path): the 30-t floor still closes.** Smallest
  closing point: **×16 launch / 150 kWe / 500 t harvest → 32.6 t delivered**;
  ×16 / 200 kWe / 1,000 t → 89.2 t; ×32 / 500 kWe / 2,000 t → 169.8 t
  (17.7–18.9 yr, waiver-only). Power is locally non-monotone (300 kWe delivers
  less than 150–200 kWe at 500 t — powerplant mass eats the mass ratio).

The corridor statement in the headline is therefore amended: the citable
self-consistent numbers are **32.6–89.2 t at 150–200 kWe / 500–1,000 t
harvest / ×16 launch**, arriving propulsively via the lunar-gravity-assist
tour. R-departure-anchor-resolution (same day) independently makes this
corridor the ONLY 30-t-closing corridor under honest resolved physics.
