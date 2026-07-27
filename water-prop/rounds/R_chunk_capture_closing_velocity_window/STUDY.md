# R-chunk-capture-closing-velocity-window — bet #1's containment risk is a GNC/mechanism wall, not a structural/energy wall

**Status:** run + STUDY complete 2026-07-22. **4/5 HELD** (H-J5 falsified in one identifiable triple-pessimistic corner; the load-bearing H-J3 holds strongly). Result JSON `results/closing_velocity_window.json`; figure `results/closing_velocity_window.png`.
**Bet under test:** #1 of three (active chunk capture at scale). Converts R-A14's mm/s-vs-low-m/s containment *judgment* into a first-principles physics **window-existence** test.
**Predecessors:** unifies + rigorizes `R_HE_graze_feasibility` (hand-set E_bag, single 482 t, hypervelocity only) and `R_bring_fine_structure_rendezvous` (v_rel free-swept, no floor derived); uses the Cassini spin prior from `R_chunk_capture_monte_carlo/tier_0_5_spin_prior.md`; sharpens `R_A14_engineering_decomposition` (`fd6fab0`).

## Hypothesis (pre-registered; see SCOPE.md)

A FLOOR on achievable closing velocity (ring dynamics: spin ω·r + Hill shear + dispersion + GNC deadband) and a mass-scaled CEILING on survivable closing velocity (bag-fabric strain-energy + peak-decel membrane-tear) bound the operating point. If floor > ceiling, bet #1 is falsified for that mass independent of any reliability guess. Predicted (H-J1..J5): floor mm/s-class, ceiling 5–30 m/s scaling as m^(−1/6), a feasible window ≥100× at p50 for every mass, weak-ice fragmentation binding below the bag-tear ceiling but yielding contained rubble, and despin not a structural prerequisite.

## Test

Deterministic, pure-Python. Per chunk mass {1, 10, 50, 200 t}: mass→radius at ρ=500 kg/m³ ring-aggregate; floor = RSS(spin at p50/p95/fast-rotator from the Cassini 1–10 m bin 0.01/0.05/0.28 rpm, Hill shear (3/2)Ω·2r with the 1.95 m/s/km fine-structure anchor as an upper sensitivity, dispersion 1 mm/s, GNC 1 mm/s); ceiling = min(strain-energy √(2·U·m_fabric/m), membrane-tear √(4π·σ_areal·spec_str·r²/m)) across fabric {Zylon, Kevlar, lightweight} × participation {whole-bag, contact-patch}; fragmentation threshold √(3σ_ice/2ρ) at ice tensile {1,10,100 kPa}. `run.py`.

## Result (chunk masses 1 / 10 / 50 / 200 t)

| mass | radius | floor p50 | floor p95 | ceiling strong | ceiling pessim | window (strong/p50) | window (pessim/p95) |
|---|---|---|---|---|---|---|---|
| 1 t | 0.78 m | 1.68 mm/s | 4.35 mm/s | 24.6 m/s | 2.40 m/s | 14700× | 552× |
| 10 t | 1.68 m | 2.40 mm/s | 8.96 mm/s | 16.8 m/s | 1.64 m/s | 7000× | 182× |
| 50 t | 2.88 m | 3.60 mm/s | 15.2 mm/s | 12.8 m/s | 1.25 m/s | 3565× | 82× |
| 200 t | 4.57 m | 5.45 mm/s | 24.1 mm/s | 10.2 m/s | 0.99 m/s | 1871× | 41× |

Fragmentation threshold (mass-independent): **1.73 m/s (1 kPa) / 5.48 (10 kPa) / 17.3 (100 kPa)**.

| Sub-claim | Pre-registered | Measured | Verdict |
|---|---|---|---|
| H-J1 floor mm/s-class; spin dominates | p50 ≤ 30 mm/s; p95 ≤ 150 mm/s | p50 1.7–5.4; p95 4.4–24 mm/s; spin ≥ shear ✓ | ✅ HELD |
| H-J2 ceiling 5–30 m/s, ~m^(−1/6) | strong 5–30; scale 2.42 | strong 10.2–24.6; **scale 2.42 exact** | ✅ HELD (pessim sub-clause missed 200 t: 0.99 < 1.5) |
| H-J3 window ≥100× p50; ≥10× p95-pessim | ≥100 / ≥10 | 1871–14700× / 41–552× | ✅ HELD (load-bearing) |
| H-J4 weak-ice frag binds below bag-tear, above floor | 1–5 m/s | 1.73 m/s; binds; > floor | ✅ HELD |
| H-J5 despin not a structural prerequisite (p95 & fast ≥10×) | ≥10× all masses | p95 41–552×; **fast 200 t = 7.4×** | ❌ FALSIFIED (fast-rotator corner) |

## Reading

**A feasible closing-velocity window robustly EXISTS at every chunk mass, and it is wide: the containment structural/energy ceiling (~10–25 m/s, mass-scaled) sits 40×–15,000× above the achievable ring-dynamics floor (~2–24 mm/s). Therefore bet #1's containment sub-step is not limited by the catch energy — it is a GNC / mechanism-reliability problem. R-A14's velocity-conditional containment collapse (0.78 at mm/s → 0.55 at low-m/s) is an operational effect (bounce-out, mis-alignment, partial mis-catch, cinch behaviour), not a materials wall.**

1. **The floor is spin-dominated and mm/s-class (H-J1).** The lowest achievable closing velocity is set by the chunk's own spin surface velocity ω·r — you contact a tumbling surface. At the Cassini-derived median spin (0.01 rpm, 1–10 m bin) that is 1.7–5.4 mm/s; even at the p95 tail (0.05 rpm) it is 4.4–24 mm/s. Hill shear ((3/2)Ω·2r ≈ 0.4–2 mm/s across the capture envelope), dispersion, and GNC deadband are all sub-spin. This is the first *derived* floor in the campaign — prior rounds swept v_rel as a free input. It confirms the tier_0_5 architecture note quantitatively: decameter-class spin makes the achievable closing velocity a mm/s problem, not a m/s problem.

2. **The ceiling is m/s-to-tens-of-m/s and scales exactly as m^(−1/6) (H-J2).** Bag area grows as r² ∝ m^(2/3) but chunk KE grows as m, so the survivable velocity falls as √(m^(2/3)/m) = m^(−1/6): the observed 1 t/200 t ceiling ratio is 2.42, matching 200^(1/6) = 2.42 to two decimals. The strong-fabric (Zylon, whole-bag) ceiling is 24.6 m/s (1 t) down to 10.2 m/s (200 t) — the energy limit binds below the tear/force limit (38 m/s at 200 t). This *derives and mass-scales* the hand-set E_bag buckets of R_HE_graze (its 100 MJ → 20 m/s for 482 t brackets our 10–13 m/s at 50–200 t). One honest sub-clause miss: the *pessimistic* corner (contact-patch participation + lightweight fabric) at 200 t is 0.99 m/s, just under the pre-registered ≥1.5 m/s — reported, not retro-edited.

3. **The window is robust — 40×–15,000× (H-J3, load-bearing).** Even under the pessimistic ceiling against the p95 spin floor, the margin is 41× (200 t) to 552× (1 t). To close the window (ceiling = floor) a 200 t chunk would have to spin at ~23 rpm — 82× the CIRS fast-rotator bound and far past centrifugal/cohesive breakup. The window does not close by any credible ring-dynamics floor. This is the load-bearing result: **the physics wall is 2–4 orders of magnitude away from the operating point.**

4. **Weak-ice fragmentation binds first, but yields contained rubble (H-J4).** The deceleration stress exceeds ring-ice tensile strength at a mass-independent 1.73 m/s (1 kPa) — below the bag-tear ceiling, above the floor. So a catch above ~2 m/s on weak unconsolidated ice may shatter the chunk. But the bag contains the rubble and water is still captured; what degrades is *coherent-chunk* delivery, not water capture. Fragmentation is a cosmetic/handling concern, not a capture kill — and it never reaches down to the mm/s achievable floor.

5. **Despin is not a structural prerequisite — except for the fast-rotator tail of the largest chunks (H-J5 falsified, informative).** For median and p95 spin the un-despun floor stays 41–552× below the pessimistic ceiling, so despinning is not needed to survive containment. **But** a *fast-rotator* (0.28 rpm, the CIRS upper bound / "recently-disturbed" tail) 200 t chunk under the *most pessimistic* containment narrows to **7.4×** — under the pre-registered 10×. So in the triple-pessimistic corner (largest mass × fast rotation × worst fabric) despin becomes a structural aid, not just a reliability one. This is a clean, identifiable exception, and it points the same way as the tier_0_5 architecture note ("fewer, larger captures") with a caveat: the larger the chunk, the more the fast-rotator tail matters, and large fast-rotators are the one case where a despin (or a stronger bag) is required rather than optional.

## Revisit

**4/5 held; H-J5 falsified in exactly one corner (fast-rotator + 200 t + pessimistic ceiling = 7.4× < 10×).** The falsification is not a surprise reversal — it is the pessimistic tail of a conclusion (window exists, despin optional) that holds everywhere else by 1–4 orders of magnitude. This is the **sixth** pre-registered *absolute-threshold* miss of the session while the *directional* prediction held: I predicted "despin not needed" (directionally right — true for median/p95 by 40–550×) but set the absolute bar at ≥10× everywhere, and one triple-pessimistic corner lands at 7.4×. The logged pattern (directional pre-registrations hold; absolute-number thresholds run optimistic) recurs; I should have pre-registered H-J5 as "≥10× except possibly the fast-rotator tail of the largest mass," which is the regime-conditional form lesson 18 prescribes. H-J2's pessimistic sub-clause (0.99 < 1.5 at 200 t) is the same failure at smaller stakes.

**Where I could be wrong.** (a) The ceiling assumes the fabric strain-energy is available to decelerate the chunk — a real bag also loses energy to fabric plastic tearing, cinch friction, and rebound; the *effective* absorbing energy could be lower than U·m_fabric, which is why I carried the contact-patch + lightweight pessimistic corner (still 41–552× at p95). (b) The floor assumes GNC can null the COM relative velocity to ~mm/s (conops Hill-drift anchor); if autonomy at Saturn light-time cannot, the *operating* velocity rises into the low-m/s regime — but that is a control limit, not the dynamics floor this round derives, and it is exactly the reliability effect the round attributes containment failure to. (c) ρ=500 kg/m³ was chosen pessimistic-large (bigger r → bigger spin floor); solid ice 917 shrinks the floor further, widening the window. (d) The bag-tear ceiling ignores dynamic/shock amplification at very short stroke; the force limit (38 m/s at 200 t) already sits above the energy limit, so the min is energy-bound and stroke-insensitive.

**Deferred (retest spec):** a despin-budget round for large fast-rotators (the H-J5 corner) — how much propellant/time to de-tumble a 200 t 0.28-rpm chunk to below the p95 floor, and whether a stronger bag is cheaper than despin; and a GNC-limited *operating*-velocity model (does Saturn-light-time autonomy hold the COM match to mm/s, or does the operating point rise into the low-m/s reliability regime R-A14 prices at 0.55?). Both are the residual after this round removes the *structural* wall.

## Cross-learning

- **Sharpens R-A14 (`fd6fab0`) / axis 19 (capture architecture):** R-A14's containment 0.78→0.55 velocity degradation is now physically located — it is **not** a structural/energy wall (which sits 40×–15,000× above the operating point) but an operational/GNC reliability effect. This *strengthens* R-A14's own demonstrator framing: an Earth-orbit catch-and-contain proxy retires exactly the GNC/mechanism question (bounce-out, alignment, cinch), and this round shows there is no materials wall lurking behind it. The mm/s-vs-low-m/s question governs *success probability*, not *survival*.
- **Unifies + rigorizes R_HE_graze_feasibility:** its hand-set E_bag → v_rel ceiling is now derived from fabric mechanics and mass-scaled (m^(−1/6)); its 482 t / 100 MJ / 20 m/s bracket is reproduced at 50–200 t (10–13 m/s). And the two rounds together bracket the regime cleanly: **window closed for hypervelocity graze (6.56 km/s ≫ 64 m/s), window wide-open for residence-class capture (mm/s ≪ 10–25 m/s).**
- **Confirms the tier_0_5 spin-prior architecture note quantitatively:** decameter spin makes the closing-velocity floor a mm/s problem; "fewer, larger captures" is right, with the caveat this round adds — large chunks are exactly where the fast-rotator tail (H-J5) makes despin a structural (not just reliability) requirement.
- **Does NOT reopen axis 19's falsified verdict:** chunk-rendezvous remains falsified at the B-ring-impact / aerocapture level (phoebe rounds). This round bounds the bet-#1 *capture-mechanics* sub-question for the demonstrator narrative; it removes the "does the chunk survive the catch energy?" concern (yes, by 2–4 orders) and narrows the residual to autonomy + 13-yr cinch life.
