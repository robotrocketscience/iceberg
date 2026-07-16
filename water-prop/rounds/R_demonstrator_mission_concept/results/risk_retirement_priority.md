# Risk-retirement priority order

Applying methodology lesson 16 (dominant-kill gate vs highest-leverage gate) to the three engineering bets as the demonstrator sees them.

## Gate classification

| Bet | Baseline readiness | Role | Retirement cost |
|---|---:|---|---|
| #1 chunk capture | 0.53 (mm/s undemonstrated) → 0.69 (demo-confirmed) | **highest-leverage** | low — Earth-orbit proxy is pre-cruise, cheap to iterate |
| #2 water-electrothermal | 0.48 (continuous-months flight-readiness) | **dominant-kill** | high — only the full multi-month Saturn run retires it |
| #3 reactor | 0.015 (delivery by 2035) | external, off critical path | deferred (fly non-nuclear) |

- **Dominant-kill gate = bet #2** (lowest on-path readiness, 0.48). It drives the demonstrator's expected kill probability and is un-retirable except by the mission itself.
- **Highest-leverage gate = bet #1.** Its Earth-orbit catch-and-contain proxy is cheap and pre-cruise, and lifts the A14 joint from 0.53 to 0.69 by retiring 3 of 5 sub-steps before any Saturn commitment.

## Recommended sequence

1. **Bet #1 Earth-orbit catch-and-contain proxy — FIRST.** Cheap, pre-cruise, retires deployment + catch + containment at mm/s. Lifts A14 to ~0.69 *before* the program commits the 12–15-year Saturn cruise. This is the option-value purchase: it converts a 0.254 program-readiness (commit cruise at baseline bet #1) into 0.331.
2. **Bet #2 continuous-months water-thruster run — during the Saturn demonstrator cruise.** The long pole and dominant-kill gate; the demonstrator's RF-ion + bag-filtration stack on chunk water IS the test article. No shortcut exists.
3. **Bet #3 reactor — DEFERRED off the critical path.** Demonstrator flies non-nuclear; reactor retired in a separate mission or by NASA Fission Surface Power, before any commercial-class commitment (L0-24).

## Demonstrator-conditional program-readiness

| Scenario | Joint readiness (bets #1 × #2; bet #3 deferred) |
|---|---:|
| A — commit Saturn cruise at baseline bet #1 (0.53) | **0.254** |
| B — Earth-orbit proxy first, lifting bet #1 to 0.69 | **0.331** |

The demonstrator is a **~1-in-3 shot** (Scenario B) at retiring both on-path bets in a single mission — dominated by bet #2's 0.48. This is honest: a single demonstrator does not make ICEBERG a sure thing; it converts two un-flown bets into ~1-in-3 retired-in-one-shot, with the cheap Earth-orbit proxy as the highest-leverage first move. Sequencing matters precisely because bet #1 is cheaply liftable and bet #2 is not.

## Why this beats the iapetus R7 external gate

| | iapetus R7 tranche-1 | re-gated tranche-1 (this round) |
|---|---|---|
| Gate | Fission-Surface-Power-Phase-2 award (external) | internal demonstrator (bets #1 + #2) |
| Pass probability | 0.023 | ~0.33 (Scenario B) — **~14×** |
| Controllable by ICEBERG? | no | yes |
| Dominant external kill-gate on critical path? | yes (FSP-2) | no (reactor deferred) |

The re-gating spends the tranche-1 budget on an experiment ICEBERG controls, at ~14× the pass probability of the external award, and removes the dominant external kill-gate from the critical path. The expected-loss story in iapetus R7 (E[loss] ≈ $80M because the program kills at the FSP-2 gate >95% of the time) should be recomputed against the internal demonstrator gate; the demonstrator cost-class ($150M–$1.5B, non-nuclear below the reactor-bundled path) is the tranche-1 spend.
