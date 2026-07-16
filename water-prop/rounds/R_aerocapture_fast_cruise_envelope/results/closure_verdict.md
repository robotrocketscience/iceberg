# R-aerocapture-fast-cruise-envelope — closure verdict

**Headline:** Round F's STRICT-closing Variant C cell is FALSIFIED at the engineering level. The broader matrix-level issue is more severe: the "aerocapture-conditional" framing across the matrix rests on a MISREAD of R-chunk-as-heat-shield's actual findings.

---

## What this round actually found

### 1. The Round F closing case fails the aerocapture envelope, with margin

For Variant C at aphelion 11 astronomical units (Round F's STRICT-closing cell), the entry conditions are:

| Quantity | Value | Implication |
|---|---:|---|
| Entry velocity at atmospheric interface (no lunar-gravity-assist) | 15.29 km/s | 18 percent higher than R-chunk-as-heat-shield's assumed 12.65 |
| Total entry mass (200 t chunk + 63.8 t tug) | 263.8 t | 2.6× R-chunk-as-heat-shield's 100 t |
| Ballistic coefficient | 5940 kg/m² | 1.5× R-chunk-as-heat-shield's 4000 |
| Required periapsis altitude for single-pass capture | < 40 km | solver hit floor, no feasible altitude found |
| Sutton-Graves peak heat flux at 40 km (model floor) | 13,161 kW/m² | 3.0× R-chunk-as-heat-shield's 4,434 kW/m² at 90 km |
| Bag radiative-equilibrium temperature at this flux | 4,127 K | polyimide laminate fails at 700 K — every layer gone immediately |
| Peak g-load on chunk | 47.9 g | ice tensile strength margin 0.62× — chunk shatters |

**Even ignoring the bag (assume sacrificed), the chunk fails structurally** at 47.9 g peak deceleration. Internal stress ~1.6 megapascals exceeds polycrystalline ice tensile strength of ~1.0 megapascals. Round F's "STRICT closure" is not just engineering-marginal; it is below the structural failure threshold of the chunk itself.

### 2. The model's altitude-floor saturation IS the finding

The solver was set to find the periapsis altitude that produces single-pass capture from entry velocity to low Earth orbit. For every entry-velocity / ballistic-coefficient pair tested, including the cross-check case (aphelion 9.58 astronomical units, 100 t chunk, with lunar-gravity-assist credit, equivalent to R-chunk-as-heat-shield's nominal case), no altitude in the 40–120 km band produced a feasible capture. The vehicle would re-emerge on a hyperbolic trajectory or a highly elliptical orbit.

This is consistent with R-chunk-as-heat-shield's underlying finding: "the ballistic coefficient is too high." For ICEBERG-class vehicles, single-pass aerocapture from Saturn-return velocities does not close at any altitude where the bag can survive thermally.

### 3. Cross-check vs R-chunk-as-heat-shield reveals model anchor was Saturn's MISREAD

The cross-check anchor used in this round's pre-registration ("R-chunk-as-heat-shield reported 180 watts-per-square-centimetre, ablation 0.5 percent, chunk closes") came from Saturn's `R_chunk_as_heat_shield_revisit/SCOPE.md`, lines 19–24:

> "That round established chunk-as-heat-shield is thermodynamically viable for single-pass aerocapture at ICEBERG's 4,000-kilograms-per-square-metre ballistic coefficient (0.5% chunk ablation; chunk survives 99.5% intact). The binding open question was chunk geometric stability through a 200-second hypersonic pulse."

Reading R-chunk-as-heat-shield's actual `STUDY.md` results table (lines 100–107):

| Periapsis altitude | Peak heat flux | Δv per pass | Passes to dissipate 6 km/s | Bag survives |
|---:|---:|---:|---:|:---:|
| 90 km | 4,434 kW/m² | 285 m/s | 22 | no (3,144 K) |
| 180 km | 9.7 kW/m² | 0.003 m/s | 2,032,041 | yes (680 K) |

R-chunk-as-heat-shield's actual aggregate verdict (lines 132–134):

> "Aggregate H-chs-agg: falsified. Multi-pass aerobraking is not the right architectural choice for ICEBERG. The ballistic coefficient is too high."

And (lines 158–160):

> "What is incorrect is treating that conditional as nearly resolved by Mars aerobraking heritage. The heritage does not transfer."

R-chunk-as-heat-shield explicitly listed THREE unresolved engineering programmes that aerocapture would require:
1. Sacrificial bag (single-mission consumable)
2. Separate deployable thermal-protection-system (inflatable ballute or equivalent)
3. Chunk-as-heat-shield with chunk-forward orientation (binding open question, NOT closed)

**Saturn's SCOPE.md cherry-picked sub-finding 2 of R-chunk-as-heat-shield's section "Three observations the result actually supports" while omitting that the same section explicitly notes "the geometric question is unaddressed by this round and is the actual binding engineering question."**

The chunk-survives-99.5%-intact figure refers to *thermal* ablation under a SINGLE-PASS aerocapture — but in that scenario the bag dies at 3,144 K (sub-finding 1 of the same section). The geometric stability question that actually decides whether the chunk-as-heat-shield architecture works was explicitly NOT resolved.

The matrix has been treating this triple-conditional as if it were nearly resolved. It is not.

---

## Hypothesis grading

| Sub-claim | Central anchor | Range | Computed | Held |
|---|---:|---|---:|:---:|
| H-afce-a — entry velocity at aphelion 11 AU, no LGA | 15.4 km/s | 14.5–16.5 | 15.29 | YES |
| H-afce-b — peak heat flux | 330 W/cm² | 200–500 | 1316 | NO (4× over upper bound) |
| H-afce-c — chunk ablation per pass | 0.9% | 0.4–2.5 | 2.59 | NO (just over) |
| H-afce-d — peak g-load | 10 g | 5–18 | 47.9 | NO (2.7× over) |
| H-afce-e — chunk tensile margin | 2.9× | 1.5–6 | 0.62 | NO (chunk shatters) |
| H-afce-f — delivered-mass adjustment | minus 1.0% | minus 0.5 to minus 4.0 | minus 2.59% AND envelope failed | NO |
| H-afce-g — periapsis altitude | 60 km | 50–75 | 40 (floor) | NO |

**1 of 7 held. H-afce-agg FALSIFIED.**

The 6 falsifications are not independent — they cascade from a single underlying error: my central anchors used Saturn's SCOPE.md summary of R-chunk-as-heat-shield, which misrepresented the prior round's findings. My anchor for q_peak was 180 W/cm² (Saturn's implied value); R-chunk-as-heat-shield's actual reported value is 443 W/cm² (= 4434 kW/m² at 90 km). My anchor for ablation was 0.5 percent at 12.6 km/s; R-chunk-as-heat-shield's actual reading was that chunk-survives-99.5% under conditions where bag dies — not a usable architectural case. My anchor for "envelope-pass" assumed the prior round closed; it did not.

---

## Recurring lesson #N — updated reading

**Seven hyperion-2 rounds, seven aggregate falsifications.**

Prior diagnosis (in batch-3 handoff): hyperion's intuition is anchored on chemical-architecture mass-ratio sensitivity, which is wrong for electric architectures. Intervention proposed: compute back-of-envelope number FIRST, then range around it.

This round's diagnosis is different. The intervention worked at the *intuition* level — the entry-velocity anchor (15.4 km/s) was within 0.7 percent of the computed value (15.29 km/s). What was wrong was the *anchor I scaled from*. Saturn's SCOPE.md summary of R-chunk-as-heat-shield was load-bearing for every other anchor (heat flux, ablation, envelope-pass). The summary was wrong — but I treated it as ground truth without re-reading the underlying STUDY.md.

**Updated lesson:** when anchoring to a prior round's findings, re-read the prior round's actual `STUDY.md` Reading and Revisit sections, not the orchestrator's downstream summary. SCOPE documents are framing devices, not authoritative summaries.

This generalises: any "the prior round established X" claim in a SCOPE document or matrix update is a derived assertion. Verify by reading the source round's actual grading and Reading.

---

## Implications for the matrix

This round's finding propagates beyond Round F:

### Direct consequences

- **Round F STRICT closure verdict (aphelion 10.5–11 AU, delivered 23.5–26 t, round-trip 12.7–13.1 yr) is FALSIFIED at the engineering level.** The trajectory closes; the vehicle does not survive the atmospheric capture.
- **Round D Variant C closure verdict (aphelion 9.58 AU Hohmann, delivered 32.1 t, round-trip 16.32 yr at ±2 yr soft margin) is FALSIFIED at the engineering level.** Same physics; the trajectory uses Earth aerocapture as the capture mechanism, which is the falsified mitigation.
- **Round D Variant D verdict (delivered 20.0 t at ±1 yr soft margin) is FALSIFIED.** Includes Earth aerocapture as one of two recoveries.
- **Variant A (no recovery) was already shown to collapse in Round D — delivered 0.0 t, RT 16.92 yr.** This is now the closest-to-physically-honest closure verdict for Variant C/D family.

### Indirect consequences

- **Multiple late-evening orchestrator commits** that integrate "aerocapture-conditional" findings into the matrix are now suspect. Any matrix row whose closure depends on Earth aerocapture has the same misread under it.
- **R-deployable-drag-skirt was killed** (orchestrator commit `34a473b`, per the SCOPE.md cross-reference). With drag skirt killed AND chunk-as-heat-shield revealed as not-actually-closed, ICEBERG has NO surviving Earth-side capture mechanism that closes engineering-side. The architecture must either (a) accept propulsive-only inbound at the ~17.97 kilometre-per-second penalty (titan's number), (b) develop a sacrificial-bag programme as a first-class mass+cost line, or (c) develop an inflatable thermal-protection-system at scales never flown.
- **The R-no-atmospheric-capture-baseline candidate** named in R-chunk-as-heat-shield's "next-round candidates" (lines 178–180) was never run. It is now the most important next round.

---

## Open follow-ons (priority-ordered)

1. **R-no-atmospheric-capture-baseline (high priority).** R-chunk-as-heat-shield explicitly named this as the conservative architecture to confirm closure for. Never run. Now the load-bearing question: with aerocapture removed entirely, does ANY combination of (chemical-kick + electric-inbound + Saturn power class) close any version of L0-05? Or is the matrix's surviving cell empty?
2. **R-sacrificial-bag-mass-and-cost (medium priority).** If aerocapture is to be retained as a conditional, the sacrificial-bag mitigation must be explicitly mass-and-cost-priced. R-chunk-as-heat-shield estimated bag at 1–3 t per unit, $5–20 million per unit — never adopted into matrix as a per-mission line. Adding it would push every closure case's delivered-mass down by 1–3 percent and add $5–20 million to every mission's cost basis.
3. **R-chunk-orientation-stability (medium priority).** R-chunk-as-heat-shield-revisit's binding question. If chunk-forward orientation cannot be held through a 200-second pulse with cold-gas-only attitude control, chunk-as-heat-shield mitigation also fails and the architecture is left with sacrificial bag as the only path.
4. **R-tug-thermal-survival (medium priority).** Even under best-case chunk-as-heat-shield, what's the heat load on the tug behind the chunk? Tug includes reactor and radiators; both have lower thermal tolerance than chunk water ice.
5. **R-outbound-kick-economics (orthogonal but related).** Round F uses 715 t of hydrolox per outbound mission. At Earth-launch costs of $500–1000/kg (Starship best case), this is $358–715 million in propellant per mission, dwarfing the matrix-implied per-mission revenue. May be the second sleeper falsifier of Variant C closure.

---

## Verdict in one sentence

**Round F's STRICT closure verdict, Round D's Variant C / D closure verdicts, and the matrix's broader "aerocapture-conditional" framing all rest on a misread of R-chunk-as-heat-shield; the prior round actually falsified aerocapture for ICEBERG-class ballistic coefficients, and the three required mitigations remain unscoped engineering programmes.**
