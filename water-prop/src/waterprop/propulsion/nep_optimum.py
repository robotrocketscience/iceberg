"""Power-constrained specific-impulse optimization for a nuclear-electric
chunk-fed propulsion spacecraft.

The classical NASA NEP analysis: with fixed available electrical power P,
fixed cruise time t, and fixed initial mass m_initial, the optimal specific
impulse maximizes delivered cargo. The math comes from solving the energy
balance against Tsiolkovsky's rocket equation.

Energy balance:
  jet_energy = 0.5 * m_propellant * v_e^2 = eta_total * P * t * duty_cycle

Tsiolkovsky:
  m_propellant = m_initial * (1 - exp(-delta_v / v_e))

Eliminating m_propellant:
  m_initial * (1 - exp(-delta_v / v_e)) * v_e^2 = 2 * eta * P * t * duty

For fixed (m_initial, delta_v, P, t, eta, duty) on the right-hand side, the
left-hand side is a one-variable function of v_e that goes to 0 as v_e -> 0
(no propellant) and grows without bound as v_e -> infinity (linearized
Tsiolkovsky). The energy-balance constraint pins v_e to a specific value.

To maximize delivered mass at the boundary of the constraint, solve for
v_e where the energy balance is satisfied. Delivered mass is
m_initial * exp(-delta_v / v_e).

For sub-optimal (lower) v_e, propellant is wasted; for higher v_e the
energy budget is exceeded (insufficient power).

Note: this assumes the propulsion system can deliver delta_v in the fixed
cruise time. If it can't (thrust too low), the spacecraft simply doesn't
make the delta_v — the operating point is infeasible, not sub-optimal.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

G0 = 9.80665


def energy_balance_residual(v_e: float, m_initial_kg: float,
                             delta_v_m_s: float,
                             eta_t_P_W_duty: float) -> float:
    """Residual of the NEP energy-balance constraint.

    Convention: `m_initial_kg` is the WET (start-of-burn) mass. The Tsiolkovsky
    factor `1 - exp(-delta_v / v_e)` returns the propellant fraction of
    starting mass; passing post-burn dry mass would silently understate
    propellant by the mass-ratio factor.

    Zero means the energy budget exactly matches what's needed to deliver
    delta_v at exhaust velocity v_e, starting from m_initial.
    """
    assert m_initial_kg > 0, "m_initial_kg must be positive (wet mass at start of burn)"
    assert v_e > 0, "v_e must be positive"
    assert delta_v_m_s > 0, "delta_v_m_s must be positive"
    m_p = m_initial_kg * (1.0 - np.exp(-delta_v_m_s / v_e))
    jet_energy_needed = 0.5 * m_p * v_e ** 2
    return jet_energy_needed - eta_t_P_W_duty


def power_optimal_isp(power_W: float,
                       cruise_time_s: float,
                       duty_cycle: float,
                       efficiency_total: float,
                       m_initial_kg: float,
                       delta_v_m_s: float) -> dict:
    """Solve for the power-optimal specific impulse.

    Convention: `m_initial_kg` is the WET (start-of-burn) mass. Propellant
    fraction returned via Tsiolkovsky `(1 - exp(-delta_v / v_e))`; passing
    post-burn dry mass would silently understate propellant and overstate
    delivered mass by the mass-ratio factor.

    Returns a dict with the power-optimal v_e, Isp, propellant mass,
    delivered mass, and chunk-delivery fraction. Returns NaN values if
    the constraint is not satisfiable within the bracket.
    """
    assert m_initial_kg > 0, "m_initial_kg must be positive (wet mass at start of burn)"
    assert power_W > 0, "power_W must be positive"
    assert cruise_time_s > 0, "cruise_time_s must be positive"
    assert 0.0 < duty_cycle <= 1.0, "duty_cycle must be in (0, 1]"
    assert 0.0 < efficiency_total <= 1.0, "efficiency_total must be in (0, 1]"
    assert delta_v_m_s > 0, "delta_v_m_s must be positive"
    eta_P_t_duty = efficiency_total * power_W * cruise_time_s * duty_cycle

    def residual(v_e):
        return energy_balance_residual(v_e, m_initial_kg, delta_v_m_s, eta_P_t_duty)

    # Bracket the solution. At very low v_e, residual is negative (propellant
    # required exceeds initial mass capability times v_e^2). At very high
    # v_e, residual goes positive (need more energy than available).
    # We use a wide search bracket.
    v_e_lo = 100.0       # m/s, super low — almost everything is propellant
    v_e_hi = 1e6         # m/s, ridiculously high

    # Make sure the bracket has a sign change.
    try:
        f_lo = residual(v_e_lo)
        f_hi = residual(v_e_hi)
        if f_lo * f_hi > 0:
            return {"power_W": power_W, "v_e_m_s": float("nan"),
                    "isp_s": float("nan"), "m_propellant_kg": float("nan"),
                    "m_delivered_kg": float("nan"),
                    "delivery_fraction": float("nan"),
                    "note": "infeasible: cannot bracket solution"}
        v_e_opt = brentq(residual, v_e_lo, v_e_hi, xtol=0.1)
    except Exception as exc:
        return {"power_W": power_W, "v_e_m_s": float("nan"),
                "isp_s": float("nan"), "m_propellant_kg": float("nan"),
                "m_delivered_kg": float("nan"),
                "delivery_fraction": float("nan"),
                "note": f"solver fail: {exc}"}

    m_p = m_initial_kg * (1.0 - np.exp(-delta_v_m_s / v_e_opt))
    m_delivered = m_initial_kg - m_p
    return {
        "power_W": power_W,
        "v_e_m_s": v_e_opt,
        "isp_s": v_e_opt / G0,
        "m_propellant_kg": m_p,
        "m_delivered_kg": m_delivered,
        "delivery_fraction": m_delivered / m_initial_kg,
    }
