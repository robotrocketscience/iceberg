# R-outbound-dv-continuous-thrust — does R-electric-outbound's outbound integrated Δv hold under continuous-thrust treatment?

**Round:** R-outbound-dv-continuous-thrust
**Started:** 2026-05-15
**Worker:** Rhea
**Branch:** iceberg-rhea
**Status:** complete, graded, committed

---

## Phase question

Titan's R-inbound-dv-continuous-thrust corrected the matrix's 6.42 km/s impulsive-equivalent inbound delta-velocity by adding the two Saturn-side terms (planet-side Edelbaum spiral + heliocentric retrograde) that continuous-thrust electric propulsion must pay in full. **Did R-electric-outbound make the same methodology error in reverse?** R-electric-outbound's outbound Δv = v_circ_LEO + v_inf_Earth = 17.97 km/s only captures segments (5') and (4') of the symmetric four-segment decomposition. Adding (2') Saturn-side heliocentric decelerate and (1') Saturn-side Edelbaum capture spiral closes the methodology asymmetry and gives the *true* outbound continuous-thrust delta-velocity. Question: by how much does the corrected number exceed 17.97 km/s, and what does it do to my prior R-electric-outbound-rerun's "0.17-year miss" of L0-05?

## Hypothesis (pre-registered)

- **H-od-a** — Outbound continuous-thrust integrated Δv to high-elliptical Saturn arrival (1 million km), no lunar gravity assist: 27–32 km/s.
- **H-od-b** — Outbound continuous-thrust integrated Δv to B-ring Saturn arrival (1.35 × 10⁵ km), no lunar gravity assist: 37–42 km/s.
- **H-od-c** — Corrected outbound Δv to high-elliptical is at least 1.5× R-electric-outbound's 17.97 km/s.
- **H-od-d** — Round-trip at 1 MWe / decomposed-mid / outbound-arrival-high-elliptical / titan-inbound-24.7 km/s **exceeds 18 years** (R-electric-outbound-rerun's value at OLD outbound Δv was 15.17 yr; predicted Δ from outbound correction alone ≥ 3 yr).
- **H-od-e** — Best-case composite (high-elliptical both ends + lunar gravity assist credit on both legs) round-trip **exceeds 15 years** (architecture cleanly falsified at L0-05 under continuous-thrust treatment at both ends).

## Test

`run.py` mirrors titan's segment decomposition, applied to the outbound leg:

- Segment **(5')** LEO Edelbaum escape spiral = v_circ at LEO altitude.
- Segment **(4')** Earth-side heliocentric accelerate = v_∞ at Earth (Hohmann perihelion − Earth orbital speed).
- Segment **(2')** Saturn-side heliocentric decelerate = v_∞ at Saturn (Saturn orbital speed − Hohmann aphelion).
- Segment **(1')** Saturn-side Edelbaum capture spiral = v_circ at the chosen arrival orbit.

Sweeps Saturn arrival orbits matching titan's departure orbits: B-ring (1.35 × 10⁵ km), high-elliptical (1.0 × 10⁶ km), Iapetus-distance (3.561 × 10⁶ km). Reports both no-LGA and LGA-credited variants for symmetry with titan's treatment.

Round-trip composition uses corrected outbound Δv (this round) AND corrected outbound burn formula (R-electric-outbound-rerun's `burn_from_dry_end`) AND titan's corrected inbound Δv AND chunk-fed wet-at-start inbound burn formula. The 1 MWe / decomposed-mid tug mass (31.5 t) is the converged value from my prior rerun at the OLD outbound Δv; in a self-consistent iteration with the new outbound Δv it would grow slightly (tank fraction scales with prop mass), so the corrected round-trip totals here are if anything slight under-counts.

## Result

### Outbound continuous-thrust integrated Δv (no lunar gravity assist)

| Saturn arrival orbit | 5' LEO spiral | 4' Earth-helio | 2' Saturn-helio | 1' Saturn spiral | **Total Δv (km/s)** | Δ vs 17.97 |
|---|---:|---:|---:|---:|---:|---:|
| B-ring 1.35 × 10⁵ km | 7.67 | 10.30 | 5.45 | 16.75 | **40.17** | +22.20 |
| high-elliptical 1 × 10⁶ km | 7.67 | 10.30 | 5.45 | 6.16 | **29.56** | +11.59 |
| Iapetus-distance 3.561 × 10⁶ km | 7.67 | 10.30 | 5.45 | 3.26 | **26.67** | +8.70 |

The B-ring outbound number (40.17 km/s) is essentially equal to titan's B-ring inbound number (40.2 km/s). Symmetric, as it should be — the two are time-reversals of each other modulo LGA direction.

### Round-trip composition at 1 MWe / decomposed-mid / Isp 2000 s / chunk 200 t

| Outbound arrival | Inbound regime | t_out (yr) | t_in (yr) | Round-trip (yr) | Delivered (t) | Closes 15 yr? |
|---|---|---:|---:|---:|---:|:--:|
| B-ring | titan high-elliptical 24.7 km/s | 2.00 | 1.55 | **16.72** | 34.2 | no |
| B-ring | titan B-ring 40.2 km/s | 2.00 | 1.89 | 17.06 | −1.7 | no |
| high-elliptical | titan high-elliptical 24.7 km/s | 1.04 | 1.55 | **15.76** | 34.2 | no |
| high-elliptical | titan B-ring 40.2 km/s | 1.04 | 1.89 | 16.10 | −1.7 | no |
| Iapetus-distance | titan high-elliptical 24.7 km/s | 0.86 | 1.55 | **15.58** | 34.2 | no |
| Iapetus-distance | titan B-ring 40.2 km/s | 0.86 | 1.89 | 15.92 | −1.7 | no |

### Best-case composite

High-elliptical Saturn arrival, lunar gravity assist credit on outbound (27.56 km/s instead of 29.56), titan high-elliptical inbound with LGA (24.7 km/s):

- t_outbound burn: 0.92 yr
- t_inbound burn: 1.55 yr
- Round-trip: **15.64 yr** — **misses the 15-year L0-05 ceiling by 0.64 yr**
- Delivered: 34.2 t out of 200 t (17.1% delivered fraction)

### Hypothesis grading

| Sub-claim | Predicted | Actual | Held? |
|---|---|---|---|
| H-od-a — outbound Δv high-elliptical no-LGA | 27–32 km/s | 29.56 km/s | yes |
| H-od-b — outbound Δv B-ring no-LGA | 37–42 km/s | 40.17 km/s | yes |
| H-od-c — corrected ≥ 1.5× 17.97 km/s | ≥ 1.5× | 1.65× | yes |
| H-od-d — round-trip > 18 yr | > 18 yr | 15.76 yr | **falsified** |
| H-od-e — best-case round-trip > 15 yr (architecture falsified at L0-05) | > 15 yr | 15.64 yr | yes |

## Reading

**The methodology asymmetry was real and load-bearing.** R-electric-outbound's outbound delta-velocity was missing the two Saturn-side terms by exact mirror to what titan's R-inbound-dv-continuous-thrust corrected for the inbound leg. The B-ring outbound number (40.17 km/s) matches titan's B-ring inbound (40.2 km/s) bit-for-bit modulo the small numerical noise of the v_∞ subtraction — that's the sanity check that the segment decomposition is correctly symmetric.

**The corrected outbound Δv adds ~0.6 yr to round-trip at 1 MWe / decomposed-mid, not 3+ yr** as H-od-d predicted. Why I over-predicted: outbound burn time at constant thrust grows with propellant mass, not directly with Δv. At 1 MWe / 31.5 t tug, the outbound mass-ratio grows from 2.50 (at 17.97 km/s) to 4.51 (at 29.56 km/s), so outbound prop grows from ~47 t to ~111 t — but burn time scales linearly with prop mass at fixed thrust, going from 0.44 yr to 1.04 yr. That's a 2.4× burn-time growth, not the 4×+ I implicitly predicted. The pre-registered H-od-d band was wishful arithmetic. Methodology lesson noted: when extrapolating burn-time effects from Δv changes at constant power, do the rocket-equation arithmetic on a napkin BEFORE writing the pre-registration band.

**Best-case composite still misses L0-05 cleanly.** Even with the most favorable assumptions (high-elliptical both ends, LGA credit applied to both legs, decomposed-mid tug, 1 MWe, Isp 2000 s, 200 t chunk), round-trip = 15.64 yr. The L0-05 miss is 0.64 yr — 3.8× the 0.17-yr miss I reported in R-electric-outbound-rerun under the under-counted outbound Δv. **At realistic conservative assumptions the megawatt all-electric end-to-end architecture is comfortably falsified at L0-05, not marginally falsified.**

**Note on the cross-check with my prior rerun.** Using R-electric-outbound's old 17.97 km/s outbound Δv at the same 1 MWe / decomposed-mid / titan-24.7-inbound operating point, this round reproduces the rerun's 15.17 yr round-trip cleanly. So this round is a layered correction on top of my prior rerun, and the chain of corrections is auditable.

**Titan's round also used the bugged-and-under-counted outbound burn time** (its `OUTBOUND_BURN_YR_BY_KWE` lookup table copied R-electric-outbound's bugged numbers). Titan's headline finding (inbound continuous-thrust Δv 24.7–40.2 km/s) is unaffected — that's an inbound-only computation — but titan's round-trip *totals* understate by ~0.27 yr at 1 MWe (matching my rerun's outbound-burn-time understatement). If the orchestrator pulls round-trip totals from titan's tables directly, they should be re-derived from this round's corrected outbound burn time.

**Architecture implications.** Combined with R-electric-outbound-rerun's L0-05 closure pattern:

- **Matrix-inbound 6.42 km/s + corrected outbound 29.56 km/s + decomposed-mid 1 MWe** would close (the chunk-fed inbound is cheap). But this is the *impulsive-inbound* assumption that titan invalidated — using it is a methodology regression.
- **Titan-inbound 24.7 km/s + corrected outbound 29.56 km/s + decomposed-mid 1 MWe** = 15.76 yr, miss by 0.76 yr.
- **Best-case composite (LGA both legs)** = 15.64 yr, miss by 0.64 yr.
- **B-ring departure either way** = chunk-fed delivered mass goes negative.

The four rescue paths from R-electric-outbound-rerun's STUDY remain, but the L0-05 amendment needed is now ≥ 17 yr (not the ≥ 15.2 yr the prior rerun implied). Chunk-size reduction is more attractive (cuts both inbound and outbound burn times). Chunk-as-heat-shield rescue is even more attractive — it collapses the ~18 km/s Earth-side terms (segments 4' + 5' on outbound and 4 + 5 on inbound) into aerodynamic passes, which could in principle save ~24 km/s of round-trip Δv ledger.

## Revisit

H-od-a, H-od-b, H-od-c, H-od-e all held cleanly. H-od-d falsified — I over-predicted round-trip growth from outbound Δv correction. The arithmetic mistake: I treated outbound burn time as scaling super-linearly with Δv (mass-ratio in propellant, then mass-ratio in burn time). Actually burn time at fixed thrust scales linearly with propellant mass, and propellant mass scales as (mass_ratio − 1) at constant tug mass. At Δv going from 18 to 30 km/s with v_e = 19.6 km/s, (e^x − 1) goes from 1.50 to 3.51 — so 2.3× growth in burn time, not 3×+. Pre-registration band [> 18 yr] presumed the wider growth.

The H-od-d falsification is informative because it tells me the bug-fix-and-DV-correction cascade does NOT push round-trip past 18 yr — the 17.06 yr B-ring-outbound + B-ring-inbound case is the worst tested at 1 MWe / decomposed-mid. So a requirements amendment to ~17 yr (not 18+) is sufficient to recover ALL but the chunk-fed-economics-break cases. Smaller-than-expected requirements amendment may be politically easier than I had been framing.

Bug-catch convention: H-od-d is a bad-pre-registration falsification, not an architectural-claim falsification. I should mark it differently in the convention log — "self-imposed numeric range too narrow" rather than "predicted effect doesn't exist."

## Cross-learning

- **Negative for R-electric-outbound:** outbound delta-velocity itself is methodologically wrong, not just the burn-time formula. The 17.97 km/s should be replaced (or annotated as a known under-count) before the matrix or any downstream document quotes it again. Orchestrator decision: patch in place, or preserve as audit-trail with forward pointer to this round.
- **Negative for titan's round-trip totals:** the OUTBOUND_BURN_YR_BY_KWE lookup in titan's run.py inherits R-electric-outbound's bugged values. Titan's inbound headline is unaffected, but the round-trip totals reported in titan's STUDY are understated by ~0.27 yr at 1 MWe. Worth a footnote in the orchestrator integration but does not change titan's conclusions.
- **Positive for R-chunk-as-heat-shield-revisit (deferred → high priority):** corrected Δv ledger says the Earth-side terms (segments 4' + 5' outbound, 4 + 5 inbound) total ~36 km/s of Δv across the round-trip — the largest single bloc. If aerodynamic passes at Earth can substitute for both legs, that's the architecturally cleanest path to L0-05 closure.
- **Negative for chunk-size-reduction as a rescue path at large chunks:** with corrected outbound Δv, even 200-t chunks now miss L0-05 by 0.6+ yr. Chunk shrinkage to 100 t (which was the cheapest rescue path under R-electric-outbound-rerun) helps but does not on its own restore closure — outbound now matters too.
- **Methodology lesson (added to convention log):** when extrapolating burn-time effects from Δv changes at constant power, do the rocket-equation arithmetic on a napkin before fixing the pre-registration band. The growth rate is (e^x − 1) at fixed tug mass, not e^x.
- **Methodology lesson:** when one round corrects a leg of a multi-leg computation under a methodology principle, audit the symmetric leg in the same pass. Titan's correction should have been a two-round pair (inbound + outbound symmetric). It wasn't — and that's now this round.

## Files of record

```
water-prop/rounds/R_outbound_dv_continuous_thrust/STUDY.md
water-prop/rounds/R_outbound_dv_continuous_thrust/run.py
water-prop/rounds/R_outbound_dv_continuous_thrust/results/outbound_dv_continuous.json
water-prop/rounds/R_outbound_dv_continuous_thrust/results/tables.md
```

## Out of scope

- Did not re-iterate self-consistent tug mass at corrected outbound Δv. Effect is small (~3–10% tug mass growth from tank fraction) but the round-trip totals here are slight under-counts. Orchestrator-level decision whether to re-run R-electric-outbound-rerun with iterated tug mass.
- Did not test outbound Δv with non-Hohmann trajectory (low-thrust spiral trajectories typically beat Hohmann under continuous thrust on time but not on Δv — and L0-05 binds at time). Out of scope for this round; promote to a separate trajectory-optimization round if the closure picture warrants the effort.
- Did not propagate to titan's `OUTBOUND_BURN_YR_BY_KWE` lookup — that's a titan-round edit and I do not own that worktree.
