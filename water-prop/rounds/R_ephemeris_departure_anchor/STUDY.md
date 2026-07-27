# R-ephemeris-departure-anchor — STUDY

**Round:** R-ephemeris-departure-anchor. SCOPE pre-registered 2026-07-22 latest+25 arc (commit `a6f4734`) before `run.py` existed. **First real-JPL-ephemeris round in the ICEBERG campaign.**
**Worker:** worktree-115637 session. Project-owner-directed: cross-apply `~/projects/trajectory-bot`'s real-ephemeris trajectory toolkit to ICEBERG.
**One line:** A real JPL-Horizons Saturn→Earth Lambert porkchop (134,396 cells; Lambert cross-validated to 5×10⁻⁵ km/s against Curtis Ex 5.2) puts the **minimum departure v∞ at 5.26 km/s**, bracketing the hand-derived vis-viva 5.44 km/s and confirming 6.21 as a realizable faster-transfer value — **retiring design-axes/04's "vis-viva-default anchoring" methodology weakness for this anchor with a real-ephemeris backing.** The reactor floor is unmoved (153–159 kWe). The one new finding: trajectory-bot's Titan constants reproduce R186's ~3.3 km/s Titan pump cap but show the revocation is **conditional on the arrival-orbit v∞_T**.

## Why this round matters beyond its number

Every prior ICEBERG Saturn-departure anchor (5.44 / 6.21 / 7.7 / 8.4–8.5 km/s) was **hand-derived vis-viva**, carrying the campaign's flagged methodology weakness — "vis-viva-default anchoring when no primary-text source" (design-axes/04, Methodology lesson 20). This is the first round to leave hand-analytic for **real JPL Horizons ephemeris**, using trajectory-bot's Horizons pipeline for the data and a vendored pure-numpy universal-variable Lambert (Curtis Alg 5.2, no JAX) for the transfer. It also imports trajectory-bot's verification discipline — the Lambert is cross-validated against an analytic reference *before* any porkchop cell is trusted.

## Hypotheses, tests, results

All in `run.py` (deterministic); input ephemeris `inputs/ephem_saturn_earth.json` (real Horizons); numbers in `results/ephemeris_findings.json`; figure `results/ephemeris.png`.

### H1 [S] — Real-ephemeris minimum departure v∞ brackets the hand 5.44 km/s — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| porkchop minimum v∞ | [5.0, 6.0] km/s | **5.259 km/s** (ToF 6.5 yr) | yes |
| vs hand min-energy 5.44 | bracket | within ~3.4% (slightly below) | yes |

**Reading.** Over a 2035–2046 launch window (134,396 Lambert cells), the minimum departure v∞ is 5.26 km/s. The per-departure-epoch minimum (figure panel 2) modulates 5.7→5.26 km/s as Saturn moves toward aphelion (10.02 AU) — the real eccentricity signature — with the hand-derived 5.44 sitting squarely in the band. **The hand vis-viva anchor is validated by real ephemeris.** That the real minimum is slightly *below* 5.44 is expected and honest: the exact-180° minimum-energy cells are skipped as Lambert-singular, so the reported minimum is if anything an upper bound, and favorable real Saturn/Earth geometry (Saturn near aphelion) beats the mean-distance circular-coplanar value.

### H2 [S] — 6.21 km/s is a realizable faster-than-minimum value — **HELD**

6.21 ≥ the 5.26 km/s porkchop minimum. **Reading.** Confirms `R-hohmann-vinf-reconciliation`'s reading against real ephemeris: 6.21 is a legitimate faster-transfer departure v∞ (conservative by ~15% vs the real minimum), not an unphysically low number.

### H3 [S] — Titan pump cap reproduces R186 ~3.3 km/s, but the revocation is conditional — **HELD (with a new nuance)**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| cap at v∞_T = 3 (R186-consistent) | ~3.3 km/s | **3.38 km/s** | yes |
| v∞_T threshold to reach 5.44 | [3.8, 4.2] km/s | **4.01 km/s** | yes |

**Reading — the interesting finding.** Using trajectory-bot's Titan@Saturn constants (v_P=5.57, μ=8978, R=2574.7), the max Saturn-centric departure excess a Titan flyby chain can build = √((v_Titan+v∞_T)² − 2μ_S/r_Titan). At the natural capture-orbit v∞_T≈3 km/s this is **3.38 km/s — reproducing R186's ~3.3 km/s cap** from an independent constant set. **But the cap scales with v∞_T** and reaches the 5.44 km/s departure requirement at v∞_T ≥ 4.01 km/s — a *slow, near-apoapsis* Titan crossing on a highly eccentric bound Saturn orbit (v_sc ≈ 1.6 km/s at Titan's orbit gives |v_sc − v_Titan| = 4.0). So **R186's Titan-lever revocation holds at nominal parameters but is *conditional* on the arrival-orbit v∞_T ≲ 3.5** — a nuance the magnitude-bound-only R186 did not quantify. Whether a patient high-v∞_T Titan tour (rotating v∞_T from anti-aligned to aligned over ~12 flybys, each turning it ~16°) can actually realize this in a real Saturn-frame geometry — and whether the pumped v∞ *direction* matches the required heliocentric departure direction — is not settled by this magnitude bound. **This does not move the reactor floor** (H4) — the departure burn supplies v∞ regardless of whether Titan helps — but it re-opens a design question.

### H4 [W] — Reactor floor unmoved by the real anchor — **HELD**

| v∞ | reactor floor |
| --- | --- |
| real min 5.26 | **153 kWe** |
| hand 5.44 | 154 kWe |
| campaign 6.21 | 159 kWe |

**Reading.** Oberth quadrature at the deep B-ring well (v_esc 26.6 km/s) suppresses the v∞ spread: the whole 5.26–6.21 km/s range maps to a 153–159 kWe floor — the bottom of / just below the campaign's stated 155–175 kWe band. The real anchor confirms the floor and shows the campaign was, if anything, marginally *pessimistic* on departure — consistent with `R-hohmann-vinf-reconciliation`. Bet #3's reactor-power gate is unchanged.

## Revisit / bug-catch (mandatory)

- **Lambert cross-validated before use** (5.2×10⁻⁵ km/s vs Curtis Example 5.2) — the higher-fidelity verification pattern borrowed from trajectory-bot; no porkchop cell was trusted until the solver reproduced an analytic reference.
- **Exact-180° cells skipped** (Lambert plane-singularity at Δθ=π, the minimum-energy geometry). The true minimum sits at ~180°, so the reported 5.26 is a slight *upper* bound on the real min-energy v∞ — the honest direction (it can only strengthen "hand 5.44 is representative," never spuriously undercut it).
- **No interpolation error.** Saturn and Earth Horizons grids are 7-day-aligned, so the porkchop uses grid points directly. Saturn's real 9.07–10.02 AU eccentricity range is captured.
- **H3 is a magnitude bound, not a Saturn-frame tour.** It reproduces R186 and exposes the v∞_T-conditionality, but the full question (can a real high-v∞_T Titan tour realize the aligned geometry, and in the right departure direction?) needs a Saturn-frame tour optimizer — trajectory-bot's tour search is heliocentric-only and would need re-hosting. Named follow-on.
- **Single-revolution short-way Lambert only.** Long-way / multi-rev not swept; the min-energy Saturn→Earth transfer is a ~6-yr single-rev short-way well inside the grid, so this does not affect the minimum.

## Cross-learning

- **To design-axes/04 (inbound-Δv accounting):** the Saturn-departure v∞ anchor now has a **real-ephemeris backing** (min 5.26 km/s, hand 5.44 validated); Methodology lesson 20's "vis-viva-default" caveat is *discharged for this anchor* — the first ICEBERG anchor to graduate from hand-vis-viva to ephemeris. The R186 Titan revocation is **corroborated at nominal params but flagged conditional on v∞_T** (a new open sub-question, not a reversal).
- **To design-axes/05 (reactor power floor):** the 155–175 kWe floor is confirmed on a real-ephemeris departure v∞ (153–159 kWe across the real range); bet #3 unchanged.
- **To `water-prop/PROTOCOL.md` (methodology):** this round demonstrates a reusable **ephemeris-fidelity tier** for ICEBERG — vendored Lambert + Horizons data + cross-validation-before-use. Candidate to fold into the protocol as the higher-fidelity check for any load-bearing trajectory anchor.
- **Named follow-ons (not run):** (1) **Saturn-frame Titan-tour optimizer** — re-host trajectory-bot's heliocentric tour search in a Saturn-centric frame to settle whether a high-v∞_T Titan tour re-opens the departure lever (the H3 conditionality); (2) **lunar-GA Earth-arrival** check of R12's 7.3→4.2 km/s claim (trajectory-bot CR3BP Earth–Moon); (3) **low-thrust spiral departure** with an Isp/mass model added to trajectory-bot's idealized low-thrust arcs.
- **What trajectory-bot could NOT help with (recorded for honesty):** aerocapture/aerobraking (it has no atmosphere model), Saturn SOI capture (its CR3BP is Earth–Moon only), and water-MET propulsion sizing (its Δv is idealized ∫|a|dt, no Isp).
