"""Constant-thrust burn helpers with the convention pinned in the function name.

This module lifts the `burn_from_wet` / `burn_from_dry_end` pattern out of
`R_electric_outbound_rerun/run.py` into the shared library. The named-helper-pair
pattern is the H4 verdict mechanism from R-shared-physics-audit: a single
`constant_thrust_burn(m_initial_t, ...)` cannot signature-type whether the caller
meant wet-mass-at-start vs dry-mass-at-end, so a value assertion is insufficient
to catch the convention bug. Splitting into two convention-named functions makes
the caller commit to which convention they are using and removes the silent-bug
class.

Migration path for round-local `constant_thrust_burn` redefinitions:

  - Round expecting wet-mass-at-start (5 of 6 current copies):
    `from waterprop.propulsion import burn_from_wet`
  - Round expecting dry-mass-at-end (1 of 6, `R_non_fission_baseline`):
    `from waterprop.propulsion import burn_from_dry_end`

The `audit-call-conventions.py` enforcement script flags any new round-local
redefinition of a name in {`constant_thrust_burn`, `burn_from_wet`, `burn_from_dry_end`}
because the canonical implementation now lives here.
"""

from __future__ import annotations

import math

from ..constants import G0

# Year length used by burn-time conversion. Matches the value used by round-local copies.
YEAR_S = 365.25 * 86400.0


def burn_from_wet(
    m_initial_wet_t: float,
    dv_km_s: float,
    power_kwe: float,
    isp_s: float,
    eta: float = 0.6,
) -> dict:
    """Constant-thrust burn given the WET (start-of-burn) mass.

    The convention is pinned by the function name: `m_initial_wet_t` is the
    spacecraft + propellant mass at the moment the burn begins. The propellant
    consumed follows Tsiolkovsky in its "what fraction of starting mass is
    propellant" form:

      m_prop = m_initial_wet * (1 - 1 / MR)

    where MR = exp(dv / v_e). Burn time = m_prop * v_e / thrust at constant
    thrust = 2 * eta * P_electrical / v_e.

    Args:
        m_initial_wet_t: wet mass at start of burn, in tonnes (> 0).
        dv_km_s: delta-velocity magnitude, in kilometres per second (> 0).
        power_kwe: electrical power into the thruster, in kilowatts (> 0).
        isp_s: specific impulse, in seconds (> 0).
        eta: thruster total efficiency (jet power / electrical power), unitless
            (0 < eta ≤ 1). Default 0.6.

    Returns dict with thrust_N, m_prop_t, mass_ratio, t_burn_s, t_burn_yr,
    m_initial_t (echoed for cross-checking), and m_final_t (= m_initial_wet - m_prop).
    """
    assert m_initial_wet_t > 0, "m_initial_wet_t must be positive"
    assert dv_km_s > 0, "dv_km_s must be positive"
    assert power_kwe > 0, "power_kwe must be positive"
    assert isp_s > 0, "isp_s must be positive"
    assert 0.0 < eta <= 1.0, "eta must be in (0, 1]"

    v_e = isp_s * G0  # m/s
    thrust_n = 2.0 * eta * power_kwe * 1000.0 / v_e  # newtons
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_initial_wet_t * (1.0 - 1.0 / mass_ratio)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_n
    return {
        "thrust_N": thrust_n,
        "m_initial_t": m_initial_wet_t,
        "m_final_t": m_initial_wet_t - m_prop_t,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_s": t_burn_s,
        "t_burn_yr": t_burn_s / YEAR_S,
    }


def burn_from_dry_end(
    m_final_dry_t: float,
    dv_km_s: float,
    power_kwe: float,
    isp_s: float,
    eta: float = 0.6,
) -> dict:
    """Constant-thrust burn given the DRY (end-of-burn) mass.

    The convention is pinned by the function name: `m_final_dry_t` is the
    spacecraft mass at the moment the burn ends (propellant exhausted to
    satisfy the delta-velocity requirement). Propellant follows Tsiolkovsky
    in its "what factor over the final mass" form:

      m_prop = m_final_dry * (MR - 1)

    Burn time uses the same constant-thrust integral as `burn_from_wet`.
    The two functions are mathematically equivalent when called consistently:
    `burn_from_wet(m_final * MR, ...)` ≡ `burn_from_dry_end(m_final, ...)`.

    Args:
        m_final_dry_t: dry mass at end of burn, in tonnes (> 0).
        dv_km_s: delta-velocity magnitude, in kilometres per second (> 0).
        power_kwe: electrical power into the thruster, in kilowatts (> 0).
        isp_s: specific impulse, in seconds (> 0).
        eta: thruster total efficiency (jet power / electrical power), unitless
            (0 < eta ≤ 1). Default 0.6.

    Returns dict with thrust_N, m_prop_t, mass_ratio, t_burn_s, t_burn_yr,
    m_final_t (echoed for cross-checking), and m_initial_t (= m_final_dry * MR).
    """
    assert m_final_dry_t > 0, "m_final_dry_t must be positive"
    assert dv_km_s > 0, "dv_km_s must be positive"
    assert power_kwe > 0, "power_kwe must be positive"
    assert isp_s > 0, "isp_s must be positive"
    assert 0.0 < eta <= 1.0, "eta must be in (0, 1]"

    v_e = isp_s * G0
    thrust_n = 2.0 * eta * power_kwe * 1000.0 / v_e
    mass_ratio = math.exp(dv_km_s * 1000.0 / v_e)
    m_prop_t = m_final_dry_t * (mass_ratio - 1.0)
    t_burn_s = m_prop_t * 1000.0 * v_e / thrust_n
    return {
        "thrust_N": thrust_n,
        "m_initial_t": m_final_dry_t + m_prop_t,
        "m_final_t": m_final_dry_t,
        "m_prop_t": m_prop_t,
        "mass_ratio": mass_ratio,
        "t_burn_s": t_burn_s,
        "t_burn_yr": t_burn_s / YEAR_S,
    }
