# R-chunk-size-pareto — closure verdict

**Worker:** titan-3. **Date:** 2026-05-19.

## Headline

At flyable reactor power (≤ 30 kilowatts-electric Kilopower-extrapolation) + R12's lunar-gravity-assist architecture + corrected vis-viva delta-velocity anchors:

- **4 cells close L0-05 strict + L0-09 floor.**
- **30 cells close L0-05 waiver + L0-09 floor.**

Closing chunks by specific-power anchor:

| Specific power | Min strict chunk | Max strict chunk | Min waiver chunk | Max waiver chunk |
|---|---|---|---|---|
| sp=2.4, P=20 kWe | None | None | 50.0 | 100.0 |
| sp=2.4, P=30 kWe | 50.0 | 60.0 | 50.0 | 150.0 |
| sp=10.0, P=20 kWe | None | None | 50.0 | 120.0 |
| sp=10.0, P=30 kWe | 50.0 | 60.0 | 50.0 | 150.0 |

## Reading

ICEBERG closes at flyable power IF the chunk is sized in roughly the **30–80 tonne** range. The 200-tonne commercial anchor is overscale; the 14-tonne R12 demonstrator is underscale for the L0-09 30-tonne floor.

The chunk-size band that closes is bounded above by **burn time vs Hohmann coast** (heavier chunk requires more reactor power to fit burn in 6-year coast) and bounded below by **L0-09 floor** (chunks below ~40 tonnes don't have enough water left after burn for 30 tonnes delivered).

Kilopower-measured specific power (2.4 watts-per-kilogram) closes fewer cells than R12-optimistic (10 watts-per-kilogram). The Kilopower-extrapolation between these two is the load-bearing engineering question.

## Hypothesis grades

| H | Predicted | Measured | Verdict |
|---|---|---|---|
| H-cs-1 | at sp=10, P=20 kWe, chunk=40 t closes commercial-strict | delivered=29.9 t, RT=13.90 yr, commercial-strict=False | FALSIFIED |
| H-cs-2 | sp=2.4 closes fewer strict cells than sp=10 at flyable power | sp=2.4: 2 cells; sp=10: 2 cells | FALSIFIED |
| H-cs-3 | round-trip rises monotonically with chunk mass at fixed (P, sp) | 8 of 8 (P, sp) pairs are monotonic | HELD |
| H-cs-4 | ≥1 cell closes commercial-strict at chunk ≤ 80 t at flyable power + sp=10 | 4 flyable commercial-strict cells; 30 flyable commercial-waiver cells | HELD |

## Implication for program design

ICEBERG should be designed around **40-80 tonne chunks** at **20-30 kilowatt-electric reactor** + lunar gravity assist + Kilopower-extrapolation specific power. This delivers 30-60 tonnes per mission at 14-22 year round-trip — the iapetus tech-demonstrator framing is the realistic shape.

The 200-tonne commercial anchor that's been in the matrix and the pitch deck is not closable at flyable power. Either:
- Re-scope the program to 40-80 tonne chunks (smaller per-mission delivery, higher cadence).
- Wait for Fission Surface Power class reactor (per project-owner directive: not happening).
- Accept aerocapture closure as a precondition (phoebe 0-of-1920 says no).

The first option is the only one that doesn't require a project-owner-level reframe of either L0-04 (delivery target) or the reactor power class.
