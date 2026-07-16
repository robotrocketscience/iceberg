# R-saturn-shadow-and-station-location

**Owner session:** enceladus-r5 (resumed 2026-05-15)
**Branch:** iceberg-enceladus-r5
**Status:** PRE-REGISTERED (hypothesis frozen before run)
**Builds on:** R-saturn-side-solar-thermal (round 1, commit `0fcab42`)

---

## Motivation

Round 1 modeled Saturn shadow as a flat 1.5× duty-cycle bump on collection area. That was a hack. The real shadow fraction depends on where the Saturn-side electrolysis station sits, and whether it carries thermal storage to bridge dark periods.

Four candidate station locations from prior enceladus-r5 conops:

1. **Saturn-Sun L1 halo orbit** — continuous sunlight, no Saturn shadow, no diurnal cycle. Station-keeping non-trivial.
2. **High Saturn orbit (semi-major-axis comparable to a Galilean-class moon)** — Saturn shadow is a small fraction of each orbit because Saturn's apparent angular radius from such a distance is small.
3. **Titan surface** — Titan is tidally locked to Saturn (orbital period 15.95 days = Titan rotational day). Solar day-night cycle is ~8 days light, ~8 days dark.
4. **Enceladus surface** — Enceladus also tidally locked, orbital period 1.37 days. Solar day-night cycle is ~16.4 hours light, ~16.4 hours dark.

If round-1's "competitive" optimistic case (101 kilograms-per-kilowatt) was duty-cycle 1.0 (Saturn-Sun L1, continuous sunlight), real moon-surface stations face duty-cycle factors of 2.0× plus thermal-storage mass penalties spanning multi-hour-to-multi-day dark periods. The reframed verdict from round 1 ("solar-thermal and Fission-Surface-Power-stretch occupy the same credibility band") only holds at the Saturn-Sun-L1 endpoint, which is conops-implausible for a station that also has to receive bag-captured chunks from Saturn's rings.

The fission alternative has no equivalent duty-cycle penalty — reactors run continuously regardless of solar position.

## Hypothesis (H-saturn-shadow)

**Pre-registered numeric prediction.**

For a 200-kilowatt-electric-equivalent useful electrolysis target, compute the effective kilograms-per-kilowatt for each station location using the round-1 optimistic stack (solid-oxide-electrolyzer, mirror areal density 0.1 kilograms-per-square-meter, optical efficiency 0.80), adjusted for:

- Shadow fraction $f_\text{dark}$ specific to that location.
- Thermal-storage mass to bridge the longest continuous dark period, at a storage specific energy 100 watt-hours-per-kilogram (latent-heat phase-change material, conservative — laboratory salts achieve 200–400 watt-hours-per-kilogram; flight heritage limited).
- Collection-area scaling: $A \cdot \text{collection} = A_\text{base} / (1 - f_\text{dark})$ to deliver the time-averaged target, assuming the stored thermal energy is recharged during sunlit periods.

**Predicted ranges (pre-registered):**

| Station location | f_dark | Longest dark period | Storage mass at 200 kW (tonnes) | Predicted total kg/kW |
|---|---|---|---|---|
| Saturn-Sun L1 halo | 0.0 | 0 (no shadow) | 0 | 101 (round 1 result, unchanged) |
| High Saturn orbit (Iapetus-class semi-major-axis) | 0.01–0.03 | minutes (orbital geometry) | small (≤ 2) | 105–115 |
| Titan surface | 0.50 | ~8 days = 192 hours | 200 kW × 192 h / 0.1 kWh/kg = 384 tonnes | 2000–2200 (dominated by storage) |
| Enceladus surface | 0.50 | ~16.4 hours | 200 × 16.4 / 0.1 = 33 tonnes | 250–300 |

**Falsification rule (pre-registered):**

The hypothesis "solar-thermal is competitive with Fission-Surface-Power-stretch at any conops-plausible Saturn-side station location" is **upheld** if and only if at least one station location with a credible conops case (i.e. not just Saturn-Sun L1 in isolation, but one compatible with receiving bag-captured chunks) yields total kilograms-per-kilowatt < 200 (i.e. better than Fission-Surface-Power Phase 1 contracted baseline).

The hypothesis is **falsified** if every conops-plausible station location yields > 416 kilograms-per-kilowatt (worse than Kilowatt-Reactor-Using-Stirling-Technology demonstrated).

If the "conops-plausible" set excludes Saturn-Sun L1 (chunks have to be captured from Saturn ring-system, not from L1), then the falsification rule reduces to whether Enceladus surface, Titan surface, or high Saturn orbit closes.

## Conops cross-check on station location

Prior enceladus-r5 STATE.md and the ICEBERG-conops shared doc do not pin the station location. Inferable constraints:

- Station receives bag-captured chunks from Saturn's rings. Inbound chunks need a stable, accessible delivery point. Saturn-Sun L1 is at ~63 Saturn radii from Saturn; chunks must traverse this distance to reach the station, adding delta-velocity cost.
- Saturn rings sit at 1.3–2.3 Saturn radii (the main rings). A station in low-equatorial Saturn orbit (semi-major-axis 2–5 Saturn radii) is nearest to ring delivery but has the worst shadow fraction.
- Titan and Enceladus surfaces are on tidally-locked moons; chunks arrive on hyperbolic trajectories relative to the moon, requiring large delta-velocity to land.
- Best conops compromise: a station in a high-eccentricity Saturn orbit with periapsis at the rings (for delivery) and apoapsis far enough out to be in shadow only briefly. This is similar to a Molniya orbit and has duty-cycle ~0.95+.

The conops-plausible set therefore includes:
- High eccentric Saturn orbit (low duty-cycle penalty).
- Titan or Enceladus surface (high duty-cycle penalty).
- Saturn-Sun L1 (low duty-cycle penalty but chunk-delivery cost not yet quantified).

## Test

`run.py` computes total mass for the round-1 optimistic stack at each candidate station location, plus the thermal-storage penalty for bridging dark periods. Outputs kilograms-per-kilowatt for each location and classifies against fission benchmarks.

## Result

Five candidate station locations evaluated at 200 kilowatts-electric useful target, round-1 optimistic stack (solid-oxide-electrolyzer, mirror areal density 0.1 kilograms-per-square-meter), thermal storage at 100 watt-hours-per-kilogram:

| Station | Shadow fraction | Longest dark (h) | Storage (tonnes) | Total (tonnes) | kg/kW | Fission comparison |
|---|---|---|---|---|---|---|
| Saturn-Sun L1 halo | 0.00 | 0 | 0.0 | 20.3 | 101 | beats Fission-Surface-Power Phase 1 baseline |
| High eccentric Saturn orbit | 0.03 | 4.0 | 8.0 | 28.5 | 142 | beats Fission-Surface-Power Phase 1 baseline |
| Low equatorial Saturn orbit | 0.40 | 2.5 | 5.0 | 30.0 | 150 | beats Fission-Surface-Power Phase 1 baseline |
| Enceladus surface | 0.50 | 16.4 | 32.8 | 60.2 | 301 | beats Kilowatt-Reactor-Using-Stirling-Technology demonstrated |
| Titan surface | 0.50 | 192.0 | 384.0 | 411.4 | 2057 | worse than Kilowatt-Reactor-Using-Stirling-Technology |

## Reading

**Storage dominates only when the longest dark period is multi-day.** Titan's 192-hour shadow eats 384 tonnes of phase-change material — by itself ~19× the round-1 stack mass. Even at the literature upper bound of 400 watt-hours-per-kilogram for salt-eutectic latent-heat storage (no flight heritage), Titan would still need 96 tonnes of storage, dominating the deployed mass. Titan-surface solar-thermal is structurally non-viable.

**Enceladus surface is borderline.** 16.4-hour dark period demands 33 tonnes of storage. Total 60 tonnes, 301 kg/kW. Better than Kilowatt-Reactor-Using-Stirling-Technology demonstrated (416 kg/kW) but worse than Fission-Surface-Power Phase 1 contracted baseline (200 kg/kW). Marginal; sensitive to storage specific energy and conops details (could a Saturn-side station accept a 16-hour batch-mode electrolysis duty cycle and skip storage entirely? Probably yes — that's the right round-3 question).

**Orbit-based stations preserve round-1's optimistic verdict.** High-eccentric Saturn orbit (periapsis at the rings for chunk delivery, apoapsis far enough out that Saturn shadow is brief) lands at 142 kg/kW — still beating Fission-Surface-Power Phase 1 contracted baseline (200 kg/kW), still in the same credibility band as Fission-Surface-Power stretch (100 kg/kW). Low equatorial Saturn orbit, despite 40 percent shadow fraction, lands at 150 kg/kW because each shadow interval is short (~2.5 hours) and storage is cheap.

**Round-1 reframed verdict survives, conditional on conops choice.** *"Saturn-side-Technology-Readiness-Level-bet-limited, solar-thermal and Fission-Surface-Power-stretch in same credibility band"* survives at orbit-based stations. It fails at moon-surface stations. The architecture matrix must therefore qualify the solar-thermal cell with a station-location precondition: only viable in Saturn orbit, not on a moon surface. Note that this is the opposite preference from a fission reactor, which a moon-surface site would otherwise prefer (gravity-aided thermal management, no station-keeping cost).

**The conops-plausible set then is high-eccentric Saturn orbit.** Most ring-system-accessible, lowest shadow penalty, doesn't depend on a moon-landing capability. This is also where most prior ICEBERG conops sketches placed the chunk-processing depot. The verdict is therefore not just abstractly preserved — it pins solar-thermal viability to the same orbital regime that the existing conops already favors.

## Revisit

**Pre-registered prediction vs measured:**

| Station | Predicted kg/kW | Measured kg/kW | Held? |
|---|---|---|---|
| Saturn-Sun L1 halo | 101 (round 1 unchanged) | 101 | held |
| High eccentric Saturn orbit | 105–115 | 142 | **partial — 24% above upper bound; storage at 4 h dark was 8 t, not 2 t as I'd anchored** |
| Titan surface | 2000–2200 | 2057 | held |
| Enceladus surface | 250–300 | 301 | held at edge |

**The miss on high-eccentric Saturn orbit.** I anchored on the round-1 mass breakdown without explicitly computing storage = 200 kW × 4 h / 0.1 kWh/kg = 8000 kg. The 2-tonne upper bound in my pre-reg was wrong by 4×. The error is the same recurring-lesson-#7 failure-mode as round 1: anchoring on one regime, extrapolating mentally without arithmetic. Lesson is reinforced.

**Falsification verdict.** Hypothesis was "solar-thermal is competitive with Fission-Surface-Power stretch at some conops-plausible station." Verdict: **upheld** for orbit-based stations (high-eccentric or low equatorial Saturn orbit, both < 200 kg/kW). **Falsified** for Titan surface. **Marginal** for Enceladus surface.

## Cross-learning

**Backward references:**

- **R-saturn-side-solar-thermal (round 1, commit `0fcab42`):** the reframed verdict ("Saturn-side-Technology-Readiness-Level-bet-limited, both paths same credibility band") survives this round's stress test for orbit-based stations. It does NOT survive for moon-surface stations. The verdict therefore needs a conops conditional: *valid if Saturn-orbit station; invalid if moon-surface station*. This makes solar-thermal an orbit-locked architecture, not a free choice.
- **R-non-fission-baseline (round 1 of enceladus-r5, commit `85a5aac`):** the all-chemical Architecture B's "hidden-infeasible on Saturn-side power" verdict can now be qualified: hidden-infeasible IF moon-surface station, but viable in same credibility band as Fission-Surface-Power-stretch if station is in Saturn orbit. Whether Architecture B's conops compatibility with a Saturn-orbit station has been checked is a separate question — most prior chemistry-centric conops assumed Titan-surface electrolysis.
- **R-chemical-plus-small-reactor (round 2 of enceladus-r5, commit `1d48cb2`):** Architecture D's Saturn-side reactor option preserves moon-surface conops if needed. Solar-thermal does not. Architecture D may therefore unbundle into two sub-options: D-fission-moon-surface vs D-solar-thermal-Saturn-orbit. Different conops, different risk profiles, same posterior band.

**Forward references / spawned threads:**

- **R-batch-mode-electrolysis-feasibility:** can Saturn-side electrolysis run in a batch cycle that accepts dark-period idleness rather than buffering thermal energy? At Enceladus surface, a 16-hour-on / 16-hour-off cycle eliminates the 33-tonne storage. The deliverable then becomes oxidizer-and-fuel storage to bridge propellant demand from a 50-percent-duty-cycle production line. Could halve Enceladus-surface kg/kW to ~150.
- **R-solar-thermal-station-keeping-cost:** high-eccentric Saturn orbit and Saturn-Sun L1 both demand propellant for station-keeping or precision pointing. For a 30,000-square-meter solar concentrator the cross-section is enormous; solar radiation pressure (already weak at Saturn) plus atmospheric drag in low orbit are negligible, but Saturn-orbit perturbations and pointing-jitter station-keeping are non-trivial. What's the mass penalty per kilowatt-electric-equivalent?
- **R-chunk-delivery-from-Saturn-Sun-L1:** if Saturn-Sun L1 is the preferred station (zero shadow, zero perturbations), what's the delta-velocity penalty for delivering bag-captured ring chunks from Saturn to L1 (~63 Saturn radii)? This was deferred in round 1's discussion and could swap which station wins.
- **Matrix update (orchestrator):** when adding solar-thermal as a Saturn-side power sub-option for Architecture D, condition it on station location: viable at Saturn-orbit station (142–150 kg/kW), marginal at Enceladus surface (301 kg/kW), inviable at Titan surface (2057 kg/kW). Fission-Surface-Power reactor cell remains viable across all four locations. The cleanest reframe is two architecture-D variants — D-fission (location-agnostic) and D-solar-thermal (Saturn-orbit-only) — with the same conditional Bayesian cascade but a different station-location precondition.

**Methodology note for future rounds:** when pre-registering numeric ranges that fold a multi-component sum (here: round-1 stack + storage), compute each component before freezing the range. The 4-tonne-vs-8-tonne high-eccentric-orbit miss was identical in failure mode to round 1's Stirling regime miss. Both rounds, same lesson: pre-registering without computing components numerically reproduces recurring-lesson-#7. Add to the protocol: pre-registration of a parameter sweep must include component-level arithmetic for at least one representative cell per regime before freezing ranges.

