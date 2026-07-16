# R-dv-anchor-audit — closure verdict

**Worker:** titan-3. **Date:** 2026-05-19 same-day follow-on.
**Predecessor:** R-chemical-electric-leapfrog (`3a97067`).
**Trigger:** user direction "question your assumptions" — audit identified two unverified delta-velocity anchors in the prior round.

---

## Headline

**The R-chemical-electric-leapfrog round's '13 cells close at flyable power' headline is retracted.** Under corrected vis-viva-derived delta-velocity anchors:

- 0 cells close commercial-strict at flyable reactor power (≤ 30 kilowatts-electric).
- 0 cells close commercial-waiver at flyable reactor power.

The two corrections:

1. **Saturn-departure delta-velocity: 5.5 → 7.7 kilometres-per-second.** Vis-viva derivation: Hohmann return v_∞ at Saturn = 6.21 km/s; elliptical parking orbit with B-ring apoapsis (107,000 km from Saturn centre) and Oberth-optimised periapsis (60,000 km, just above clouds); periapsis burn = 36.1 − 28.4 = 7.7 km/s. The prior round's 5.5 km/s anchor was understated by 40%.

2. **Earth-arrival chemical capture delta-velocity: 3.5 → 7.3 kilometres-per-second** (direct from Hohmann v_∞ 10.3 km/s to low Earth orbit) **or 4.2 kilometres-per-second** (after R12 10-flyby lunar gravity assist tour). The prior round's 3.5 km/s anchor was understated by ~2× under both readings.

Combined, the corrected anchors raise the chemical propellant burden by ~38 tonnes (Saturn departure) + 0–32 tonnes (Earth capture, scenario-dependent) on a 220-tonne vehicle. This drops delivered mass by 38–70 tonnes per mission, putting it below the L0-09 30-tonne commercial floor at every flyable cell tested.

---

## Hypothesis verdicts

| H | Predicted | Measured | Verdict |
|---|---|---|---|
| H-anchor-1 | max delivered at flyable+aerocapture under corrected anchors < 30 t | 16.4 t | HELD |
| H-anchor-2 | chemical_direct at flyable power delivered ≤ 0 t (vehicle can't close mass) | max delivered = 0.0 t | HELD |
| H-anchor-3 | lunar_ga + chemical at flyable power max delivered ≤ 5 t | 0.0 t | HELD |
| H-anchor-4 | 0 cells close L0-09 commercial floor at flyable power under corrected anchors | 0 cells close floor at flyable power | HELD |

---

## Reading

**The leapfrog architecture at commercial chunk scale (200 tonnes) doesn't close L0-09 commercial floor at flyable Kilopower-extrapolation reactor power under corrected delta-velocity anchors.** This was hidden by the prior round's understated Saturn-departure anchor. The corrected reading aligns with what the campaign has been saying all session — commercial-scale ICEBERG inbound delivery is empty at flyable power — but my prior leapfrog round had erroneously suggested otherwise.

**Aerocapture closure remains the load-bearing question, but is no longer sufficient by itself.** Even with Earth aerocapture working perfectly (zero propulsive capture), the Saturn-departure burn alone consumes 182 tonnes of the 200-tonne chunk, leaving only ~15 tonnes delivered. Below floor.

**The lunar gravity assist scenario (R12 architecture) is also empty at commercial scale under corrected anchors.** Even with 5.83 kilometres-per-second of v_∞ shed via 10 flybys, the residual 4.2 kilometres-per-second chemical capture burn on top of the corrected 7.7-kilometre-per-second Saturn departure still over-spends the chunk's propellant budget.

**R12's 13.91-year / 70%-delivery closing cell survives in this round's terms ONLY because R12 was sized for a 14-tonne chunk, not 200 tonnes.** At demonstrator scale, the corrected anchors don't change the verdict materially because the propellant requirements scale linearly with chunk mass but the relative delivered fraction is preserved.

---

## Methodology lesson — candidate lesson 20

**Vis-viva-default anchoring.** When a delta-velocity value is used as an architecture-defining anchor without a primary-text citation, default to deriving it from vis-viva at the relevant orbital geometry. The R-chemical-electric-leapfrog round used Saturn-departure 5.5 km/s and Earth-capture 3.5 km/s as informal-sketch values; both were wrong by 30–100% in the conservative direction (less Δv than reality). A 5-minute vis-viva re-derivation would have caught both errors before the round committed.

This is closely related to lesson 9 (anchor-on-PRIMARY-text) — the difference is that lesson 9 applies when the prior round's text exists; lesson 20 applies when the anchor has no primary source at all and must be derived from physics. Both reduce to the same discipline: **don't use numbers that aren't sourced or derived.**

---

## What this changes about the session's conclusions

1. **R-chemical-electric-leapfrog headline retracted.** The 33–42 tonnes delivered figure is artefact of understated Saturn-departure anchor. Real delivered mass at flyable power and commercial chunk is below floor.

2. **R12 lunar-gravity-assist verdict is now load-bearing for demonstrator-scale only.** At commercial scale (200-tonne chunk), even the lunar gravity assist tour doesn't rescue the architecture under corrected anchors.

3. **Minimum reactor power for commercial closure with lunar gravity assist + corrected anchors:** see Pareto closure table. Probably well into Fission Surface Power class.

4. **The campaign-wide reading converges:** at flyable reactor power, ICEBERG closes only at demonstrator scale. iapetus's staged-options framing is the correct program-level reading. The matrix's 'commercial cell exists at heritage anchor' rows need retraction.

5. **The session's earlier 'leapfrog is the architecture' reading should be downgraded** to 'leapfrog is a real architectural option that improves the math but doesn't close commercial scale at flyable power; its primary value is making the demonstrator cell more defensible.'

---

## Critical follow-on

- **R-chunk-size-pareto-flyable-power** — at flyable Kilopower-extrapolation (≤ 30 kilowatts-electric) and corrected delta-velocity anchors, what chunk mass closes both L0-05 strict + L0-09 floor? Probably ~80–120 tonnes (between R12 demonstrator and commercial floor). If yes, that becomes the realistic commercial scale and L0-09 should be re-examined.
- **R-cruise-time-vs-trans-Saturn-injection-pareto** — faster cruise (higher trans-Saturn-injection delta-velocity at launch) shortens round-trip at the cost of more launch-vehicle propellant. Could shift the L0-05 strict envelope.
- **R-saturn-aerocapture-feasibility** — Saturn arrival via aerocapture was assumed; needs its own physics check.
- **R-saturn-departure-from-titan-orbit** — if chunk acquisition occurs in a more distant Saturn-system parking orbit (e.g., at Titan's altitude), Saturn-departure delta-velocity drops to ~4 km/s. Tradeoff round.
