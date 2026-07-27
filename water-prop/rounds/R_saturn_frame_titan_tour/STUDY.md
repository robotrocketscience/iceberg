# R-saturn-frame-titan-tour — STUDY

**Round:** R-saturn-frame-titan-tour. SCOPE pre-registered 2026-07-22 latest+25 arc (commit `0089442`) before `run.py` existed.
**Worker:** worktree-115637 session. Project-owner-directed: chase the crack `R-ephemeris-departure-anchor` opened.
**One line:** A Saturn-centric moon-tour analysis (re-hosting trajectory-bot's flyby/Tisserand primitives) **closes the crack and confirms R186's Titan-lever revocation — now with a derived reason, not an asserted bound.** The spacecraft harvests at the B-ring, which Tisserand-fixes its Titan-relative excess at v∞_T = 3.34 km/s (reproducing R186's ~3.3 from first principles); Titan flybys conserve v∞_T, so the best Saturn-system departure excess is Titan's **4.15 km/s < the 5.44 km/s requirement**, and the inner moons are too small (turn < 1°/flyby) to pump v∞_T. Reaching the v∞_T = 4 threshold needs propulsion — i.e. supplying the departure energy the tour was meant to save.

## The crack, and why it mattered

`R-ephemeris-departure-anchor` showed R186's Titan revocation is *conditional*: a Titan pump reaches the 5.44 km/s heliocentric departure requirement if the Titan-relative excess v∞_T ≥ 4.01 km/s. Since that revocation sets the **155–175 kWe reactor floor** — which feeds bet #3, the program's hardest gate — a re-open would be material: the dead 117 kWe Titan branch would return. This round settles whether a real Saturn-system tour can reach v∞_T ≥ 4 (and point the excess correctly).

## Hypotheses, tests, results

All in `run.py` (deterministic Saturn-centric two-body + flyby primitives); numbers in `results/tour_findings.json`; figure `results/tour.png`.

### H1 [S] — v∞_T reachable from the B-ring is ~3.3 km/s (Tisserand-fixed), not 4.0 — **HELD**

v∞_T from the minimal B-ring→Titan transfer = **3.34 km/s** (predicted [3.0, 3.6]). **Reading.** The spacecraft harvests at the B-ring (r ≈ 107,000 km, deep inside Titan's 1.22×10⁶ km orbit). The minimal transfer to Titan (periapsis at the B-ring, apoapsis at Titan) arrives tangentially at 2.24 km/s against Titan's 5.57 km/s, giving v∞_T = 3.34 km/s — **R186's ~3.3 km/s cap, now derived from the harvest geometry.** Because Titan flybys conserve |v∞_T|, this is a hard ceiling for Titan-only tours.

### H2 [S] — Best single-moon departure excess is Titan ~4.1 km/s < 5.44 — **HELD**

| moon | v∞ from B-ring | departure excess | v∞ needed for 5.44 | gap |
| --- | --- | --- | --- | --- |
| Tethys | 3.06 | **0.00** | 5.60 | +2.53 |
| Dione | 3.36 | **0.00** | 5.16 | +1.80 |
| Rhea | 3.55 | **0.99** | 4.69 | +1.13 |
| **Titan** | 3.34 | **4.15** | 4.00 | **+0.67** |
| Iapetus | 2.48 | **3.41** | 3.87 | +1.40 |

**Reading.** Titan gives the best departure excess (4.15 km/s) — it's the *sweet spot* balancing moon orbital speed against Saturn well depth. It is still 1.29 km/s short of the 5.44 km/s requirement, and closest of all moons (v∞ gap +0.67 km/s).

### H3 [S] — Every moon underprovides; inner moons and Iapetus are worse — **HELD**

Max departure excess over all moons = **4.15 km/s < 5.0**; every moon's v∞ gap > 0. **Reading.** Inner moons (Tethys, Dione) are so deep in Saturn's well that a pump from the B-ring-constrained v∞ can't even reach escape (excess 0.00); Rhea barely (0.99). Iapetus is far and slow (v_moon 3.26) so its absolute excess (3.41) is below Titan's. No moon and no single-moon choice reaches 5.44.

### H4 [W] — The v∞_T gap is unbridgeable without propulsion → R186 confirmed, crack closed — **HELD**

| moon | per-flyby turn δmax | can pump v∞_T? |
| --- | --- | --- |
| Tethys | 0.33° | no |
| Dione | 0.47° | no |
| Rhea | 0.79° | no |
| Titan | 21.2° | **but conserves v∞_T** |

**Reading — the decisive point.** Titan conserves v∞_T (it's the pump moon), so the only way to *grow* v∞_T from 3.34 to the needed 4.01 is a non-Titan handoff. But the inner moons turn the spacecraft **< 1°/flyby** (μ 41–154 km³/s² vs Titan's 8978) — far too weak to manufacture the 0.67 km/s v∞_T gap over any realistic tour. So reaching v∞_T = 4 requires a propulsive burn, which is precisely **supplying the departure energy the tour was meant to save** — R186's original conclusion, now derived. The crack is closed: the v∞_T = 4.01 threshold is real but unreachable from the harvest orbit.

## Revisit / bug-catch (mandatory)

- **Analytic Tisserand/δmax model, not a time-dependent beam search.** The single-moon departure-excess caps are *geometry* (not phasing) dependent, so a phased tour cannot exceed them; a full Saturn-frame beam search (re-hosting trajectory-bot's heliocentric tour code — a large build) would add tour *depth*, not raise the per-moon escape cap. It cannot beat Titan's 4.15 km/s. This is why the analytic version is decisive here.
- **Direction compounds the shortfall** (noted, not separately graded). The Titan-pumped Saturn-centric v∞ points in a flyby-geometry-constrained direction that must then add to Saturn's heliocentric velocity in the *retrograde* (sunward-dropping) sense for an Earth-return transfer. Even the 4.15 km/s magnitude pays a cosine penalty to point correctly — so **4.15 km/s is an optimistic upper bound** on the usable departure contribution; the true shortfall is worse.
- **v∞_T conservation is the crux.** Titan flybys conserve v∞_T, so the 3.34 arrival value is a hard Titan-only ceiling; non-Titan pumping needs the inner moons, which are shown too weak.
- **B-ring at r = 107,000 km** (campaign R_RING). A deeper harvest orbit gives marginally higher v∞_T at Titan but also a deeper well to climb; the Titan cap is insensitive at the ~0.1 km/s level.

## Cross-learning — the Titan/departure thread closes

- **To design-axes/04 & 05, and R186:** the crack `R-ephemeris-departure-anchor` opened is **closed**. R186's Titan-lever revocation is **confirmed, upgraded from an asserted magnitude bound to a derived Saturn-frame result** — the reachable Titan-pump departure excess from the B-ring harvest orbit is 4.15 km/s (v∞_T-limited to 3.34), short of the 5.44 km/s requirement; the inner moons can't pump v∞_T; and manufacturing the gap propulsively defeats the purpose. **The 155–175 kWe reactor floor and bet #3 stand; the 117 kWe Titan branch stays dead.**
- **Methodology note:** the ephemeris round (real Horizons) and this round (Saturn-frame Tisserand) together demonstrate the value of the trajectory-bot cross-application — the first opened a conditional crack in a load-bearing claim; the second closed it with the moon-system physics. A claim that was an *assertion* in R186 is now *derived* twice over.
- **What this did NOT need:** a full Saturn-frame tour optimizer (the analytic caps are decisive). That named follow-on is now **de-prioritized** — it would only confirm the same escape caps at greater tour depth.
- **Remaining trajectory follow-ons (unchanged):** lunar-GA Earth-arrival check of R12's 7.3→4.2 km/s; low-thrust spiral departure with an Isp model. Neither bears on the (now-closed) Titan question.
