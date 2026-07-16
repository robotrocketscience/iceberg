# READING — R-A14-engineering-decomposition

## Load-bearing reading

**A14 chunk-capture closure at the matrix-canonical 200 t chunk EXISTS but is conditional, razor-thin, and regime-gated on closing velocity.**

- Engineering-anchored joint at pitch-nominal **mm/s** closing velocity: **0.53 (mid)** — clears the 25 t commercial floor (threshold 0.451), does NOT clear the 30 t L0-09 floor (0.542).
- At realistic **low-m/s** autonomy: **0.41 (mid)** — **fails the 25 t floor.**
- **Demonstrator-confirmed** (Earth-orbit catch-and-contain + Saturn small-chunk): **0.69** — clears both floors.

The desk-study 0.85 anchor is too high (honest mm/s mid is a 0.62 multiplier of it). The Saturn-worker 0.46 placeholder was close at mm/s but did not name the velocity regime it assumed. **The real question is not "is 0.85 right?" but "is the operating point mm/s or low-m/s?" — and that is exactly what a ground-cheap Earth-orbit demonstrator retires.**

## Recommended amendments

**mission_graph framework:** replace the single 0.85 / 0.65–0.85 capture-efficiency anchors with a velocity-conditional, demonstrator-conditional set:
- `capture_efficiency_mm_s_undemonstrated = 0.53`
- `capture_efficiency_low_m_s = 0.41`
- `capture_efficiency_demonstrator_confirmed = 0.69`

**Matrix (decision #13, pitch staged-options reframe):** carry the 200 t closure cell as **demonstrator-conditional**, not as a standing 0.85. Re-gate iapetus tranche-1 from the external FSP-2-award gate (moot per decision #14) to an internal Earth-orbit catch-and-contain + continuous water-electrothermal demonstrator gate. See `results/iapetus_staged_options_re_gating.md`.

**Design-axis 19 (capture architecture):** the load-bearing sub-step is **containment at closing velocity** (0.78 mm/s → 0.55 high-m/s); the un-retirable cruise residual is **cinch-fatigue over 13 years** (mitigated by redundant cinches, not by any demonstrator). Sublimation/mass-loss is benign at cold passive cruise — a correction to the desk study's implicit fear.

## Highest-leverage next action

An **Earth-orbit catch-and-contain demonstrator** (deployable target masses, controlled mm/s closing) retires the three weakest/cheapest sub-steps and directly tests the mm/s-vs-low-m/s question the entire A14 joint pivots on. This is the bet-#1 retirement; pair it with a continuous water-electrothermal demonstrator (bet #2, currently un-audited) for the tranche-1 gate.
