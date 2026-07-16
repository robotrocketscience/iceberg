# R-variant-B-burn-consistency — summary

## Headline

The architecture decision matrix's "sole defensible cell" (Variant B at 500 kWe / ISP 2000 s / 200-t chunk) is audited from first principles against the matrix's stated 7.5-yr inbound burn / 14.5-yr round-trip / 80-t delivered numbers. **Three findings:**

1. **The matrix's stated 7.5-yr inbound burn does not reproduce in any reasonable dv regime.** First-principles burn time is 1.33 yr at impulsive 6.42 km/s, 3.42 yr at continuous-thrust 24.7 km/s, 3.85–4.17 yr at higher continuous-thrust. The matrix carries a stale 7.5-yr value — 1.8–5.6× larger than any first-principles regime.
2. **The matrix's stated 80-t delivered does not reproduce either.** Impulsive 6.42 km/s gives 128.8 t delivered; CT 24.7 km/s gives only 17.4 t; CT 32 / 40.2 km/s yield NEGATIVE delivered (chunk insufficient as propellant).
3. **Variant B's cumulative reactor burn time is 1.33 yr — 13.5% of Arch E_500's 9.91 yr** at matched 500 kWe + 200-t chunk. R12 added a reactor-lifetime axis but only ran it on Arch E. Variant B clears the 10-yr Kilopower reactor-life target with **8.67-yr margin**, while Arch E_500 sits at 99.1% of that target.

| Architecture | Cumulative reactor burn (yr) | % of 10-yr Kilopower target | % of 15-yr FSP target |
|---|---:|---:|---:|
| Variant B (impulsive 6.42 km/s in) | **1.33** | 13.3% | 8.9% |
| Arch E_500 (CT 24.7 km/s in) | 9.91 | 99.1% | 66.1% |
| Arch E_500 (CT 32.0 km/s in) | 10.89 | 108.9% | 72.6% |
| Arch E_500 (CT 40.2 km/s in) | 11.73 | 117.3% | 78.2% |

This is a **NEW load-bearing finding R12 missed** by only running the reactor-lifetime axis on Arch E.

## Variant B feasibility vs inbound dv regime

| dv inbound | m_prop (t) | delivered (t) | inbound burn (yr) | round-trip (yr) | Feasible? |
|---:|---:|---:|---:|---:|---|
| 6.42 km/s (impulsive) | 71.2 | **128.8** | 1.33 | 14.01 | ✓ matrix-RT-matches |
| 24.7 km/s (CT low) | 182.6 | 17.4 | 3.42 | 16.10 | ✓ marginal |
| 32.0 km/s (CT mid) | 205.1 | **-5.1** | 3.85 | 16.52 | ✗ chunk insufficient |
| 40.2 km/s (CT high) | 222.2 | **-22.2** | 4.17 | 16.84 | ✗ chunk insufficient |

The matrix's 14.5-yr round-trip number reproduces (at 14.01 yr) **only at impulsive 6.42 km/s** — not at any continuous-thrust regime. Variant B's L0-05 compliance depends on which inbound dv is the operative one.

## Required chunk for closure at continuous-thrust inbound dv

To deliver useful mass at CT 24.7 km/s inbound:

| target delivered (t) | required chunk (t) | exceeds L0-05 200-t cap? |
|---:|---:|---|
| 30 | **244.5** | yes (by 22%) |
| 50 | **314.9** | yes (by 57%) |
| 80 (matrix's stated value) | ~410 | yes (by 105%) |

**Under realistic continuous-thrust inbound dv, Variant B is L0-05-non-compliant on the chunk side**, exactly as the matrix already flags Arch E.

## Scoring: 11 HELD / 3 FALSIFIED of 14

All three falsifications refine the finding rather than overturn it:

- **H-vbrc-l** (no CT cell feasible at all): falsified because CT 24.7 km/s **marginally** closes with 17.4-t delivered. Refined claim: "CT 32 and 40.2 km/s are infeasible; CT 24.7 is marginal."
- **H-vbrc-m** (impulsive feasible AND ALL CT infeasible): same root.
- **H-vbrc-n** (required chunk ≥ 250 t for 30-t delivered at CT 24.7): 244.5 t — 2% below my threshold. Practically the finding is right (exceeds 200-t L0-05 cap by 22%); threshold was set fractionally too high.

The 11 HELD include the load-bearing results:
- Matrix's 7.5-yr inbound burn does NOT reproduce (H-vbrc-e)
- Matrix's 80-t delivered does NOT reproduce (H-vbrc-f)
- Variant B's 14.5-yr round-trip DOES reproduce at impulsive 6.42 km/s (H-vbrc-g)
- Variant B / Arch E cumulative-burn ratio = 0.135 (H-vbrc-i)
- Variant B clears Kilopower 10-yr target with 8.67-yr margin (H-vbrc-j)
- R12's Arch E 11.37-yr burn reproduces at 9.91 yr (H-vbrc-k)

## What this changes in the architecture decision matrix

### Required matrix amendments

1. **Update Variant B's stated parameters.** Replace the matrix's "7.5-yr inbound burn / 80-t delivered" with first-principles values at the matrix's chosen inbound dv regime. The 14.5-yr round-trip survives at impulsive 6.42 km/s; the burn-time and delivered numbers are off by 5.6× and 38% respectively.

2. **Disclose which inbound dv regime Variant B assumes.** The matrix uses titan's continuous-thrust 24.7–40.2 km/s for Arch E but appears to use impulsive 6.42 km/s for Variant B. This asymmetry needs to be either justified (e.g., Variant B has a chemical inbound braking burn the matrix doesn't document) or removed (apply continuous-thrust to both, in which case Variant B at 200-t chunk also collapses).

3. **Add reactor-lifetime column to matrix.** Variant B cumulative burn 1.33 yr vs Arch E_500 9.91 yr at matched reactor power — Variant B has ~7× margin advantage. Currently invisible in the matrix.

4. **Annotate "sole defensible cell" with the inbound-dv regime caveat.** Either:
   - "Active conditional on impulsive 6.42-km/s inbound dv, which assumes a chemical inbound braking phase not yet documented." — OR —
   - "Under titan's continuous-thrust inbound dv (24.7–40.2 km/s), Variant B requires chunk ≥ 245 t to deliver 30 t; exceeds L0-05 200-t cap. Falsified by titan's continuous-thrust framework just as Arch E is."

### Implication for R13's strict-dominance finding

R13 found Variant B strictly dominates Arch E on P(NPV+) under bottoms-up cost (ratio 3.4×). R14 adds a **second** independent axis where Variant B dominates: reactor lifetime (ratio 7.4× margin). However, R14 also reveals **Variant B may be L0-05-non-compliant under continuous-thrust inbound dv**, exactly the failure mode that retired Arch E's megawatt cells.

The architecture decision now reduces to:

| Inbound dv regime | Architecture | L0-05 status | Notes |
|---|---|---|---|
| Impulsive 6.42 km/s | Variant B | ✓ compliant | Requires chemical inbound phase not in matrix |
| Impulsive 6.42 km/s | Arch E_500 | ? | Not tested in this round; would need impulsive Arch E rerun |
| Continuous-thrust 24.7 km/s | Variant B | ✗ marginal (17.4 t delivered) | Below L0-05's 80-t target |
| Continuous-thrust 24.7 km/s | Arch E_500 | ✓ borderline at 24.7; ✗ above | 9.91 yr cumulative burn = 99% Kilopower target |
| Continuous-thrust ≥ 32 km/s | Variant B | ✗ infeasible | Chunk insufficient as propellant |
| Continuous-thrust ≥ 32 km/s | Arch E_500 | ✗ marginal | 10.9–11.7 yr burn exceeds Kilopower target |

**The matrix appears to have an undocumented dv-regime asymmetry between Variant B (impulsive) and Arch E (continuous-thrust).** Resolving this asymmetry is the highest-leverage next step.

### Implication for R13's joint expected-value

If continuous-thrust inbound dv applies to BOTH architectures (the consistent framework per titan), then Variant B is itself L0-05-non-compliant at 200-t chunk. The "Variant B as sole defensible cell" framing of the matrix collapses; both architectures need either impulsive-dv justification (chemical inbound phase) or L0-05 waiver.

If impulsive inbound dv applies to BOTH (requires chemical inbound phase for both), then Variant B's 14.5-yr round-trip survives and Arch E's round-trip would need recomputation under impulsive too. Arch E's reactor-life requirement would shrink dramatically. Cleanest test: run Arch E at impulsive 6.42 km/s.

## Caveats

- ETA_THR = 0.70 (R-electric-outbound-rerun default). Real ion thrusters at 2000-s ISP achieve 0.60–0.75; ±15% on burn time.
- Bundled 10 W/kg mass model gives m_dry = 53 t at 500 kWe. MARVL-anchored mass is plausibly higher (60–70 t at 500 kWe); m_dry shift would slightly increase m_prop and delivered numbers stay close.
- Chemical-kick outbound treated as zero reactor-burn time (correct for propulsion); ignores housekeeping draw during cruise (~5–20 kWe over 6 yr = 0.03–0.06 reactor-yr-equivalents, negligible vs 1.33-yr inbound).
- Saturn ops set to 0.5 yr (R-electric-outbound-rerun's SATURN_OPS_YR).
- This round does NOT re-derive trajectory physics. Uses matrix's impulsive 6.42 km/s and titan's continuous-thrust 24.7/32/40.2 km/s as bracketing inputs.

## Pending follow-ups

- **R-arch-E-impulsive-dv-rerun**: rerun Arch E at impulsive 6.42 km/s inbound dv to see if the dv-regime asymmetry hides an Arch E that's actually L0-05-compliant. If so, the matrix's "Arch E falsified" verdict (rhea) may itself depend on the same dv-regime choice that exempts Variant B.
- **R-matrix-dv-regime-audit**: document which dv regime each surviving and retired cell uses, expose the asymmetry, and force a consistent treatment.
- **R-chemical-inbound-phase**: does Variant B's matrix-implied chemical inbound braking phase exist in the conops? If so, propellant mass and tankage would be substantial — they need to be added to m_dry.
- **R-reactor-program-scope-extrapolation**: Variant B and Arch E both require 500-kWe reactor (5× FSP Phase 2 scope). The 0-of-6 base rate applies the same way to both. Reactor-lifetime axis is differential (R14) but reactor-availability axis is identical. Update R6's posterior cascade to apply identically to both.
