"""R-departure-anchor-resolution — Δv(a) from B-ring residence to hyperbolic escape.

Planar two-body Saturn, tangential constant thrust acceleration, RK4 with
orbital-timescale-adaptive step. See STUDY.md for pre-registration.

Run from repo root:
  water-prop/.venv/bin/python water-prop/rounds/R_departure_anchor_resolution/run.py

Writes results/dv_vs_accel.json (small, committed).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

GM = 3.7931e7 * 1e9          # Saturn GM, m^3/s^2
R0 = 100_000e3               # B-ring residence radius, m
VINF = 5.44e3                # target hyperbolic excess, m/s (titan-2 anchor)
E_TARGET = 0.5 * VINF ** 2   # specific orbital energy target, J/kg

V_CIRC = math.sqrt(GM / R0)  # 19,475 m/s
R_SOI = 5.45e10              # Saturn sphere of influence, m; beyond it the
                             # field-free residual dv = v_inf_target - v is exact
                             # to two-body fidelity


def accel(state, a_thrust):
    x, y, vx, vy = state
    r = math.hypot(x, y)
    v = math.hypot(vx, vy)
    g = -GM / r**3
    ux, uy = (vx / v, vy / v) if v > 0 else (0.0, 1.0)
    return (vx, vy, g * x + a_thrust * ux, g * y + a_thrust * uy)


def rk4_step(state, dt, a_thrust):
    k1 = accel(state, a_thrust)
    s2 = tuple(state[i] + 0.5 * dt * k1[i] for i in range(4))
    k2 = accel(s2, a_thrust)
    s3 = tuple(state[i] + 0.5 * dt * k2[i] for i in range(4))
    k3 = accel(s3, a_thrust)
    s4 = tuple(state[i] + dt * k3[i] for i in range(4))
    k4 = accel(s4, a_thrust)
    return tuple(state[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                 for i in range(4))


def integrate(a_thrust, dt_frac=1.0 / 200.0, dt_cap=2000.0):
    """Thrust tangentially from circular orbit until E >= E_TARGET or r > SOI.

    If the SOI is reached below the target energy, the residual Δv is added in
    the field-free limit (dv = v_inf_target − v_current, exact far from the
    planet). Returns (dv_km_s, dv_escape_km_s, thrust_years, revolutions).
    """
    state = (R0, 0.0, 0.0, V_CIRC)
    t = 0.0
    theta_acc = 0.0
    prev_angle = 0.0
    dv_escape = None
    residual = 0.0
    while True:
        x, y, vx, vy = state
        r = math.hypot(x, y)
        v = math.hypot(vx, vy)
        energy = 0.5 * v**2 - GM / r
        if dv_escape is None and energy >= 0.0:
            dv_escape = a_thrust * t
        if energy >= E_TARGET:
            break
        if r > R_SOI:
            v_now = math.sqrt(max(2.0 * energy, 0.0))
            residual = max(0.0, VINF - v_now)
            break
        period_local = 2 * math.pi * math.sqrt(r**3 / GM)
        dt = min(dt_cap, dt_frac * period_local)
        state = rk4_step(state, dt, a_thrust)
        angle = math.atan2(state[1], state[0])
        d = angle - prev_angle
        if d < -math.pi:
            d += 2 * math.pi
        elif d > math.pi:
            d -= 2 * math.pi
        theta_acc += abs(d)
        prev_angle = angle
        t += dt
    dv = a_thrust * t + residual
    if dv_escape is None:
        dv_escape = a_thrust * t
    return (dv / 1000.0, dv_escape / 1000.0,
            (t + residual / a_thrust) / (365.25 * 86400.0),
            theta_acc / (2 * math.pi))


def impulsive_reference():
    """Single periapsis burn from circular r0 to v_inf (Oberth)."""
    v_hyp = math.sqrt(VINF**2 + 2 * GM / R0)
    return (v_hyp - V_CIRC) / 1000.0


def main():
    rows = {}
    print(f"v_circ(r0) = {V_CIRC/1000:.2f} km/s; impulsive Oberth reference = "
          f"{impulsive_reference():.2f} km/s; target v_inf = {VINF/1000:.2f} km/s")
    for a in (1e-5, 3e-5, 1e-4, 1e-3, 1e-2, 1e-1):
        dv, dv_esc, yrs, revs = integrate(a)
        rows[f"{a:.0e}"] = {"dv_km_s": round(dv, 2),
                            "dv_escape_km_s": round(dv_esc, 2),
                            "thrust_years": round(yrs, 2),
                            "revolutions": round(revs, 1)}
        print(f"a = {a:.0e} m/s^2 : dv = {dv:6.2f} km/s (escape {dv_esc:6.2f})  "
              f"thrust time = {yrs:8.2f} yr  revs = {revs:8.1f}")
    out = {
        "model": "planar two-body Saturn, tangential constant-a, RK4, "
                 "dt = period/200 capped 2000 s",
        "r0_km": R0 / 1000, "v_circ_km_s": round(V_CIRC / 1000, 2),
        "v_inf_target_km_s": VINF / 1000,
        "impulsive_oberth_km_s": round(impulsive_reference(), 2),
        "edelbaum_escape_term_km_s": round(V_CIRC / 1000, 2),
        "dv_vs_accel": rows,
        "campaign_electric_accel_band_m_s2": [1.3e-5, 1.0e-4],
    }
    (HERE / "results").mkdir(exist_ok=True)
    with open(HERE / "results" / "dv_vs_accel.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/dv_vs_accel.json")


if __name__ == "__main__":
    main()
