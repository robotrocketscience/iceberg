# candidates.md — Pre-R0 architecture shortlist

**Status:** Scoping doc. No rounds run yet. Numbers below are pre-registered numeric ranges in the protocol §4 sense — committed to before any sim runs, so R0 can falsify or confirm them.

**Purpose:** Surface the candidate water-propulsion architectures, list expected numeric performance, flag which 3-5 deserve R0 trade-study energy. The protocol (§3, §4) requires we name numbers we'd be embarrassed by if wrong — so the table commits to ranges, not vibes.

## Constraints inherited from ICEBERG architecture

The campaign does not get to optimize the thruster in isolation. The mission imposes:

1. **Power, not bag ṁ, is the binding constraint on thruster mass flow.** *(Spot-check correction 2026-05-14, per protocol §9 — pre-R0 catch.)* Original pre-registration said bag-shroud ṁ_max ≈ 10-100 mg/s bounds the thruster. Reading `ICEBERG-bag-engineering.md` §5.2 + conops §line 87 + Tsiolkovsky math gives the opposite finding:
   - Inbound cruise burns ~12.6 t propellant over 7 yr (Isp=700s, ΔV=4.2 km/s, ~14 t delivered): time-averaged ṁ ≈ 57 μg/s.
   - Peak instantaneous demand during the 1.5 km/s Saturn-departure burn: order of low-mg/s if continuous over months.
   - Bag sublimation rate from a 14-tonne chunk under controlled solar input is many orders of magnitude above either number. The chunk has ~6 months of cumulative max-thrust propellant at all foreseeable demand.
   - **The thruster's ṁ is set by `F = ṁ × v_e`, where F is set by available electrical power. Bag supply is non-binding.**
2. **Power available** *(conops disclosure is thin; using bag-engineering §5.2 and standard NewSpace OTV sizing)*:
   - **Earth-side (Flight 1, outbound to Saturn at 1 AU):** 5-10 kWe continuous from solar arrays. Bag-engineering §5.2: "open-literature water-MET thrust is in the 10-500 mN class for 1-10 kWe input."
   - **Saturn-side (inbound cruise, 9.5 AU):** solar derates by 1/r² to ~1-2% of 1 AU insolation. Either ~100 W effective from a large array, or — *more likely for ICEBERG-scale ΔV* — a fission surface power (FSP) class reactor (1-10 kWe continuous, mass ~500-2000 kg). Conops mentions "FSP era" without sizing it. Treat both regimes as branches in R0.
3. **Inbound ΔV target is 4.2 km/s** (Saturn departure 1.5 + cruise braking 2.0 + Earth trim 0.5 + RCS 0.2). Tsiolkovsky closes at delivery efficiency 54% (Isp=700s), 66% (Isp=1000s), 70% (Isp=1200s). **Isp ≥ 700s is the load-bearing performance floor; ≥ 1000s materially changes delivered mass.**
4. **LEO debris demo (Flight 1)** has different needs: terminal RPO wants ~N-class thrust over minutes-hours, not the mN-class thrust over months that wins on Saturn-cruise Isp. Flight 1 may need a separate or hybrid thruster.
5. **TRL ≥ 4 on critical components** before committing program capital. Clean-sheet physics is fine; clean-sheet *components* are not.

## Candidate architectures

Eight candidates surveyed. Numeric ranges are pre-registered per §4.

| # | Architecture | Mechanism | Isp range (s) | Thrust per kW (mN/kW) | ṁ for 50 mN (mg/s) | TRL today | $ to flight-ready (M) | Bag-feed fit |
|---|---|---|---|---|---|---|---|---|
| A | **Water MET** (microwave-electrothermal) | 10 GHz resonant cavity ionizes water vapor; thermal expansion through nozzle | 600-1000 | 5-12 | 7-12 | 4-5 (Momentus flown) | 15-40 | HIGH — direct vapor inlet |
| B | **Water arcjet** | DC arc heats water vapor; thermal expansion | 400-600 | 8-15 | 10-15 | 4-5 (NH3/N2H4 flown 1990s; water research-grade) | 10-25 | HIGH — direct vapor inlet |
| C | **Water resistojet** | Resistive heater + nozzle, no plasma | 70-150 | 30-80 | 40-90 | 9 (Pale Blue, EQUULEUS flight) | 2-5 | HIGH — direct vapor inlet |
| D | **Solar thermal water** | Concentrator → heat exchanger → water vapor expansion. No electricity in thrust loop. | ~~700-900~~ **330-420** (see derivation-thermal-isp-ceilings.md §D) | N/A (solar-powered) | 1-5 (concentrator-limited) | 3-4 (AFRL STAR breadboard) | 30-70 | MED — needs preheat stage |
| D' | **Solar thermal H₂** (new — hybrid of D + G) | Concentrator → heat exchanger → H₂ vapor expansion. Requires electrolysis preprocessing. | 800-960 | N/A (solar-powered) | 0.1-1 (H₂ very low density) | 2-3 (no integrated demo with electrolyzer) | 40-80 | LOW — needs electrolyzer + cryo H₂ storage (multi-year storage kills it for Saturn cruise) |
| E | **Water electrolysis → H2/O2 chemical** | On-board electrolysis splits water; H2/O2 burned in chemical thruster | 300-380 | N/A (chemical) | bursts at kg/s | 6 (Tethers HYDROS-C flown 2021) | 8-20 | LOW — must liquefy or pressurize first |
| F | **Water-vapor gridded ion** | Ionize vapor; electrostatic grid acceleration | 500-1500 (op-point-dep.) | 0.5-3 | 1-3 (life-limited) | 8 (Pale Blue PBI flown 2025) | 15-30 | MED — needs ionization stage but vapor input natural |
| G | **Hybrid: electrolysis → H2-fed MET or arcjet** | Electrolyze water; feed H2 to high-Isp thermal thruster (H2 has ~3× better Isp than H2O in MET) | 800-1500 (on H2) | 4-10 | 3-5 | 3-4 (no integrated demo) | 25-60 | LOW — adds electrolyzer + cryo H2 storage |
| H | **Water-fed pulsed plasma thruster (PPT)** | Pulse discharge through water layer; ablation + acceleration | 500-1500 | 1-5 (pulsed avg) | 1-5 | 3 (research only) | 20-40 | MED — needs pulsed feed, condensation control |

(Power-per-thrust for thermal classes (A, B, D) is set by energy balance: P_min ≈ 0.5 · ṁ · v_e². At Isp=700s, v_e ≈ 6.87 km/s, so 50 mN at 7.3 mg/s needs ~170W minimum, ~350W realistic with 50% thermal efficiency. At Isp=1000s, 50 mN needs ~350W minimum, ~700W realistic.)

## §9 bug catches (running)

- **2026-05-14, pre-R0:** P6 originally said "bag-shroud ṁ_max bounds the thruster" — *wrong*. Power bounds the thruster; bag supply is non-binding by 3+ orders of magnitude. Corrected in §1 above and in P6 row.
- **2026-05-14, pre-R0:** Row D (solar thermal) originally listed Isp 700-900s — *wrong by 2×*. That number assumed hydrogen propellant; on water alone, solar thermal caps at ~400s due to molecular weight. Corrected by textbook derivation in `derivation-thermal-isp-ceilings.md` §D. New row D' added for the hybrid solar-thermal-on-electrolyzed-H₂ variant.

## Architectural integration story

The ICEBERG-specific design opportunity is **integration of the thruster with the bag-shroud sublimation loop**. The chunk surface sublimes at a rate set by absorbed solar power and surface temperature. That vapor is captured on the cold-wall as frost. Re-sublimation off the cold-wall feeds the thruster.

This means the thruster sees a **vapor input at low pressure (~10 Pa), at the rate the cold-wall heater chooses to re-sublimate**. That input matches MET / arcjet / resistojet natural inlet conditions. It does *not* match electrolysis-chemical (E, G) or gridded-ion (F) without an intermediate stage.

**Two distinct architectural bets sit inside this shortlist:**

- **Bet 1 (thermal-direct):** The bag's vapor output feeds the thruster directly. Candidates A, B, C, D. Simplest integration. Performance ceiling is thermal Isp ~ √(T) limit — fundamentally bounded by what gas temperature you can sustain in the thrust chamber without melting the nozzle. MET wins on Isp because plasma temperatures exceed metallurgical limits.
- **Bet 2 (chemical preprocessing):** Electrolyze the water first, then thrust on H2 (or H2/O2 chemical). Candidates E, G. Higher Isp ceiling on H2-fed thermal, or higher thrust burst on H2/O2 chemical. Pays for it with electrolyzer mass, cryo storage, and an extra failure mode.

These bets pivot the architecture in opposite directions and **can't both win**. R0 should pick the bet first, then pick the thruster within the bet.

## Pre-registered numeric predictions (commit before R0)

Following §4, here are the numbers I am willing to be wrong about:

| Prediction | Held with margin | Held | Wrong: useful | Wrong: informative |
|---|---|---|---|---|
| **P1**: Bet 1 (thermal-direct) beats Bet 2 (chemical preprocessing) on delivered-chunk-mass-per-dry-kg for the Saturn cruise leg. | Bet 1 delivers ≥ 20% more chunk mass | Bet 1 wins by 5-20% | Bet 1 wins by < 5%, or ties | Bet 2 wins outright |
| **P2**: Within Bet 1, MET (A) beats arcjet (B) on Saturn-leg delivered mass by 8-15%. | ≥ 15% | 8-15% | 0-8% | Arcjet wins |
| **P3**: Solar thermal (D) is thrust-limited below 5 mN at chunk-class concentrator sizes (10-50 m² collecting area), and therefore fails to close the Saturn cruise leg within 13 years. | Thrust ≤ 3 mN | 3-5 mN | 5-10 mN | ≥ 10 mN |
| **P4**: Flight 1 (LEO debris demo) propulsion is decoupled from Saturn-leg propulsion. Best Flight 1 choice is **not** the same as best Saturn-leg choice. | Different category | Same category but different SKU | Same SKU | (single architecture wins both) |
| **P5**: Total clean-sheet development cost to TRL 7 flight-ready hardware lands in the $15-40M range for the winner (consistent with published commercial water-propulsion development costs). | $25-40M | $15-25M | $10-15M | $5-10M or > $40M |
| **P6 (CORRECTED 2026-05-14, see §1 above):** ~~Bag-shroud ṁ_max ≈ 10-100 mg/s bounds the thruster.~~ **Restated:** Power is the binding constraint. At 1 AU with 5-10 kWe, water-MET thrust lands in 50-500 mN range (bag-eng §5.2). At Saturn with FSP-class 1-10 kWe, similar range; with solar-only ~100 W, thrust falls to 1-10 mN. Saturn-side power source (FSP vs solar) is the more consequential architectural sub-decision than thruster choice within Bet 1. | FSP confirmed required | FSP probably required; solar marginal | Solar viable with 200+ m² arrays | Solar viable with conops baseline arrays |

Aggregate prediction: **MET (A) wins on Saturn-leg, arcjet (B) is the budget option, water electrolysis+chemical (E) is the Flight-1 RPO answer. The campaign's verdict will be: adopt MET for the deep-cruise architecture, defer or hybrid arcjet for the demonstrator, and reject solar-thermal, gridded-ion, and PPT as architectural dead-ends for ICEBERG specifically (not for other missions).**

**Treat the aggregate prediction as a hypothesis, not a baseline.** I am committing to it before R0 specifically so that if R0 falsifies it, the campaign produces a real surprise. The whole point of pre-registration (§4 of the protocol) is that the prediction has teeth — being wrong is informative. If the aggregate is right, the campaign reinforces the conops baseline at lower cost; if wrong, we re-architect from the surprise.

Known reasons the aggregate could be wrong:
- **MET vs arcjet on the Saturn-cruise leg might invert** if arcjet thermal efficiency at high power (kW-class) exceeds MET. The MET literature is dominated by lab-scale 10-W-class data; high-power scaling is an open question.
- **Solar-thermal (D) might actually close** if we relax the Saturn-side constraint (i.e., Saturn-leg uses FSP and solar-thermal is competitive only on the outbound 1 AU leg).
- **Bet 2 (chemical preprocessing, E or G) might win** if the H2/O2 chemical kick stage *replaces* the bought TSI chemical kick stage in the conops, eliminating a chemical-stage purchase. That changes the cost-side accounting in a way the trade-study metric should capture.
- **The whole "single architecture" framing might be wrong.** If the optimal answer is a *stack* (e.g., MET for cruise, arcjet for stationkeeping, electrolyzed-H2/O2 for RPO and capture), then the verdict isn't one winner — it's a propulsion-suite spec.

## Recommended R0 trade study

R0 should be a numeric trade across the 8 candidates on a single mission scenario, with the bag-shroud ṁ constraint binding. The metric is **delivered chunk mass per dry-tug kg** for the Saturn cruise leg, with secondary metrics on thrust-time integrand (for ΔV closure within 13 years) and development $.

Concretely:

```
run_R0_saturn_cruise_trade.py
  inputs: Isp(architecture), thrust_per_kW(architecture), mdot_max_bag(t),
          mission_duration_y=13, deltaV_target_km_s=4.2, P_array_kW=5
  loop over architectures A..H
  for each: compute delivered_chunk_mass_per_dry_kg
  output: ranked table, JSON to results/R0_saturn_cruise_trade.json
```

This is a closed-form sim (Tsiolkovsky + Edelbaum + thermal energy balance), runs in seconds, deterministic. No Monte Carlo, no DSMC. Just the rocket equation done eight ways.

## Open questions before R0

1. **Which candidates do we keep?** The recommendation is to keep all 8 for R0 (it's a one-script trade), drop in R1 based on R0 ranking. But if you want to cut earlier (e.g., drop gridded-ion (F) and PPT (H) outright as architectural dead-ends), name it.
2. **Power budget.** Conops says 5-10 kW at 1 AU. For the Saturn-cruise leg, 40-80 W. Do we run R0 at *both* power regimes (Earth-side and Saturn-side) and compare, or pick one?
3. **Bag ṁ_max.** I've assumed 10-100 mg/s for the 14-tonne demonstrator. Is this consistent with what `ICEBERG-bag-engineering.md` actually models, or do we need a quick check before R0?
4. **Aggregate prediction.** Above I committed to "MET wins on Saturn-leg." Want to amend before we run R0 and lock it as the pre-registered baseline?

Once these are decided, HYPOTHESES.md gets the formal pre-registration, RUNNING_DOC.md gets its skeleton, and `harness.py` gets the closed-form sim primitives (Tsiolkovsky, Edelbaum, MET energy balance, bag sublimation flux).
