# R-saturn-frame-titan-tour — can a Saturn-system tour re-open the Titan departure lever?

**Status:** SCOPE pre-registered 2026-07-22 (latest+25 arc), before `run.py` was written or executed.
**Worker:** worktree-115637 session. Project-owner-directed: chase the crack `R-ephemeris-departure-anchor` opened.
**Predecessors:** `R-ephemeris-departure-anchor` (`5e13121`) — showed R186's Titan-pump revocation is *conditional*: the Saturn-centric departure excess reaches the 5.44 km/s heliocentric requirement at Titan-relative excess v∞_T ≥ 4.01 km/s. `R_titan_tour_ephemeris` (R186, `623d779`) — revoked the lever via a magnitude bound (~3.3 km/s). `design-axes/04, 05` — the revocation sets the 155-175 kWe reactor floor (bet #3).
**Toolkit source:** `~/projects/trajectory-bot` — flyby-as-bounded-v∞-rotation and δmax primitives (`tisserand_3d.py`, `flyby_leverage.py`), re-hosted here in a Saturn-centric frame.

## The question and what would flip it

R186 revoked the Titan departure-pump lever; the ephemeris round showed that revocation is conditional — it holds only if the spacecraft's Titan-relative excess v∞_T stays ≲ 3.5 km/s (at v∞_T ≥ 4.01 a Titan pump *would* supply the 5.44 km/s departure requirement). **If a patient multi-flyby Saturn-system tour can actually reach v∞_T ≥ 4 at Titan — and point the pumped excess in the required retrograde-heliocentric departure direction — then R186's revocation is (partially) wrong and the Titan reactor-floor branch (117 kWe) goes back on the table.** This round settles it in a Saturn-centric frame.

**The decisive physics:** v∞_T (spacecraft velocity relative to a moon at its orbit) is **conserved by that moon's flybys** (Tisserand) — flybys *rotate* v∞, they do not grow |v∞|. So v∞_T is fixed by the *arrival orbit*. The spacecraft harvests at the B-ring (r ≈ 107,000 km, deep inside Titan's 1.22×10⁶ km orbit); the minimal transfer from the B-ring to a moon fixes the arrival v∞ at that moon. Growing v∞_T beyond that requires either propellant (= supplying the departure energy yourself, R186's point) or a non-Titan handoff — and the inner moons are too small to turn the spacecraft.

## Boundary

- **IN:** v∞ relative to each major moon (Titan, Rhea, Dione, Tethys, Iapetus) on the minimal B-ring→moon transfer; the max Saturn-centric departure excess from a single-moon prograde pump; per-flyby turn (δmax) at each moon (whether inner-moon handoffs can pump v∞_T); the v∞_T needed at each moon to reach 5.44 vs what the B-ring provides; the pumped-v∞ direction constraint (qualitative).
- **OUT:** a full time-dependent Saturn-frame beam-search tour (this is the analytic Tisserand/δmax version — trajectory-bot's full tour SEARCH is heliocentric and would need a large re-host); the Saturn-centric Oberth escape burn detail (R179); moon ephemeris phasing (the caps are geometry, not phasing, dependent); disposal via Titan (axis 20 — different, and R190 already covered).

## Pre-registered hypotheses (numeric, falsifiable, written before the run)

**H1 [S] — v∞_T reachable from the B-ring is ~3.3 km/s (Tisserand-fixed), not the 4.0 the threshold needs.** Minimal B-ring→Titan transfer (periapsis at B-ring, apoapsis at Titan, tangential at apoapsis) → v∞_T = v_Titan − v_sc,apo. **SCOPE:** v∞_T from B-ring ∈ [3.0, 3.6] km/s (reproduces R186's ~3.3 from first principles). **Falsified** if v∞_T from B-ring ≥ 4.0 (crack would be real).

**H2 [S] — Best single-moon departure excess is Titan ~4.1 km/s < 5.44.** Departure excess = √((v_moon+v∞_moon)² − 2μ_S/a_moon). **SCOPE:** best single-moon excess ∈ [3.8, 4.5] km/s < 5.44 (Titan is the sweet spot — balances moon speed against well depth). **Falsified** if any single moon reaches 5.44.

**H3 [S] — Inner moons and Iapetus are worse, not better; every moon needs more v∞ than the B-ring provides.** Inner moons (Rhea/Dione/Tethys) are deeper → need more to escape; Iapetus is far/slow → lower absolute excess. **SCOPE:** max over all moons < 5.0 km/s; at every moon the v∞ needed to reach 5.44 exceeds the B-ring-provided v∞ (Titan closest, short by ~0.67 km/s). **Falsified** if any moon reaches 5.44.

**H4 [W] — The v∞_T gap is unbridgeable without propulsion → R186 revocation confirmed, crack closed.** Titan flybys conserve v∞_T; only a non-Titan handoff could pump it, but the inner moons turn the spacecraft < 1°/flyby (μ too small). **SCOPE:** best reachable departure excess < 5.44 AND inner-moon per-flyby turn < 2° (cannot pump v∞_T); so the 0.67 km/s v∞_T gap requires a burn = supplying the departure energy yourself. **Falsified** if a reachable, correctly-directed tour hits 5.44.

**Honest expected reading:** all four hold → **the crack the ephemeris round opened is closed, and R186's revocation is confirmed — now with a derived Saturn-frame reason rather than an asserted bound.** The v∞_T = 4 threshold is real but unreachable from the harvest orbit: the B-ring fixes v∞_T at ~3.3, Titan conserves it, the inner moons are too small to pump it, and manufacturing the gap propulsively is just supplying the departure energy the tour was meant to save. If instead a moon or handoff reaches 5.44, the reactor-floor argument's Titan branch reopens — a material result either way.

## Method

Closed-form Saturn-centric two-body + flyby primitives, deterministic. `run.py`:

- **Moon set:** Titan (a=1.22×10⁶ km, μ=8978.14, R=2574.7 — from trajectory-bot tisserand_3d), Rhea, Dione, Tethys, Iapetus (standard JPL/IAU a/μ/R). μ_S=3.793×10⁷ km³/s², B-ring r=107,000 km.
- **Arrival v∞:** minimal B-ring→moon transfer, v∞_moon = v_circ(a) − v_sc,apo.
- **Departure excess:** √((v_moon+v∞_moon)² − 2μ_S/a_moon).
- **v∞-to-5.44:** invert the excess formula per moon; compare to B-ring-provided v∞.
- **Handoff pumping:** δmax = 2·arcsin(1/(1+r_p·v∞²/μ_moon)) per moon (peri alt {500,1000,2000} km); show inner-moon δmax ≪ Titan's.
- **Direction (qualitative):** the Titan-pumped v∞ direction vs the required retrograde-heliocentric departure — a compounding penalty noted in the reading.

**Anchors:** μ_S=3.793e7 km³/s² (R179), Titan constants from trajectory-bot; requirement 5.44 km/s (from `R-ephemeris-departure-anchor`); B-ring 107,000 km (campaign R_RING).
