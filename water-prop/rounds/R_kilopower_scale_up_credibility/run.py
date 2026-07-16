"""R-kilopower-scale-up-credibility — run.py

Two independent computations, both deterministic (no Monte Carlo; the
programmatic posterior reuses hyperion R-power-bayesian-update's already-run
three-prior bracket as a fixed input rather than re-simulating it):

  STEP 4 (mass-budget feedback): re-run titan-3 R-chunk-size-pareto's exact
    closure formula across a fine sweep of *effective system specific power*
    to find the sp threshold at which the closure cell collapses on the
    L0-09 floor, the L0-05 strict round-trip, and the L0-05 waiver round-trip.
    This answers H2 / H3: does a Path-B parallel-module specific-power penalty
    collapse the cell?

  STEP 3 (programmatic-credibility conjunction): take the heritage
    P(any United States fission orbit by 2035) bracket
    {uniform 0.089, Jeffreys 0.049, skeptical 0.029} from
    R-power-bayesian-update and condition it on the path-specific delivery
    requirements the titan-3 cell actually needs:
      (i)  power class >= 30 kilowatt-electric
      (ii) cumulative full-power lifetime >= the cell's own burn time (~6-8 yr)
      (iii) the *specific architecture* of the path is the one that flies
    This answers H1 / H4 / H5: what is the joint posterior that any path
    delivers inside the 2032-2035 demonstrator window, and is any path
    defensibly "Kilopower-extrapolation" under the locked-memory directive?

The titan-3 closure constants and m_dry / evaluate formulas are copied
verbatim from water-prop/rounds/R_chunk_size_pareto/run.py (cited in
SCOPE.md as the input this round must use, not re-derive). The only change
is sweeping sp_w_per_kg as a free variable instead of {2.4, 10.0}.
"""

import json
import math
import pathlib

# ---------------------------------------------------------------------------
# titan-3 R-chunk-size-pareto constants (verbatim) ---------------------------
# ---------------------------------------------------------------------------
G0 = 9.80665
ISP_ELECTRIC_S = 2000.0
V_ELECTRIC = ISP_ELECTRIC_S * G0          # 19613.3 m/s exhaust velocity

DV_INBOUND_RESIDUAL_MPS = 4470.0          # residual after 10-flyby lunar gravity assist
LUNAR_PHASING_YR = 0.725                   # 8.7 months

OUTBOUND_YR = 6.0
SATURN_SIDE_YR = 1.0
HOHMANN_INBOUND_YR = 6.09

L0_05_STRICT_YR = 15.0
L0_05_WAIVER_YR = 25.0
L0_09_FLOOR_T = 30.0

M_BUS_T = 5.5
M_THRUSTER_KG_PER_KW = 10.0                # 0.01 t/kW
M_BAG_LINEAR_FRAC = 0.05                    # 5% of chunk
ETA_THRUSTER = 0.5                          # electric -> jet conversion efficiency

SEC_PER_YEAR = 365.25 * 24 * 3600

HERE = pathlib.Path(__file__).parent
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)


def m_dry(chunk_t, P_kw, sp_w_per_kg):
    """titan-3 m_dry, verbatim. Pure-electric stack: no chemical engine,
    no electrolyser, no big tank."""
    m_bag = max(0.5, M_BAG_LINEAR_FRAC * chunk_t)
    m_reactor = P_kw * 1000.0 / sp_w_per_kg / 1000.0      # tonnes
    m_thrusters = M_THRUSTER_KG_PER_KW * P_kw / 1000.0
    return M_BUS_T + m_bag + m_reactor + m_thrusters


def evaluate(chunk_t, P_kw, sp_w_per_kg):
    """titan-3 evaluate, verbatim. Returns the closure record for one cell."""
    md = m_dry(chunk_t, P_kw, sp_w_per_kg)
    m_initial_t = md + chunk_t
    propellant_t = m_initial_t * (1.0 - math.exp(-DV_INBOUND_RESIDUAL_MPS / V_ELECTRIC))
    m_after_t = m_initial_t - propellant_t
    delivered_t = max(0.0, m_after_t - md)

    e_jet_J = 0.5 * (propellant_t * 1000.0) * V_ELECTRIC ** 2
    e_elec_J = e_jet_J / ETA_THRUSTER
    t_burn_s = e_elec_J / (P_kw * 1000.0)
    t_burn_yr = t_burn_s / SEC_PER_YEAR

    inbound_tof_yr = max(HOHMANN_INBOUND_YR, t_burn_yr) + LUNAR_PHASING_YR
    round_trip_yr = OUTBOUND_YR + SATURN_SIDE_YR + inbound_tof_yr
    return {
        "chunk_t": chunk_t, "P_kw": P_kw, "sp_w_per_kg": sp_w_per_kg,
        "m_dry_t": md, "m_reactor_t": P_kw / sp_w_per_kg,
        "m_initial_t": m_initial_t, "propellant_t": propellant_t,
        "delivered_t": delivered_t, "t_burn_yr": t_burn_yr,
        "round_trip_yr": round_trip_yr,
        "meets_floor": delivered_t >= L0_09_FLOOR_T,
        "closes_strict": round_trip_yr <= L0_05_STRICT_YR and delivered_t >= L0_09_FLOOR_T,
        "closes_waiver": round_trip_yr <= L0_05_WAIVER_YR and delivered_t >= L0_09_FLOOR_T,
    }


# ---------------------------------------------------------------------------
# STEP 4 — mass-budget feedback: cell-collapse vs effective specific power ---
# ---------------------------------------------------------------------------
def mass_budget_feedback():
    """Sweep effective specific power finely at titan-3's two closing chunk
    sizes (50, 60 t) at P=30 kWe and find the collapse thresholds."""
    sp_grid = [round(0.1 * i, 2) for i in range(2, 121)]   # 0.2 .. 12.0 W/kg
    out = {}
    for chunk in (50.0, 60.0):
        rows = [evaluate(chunk, 30.0, sp) for sp in sp_grid]
        # Lowest sp that still satisfies each closure mode (sweep is monotone:
        # higher sp -> lighter reactor -> easier closure).
        def lowest_sp(key):
            passing = [r["sp_w_per_kg"] for r in rows if r[key]]
            return min(passing) if passing else None
        out[f"chunk_{int(chunk)}t"] = {
            "anchor_2p4": evaluate(chunk, 30.0, 2.4),
            "anchor_1p0": evaluate(chunk, 30.0, 1.0),
            "lowest_sp_meets_floor": lowest_sp("meets_floor"),
            "lowest_sp_closes_strict": lowest_sp("closes_strict"),
            "lowest_sp_closes_waiver": lowest_sp("closes_waiver"),
            # Full per-sp sweep is regenerable from run.py; not persisted to
            # keep the committed artifact small (no large results files).
            "sweep_sp_grid": [sp_grid[0], sp_grid[-1], len(sp_grid)],
        }
    return out


# ---------------------------------------------------------------------------
# STEP 3 — programmatic-credibility conjunction posterior --------------------
# ---------------------------------------------------------------------------
# Heritage input: hyperion R-power-bayesian-update three-prior bracket on
# P(any United States fission reactor reaches orbit by 2035). These are the
# already-run posteriors; this round does NOT re-simulate them.
P_ORBIT_BY_2035 = {"uniform": 0.089, "jeffreys": 0.049, "skeptical": 0.029}

# Conditional factors, given a United States fission reactor reaches orbit in
# the window. Each is a credibility weight in [0, 1] with documented rationale
# in STUDY.md. They are deliberately *generous-to-the-architecture* (high end
# of defensible) so the resulting posterior is an upper bound, per lesson 7
# (compute under the most pessimistic credible anchor first -> here we instead
# bound from ABOVE to show even the charitable case is sub-threshold).
#
#   p_power   = P(the orbited reactor is >= 30 kWe | orbit)
#   p_life    = P(it sustains the cell's ~6-8 yr cumulative full-power burn
#               | orbit)  -- KRUSTY flew 28 hr; Kilopower 10-yr life is a
#               design target, never demonstrated.
#   p_arch    = P(the *specific path architecture* is the one that flies
#               | a >=30 kWe reactor orbits) -- Path A (single large core) is
#               the funded direction (Fission Surface Power); Path B (parallel
#               Kilopower modules) is nobody's funded plan; Path C is between.
PATHS = {
    "A_single_30kwe": {
        "label": "Single 30 kWe core (Fission-Surface-Power-class scale-up)",
        "kilopower_extrapolation": False,   # this is FSP-Phase-1-class, not Kilopower
        "p_power": 0.60,    # 30 kWe sits just below FSP Phase-1 40 kWe scope; prospective
                            # scope distribution per iapetus lesson 12 favours <100 kWe
        "p_life": 0.40,     # 10-yr design target exists; never demonstrated past 28 hr
        "p_arch": 0.70,     # single large core IS the funded direction
    },
    "B_parallel_30x1kwe": {
        "label": "30x parallel 1 kWe Kilopower modules",
        "kilopower_extrapolation": True,    # literally Kilopower-class modules
        "p_power": 0.60,    # same orbit->power-class conditional
        "p_life": 0.40,     # same lifetime gap
        "p_arch": 0.07,     # no funded program pursues a parallel-module power plant
    },
    "C_intermediate": {
        "label": "Intermediate N x k = 30 (e.g. 3 x 10 kWe)",
        "kilopower_extrapolation": None,    # project-owner call: partial
        "p_power": 0.60,
        "p_life": 0.40,
        "p_arch": 0.20,     # interpolated between A and B
    },
}


def programmatic_posterior():
    out = {}
    for pid, p in PATHS.items():
        rows = {}
        for prior, p_orbit in P_ORBIT_BY_2035.items():
            joint = p_orbit * p["p_power"] * p["p_life"] * p["p_arch"]
            rows[prior] = joint
        out[pid] = {
            "label": p["label"],
            "kilopower_extrapolation": p["kilopower_extrapolation"],
            "conditionals": {"p_power": p["p_power"], "p_life": p["p_life"],
                             "p_arch": p["p_arch"]},
            "joint_posterior": rows,
        }
    return out


def main():
    mb = mass_budget_feedback()
    pp = programmatic_posterior()

    summary = {
        "round": "R-kilopower-scale-up-credibility",
        "worker": "hyperion",
        "date": "2026-05-22",
        "heritage_inputs": {
            "P_orbit_by_2035": P_ORBIT_BY_2035,
            "source": "hyperion R-power-bayesian-update results/R_power_bayesian_update_summary.json",
            "titan3_closure_formula": "water-prop/rounds/R_chunk_size_pareto/run.py (verbatim)",
        },
        "step4_mass_budget_feedback": mb,
        "step3_programmatic_posterior": pp,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2))

    # Human-readable console digest.
    print("=" * 72)
    print("STEP 4 — mass-budget feedback (titan-3 cell, P=30 kWe)")
    print("=" * 72)
    for cell, d in mb.items():
        a = d["anchor_2p4"]
        print(f"\n{cell}: at KRUSTY-measured sp=2.4 W/kg -> "
              f"reactor={a['m_reactor_t']:.1f}t dry={a['m_dry_t']:.1f}t "
              f"delivered={a['delivered_t']:.1f}t RT={a['round_trip_yr']:.2f}yr "
              f"strict={a['closes_strict']} waiver={a['closes_waiver']}")
        print(f"   lowest sp meeting L0-09 floor (30 t): {d['lowest_sp_meets_floor']} W/kg")
        print(f"   lowest sp closing L0-05 strict (15 yr): {d['lowest_sp_closes_strict']} W/kg")
        print(f"   lowest sp closing L0-05 waiver (25 yr): {d['lowest_sp_closes_waiver']} W/kg")

    print("\n" + "=" * 72)
    print("STEP 3 — programmatic joint posterior P(path delivers by 2035)")
    print("=" * 72)
    print(f"{'path':<22}{'kilopower?':<12}{'uniform':>10}{'jeffreys':>10}{'skeptical':>11}")
    for pid, d in pp.items():
        jp = d["joint_posterior"]
        ke = {True: "yes", False: "no", None: "owner-call"}[d["kilopower_extrapolation"]]
        print(f"{pid:<22}{ke:<12}{jp['uniform']*100:>9.3f}%{jp['jeffreys']*100:>9.3f}%"
              f"{jp['skeptical']*100:>10.3f}%")
    print(f"\nWrote {RESULTS / 'summary.json'}")


if __name__ == "__main__":
    main()
