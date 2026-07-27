---
axis: "Round-trip ceiling (L0-05)"
status: open
confidence: high
last_revised: 2026-07-22 (latest+26)
related:
  - "[[program-class]]"
  - "[[surviving-cell]]"
  - "[[cruise-trajectory]]"
  - "[[chunk-mass-cap]]"
  - "[[17-pitch-capital-framing]]"
---

# Round-trip ceiling (L0-05)

## Current

15 years strict. Variant C and Architecture E both miss strict L0-05; Architecture E was retired anyway under flown-anchored specific power (enceladus-r5 `62f7079`). **2026-05-19 latest+13 (titan-3 R-chunk-size-pareto `1997a51`):** at 40-80 tonne chunks + 30 kilowatt-electric Kilopower-extrapolation + R12 lunar-gravity-assist Earth-arrival, 4 cells close L0-05 strict (50-60 tonne chunks; round-trip 14-15 years; delivered 30-37 tonnes per mission). 30 cells close L0-05 waiver across 50-150 tonne chunks / 20-30 kilowatt-electric / round-trip 14-22 years / delivered 30-60 tonnes per mission. Strict closure exists physically but only at the smallest closing chunk band — commercial value reduces to 30-37 tonnes per mission, near the L0-09 floor.

**2026-07-21 latest+25 — round-trip *duration* now carries a market-decay economic headwind, and the "fast first chunk, then longer later round-trips" fleet path was tested and closed NPV-dead (R188 `R_clearing_price_time_path` `93a9888`; R182-R187 relay/fleet arc; R184 `R_shuttle_reuse_fleet` `7b9adf6`).** R188 anchored the delivered-water clearing price to the launch-cost experience curve — a 9-18 percent/yr decline (central ~13 percent) that exceeds both campaign hurdles outright — so over a 13-23-year round-trip the market discounts delivered-water revenue *faster than capital*. The strict-vs-waiver decision on this axis is therefore no longer purely an L0-05 compliance question: **every additional year of round-trip is now also a revenue-decay exposure**, which pushes toward the strict 15-year reading and away from the ≥25-year waiver on economic grounds independent of engineering feasibility (see [[17-pitch-capital-framing]]). Separately, the project-owner "return a chunk fast first, then let later vehicles take longer round-trips into the green" fleet hypothesis (recorded in [[02-surviving-cell]] USER-NOTES) was operationalised as the R182-R187 dive-shuttle relay + R184 reusable-fleet ramp: R187 closes the fleet economics NPV-dead at honest departure (best d\* 7.0 percent < 8 percent hurdle). Longer later-vehicle round-trips do not climb into the green; the market-decay headwind is one structural reason why.

**2026-07-22 latest+26 — the titan-3 strict-15yr closure cells cited above lose their inbound-braking mechanism: R12's lunar-gravity-assist Earth-arrival is FALSIFIED (`R-lunar-ga-arrival-fidelity`, `7bcc2e7`, 6/6 HELD).** The 2026-05-19 latest+13 result above ("4 cells close L0-05 strict … under … R12 lunar-gravity-assist Earth-arrival") depended on R12's tour shedding 5.83 km/s of the 10.30 km/s Earth arrival to a 4.47 km/s residual in 10 flybys. That is physically impossible: a lunar flyby conserves the Moon-relative speed U_m (v∞-globe / Tisserand invariant), so a tour sheds at most **v_sc − 2·v_M = 2.07 km/s** at any flyby count (measured 2.069 = analytic bound; inclination second-order), reaching residual 8.23 km/s only over **~51 flybys / ~4.1 yr of Earth-orbit phasing** — which alone pushes the best honest round-trip to **17.3 yr, past the strict 15-yr ceiling → 0 strict cells.** So the strict-closure band on this axis no longer has a lunar-GA path; with aerocapture also closed ([[11-earth-arrival-mode]], 0/1920), the inbound leg reduces to direct-propulsive capture (~7.3 km/s, [[04-inbound-dv-accounting]]), which the titan-4 latest+18 full-round-trip parity already showed closes 0 cells at flyable power. This does not change the current market-decay reading above (that path never used lunar-GA) — it retires the last optimistic inbound lever.

## Open question

Project-owner decision (amended 2026-05-19 latest+13): hold L0-05 strict at 15 years and accept the narrow 50-60 tonne / 30-37 tonne-delivered closure cell, OR admit waiver to ≥ 25 years and unlock the broader 50-150 tonne / 30-60 tonne-delivered band. Architecture E's prior 50 tonnes-at-25-years framing is moot per Architecture E falsification and the 500 kilowatt-electric retirement; the live decision is between strict vs waiver under the titan-3 closure cell.

## Last touched by

- enceladus-r5 R-architecture-E — `448505e` [Architecture E falsified]
- hyperion R-cruise-time-optimization — `db249ba`
- titan-3 R-chunk-size-pareto — `1997a51`
- worktree-115637 R-clearing-price-time-path — `93a9888` (latest+25; round-trip duration = revenue-decay exposure)
- worktree-115637 R-relay-ledger-reconciliation — `aed61c4` (latest+25; fast-first-chunk fleet path closed NPV-dead)
- worktree-115637 R-lunar-ga-arrival-fidelity — `7bcc2e7` (latest+26; R12 lunar-GA inbound braking falsified → titan-3 strict cells lose their inbound mechanism)

## HISTORY

### 2026-05-15 — Initial scaffold from `ARCHITECTURE-DECISION-MATRIX.md` current-decision-state table

Status: open. Confidence: high.

Current state and open question captured from the matrix's top section as of commit `9704700`. Full audit trail of how this axis arrived at its current state is in the matrix HISTORY section (`water-prop/docs/ARCHITECTURE-DECISION-MATRIX.md`).

---

<!-- Append-only HISTORY entries go below this line. Each entry: ### YYYY-MM-DD — round-name or commit-hash — one-line summary -->

### 2026-05-19 latest+13 — titan-3 R-chunk-size-pareto (`1997a51`) — strict L0-05 closes at narrow 50-60 tonne chunk band; waiver closes broader 50-150 tonne band

Under the 500 kilowatt-electric retirement + corrected vis-viva delta-velocity anchors + R12 lunar-gravity-assist Earth-arrival, the strict 15-year ceiling closes at 4 cells (50-60 tonne chunks / P=30 kilowatt-electric / both Kilopower-measured 2.4 watts-per-kilogram and R12-optimistic 10 watts-per-kilogram). Delivered 30-37 tonnes per mission, just above L0-09 floor. Waiver to 25 years adds 30 cells across 50-150 tonne chunks / 20-30 kilowatt-electric / delivered 30-60 tonnes. Strict-vs-waiver decision is now meaningful (both have non-empty closures); the gain from waiver is broader chunk-mass band and higher per-mission delivered mass at the cost of an additional 7-10 years of mission duration. Status held at open / high pending project-owner decision.

### 2026-07-21 latest+25 — worktree-115637 R-clearing-price-time-path (`93a9888`) + relay/fleet arc (R182-R187 `aed61c4`, R184 `7b9adf6`) — round-trip duration reframed as a revenue-decay exposure; fast-first-chunk fleet path closed NPV-dead

R188 anchored the open water-price-decay parameter to the launch-cost experience curve ($3,868 → ~$273/kg LEO 2025-2040; 9-18 percent/yr decline, central ~13 percent), which exceeds both campaign hurdles. Over a 13-23-year round-trip the market discounts delivered-water revenue faster than capital, so the strict-vs-waiver trade on this axis gains an economic term it did not have: the waiver's extra 7-10 years of mission duration is now also 7-10 more years of price decay against the delivered product, pushing the decision toward strict-15 on economic grounds independent of engineering. Separately, the project-owner "fast first chunk, then longer later round-trips into the green" fleet hypothesis (axis 02 USER-NOTES) was tested via the R182-R187 dive-shuttle relay + R184 reusable-fleet ramp and closed NPV-dead at honest departure (best d\* 7.0 percent < 8 percent). The market-decay headwind is one structural reason longer later-vehicle round-trips do not reach the green. Status held at open / high; the strict/waiver decision remains a project-owner call, now with the economic headwind made explicit.

### 2026-07-21 latest+25 — worktree-115637 R-fast-first-chunk-decaying-price (`83badb1`) — decay-robustness of the strict-vs-waiver economics

Folded R188's decaying clearing price into R_heterogeneous_cadence's engine (the one input that round deferred) and confirmed the round-trip-duration headwind at the schedule level: whole-program schedule *compression* is net-negative under decay (it un-discounts committed capex −$269M against +$63M of rescued revenue), while stage-gating the fleet on first-mission success grows *more* valuable under decay (+$1,450M → +$5,626M). Reading for this axis: a longer round-trip is a revenue-decay exposure, but the mitigant is not a faster/shorter trip (which pulls capex forward) — it is deferring the fleet capital via staging. Status held at open / high.

### 2026-07-22 latest+26 — worktree-115637 R-lunar-ga-arrival-fidelity (`7bcc2e7`) — titan-3 strict cells lose their lunar-GA inbound-braking mechanism

The latest+13 strict-15yr closure (4 cells) was conditioned on "R12 lunar-gravity-assist Earth-arrival" shedding 5.83 km/s of the 10.30 km/s arrival to a 4.47 km/s residual over 10 flybys. Falsified: a lunar flyby conserves the Moon-relative speed U_m (v∞-globe invariant); R12 recomputed U_m from the reduced Earth-frame v∞ each flyby (implied U_m falls 73 %). Honest max total shed = v_sc − 2·v_M = 2.07 km/s at any flyby count (measured 2.069 = analytic; inclination second-order), residual 8.23 km/s over ~51 flybys / ~4.1 yr phasing → best honest round-trip 17.3 yr, 0 strict cells. With aerocapture closed (axis 11) the inbound leg is direct-propulsive ~7.3 km/s (axis 04). Current market-decay reading unchanged (never used lunar-GA); the last optimistic inbound lever is retired. Status held open / high.
