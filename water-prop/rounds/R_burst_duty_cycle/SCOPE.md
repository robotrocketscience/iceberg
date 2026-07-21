# R-burst-duty-cycle — the duty-cycle envelope that makes the generator worth having

**Status:** SCOPE pre-registered 2026-07-21, before `run.py`. Bounds from `scope_bounds.py`, committed alongside.
**Worker:** worktree-115637 session. Owner-directed: *"i dont really care about continuous power, the win is figuring out what duty cycle enables burst power from the generator."*
**Predecessors:** R171 (plant constants, hotel duty grid), R172 (one-shot burst pricing, 5–20× over batteries), R177/178 (recharge power available: 0.8–2.2 kWe fission-free spare at Saturn), R179 (reactor-margin recharge 10–30 kWe is the surviving Saturn-side context).

## Model

Three closed forms govern the envelope; the round's job is to map them and adjudicate the campaign's actual burst loads against the map. (1) **Sustainability:** average burst draw ≤ η_rt × P_recharge, with round-trip η_rt = 0.66 × 0.55 = **0.363**; cadence τ = P_b·t_b/(η_rt·P_re). (2) **Plant-vs-inventory:** per kWe of burst, fuel-cell plant ~10 kg vs cycled gas 0.59 kg/kWe-h → crossover **t\* ≈ 17 h**. (3) **Battery comparator:** 5 kg/kWe-h at 80 % DoD → battery/bank crossover **≈ 2.3 h**. Sweep: P_re {0.8, 2.2, 10, 30, 100} kWe × P_b {5–200 kWe} × t_b {0.1 h – 7 d}; task anchors: R172's burst grid, R171's hotel duties, bet #2's flight-scale MET demonstration, 10 t one-shot reserve.

## Pre-registered hypotheses (bounds scripted)

**H1 [S] (the envelope law).** Sustainable duty is average-power-limited: P_b × duty-fraction ≤ **0.34–0.39** × P_re (scripted 0.363), independent of burst size; at Saturn's 2.2 kWe spare, a 100 kWe × 1 d burst is sustainable every **115–135 d** (scripted 125); at 0.8 kWe, every **320–370 d** (scripted 344). Falsified outside bands.

**H2 [S] (the technology map).** The bank's competitive niche is **multi-hour-to-multi-day bursts**: battery/bank crossover at **2.0–2.6 h** (scripted 2.27), plant/inventory crossover at **15–20 h** (scripted 16.9). Sub-2-h bursts belong to batteries; sustained loads beyond inventory belong to the recharge source directly. Falsified outside bands.

**H3 [W] (ops adjudication).** R172's 50–100 kWe × 1–3 d burst class is sustainable fission-free at Saturn **no better than bi-monthly** (scripted: 63 d best case; 100 kWe × 3 d only annually); weekly 50 kWe-d operations require **15–25 kWe** of recharge (scripted 19.7) — reactor-margin class, cohering with R179's verdict that Saturn-side operations at scale are reactor-gated. Falsified if any fission-free recharge ≤ 3 kWe sustains weekly 50 kWe-d.

**H4 [S] (the demonstrator gate fits).** At 1 AU with the 100 kW array, the envelope sustains 100 kWe MET firing **≥ 6 h/day** (scripted 8.7) — bet #2's flight-scale continuous-thrust demonstration fits the fission-free array+bank demonstrator, with a 10 t bank adding a **~8.5-day 100 kWe one-shot reserve**. Falsified below 6 h/day.

## Deliverables

`scope_bounds.py`, `run.py` (+ `results/burst_duty_envelope.png`), `results/findings.json`, `STUDY.md` with Revisit; matrix note: the bank's role statement (burst concentrator with a 2 h–multi-day niche; duty law 0.36×recharge) and the ops-cadence implication for capture planning.
