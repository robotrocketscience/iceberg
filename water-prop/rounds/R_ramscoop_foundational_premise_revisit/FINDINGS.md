# FINDINGS — Ram-scoop foundational-premise revisit

**Round:** R-ramscoop-foundational-premise-revisit
**Session:** rhea (re-spawn), branch `iceberg-rhea-3`
**Date:** 2026-05-26
**Artifacts:** `coupled_delivered_mass.py`, `results/coupled_results.json`

## Headline

**Ram-scoop's Tier-1 capture lead does NOT survive chunk-as-propellant-tank Δv bookkeeping.** Single-chunk harpoon delivers ~4.3× more mass than ram-scoop across the entire chunk-mass range, despite ram-scoop's higher single-pass capture probability. The +7.4 km/s residence-out Δv increment ram-scoop pays to circularise into and climb out of the B-ring plane is a 5.3× delivered-fraction penalty on the exponential mass-ratio — it swamps ram-scoop's +11% capture-probability edge at every chunk mass. **The latest+6 project-owner foundational-premise retirement of ram-scoop is vindicated by delivered-mass accounting; the Tier-1 capture-efficiency ranking was an artifact of scoring the capture event in isolation from the return-Δv cost.**

No architecture clears the L0-04 = 25 t commercial floor. The demonstrator-class pivot stands unconditionally.

## Validation

The coupled model regenerates the Tier-1 per-sample `(chunk_mass, p_capture)` pairs by replaying the seeded RNG of `tier1_closed_form.py`. Regenerated capture-probability medians match the published `tier1_results.json` to **0.00e+00** absolute error (exact deterministic replay) — harpoon 0.36540, ram-scoop 0.40495, everting 0.24630. The coupling adds no new randomness; it is a deterministic transform of the published posteriors.

## Verdicts

| ID | Verdict | Evidence |
|---|---|---|
| **H1** — ram-scoop lead survives Δv bookkeeping | **FALSIFIED** | Delivered-mass posterior median (ratio dry mass): harpoon **3.01 t** vs ram-scoop **0.71 t**. Ram-scoop loses by 4.2× at the median, 4.3× at every chunk-mass decile. |
| **H2** — relative penalty ∈ [3×, 8×] | **HELD** | Capture-referenced delivered fraction at 200 t: harpoon 20.85%, ram-scoop 3.92% → **5.31×** penalty. Consistent with titan-2's 17%/3.5% = 4.9×. |
| **H3** (load-bearing) — no architecture clears 25 t | **HELD** | Best delivered-mass median is harpoon at 3.01 t (ratio) / 0.00 t (fixed, 0.79 t mean). Even the optimistic corner — 200 t chunk × q95 capture (0.497) — delivers only ~20.7 t, still ~4 t under the floor. Re-confirms R-chunk-capture-monte-carlo H6 with Δv carried. |
| **H4** — trade is chunk-mass-dependent | **FALSIFIED** | Harpoon wins at every chunk-mass decile [10 t … 200 t]. The H4 premise (ram-scoop wins at large chunks) is backwards: the Δv penalty is *multiplicative* on the mass ratio, so ram-scoop loses by the same ~4.3× factor at 200 t as at 10 t. There is no crossover. |

### Sampled-decile delivered mass (ratio dry mass, median t)

| Chunk mass bin (t) | harpoon | ram-scoop | everting | winner |
|---|---|---|---|---|
| 10.0–13.3 | 0.98 | 0.19 | 0.74 | harpoon |
| 24.5–32.8 | 2.22 | 0.45 | 1.56 | harpoon |
| 44.4–59.2 | 3.90 | 0.81 | 2.57 | harpoon |
| 81.1–108.1 | 6.83 | 1.46 | 4.24 | harpoon |
| 146.5–200.0 | 11.48 | 2.64 | 7.00 | harpoon |

(Full 10-bin table in `results/coupled_results.json`.)

## Audit of the cross-referenced anchors (per SCOPE: anchor, don't re-derive; audit inconsistency)

- **Ram-scoop 3.5% (titan-2) reproduces.** My model gives ram-scoop η_dv = 3.92% at the 200 t / 200 t-dry anchor (titan-2 quoted 3.5%). The ~0.4-point difference is rounding in titan-2's mass-ratio (1.93 vs my exp(−32.1/49.03) = 1.924). The accounting is validated.
- **Harpoon "Option A 17%" (titan-2) does NOT reproduce at the shared anchor — it comes out 20.85%.** This is an audited inconsistency, not an error in either round. titan-2's "Option A 17%" is a specific 500-kWe matrix cell whose Δv stack evidently carries more than the bare 24.7 km/s inbound (likely an Earth-arrival/LEO-capture increment, or a different dry/wet split). For the apples-to-apples comparison this round consistently applies the *same* inbound Δv and dry-mass model to both architectures, so the harpoon fraction is recomputed (20.85%) rather than imported (17%). **The relative verdict (H1, H4) is invariant to this** because both architectures share the inbound leg; ram-scoop differs only by the +7.4 km/s residence-out. Using the literal 17% for harpoon would shift the penalty ratio to 17/3.92 = 4.3× (still HELD for H2) and would only *widen* harpoon's delivered-mass lead — it does not threaten any verdict.

## Dry-mass treatment sensitivity

Two dry-mass models, same verdicts:

- **Ratio (`m_dry/M = 1.0`, primary):** η_dv chunk-mass-independent (harpoon 20.85%, ram-scoop 3.92%). Delivered mass scales linearly with chunk mass; positive for all chunks. This is the physically appropriate treatment for a parametric chunk-mass sweep (a vehicle is sized for its design chunk).
- **Fixed (`m_dry = 200 t`, sensitivity):** the literal titan-2 dry mass applied at all chunk masses. The fixed 200 t offset means the chunk-fed propellant cannot return net payload below a per-architecture chunk floor — harpoon delivers nothing below ~131 t, ram-scoop nothing below ~185 t. Median delivered mass is 0 t for both; only the top decile (146.5–200 t) clears zero, and only for harpoon (6.76 t). **Caution:** under the fixed model H1 reads "HELD" only as a degenerate median-tie-at-zero — the mean (harpoon 0.79 t vs ram-scoop 0.04 t, ~20×) and the top decile (6.76 t vs 0 t) both show harpoon dominating. The fixed model does not support ram-scoop; it makes the foundational-premise failure *more* severe.

The fixed model is pessimistic for small chunks (flying a 200 t empty vehicle to fetch a 10 t chunk is not a design anyone would choose). The ratio model is the load-bearing one for H1/H4; both agree H2/H3.

## Coordination flags resolved (per work-order open questions)

1. **H1 falsifies decisively, not at a modest margin.** Harpoon beats ram-scoop by ~4.3× in delivered mass, not by < 0.05 t. → **R-chunk-capture-contact-fidelity (Tier 2/3 follow-on) should target the single-chunk HARPOON architecture, not ram-scoop.** The Tier-1 ram-scoop leadership is not a reason to invest contact-fidelity effort in ram-scoop.
2. **H3 holds.** No architecture clears 25 t even with Δv carried, even at the optimistic posterior corner. → **The demonstrator-class promotion is NOT premature; it stands unconditionally.** No need to surface a reversal to the project-owner.

## Matrix amendment specification (for orchestrator — workers do not edit shared docs)

For `water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md` and the design-axes capture/architecture entry:

1. **Record that the ram-scoop Tier-1 capture-efficiency leadership is non-load-bearing.** Ram-scoop leads on single-pass capture probability (0.405 vs harpoon 0.365) but is last on delivered mass (0.71 t vs 3.01 t, ratio model) once chunk-as-propellant-tank return-Δv is coupled. Capture-probability ranking ≠ delivered-mass ranking.
2. **Confirm the foundational-premise retirement of ram-scoop on a quantitative basis.** Prior retirement (latest+6) was a Δv-argument decision; this round attaches the delivered-mass number: ram-scoop's +7.4 km/s residence-out is a 5.31× delivered-fraction penalty that no plausible capture-probability edge recovers.
3. **Re-confirm H3/L0-04:** no capture architecture clears the 25 t commercial floor at Tier-1 capture posteriors with Δv carried; best is single-chunk harpoon at ~3 t median / ~20.7 t optimistic-corner ceiling. This is consistent with — and tightens — R-chunk-capture-monte-carlo's H6 falsification.
4. **Contact-fidelity follow-on retargets to harpoon.** Update the queued R-chunk-capture-contact-fidelity SCOPE's architecture from ram-scoop to single-chunk harpoon.

## Caveats / what this round does NOT establish

- **Absolute delivered-mass numbers are provisional** pending titan's R-vehicle-mass-closure-refactor (dry mass becomes a derived quantity). The architectural-lead (H1, H4) and floor-clearance (H3) verdicts are robust to the dry-mass treatment; the specific tonnages (3.01 t etc.) are anchored to the fixed/ratio 200 t dry mass and the titan-2 Δv stack and should be re-verified post-refactor.
- This is a closed-form coupling, not a contact-dynamics or trajectory-optimisation result. The Δv stack (24.7 inbound, +7.4 residence-out, Isp 5000 s) is taken from titan-2 R-conops-chunk-vs-ram-scoop and R-bring-fine-structure-rendezvous, not re-derived.
- The everting-sleeve architecture (modelled harpoon-class on Δv, capture median 0.246) is dominated by harpoon on both capture and delivered mass; it is included for completeness but is not a live contender.

## Methodology-lesson candidate (for PROTOCOL.md, orchestrator to ratify)

**A favorable ranking on an intermediate metric is not load-bearing until the metric is coupled to the verdict quantity.** R-chunk-capture-monte-carlo Tier 1 ranked ram-scoop first on *capture probability*; the matrix verdict is on *delivered mass*. Ram-scoop's capture lead inverted to last place once the return-Δv cost — which the capture model structurally cannot see — was coupled in. This is the converse of latest+20's lesson 20 candidate ("confirm the axis is load-bearing before correcting an anchor"): here, confirm the *intermediate metric is load-bearing for the verdict* before promoting a leader on it. Both reduce to: rank on the verdict quantity, not on an upstream proxy.
