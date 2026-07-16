# R-no-atmospheric-capture-baseline — does ANY surviving cell exist with Earth aerocapture entirely removed?

**Author:** hyperion (post-STOP override session, 2026-05-15).
**Status:** pre-result (hypothesis pre-registered with central estimates computed BEFORE range, per recurring-lesson-#N updated intervention).

---

## Motivation

R-chunk-as-heat-shield closed with aggregate verdict "falsified — multi-pass aerobraking is not the right architectural choice for ICEBERG, the ballistic coefficient is too high." It explicitly named THREE follow-on candidates (lines 178–180 of its STUDY.md):

> - **R-deployable-drag-skirt:** size the inflatable area, propellant cost to deploy, mass penalty.
> - **R-hybrid-aerocapture-aerobraking:** model the single-pass-then-multi-pass trajectory with bag sacrificed in the first pass.
> - **R-no-atmospheric-capture-baseline:** explicitly fall back to the pre-aerocapture matrix and confirm that propulsive-only inbound (the conservative architecture) closes economically.

R-deployable-drag-skirt was killed at orchestrator commit `34a473b`. R-hybrid-aerocapture-aerobraking was never run. R-no-atmospheric-capture-baseline was never run. R-aerocapture-fast-cruise-envelope (this session, prior round) just showed that the chunk-as-heat-shield mitigation also collapses under Round F's higher entry velocity (and that the anchor used in matrix updates was Saturn's misread of R-chunk-as-heat-shield's actual aggregate verdict).

This round runs the conservative-architecture confirmation that R-chunk-as-heat-shield asked for, eight rounds and one matrix-reframing later. The question is binary: with Earth aerocapture removed (no chunk-as-heat-shield, no drag skirt, no aerobraking), is ANY combination of (chemical-kick, electric-inbound, Saturn power class, chunk size, transfer time) a surviving cell?

---

## Pre-registered hypothesis (H-nacb)

### Recurring-lesson-#N anchor — derived from PRIMARY texts (not SCOPE summaries)

Per the updated recurring-lesson reading from R-aerocapture-fast-cruise-envelope: anchors must come from primary STUDY.md Reading and Revisit sections of source rounds, not orchestrator SCOPE summaries.

**Anchored back-of-envelope (computed FIRST, before sub-claim ranges):**

| Quantity | Anchor (primary source) | Source |
|---|---:|---|
| Earth velocity-at-infinity at heliocentric Hohmann arrival | 10.55 km/s | computed from Round F config (`v_perihelion 40.33 − v_Earth 29.78`) |
| Earth periapsis velocity (hyperbolic, no aerocapture) | 15.29 km/s | sqrt(v_∞² + v_escape²) at 125 km |
| Δv for chemical impulsive capture into low Earth orbit | 7.62 km/s | v_periapsis_hyp − v_circ_LEO 7.67 |
| Hydrolox mass ratio at Δv = 7.62 km/s, Isp 450 s | 5.62 | exp(7620/(450 × 9.80665)) |
| Propellant required for chemical Earth capture, 263.8 t entry mass | 1219 t | 263.8 × (5.62 − 1) |
| If propellant carried from Saturn at 6.16 km/s electric-inbound burn (mass ratio 1.366) | 2025 t at Saturn departure | (1219 + 263.8) × 1.366 |
| Chunk water available (200 t) as fraction of Saturn-departure propellant | 9.9 percent | 200 / 2025 |
| Continuous-thrust electric inbound total Δv (titan) | 17.97 km/s Earth-side + 6.16 km/s Saturn-egress = 24.13 km/s | titan R-inbound-dv-continuous-thrust |
| Mass ratio for full electric inbound at Isp 2000 s | 3.50 | exp(24130/(2000 × 9.80665)) |
| Chunk-fed propellant fraction at this mass ratio | 71.4 percent of chunk | (1 − 1/3.50) × 100 |
| Chunk water remaining after full electric inbound | 57 t | 200 × (1/3.50) |
| Tug delivered after chunk consumed | depends on vehicle dry mass | rhea baseline ~64 t tug, no remaining chunk delivery margin |

### Sub-claim ranges (anchored to back-of-envelope FIRST)

| Sub-claim | Central anchor | Predicted range | Falsification threshold |
|---|---:|---|---|
| H-nacb-a — chemical-Earth-capture propellant for Round F closing-case mass | 1219 t | 1000–1500 t | outside range |
| H-nacb-b — Saturn-departure mass if chemical-Earth-capture propellant carried | 2025 t | 1700–2400 t | outside range |
| H-nacb-c — chunk-water fraction of Saturn-departure propellant (chemical-capture branch) | 9.9 percent | 7–13 | outside range |
| H-nacb-d — electric-only inbound mass-ratio at full-titan Δv 24.13 km/s, Isp 2000 s | 3.50 | 3.0–4.2 | outside range |
| H-nacb-e — chunk water remaining after electric-only inbound | 57 t | 45–80 | outside range |
| H-nacb-f — number of surviving cells (any combination) at L0-05 strict 15 yr round-trip with aerocapture removed | 0 | 0–2 | outside range |
| H-nacb-g — number of surviving cells at L0-05 soft-margin 17 yr round-trip with aerocapture removed | 0 | 0–4 | outside range |

### Aggregate (H-nacb-agg)

With Earth aerocapture entirely removed (no chunk-as-heat-shield, no drag skirt, no aerobraking), there are ZERO surviving cells in the architectural matrix at the strict L0-05 15-year round-trip ceiling, and ZERO surviving cells at the soft-margin 17-year ceiling. Both candidate Earth-arrival mechanisms (chemical impulsive at Earth periapsis, electric continuous-thrust spiral) collapse: the chemical-capture branch demands 1200+ tonnes of propellant at Earth that cannot be sourced from chunk water, requires Earth-launch tankering at ~12 Starship launches per mission, and back-propagates to a 2000+ tonne Saturn-departure mass; the electric-inbound branch is the falsified all-electric end-to-end architecture from rhea's R-megawatt-marvl-radiator, with closest miss at 1 megawatt-electric of round-trip 19.56 yr, delivered minus 34.4 t.

The matrix's surviving cell is the falsified cell. With this round's confirmation, the matrix's "surviving cell" entry should read EMPTY pending fresh architectural recovery (smaller chunks per R-megawatt-chunk-100t, hybrid aerocapture-then-aerobraking with bag-sacrificed first pass per R-chunk-as-heat-shield's named follow-on, or sacrificial-bag economic line-item).

### Recurring lesson #N watchpoint

This round is anchored on PRIMARY-text numbers (titan's STUDY.md, rhea's STUDY.md, R-chunk-as-heat-shield's STUDY.md, Round F's JSON output) per the R-aerocapture-fast-cruise-envelope updated lesson. If pre-registration intuition is falsified again this round, the lesson updates further: hyperion's anchoring problem extends to PRIMARY-text reading too — possibly hyperion is selectively quoting primary text the same way Saturn selectively quoted from R-chunk-as-heat-shield.

If this round HOLDS, that is hyperion-3's first held aggregate after seven falsifications (counting R-aerocapture-fast-cruise-envelope) — and the broader matrix takeaway is the kill-shot finding: with aerocapture removed, the matrix's surviving cell is empty.

---

## Method

Deterministic. Sub-second wall clock. No randomness.

For each (transfer-time aphelion, reactor power class, chunk size, Earth-arrival mechanism) tuple:

1. **Compute heliocentric arrival velocity** at Earth orbit from vis-viva (using Round F config).
2. **Compute Earth velocity-at-infinity** = v_perihelion − v_Earth − optional 2 km/s lunar gravity assist credit.
3. **Compute Earth-arrival propellant** under each mechanism:
   - Chemical impulsive: Δv = sqrt(v_∞² + v_escape²) − v_circ_LEO; propellant = m_arrival × (exp(Δv/(Isp × g)) − 1).
   - Electric continuous-thrust: Δv = v_∞ + v_escape (heliocentric decelerate + LEO spiral, per titan); propellant = m_arrival × (exp(Δv/(Isp × g)) − 1).
4. **Back-propagate** through inbound electric burn (Saturn-egress 6.16 km/s, Isp 2000 s) to find Saturn-departure mass.
5. **Back-propagate** through outbound chemical-kick (matrix-impulsive ~6 km/s) to find low-Earth-orbit mission-1 launch mass.
6. **Closure check** at L0-05 strict (15 yr) and soft-margin (17 yr) round-trip.

### Sweep axes

- Transfer time aphelion: 9.58, 10.50, 11.0, 12.0 astronomical units.
- Reactor power class: 500, 1000, 2000 kilowatt-electric.
- Chunk size: 100, 200, 350 tonnes.
- Earth-arrival mechanism: chemical-impulsive, electric-continuous.
- Lunar gravity assist: with 2 km/s, without.

### Outputs

- `results/R_no_atmospheric_capture_baseline.json` — per-tuple closure verdict.
- `results/tables.md` — human-readable summary.
- `results/closure_verdict.md` — single-paragraph kill-shot verdict.

---

## Validity caveats

1. **Heliocentric Δv approximations.** Vector-Lambert-DV machinery from Round F is reused; same caveats apply (Type-I half-orbit symmetric).
2. **Chemical-capture single-impulse assumption** is best-case for chemical; multi-burn would not improve much in vacuum but adds gravity losses.
3. **Electric-capture mass-ratio assumes chunk-fed.** If propellant is non-chunk-water, mass ratio is the same but the architecture is different (and worse, because non-chunk propellant must be Earth-launched).
4. **No solar-augmentation upside.** R-hybrid-solar-augmentation (orphan branch round) showed solar gain is negligible at megawatt-class power; included as Validity caveat #11 not a closure path.
5. **Tug dry mass not reactor-scaled within this round** — using rhea baseline 63.8 t at 500 kWe and scaling proportionally for higher powers per MARVL anchored mass.
6. **Lunar gravity assist credit at 2 km/s** is matrix standing value; favorable epochs only (per R2 lunar gravity assist analysis, 60–85% of arrival epochs).
7. **Saturn-egress chemical kick still allowed.** Variant B configuration (chemical Saturn-egress + electric inbound + electric or chemical Earth arrival) still tested; Variant A (no recoveries) is the baseline.
8. **Outbound chemical kick uses 5 km/s realistic rather than 9 km/s conservative.** Per Round F config.
9. **Tug survival on entry not modeled** because there is no aerocapture; tug arrives at LEO via propulsive capture or fails entirely.

---

## Test

`run.py`. Deterministic.

---

## Revisit clause

To be filled after run. Will report number of surviving cells at strict and soft-margin L0-05 across the sweep, identify any closing combination, and update recurring-lesson-#N reading based on whether pre-registration intuition (kill-shot prediction) held or failed.
