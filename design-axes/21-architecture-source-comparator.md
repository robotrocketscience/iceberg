---
axis: "Architecture source comparator"
status: open
confidence: medium
last_revised: 2026-05-21
related:
  - "[[surviving-cell]]"
  - "[[capture-architecture]]"
  - "[[inbound-dv-accounting]]"
---

# Architecture source comparator

## Current

Saturn-ring is the canonical ICEBERG source. **Main belt is geometrically incompatible with the trawl architecture** (saturn-worker wonder pass, commit `030cb5e`): water is bound in phyllosilicate clays not free ice, and particle number density is ~10^20× lower than Saturn ring annuli. Only ~4 of ~700,000 catalogued main-belt objects sit below 7 kilometres-per-second rendezvous Δv. **Near-Earth asteroid is the most credible alternative architecture** under current-technology constraints: 5-9 kilometres-per-second round-trip Δv for low-Δv near-Earth asteroids (2008 EV5 at 6.29 kilometres-per-second rendezvous is the canonical low-Δv target), 1-10 percent water by mass in carbonaceous chondrite phyllosilicates (Bennu and Ryugu returned samples), thermal extraction at 400-700 °C rather than scoop-and-melt; Keck Institute for Space Studies 2012 Asteroid Retrieval Feasibility Study is the reference architecture (28:1 in-mass-amplification to low-Earth orbit for the 7-metre, 500-tonne boulder case). **Lunar polar in-situ resource utilization is the most-cited competitor:** 5.6 ± 2.9 percent water best-case (LCROSS Cabeus), ~1 percent average; ~4.6 kilometres-per-second round-trip with aerobraking (per axis 04 correction); ore-grade ratio for Saturn-ring is 18× best-case lunar / ~100× average lunar.

## Open question

Pending dedicated round (`R_near_earth_asteroid_mission_tree` SCOPE'd as `SATURN-PUNCH-LIST-20260521.md` item S-2; not yet authored as directory). Side-by-side throughput comparison via `water-prop/sims/mission_graph/analysis/mining_view.py` once the near-Earth-asteroid mission graph is encoded as a second tree in the mission_graph forest. Question for project owner: is the near-Earth-asteroid alternative worth bracketing as a serious comparator, or filed as a falsified alternative under phoebe R-mission-architecture-pivot-survey (`bb570d7`, 31 of 31 candidates DEAD-ON-ARRIVAL under conservative anchors)?

## Last touched by

- saturn-worker assumption-audit wonder + reason passes — `030cb5e`
- phoebe R-mission-architecture-pivot-survey — `bb570d7`
- punch-list items M-2 + D-4 + S-2 — `SATURN-PUNCH-LIST-20260521.md`

## HISTORY

### 2026-05-21 latest+15 — saturn-worker assumption-audit wonder + reason passes; orchestrator new-axis creation

Wonder pass surfaced the geometric incompatibility of main-belt water with the trawl architecture (~10^20× lower particle number density; phyllosilicate-bound water). Reason pass synthesized the near-Earth-asteroid alternative architecture per Keck Institute for Space Studies 2012 reference, and corrected the lunar-aerobraking accounting per Wikipedia delta-v-budget table. Saturn-worker recommended a dedicated axis so future SCOPEs do not relitigate. Orchestrator (latest+15 integration pass) creates this axis file from the saturn-worker punch-list item D-4 + matrix axis 21 row. Status: open / medium confidence (the three source candidates are well-anchored in literature; the comparison conclusion is sensitive to which architecture-cell filter — phoebe pivot-survey conservative-anchor versus iapetus F6-conditional — is applied to the alternative candidates).

### 2026-05-22 latest+16 — belief-trace for the wonder + reason passes that produced this axis

Saturn-worker punch-list section 5 asked for a dedicated matrix HISTORY entry citing the belief IDs from the wonder + reason passes. Routed to this axis instead because the relevant beliefs are axis-21-specific. Three load-bearing beliefs anchor this axis's Current section:

- **`c646b3c68ec5a6f3`** (locked, 2026-05-21 Saturn worker) — A4 chunk water fraction CONFIRMED by Cassini microwave radiometry: B-ring 99.7-99.8% water by volume; main rings overall > 99%. Anchors the Saturn-ring side of the source-concentration comparator. Source: water-prop/rounds/R_assumption_audit_2026_05_21/FINDINGS.md.
- **`8be3ec81e5902bf4`** (Saturn-worker gap-filler, 2026-05-21) — lunar-surface-to-low-Earth-orbit with aerobraking is ~4.6 km/s (1.87 ascent + 5.93 low-lunar-orbit-to-LEO − 3.2 aerobraking savings per Wikipedia delta-v-budget table). Anchors the lunar side of the Δv comparator AND the "do not argue per-tonne Δv against lunar with aerobraking admitted" framing. Cross-references axis 04 latest+15 amendment and ICEBERG-pitch.md line 229 latest+16 correction (commit `e572228`). Source: water-prop/rounds/R_assumption_audit_2026_05_21/ wonder pass; saturn-worker commit `030cb5e`.
- **`1488270c10c5bc38`** (Saturn-worker, 2026-05-21) — near-Earth-asteroid round-trip ~6.7 km/s with aerocapture; chunk-tow delivery ratio claim (originally 75 percent; first-principles Tsiolkovsky at stated Isp 800 s + Δv 6.7 km/s gives 42.5 percent — the 75 percent number requires either lower Δv via more aggressive aerocapture or higher Isp than the water-MET literature supports). Anchors the near-Earth-asteroid side of the source-concentration comparator AND flags the delivery-ratio question that R-near-earth-asteroid-mission-tree (SCOPE'd 2026-05-22 latest+16) resolves. Source: water-prop/rounds/R_assumption_audit_2026_05_21/ wonder pass.

Saturn-worker source commit `030cb5e` ("consolidate audit findings") carries the wonder + reason passes' working notes. The other seven locked beliefs from the assumption audit (`31a13abb`, `650938e3`, `c9562697`, `5535179f`, `776575c0`, `edcfe909`, `0418e2c9`, `0d5c882c`) are cited in the matrix's latest+15 HISTORY entry; they touch axes 02, 04, 05, 06, 07, 09, 17, 20 rather than axis 21.
