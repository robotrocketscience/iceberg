# Round 2 — Lunar Gravity Assist Trajectory Analysis

**Question.** The conops claims a 3-flyby lunar gravity assist tour delivers approximately 3 km/s of arrival velocity reduction at zero propellant cost (risk B01). What is the actual distribution of delivered braking velocity across realistic arrival velocities (4–8 km/s) and across the lunar nodal regression cycle (trajectory-plane inclinations from 0 to 30 degrees relative to the Moon's orbital plane)?

**Method.**
- Patched-conic two-body model in `src/waterprop/trajectory/lunar_flyby.py`. Each flyby is treated as an instantaneous velocity rotation in the Moon-centered frame; the in-plane component of the Earth-frame velocity change is realized as braking, multiplied by `cos(inclination)` to account for out-of-plane geometry.
- Three sequential maximum-braking flybys at fixed periapsis altitude. Each subsequent flyby starts from the spacecraft's reduced velocity at infinity.
- Sweep: arrival velocity at infinity 4, 5, 6, 7, 8 km/s; periapsis altitude 100, 500, 1000, 2000, 5000 km; trajectory-Moon inclination 0, 5, 10, 15, 20, 25, 30 degrees.

**Validity caveats.**
- Planar approximation with a scalar inclination penalty `cos(angle)` for out-of-plane misalignment. Real three-dimensional flyby geometry can yield a different penalty curve — the cosine factor is the right qualitative behavior but the magnitude is approximate.
- Earth-Moon trajectory between flybys is not modeled. Real lunar gravity assist tours require careful phasing-orbit design between flybys; mid-course correction propellant cost is captured only as an "MCC budget" line item, not computed here.
- "Maximum braking" assumes the flyby geometry can be oriented optimally each time. Real geometry constraints (arrival declination, available lunar encounter epochs) reduce the achievable per-flyby delta-V from the maximum.
- The model does not include the small terms involving Earth's gravity well at the lunar orbital distance beyond the initial speed boost — fine for the leading-order analysis here.

**Result.** See `results/lunar_gravity_assist_sweep.png` and `results/three_flyby_tour_sweep.csv`.

| Metric | Predicted (H2) | Measured | Held? |
|---|---|---|---|
| Maximum velocity change per flyby at v∞ = 6 km/s, 100 km altitude | 1.5–2.0 km/s | **0.71 km/s** | **falsified-load-bearing** |
| Three-flyby total braking at v∞ = 6 km/s, favorable geometry (inclination = 0) | 2.5–4.0 km/s | **2.33 km/s** | **falsified-conservative** (below the predicted range) |
| Three-flyby total braking at v∞ = 6 km/s, worst geometry (inclination = 30 degrees) | 1.0–2.0 km/s | 1.99 km/s | **held** (just inside the upper end) |
| Mid-course correction budget at worst geometry | 50–300 m/s | not computed in this model | deferred |
| Fraction of arrival epochs that meet the 3 km/s target | 60–85% | **near 0% at v∞ = 6 km/s** — the model gives at most 2.33 km/s even at perfect geometry | **falsified-load-bearing** |

**Aggregate hypothesis H2 status: falsified.** The conops claim of "3 km/s at zero propellant cost from a 3-flyby lunar gravity assist tour" is not supported by the patched-conic model at the published arrival velocity. At v∞ = 6 km/s the maximum achievable braking from 3 flybys is 2.33 km/s, not 3.0 km/s.

**Reading.**

The conops claim was off by approximately 30 percent. Two ways to reconcile:

1. **The arrival velocity at infinity is actually lower than 6 km/s.** At v∞ = 4 km/s, the 3-flyby tour delivers 3.24 km/s (favorable geometry) — matching the conops claim. The conops cites "v∞ ≈ 5.4 km/s" or "~6 km/s" in different places; if the true value is lower (say 4–5 km/s), the claim is approximately correct. **Action: re-check the conops's heliocentric trajectory math; the arrival velocity might be conservatively reported.**

2. **The 3-flyby tour is supplemented with one or more additional flybys, or with a propulsive trim.** With 4 or 5 flybys, the cumulative braking could reach 3 km/s even at v∞ = 6 km/s. The conops mentions "2–3 flybys" — extending to 4–5 is operationally feasible if the timeline allows the additional phasing-orbit time (~27 days per flyby).

The single-flyby velocity change of 0.71 km/s at v∞ = 6 km/s is dramatically below the 1.5–2.0 km/s I predicted because I was using the wrong limit — the formula `2 × v∞ × v_moon / (v∞ + v_moon)` is the limit for a 180-degree turn, which is unreachable at high v∞ (the actual turning angle at 100 km altitude is only ~6 degrees).

**Per-flyby velocity change at v∞ = 6 km/s, periapsis altitude 100 km, by flyby number:**

| Flyby | v∞ in (km/s) | v∞ out (km/s) | delta-v (km/s) |
|---|---|---|---|
| 1 | 6.000 | 5.294 | 0.706 |
| 2 | 5.294 | 4.501 | 0.793 |
| 3 | 4.501 | 3.667 | 0.834 |

Subsequent flybys deliver more delta-v because as v∞ drops, the turning angle grows. This is the favorable compounding the conops anticipates, but it stalls short of 3 km/s.

**Revisit.** Hypothesis H2 was wrong in the load-bearing direction. The conops claim of 3 km/s lunar gravity assist tour does not hold at v∞ = 6 km/s under this patched-conic model. Either the arrival velocity is lower than I assumed, or additional flybys are required. **Risk B01 is confirmed as upward-pressuring — the conops' propulsion budget needs to absorb at least 0.7 km/s of additional propulsive braking at v∞ = 6 km/s, or the trajectory plan needs revision.**

**Cross-learning.**
- **Positive for risk register**: B01 confirmed upward. Risk score stays at 16 (already critical from earlier reweight); now backed by data, not just intuition.
- **Negative for the 4.2 km/s inbound delta-V baseline** used in R0 and all subsequent rounds. If the lunar gravity assist tour delivers 2 km/s instead of 3 km/s at v∞ = 6 km/s, the propulsion system has to absorb an extra 1 km/s. **Inbound chunk-fed delta-V revises from 4.2 km/s to roughly 5.2 km/s.** This propagates back into the chunk-delivery numbers for every candidate technology — they all get worse by a few percentage points.
- **Methodology issue flagged for R-mid (mid-cycle audit)**: re-check whether the conops' inbound v∞ is actually 6 km/s or whether a lower value would resolve the gap. This requires a heliocentric-cruise round, not in the current queue.
- **Methodology issue flagged for R2b (potential retest)**: extend to 4 or 5 flybys, compute timeline penalty, see whether the conops claim recovers with more flybys.
- **Positive for downstream rounds**: the per-flyby compounding is correct in direction — subsequent flybys deliver more delta-v. The model can be trusted to estimate the marginal benefit of additional flybys.
