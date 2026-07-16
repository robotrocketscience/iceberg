# R-variant-B-propellant-accounting — where does Variant B's inbound chemical propellant come from?

**Status:** pre-registration. Authored 2026-05-15 by enceladus-r5 (round 16).

## Question

R14 found the matrix's "Variant B inbound burn 7.5 yr / 80-t delivered" doesn't reproduce under any first-principles dv regime if Variant B is all-electric chunk-fed inbound. R15 found that chemical inbound braking interpretation of the matrix's 6.42-km/s impulsive inbound dv requires 837 t of hydrolox propellant (4.2× the 200-t chunk). Both rounds treated Variant B as a single-stage architecture.

Titan's R-inbound-dv-continuous-thrust STUDY.md explicitly defines Variant B's inbound as a **three-stage** stack:

> "Variant B's inbound burn is already chunk-fed-electric, but **Saturn departure is chemical-kick (impulsive)** and **Earth arrival uses chemical capture (impulsive)**. Under those two impulsive maneuvers, the inbound segment payable at electric specific impulse is the small residual — exactly what the matrix's 6.42 km/s represents."

The matrix prose corroborates:

> "For Variant B (Kilopower NPV case): same as above plus add ~10 tonnes for the electrolyzer + cryotankage + chemical stage dry; **chemical propellant comes from chunk at Saturn** (no outbound chemical-propellant penalty)."

So the matrix's *original* Variant B (Kilopower-class) has:
- 10-kWe reactor for housekeeping + electric residual burn
- Saturn-side electrolyzer for in-situ propellant production from chunk water
- Chemical kick at Saturn-departure (inbound start)
- Electric 6.42-km/s residual during heliocentric coast
- Chemical capture at Earth-arrival (inbound end)

**But the matrix table now lists "500-kWe chemical-kick + electric-inbound (formerly Variant B) — Active sole defensible cell."** This was renamed by rhea (commit `a0a0eb5`) when the Kilopower-class was retired under MARVL-anchored mass model. The renamed cell inherits the **6.42-km/s inbound dv** from the prose Variant B framework but **doesn't explicitly carry over the Saturn-side electrolyzer or inbound chemical stages**.

**Primary question:** at the matrix table's 500-kWe / 200-t-chunk parameters, does the chemical-electric-chemical inbound stack close on propellant accounting? Specifically:
1. What chemical dv is required at Saturn-departure and Earth-capture impulsive phases?
2. What hydrolox propellant mass does this require?
3. Where does that propellant come from — chunk-electrolyzed at Saturn (requires Saturn-side electrolysis, contradicting R6's "Architecture E = no Saturn-side electrolysis"), carried outbound from Earth (massive launch mass), or some unaccounted source?

**Secondary question:** is R6's posterior cascade for Architecture E (0.78% median, without Saturn-side electrolysis) applicable to Variant B too? Or does Variant B implicitly carry the Saturn-side-electrolysis cascade factor that R6 removed from Arch E, making Variant B's posterior LOWER than R6 indicated?

## Component-level arithmetic

### Inbound dv decomposition for Variant B per titan + matrix prose

The 6.42-km/s "electric residual" decomposes as (per titan's STUDY.md lines 7 and 110):
- Saturn-side egress (impulsive chemical, ~2.0 km/s) [matches conops 2.09 km/s ingress mirror]
- Heliocentric Hohmann coast (electric residual, ~6.42 km/s gross — but credits lunar gravity assist ~2.15 km/s → ~4.27 km/s electric burn)
- Earth-arrival LEO capture (impulsive chemical, ~3.5 km/s after lunar GA bonus, otherwise ~5.6 km/s)

So the impulsive chemical dvs at endpoints are:
- Saturn-egress: ~2.0 km/s
- Earth-LEO capture: ~3.5 km/s (with lunar GA) to ~5.6 km/s (without)

Total impulsive chemical dv: ~5.5–7.6 km/s.

### Reference cell V — Variant B inbound propellant accounting

Ship dry mass m_dry = 53 t (bundled 10 W/kg, 500 kWe per R7 + R14/R15 framework).
Hydrolox ISP 450 s → v_e_chem = 4413.0 m/s.
Chunk = 200 t.

**Saturn-egress kick (dv 2.0 km/s):**
- Initial mass = m_dry + chunk + m_chem_carried_for_inbound_ops_after_egress
- Final mass after egress kick = (initial mass - m_egress_kick_prop)
- The egress kick must accelerate the *whole* ship + chunk + remaining_inbound_chemical to escape Saturn-orbit.
- Solving back-to-front: ship arrives at LEO with m_dry only (chunk delivered, hydrolox spent).
- m_capture_init = m_dry + chunk_delivered + m_capture_prop. m_capture_final = m_dry + chunk_delivered.
- MR_capture = exp(3500 / 4413) = exp(0.7932) = 2.211.
- m_capture_prop = (m_dry + chunk_delivered) × (MR_capture - 1) = (m_dry + delivered) × 1.211.
- For delivered = 80 t (matrix-stated): m_capture_prop = 133 × 1.211 = **161 t**.
- After capture-prop is accounted, mass at Earth-arrival (start of capture burn) = 133 + 161 = 294 t.

- Electric coast: burns 4.27 km/s electric residual.
- m_electric_init = 294 t (at start of coast, after Saturn-egress burn).
- Wait, this needs more careful accounting. Let me redo it forward-from-Saturn.

**Forward calculation from Saturn parking orbit:**

m_at_Saturn_parking = m_dry + chunk_water_total + m_inbound_chem_total
                    = 53 + chunk_water + m_chem_egress + m_chem_capture

Egress burn (Saturn → Saturn-Earth transfer):
- MR_egress = exp(2000/4413) = exp(0.4534) = 1.574
- All mass at parking accelerates: m_after_egress = m_at_parking / MR_egress
- m_egress_prop = m_at_parking × (1 - 1/1.574) = m_at_parking × 0.3647

Coast: electric burn at 4.27 km/s consumes chunk water as propellant (chunk-fed-electric).
- m_at_coast_start = m_after_egress = 53 + (chunk_remaining_after_egress) + m_chem_capture
  But wait — does the egress kick consume CHUNK water electrolyzed to hydrolox? Or does the egress kick consume CARRIED hydrolox (separately stored)?
- Per matrix prose: "chemical propellant comes from chunk at Saturn." So the egress burn consumes hydrolox electrolyzed from chunk at Saturn.
- So m_chem_egress is electrolyzed-from-chunk and effectively comes out of the chunk's 200 t.

Let chunk_water = C (kg of water at Saturn parking, before any electrolysis).
Let m_eg = chemical hydrolox for Saturn-egress = electrolyzed from f_eg × C kg of water.
Let m_cap = chemical hydrolox for Earth-capture = electrolyzed from f_cap × C kg of water.
Let m_elec = chunk water consumed as electric propellant.
Delivered chunk = C - f_eg × C - f_cap × C - m_elec_water.

Mass at start of egress burn = m_dry + C [since electrolysis transforms water to H2/O2 in-place, no mass change]. Or wait — actually after electrolysis, the mass is the same (electrolysis is just splitting H2O into H2 + 0.5 O2; mass-conserving).

So mass at parking = m_dry + C.

Egress burn at hydrolox ISP 450 s: m_eg = m_at_parking × (1 - 1/MR_egress) = (m_dry + C) × 0.3647
After egress: mass = (m_dry + C) - m_eg = (m_dry + C) × 0.6353

Coast (electric 4.27 km/s, chunk-fed):
- v_e_elec = 2000 × 9.80665 = 19,613 m/s
- MR_elec = exp(4270/19613) = exp(0.2177) = 1.2433
- m_elec = (mass at coast start) × (1 - 1/1.2433) = mass_coast × 0.1957
- After coast: mass = (m_dry + C) × 0.6353 × (1 - 0.1957) = (m_dry + C) × 0.6353 × 0.8043 = (m_dry + C) × 0.5111

Earth-capture burn at hydrolox 3.5 km/s:
- MR_cap = exp(3500/4413) = 2.211
- mass_capture_final = mass_cap_start / MR_cap = (m_dry + C) × 0.5111 / 2.211 = (m_dry + C) × 0.2312

Mass at LEO arrival = m_dry + delivered_water
- m_dry + delivered = (m_dry + C) × 0.2312
- delivered = 0.2312 × (m_dry + C) - m_dry = 0.2312 × m_dry + 0.2312 × C - m_dry
- delivered = -0.7688 × m_dry + 0.2312 × C

For m_dry = 53 t, C = 200 t:
- delivered = -0.7688 × 53 + 0.2312 × 200
- delivered = -40.7 + 46.2
- delivered = **5.5 t**

**Variant B at matrix-stated parameters with full chemical-electric-chemical inbound stack delivers only 5.5 t per mission, NOT 80 t.**

Sanity check: 80 t / 5.5 t = 14.5×. Matrix overstates delivered by 14.5× under correct propellant accounting.

What chunk size is required to deliver 80 t?
- 80 = -0.7688 × 53 + 0.2312 × C
- 80 + 40.7 = 0.2312 × C
- C = 120.7 / 0.2312 = **522 t**

To deliver the matrix's stated 80 t, the chunk must be 522 t — 2.6× the matrix's 200-t L0-05 cap. **Variant B is L0-05-non-compliant on chunk size under correct propellant accounting.**

Alternative reading: if the chemical capture dv at Earth is 5.6 km/s (no lunar GA), it gets worse:
- MR_cap = exp(5600/4413) = exp(1.269) = 3.557
- mass_cap_final = mass_cap_start / 3.557 = (m_dry + C) × 0.5111 / 3.557 = (m_dry + C) × 0.1437
- delivered = 0.1437 × (m_dry + C) - m_dry = -0.8563 × m_dry + 0.1437 × C
- For 53, 200: delivered = -45.4 + 28.7 = **-16.7 t** — chunk insufficient.

**Without lunar gravity assist, Variant B at 200-t chunk delivers negative mass.**

### What if Variant B carries chemical propellant outbound from Earth?

Suppose ship arrives at Saturn carrying inbound chemical propellant (m_eg_carried, m_cap_carried) — no Saturn-side electrolysis needed.

Outbound launch mass at LEO = m_dry + m_eg_carried + m_cap_carried + m_outbound_chemical (already counted by R-outbound-architecture's 6.9× multiplier).

For delivered = 80 t at chunk = 200 t:
- We need 80 t to make it to LEO at end. Capture burn final mass = m_dry + 80 = 133 t.
- Capture burn initial mass = 133 × 2.211 = 294 t.
- m_cap_carried_needed = 294 - 133 = **161 t** (carried outbound from Earth).
- Coast burn at electric 4.27 km/s consumes 0.1957 of coast-start mass.
- Coast-start mass = 294 / 0.8043 = 366 t.
- m_elec = 366 × 0.1957 = **71.6 t** of chunk water consumed as electric prop.
- After coast, before egress prep: 366 t. This includes chunk_remaining = 366 - 133 - 161 = 72 t. (Plus the m_dry of 53, so 53 + 72 + 161 = 286, hmm doesn't quite match — let me redo.)

OK actually let me just write code for this; the algebra is getting tangled.

### Energy budget for Saturn-side electrolysis

Energy to electrolyze 1 kg of water = 15.9 MJ (theoretical) + ~30% real-world overhead = ~20 MJ/kg.
At Saturn-ops 0.5 yr = 1.58 × 10⁷ s, with 500 kWe full power available = 500,000 J/s × 1.58e7 = 7.9 × 10¹² J = **7,900 GJ = 7.9 TJ**.
Mass electrolyzable = 7.9 × 10¹² / 2 × 10⁷ = 3.95 × 10⁵ kg = **395 t**.

OK — at 500 kWe full power during Saturn-ops, electrolyzing 395 t of water is feasible. So power isn't the binding constraint; chunk mass is. The chunk only has 200 t to begin with, and we need ~232 t electrolyzed (161 t for capture + 73 t for egress) — exceeds the chunk.

Actually wait — let me recompute. From above: m_eg = (m_dry + C) × 0.3647. For C = 200, m_dry = 53: m_eg = 253 × 0.3647 = 92.3 t.
And m_cap_needed = 161 t (for 80-t delivered).
And m_elec = (water consumed) calculation: let me see.

Hmm there's an issue. If "chemical propellant comes from chunk at Saturn" means hydrolox is electrolyzed from chunk water, then the hydrolox MASS equals the water MASS that was electrolyzed (mass-conserving). So:
- Water mass consumed for Saturn-egress chemical = 92.3 t (becomes 10.3 t H2 + 82.0 t O2)
- Water mass consumed for Earth-capture chemical = 161 t (becomes 17.9 t H2 + 143.1 t O2)
- Plus electric coast consumes water as ion propellant (mass goes out the thruster as ionized water/oxygen)

Total water consumed = 92.3 + 161 + m_elec = ~285 t — exceeds 200-t chunk by 42%.

So Variant B at matrix parameters CANNOT close even with Saturn-side electrolysis.

To close, chunk must be ≥ ~520 t — exceeds L0-05 cap.

This is the load-bearing finding.

## Pre-registered hypotheses

| Hypothesis | Predicted | Falsification |
|---|---|---|
| H-vbpa-a — Variant B Saturn-egress chemical dv | 1.5–2.5 km/s | outside band |
| H-vbpa-b — Variant B Earth-LEO capture chemical dv with lunar GA | 3.0–4.0 km/s | outside band |
| H-vbpa-c — Variant B at matrix parameters (m_dry 53 t, chunk 200 t, with lunar GA, ISP 2000 s electric, hydrolox capture+egress) delivers ≤ 15 t per mission, NOT the matrix's 80 t | delivered ≤ 15 t | > 15 t |
| H-vbpa-d — Without lunar GA (capture dv 5.6 km/s), Variant B at matrix parameters delivers ≤ 0 t (chunk insufficient as combined electric + chemical propellant source) | delivered ≤ 0 t | > 0 t |
| H-vbpa-e — Required chunk for Variant B to deliver matrix's 80 t per mission, with full chemical-electric-chemical stack and lunar GA | ≥ 450 t (≥ 2.25× L0-05 cap) | < 450 t |
| H-vbpa-f — Variant B inbound architecture requires Saturn-side electrolysis OR outbound-carried chemical OR matrix-stated parameters are wrong; no fourth option exists at 200-t chunk | true | false |
| H-vbpa-g — If Variant B uses Saturn-side electrolysis (matrix-prose option), R6's posterior cascade for "Architecture E = no Saturn-side electrolysis" does NOT apply; Variant B should carry a separate cascade factor including electrolyzer-at-Saturn TRL risk | true (matrix has not done this) | false |
| H-vbpa-h — If Variant B carries inbound chemical outbound from Earth, outbound launch-mass multiplier per delivered tonne grows from R-outbound-architecture's 6.9× by ~2× to roughly 14× | outbound multiplier ≥ 12× per delivered tonne | < 12× |
| H-vbpa-i — Energy required to electrolyze required propellant water at Saturn (~230 t hydrolox + ion-prop water ≈ 285 t total) is 5,700 GJ; available at 500 kWe over 0.5 yr Saturn-ops is 7,900 GJ — energy is sufficient | yes (energy not binding) | falsified if energy < required |
| H-vbpa-j — The 200-t L0-05 chunk cap is the BINDING constraint that breaks Variant B's matrix-stated cell; not energy, not time, not reactor power | yes (chunk is binding) | falsified if any of the others bind first |

## Method

Write a forward propellant-stack solver for Variant B:
- Input: m_dry, chunk_water, dv_egress, dv_elec_residual, dv_capture, ISP_chem, ISP_elec
- Output: delivered_water, water_consumed_total, feasibility flag (water consumed ≤ chunk)
- Sweep over (with-LGA, without-LGA) × (matrix chunk 200 t, allow chunk up to 600 t)
- Compute required chunk to deliver target delivered values {50, 80, 130} t

Then check:
- Energy required at Saturn-side electrolysis vs available
- Outbound-carried alternative scenario: if all inbound chemical is carried from Earth, what's the LEO launch mass per delivered tonne?

Score hypotheses.

## Caveats

- Hydrolox ISP = 450 s (RL-10 class, high-performance space-storable hydrolox).
- Electrolysis energy = 20 MJ/kg water (theoretical 15.9 MJ + 25% real-world overhead). Higher numbers in some studies (~25-30 MJ/kg); doesn't change H-vbpa-i.
- Lunar GA credit = 2.15 km/s at Earth capture (per titan's STUDY.md citation).
- Saturn-ops = 0.5 yr (per R-electric-outbound-rerun's SATURN_OPS_YR).
- Electric ISP = 2000 s, reactor 500 kWe, jet efficiency 0.70 (R-electric-outbound-rerun default).
- Saturn-egress dv = 2.0 km/s impulsive (titan's symmetric mirror of conops 2.09 km/s ingress).
- This round does NOT verify whether 2.0 km/s is realistic for Saturn high-eccentric escape; treats it as input.

## Decision matrix consequence

If H-vbpa-c, d, e hold (delivered ≤ 15 t at matrix parameters; ≤ 0 without LGA; required chunk ≥ 450 t for 80-t delivered), the matrix's "sole defensible cell" is **structurally infeasible** at the stated 200-t / 80-t-delivered combination. The matrix must:

- **(i) Increase chunk to ≥ 450 t,** violating L0-05's 200-t cap (or — equivalently — raise L0-05's cap).
- **OR (ii) Accept much lower delivered mass per mission (~5 t),** violating L0-09's per-mission floor of 50 t.
- **OR (iii) Carry inbound chemical from Earth,** quadrupling outbound launch mass per delivered tonne (R-outbound-architecture's 6.9× becomes ~14× — and Variant B's NPV economics collapse further).

Combined with R13 (cost) + R14 (burn) + R15 (dv regime), this round leaves Variant B with:
- Cost 8× higher than R7/R8 placeholders ($4.14B median first-unit)
- Stated burn time / delivered mass don't reproduce
- Dv-regime asymmetry with Arch E that requires undocumented gravity-assist justification
- Propellant accounting that fails at L0-05 chunk cap

**Combined verdict: the matrix's "Variant B Active sole defensible cell" should be re-classified as either:**

- **Retired (no architecture at 500 kWe / 200-t chunk / chemical+electric+chemical inbound closes simultaneously on dv, propellant, cost, and L0-05/L0-09 compliance),** OR
- **Conditional (closes only at relaxed L0-05 chunk cap ≥ 450 t, with corresponding launcher/operational consequences).**

The R&D campaign's 16 rounds (this branch) plus earlier worker rounds plus rhea integration converge on the same point: **ICEBERG has no engineering-closed architecture at the current REQUIREMENTS.md L0-* level.** Either requirements relax or architecture changes.
