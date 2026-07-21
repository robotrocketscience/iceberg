# R-burst-duty-cycle — STUDY

**Round:** R-burst-duty-cycle. SCOPE pre-registered 2026-07-21 with scripted bounds. Owner-directed: the generator's value is burst power, so map the duty cycle that enables it.

## Results vs registered hypotheses — all four HELD

### H1 — the envelope law — **HELD**

The whole envelope reduces to one line: **burst power × duty fraction ≤ 0.363 × recharge power** (η_electrolysis × η_fuel-cell), independent of burst size. At Saturn's fission-free 2.2 kWe spare, a 100 kWe-day burst is repeatable every **125 days**; at 0.8 kWe, yearly.

### H2 — the technology map — **HELD**

The bank's competitive niche is **2.3 hours to multi-day**: below 2.3 h, batteries win (no plant mass); above ~17 h, cycled gas dominates the mass and the bank amortizes beautifully (0.59 kg/kWe-h vs the battery's 5.0). Sustained loads beyond inventory belong to the recharge source directly. This quantifies R172's 5–20× burst advantage and bounds it.

### H3 — ops adjudication — **HELD**

R172's 50–100 kWe × 1–3 d burst class is sustainable fission-free at Saturn **no better than bi-monthly** (63 d best case; the 100 kWe × 3 d case only annually). Weekly heavy-burst operations need **~20 kWe of recharge — reactor margin**, cohering with R179: Saturn operations at tempo are reactor-gated; the fission-free bank supports *campaign-style* ops (a heavy burst per orbit-season), not *industrial-style* ops.

### H4 — the demonstrator fits — **HELD**

At 1 AU the 100 kW array sustains **100 kWe MET firing 8.7 h/day indefinitely**, and a 10 t bank adds an 8.5-day 100 kWe one-shot reserve — bet #2's flight-scale continuous-thrust demonstration fits the fission-free demonstrator with margin. The burst architecture's cleanest customer is the demonstrator, not the Saturn ship.

## Bug-catch (protocol §bug-catch)

None at run time; the round is closed-form and the pre-script implemented every registered mechanism (R177's convention holding).

## Revisit (mandatory)

Thin spots: turbine variant not separately mapped (η 0.30 halves η_rt to 0.20 — fuel-cell assumed; turbine only competes on plant W/kg, unpriced); battery cycle-life and thermal derating at Saturn unmodeled (favors the bank); recharge assumed fully divertible to electrolysis (competes with R178's regeneration credits for the same spare watts — the allocation law needs a burst term if ops planning wants both); plant 100 W/kg is R171's number, not a flight anchor.

## Cross-learning

- **Matrix role statement for the bank:** *a burst concentrator with a 2 h–multi-day niche governed by duty ≤ 0.36 × recharge; campaign-tempo ops fission-free, industrial-tempo ops reactor-gated; primary customer the demonstrator gates.*
- **Coheres with R179** independently: two different physics (departure energetics, ops tempo) now point at the same 15–25 kWe Saturn-side floor for operations at scale.
- **Follow-ons:** spare-watt allocation law v2 (regen + trickle + burst recharge competing); turbine-vs-fuel-cell plant trade at flight W/kg anchors.
