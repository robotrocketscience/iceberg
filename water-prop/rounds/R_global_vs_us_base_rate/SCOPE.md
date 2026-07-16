# R-global-vs-US-base-rate — does broadening the base rate flip H6?

**Status.** Pre-registration. Authored by iapetus, 2026-05-15 (latest+9, after R-demonstrator-window-sensitivity).

**Why.** R-reactor-specific-power-program-targets H6 verdict and R-demonstrator-window-sensitivity confirmation are both anchored on a US-only fission-orbit base rate of 0-of-6 since SNAP-10A (1965). That anchor comes from locked belief 2 ("ICEBERG power finding 2"). It is a deliberate scoping choice — the ICEBERG demonstrator is intended to fly under US sovereignty / capital — but it may not be the correct base rate for the underlying technical question "what is the probability that any reactor delivers the required specific-power × lifetime × scope point in the demonstrator window?".

**Question.** If we substitute a *global* fission-orbit base rate (US + USSR/Russia + China) for the US-only base rate, does the conjunction posterior change enough to flip H6?

This challenges the most-load-bearing remaining assumption in the chain. The global base rate is qualitatively different:
- USSR/Russia successfully orbited ~32 fission reactors (BUK series 1970-1988 + TOPAZ 1987). 0 of these were ≥ 500 kilowatt-electric (BUK was ~3 kilowatt-electric, TOPAZ was ~6 kilowatt-electric).
- China has a public megawatt-class space-nuclear roadmap (CASC, CNSA) but 0 fission orbits to date. Stated 2030 goal for high-temperature-gas-cooled-reactor-derivative megawatt-class.
- Russia has stated megawatt-class ambitions (Zeus program, ~0.5-1 megawatt-electric Brayton-conversion target). 0 orbits since 1988.

The structural trade-off: a global base rate gives **higher** p(any-reactor-orbit-by-year-T) but **lower** p(scope ≥ 500 kilowatt-electric | orbit), because the orbited fission reactors have all been ≤ 6 kilowatt-electric. The net conjunction may shift up, down, or stay flat.

---

## Pre-registered hypotheses

| # | Hypothesis | Predicted | Falsification |
|---|---|---|---|
| H1 | The global per-decade fission-orbit base rate is ≥ 3× the US-only rate at program-level (counting distinct programs that intended orbit), driven by USSR-BUK + USSR-TOPAZ + China + Russia-Zeus additions. | global rate / US rate ≥ 3× at uniform prior | H1 falsified if ratio < 2× |
| H2 | The scope conditional p(scope ≥ 500 kilowatt-electric | global-orbit) is ≤ 1/3 of the US-only scope conditional p(scope ≥ 500 kilowatt-electric | US-orbit, where Fission-Surface-Power-Phase-2 derivative is the canonical 500 kilowatt-electric program). Historical orbited fission reactors are all ≤ 6 kilowatt-electric; only paper programs (Zeus, China's megawatt roadmap) target ≥ 500 kilowatt-electric. | global scope conditional / US-only scope conditional ≤ 0.33 | H2 falsified if ratio > 0.5 |
| H3 | The net conjunction posterior at the 2032-2035 window is within a factor of 2× of the prior round's US-only result (max conjunction ~0.0055% under uniform + rendezvous-hi). The orbit-rate-up and scope-conditional-down effects approximately cancel. | global max conjunction at 2032-2035 in [0.0028%, 0.011%] | H3 falsified if outside this range |
| H4 | H6 remains intact under global base rate: max conjunction never crosses venture (10%) threshold within the 50-yr-horizon under any prior. | venture breakeven = never-in-horizon under all priors | H4 falsified if venture is crossed at any year under any prior |
| H5 | The methodology-lesson candidate: when the load-bearing parameter is the scope conditional (not the orbit rate), broadening the base rate is a no-op because the binding constraint moves with the base. This is the symmetric counterpoint to the prior round's "window-extension is no-op because base is too small". | conjunction at global-base-rate, 2032-2035 within ±50% of US-only result | H5 falsified if conjunction shifts by > 2× in either direction |

---

## Method sketch

1. **Re-instantiate Bayesian Monte Carlo** with global program-level base rate. The new "observed-data" set is:
   - US: 1 program with orbit (SNAP-10A), 6 programs without orbit (SP-100, Timberwind, Prometheus, DRACO, Kilopower-flight, Fission-Surface-Power-Phase-2-pending). Net 1-of-7 at program level.
   - USSR/Russia: BUK (1 program, orbited), TOPAZ (1 program, orbited), Zeus (1 program, not orbited). Net 2-of-3.
   - China: CASC-megawatt (1 program, not orbited). Net 0-of-1.
   - Global: 3-of-11 → Beta-Binomial posterior much shifted from US-only 0-of-6.
2. **Scope conditional**: re-derive p(scope ≥ 500 kilowatt-electric | orbit) from the historical scope distribution.
   - Historical orbited scope: SNAP-10A 0.5 kilowatt-electric; BUK ~3 kilowatt-electric × ~30 units; TOPAZ ~6 kilowatt-electric × 2 units. **Zero orbited reactors at ≥ 500 kilowatt-electric.**
   - But the conditional is about prospective programs in the demonstrator window, not retrospective. Use a mix: prospective programs explicitly targeting ≥ 500 kilowatt-electric (Fission-Surface-Power-Phase-2 derivative, Zeus, China-megawatt) vs the historical scope distribution.
   - Anchor: p(scope ≥ 500 kilowatt-electric | global-orbit-in-window) ≈ p(scope ≥ 500 kilowatt-electric | orbit-of-currently-pending-program). Of currently-pending programs:
     - Fission-Surface-Power-Phase-2 (US): target 100 kilowatt-electric per Duffy directive (scope grew from 40 to 100 kilowatt-electric Aug 2025). Below 500 kilowatt-electric.
     - Zeus (Russia): target ~500-1000 kilowatt-electric. At threshold.
     - China-megawatt: target ~1-10 megawatt-electric. Above threshold.
   - Net subjective: p(scope ≥ 500 kilowatt-electric | global-orbit-in-window) ≈ 0.4 (down from 0.6 for US-only, since Fission-Surface-Power-Phase-2 itself targets only 100 kilowatt-electric, well below 500).
   - Sensitivity: report at 0.3 and 0.5 brackets.
3. **Re-apply** R-reactor-specific-power-program-targets conditional-prior chain (specific-power conditional, lifetime conditional, aerocapture conditional, engineering-closure priors, capital-class thresholds) at the new orbit-and-scope posterior.
4. **Compute sensitivity table** at the 2032-2035, 2040, 2045, 2050, ever-50yr windows.
5. **Compare side-by-side with prior round** at the 2032-2035 window.

---

## Method caveats

- USSR/Russia BUK and TOPAZ orbits were in 1970-1988, with no orbits since 1988 (~37 years). The "alive" program count for global base rate must reflect this: USSR space-fission ended after the Kosmos 1818 leak incident and the end of RORSAT. Treating BUK as a current program would over-count; treating it as a closed program may under-count because the underlying base rate of US-USSR-China-fission-orbits should include the historical successes.
- A more-honest model uses an inhomogeneous Poisson process with time-varying rate. But for this round, a Beta-Binomial on program-level success rate is sufficient as a sensitivity test; the qualitative result is what matters.
- The scope conditional in the prior round (0.6) was hyperion's planning anchor for Fission-Surface-Power-Phase-2-to-500-kilowatt-electric scope grow. The right counterfactual for the global base rate is: given the actual mix of currently-pending programs and their scope targets, what is p(any of them orbits at ≥ 500 kilowatt-electric in window)? This is what subjective-prior anchoring delivers.
- **The specific-power and lifetime conditionals are anchored on US Fission-Surface-Power-Phase-1 design specs.** They may not be the right conditionals for Chinese or Russian programs. Documented as an open methodology concern; not addressed in this round.

---

## Reading template

- **Hypotheses adjudicated.** H1-H5 verdicts.
- **Headline.** Does global base rate flip H6?
- **Reading.** Recommendation: if H6 inverts, project owner must add a non-US-reactor-program Level-0 to the requirements doc (i.e. permit non-US-sovereign supply). If H6 holds, the US-only anchor is robust and the conclusion strengthens.
- **Cross-learning.** Connection to R-power-bayesian-update (and whether non-US should be added to that round's likelihood multipliers). Connection to R-reactor-roadmap (which has the cumulative-distribution-function for FSP).
- **Next-round candidates.** Per methodology, this is the last load-bearing sensitivity left. After this, if H6 holds, the conclusion is settled.

---

## Worker assignment

- **Round priority:** high. The remaining sensitivity that could plausibly flip the load-bearing reading.
- **Worker fit:** iapetus (this session) — synthesis chain already loaded.
- **Inputs:** locked beliefs 2-4; `R_power_bayesian_update/run.py`; `R_reactor_specific_power_program_targets/results/reactor_program_targets.json`; `R_demonstrator_window_sensitivity/results/demonstrator_window_sensitivity.json` (for the cross-comparison).
- **Out-of-scope:** competitive-strategy implications of relying on non-US reactor supply for ICEBERG. That's a project-owner / Level-0 question downstream of this round's technical result.
