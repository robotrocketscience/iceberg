# R-solar-thermal-hybrid-power — RESULTS

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26. Deterministic; `python3 run.py` reproduces `results/hybrid_power_summary.json`.

## Headline

**The hybrid reactor+solar architecture does NOT move the closed-loop closure verdict, and the invasive location-aware-power framework refactor is NOT justified by closure.** The project owner's insight (dial-up thrust on the sunward approach) is real but addresses a non-binding axis. Two independent reasons:

1. **The dial-up benefit is modest** — the bulk of inbound Δv is burned at Saturn departure (9.5 AU), where a 20-kWe-at-1-AU array delivers 0.22 kW (2.2% of a 10-kWe reactor), and where the vehicle is heaviest. Total inbound burn-time reduction: **10.6% (nominal Δv allocation), 22.7% (even under a generous-to-hybrid allocation)**. Below the 25% the hypothesis pre-set, far below the 40% falsification band.
2. **It does nothing for the binding constraint.** For fixed Δv + Isp, propellant is fixed by Tsiolkovsky and is independent of power; more power buys shorter *burn time*, not less *mass*. The closed-loop Saturn kill (0/150, titan-6) is the **powerplant mass-floor** (a static dry-mass constraint) plus reactor lifetime — neither relieved by an inbound power profile.

**Bonus finding:** the SCOPE's worked example (10 kWe reactor) is *catastrophically underpowered* — the inbound burn alone is **~100–113 years** at 10 kWe (185 t propellant through a ~1 N thruster), ~7× over the L0-05 15-year round-trip ceiling, before any mass-floor or dial-up consideration. The 10-kWe hybrid fails the round-trip axis outright; the dial-up to 30 kW near Earth trims it by 10–23% but cannot rescue a ~7× overage.

## Hypothesis verdicts

| # | Verdict | Basis |
|---|---|---|
| H1 | **HELD for the majority of inbound Δv; precise threshold split** | Solar share of hybrid power: Saturn 2.2%, Jupiter 6.9% (the two bins carrying the majority of Δv: <10%); belt 21.5%, Mars 47.1%, Earth 66.7%. The literal "<10% across all three outer bins" fails at the belt (21.5%), but the load-bearing claim — solar is negligible where most inbound Δv is spent — holds: ~65% of nominal Δv is at <10% solar share. |
| H2 | **HELD** | Inbound burn-time reduction is 10.6% (nominal) and 22.7% (generous-to-hybrid) — both <25%, neither near the 40% falsification band. Modest, because the heaviest, highest-propellant burn (Saturn departure) gets ~no solar. |
| H3 | **HELD** | Hybrid does not change the closed-loop closure verdict. Saturn is 0/150 on the mass-floor + reactor-lifetime axes; the inbound power profile relieves neither (mass floor static; lifetime helped only by the modest burn-time reduction). |
| H4 | **HELD** | The hybrid's genuine value is inner-system / NEA (where solar dominates anyway — this session's NEA round) and conops thrust-authority on final approach, not Saturn closure. |
| **H5 (load-bearing / decision gate)** | **HELD — refactor not justified for closure** | The invasive VehicleState two-field split + per-executor power recompute + new sweep axes is not warranted by the closure verdict. A local `power(r)` function in the inbound burn-time accounting captures the dial-up for round-trip / reactor-hours fidelity and conops, cheaply, without re-plumbing every executor. |

**5/5 held** (H1 with a precise threshold caveat that does not affect the load-bearing reading).

## Framework recommendation (the SCOPE's decision gate)

**Do NOT perform the full invasive location-aware-power refactor for closure's sake.** Recommended instead:
- A documented `power_at(distance_au, reactor_kwe, solar_leo_kwe)` helper (the ~10-line function in this round's `run.py`) used *only* in the inbound burn-time / reactor-hours accounting, where the dial-up actually matters for round-trip and lifetime margin.
- Keep `power_available_kwe` as the closure-gating scalar (set to the reactor floor — the conservative, sun-independent value — which is what the mass-floor and Saturn-departure burn see anyway).
- If a future inner-system / NEA round wants location-aware solar as a first-class sweep axis, that is where the refactor pays off (solar is load-bearing at 1 AU), not in the Saturn tree.

## Notes / caveats

- Δv-by-distance allocation is a transparent modeling choice; the round reports both a nominal (outer-heavy, physically expected for a Saturn-departure spiral) and a generous-to-hybrid (near-sun-heavy) allocation to bound the benefit. The verdict holds across both.
- The ~100-yr absolute burn time at 10 kWe assumes a 60-t dry+payload vehicle and Isp 2000 s; it is illustrative of the power class being wrong, consistent with titan-3's 30-kWe cells needing 14–16 yr cumulative burn (lifetime-falsified) and enceladus-r5's reactor-lifetime finding.
- This round supersedes the lightweight solar-thermal gate (`89a1b82`) conceptually: solar-as-sole-source is rejected at Saturn (correct), and solar-as-hybrid-augmentation is shown non-load-bearing for Saturn closure (this round).
