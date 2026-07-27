# R-solar-thermal-hybrid-power — READING (5-section template)

**Worker:** hyperion (re-spawn 2) · **Date:** 2026-05-26

## Hypotheses adjudicated

H1 **held** (solar negligible where most inbound Δv is spent; precise threshold split at the belt) · H2 **held** (burn-time reduction 10.6% nominal / 22.7% generous, <25%) · H3 **held** (hybrid does not move the closed-loop closure verdict) · H4 **held** (hybrid's home is inner-system/NEA + conops, not Saturn closure) · **H5 (load-bearing) held** (invasive refactor not justified for closure; a local `power(r)` function suffices).

Predicted-vs-measured: the frozen prior — "hybrid addresses a non-binding axis; refactor not justified for closure" — held on all five. The model added one finding the prior did not anticipate: at 10 kWe the inbound burn is ~100 yr, so the SCOPE's worked example fails the round-trip ceiling outright, independent of the dial-up.

## Headline

**The dial-up-thrust insight is real physics but aimed at a non-binding axis.** A hybrid reactor+solar vehicle does get 3× more power on Earth approach than at Saturn departure — but the inbound Δv is dominated by the Saturn-departure spiral at 9.5 AU, where solar contributes 2.2% and the vehicle is heaviest. The total inbound burn-time reduction is 10–23%, and burn time is not the binding constraint: the closed-loop Saturn kill is the powerplant mass-floor (0/150, titan-6), which more inbound power does nothing to relieve because propellant is fixed by Tsiolkovsky, not by power. **The invasive location-aware-power framework refactor is not justified by the closure verdict.**

## Reading (for the project owner)

1. **Don't pay for the full refactor to chase closure.** Making `power_available_kwe` a per-executor location-derived field across VehicleState + Phase 4/5/6 + every gating precondition + two new sweep axes is a large, invasive change. It would not flip a single closed-loop cell, because Saturn dies on static vehicle mass and reactor lifetime, not on inbound thrust authority. Capture the dial-up where it actually matters — the inbound burn-time / round-trip / reactor-hours accounting — with the ~10-line `power(distance, reactor, solar)` helper this round provides, and keep the conservative reactor floor as the closure-gating power.

2. **The hybrid's real home is the inner-system / NEA arm.** This session's NEA round showed solar at ~1 AU is the light-powerplant path that closes the mass loop where Saturn fission can't. A hybrid is just a reactor-heavy point on that spectrum; at the inner system you don't need the reactor at all (NEA closes on pure solar). So the architectural energy behind "hybrid" is better spent on the NEA/inner-system tree, where location-aware solar IS load-bearing — not on rescuing the Saturn inbound leg.

3. **The 10-kWe worked example is underpowered by ~7×.** At 10 kWe the inbound spiral is ~100 yr (vs the 15-yr L0-05 ceiling). This is the same power-class problem titan-3 (30 kWe → 14–16 yr cumulative burn, lifetime-falsified) and enceladus-r5 hit. The hybrid does not change the power-class verdict; if anything it underscores that flyable-power continuous-thrust round-trip from Saturn is the wrong end of the design space.

## Cross-learning

- **Consistent with titan-6 (closed-loop 0/150), titan-3 (30-kWe lifetime), enceladus-r5 (reactor-lifetime):** the Saturn binding constraints are mass + lifetime, and this round confirms a power-profile change does not touch them.
- **Reinforces this session's NEA + K2 rounds:** location-aware solar is load-bearing at the inner system (NEA closes on solar; K2 productizes it), and non-load-bearing for Saturn closure. The "hybrid" idea is the seam between the two arms; it belongs on the NEA side.
- **For the framework / fidelity-refinement round:** adopt the `power(r)` helper in the inbound burn-time accounting only; do NOT add per-executor location-aware power as a closure-gating mechanism. Recorded as a guard against an invasive refactor that wouldn't change a verdict.
- **Methodology note (recurring lesson):** check whether a proposed change touches the *binding* axis before paying for it. Hybrid power is the third architectural proposal this campaign-arc to be real-but-non-load-bearing (cf. depot-waiver relay re-importing the kill; pricing-anchor not on the binding axis). Same discipline each time.

## Revisit

The prediction held cleanly. The reframe worth carrying forward: "hybrid" is not a Saturn rescue and not a distinct architecture — it is a point on the solar↔fission power spectrum, and the campaign's two live arms already bracket it (Saturn = fission, mass-bound; NEA = solar, resource-bound). The dial-up belongs to the NEA/inner-system arm, modeled cheaply, not to an invasive Saturn-tree refactor.

## Deferred / handed-off

- The `power(distance, reactor, solar)` helper (in `run.py`) is ready to drop into the inbound burn-time accounting if the fidelity-refinement round (titan-6 D5 successor) wants round-trip/reactor-hours fidelity. Not wired into the framework here (would be the invasive refactor this round recommends against for closure).
