# Saturn ICEBERG Ship — Subsystem Specification

**Status:** working draft. Numbers are bottom-up estimates from published heritage components, sanity-checked against the ICEBERG conops top-line anchors (~5 t dry vehicle at Saturn arrival, ~45 t pre-Trans-Saturn-Injection). This document is the input to Basilisk vehicle definition and to any subsequent mass-budget-corrected R&D rounds.

**Reference architecture (post-R10):**
- Propulsion: water radio-frequency ion (Pale Blue class), 2000 s specific impulse, electrical-to-jet efficiency 0.65
- Power: NASA Kilopower 10 kWe, Stirling power conversion, 5 W/kg specific power (mid-band per R1)
- Propellant: Earth-launched water on outbound + Saturn-side burns; chunk-fed water on inbound (after grapple)
- Capture: trawl bag with hot/cold-side sublimation distillation feed (per conops + R11)
- Trajectory: Hohmann or slow-Hohmann variant (R9 pending); chunk-fed inbound delta-velocity 2.85–5.94 km/s (R8 Case C–B)

**Mission anchors:**
- Trans-Saturn-Injection: 7.3 km/s, chemical kick stage (bought, jettisoned)
- Saturn capture: 0.6 km/s, Earth-water-fed via water radio-frequency ion
- Saturn ring rendezvous: 1.49 km/s, Earth-water-fed
- Saturn egress (post-grapple): ~2.09 km/s, chunk-fed
- Inbound cruise braking: residual after lunar gravity assist
- Earth-arrival trim: ~0.1 km/s, water-reaction-control-system

---

## Mass budget

Mass at Saturn arrival (post-chemical-kick-stage jettison, pre-grapple). Sources noted; heritage components prefer published numbers from comparable flown hardware.

| Subsystem | Subcomponent | Mass (kg) | Source / sizing note |
|---|---|---:|---|
| **Reactor + power** | NASA Kilopower 10 kWe core | 400 | NASA Glenn KRUSTY publications |
|  | Stirling power conversion (4 × 2.5 kWe) | 200 | Kilopower technology demonstrator unit reference |
|  | Heat rejection radiator (~50 m² at 10 kg/m²) | 500 | Kilopower 1 kWe scales linearly |
|  | Shadow shield (partial, for chunk-water assist) | 350 | Reduced from full Kilopower shield because chunk water provides bulk shielding inbound |
|  | Power management + distribution | 150 | RTG / radioisotope-power-system heritage |
|  | **Subtotal reactor + power** | **1600** |  |
| **Propulsion** | 4 × Pale Blue radio-frequency ion thruster (15 kg each, redundant pairs) | 60 | Pale Blue published thruster mass |
|  | Power Processing Unit (2 × redundant) | 80 | NASA Solar Electric Propulsion heritage scaling |
|  | Earth-water tank (3-axis composite, 5 m³ at 10 kg/m³ structural) | 80 | Standard composite tank scaling |
|  | Plumbing, valves, vaporizer | 40 | Pale Blue feed system reference |
|  | **Subtotal propulsion** | **260** |  |
| **Bag system** | Vectran bag fabric (4-m bag, 30 m² shell at 0.5 kg/m²) | 30 | Bag-engineering doc Vectran heritage |
|  | Aerogel intake (for soft capture) | 50 | Stardust mission scaling |
|  | Hot-wall heaters + cold-wall radiator integration | 100 | Heat-pipe + multilayer-insulation network |
|  | Harvest port + secondary mesh filter (R11) | 30 | 14 kg filter + harvest plumbing |
|  | Bag-deployment mechanism (boom + grapple) | 70 | R18 power-law scaling, conops-baseline |
|  | **Subtotal bag system** | **280** |  |
| **Avionics + Guidance/Navigation/Control** | Rad-hard CPU (RAD750 or RAD5500) | 10 | Cassini, Mars Reconnaissance Orbiter heritage |
|  | Inertial Measurement Unit (3-axis, redundant) | 8 | Standard small-spacecraft |
|  | Star trackers (2 × redundant) | 10 | Standard |
|  | Reaction wheels (4 × 10 kg) | 40 | 4-wheel pyramidal redundancy |
|  | **Subtotal avionics + Guidance/Navigation/Control** | **68** |  |
| **Sensors (rendezvous + proximity operations)** | Radar (millimeter-wave) | 15 | commercial-tug heritage |
|  | Lidar (3-axis scanning) | 10 | Standard rendezvous suite |
|  | Stereo cameras + processing | 8 | OSIRIS-REx asteroid-rendezvous heritage |
|  | Particle / dust sensor (for B-ring composition) | 5 | Cassini Cosmic Dust Analyzer scaling |
|  | **Subtotal sensors** | **38** |  |
| **Communications** | High-gain antenna (3 m dish, deployable) | 35 | Cassini / Juno heritage |
|  | X-band + Ka-band transponder | 15 | Deep Space Network compatible |
|  | Solid-state amplifier | 10 | Standard |
|  | Low-gain antennas (2 × omni) | 5 | Backup link |
|  | **Subtotal communications** | **65** |  |
| **Reaction Control System** | 12 × water-vapor cold-gas thrusters | 20 | commercial-tug heritage design (R36 Option A reference) |
|  | Vaporizer + valves | 15 | R36 reference |
|  | Cold-gas water tank (50 kg reserve) | 8 | Small dedicated tank |
|  | **Subtotal Reaction Control System** | **43** |  |
| **Thermal management** | Radiators (beyond reactor) | 25 | Avionics + electronics thermal |
|  | Heat pipes + multilayer insulation | 20 | Standard practice |
|  | **Subtotal thermal** | **45** |  |
| **Power storage** | LiFePO₄ battery (5 kWh for startup + safe mode) | 35 | Modern Lithium-Iron-Phosphate cell heritage |
| **Harness** | Wiring + connectors (~6% of dry mass) | 160 | Standard Mission Analysis and Design handbook fraction |
| **Structure** | Chassis + booms + brackets (~12% of dry mass) | 320 | Standard Mission Analysis and Design §18 lower-bound |
| **Subtotal before margin** |  | **2914** |  |
| **Margin (20% at concept design phase)** |  | **583** | Standard concept-phase reserve |
| **Total spacecraft dry mass** |  | **3497 kg ≈ 3.5 t** |  |

**Cross-check vs conops:** conops cites ~5 t dry vehicle at Saturn arrival. The bottom-up here gives ~3.5 t. **The conops's 5 t was a top-down estimate; this bottom-up is ~30% lighter.** Possible reasons:
- I used 10 kWe Kilopower; if the design actually wants 20 kWe (faster cruise), reactor mass roughly doubles, adding ~1.5 t. That would bring the total to ~5 t — consistent with the conops being sized for a higher-power reactor than R6 recommended.
- I sized the bag at 4 m / 30 m² shell; if the bag is significantly larger (per the trawl-bag scaling for a swept-volume collection), the bag mass grows substantially.
- The shadow shield could be heavier in a non-chunk-assist scenario.

This delta is itself a finding for a follow-up sanity round.

---

## Wet mass roll-up (at Trans-Saturn-Injection)

| Phase | Mass component | Mass (kg) |
|---:|---|---:|
| Saturn-arrival state | Spacecraft dry | 3500 |
|  | Earth-water reserve (for capture + rendezvous + outbound trim + margin) | 8500 |
|  | **Saturn-arrival wet mass** | **12,000** |
| Outbound coast cumulative water consumed | Trim burns (Earth-water-fed radio-frequency ion) | ~500 |
| Pre-coast (post-Trans-Saturn-Injection) wet mass | (3500 + 8500 + 500) | 12,500 |
| Chemical kick stage | Centaur V class dry | ~2000 |
|  | Centaur V class propellant for 7.3 km/s Trans-Saturn-Injection | ~30,000 |
|  | **Kick stage subtotal** | **32,000** |
| **Pre-Trans-Saturn-Injection wet mass at low-Earth-orbit** |  | **~44,500 kg ≈ 45 t** |

**Cross-check:** matches conops's 45 t pre-Trans-Saturn-Injection within rounding. Within Falcon Heavy expendable capability (64 t to low-Earth-orbit). Within Starship capability (>100 t). **Architecture closes on launch mass.**

---

## Inbound mass closure (post-grapple)

| Quantity | Value |
|---|---:|
| Spacecraft dry | 3500 kg |
| Earth-water remaining at Saturn departure (post capture + rendezvous-in) | ~6500 kg |
| Grappled chunk | 14,000 kg |
| **Inbound initial mass** | **24,000 kg** |
| Chunk-fed inbound delta-velocity (R8 Case B) | 5.94 km/s |
| Water radio-frequency ion exhaust velocity (2000 s × 9.81) | 19,620 m/s |
| Tsiolkovsky propellant fraction | 0.262 |
| Propellant required | 6280 kg |
| **Delivered to low-Earth-orbit (post-burn)** | **17,720 kg** |
| Delivered chunk (chunk minus what's burned, assuming Earth-water reserve is consumed first) | **~11,000 kg = 78.6% of chunk** |
| Delivered chunk if Earth-water reserve is preserved as ballast | **7720 kg = 55.1% of chunk** |

**Note on the bookkeeping:** the inbound burn consumes propellant from somewhere. If the spacecraft draws first from the remaining Earth-water reserve (6.5 t) and then from the chunk, the chunk is preserved as long as possible — yielding ~78.6% delivery. If the spacecraft burns chunk water only and preserves Earth-water as reserve for Earth-arrival trim, the chunk delivery drops to ~55%. The conops's 75% headline is consistent with the first bookkeeping (Earth-water reserve burned first).

This is a real architectural choice. **The natural choice is to burn Earth-launched water first, since it's "free" mass already at Saturn — but that requires the radio-frequency ion thrusters to switch propellant source seamlessly mid-cruise.** Pale Blue's water thrusters can do this; the choice is at the bag harvest plumbing.

---

## Power budget (steady-state cruise, post-grapple)

| Subsystem | Steady-state (W) | Peak (W) | Notes |
|---|---:|---:|---|
| Propulsion (1 × Pale Blue at 70% throttle) | 7000 | 10,000 | Single thruster nominal; second on standby |
| Avionics + Guidance/Navigation/Control | 80 | 200 | Higher during burn or maneuver |
| Sensors (mostly off during cruise) | 20 | 100 | Lidar + camera during ring approach |
| Communications (downlink at apogee passes) | 50 | 200 | High-gain antenna + amplifier |
| Reaction Control System (off during cruise) | 5 | 50 | Vaporizer pre-heat only |
| Thermal control (heaters) | 100 | 300 | Cold-side bag heaters |
| Bag heaters (sublimation control) | 1500 | 2500 | Maintains hot-wall temperature gradient |
| Battery charging | 200 | 500 | Idle during steady cruise |
| Total | **8955 W** | **13,850 W** | Within 10 kWe Kilopower with margin |

**Sanity:** Kilopower 10 kWe Beginning-of-Life provides 10,000 W; End-of-Life after 14 years estimated at 8000–9000 W. The steady-state budget at 9 kW leaves 1 kW margin Beginning-of-Life and goes negative End-of-Life. **This is tight.** Either reactor specific power should be re-validated, or the bag heaters or propulsion throttle need to give. Flagged as a finding for R5 follow-on.

---

## Basilisk integration notes

For Basilisk vehicle definition, this document provides:

1. **Mass properties:** total dry mass 3500 kg. Center-of-Mass location and inertia tensor to be computed once the layout drawing exists (not in this revision).
2. **Thruster definitions:** 4 × Pale Blue radio-frequency ion at fixed mounting locations on the aft end, plus 12 × Reaction Control System water-vapor cold-gas thrusters at corners of the spacecraft envelope. Each thruster needs `Force_N`, `Isp_s`, `mountingLocation_m`, `mountingDirection_unitvec`, and `minOnTime_s`. Numbers above provide F and Isp; geometry needs the layout drawing.
3. **Sensor models:** RPO sensor suite (radar + lidar + cameras). Each needs `field_of_view_deg`, `range_m`, `update_rate_Hz`, `noise_model`. Listed but not parameterized here.
4. **Power model:** time-varying power available (Kilopower Beginning-of-Life 10 kW → End-of-Life ~8 kW). Battery 5 kWh buffer.
5. **Environmental:** for the cruise portion, heliocentric 2-body; for Saturn-system, n-body with Saturn + ring moons; for Earth approach, n-body with Earth + Moon (per R2's lunar-flyby model).
6. **Guidance modes** (to define separately):
   - Trans-Saturn-Injection coast
   - Saturn approach + capture (multi-pass spiral)
   - Saturn ring rendezvous + phasing
   - Ring station-keeping + chunk identification
   - Soft capture (trawl-bag inflation + drift)
   - Saturn-system egress (multi-pass spiral)
   - Heliocentric inbound cruise + braking
   - Lunar gravity assist tour
   - Earth-arrival trim + depot delivery

---

## Open questions surfaced by the spec

1. **Reactor power level.** 10 kWe leaves no margin on the steady-state load. Either bag heaters are over-sized in my estimate, or 15–20 kWe is the real requirement. Pulls reactor mass up ~50–100%.
2. **Earth-water reserve at Saturn arrival.** I assumed 8.5 t Earth-water on top of 3.5 t dry → 12 t at Saturn arrival. Conops anchors to 5 t dry vehicle at Saturn arrival but doesn't separately call out the water reserve. Different decomposition.
3. **Chunk-fed vs Earth-water-reserve burn priority.** This is a bookkeeping choice that changes the 75% headline into 55% or vice versa. Architectural decision.
4. **Bag mass.** I sized at 280 kg total (Vectran + aerogel + thermal + mechanism). The bag-engineering doc may have a different number — worth cross-checking.
5. **Radiation shielding sizing.** I assumed chunk-water bulk assist on the inbound leg, so only a partial reactor shadow shield. On the outbound leg (no chunk), this is more exposed; reactor shielding may need to be heavier.
6. **Communications power budget at Saturn.** 50 W steady-state may be optimistic at 9.5 Astronomical Units; Cassini drew up to 80 W on the downlink. Bump to 80 W and the steady-state load grows.

---

## What this document is NOT

- Not a flight-design document. Mass-precision is ±20% at concept-design phase.
- Not yet a Basilisk input file. It enumerates what Basilisk would need but doesn't produce the parameter file.
- Not validated against detailed thermal, structural, or radiation analysis. Those are subsystem deep-dives.
- Not the Flight 1 demonstrator. That's a separate spec (Earth-launched propellant, no reactor, ESPA-Grande mass class).

---

*Working draft 2026-05-14. Revisions tied to R5/R9/R11 follow-ons and to Basilisk integration progress.*
