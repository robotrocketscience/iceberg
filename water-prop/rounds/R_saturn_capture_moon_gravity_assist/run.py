"""Saturn capture via moon gravity assists — patched-conic analysis.

Adapted from R2_lunar_gravity_assist_trajectory. Each moon flyby is treated
as an instantaneous velocity rotation in the moon-centered frame. Saturn-
frame energy change is computed by transforming back to the Saturn frame.

Five sweeps map to the five pre-registered hypotheses in STUDY.md.

Outputs:
  results/single_titan_flyby.csv          — H1
  results/all_moons_single_flyby.csv      — H3
  results/multi_titan_tour.csv            — H2
  results/apoapsis_sweep.csv              — H5
  results/iapetus_then_titan.csv          — H4
  results/*.png                           — companion plots
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from horizons_fetch import fetch_all

# -----------------------------------------------------------------------------
# Physical constants
# -----------------------------------------------------------------------------

GM_SATURN = 37931207.7  # km^3 / s^2  (Jacobson 2006 / NASA Saturn fact sheet)

# Moon gravitational parameters (km^3 / s^2) from JPL Saturn satellite ephem
# SAT441 (consistent with Horizons CENTER='500@6' source).
GM_MOONS = {
    "Mimas":     2.503,
    "Enceladus": 7.211,
    "Tethys":    41.21,
    "Dione":     73.116,
    "Rhea":      153.94,
    "Titan":     8978.14,
    "Hyperion":  0.3727,
    "Iapetus":   120.50,
    "Phoebe":    0.5532,
}

# Mean radii [km] — for the flyby-altitude minimum (don't fly through the moon).
MOON_RADII = {
    "Mimas":     198,
    "Enceladus": 252,
    "Tethys":    533,
    "Dione":     561,
    "Rhea":      764,
    "Titan":     2575,
    "Hyperion":  135,
    "Iapetus":   735,
    "Phoebe":    107,
}

# Sphere-of-influence radii [km] — approx, r_moon * (M_moon/M_saturn)^(2/5).
# Important: flybys must occur INSIDE the sphere-of-influence for the
# patched-conic approximation to hold.
def soi_radius(moon: str, moon_radius_from_saturn_km: float) -> float:
    return moon_radius_from_saturn_km * (GM_MOONS[moon] / GM_SATURN) ** 0.4


@dataclass
class MoonState:
    name: str
    r_km: float      # distance from Saturn at the analysis epoch
    v_kms: float     # speed in Saturn frame at the analysis epoch
    mu_kms2: float   # gravitational parameter
    radius_km: float  # mean physical radius

    @property
    def soi_km(self) -> float:
        return soi_radius(self.name, self.r_km)


def load_moon_states(epoch: str = "2045-01-01") -> dict[str, MoonState]:
    raw = fetch_all(epoch=epoch)
    out = {}
    for name, data in raw.items():
        out[name] = MoonState(
            name=name,
            r_km=data["r_km"],
            v_kms=data["v_kms"],
            mu_kms2=GM_MOONS[name],
            radius_km=MOON_RADII[name],
        )
    return out


# -----------------------------------------------------------------------------
# Patched-conic physics
# -----------------------------------------------------------------------------

def sc_speed_in_saturn_frame(v_inf_at_saturn_kms: float, r_km: float) -> float:
    """Vis-viva: spacecraft speed at distance r on a hyperbolic Saturn approach."""
    return float(np.sqrt(v_inf_at_saturn_kms ** 2 + 2 * GM_SATURN / r_km))


def turning_angle(v_inf_moon_kms: float, periapsis_radius_moon_km: float, mu_moon: float) -> float:
    """Patched-conic turning angle [rad] for a hyperbolic flyby."""
    e = 1.0 + periapsis_radius_moon_km * v_inf_moon_kms ** 2 / mu_moon
    return 2.0 * np.arcsin(1.0 / e)


def best_capture_dv_single_flyby(
    moon: MoonState,
    v_inf_saturn_kms: float,
    flyby_altitude_km: float,
) -> dict:
    """Compute the Saturn-frame Δv saved by an optimal-geometry flyby of `moon`.

    Sign convention: positive `dv_saturn_frame_kms` means the spacecraft has
    lost kinetic energy relative to Saturn (good for capture).

    Geometry: spacecraft on a hyperbolic Saturn approach intercepts the moon at
    its orbital radius. We resolve the encounter-frame velocities (assume the
    spacecraft and moon orbital planes coincide — the 2D leading-order case),
    compute the moon-frame v_inf, apply the optimal retrograde turn, and
    transform back.

    Returns dict with `dv_saturn_frame_kms`, `v_inf_moon_kms`, `turn_deg`,
    `v_inf_saturn_after_kms`, `bound_after`.
    """
    # spacecraft Saturn-frame speed at the moon's distance
    v_sc = sc_speed_in_saturn_frame(v_inf_saturn_kms, moon.r_km)
    v_moon = moon.v_kms

    # Optimal-geometry encounter: spacecraft is travelling tangentially with the
    # moon (so v_inf_moon is minimised → maximum turning). Choose the spacecraft
    # heading such that the prograde tangential component matches the moon's
    # heading. Then v_inf_moon = v_sc - v_moon (scalar, prograde encounter).
    # This minimises v_inf_moon and maximises the energy that can be shed.
    v_inf_moon = abs(v_sc - v_moon)

    # Pure retrograde turn: rotate v_inf_moon by `theta`, choose the sign so
    # the post-flyby tangential component decreases (energy is shed).
    rp = moon.radius_km + flyby_altitude_km
    theta = turning_angle(v_inf_moon, rp, moon.mu_kms2)

    # Post-flyby velocity components in moon frame:
    # incoming v_inf_moon aligned along +tangential (prograde encounter);
    # rotation in the encounter plane by theta with optimal sign (negative
    # tangential component after turn).
    vt_in = v_inf_moon
    vr_in = 0.0
    # Optimal turn: rotate by theta with negative-tangential bias.
    vt_out = vt_in * np.cos(theta) - vr_in * np.sin(theta)
    vr_out = vt_in * np.sin(theta) + vr_in * np.cos(theta)
    # The "optimal-for-energy-loss" choice picks the half-plane that puts the
    # post-flyby tangential component furthest below +tangential. Among the two
    # rotation directions, pick the one with smaller vt_out.
    vt_out_alt = vt_in * np.cos(-theta) - vr_in * np.sin(-theta)
    if abs(vt_out_alt) < abs(vt_out):
        vt_out = vt_out_alt
        vr_out = vt_in * np.sin(-theta) + vr_in * np.cos(-theta)

    # back to Saturn frame: spacecraft velocity = moon velocity + v_inf_moon (vec)
    vt_sc_after = v_moon + vt_out
    vr_sc_after = vr_out
    v_sc_after = float(np.sqrt(vt_sc_after ** 2 + vr_sc_after ** 2))

    # Saturn-frame energy change as an equivalent Δv at the moon's distance:
    # the spacecraft now has speed v_sc_after. Equivalent v_inf at infinity:
    e_specific_after = 0.5 * v_sc_after ** 2 - GM_SATURN / moon.r_km
    if e_specific_after < 0:
        v_inf_after = 0.0  # captured (energetically bound)
        bound_after = True
    else:
        v_inf_after = float(np.sqrt(2 * e_specific_after))
        bound_after = False

    # Δv saved at the eventual capture burn at low periapsis (vs paying the
    # full hyperbolic-excess tax). Use the hyperbolic-vs-elliptical capture
    # cost differential at a representative low periapsis = 4 Saturn radii
    # (60240 km, ring-clearing safe).
    r_p_burn = 4 * 60268.0  # 4 Saturn equatorial radii
    v_p_before = float(np.sqrt(v_inf_saturn_kms ** 2 + 2 * GM_SATURN / r_p_burn))
    v_p_after = float(np.sqrt(v_inf_after ** 2 + 2 * GM_SATURN / r_p_burn))
    dv_capture_saving = v_p_before - v_p_after

    return {
        "moon": moon.name,
        "v_inf_saturn_in_kms": v_inf_saturn_kms,
        "v_sc_at_moon_kms": v_sc,
        "v_inf_moon_kms": v_inf_moon,
        "flyby_altitude_km": flyby_altitude_km,
        "periapsis_km": rp,
        "soi_km": moon.soi_km,
        "in_soi": rp < moon.soi_km,
        "turn_deg": float(np.degrees(theta)),
        "v_sc_after_kms": v_sc_after,
        "v_inf_saturn_after_kms": v_inf_after,
        "dv_capture_saving_kms": dv_capture_saving,
        "bound_after": bound_after,
    }


def flyby_2d(
    v_sc: np.ndarray,
    v_moon: np.ndarray,
    rp_moon_km: float,
    mu_moon: float,
    mode: str = "decelerate",
) -> tuple[np.ndarray, float, float]:
    """Single moon flyby in 2D (orbital plane). Returns (v_sc_after, theta_deg, v_inf_moon).

    Try both in-plane rotation senses, pick the one matching `mode`:
      "decelerate" → minimize post-flyby Saturn-frame KE (best for capture pumping)
      "accelerate" → maximize it
    """
    v_inf_in = v_sc - v_moon
    v_inf_mag = float(np.linalg.norm(v_inf_in))
    if v_inf_mag < 1e-6:
        return v_sc.copy(), 0.0, 0.0
    e = 1.0 + rp_moon_km * v_inf_mag ** 2 / mu_moon
    theta = 2.0 * np.arcsin(1.0 / e)
    candidates = []
    for sign in (+1.0, -1.0):
        c, s = np.cos(sign * theta), np.sin(sign * theta)
        R = np.array([[c, -s], [s, c]])
        v_sc_out = v_moon + R @ v_inf_in
        candidates.append(v_sc_out)
    key = (lambda v: float(np.dot(v, v))) if mode == "decelerate" else (lambda v: -float(np.dot(v, v)))
    v_sc_out = min(candidates, key=key)
    return v_sc_out, float(np.degrees(theta)), v_inf_mag


def multi_flyby_titan_tour(
    titan: MoonState,
    v_inf_saturn_initial_kms: float,
    n_flybys: int,
    flyby_altitude_km: float,
    initial_apoapsis_titan_radii: float = 3.0,
    r_p_burn_km: float = 4 * 60268.0,  # 4 Saturn equatorial radii (ring-clearing)
) -> dict:
    """Simulate a Cassini-style multi-flyby Titan tour for Saturn capture.

    Setup:
      1. Initial Saturn-Orbit-Insertion burn at low periapsis (r_p_burn_km),
         placing the spacecraft on a bound ellipse with periapsis r_p_burn_km
         and apoapsis `initial_apoapsis_titan_radii × r_titan`. The apoapsis
         is deliberately chosen ABOVE Titan's orbital radius so the spacecraft
         is moving faster than Titan at the first encounter (prograde-encounter
         regime), which is the condition required for Titan flybys to shed
         energy in the Saturn frame.
      2. Each subsequent Titan encounter reduces orbital energy. Encounters
         occur at r = r_titan; the spacecraft state at that radius drives the
         flyby physics. After each flyby, the orbit's semi-major axis shrinks
         (apoapsis lowers toward r_titan).
      3. Termination: pumping stops when the spacecraft's speed at r_titan
         drops below Titan's orbital speed (encounter would flip to retrograde,
         adding energy instead of shedding it).
      4. Final periapsis-lowering trim to B-ring outer edge (92,000 km) is
         performed at apoapsis. Reported separately from the tour itself.

    Returns dict with the per-flyby trajectory history and total cost.
    """
    # --- Step 1: initial SOI burn ---
    r_a_initial = initial_apoapsis_titan_radii * titan.r_km
    a_initial = 0.5 * (r_p_burn_km + r_a_initial)
    E_after_burn = -GM_SATURN / (2 * a_initial)
    # cost of placing spacecraft on this ellipse vs hyperbolic arrival:
    v_p_hyperbolic = float(np.sqrt(v_inf_saturn_initial_kms ** 2 + 2 * GM_SATURN / r_p_burn_km))
    v_p_ellipse = float(np.sqrt(2 * (E_after_burn + GM_SATURN / r_p_burn_km)))
    initial_burn_kms = v_p_hyperbolic - v_p_ellipse

    # --- Step 2: track orbit through Titan flybys ---
    # Use 2D vector state (radial, azimuthal) at r = r_titan. Moon moves
    # azimuthally at v_titan; spacecraft has both radial and azimuthal
    # components determined by the current orbit's (E, h).
    h = float(np.sqrt(GM_SATURN * r_p_burn_km * r_a_initial / a_initial))
    v_az = h / titan.r_km  # azimuthal component at r = r_titan
    v_total = float(np.sqrt(2 * (E_after_burn + GM_SATURN / titan.r_km)))
    v_rad = float(np.sqrt(max(0.0, v_total ** 2 - v_az ** 2)))
    # Sign convention: inbound leg has v_rad < 0, outbound has v_rad > 0.
    # For the first encounter we pick outbound (spacecraft has just passed
    # periapsis). For decelerate-mode flyby, sign of v_rad does not change
    # the optimal-rotation result (model symmetry).
    v_sc_vec = np.array([v_rad, v_az])
    v_moon_vec = np.array([0.0, titan.v_kms])

    E = E_after_burn
    history = []
    total_pumping_days = 0.0
    period_initial_days = 2 * np.pi * np.sqrt(a_initial ** 3 / GM_SATURN) / 86400.0
    rp_moon = titan.radius_km + flyby_altitude_km

    for i in range(n_flybys):
        v_inf_pre = np.linalg.norm(v_sc_vec - v_moon_vec)
        E_pre = 0.5 * float(np.dot(v_sc_vec, v_sc_vec)) - GM_SATURN / titan.r_km

        v_sc_after_vec, theta_deg, v_inf_mag = flyby_2d(
            v_sc_vec, v_moon_vec, rp_moon, titan.mu_kms2, mode="decelerate",
        )
        E_new = 0.5 * float(np.dot(v_sc_after_vec, v_sc_after_vec)) - GM_SATURN / titan.r_km

        # If the flyby would not decrease energy (asymptote reached), stop.
        if E_new >= E_pre - 1e-3:
            history.append({
                "flyby": i + 1,
                "v_inf_moon_kms": v_inf_mag,
                "turn_deg": theta_deg,
                "E_kms2": E_new,
                "encounter": "no further pumping possible",
            })
            break
        if E_new >= 0:
            history.append({
                "flyby": i + 1,
                "encounter": "escaped Saturn",
                "E_kms2": E_new,
            })
            break

        a_new = -GM_SATURN / (2 * E_new)
        # angular momentum after flyby = r_titan × azimuthal_component
        h_new = titan.r_km * float(v_sc_after_vec[1])
        ecc_sq = max(0.0, 1.0 - h_new ** 2 / (GM_SATURN * a_new))
        ecc = float(np.sqrt(ecc_sq))
        r_p_new = a_new * (1.0 - ecc)
        r_a_new = a_new * (1.0 + ecc)
        period_new_days = 2 * np.pi * np.sqrt(a_new ** 3 / GM_SATURN) / 86400.0
        total_pumping_days += period_new_days

        history.append({
            "flyby": i + 1,
            "v_inf_moon_kms": v_inf_mag,
            "turn_deg": theta_deg,
            "v_sc_at_titan_after_kms": float(np.linalg.norm(v_sc_after_vec)),
            "v_azimuthal_after_kms": float(v_sc_after_vec[1]),
            "a_new_km": a_new,
            "r_p_km": r_p_new,
            "r_a_km": r_a_new,
            "period_days": period_new_days,
            "cumulative_pumping_days": total_pumping_days,
            "delta_E_kms2": E_new - E_pre,
        })

        E = E_new
        v_sc_vec = v_sc_after_vec

    # --- Step 3: final trim to bring periapsis to B-ring outer edge ---
    r_p_target = 92000.0  # km (B-ring outer)
    if E >= 0:
        dv_trim = float("nan")
        r_p_final = float("nan")
        r_a_final = float("nan")
    else:
        a_current = -GM_SATURN / (2 * E)
        h_current = titan.r_km * float(v_sc_vec[1])
        ecc_cur = float(np.sqrt(max(0.0, 1.0 - h_current ** 2 / (GM_SATURN * a_current))))
        r_a_final = a_current * (1.0 + ecc_cur)
        r_p_final = a_current * (1.0 - ecc_cur)
        if r_p_final <= r_p_target:
            dv_trim = 0.0
        else:
            v_a_current = float(np.sqrt(GM_SATURN * (2 / r_a_final - 1 / a_current)))
            a_target = 0.5 * (r_a_final + r_p_target)
            v_a_target = float(np.sqrt(GM_SATURN * (2 / r_a_final - 1 / a_target)))
            dv_trim = abs(v_a_current - v_a_target)

    return {
        "v_inf_saturn_initial_kms": v_inf_saturn_initial_kms,
        "initial_apoapsis_titan_radii": initial_apoapsis_titan_radii,
        "n_flybys_attempted": n_flybys,
        "n_flybys_useful": len([h for h in history if "v_inf_moon_kms" in h and "encounter" not in h]),
        "initial_burn_kms": initial_burn_kms,
        "period_initial_days": period_initial_days,
        "history": history,
        "total_pumping_days": total_pumping_days,
        "dv_trim_kms": dv_trim,
        "total_propulsive_kms": initial_burn_kms + (dv_trim if not np.isnan(dv_trim) else 0.0),
        "r_p_final_km": r_p_final,
        "r_a_final_km": r_a_final,
    }


# -----------------------------------------------------------------------------
# Sweep drivers
# -----------------------------------------------------------------------------

def sweep_single_titan(states: dict[str, MoonState], out_dir: Path) -> None:
    """H1 sweep: single Titan flyby across v_inf and altitude."""
    titan = states["Titan"]
    v_inf_sweep = [4.0, 5.0, 5.44, 6.0, 7.0, 8.0]
    altitude_sweep = [500, 1000, 2000, 5000, 10000]
    rows = []
    for v_inf in v_inf_sweep:
        for alt in altitude_sweep:
            res = best_capture_dv_single_flyby(titan, v_inf, alt)
            rows.append({"v_inf_saturn_kms": v_inf, **res})
    write_csv(out_dir / "single_titan_flyby.csv", rows)

    # plot
    fig, ax = plt.subplots(figsize=(8, 5))
    for alt in altitude_sweep:
        xs = v_inf_sweep
        ys = [r["dv_capture_saving_kms"] for r in rows if r["flyby_altitude_km"] == alt]
        ax.plot(xs, ys, marker="o", label=f"{alt} km altitude")
    ax.axhline(0.5, ls="--", color="gray", alpha=0.5, label="H1 lower bound (0.5 km/s)")
    ax.set_xlabel("Saturn-arrival hyperbolic excess velocity v_inf [km/s]")
    ax.set_ylabel("capture-burn savings from single Titan flyby [km/s]")
    ax.set_title("H1 — single Titan flyby Saturn-capture savings")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "single_titan_flyby.png", dpi=130)
    plt.close(fig)


def sweep_all_moons(states: dict[str, MoonState], out_dir: Path) -> None:
    """H3, H4 sweep: each moon's best single-flyby Saturn-capture savings at v_inf=5.44 km/s."""
    rows = []
    for name, moon in states.items():
        # safe minimum flyby altitude = 200 km above surface (generic);
        # but enforce inside sphere-of-influence.
        alt = 200
        if moon.radius_km + alt > moon.soi_km:
            alt = max(50, int(0.5 * moon.soi_km - moon.radius_km))
        res = best_capture_dv_single_flyby(moon, 5.44, alt)
        rows.append(res)
    write_csv(out_dir / "all_moons_single_flyby.csv", rows)

    # plot
    fig, ax = plt.subplots(figsize=(9, 5))
    names = [r["moon"] for r in rows]
    savings = [r["dv_capture_saving_kms"] for r in rows]
    colors = ["tab:blue" if r["in_soi"] else "tab:red" for r in rows]
    bars = ax.bar(names, savings, color=colors)
    for bar, r in zip(bars, rows):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f"{r['turn_deg']:.0f}°", ha="center", fontsize=8)
    ax.set_ylabel("capture-burn savings [km/s]  (single optimal-geometry flyby)")
    ax.set_title("H3 / H4 — per-moon ranking at v_inf_saturn = 5.44 km/s (Hohmann)")
    ax.grid(alpha=0.3, axis="y")
    ax.set_xticklabels(names, rotation=20)
    fig.tight_layout()
    fig.savefig(out_dir / "all_moons_single_flyby.png", dpi=130)
    plt.close(fig)


def sweep_multi_titan(states: dict[str, MoonState], out_dir: Path) -> None:
    """H2 sweep: Cassini-style multi-flyby Titan tour."""
    titan = states["Titan"]
    # Initial apoapsis sets prograde-encounter regime. Sweep the choice.
    initial_apoapsis_sweep = [2.0, 3.0, 4.0]  # multiples of r_titan
    n_sweep = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
    rows = []
    for ra_factor in initial_apoapsis_sweep:
        for n in n_sweep:
            res = multi_flyby_titan_tour(titan, 5.44, n, 1000.0, initial_apoapsis_titan_radii=ra_factor)
            rows.append({
                "initial_apoapsis_titan_radii": ra_factor,
                "n_flybys": n,
                "n_flybys_useful": res["n_flybys_useful"],
                "initial_burn_kms": res["initial_burn_kms"],
                "total_pumping_days": res["total_pumping_days"],
                "dv_trim_kms": res["dv_trim_kms"],
                "total_propulsive_kms": res["total_propulsive_kms"],
                "r_p_final_km": res["r_p_final_km"],
                "r_a_final_km": res["r_a_final_km"],
            })
    write_csv(out_dir / "multi_titan_tour.csv", rows)

    # comparison: full chemical capture (no tour) to same final orbit
    # (r_p = B-ring outer, r_a = r_titan), at v_inf = 5.44 km/s
    r_p_target = 92000.0
    r_p_burn = 4 * 60268.0
    r_a_target = titan.r_km
    a_target = 0.5 * (r_p_target + r_a_target)
    v_p_hyp = float(np.sqrt(5.44 ** 2 + 2 * GM_SATURN / r_p_burn))
    a_via_4Rs = 0.5 * (r_p_burn + r_a_target)
    v_p_via_4Rs = float(np.sqrt(GM_SATURN * (2 / r_p_burn - 1 / a_via_4Rs)))
    full_chemical_capture = v_p_hyp - v_p_via_4Rs  # full SOI to apoapsis = r_titan
    # plus a periapsis-lowering trim from 4 R_S to B-ring outer:
    v_a_after_soi = float(np.sqrt(GM_SATURN * (2 / r_a_target - 1 / a_via_4Rs)))
    v_a_target = float(np.sqrt(GM_SATURN * (2 / r_a_target - 1 / a_target)))
    full_trim = abs(v_a_after_soi - v_a_target)
    full_no_tour_total = full_chemical_capture + full_trim

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ra_factor in initial_apoapsis_sweep:
        xs = n_sweep
        ys1 = [r["total_propulsive_kms"] for r in rows if r["initial_apoapsis_titan_radii"] == ra_factor]
        ys2 = [r["total_pumping_days"] for r in rows if r["initial_apoapsis_titan_radii"] == ra_factor]
        axes[0].plot(xs, ys1, marker="o", label=f"initial r_a = {ra_factor}×Titan")
        axes[1].plot(xs, ys2, marker="o", label=f"initial r_a = {ra_factor}×Titan")
    axes[0].axhline(full_no_tour_total, ls="--", color="red", alpha=0.7,
                    label=f"no-tour chemical baseline = {full_no_tour_total:.2f} km/s")
    axes[0].set_xlabel("number of Titan flybys attempted")
    axes[0].set_ylabel("cumulative propulsive cost [km/s]")
    axes[0].set_title("H2 — total propulsive cost (SOI burn + trim) vs flyby count")
    axes[0].legend(); axes[0].grid(alpha=0.3)
    axes[1].set_xlabel("number of Titan flybys")
    axes[1].set_ylabel("cumulative pumping time [days]")
    axes[1].set_title("H2 — pumping window vs flyby count")
    axes[1].legend(); axes[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "multi_titan_tour.png", dpi=130)
    plt.close(fig)


def sweep_apoapsis(states: dict[str, MoonState], out_dir: Path) -> None:
    """H5 sweep: target capture-orbit apoapsis vs total burn cost."""
    titan = states["Titan"]
    # The capture burn at periapsis to bring an arriving hyperbolic spacecraft
    # to a bound orbit with periapsis r_p and apoapsis r_a:
    r_p_burn = 4 * 60268.0  # 4 Saturn radii periapsis
    v_inf = 5.44
    rows = []
    for ra_factor in [1.5, 2.0, 3.0, 4.0, 6.0]:
        r_a = ra_factor * titan.r_km
        v_p_hyp = float(np.sqrt(v_inf ** 2 + 2 * GM_SATURN / r_p_burn))
        a = 0.5 * (r_p_burn + r_a)
        v_p_ell = float(np.sqrt(GM_SATURN * (2 / r_p_burn - 1 / a)))
        dv_capture = v_p_hyp - v_p_ell
        rows.append({
            "ra_factor_titan_radii": ra_factor,
            "r_a_km": r_a,
            "v_p_hyperbolic_kms": v_p_hyp,
            "v_p_elliptical_kms": v_p_ell,
            "capture_burn_kms": dv_capture,
        })
    write_csv(out_dir / "apoapsis_sweep.csv", rows)

    fig, ax = plt.subplots(figsize=(8, 5))
    xs = [r["ra_factor_titan_radii"] for r in rows]
    ys = [r["capture_burn_kms"] for r in rows]
    ax.plot(xs, ys, marker="o")
    spread = max(ys) - min(ys)
    ax.set_xlabel("target apoapsis [Titan orbital radii]")
    ax.set_ylabel("propulsive Saturn-Orbit-Insertion burn [km/s]")
    ax.set_title(f"H5 — capture-orbit apoapsis sweep (spread = {spread*1000:.0f} m/s)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "apoapsis_sweep.png", dpi=130)
    plt.close(fig)


def sweep_iapetus_pre_titan(states: dict[str, MoonState], out_dir: Path) -> None:
    """H4 — Iapetus single flyby as first energy-reducer, then Titan tour."""
    iapetus = states["Iapetus"]
    titan = states["Titan"]
    rows = []
    for v_inf in [4.0, 5.44, 7.0]:
        iap = best_capture_dv_single_flyby(iapetus, v_inf, 1000.0)
        rows.append({
            "v_inf_saturn_initial_kms": v_inf,
            "iapetus_dv_kms": iap["dv_capture_saving_kms"],
            "iapetus_v_inf_after_kms": iap["v_inf_saturn_after_kms"],
            "iapetus_turn_deg": iap["turn_deg"],
            "iapetus_bound_after": iap["bound_after"],
        })
    write_csv(out_dir / "iapetus_then_titan.csv", rows)


# -----------------------------------------------------------------------------
# IO
# -----------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> int:
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading Saturnian moon state from Horizons cache ...")
    states = load_moon_states()
    print("Loaded moons:", ", ".join(states.keys()))
    print()

    print("[H1] Single-Titan-flyby sweep ...")
    sweep_single_titan(states, out_dir)

    print("[H3/H4] All-moons single-flyby comparison ...")
    sweep_all_moons(states, out_dir)

    print("[H2] Multi-Titan tour sweep ...")
    sweep_multi_titan(states, out_dir)

    print("[H5] Capture-orbit apoapsis sweep ...")
    sweep_apoapsis(states, out_dir)

    print("[H4] Iapetus pre-Titan reducer ...")
    sweep_iapetus_pre_titan(states, out_dir)

    print("\nDone. Outputs in", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
