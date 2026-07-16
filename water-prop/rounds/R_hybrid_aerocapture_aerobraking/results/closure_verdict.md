# R-hybrid-aerocapture-aerobraking — closure verdict

## Headline

The hybrid pass-1-deep-aerocapture + pass-2-onward-shallow-aerobraking architecture DOES NOT CLOSE at any cell in the architecturally-relevant envelope under conservative anchors (US Standard 1976 atmosphere, ice tensile 1.0 MPa, boundary-layer-blocking 0.4, body-absorbed fraction 0.5, L0-05 strict 15-yr ceiling).

**The matrix's 'hybrid-engineering-pending' framing (introduced by phoebe's prior R-chunk-as-heat-shield-revisit) is now closed.** Aerocapture-adjacent surviving cells collapse to drag-skirt-conditional only — R-deployable-drag-skirt is the new critical-path round. The Round-F STRICT-closing Variant C cell remains falsified at the engineering level; phoebe's prior round closed single-pass aerocapture; this round closes hybrid pass-1-deep + multi-pass shallow.

## Numbers anchored

- Pass-1 envelope: 230 of 1920 cells capture Δv-to-insert at the swept pass-1 altitudes.
- Pass-1 structural: 1780 of 1920 cells survive pass-1 chunk structurally.
- Pass-1 BOTH captures AND survives structurally: 90 of 1920.
- Aerobraking + sublimation + L0-05 closure: 0 of 1920.
- Sub-claims held: 8 of 9 gradable (+ 1 deferred).
- Aggregate H-hyb-agg: HELD.

## Three independent failure modes (mutually exclusive across periapsis axis)

1. **Pass-1 fails structurally** at any altitude where pass-1 Δv ≥ 4.18 km/s (chunk stress > 1 MPa tensile).
2. **Aerobraking is unphysical timescale** at any altitude where chunk T_eq < ice melt point (need ≥ 180 km, where pass count ≥ 3 million and time ≥ 700 yr).
3. **Chunk consumed by sublimation** at any altitude where time is tractable (≤ 130 km). Computed totals (after BLBF=0.4 × body-absorbed=0.5 = 0.20 reduction): 77 t at 110 km / 259 t at 130 km / 521 t at 150 km / 1040 t at 180 km / 1486 t at 200 km — all exceed the 100 t (50%) chunk-mass tolerance for a 200 t chunk, with the lowest-altitude (most tractable-timescale) cases worsening dramatically deeper.

The "deep, tractable, low-loss" interior solution does not exist — the three failure constraints are aligned along the periapsis axis without an interior closing region.

**Hypothesis H-hyb-e was falsified-conservative (predicted 1505 t at 130 km, computed 259 t).** The BOE applied heat-of-sublimation directly without compounding BLBF and body-absorbed fractions; the run.py applies both. The qualitative verdict (sublimation > tolerance) holds in both cases, so the conservative falsification does not rescue any cell.

## Three SCOPE input-assumption errors documented

Per methodology lesson 9 (anchor on PRIMARY-text aggregate verdict). All three errors documented in STUDY.md §'Three load-bearing methodology choices the SCOPE got partly wrong':

1. **β-by-chunk-size is non-monotonic when tug mass is held fixed.** β minimum is at chunk 100 t (β=5,936), not chunk 50 t (β=6,546). SCOPE's 'smaller-chunk-rescues-β' is geometrically broken.
2. **Pass-1 Δv-to-insert is set by parabolic-velocity threshold, not by 'engineering judgment 65 percent of total'.** At periapsis 75 km, Δv-to-insert = 4.175 km/s. The 'hybrid relaxes pass-1' intuition is wrong.
3. **Single-scale-height exponential atmosphere is qualitatively wrong above 110 km** where scale height grows to 20-30 km. Atmospheric model has been silently varying across aerocapture-adjacent rounds.

## Methodology propagation

**Methodology lesson 1 update:** at end of this round, the pessimistic-default heuristic has held in 13 of 13 aerocapture-adjacent pre-registrations across this campaign. The more-pessimistic-than-pre-registered pattern remains the dominant empirical signal — domain anchor for aerocapture-adjacent rounds is engineer-pessimistic-insufficient.

**Atmosphere-model PROTOCOL lesson candidate:** R-chunk-as-heat-shield, R-aerocapture-fast-cruise-envelope, R-chunk-as-heat-shield-revisit, and this round have used three different atmospheric models. The hyperion single-scale-height exponential (5.6e-7 at 100 km, H=7.5 km) underestimates US Standard 1976 density by ~40× at 180 km. For atmospheric-capture rounds spanning both deep (40-90 km) and shallow (130-200 km) regimes, the choice dominates aerobraking-pass-count verdict. Adopt US Standard 1976 / NRLMSISE-00 as the campaign default; flag prior aerocapture rounds for re-derivation if verdict changes under the standard model. Candidate for PROTOCOL methodology lesson 10.

## Matrix updates

- Retire 'hybrid-engineering-pending' framing. Replace with 'atmospheric-capture-falsified-without-drag-skirt.'
- R-deployable-drag-skirt promoted to next critical-path round.
- Adopt US Standard 1976 atmosphere as campaign default; re-derive prior aerocapture rounds at the standard model if their verdicts are atmosphere-sensitive.

## Open dependencies

- R-chunk-as-heat-shield-revisit's orientation-stability question remains open and is now downstream of an aerocapture branch whose every cell has been falsified.
- R-deployable-drag-skirt (mass budget for inflatable ballute) — primary recovery candidate.
- R-mission-architecture-pivot-survey (lunar-orbit catcher, cislunar processing) — alternative-branch follow-on.