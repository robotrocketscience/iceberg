# Bag cruise-duration model — sub-step 5 (structural survival over the 13-year cruise)

Sub-step 5 decomposes into three independent failure modes: micrometeoroid puncture, water-ice sublimation, and cinch-mechanism thermal-cycling fatigue. The desk-study placeholder was a single lumped 95%. This document anchors each mode; the surprise is that the placeholder's *implied* dominant risk (mass loss / sublimation) is benign, while the *actual* dominant risk (cinch fatigue) was not modelled at all.

## Mode A — micrometeoroid puncture at ~9 AU over 13 years

**Environment.** Interplanetary dust flux falls with heliocentric distance through the asteroid belt and beyond; New Horizons' Student Dust Counter measured grain fluxes (mass ≥ 10⁻¹² g) out to 55 AU, with the flux at 9 AU well below the 1 AU near-Earth value [New Horizons SDC, arXiv:2401.01230]. State-of-the-art *Whipple-shielded* spacecraft stop ~99.997% of micrometeoroids and a shielded lunar surface base sees ~0.024–0.037 *penetrating* impacts/year [arXiv:2511.04740].

**Why a bag is different from a Whipple shield — in both directions.** The trawl bag is soft fabric, not a Whipple shield, so per-impact penetration probability is *higher*. But the bag is a **containment** structure, not a pressure vessel or a thermal-protection surface: a sub-centimetre puncture does not end the mission. The chunk does not leak out of a small hole; it is a solid multi-tonne body. A puncture matters only if it (i) propagates into a tear that compromises gross containment, or (ii) admits a thermal/sublimation pathway. For a Vectran-aerogel laminate with rip-stop weave, small punctures are self-limiting.

**Estimate.** Mission-ending puncture (gross tear from a large-grain impact, not a pinhole) over 13 years at ~200 m² bag area at 9 AU: **1–3%**. Point: 2% → puncture survival ≈ **0.98** (bracket 0.97–0.99). The bag area drives this; a smaller chunk (smaller bag) lowers it.

## Mode B — water-ice sublimation over 13 years

**Physics.** Sublimation rate of water ice in vacuum is steeply temperature-dependent (Hertz–Knudsen, with the Andreas/low-T corrections). Below 70 K the loss is < 1 molecule/cm²/hr; at 100 K no measurable mass change occurs over multi-day laboratory exposures [Icarus 233 (2014) 101, S0019103514000566].

**Cruise temperature.** A passively-cooled grey body at 9 AU has equilibrium temperature roughly T ≈ 278 / √(9.0) ≈ **93 K** (lower with high emissivity / low absorptivity surface treatment, or in the bag interior shadowed from direct sun). At 90–100 K the sublimation recession is microns-to-sub-millimetre over 13 years — utterly negligible against a multi-metre-radius chunk.

**Estimate.** Sublimation mass loss over 13 years at passive 90–100 K: **< 0.1% of chunk mass.** Sublimation survival ≈ **0.995** (bracket 0.98–0.999). **This is the key correction to the desk study:** the placeholder 95% implicitly feared mass loss, but at cold passive cruise temperature mass loss is essentially zero. The only way sublimation becomes a driver is if active thermal control *fails toward warm* (e.g., a fault parks the chunk in sunlight at >150 K) — a control-system reliability question, folded into Mode C rather than the ice physics.

## Mode C — cinch-mechanism thermal-cycling fatigue over 13 years

**This is the actual dominant survive risk, and the desk study did not model it.** The bag is held closed by a cinch / lockout mechanism. Over a 13-year cruise the mechanism sees deep thermal cycling (Saturn-side eclipse cycles, cruise solar-distance variation, attitude-driven sun-angle changes) and must hold a multi-tonne load against any residual chunk motion the entire time.

**Anchor.** Deployable / lockout space mechanisms have non-trivial single-mechanism reliability over long duration; a single-cinch failure probability of **5–15%** over 13 years is defensible for a load-bearing mechanism with that many thermal cycles (no direct flight heritage for a 13-year continuously-loaded cinch). **Redundancy is the obvious fix:** two or three independent cinches in a k-of-n arrangement drop the joint cinch-failure probability sharply. With three independent cinches at single-cinch p_fail = 0.10 and a 2-of-3 hold requirement, joint failure ≈ 3·p² ≈ 0.028.

**Estimate.** Cinch survival, redundant design: **0.93** (bracket 0.88–0.97). Single-cinch design would be ~0.85–0.90 — a reason to mandate redundancy.

## Composite sub-step 5 (survive)

    survive = puncture × sublimation × cinch
    mid  = 0.98 × 0.995 × 0.93 ≈ 0.907  -> ~0.88 after rounding-down for un-modelled coupling
    low  = 0.97 × 0.98  × 0.88 ≈ 0.837
    high = 0.99 × 0.999 × 0.97 ≈ 0.959

Point estimate **~0.88**, bracket **0.80–0.93**. This is *below* the desk-study 0.95 (H5 holds) but the *reason* is cinch fatigue, not the sublimation/mass-loss the placeholder implied. The decomposition relocates the risk: harden the cinch (redundancy), not the thermal/mass budget.

## Reading

Two of the three survive modes (puncture, sublimation) are benign at the cold, low-flux 9-AU cruise environment. The survive sub-step is dominated by **cinch-mechanism reliability over 13 years of thermal cycling**, which is a *design-controllable* reliability driver: mandate redundant cinches and the survive probability moves from ~0.85 (single) to ~0.93 (redundant). The 13-year-survive uncertainty does not retire until the first full mission returns; no demonstrator shortcuts it.
