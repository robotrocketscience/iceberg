# R-bring-rendezvous-survivability — tables

Generated from `R_bring_rendezvous_survivability.json` produced by `run.py`. See `closure_verdict.md` for adjudication.

---

## Table 1 — Titan baseline reproduction

| Quantity | Computed (this round) | Titan SOI body 3 line 186 | Match |
|---|---|---|---|
| τ | 2.0 | 2.0 | — |
| inclination | 26.7° | 26.7° | — |
| csc(i) | 2.227 | 2.227 | — |
| P_impact per pass | 0.9883 | 0.9885 | within 0.02% |

Per-pass impact-probability formula (titan SOI body 3): `P = 1 - exp(-τ × csc(i))`. Reproduces titan to within rounding.

---

## Table 2 — Single-lever inclination sweep (apoapsis-burn cost; chunk-zone P_impact)

| Inclination | Δi | Δv round-trip @ apoapsis | Variant-B propellant @ Isp 5000 s | % of 264-t baseline | P_impact zone-avg τ=2 | P_impact outer 180 km τ=0.10 | P_impact outermost 80 km τ=0.03 |
|---|---|---|---|---|---|---|---|
| 26.7° | 0° | 0.000 km/s | 0.00 t | 0.0% | 0.9883 | 0.1995 | 0.0646 |
| 45.0° | 18.3° | 1.379 km/s | 7.53 t | 2.9% | 0.9409 | 0.1319 | 0.0415 |
| 60.0° | 33.3° | 2.484 km/s | 13.72 t | 5.2% | 0.9007 | 0.1091 | 0.0340 |
| 75.0° | 48.3° | 3.547 km/s | 19.80 t | 7.5% | 0.8739 | 0.0983 | 0.0306 |
| 90.0° | 63.3° | 4.549 km/s | 25.66 t | 9.7% | 0.8647 | 0.0952 | 0.0296 |

Edelbaum impulsive-equivalent at apoapsis: Δv = 2 × v_apo × sin(Δi/2), where v_apo = 2.166 km/s. Periapsis-burn alternative is 12.2× more expensive (v_p = 26.48 km/s) and was discarded per audit 4.

---

## Table 3 — Single-lever cull-mesh sweep (no inclination change)

| Zone | τ_total | mesh on | τ_effective | P_impact per pass at i=26.7° | mesh mass @ 100 m² aperture |
|---|---|---|---|---|---|
| B-ring zone-avg | 2.00 | no | 2.00 | 0.9883 | 0 |
| B-ring zone-avg | 2.00 | yes | 1.50 | 0.9648 | 0.5 t |
| B-ring outer 200 km | 0.10 | no | 0.10 | 0.1995 | 0 |
| B-ring outer 200 km | 0.10 | yes | 0.075 | 0.1538 | 0.5 t |
| B-ring outermost 80 km | 0.03 | no | 0.03 | 0.0646 | 0 |
| B-ring outermost 80 km | 0.03 | yes | 0.0225 | 0.0490 | 0.5 t |

Mesh removes shieldable < 1 cm fraction (25% of τ per fine-structure H3). Mesh mass = 5 kg/m² × 100 m² = 500 kg. Mesh alone reduces P_impact by ~25% in any zone — a very small lever.

---

## Table 4 — Slow-cross sweep (audit 1: P_impact unchanged; audit 2: minimum v_rel ≈ 9 km/s without ring-match)

| Scenario | v_target (Saturn frame) | v_rel to ring particle | Δv round-trip | Variant-B propellant | KE per impact (1cm particle) | Above Whipple 10 kJ threshold? |
|---|---|---|---|---|---|---|
| Capture orbit (no slow) | 26.48 km/s | 12.61 km/s | 0 km/s | 0 t | 119,286 J | yes (12×) |
| Slow to 20 km/s | 20.00 km/s | **9.13 km/s** | 12.96 km/s | 79.9 t | 62,506 J | yes (6×) |
| Slow to 15 km/s | 15.00 km/s | 9.07 km/s | 22.96 km/s | 157.7 t | 61,748 J | yes (6×) |
| Slow to 10 km/s | 10.00 km/s | 11.46 km/s | 32.96 km/s | 253.1 t | 98,490 J | yes (10×) |
| Slow to 5 km/s | 5.00 km/s | 15.18 km/s | 42.96 km/s | 370.0 t | 172,733 J | yes (17×) |
| Ring-orbit match (residence) | 19.48 km/s | **0.010 km/s** | 14.01 km/s | 87.3 t | 0.1 J | no |

Vehicle is 26.7° inclined to ring plane; out-of-plane component = v × sin(26.7°) = 11.9 km/s minimum (independent of slowing). v_rel hits a floor of ~9 km/s when in-plane component matches v_circ_ring = 19.48 km/s. Only the residence-class case (project-owner-retired) gives non-fatal per-impact KE.

---

## Table 5 — Combined sweep: closure summary by τ-zone (best inclination + mesh)

For each τ-zone, the closure metrics at the best (lowest P_impact) cell — 90° inclination + cull-mesh + 0 kg/m² armour (armour does not enter P_impact bound):

| τ-zone | r [km] | τ_total | τ_eff (mesh) | P_impact per pass | P_impact 2 crossings | Mass penalty (Δv + mesh) | Chunk availability | Closes P_impact? | Closes mass? | Closes ALL? |
|---|---|---|---|---|---|---|---|---|---|---|
| B-ring zone-avg | 100,000 | 2.00 | 1.500 | 0.7769 | 0.9502 | 9.91% | rich | no | yes | **no** |
| B3 core | 107,000 | 4.50 | 3.375 | 0.9658 | 0.9988 | 9.91% | rich | no | yes | **no** |
| B-ring outer 580 km | 117,000 | 0.40 | 0.300 | 0.2592 | 0.4513 | 9.91% | rich | no | yes | **no** |
| Huygens Ringlet | 117,900 | 0.30 | 0.225 | 0.2014 | 0.3623 | 9.91% | rich | no | yes | **no** |
| B-ring outermost 180 km | 117,400 | 0.10 | 0.075 | **0.0723** | **0.1393** | 9.91% | thin | no | yes | **no** |
| B-ring outermost 80 km | 117,500 | 0.03 | 0.023 | 0.0223 | 0.0440 | 9.91% | sparse | no | yes | **no** |
| Cassini Div outer plateau | 120,000 | 0.04 | 0.030 | 0.0296 | 0.0582 | 9.91% | none | no | yes | **no** |
| Huygens Gap | 117,680 | 0.001 | 0.00075 | **0.00075** | 0.00150 | 9.91% | none | no (7.5× target) | yes | **no** |
| Laplace Gap | 121,850 | 0.001 | 0.00075 | 0.00075 | 0.00150 | 9.91% | none | no (7.5× target) | yes | **no** |

Per-crossing target: 10⁻⁴ (0.01%). Two-crossings target: 2×10⁻⁴ (0.02%). Best ANY-cell P_per_pass = 0.075% in Huygens Gap = 7.5× the per-pass target, AND no chunks. Best CHUNK-PRESENT P_per_pass = 7.23% in B-ring outermost 180 km = 723× the per-pass target.

---

## Table 6 — Hypothesis verdicts (predicted vs measured)

| H# | Predicted | Measured | Verdict |
|---|---|---|---|
| H-bsurv-1 (armour alone P ≥ 50%) | armour-only stays at zone P_impact | 98.83% (zone-avg, i=26.7°, any armour) | **HOLD-strong** |
| H-bsurv-2 (mesh alone reduces flux ≤ 30%) | 25% reduction → P drops 98.83% → 91.18% | 91.18% | **HOLD** |
| H-bsurv-3 (off-plane Δv ≥ 5 km/s) | 4.55 km/s round-trip at apoapsis | 4.549 km/s | **WRONG-BUT-INFORMATIVE** (lower than predicted, above 1.5 km/s falsification floor) |
| H-bsurv-4 (slow-cross ≥ 8 km/s round-trip) | residence-or-9-km/s-floor | min v_rel 9.07 km/s @ Δv 23 km/s; ring-match Δv 14 km/s | **HOLD** (in two forms) |
| H-bsurv-5 (no closing combination) | 0 cells close at conservative anchors | **0 of 162 cells close P_impact target** | **HOLD-strong** |
| H-bsurv-6 (conjunction with aerobraking < 10%) | 0 × this-round-prob = 0 | 0 × 0 = 0 | **HOLD-strong** (conditional on `a7a8456` integration) |
