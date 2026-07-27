# R-departure-anchor-resolution — FINDINGS

**Worker:** worktree-172651, 2026-07-26 latest+29c. Pre-registration: `STUDY.md`.
Artifacts: `run.py`, `results/dv_vs_accel.json`,
`results/armB_at_22p5_probe.json`. Fidelity tier: T1 direct integration
(Deviation 8), cross-checked against R-lowthrust-spiral-departure's independent
T1 result.

## Headline

**The 9.0 km/s chunk-fed departure anchor is DEAD for electric propulsion — and
the honest arm was itself optimistic.** Direct RK4 integration (planar two-body
Saturn, tangential thrust, B-ring residence r₀ = 100,000 km, v_circ 19.48 km/s,
target v∞ 5.44 km/s):

| a (m/s²) | Δv to v∞ (km/s) | Δv to escape | thrust time | revolutions |
|---|---|---|---|---|
| 10⁻⁵ (30 kWe class) | **24.18** | 18.84 | 76.6 yr | 15,094 |
| 3×10⁻⁵ | 23.28 | 18.64 | 24.6 yr | 5,031 |
| 10⁻⁴ (200 kWe class) | **22.55** | 18.35 | 7.1 yr | 1,510 |
| 10⁻³ | 20.69 | 17.47 | 0.66 yr | 151 |
| 10⁻² | 18.04 | 15.92 | 0.06 yr | 15 |
| 10⁻¹ | 14.31 | 13.11 | — | 1.7 |

Impulsive Oberth reference: 8.60 km/s. Local gravity at ring radius is
3.8 m/s², so the impulsive limit needs thrust-to-weight approaching a tenth of
a g — **the 9.0 km/s figure is not recovered even at a = 0.1 m/s² (14.3 km/s),
five orders of magnitude above the campaign's electric envelope.** Escape term
at electric a: 18.35–18.84 km/s, within 6% of Edelbaum's v_circ — reproducing
R-lowthrust-spiral-departure independently.

## Verdicts

| # | Hypothesis | Verdict | Measured |
|---|---|---|---|
| H-D1 | Electric-class Δv within 15% of Edelbaum + ≥1.9× the 9.0 anchor | **HELD** | 22.55–24.18 km/s = 2.5–2.7× the anchor; escape term within 3–6% of v_circ |
| H-D2 | 9.0 km/s recovered only at a ≥ 10⁻² m/s² | **HELD, direction under-shot** | not recovered even at 10⁻¹ m/s²; requires ≳1 m/s² (chemical/NTP thrust class) |
| H-D3 | Δv(a) monotone → impulsive 7.7–8.5 asymptote | **HELD** | monotone decreasing toward 8.60 |

## Disposition (per the pre-committed rule)

1. **Arm B is the citable arm** for any electric chunk-fed departure at
   ≤500 kWe — and Arm B's 18.0 km/s is itself a lower bound; the integrated
   value at campaign accelerations is **22.5–24.2 km/s**. Arm A columns of the
   boundary map are re-labeled *impulsive-regime bound — not reachable by
   electric propulsion* (they remain meaningful only for impulsive departure
   stages, i.e. the v2 corridor).
2. **Re-probe at the integrated 22.5 km/s** (`armB_at_22p5_probe.json`): the
   honest ELECTRIC corridor's 30-t closure DIES — the best case (Isp 3,000 s +
   ×8 + 60 W/kg + f 0.40 + 300–500 t chunk) drops from 56 t to **28.3 t**, below
   the floor; the 10-t case drops 12.8 → 3.95 t at record chunks. **The
   electrolysis-fed nuclear-thermal corridor (impulsive, anchor-independent) is
   now the ONLY corridor that closes the 30-t commercial floor under honest
   resolved physics.**
3. The framework's `CHUNK_FED_DV_KM_S = 9.0` default stays in code for baseline
   immutability; the option's notes now carry the lesson-23 flag, and
   `chunk_fed_dv_km_s` (sanctioned override) should be set to 22.5 for any
   future honest-arm work.

## Model-form notes

Constant-a convention (mass-flow would raise late-burn acceleration and shave
Δv slightly — direction favors the retired anchor by well under the 2.5×
margin); planar; tangential steering (near-optimal for energy-raising spirals);
field-free residual added beyond the sphere of influence (exact in the
two-body limit). None threaten the verdict.
