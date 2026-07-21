# R-titan-tour-ephemeris — STUDY

**Round:** R-titan-tour-ephemeris. SCOPE pre-registered 2026-07-21. All four hypotheses **HELD** — and because this round registered the *falsification of R179's adopted lever* as its hypotheses, "held" means: **the Titan pump-up departure tour is revoked.** This is the check R179's own Revisit demanded before baselining. It did its job.

## Results vs registered hypotheses — all four HELD

### H1 — the bound-chain ceiling — **HELD**

A flyby conserves v∞ relative to Titan; every orbit between flybys must stay bound to re-encounter Titan. A pure flyby chain's departure excess is therefore capped by one final kick from a barely-bound orbit: **3.28 km/s** central (3.05–3.33 across Titan-radius × flyby-altitude corners) — **53 % of the required 6.21 km/s**, at every corner. R179's "v∞ pumped free" line was assumed, never bound-checked; it is impossible from any raise orbit at any flyby count. The pump-*down* (capture) direction is immune — its free direction descends *into* the bound region — which is why the two sides R179 priced as symmetric are not.

### H2 — the honest floor — **HELD (R179's floor falsified)**

Best repair over four strategy families: **8.38 km/s**, achieved not by a tour at all but by **S4 — a 5.4 km/s-excess periapsis burn plus a single outbound Titan kick**. Saving vs the direct 8.45: **0.07 km/s (0.8 %)**, not 1.45 km/s (17 %). Powered final flyby 8.63; contour-periapsis residual 8.84; pump-plus-post-escape-burn 10.01 (worse than direct — buying v∞ without Oberth leverage). The S5 family converging to the single-burn cost as r_a → ∞ is the Tisserand-continuum consistency check: there is no contour you can reach cheaply that pays out more than it cost. **R179's registered floor band 6.8–7.3 is falsified; the −17 % departure lever is revoked.**

### H3 — the −33 % power lever dies — **HELD**

2-yr chunk-fed departure burn, honest anchors: impulsive-gas-hybrid best **155 kWe** (−11 %); **pure low-thrust Titan-assisted 224 kWe (+28 % — the detour *hurts* a pure low-thrust ship**, which buys the exit kick's 2.9 km/s shortfall back at no leverage). The 117 kWe branch is revoked; **bet #3's requirement band collapses from 117–175 to ≈ 155–175 kWe.**

### H4 — what survives — **HELD**

Capture-side ring circularization **6.70 km/s stands** (it *is* the Hohmann-tangential bound; R179 was right for the reason it gave). Honest max-assist round trip **15.09 km/s** — above R179's 13.3–14.1 band and within **3 % of retired axis-19's 14.7**; the desk-retired residence figure looks better with every honesty pass. Exit sequencing is schedule, not Δv: 6 flybys ≈ 0.52 yr (phoebe 2×T convention), plus 0–1.3 declination-crank flybys depending on epoch (free at the 2032.7 solstice, worst at the 2040.1 equinox). Iapetus adds ≈ 0.2 km/s of exit excess — a trim, not a bridge.

## Bug-catch (protocol §bug-catch)

Two pre-freeze fixes documented in SCOPE (hand-typed H3 constants replaced with derived values per the R184 red-flag rule; mangled Iapetus print). None at run time.

## Revisit (mandatory)

Patched conics throughout; the ceiling assumes optimal single-kick geometry (real targeting derates it — the honest saving is if anything *smaller*). Same-rev double flybys (π-transfer-like Titan-Titan pairs) could in principle chain two kicks without an intervening bound return; rare, fragile phasing, unmodeled — bounded above by 2× the single-kick ceiling, still short of 6.21. v∞-leveraging DSMs change v∞,T at 2–5× leverage but the S5 continuum shows contour-hopping has no free endpoint; a full VILT sweep would tighten, not overturn. The 6.21 km/s requirement itself is the state-of-record Hohmann-return excess; a slower heliocentric return (lower v∞) trades transit years against departure Δv and was not re-opened here. Capture-side pump-down claims (`R_saturn_moon_ga_ephemeris`) not re-adjudicated: its single-flyby capture works only at arrival v∞ ≲ 4.4 km/s — **flag to orchestrator**: verify the mission_graph capture options' arrival-v∞ assumptions against that threshold when absorbing this round.

## Cross-learning

- **For the matrix (headline):** *R179's Titan pump-up departure lever is revoked by its own demanded ephemeris check.* Departure from co-orbital B-ring is 8.4–8.5 km/s propulsive, Titan or no Titan. Bet #3's power band narrows to ≈ 155–175 kWe (the 117 kWe floor is gone). The capture-side adoption (pump-down) is untouched.
- **Method lesson (proposed):** *symmetry claims between time-reversed trajectory legs must be checked against constraints that are not time-symmetric* — boundedness between flybys binds pump-up, not pump-down. R179 corrected six rounds and then planted its own uncorrected assumption; the campaign's correction machinery caught it one round later.
- **Third corroboration of retired axis-19:** 14.7 vs honest 15.09 (2.6 %). The retired residence-class number is the best desk anchor the campaign ever produced.
- **Follow-ons:** slow-return trade (v∞ < 6.21 for longer transit — does it beat the S4 floor on launched-mass?); VILT sweep (tighten, not overturn); orchestrator flag on capture-arrival v∞ assumptions.
