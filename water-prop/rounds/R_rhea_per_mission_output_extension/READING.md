# READING — rhea per-mission output extension

## Load-bearing reading

**The het-cadence program-NPV-positive verdict is price-risk-driven, not concentration-driven. The answer to decision #13's question — "does the program-NPV-positive verdict rest on a single windfall mission?" — is no.** Within each simulated program the missions are near-identical, and NPV sign is a deterministic function of the exogenous clearing-price draw crossing a fixed breakeven (~$6.3k/kg heterogeneous, ~$5.5k/kg homogeneous). There is no windfall mission, in either cadence; the 46.26% / 50.83% NPV-positive figures are simply `P(sampled clearing price > breakeven)`. Hamiltonian Layer 1 confirms this by **ruling out** momentum-concentration: only 14% of trajectories are MOMENTUM-DEPENDENT, and 41 of 51 NPV-negative programs are pure monotonic decline.

This is the converse of the hypothesis the round was built to test (H6: het is concentration-driven). H6 is falsified, and the falsification is the finding.

## Three findings

1. **Het loses to hom by raising the breakeven price, not by concentrating revenue.** het's breakeven (~$6.3k/kg) sits ~$0.5–1.5k/kg above hom's (~$5.5k/kg) because mission 1 delivers 20 t instead of 80 t — less early revenue for comparable early cost. This is a steady structural drag visible as a price shift, fully consistent with rhea's existing R-heterogeneous-cadence verdict that chunk-shrinking loses NPV in every regime. The new evidence is the *mechanism*: it is a breakeven-price penalty, not a momentum/variance effect. The cadence choice does not change the *character* of the program's risk (both are pure price risk); it only moves the price at which the program clears.

2. **The iapetus tranche-1 expected-loss anchor ($80M) is robust to this decomposition.** The accumulation-vs-momentum lens does not reveal a hidden concentration fragility that the clearing-price Monte Carlo failed to capture. The program's NPV variance is already the clearing-price variance the MC samples; there is no additional within-program momentum risk to add. So the $80M expected-loss number is not secretly propped up by — nor secretly threatened by — a windfall-mission assumption. (This is a *non*-revision: the anchor stands as-is.)

3. **Hamiltonian Layer 1 has limited discriminating power on near-homogeneous cumulative-NPV trajectories.** When the per-mission contributions are smooth and decline monotonically with discounting, the regime labels are dominated by the (dq)² gradient (early = MOMENTUM, late = ACCUMULATION) and the conservation slope is DISSIPATIVE almost by construction. Layer 1 earned its keep here as a *falsifier* of the concentration hypothesis, not as a generator of regime structure. For a trajectory where the lens would bite, you need genuine inter-mission heterogeneity in contribution magnitude — which this fleet, by design, does not have.

## Cross-references

- **Matrix decision #13** (pitch staged-options reframe / tranche-1 expected-loss): this round answers the windfall question — the verdict is price-driven, not windfall-driven; the $80M anchor needs no concentration adjustment.
- **rhea R-heterogeneous-cadence** (`2e85d4f`): existing verdict (chunk-shrinking loses NPV in every regime) HELD and now mechanistically explained — het loses via a higher breakeven price, not via revenue concentration.
- **iapetus R-staged-options-with-technology-gates** (`7ffc1e6`): produces the $80M tranche-1 expected-loss anchor; this round stress-tests its accumulation-vs-momentum dependence and finds it robust.
- **Locked beliefs** `5535179f` (three engineering bets) and `c95626970c` (L0-04 = 25 t provisional): the economic axis remains non-binding — consistent with titan-5's inverse-risk finding that pricing/cadence cannot rescue the program; the binding constraint is reactor-program availability (L0-24), not revenue cadence.

## Caveat

Hamiltonian Layer 1 is descriptive, not predictive (skill caveat 1). The price-threshold separation is the load-bearing empirical fact; the regime labels are illustrative and partly mechanical (RESULTS §"Methodological caveat"). The dollar figures are anchored to the het-cadence model's WACC 3% / LR 15% / single-flight assumptions and the R-LEO-water-demand-curve clearing-price distribution; the **structural** reading (price-driven, not concentration-driven; het penalty as a breakeven shift) is robust to those anchors.
