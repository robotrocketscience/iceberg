# PROPOSED-PITCH-DIFF — R-pitch-arithmetic-audit

**NOT APPLIED.** This is a proposed diff for the FAIL claims only. Orchestrator applies after the project owner ratifies the per-claim verdicts in `claims_inventory.csv` / `RESULTS.md`. Survive/footnote claims are not diffed here.

Convention: `CURRENT` = verbatim on-disk text; `PROPOSED` = recommended replacement; `WHY` = one-line rationale + claim ID.

---

## D-1 — §2 ΔV table, Saturn departure (C12, line 128) — **highest severity**

**CURRENT**
```
| Saturn departure (low-thrust) | ~1.5 | Water-MET | **Chunk-fed** |
```
**PROPOSED**
```
| Saturn departure (low-thrust spiral + Titan assist) | ~5.5–7.7 | Water-MET | **Chunk-fed** |
```
**WHY:** From the circular B-ring orbit (v_circ 18 km/s, per the pitch's own §1) escape alone is 7.5 km/s impulsive; campaign vis-viva anchors are 5.5 km/s (titan-2 `1b1b889`) to 7.7 km/s (titan-3 `42120cf`). 1.5 km/s is 4–5× too low and internally contradicts §1's ~17 km/s orbital velocity. **This single change cascades into D-2 and D-3.**

---

## D-2 — §2 inbound-ΔV total + delivery efficiency (C10, C13, line 137)

**CURRENT**
```
**Inbound chunk-fed ΔV totals ~4.2 km/s** (Saturn departure 1.5 + cruise braking 2.0 + Earth trim 0.5 + RCS 0.2)... Tsiolkovsky closes at **~54% chunk delivery efficiency** at Isp = 700 s (open-literature water-MET proxy). At Isp = 1000 s the delivery efficiency rises to ~66%; at Isp = 1200 s, ~70%.
```
**PROPOSED**
```
**Inbound chunk-fed ΔV totals ~8–10 km/s impulsive-equivalent** (Saturn departure 5.5–7.7 + cruise braking 2.0 + Earth trim 0.5 + RCS 0.2), with the LGA tour absorbing ~3 km/s at zero propellant cost. Under impulsive accounting this gives **~22–30% chunk delivery efficiency at Isp = 700 s**. Under continuous-thrust (low-thrust spiral) accounting — the regime ICEBERG actually flies — the Saturn-departure and Earth-spiral legs cost 3.8–6.3× their impulsive value (per the water-prop campaign's continuous-thrust audit), and the delivered fraction falls to **~17–28%** at the Isp the surviving cells run (1000–2000 s). The reactor table below is sized in *delivered* chunk mass, so this derate sets how much raw ice each ship must capture.[^isp][^contthrust]
```
**WHY:** The 54% reproduces correctly *only* on the indefensible 1.5 km/s input and *only* in the impulsive frame. The campaign's load-bearing physics (continuous-thrust 3.8–6.3× penalty; surviving-cell delivered fraction 17–22% per titan-2 Block-4 / Option A) puts the honest number at 17–28%. **Add footnote `[^contthrust]`** pointing to the continuous-thrust accounting (titan R-inbound-dv-continuous-thrust; pitch line 35 already cites 24.7 km/s inbound continuous vs 6.42 impulsive). Exact framework value pending R-framework-matrix-parity.

---

## D-3 — §2 round-trip total (C10, line 121 + table line 133)

**CURRENT**
```
**ΔV budget.** Round-trip total ~13 km/s with a 2–3 flyby lunar-gravity-assist...
| **Round-trip total (chemical + electric only)** | **~13.0** | | |
```
**PROPOSED**
```
**ΔV budget (impulsive-equivalent).** Round-trip total ~17–19 km/s impulsive-equivalent with a 2–3 flyby lunar-gravity-assist... (continuous-thrust spiral legs cost more; see footnote [^contthrust])
| **Round-trip total (chemical + electric, impulsive-equivalent)** | **~17–19** | | |
```
**WHY:** Raising Saturn departure 1.5→5.5–7.7 raises the round-trip from ~13 to ~17–19 km/s impulsive. Label the frame explicitly so a sophisticated reader doesn't catch the impulsive-vs-continuous gap unflagged.

---

## D-4 — §3.4 lunar-vs-ICEBERG comparison (C22, line 229)

**CURRENT**
```
Saturn ring → LEO is **~1.5 km/s of chunk-fed-spiral Saturn-departure on water-MET** (consistent with the §4 inbound-ΔV breakdown above)...
```
**PROPOSED**
```
Saturn ring → LEO is **~5.5–7.7 km/s of chunk-fed Saturn-departure on water-MET** — but ICEBERG pays it *once at departure with the cargo as the propellant tank*, where lunar ISRU pays its ~4.6 km/s on *every* delivered tonne. The decisive lever is not per-tonne ΔV (which is comparable) but source concentration (reason 2 below): B-ring ice is ~99% water vs single-digit-weight-% lunar polar regolith.[^contthrust]
```
**WHY:** Punch-list P-2 explicitly warned: do not argue lunar-vs-ICEBERG on per-tonne ΔV (ICEBERG loses or ties once the departure number is corrected). Pivot the argument to source concentration, which ICEBERG wins by 16–98×. Honest and stronger.

---

## D-5 — §6 revenue-stream table, Stream 3 (C33, line 362) + reconcile with §4/§7

**CURRENT**
```
| **3. Saturnian-ring science samples** | NASA / ESA / JAXA flagship programs | First-and-only access to Saturn-system samples |
```
**PROPOSED**
```
| **3. Saturnian-ring science (speculative)** | NASA / ESA / JAXA flagship programs | Hardware-contribution consortium precedent (Cassini-Huygens, BepiColombo); a *science-allocation prebuy* would be a new deal class with no precedent — see §4/§7 |
```
**WHY:** §4 (line 271) and §7 (line 394) already label this speculative / not-in-table / not-load-bearing. §6 over-bills it as a co-equal revenue stream. Gap-filler found no precedent for a sample-allocation prebuy; the precedented analogue is hardware-contribution consortium. Reconcile §6 down to match the §4/§7 hedge. **No revenue-model number depends on this** (bulk water closes alone), so the edit is low-risk.

---

## Suggested new footnote

```
[^contthrust]: **On impulsive vs continuous-thrust ΔV.** The ΔV figures in this section are impulsive-equivalent. Low-thrust electric propulsion spiraling out of (or into) a gravity well accrues 3.8–6.3× the impulsive ΔV on the spiral legs (Saturn departure, Earth-capture spiral), per the water-prop continuous-thrust audit. Deep-space cruise braking is near-impulsive-equivalent. Delivered-fraction figures here apply the continuous-thrust penalty to the spiral legs; the exact value is being reconciled against the mission_graph framework executors.
```

---

## Diff summary

5 edits, all clustered on **one finding** (the §2 ΔV budget) plus one framing reconciliation (§6↔§4/§7). D-1 is the load-bearing fix; D-2/D-3/D-4 cascade from it. None of these change the *qualitative* pitch thesis (water-MET architecture, the moat, the staged gates) — they correct the arithmetic that an outside propulsion engineer would check in the first five minutes.
