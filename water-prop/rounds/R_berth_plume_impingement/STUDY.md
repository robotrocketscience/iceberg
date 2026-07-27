# R-berth-plume-impingement — STUDY

**Round:** R-berth-plume-impingement. SCOPE pre-registered 2026-07-21 latest+25 (commit `8c38ff1`) before `run.py` existed.
**Worker:** worktree-115637 session. Project-owner-directed: the **pivot** of the momentum-management trade — "does thruster plume at the flexible-bag interface actually damage or re-perturb the bag?"
**One line:** Firing the onboard water cold-gas RCS to dump the ~5000 N·m·s berth injection is **not a mechanical or contamination showstopper** (pressure 3.6 orders below the aerogel limit; intake icing is grams over 50 berths), but re-perturbation is **geometry-conditioned**: benign with the bag in the plume backflow (boom ≥ 3 m), re-exciting (~22 % of the dump torque) if a dump axis forces the bag into the plume core. **Verdict: leg A (thruster dump) is viable under a thruster-placement / boom-length constraint — so the CMG (leg B) and precision-capture (leg C) drop from *mandatory* to *optional* worst-case-axis risk reduction.**

## Why this round was the pivot

`R-berth-momentum-management` (`b3b579c`) ranked the legs C < B < A but flagged that the whole ranking *inverts* on one unanswered question: leg A's only cost is "N plume firings at the bag," and whether that is acceptable was never quantified. If the plume damages the Vectran/aerogel or re-excites the just-settled slosh, legs C/B become **mandatory** and the ~300–600 kg CMG / days-scale cadence cost is real. This round resolves that pivot.

## Hypotheses, tests, results

All in `run.py` (deterministic closed form, parametrized plume model); numbers in `results/plume_findings.json`; figure `results/plume.png`.

### H1 [S] — Plume pressure ≪ structural limits: no fabric/aerogel damage — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| worst core pressure (F=10 N, r=2 m, κ=6) | < 100 Pa | **2.39 Pa** | yes |
| margin vs aerogel limit (10 kPa) | — | **4189× (3.6 orders)** | yes |

**Reading.** Even the worst-case plume core pressure at the closest standoff is 2.4 Pa against a conservative 10 kPa aerogel compressive limit (Vectran laminate is ~1000× stronger still, so aerogel is correctly the binding surface). No plausible plume-shape assumption closes a 3.6-order gap. **Mechanical damage is not a concern.**

### H2 [S] — Bag in backflow: plume torque ≪ dump torque (no re-excite); core geometry is the design constraint — **HELD (geometry-conditioned)**

| case | plume torque | vs 2.5 N·m threshold |
| --- | --- | --- |
| operating (backflow, r=3 m, β=1e-2) | **0.22 N·m** | 1/11 of threshold, 1/250 of dump ✓ |
| stress corner (backflow, r=2 m, β=3e-2, F=10) | 2.98 N·m | marginally over ✗ |
| bag in **core** (r=2 m) | **10.9 N·m** | ~22 % of the 50 N·m dump → re-excites ✗ |

**Reading — the honest, non-collapsing result.** With the bag in the plume *backflow* (θ > 90°, achieved by the tangential-couple geometry of a momentum dump) and a standoff ≥ 3 m, the plume torque is 0.22 N·m — 1/250th of the dump torque — and does **not** re-excite the slosh/attitude we just spent 2–10 min settling. But two edges bite: the closest-standoff / highest-backflow stress corner (2.98 N·m) marginally exceeds the threshold, and if a dump axis forces the bag into the plume **core**, the torque reaches ~11 N·m (22 % of the dump) and **would** re-excite. So the finding is not "plume is harmless" but **"plume is harmless provided the momentum-dump thrusters are placed so the bag is in backflow and the grapple boom holds ≥ 3 m standoff."** Boom length becomes a real design parameter.

### H3 [S] — Cumulative water-ice on the aerogel intake over N berths is grams: no clog — **HELD**

| metric | predicted | measured | held? |
| --- | --- | --- | --- |
| central (β_m=1e-3, f=0.1, N=30) | < 500 g | **4.4 g (0.009 %)** | yes |
| stress corner (β_m=1e-2, f=0.2, N=50) | < 500 g | **291 g (0.58 %)** | yes |

**Reading.** Even the worst-case backflow deposition — highest backflow mass fraction, largest intake-subtended fraction, unity sticking, 50 berths — puts 291 g of water-ice on a 50 kg aerogel intake (0.58 %), below the 1 % clog threshold. Central case is 4 g. **Icing does not clog the soft-capture intake** (in backflow; the core case would multiply this 100–1000× and is covered by the H2 placement constraint).

### H4 [W] — Synthesis: the pivot resolves; momentum-management cost drops from mandatory to optional — **HELD**

**Reading.** H1 and H3 hold robustly; H2 holds at the operating point under a geometry constraint. Therefore **leg A (thruster dump) is viable** provided the 12-corner thruster layout is used so the bag sits in the plume backflow at ≥ 3 m standoff — a *placement/boom-length* constraint, not a physics wall. Consequently the CMG (leg B, +300–600 kg) and precision-capture (leg C) **drop from mandatory to optional** risk reduction, existing only to retire the residual worst-case-dump-axis geometry. **The trade does not fully collapse to "just fire the thrusters" — it resolves to: *fire the thrusters, place them for backflow, keep the boom ≥ 3 m, and hold C/B as the worst-axis backstop.*** That is the honest state: leg A is the default, the momentum-management hardware is no longer forced, and one geometry question (below) remains to fully close it.

## Revisit / bug-catch (mandatory)

- **Parametrized plume model, not DSMC.** Pressures use P ~ F/r² with a core-peaking κ and a backflow ratio β. Absolute Pa could shift with a rarefied-plume (DSMC) sim, but H1's 3.6-order margin survives any plausible κ, and the load-bearing H2/H4 conclusion is the *core-vs-backflow geometry distinction*, not the exact pressure — that is robust to the model.
- **The H2 stress corner exceeds threshold.** At r = 2 m with the highest backflow ratio and F = 10 N, backflow torque is 2.98 N·m > 2.5 N·m. Standoff ≥ 3 m (grapple-boom length) clears it. This is why the verdict carries an explicit boom-length constraint rather than declaring plume unconditionally safe.
- **Aerogel-retraction mitigation.** If the aerogel intake is stowed/retracted during the dump (it is only needed during capture, not during the post-capture settle/dump), even the core case is mechanically and contamination-safe. This is a cheap operational mitigation not required by the verdict but worth noting.
- **Sticking coefficient = 1 (worst case).** If the bag surface is above the water frost point during the dump, deposition → 0 and H3 is safer still; deep-Saturn-shadow (~90 K) justifies stick ≈ 1, so the round used the conservative value.
- **The worst-case-dump-axis question is answered qualitatively, not by a full geometry sweep.** Whether a backflow-keeping placement exists for *every* required dump axis (given the 12 fixed corner thrusters and the bag's fixed grapple position) needs an attitude-geometry sweep. Until that runs, the residual worst-axis risk is exactly what legs C/B retire — which is why H4 is [W] and the trade does not fully collapse.

## Cross-learning

- **To `R-berth-momentum-management` (`b3b579c`):** the A-vs-B-vs-C pivot is resolved in leg A's favor **under a placement/boom constraint.** The C < B < A ranking on plume/mass stands, but legs B and C are now **optional** (worst-axis risk reduction), not mandatory — the ~300–600 kg CMG is not forced. Corrections live forward.
- **To `vehicle/SATURN-SHIP-SPEC.md` (Open-Question #7):** the momentum-buffer gap is real but its resolution is now cheaper than a CMG — a **thruster-placement + boom-length (≥ 3 m) constraint** plus optionally retracting the aerogel intake during the dump. The 12-corner RCS layout must be checked against the required dump axes (named follow-on).
- **To design-axes 15 / REQUIREMENTS obj #4:** the demonstrator's berth rehearsal should measure not only the injected momentum and leg-C capture precision, but **the plume-geometry at the actual dump (is the bag in backflow?) and the re-perturbation it induces** — the number that decides whether any momentum-management *hardware* is needed.
- **Named follow-on (not run):** the attitude-geometry sweep — for each physically-required momentum-dump axis, does a backflow-keeping thruster subset exist given the fixed 12-corner layout and grapple position? That sweep fully closes (or re-opens) the trade; it is the last question standing.
