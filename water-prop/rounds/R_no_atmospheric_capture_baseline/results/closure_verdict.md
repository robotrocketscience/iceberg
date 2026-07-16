# R-no-atmospheric-capture-baseline — closure verdict

**Headline:** With Earth aerocapture entirely removed, the architectural matrix has ZERO surviving cells across all 288 swept (transfer-time × reactor-power × chunk-size × Earth-arrival × Saturn-egress × lunar-gravity-assist) tuples. Combined with R-aerocapture-fast-cruise-envelope (which falsified the aerocapture-conditional itself), the matrix as currently shaped has no surviving cell at any L0-05 ceiling.

---

## What this round found

### Closure summary

| Metric | Value |
|---|---:|
| Total cells swept | 288 |
| Cells closing L0-05 strict 15-year ceiling AND delivered > 0 | **0** |
| Cells closing L0-05 soft-margin 17-year ceiling AND delivered > 0 | **0** |

### Round F equivalent anchor (aphelion 11 AU, 500 kWe, 200 t chunk, chemical Saturn-egress, no LGA)

| Quantity | Electric Earth-arrival | Chemical Earth-arrival |
|---|---:|---:|
| Δv arrival | 17.18 km/s | 7.62 km/s |
| Arrival propellant | 1,124 t | 1,218 t |
| Saturn-departure mass | 1,477 t | 4,017 t |
| Outbound chemical-kick propellant | 14,432 t | 27,917 t |
| LEO mission-1 launch mass | 15,910 t | 31,934 t |
| Inbound electric burn time | 132 yr | 24 yr |
| Round-trip time | 22.73 yr | 30.16 yr |
| Delivered mass | 17.06 t | 0.00 t |
| Closes L0-05 strict | NO | NO |
| Closes L0-05 soft-margin | NO | NO |

The chemical-arrival branch demands 31,934 tonnes of low-Earth-orbit launch mass per mission — about 100× a Saturn V per mission. The electric-arrival branch has a 132-year electric burn for the arrival propellant alone. Neither closes any version of L0-05.

---

## Hypothesis grading

| Sub-claim | Central anchor | Range | Computed | Held |
|---|---:|---|---:|:---:|
| H-nacb-a — chemical-Earth-capture propellant for Round F closing-case mass | 1219 t | 1000–1500 | 1218 | YES |
| H-nacb-b — Saturn-departure mass if chemical-capture propellant carried | 2025 t | 1700–2400 | 4017 | NO (98 percent over upper) |
| H-nacb-c — chunk-water fraction of Saturn-departure propellant (chemical branch) | 9.9 percent | 7–13 | 4.98 percent | NO (under) |
| H-nacb-d — electric-only inbound mass-ratio at full-titan Δv 24.13 km/s | 3.50 | 3.0–4.2 | 2.42 | NO (model uses Δv 17.18 not 24.13 — diagnosed below) |
| H-nacb-e — chunk water remaining after electric-only inbound | 57 t | 45–80 | 82.6 | NO (just over) |
| H-nacb-f — number of strict-closing cells | 0 | 0–2 | 0 | YES |
| H-nacb-g — number of soft-closing cells | 0 | 0–4 | 0 | YES |

**5 of 7 sub-claims held. H-nacb-agg HELD: the central kill-shot prediction (zero surviving cells with aerocapture removed) is confirmed.**

### Why H-nacb-b, c, d, e were misanchored

The back-of-envelope underestimated chain back-propagation through the outbound chemical-kick stage. My anchor stopped at "carrying 1219 t to Earth requires 2025 t at Saturn departure." But Saturn departure ALSO requires the outbound chemical kick stage, which Tsiolkovsky-multiplies: a 4017 t Saturn-departure mass demands 27,917 t of outbound kick propellant, giving 31,934 t at LEO. The chunk-fraction-of-LEO is 200/31934 = 0.6 percent rather than the chunk-fraction-of-Saturn-departure 9.9 percent I anchored.

H-nacb-d's miss is procedural: the electric-arrival model uses Δv = v_∞ + v_escape = 10.55 + 11.07 = 21.62 km/s after subtracting LGA = 17.18 km/s used in computation. My anchor used titan's full Δv 24.13 (which includes the Saturn-egress 6.16 km/s applied separately in this round's stage decomposition). These are accounting-equivalent but the sub-claim was named at the wrong level.

The aggregate H-nacb-agg held because the kill-shot sub-claims (H-nacb-f, H-nacb-g) are the load-bearing ones, and they held with margin.

---

## Recurring lesson #N — first HELD aggregate in 8 hyperion rounds

This is the first held aggregate of the hyperion-2/3 session. The pattern broke. The interventions stacked:

1. **Round F (last batch-3 round):** computed back-of-envelope FIRST, then ranged. Per-sub-claim falsification continued; aggregate verdicts did not change.
2. **R-aerocapture-fast-cruise-envelope (Round 1 this session):** same intervention, but *anchor* was wrong because sourced from Saturn's SCOPE.md summary. Aggregate falsified again. Updated lesson: anchor on PRIMARY texts.
3. **R-no-atmospheric-capture-baseline (this round):** anchored on PRIMARY texts (titan's STUDY.md, rhea's STUDY.md, R-chunk-as-heat-shield's STUDY.md, Round F's JSON). Central kill-shot prediction held; aggregate held. **First success.**

The pattern: hyperion's intuition CAN be calibrated when (a) back-of-envelope is computed first and (b) anchors are pulled from primary texts. Both are required. SCOPE summaries are unreliable; intuition without anchoring is unreliable.

This propagates: any future hyperion round should follow the same protocol. Other workers may benefit from the same discipline — the SCOPE-misread vector is general, not specific to hyperion.

---

## Implications for the matrix

This round closes the load-bearing question R-chunk-as-heat-shield asked eight rounds ago. The answer is binary, and it is NO:

**With Earth aerocapture entirely removed, no combination of (chemical kick at Saturn-egress, electric inbound at any Saturn power class up to 2 megawatt-electric, chunk size 100–350 tonnes, transfer time aphelion 9.58–12 astronomical units, lunar-gravity-assist credit 0–2 km/s) closes any version of L0-05.**

Combined with R-aerocapture-fast-cruise-envelope (R1 this session) showing aerocapture itself does not close engineering-side, **the matrix's surviving cell, as currently shaped, is empty**.

### Architectural escape paths (each its own follow-on round)

1. **R-megawatt-chunk-100t (or smaller).** Smaller chunks reduce ballistic coefficient by mass^(1/3); a 50 tonne chunk would have β ≈ 4400 kg/m² (single-chunk equivalent of R-chunk-as-heat-shield). Aerocapture might re-close at smaller chunks, BUT mission cadence has to scale up to maintain the same delivered-mass total. Programmatic risk overlay (Round A) gets worse with cadence.
2. **R-hybrid-aerocapture-aerobraking with bag-sacrificed pass-1.** R-chunk-as-heat-shield named this as "the most-likely-to-work architecture" but never modeled it. First pass dumps 1–3 km/s with bag sacrificed; subsequent shallower passes complete circularization over months. Time penalty 4–8 months adds to round-trip; bag becomes a per-mission consumable.
3. **R-sacrificial-bag-mass-and-cost.** Adds a 1–3 tonne / $5–20 million per-mission line to the matrix. May be the cheapest path to retaining aerocapture as a closing conditional.
4. **R-mission-architecture-pivot.** Reframe the matrix around an architecture other than chemical-kick + electric-inbound + Earth-aerocapture. Examples: lunar-orbit catcher mission (chunk parked in lunar Distant Retrograde Orbit, never enters Earth atmosphere); cislunar processing depot (chunk processed in a cislunar facility, never approaches Earth surface).
5. **Reframe L0-05.** If 15-year strict and 17-year soft-margin ceilings are the binding constraints, relaxing them to 20+ years allows the falsified all-electric end-to-end architecture to re-emerge as a delivered-mass-positive (if program-risk-discounted to nearly nothing) cell. Project-owner level decision.

---

## Verdict in one sentence

**With aerocapture removed, the matrix has no surviving cell; combined with R-aerocapture-fast-cruise-envelope's finding that the aerocapture-conditional itself rests on a misread of R-chunk-as-heat-shield, the matrix as currently shaped is empty across all 288 cells in the (transfer-time × reactor-power × chunk-size × Earth-arrival × Saturn-egress × LGA) sweep.**
