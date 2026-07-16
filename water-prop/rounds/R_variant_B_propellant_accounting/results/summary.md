# R-variant-B-propellant-accounting — summary

## Forward propellant stack at matrix parameters (m_dry 53 t, chunk 200 t, with lunar GA)

| Stage | dv (km/s) | MR | mass before (t) | mass after (t) | water/prop consumed (t) |
|---|---:|---:|---:|---:|---:|
| Start at Saturn parking | — | — | — | 255.0 | — |
| Saturn-egress chem | 2.0 | 1.573 | 255.0 | 162.1 | 92.9 |
| Heliocentric electric residual | 4.27 | 1.243 | 162.1 | 130.4 | 31.7 |
| Earth-LEO chem capture | 3.5 | 2.210 | 130.4 | 59.0 | 71.4 |

**Total water/propellant consumed:** 196.0 t from a 200-t chunk.
**Delivered to LEO:** 4.0 t (matrix-stated 80 t).
**Water deficit:** -4.0 t (cannot close without supplemental propellant).

## Required chunk to deliver matrix-stated 80 t

- With lunar gravity assist: **529 t** (matrix L0-05 cap is 200 t; **2.64× over cap**)
- Without lunar gravity assist: **993 t**
- For L0-09 floor 50 t delivered with lunar GA: **399 t** (still over L0-05's 200-t cap)

## Energy budget at Saturn

- Electrolysis energy required for water consumed at 200-t chunk: **3.92 TJ**
- Available at 500 kWe × 0.5 yr × 75% efficiency: **5.92 TJ**
- Ratio available / required: **1.51**
- **Energy is sufficient; the binding constraint is chunk mass.**

## Outbound-carried-chemical scenario (no Saturn-side electrolysis)

If Variant B cannot use chunk water for chemical propellant (e.g., to avoid Saturn-side electrolysis):
- target 30 t delivered, chunk 200 t: carry 236.8 t chemical from Earth; mass at Saturn parking = 367.5 t → LEO launch ≈ 2536 t = **84.5× per delivered tonne**
- target 30 t delivered, chunk 300 t: carry 236.8 t chemical from Earth; mass at Saturn parking = 367.5 t → LEO launch ≈ 2536 t = **84.5× per delivered tonne**
- target 50 t delivered, chunk 200 t: carry 292.5 t chemical from Earth; mass at Saturn parking = 454.0 t → LEO launch ≈ 3132 t = **62.6× per delivered tonne**
- target 50 t delivered, chunk 300 t: carry 292.5 t chemical from Earth; mass at Saturn parking = 454.0 t → LEO launch ≈ 3132 t = **62.6× per delivered tonne**
- target 80 t delivered, chunk 200 t: carry 376.1 t chemical from Earth; mass at Saturn parking = 583.7 t → LEO launch ≈ 4027 t = **50.3× per delivered tonne**
- target 80 t delivered, chunk 300 t: carry 376.1 t chemical from Earth; mass at Saturn parking = 583.7 t → LEO launch ≈ 4027 t = **50.3× per delivered tonne**

## Scoring: 8 HELD / 2 FALSIFIED of 10

Two falsifications are framing refinements, not load-bearing overturns: H-vbpa-f predicted water consumed > 200-t chunk; measured 196.0 t fits within the chunk but leaves only 4 t for delivery. H-vbpa-j had the same root. The substantive finding — delivered mass at matrix parameters is 4 t (not 80 t) — stands.

See `hypothesis_scoring.md` for per-hypothesis verdicts.

## Headline finding — Variant B at matrix parameters delivers 4 t per mission, not 80 t

Under correct propellant accounting (chemical-Saturn-egress + electric-residual + chemical-Earth-LEO-capture per titan's R-inbound-dv-continuous-thrust STUDY.md and the architecture-decision-matrix prose), Variant B at the matrix-stated 200-t chunk with lunar gravity assist delivers **4.0 t per mission**. The matrix's stated 80-t delivered is **20× overstated** under correct propellant accounting.

Without lunar gravity assist, the same configuration delivers **-22.2 t** — chunk insufficient to fuel both inbound impulsive chemical phases AND electric residual coast.

To deliver matrix-stated 80 t per mission requires **528.7-t chunk** (2.64× L0-05 cap). To deliver merely L0-09's 50-t per-mission floor requires **399-t chunk** (2× L0-05 cap).

## Architecture matrix consequence — Variant B "Active sole defensible cell" should be retired

The matrix's current verdict: "Year 0–15 deployment path: 500-kilowatt-electric chemical-kick + electric-inbound (formerly 'Kilopower Variant B'). Active — sole defensible cell."

Under correct propellant accounting at L0-05 chunk cap:
- Delivers 4 t per mission (not 80 t) — fails L0-09's per-mission floor by 92%
- Requires 528.7-t chunk to deliver 80 t — fails L0-05 by 164%
- Requires 399-t chunk just to deliver L0-09's 50-t floor — fails L0-05 by 99.5%

**The matrix has no architectural cell that simultaneously satisfies L0-05 (chunk cap 200 t), L0-09 (per-mission delivered ≥ 50 t), and self-consistent propellant accounting at 500 kWe / ISP 2000 s.**

## Downstream impact on R7 / R8 / R13 NPV chain

R7 / R8 / R13 used `delivered_t = 80.0` for Variant B. Under correct accounting, true delivered is **4 t** — 20× lower. Revenue per mission scales 20× lower, meaning:

- R7's "Variant B break-even revenue $964M at corp 8.7% LR 15%" becomes ~$19,300M per mission. At a corrected per-kg basis, the required clearing price for break-even is far outside R8's plausible distribution.
- R8's "Variant B 51.1% P(NPV+) at sov 3% LR 15%" collapses to essentially zero under corrected delivered mass.
- R13's $4.14B median first-unit cost was already 8× above placeholder. Combined with 20× lower delivery, Variant B's NPV is comprehensively negative under any defensible cost regime.

## Combined R13 → R16 arc — campaign-flipping conclusion

Four rounds (R13 bottoms-up cost; R14 burn consistency; R15 dv-regime; R16 propellant accounting) converge on a conclusion the matrix did not previously articulate:

**ICEBERG has NO engineering-closed architecture at current REQUIREMENTS.md L0-* levels** when:
- First-unit ship cost is anchored to bottoms-up cost-estimating relationships (~$4B median, not the $300–500M placeholder)
- Inbound dv regime is consistent across architectures (impulsive or continuous-thrust)
- Propellant accounting closes self-consistently (chemical mass and chunk mass both conserved)

The matrix's "Active sole defensible cell" framing only survived because earlier rounds combined incompatible assumptions:
- Wrong cost framework ($500M placeholder, 8× too low)
- Wrong inbound stack framework (matrix's "7.5-yr burn / 80-t delivered" doesn't reproduce at any consistent regime; first-principles at 200-t chunk with chemical+electric+chemical gives 4 t delivered)
- Undocumented gravity-assist sequence for impulsive inbound dv
- Inherited stale 80-t delivered figure from a Kilopower-class Variant B that was retired by rhea

**The orchestrator action is now a REQUIREMENTS decision, not an architecture decision.** Options:

| Option | Change | Cost |
|---|---|---|
| **A** | Relax L0-05 chunk cap to ≥ 400 t | Larger ships, harder bag engineering, longer Saturn-ops, launcher impact |
| **B** | Relax L0-09 per-mission delivered to ~5 t | 10× more missions to meet annual target → L0-07 cadence stress |
| **C** | Unlock Earth aerocapture R&D | R-chunk-as-heat-shield revisit is load-bearing; aerocapture-at-Earth removes the 3.5-km/s chemical-capture burn, allowing 200-t chunk to suffice |
| **D** | Retire program as structurally infeasible | Documented in matrix; orchestrator decision |

No additional R&D round on this enceladus-r5 branch will change this verdict; only a requirements amendment or an external aerocapture-R&D breakthrough can. **R-chunk-as-heat-shield-revisit is now the single load-bearing rescue path for the entire program** (matrix Item #13 from earlier rounds, but now elevated to gating-status).

## Caveats

- Hydrolox ISP 450 s is high-performance; some Saturn-side cryogenic implementations may achieve only 430–445 s due to storage and reignition penalties. Modest sensitivity.
- Saturn-egress dv = 2.0 km/s is the conops ingress mirror; actual departure depends on whether ship is parked at Saturn-orbit, ring-region, or moon-surface. Round-trip cost may shift by ±0.5 km/s.
- Earth-LEO capture dv with lunar GA = 3.5 km/s; without LGA = 5.6 km/s. Both are at the conservative end. Some VEEGA-style returns could shave another 0.5–1.0 km/s; doesn't change the headline.
- Bundled 10 W/kg mass model gives m_dry = 55 t at 500 kWe. MARVL-anchored may be higher (~70 t). Doesn't change the qualitative finding; pushes "required chunk for 80 t delivered" from 528 to ~600 t.
- Saturn-ops 0.5 yr is the matrix default; longer ops (1–2 yr) would not unlock more delivered mass because chunk is the binding constraint, not energy.
- This round does NOT model the chemical stage dry mass (electrolyzer + tankage + RL-10 engines). The matrix prose says ~10 t additional. Adding this to m_dry would shift delivered from 4 t to ~3 t — same qualitative result.
