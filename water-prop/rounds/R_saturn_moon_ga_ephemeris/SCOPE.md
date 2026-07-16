# R-saturn-moon-ga-ephemeris — ephemeris-driven Saturn moon gravity assist modeling

**Status:** scope, pre-study. Authored by Saturn (worker), 2026-05-21 latest.

**Context.** The mission_graph framework gained three desk-study Saturn-moon gravity-assist capture options at Phase 2 (commit `e8f1733` in branch `iceberg-saturn`):

- `titan_gravity_assist_capture` — single moon, ~4 km/s v_inf reduction, 8 month tour
- `rhea_gravity_assist_capture` — single moon, ~1.5 km/s v_inf reduction, 12 month tour
- `cassini_class_multi_moon_tour` — Titan + Rhea + Dione + Tethys + Enceladus + Mimas, ~5.5 km/s, 24 month tour

All three use constant delta-velocity anchors. The actual delta-velocity available from each moon flyby depends on (a) the relative velocity geometry between spacecraft and moon at flyby, (b) the moon's orbital position relative to the spacecraft's incoming trajectory, (c) the flyby altitude (subject to atmosphere or surface), (d) sequencing constraints between flybys. Constant anchors hide all of that.

The locked belief 1a564ee4 references JPL's MALTO/SCOPE (Mission-design and Analysis Low-Thrust Optimization, and Satellite Constellation Operation and Planning Environment) trajectory-optimization toolchain as the industry standard for this trajectory class, and notes it is freely available under NASA tech transfer.

This round answers: **what delta-velocity is actually achievable from a Cassini-class multi-moon tour at Saturn under real ephemerides, and how does that compare to the constant anchors currently in the framework?**

## Out of scope

- Real-time autonomous trajectory replanning. This is an offline analysis.
- Atmospheric corrections (Titan has a substantial atmosphere; flyby altitude is a constraint).
- Multi-vehicle sequencing for a campaign of N icebergs.

## Inputs to acquire

1. JPL Horizons ephemeris data for Titan, Rhea, Dione, Tethys, Enceladus, Mimas across the 2032-2050 demonstrator window. The robotrocketscience website infrastructure already pulls Horizons data; reuse that path.
2. MALTO or an open-source equivalent (poliastro, GMAT, OpenMDAO/CADRE) for the trajectory-optimization step.
3. Saturn-arrival v_inf range to sweep: 3.0 to 6.5 km/s (matches the Phase 2 v_inf precondition gates already in the framework).

## Deliverables

1. A per-arrival-v_inf table of optimized capture-tour delta-velocity available, time-cost, and propellant cost.
2. Updated framework constants — either replace the three constant-delta-velocity anchors or add a fourth option `ephemeris_driven_moon_tour` that calls a precomputed lookup table.
3. A falsification verdict on the existing `cassini_class_multi_moon_tour` anchor: does the 5.5 km/s claim hold under real ephemerides, or is it optimistic?

## Predecessor work

- `e8f1733` (commit on iceberg-saturn) — desk-study constant-delta-velocity options added.
- Locked belief 1a564ee4 — lunar gravity-assist Earth-return pattern that the Saturn analogue extends.
- Cassini real-world tour data — accessible via NASA Planetary Data System.

## Priority

Medium. The constant-delta-velocity anchors are doing useful framework work right now — they show the *shape* of the trade. Refining to ephemeris-driven values is a quantitative correction, not a structural change.
