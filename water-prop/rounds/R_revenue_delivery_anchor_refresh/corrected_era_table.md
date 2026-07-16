# Corrected §4 era-table delivered-tonnage column — drop-in for the pitch rewrite

**Status:** drop-in proposal. **Do NOT auto-apply** — orchestrator-owned (`ICEBERG-pitch.md` is a shared doc), and the pitch rewrite is gated on project-owner ratification (same gate as R-pitch-arithmetic-audit `PROPOSED-PITCH-DIFF.md`). Feeds the deferred R-pitch-arithmetic-audit claims C20 / C26 / C28.

**Source of the correction:** R-pitch-arithmetic-audit (`f9f7fc2`) honest delivery fraction 17–28%; R-framework-matrix-parity full-round-trip pin (39.5 t / 200 t ≈ 20% constraints-OFF; 0 t constraints-ON); REQUIREMENTS L1-007 chunk-mass cap = 200 t captured.

---

## The one arithmetic fact that fixes the table

Delivered-per-mission = **delivery-fraction × captured-tonnes**, and captured-tonnes is capped at **200 t (L1-007)**. So the cap-respecting delivered-per-mission ceiling at each fraction is:

| Delivery fraction | Reading | Max cap-respecting delivered/mission (= fraction × 200 t) |
|---|---|---|
| 0% | conservative / matrix-faithful (no closing cell) | **0 t** |
| 17% | band floor | 34 t |
| ~20% | **framework constraints-OFF pin (39.5 t / 200 t)** | **~40 t** |
| 25% | band optimistic | 50 t |
| 28% | band ceiling | 56 t |

**The pitch's "50 t delivered" is only honest at a 25% fraction — the optimistic end of the corrected band.** At the framework's pinned constraints-off fraction (~20%) the cap-respecting delivered mass is **~40 t**, not 50 t. Under the matrix-faithful conservative reading it is **0 t**. To deliver 50 t at the framework-pinned ~20% you would need to capture **250 t**, which violates the 200 t cap by 25%.

---

## Current §4 table (lines 72–74 of `ICEBERG-pitch.md`)

| Era | Tonnage | Per-ship gross | Annual run-rate |
|---|---|---|---|
| Entry tier (Kilopower-era) | 50 t | ~$400M | ~$370M/yr |
| Mid program (FSP-era) | 200 t | ~$700M | ~$550M/yr |
| Steady state (sub-MW+ era) | 500–1000 t | ~$1.3–2.3B | ~$1.2–2.1B/yr |

(The §2 text states the table is "sized in *delivered* chunk mass." The reader's notes at lines 76 / 41 already flag the 200 t and 500–1000 t rows as infeasible; this drop-in makes the delivered-tonnage column internally consistent with L1-007 and the corrected fraction.)

## Corrected delivered-tonnage column

| Era | **Delivered/mission (corrected)** | Note |
|---|---|---|
| Entry tier (Kilopower-era / demonstrator-class) | **0 t (conservative) — 34–56 t (constraints-off band); ~40 t at the framework pin** | The single number "50 t" was the 25% (optimistic) corner. State as a band, not a point. The conservative matrix-faithful reading delivers **0 t** (no closing cell). |
| Mid program (FSP-era) | **≤ 56 t** (capped) — not 200 t | 200 t is the **captured** chunk ceiling (L1-007), not the delivered mass. Delivered = 17–28% of it = 34–56 t. The "200 t" figure conflates captured with delivered. |
| Steady state (sub-MW+ era) | **structurally infeasible** at 500–1000 t | 500–1000 t delivered needs 1,800–5,900 t captured — 9–29× the 200 t cap. Already flagged infeasible (line 41, line 76). The delivered ceiling at any era is 56 t while L1-007 = 200 t holds. |

### Revenue restatement (proportional to delivered tonnage)

Per-ship gross scales linearly with delivered tonnes at a fixed $/kg. The current entry-tier "~$400M" implies ~$8,000/kg at 50 t. Holding that price:

| Delivered/mission | Per-ship gross at ~$8k/kg |
|---|---|
| 0 t (conservative) | $0 |
| 34 t (17%) | ~$270M |
| ~40 t (framework pin, 20%) | ~$320M |
| 50 t (25%, the old headline) | ~$400M |
| 56 t (28%) | ~$450M |

**The entry-tier per-ship gross is a band ~$270–450M (centered ~$320M at the framework pin), not a point $400M — and $0 under the conservative reading.** The mid-program and steady-state per-ship figures ($700M, $1.3–2.3B) assumed 200 t and 500–1000 t delivered, which the cap forbids; at the delivered ceiling of 56 t the per-ship gross cannot exceed ~$450M at this price regardless of era.

---

## What this drop-in does NOT change

- The **program-class verdict is unchanged** (see `READING.md`): sub-sovereign-bond / technology-demonstrator at conservative anchors. The delivery correction lowers per-mission tonnage and revenue but does not move the binding constraint (reactor-program availability, L0-24). This is a **pitch-honesty fix, not a thesis change**.
- The $/kg price anchor (R-pricing-anchor-revisit: floor $1,400–3,000, operative blend $5–25k+ for mission-essential segments). That correction is independent and already covered.
- L1-007 (200 t cap) and the retired 200–500 kWe / megawatt power classes — taken as given.
