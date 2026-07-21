# R-bag-dynamics-envelope — STUDY

**Round:** R-bag-dynamics-envelope. SCOPE pre-registered 2026-07-21. All four hypotheses **HELD**. The round does what it registered: it **bounds** the campaign's single largest unmodeled physics and shows exactly which part is desk-tractable and which part is not.

## Results vs registered hypotheses — all four HELD

### H1 — contact is not the problem — **HELD**

Peak capture force spans **0.1–6.3 kN** across berthing rates 0.01–0.1 m/s × soft-capture stiffness 10³–10⁵ N/m; the soft-capture region (v_c ≤ 0.05 m/s, k_c ≤ 10⁴ N/m) holds it **≤ 1 kN**, within a purpose-built berthing arm; arrest impulse 0.4–4 kN·s. The instantaneous contact mechanics are tractable and are **not** the risk driver — a slow, compliant capture keeps first contact benign.

### H2 — slosh overlaps the control bandwidth — **HELD**

First-mode slosh frequency spans **0.003–0.1 Hz** (T_s 10–300 s) and **overlaps a large spacecraft's ACS bandwidth (0.01–0.1 Hz) for all T_s ≲ 100 s** — most of the plausible range. A berthing controller and a sloshing 40 t load live in the same frequency band: control-structure interaction is the default, not the exception, unless the bag is engineered very floppy (T_s ≳ 150 s).

### H3 — mass-ratio dominance defeats wheel control — **HELD**

The bagged load is **10:1** against a relay bus and **2:1** against the monolithic ship — the sloshing half (20 t) exceeds a relay bus and equals a monolithic. Hub disturbance torque spans **1.8–1579 N·m**: it exceeds reaction-wheel authority (~5 N·m) for T_s ≲ 180 s and **exceeds even thruster authority (~50 N·m) for a stiff bag** (T_s ~10 s → 1.6 kN·m). Attitude cannot be held on wheels during berth; thruster control is forced, firing near the bag with its plume and contamination — the tail wags the dog.

### H4 — a narrow viable corner that prescribes unprecedented bag design — **HELD**

A comfortable design point **exists but is narrow**: **7 % of the T_s × ζ grid** is both reaction-wheel-controllable and settles inside a 30-min berth window (**34 %** if thrusters are allowed). That corner sits at **high T_s (≳ 180 s, off the ACS band, low torque) with high damping (ζ ≳ 0.06, to settle in time)** — it prescribes a specific 40 t space-bag (moderate-to-soft membrane compliance *and* baffled or actively-damped slosh) that **has no flight precedent at this scale**. Outside it, at least one of {CSI overlap, thruster-exceeding torque, over-window settling} bites. The desk model **locates** the corner but **cannot verify coupled stability inside it** — that requires the named Basilisk 6-DOF sim. This envelope **explains R185's low berth_bag stage probability (0.88–0.95) and R189's berth-driven mothership threat from first principles**, rather than from desk anchor.

## Bug-catch (protocol §bug-catch)

1. **Registration rounding blemish (documented):** SCOPE H1 quoted the envelope max as "6.3 kN"; the exact value is **6.32 kN** (v_c 0.1 m/s, k_c 10⁵ N/m). The registered *falsification* criterion (any soft-capture corner > 10 kN) is unaffected; the run.py check was aligned to that criterion, not the rounded descriptive figure. Corrections live forward — SCOPE not retro-edited.
2. **Grid-resolution note:** the viable-corner fraction is 7 % on the run.py 60×40 grid vs 9 % on the pre-script's 25×15 grid — both inside the registered "narrow, ~10 %, < 50 %" band; the finer grid is reported.

## Revisit (mandatory)

This is a **lumped, decoupled** model and its limits are the whole point: (1) it treats contact and slosh as separable and linear; the real problem is their **coupling** to the 6-DOF attitude loop, which a scalar model cannot represent. (2) The slosh restoring stiffness in microgravity is dominated by bag-membrane mechanics with **no anchor** — T_s is swept 10–300 s because nobody has measured it; the whole envelope rides on that guess. (3) First-mode mass fraction 0.5, amplitude 0.1 m, offset 2 m, damping 0.01–0.1 are all order-of-magnitude desk anchors. (4) Multi-mode slosh, bag wrinkling/collapse, ice-vs-liquid phase (a partially-frozen chunk behaves very differently), and thermal state are all unmodeled. (5) The berth window (30 min) is a stand-in. **The honest verdict: the desk study can bound the envelope and locate a narrow viable corner, but the campaign cannot close bag dynamics without simulation.**

## Cross-learning

- **For the risk register (matrix):** bag dynamics is **the one desk-irreducible unknown** in the campaign. Envelope bounded — contact tractable; the hazard is the coupled attitude dynamics of a **host-dominating sloshing mass** (2:1–10:1), with slosh in the ACS band, torque beyond wheel authority, and a **narrow (~7 %) viable design corner** that prescribes an unprecedented bag. This grounds R185's berth_bag probability and R189's mothership threat in physics.
- **Named simulation follow-on (the way to close it):** a Basilisk 6-DOF scenario with `linearSpringMassDamper` slosh particles representing the bagged water, coupled to the mothership hub and its ACS, sweeping T_s × ζ × berthing-rate to test **closed-loop stability and settling** inside the H4 corner. Requires standing up `water-prop/.venv-bsk` and a new `water-prop/sims/bag_berthing/`. This is the single highest-value simulation in the campaign's backlog.
- **For the demonstrator:** the LEO handoff-rehearsal gate (R185/R189) gains **bag-slosh characterization** as an explicit objective — measure T_s and ζ of a real bagged multi-tonne load, the two numbers this entire envelope rides on.
- **Follow-ons:** the Basilisk berthing sim (above); an ice-vs-liquid phase round (a frozen chunk changes the slosh model entirely); a bag-membrane mechanics round to anchor T_s.
