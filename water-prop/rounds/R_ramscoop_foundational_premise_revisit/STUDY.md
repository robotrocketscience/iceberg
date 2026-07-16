# Round — Ram-scoop foundational-premise revisit: does the Tier-1 capture lead survive the chunk-as-propellant-tank delta-velocity penalty?

**Status:** pre-result (hypotheses pre-registered before running `coupled_delivered_mass.py`).

**Round directory:** `water-prop/rounds/R_ramscoop_foundational_premise_revisit/`.

**Owning session:** rhea (re-spawn), branch `iceberg-rhea-3`.

**Date:** 2026-05-26.

**Predecessor rounds (inputs, not re-derived):**
- R-chunk-capture-monte-carlo Tier 1 (`464927e`, 2026-05-26) — per-architecture single-pass capture-probability posteriors. Tier-1 leader is **ram-scoop** (median 0.405, 90% credible interval [0.327, 0.491]), ahead of single-chunk **harpoon** (0.365 [0.136, 0.497]) and **everting-sleeve** (0.246 [0.130, 0.418]). All three fail the H6 threshold (0.544). Input file: `../R_chunk_capture_monte_carlo/results/tier1_results.json` + regenerated per-sample draws from `../R_chunk_capture_monte_carlo/tier1_closed_form.py` (seed 20260526).
- titan-2 R-conops-chunk-vs-ram-scoop (`07b73ec`, 2026-05-15 latest+7) — chunk-fed exit-Δv bookkeeping under continuous-thrust accounting. Ram-scoop residence-class delivered fraction 3.5% vs harpoon-class Option-A 17%, at megawatt-electric specific impulse 5000 s, ~200 t dry, ~200 t collected. Ram-scoop pays +7.4 km/s residence-out continuous-thrust Δv on top of the 24.7 km/s interplanetary inbound (32.1 km/s total) because it must circularise into the B-ring plane and climb back out.
- Project-owner foundational-premise decision latest+6 (2026-05-15) — ram-scoop retired because the +14.7 km/s Saturn-side round-trip Δv defeats ICEBERG's foundational delta-velocity-minimisation-via-chunk-as-propellant-tank lever.
- Project-owner H6-cascade decision (2026-05-26) — demonstrator-class promoted to primary programmatic path after R-chunk-capture-monte-carlo H6 falsified.

## Question

R-chunk-capture-monte-carlo Tier 1 ranks ram-scoop **first** on single-pass capture probability. But that model carries no Δv bookkeeping — it scores the probability of a successful capture event, not the delivered mass after the chunk-fed return burn. The foundational-premise retirement of ram-scoop rests on a Δv argument the Tier-1 model does not see. **Does ram-scoop's capture lead survive once capture probability and chunk-fed return-Δv are carried in one coupled model?** The matrix verdict (L0-04 = 25 t commercial floor) is on delivered mass per mission, not on capture probability alone.

## Coupled model

Per successful capture, the captured ice **is** the propellant for the return burn (chunk-as-propellant-tank, the foundational ICEBERG premise). Tsiolkovsky on the return leg:

```
m_final = (m_dry + m_captured) · exp(−Δv_arch / v_e)
delivered_if_captured = max(0, m_final − m_dry)
```

Per Tier-1 sample i (architecture a), the delivered-mass realisation is

```
delivered_i = p_capture_i · delivered_if_captured(M_i ; a)
```

where `M_i` and `p_capture_i` are the **same Tier-1 sample's** chunk mass and joint capture probability (the Tier-1 model samples `chunk_mass_t` log-uniform [10, 200] t jointly with capture probability, so reusing the per-sample pairs preserves the mass↔capture correlation and is the marginalisation over chunk mass that SCOPE step 3 calls for).

Multiplying by `p_capture` is consistent with the matrix/A14 accounting, where delivered mass folds capture efficiency ("net efficiency" = capture × delivery).

### Anchors (from published rounds — NOT re-derived; inconsistencies audited, not silently reconciled)

- `v_e = Isp · g0 = 5000 s × 9.80665 m/s² = 49.03 km/s` (titan-2 megawatt-electric specific-impulse anchor).
- `Δv_harpoon = 24.7 km/s` (interplanetary inbound continuous-thrust; single-chunk capture on an eccentric pass, no ring-plane circularisation).
- `Δv_ramscoop = 24.7 + 7.4 = 32.1 km/s` (adds residence-out continuous-thrust to climb out of the circularised B-ring orbit).
- `Δv_everting = 24.7 km/s` (everting-sleeve is single-chunk active enclosure on a pass — harpoon-class on Δv).
- Dry mass: two treatments, both reported.
  - **Primary — constant ratio** `m_dry / M = 1.0` (titan-2 anchored 200 t dry to a 200 t chunk). Physically appropriate for a parametric chunk-mass sweep: a vehicle is sized for its design chunk. Under this treatment `η_dv = 2·exp(−Δv/v_e) − 1` is chunk-mass-independent.
  - **Sensitivity — fixed** `m_dry = 200 t` regardless of chunk mass (the literal titan-2 number). Pessimistic for small chunks: a 200 t empty vehicle returning a 10 t chunk barely returns itself, so delivery goes to zero below a per-architecture chunk-mass floor.

The **relative** comparison (which architecture delivers more) is robust to the dry-mass treatment because both architectures share the same `m_dry` model and inbound Δv; ram-scoop differs only by the +7.4 km/s residence-out increment. The **absolute** delivered-mass numbers depend on the dry-mass anchor and will need re-verification after titan's R-vehicle-mass-closure-refactor makes dry mass a derived quantity (per the work-order sequencing note).

## Pre-registered hypotheses

| ID | Hypothesis | Falsification |
|---|---|---|
| **H1** | Ram-scoop's Tier-1 capture lead is **preserved** after Δv bookkeeping: ram-scoop's delivered-mass posterior median ≥ harpoon's. | Falsified if ram-scoop delivered-mass posterior median < harpoon's. |
| **H2** | The ~5× delivered-fraction drop (harpoon 17% → ram-scoop 3.5%) of titan-2 R-conops-chunk-vs-ram-scoop **holds at the Tier-1 chunk-mass distribution**: ram-scoop relative penalty vs harpoon ∈ [3×, 8×]. | Falsified if the relative penalty (harpoon η_dv / ram-scoop η_dv) is < 3× or > 8×. |
| **H3** (load-bearing) | **Even with ram-scoop carried, no architecture clears the L0-04 = 25 t commercial floor** at the Tier-1 delivered-mass posterior. Re-tests R-chunk-capture-monte-carlo H6 with Δv bookkeeping. | Falsified if any architecture's delivered-mass posterior median ≥ 25 t at any operating chunk mass. |
| **H4** | The architecture trade is **chunk-mass-dependent**: ram-scoop wins at large chunks (capture advantage dominates), harpoon at small chunks (Δv penalty matters less). | Falsified if the better architecture is the **same** across the full chunk-mass range [10, 200] t. |

### Pre-registered predictions (analyst priors, for honesty)

- H1: expected **FALSIFIED**. Ram-scoop's +7.4 km/s residence-out on an exponential mass-ratio penalty (≈5× delivered-fraction hit per titan-2) swamps its +0.04 capture-probability edge. Back-of-envelope at M = 200 t: harpoon 0.365 × ~21% ≈ 15 t vs ram-scoop 0.405 × ~3.9% ≈ 3.2 t.
- H2: expected **HELD** (relative penalty ≈ 5.3×, between the titan-2 17/3.5 = 4.9× and my recomputed harpoon-fraction at the same anchor).
- H3: expected **HELD** (best architecture ~15 t at the 200 t chunk in expectation, far below 25 t; less when marginalised over the log-uniform prior).
- H4: expected **FALSIFIED** (harpoon's η_dv exceeds ram-scoop's at every chunk mass and harpoon's zero-delivery floor is at a lower chunk mass, so harpoon wins across the entire range — the larger Δv penalty dominates the capture edge everywhere, not just at small chunks).

## Method

1. Replay the Tier-1 seeded RNG (`tier1_closed_form.py`, seed 20260526) to regenerate the exact per-sample `(chunk_mass_t, p_capture)` pairs for all three architectures. **Validation gate:** regenerated capture-probability medians must match `tier1_results.json` (harpoon 0.3654, ram-scoop 0.4049, everting 0.2463) to within floating-point tolerance, else abort.
2. Apply the coupled delivered-mass model per sample, under both dry-mass treatments.
3. Report delivered-mass posteriors (median, 5/25/75/95 quantiles, mean) per architecture per treatment.
4. H4: bin samples by chunk-mass decile; report the winning architecture per bin.
5. Verdict on H1–H4 + matrix-amendment specification if H3 moves.

### Validity caveats

- This is a coupled-model round on existing posteriors plus existing Δv bookkeeping. **No new Monte Carlo, no new physics.** The capture posteriors and the Δv stack are both inputs.
- The titan-2 harpoon "Option A 17%" is a cross-referenced anchor from a specific 500-kWe matrix cell; my consistent re-derivation at the shared anchor may differ by a few points (audited in FINDINGS, not silently reconciled). The ram-scoop 3.5% reproduces within rounding under my model, validating the accounting.
- Absolute delivered-mass numbers are anchored to a fixed/ratio dry mass and the titan-2 Δv stack; they require post-R-vehicle-mass-closure-refactor re-verification. The architectural-lead (H1, H4) and floor-clearance (H3) verdicts are the robust outputs.
- Workers do not edit shared docs (`PARALLEL-SESSIONS.md`); FINDINGS specifies matrix amendments for the orchestrator to apply.
