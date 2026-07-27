# R-berth-momentum-management — STUDY

**Round:** R-berth-momentum-management. SCOPE pre-registered 2026-07-21 latest+25 (commit `db3aba1`) before `run.py` existed.
**Worker:** worktree-115637 session. Project-owner-directed: reframed from a redundant "water-RCS momentum" round after the project owner flagged (a) water-fed RCS momentum management is prior art and (b) gravity-gradient torque could desaturate the wheels using the boulder's inertia.
**One line:** The bag-berth capture injects ~5000 N·m·s the reaction wheels cannot buffer. Three legs manage it — thruster dump, gravity-gradient desaturation, capture-geometry control. GG-desat is **real and boulder-strengthened** (clears a berth in 2.5–8.3 days) but **not free** (~300–600 kg CMG buffer + a days-scale cadence floor); **capture-geometry control eliminates the dump entirely** where reachable and is the preferred architecture, with cheap thrusters (plume-managed) the robust fallback.

## Why this is not a re-run of R_chunk_despin_budget

`R_chunk_despin_budget` already priced water thrusters dumping captured angular momentum — up to 15,000 N·m·s for < 125 kg cold-gas — and the vehicle already carries 12× water cold-gas RCS + 4×10 kg reaction wheels. **This round does not re-price thruster propellant.** It tests the *capture-transient* momentum injection (a different L than chunk de-spin), the reaction-wheel *saturation-at-berth* problem the `bag_dynamics_6dof` sim exposed, and — new to the campaign — **gravity-gradient desaturation** enabled by the boulder's inertia. GG-desat appears nowhere prior (the only "gravity gradient" mentions are aerobraking perturbations).

## Hypotheses, tests, results

All computations in `run.py` (deterministic closed form); numbers in `results/berth_momentum_findings.json`; figure `results/berth_momentum.png`.

### H1 [S] — GG torque is a usable desaturation actuator; clears one berth in days — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| τ_gg,max (ΔI = m·r_off² ≈ 1e6 kg·m²) | [0.02, 0.08] N·m | **0.046 N·m** | yes |
| clear-time for 5000 N·m·s (η_gg 0.15–0.5) | [2.5, 10] d | **[2.5, 8.3] d** | yes |
| falsify line | > 30 d | 8.3 d worst | not triggered |

**Reading.** The boulder is why GG works here. A 40 t mass on a 5 m arm gives an inertia asymmetry ΔI ≈ 1×10⁶ kg·m² that *dominates* the vehicle tensor, producing ~0.046 N·m of GG torque at the B-ring — 10–100× what a normal smallsat sees. Over the 9.9 h ring orbit that sheds ~250–830 N·m·s, clearing one berth injection in **2.5–8.3 days** with zero propellant and zero thruster firing. GG-desaturation is a genuine, unstudied actuator for this vehicle, and the project owner was right to flag it.

### H2 [S] — Buffering leg B costs CMG-class mass (~300–600 kg) ≫ thruster propellant (~42 kg) — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| CMG buffer to hold 5000 N·m·s (×1 / ×2) | [285, 600] kg | **286 / 571 kg** | yes |
| thruster-dump propellant (cold-gas / MET) | [3, 45] kg | **42 / 5 kg** | yes |
| 4×10 kg RW cluster vs one injection | RW < injection | **150 ≪ 5000 (33–50× short)** | yes |

**Reading — the counter-intuitive part.** Leg B (GG-desat) is propellant-free, but to *catch* the impulsive berth injection and hold it while GG bleeds it off over days, you need a buffer that can store ~5000 N·m·s. The current 4×10 kg reaction wheels hold ~100–150 N·m·s — **33–50× too little.** Closing that gap takes a CMG (ISS M2000: 4760 N·m·s @ 272 kg), i.e. **~286 kg (×1) to ~571 kg (×2 redundant)** of *dry mass*. The thruster dump it replaces costs ~42 kg of water (cold-gas) or ~5 kg (MET). **So GG-desat does not save mass — it costs ~250–550 kg more dry mass than just firing thrusters.** What it buys is plume-avoidance (see H4), not propellant.

### H3 [S] — Capture-geometry control eliminates the dump entirely — **HELD**

| r_off | max v_c for RW-only (cluster 100–150 N·m·s) | reachable? |
| --- | --- | --- |
| 1 m | 5.0–7.5 mm/s | yes |
| 2 m | 2.5–3.75 mm/s | yes |
| 5 m | 1.0–1.5 mm/s | marginal |
| 10 m | 0.5–0.75 mm/s | **< 1 mm/s floor** |

**Reading.** The injected momentum is L = m_s·v_c·r_off; keeping it inside the existing wheel capacity needs v_c·r_off ≤ H_rw/m_s ≈ **0.005–0.0075 m²/s**. That is reachable with a **close, slow capture** — r_off ≤ 2 m at a few mm/s — which needs no thrusters, no CMG, and no dump. Consistent with the sim's own diagnostic (L = 100 N·m·s held attitude to 4.5°, L = 500 tumbled → the RW-only threshold sits right at cluster capacity). Leg C is the cleanest architecture where the capture concept can be controlled that tightly; it fails only if the bag geometry forces r_off ≥ ~5 m *and* the closing rate can't be held below ~1 mm/s.

### H4 [W] — Synthesis: leg C < B < A; the trade is real (plume-avoidance costs mass + cadence) — **HELD**

| leg | propellant | plume at bag | +dry mass | cadence floor |
| --- | --- | --- | --- | --- |
| **C · geometry control** | 0 | no | 0 | none |
| **B · GG desaturation** | 0 | no | ~286–571 kg | ≥ 2.5 d/berth |
| **A · thruster dump** | ~42 kg (0.042% wet) | **yes** | 0 | none |

**Reading.** Thruster propellant is 0.042% of wet mass — immaterial, exactly as despin found. So leg A is not disqualified on mass; its only real cost is **N thruster firings at the flexible-bag interface** (plume, once per berth). GG-desat (leg B) removes that plume, but pays ~300–600 kg of CMG dry mass **and** imposes a berth-cadence floor of ~2.5–8.3 days (you must wait for GG to bleed the previous injection before the buffer can catch the next). **Capture-geometry control (leg C) dominates both where reachable** — no propellant, no plume, no extra hardware, no cadence limit. The honest ranking: **pursue leg C in the capture concept; fall back to leg A (cheap thrusters, manage the plume) as the robust default; reserve leg B (GG-desat) for the specific case where plume at the bag is shown to be a hard showstopper and the mission cadence is slow enough to absorb the days-scale floor.**

## Revisit / bug-catch (mandatory)

- **η_gg is a modeled band, not a derived control law.** The GG secular-desaturation efficiency [0.15, 0.5] sets H1's clear-time; a proper GG-steering control law would pin it. The verdict is robust — even at η_gg = 0.15 the clear-time (8.3 d) sits well under the 30-day falsify line.
- **GG desaturates in-plane momentum only.** The momentum component along the orbit normal is not GG-controllable and still needs a small RW/thruster trim, so leg B is *mostly* plume-free, not strictly zero-fire. Quantifying the residual-axis fraction (and whether it re-introduces a small plume) is a named follow-on — it does not change the H2/H4 ranking (leg B already loses on mass).
- **Thruster propellant is despin-scaled, not re-derived.** Leg A's 42 kg is `R_chunk_despin_budget`'s 125 kg/15000 N·m·s bound scaled linearly (angular impulse is linear in L at fixed geometry). Leg A's cost claim rests on despin's frozen result, not on new work here — deliberately, to avoid re-litigating settled ground.
- **CMG mass anchored to ISS M2000.** 272 kg/4760 N·m·s is a heavy heritage point; lighter modern CMGs exist, but even the lightest keeps buffer mass an order above the ~42 kg propellant, so H2's *direction* is anchor-robust.
- **No verdict blemish this round** (unlike R191's H1 rounding). All four bands were set at the run grid's edges in `scope_bounds.py` and all four cleared with margin.

## Cross-learning

- **Corrects the `bag_dynamics_6dof` sim STUDY's framing (lives forward, not retro-edited):** the sim concluded "momentum-dumping thrusters are **mandatory**." Sharpened: thrusters are the *robust fallback*, not the only option — **gravity-gradient desaturation (leg B) or capture-geometry control (leg C) both avoid the berth-window thruster firing**, with leg C avoiding all extra cost. The sim's structural finding (reaction wheels store but cannot remove; the injection ≫ RW capacity) stands; "mandatory" was too strong.
- **To `vehicle/SATURN-SHIP-SPEC.md`:** a real spec gap surfaced — the 4×10 kg reaction wheels (~100–150 N·m·s) cannot buffer a nominal berth injection (5000 N·m·s). Either the capture concept must hit leg C's v_c·r_off ≤ 0.0075 m²/s, or the vehicle must carry a CMG (adds ~300–600 kg), or it fires RCS at every berth. This is a design decision the spec does not yet reflect.
- **To design-axes 15 (per-mission reliability):** the R189 mothership-SPOF "saturated-wheel tumble at berth" loss mode is now bounded by an *architectural choice* — leg C removes the saturation entirely; the SPOF tail is worst under leg A if a plume event damages the bag.
- **To REQUIREMENTS §7.5 demonstrator objective #4 (LEO handoff/berth rehearsal):** the rehearsal should measure which leg the capture concept can actually achieve — specifically whether v_c·r_off ≤ 0.0075 m²/s (leg C) is operationally holdable, since that single number decides whether any momentum-management hardware/propellant is needed at all.
- **Named follow-ons (not run):** (1) GG-desat control law + orbit-normal residual-axis quantification; (2) plume-impingement assessment on the bag laminate (decides whether leg A's plume is actually a showstopper — the pivot of the whole trade); (3) capture-concept study on whether v_c ≤ few mm/s at r_off ≤ 2 m is mechanically reachable for a flexible 40 t bag.
