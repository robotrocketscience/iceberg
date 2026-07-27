# Wertz / SMAD subsystem-mass anchor review (H2, H3)

**Worker:** hyperion (re-spawn 2). **Date:** 2026-05-26.

Reviews each `saturn_mass_demands.py` demand function against standard space-systems-engineering mass models (Wertz & Larson, *Space Mission Engineering: The New SMAD*, ch. 11 dry-mass fractions; flown anchors; locked beliefs). **Citation honesty:** SMAD figures below are the *standard-reference-typical* dry-mass fractions from that text's subsystem tables as I recall them; exact page/edition numbers should be confirmed against the physical text before any number is quoted externally. Locked-belief anchors (KRUSTY, MARVL) carry primary-source attribution in the belief store.

## Per-subsystem table

| Subsystem | Framework demand (`saturn_mass_demands.py`) | SMAD-typical / flown anchor | Discrepancy | Verdict |
|---|---|---|---|---|
| Powerplant (reactor+radiator+thrusters) | `required_powerplant_mass_kg`: reactor = kWe·1000/2.4 (KRUSTY); radiator 5 t + 0.1 t/kWe (MARVL); thrusters 10 kg/kWe | SMAD power-subsystem mass fractions are derived for solar/battery LEO buses, not deep-space fission; not directly comparable. Fission anchor is the locked KRUSTY 2.4 W/kg + MARVL (National Academies / NASA). | n/a (SMAD has no fission analogue) | **Anchored to locked beliefs; conservative.** SMAD would *understate* a fission stack (its tables assume PV). The framework is correctly NOT using SMAD here. |
| Bus | 2000 kg floor | SMAD bus/structure for a large deep-space bus: Cassini dry ~2150 kg total; bus subset ~600–1000 kg. The 2000 kg "bus" floor folds in guidance/avionics baseline. | within ~2–3× of a heritage bus subset; conservative | **HELD** (conservative, per constraint-3 retraction from Cassini ~600 kg). |
| Capture mechanism | ram-scoop 1000 + 0.08·chunk + 50·aperture; harpoon 500 + 0.05·chunk; everting 2000 + 0.10·chunk | No SMAD analogue (novel subsystem). First-pass. At 200 t chunk: ram-scoop ≈ 1000 + 16000 + (50·50) = 19.5 t. | unanchorable against SMAD | **First-pass, largest novel-subsystem uncertainty (H3).** The 0.08·chunk coefficient is the load-bearing assumption; ±50% on it swings dry mass by ~8 t at 200 t chunk. |
| Aerocapture TPS | 0.10·chunk + 200·entry_v | SMAD/heritage TPS fractions: 10–15% of entry mass for ablative (Stardust ~17% of capsule; Apollo ~13%). 0.10·chunk ≈ 10% of chunk. | in-family with heritage TPS fractions | **HELD** as a fraction, but charged on *chunk* not on *entry mass* — conservative (entire chunk is not the entry body). Path-conditional refinement (H4) deferred to titan. |
| Primary structure | 0.05·chunk + 100·max_load_kN | SMAD primary structure ~8–12% of dry mass for a loaded bus; here charged as 5% of *chunk*. At 200 t chunk = 10 t structure. | comparable order; basis differs (chunk vs dry) | **First-pass; within order.** Charging on chunk (the towed load) is defensible for a tug; SMAD's %-of-dry would give ~6–12 t at 120 t dry — similar. |
| Comms+guidance+computer | 2000 kg floor | SMAD C&DH + comms for a deep-space bus: ~150–400 kg; 2000 kg floor folds in redundancy + DSN-class HGA. | framework ~5–13× SMAD subsystem | **Conservative** (deliberate deep-space floor); not load-bearing (small vs powerplant/chunk terms). |
| Tankage | 0.05·propellant | SMAD tankage 3–10% of propellant (cryo higher, storable lower); xenon high-pressure ~10%. | 5% is mid-range | **HELD.** |
| Dry margin | 0.20·subtotal | NASA Class-B / SMAD recommended 20–30% growth margin at this maturity | 20% is the low end of standard | **HELD** (arguably should be 25–30% at concept maturity — would make the verdict *more* pessimistic, not less). |

## H2 verdict — HELD

The well-anchored subsystems (powerplant, tankage, TPS-as-fraction, margin) are within standard-reference family or are *conservative* relative to SMAD. The one place the framework departs hardest from SMAD — the fission powerplant — is correct to do so (SMAD's PV-bus tables would *understate* a reactor stack). No subsystem shows a >30% *unexplained* discrepancy in the optimistic direction. Where the framework differs, it is conservative (heavier), which makes the closure verdict more robust, not less.

## H3 verdict — HELD (capture mechanism is the largest *novel*-subsystem uncertainty; powerplant is the largest *absolute* mass)

Two distinct readings:
- **Largest absolute dry-mass contributor:** the powerplant at high kWe (16.7 t reactor + 9 t radiator at 40 kWe) and the chunk-scaled terms (TPS 20 t + structure 10 t + capture 19.5 t at 200 t chunk). At the canonical 30 kWe / 200 t cell (120.8 t dry), chunk-scaled subsystems dominate.
- **Largest *uncertainty* (the SCOPE's H3):** the **capture mechanism** is the only subsystem with no SMAD/flown anchor at all — its coefficient is pure first-pass. So it is the largest source of *epistemic* uncertainty even though the powerplant + chunk-TPS are larger in magnitude. A full total-order sensitivity index (deferred) would quantify this; the analytic reading supports H3 as stated (capture is the least-anchored term).

**Neither reading changes H5:** the binding failure is launch mass (the *sum* of these terms makes the wet vehicle unlaunchable), and every term is first-pass-or-conservative, so refining them down within defensible bounds does not bring the wet vehicle under launch capacity. See FINDINGS.
