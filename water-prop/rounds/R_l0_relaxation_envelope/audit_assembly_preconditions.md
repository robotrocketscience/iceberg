# Assembly-precondition audit — verdict memo

**Worker:** rhea-5 (`iceberg-rhea-5`, worktree 131949)
**Date:** 2026-06-12 (work order dispatched 2026-05-26 latest+25; re-dispatched 2026-06-12 by project owner)
**Work order:** `~/.claude/handoffs/iceberg-saturn-to-rhea-20260526-assembly-audit.md`
**Question:** Are the 180 P0b_assembly failures in the `saturn_water_v1` closed-loop sweep a walker option-pairing bug, or honest precondition rejections?
**Audit artifact:** `audit_assembly_preconditions.py` (this directory; writes `results/audit_assembly_preconditions.json`, not committed)

## Verdict: NO BUG — the walker enumeration is correct; the 180 P0b failures are honest precondition rejections.

Decision rule (from the work order): a bug requires at least one multi-launch path
prefix that reaches P0b with NO sibling branch continuing through
`autonomous_assembly` — i.e., real mission designs lost at P0b.

Result: **zero orphaned prefixes.** All 90 multi-launch prefixes that reach
P0b generate exactly 2 stub records each (`passthrough_no_assembly` rejects on
the pending-assembly flag; `depot_relay_assembly` rejects because
`existing_leo_depot` is absent from base params — both rejections correct) and
every one of the 90 continues through `autonomous_assembly` into Phase 1.
`autonomous_assembly` never appears in the failure list because it always
passes — exactly as the work order suspected.

## What "0 of 1744" actually means (sharpened)

The 1744 figure counts enumeration records, not mission designs. Full accounting:

| Bucket | Records | Nature |
|---|---:|---|
| P0 launch-cap rejections | 660 | honest: derived wet vehicles 138–708 t vs caps (Falcon Heavy 63.8 t, Starship 100 t, multi-Falcon-2 100 t fail in all 150 cells; multi-Falcon-4/6 fail in the heavier cells) |
| P0b stub rejections | 180 | honest: structurally-incompatible (P0, P0b) option pairings in the open enumeration — **not lost designs** |
| Genuine downstream mission attempts | 904 | all routed multi-Falcon → autonomous assembly; all die at deep-space preconditions |
| Feasible leaves (complete the phase graph) | **0** | no path even reaches closure-predicate judgment |

The honest restatement for the matrix: **904 walked mission designs, 0 complete
the phase graph, 0 close.** The structural verdict survives this audit
unchanged; the relaxation-envelope question stays gated on titan-7's
R-vehicle-mass-fidelity-refinement exactly as SCOPE'd.

## Where the 904 genuine attempts die

| Phase | n | Dominant kills |
|---|---:|---|
| P1_LEO_to_Saturn | 445 | kick wet mass exceeds launch-manifest dry envelope (180); chemical propellant short for trans-Saturn injection (90 + 90 reduced); electric thruster needs ≥ 20 kWe, have 1/10/11 (65); burn-time vs coast window (20) |
| P4_Saturn_departure | 408 | chemical trans-Earth-injection propellant short (136); power < 30 kWe for chunk-fed water-microwave-electrothermal / electric leg (144); **chunk water insufficient for the return leg (121; shortfall median 5.2×, range 2–275×)**; kick propellant (7) |
| P2_Saturn_capture | 36 | gravity-assist capture options gate on arrival v_inf ≥ 3.0–4.0 km/s but see 0.50 (30); low-thrust capture power (6) |
| P1b_cruise_ops | 15 | gravity-assist options gate on ballistic-class arrival v_inf (15) |

Two physics observations fall out (neither alters this audit's verdict):

1. **The 30/55-kilowatt-electric paths — the only ones passing both power
   gates — die on chunk-water arithmetic at P4**: even a fully-captured chunk
   carries 2–275× (median 5.2×) less water than the derived 120 t-dry vehicle
   needs for the return leg. This is the closed-loop mass coupling doing its
   job, and is consistent with locked audit finding 1 (capture efficiency) and
   the titan-6 dry-mass derivation.
2. **Observed, not investigated:** P2/P1b gravity-assist options gate on high
   arrival v_inf (≥ 3.0–4.0 km/s) while the surviving branches arrive at
   0.50 km/s. Phoebe's R-saturn-moon-ga-ephemeris already flagged comment
   inversion on this gate; whether the gate itself should admit low-v_inf
   arrivals is a phoebe/orchestrator question, not rhea's. 45 records ride on
   it — not verdict-changing (those branches still face P4's water wall).

## Incidental fix shipped with this audit

`relaxation_sweep.py:65` read `r.final_state`, an attribute `WalkResult` does
not have (`leaf_state` is the field). Latent `AttributeError`, masked because
the guard clause requires a closing path and nothing closes. Fixed in this
branch so the sweep does not crash on the day something closes.

## Prediction scorecard (work order outcomes)

- Work order outcome 1 (real fix, opens 180 paths): **did not obtain.**
- Work order outcome 2 (no bug, tight preconditions, walker correct): **obtained**, with one sharpening the work order did not predict — the 1744 denominator mixes 840 enumeration stubs with 904 genuine attempts, so the orchestrator's headline "0 of 1744 paths arrive" was directionally right but the denominator overstates the walked design space by ~2×. Recommended phrasing going forward: "0 of 904 walked designs complete the phase graph."
