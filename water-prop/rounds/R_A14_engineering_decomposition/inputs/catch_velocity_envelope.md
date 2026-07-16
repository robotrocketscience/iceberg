# Catch-velocity envelope — sub-steps 3 (catch) and 4 (containment)

The pitch text quotes a **millimetre-per-second** closing velocity for the trawl-bag capture. This document derives where that figure comes from, what the *realistic* closing-velocity envelope is under autonomous-proximity-ops uncertainty, and why catch (3) and containment (4) probabilities split sharply by regime.

## Where the mm/s figure comes from

Two co-orbiting bodies on nearly-identical heliocentric / Saturn-centric orbits have a relative velocity dominated by the small difference in their orbital elements. For a tug that has matched the target chunk's orbit to within a small radial offset Δr at semi-major axis a (Saturn-centric), the differential orbital velocity is approximately:

    Δv_orbital ≈ (1/2) · v_orbit · (Δr / a)

In Saturn's B-ring (a ≈ 1.1 × 10⁵ km, v_orbit ≈ 18 km/s Keplerian), matching to Δr ≈ 100 m gives Δv ≈ 0.5 × 18000 × (0.1 km / 110000 km) ≈ **8 mm/s**. So mm/s closing is *physically achievable* — it is the natural relative velocity once the tug has station-kept to ~100 m. This confirms the pitch's mm/s claim is not fantasy: it is the co-orbital drift velocity at close station-keeping.

## Why the realistic envelope is wider

The mm/s figure is the **achievable floor** under ideal station-keeping, not the **operating point** under autonomy uncertainty. Three effects widen it upward:

1. **Light-time autonomy.** Saturn one-way light-time is ~70–90 minutes. Closed-loop terminal guidance must be fully autonomous; ground cannot intervene during the final approach. OSIRIS-REx and Hayabusa2 both ran autonomous terminal descent, but over *seconds-to-minutes* of light-time, not 80 minutes of round-trip latency. Residual closing-velocity error after autonomous nulling is plausibly 0.1–1 m/s, not mm/s.
2. **Ring-particle proper motion + rotation.** A multi-tonne ring chunk is not a cooperative target. It tumbles (unknown spin state) and has local Keplerian shear across its own diameter. The bag must close on a moving, rotating surface; the effective closing velocity at the contact point includes the surface tangential velocity from rotation.
3. **Bag-aperture approach geometry.** To get the chunk *inside* the aperture rather than glancing off the rim, the approach must be near-axial. Off-axis components convert to tangential velocity at contact, raising the effective catch energy.

## Three operating points used in the sensitivity table

| Regime | Closing velocity | Interpretation | Catch (3) | Containment (4) |
|---|---|---|---|---|
| mm/s (pitch nominal) | ~0.01 m/s | ideal co-orbital station-keeping; bag aperture margin large vs chunk cross-section; near-zero impact energy | high (~0.88) | high (~0.78) |
| low-m/s (realistic autonomy) | ~0.3 m/s | residual after autonomous terminal nulling at Saturn light-time; modest impact energy; some rim-glance risk | mid (~0.78) | mid (~0.68) |
| high-m/s (worst credible) | ~1.0 m/s | poor terminal nulling + tumbling target; chunk fragments on contact transfer momentum the soft bag may not absorb cleanly | low (~0.65) | low (~0.55) |

**Why containment degrades faster than catch with velocity.** Catch is a geometry problem (did the chunk cross the aperture plane?). Containment is an energy problem (did the chunk stay in after entering?). Impact kinetic energy scales as v², so a 100× velocity increase (0.01 → 1.0 m/s) is a 10⁴× energy increase. At mm/s the chunk drifts to rest against the bag with negligible energy; at 1 m/s a 200-tonne chunk carries 100 kJ, enough to tear a soft-fabric bag or fragment a friable ice aggregate, which then transfers momentum to the bag in ways the Vectran-aerogel laminate may not absorb without a tear or cinch failure. This is why containment (sub-step 4) is the load-bearing weakest link, and why it is *velocity-conditional*, not a fixed number.

## Reading

The mm/s closing velocity is achievable and is the right *design target*, but it is not yet *demonstrated* on a non-cooperative tumbling target at Saturn light-time. The whole A14 joint posterior pivots on whether a demonstrator confirms catch + containment at mm/s, or whether autonomy uncertainty forces the operating point up to the low-m/s regime where containment falls to ~0.68. **This is the single most decision-relevant uncertainty in the A14 decomposition** and the primary thing an Earth-orbit catch-and-contain demonstrator retires.
