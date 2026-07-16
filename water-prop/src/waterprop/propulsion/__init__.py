"""Propulsion-system performance models.

Module contents:
  dual_ion — hydrogen-ion + oxygen-ion electric thruster from on-board
             water electrolysis. Mass-weighted specific impulse, thrust
             per unit electrical power, and chunk-delivery fraction under
             ICEBERG-class mission constraints.
"""
from .dual_ion import (
    ion_exhaust_velocity_m_s,
    dual_ion_isp_s,
    dual_ion_thrust_per_kw,
    delivery_fraction_chunk_fed,
    MASS_FRAC_H_IN_WATER,
    MASS_FRAC_O_IN_WATER,
    AMU_KG,
    H_MASS_AMU,
    O_MASS_AMU,
    H2_MASS_AMU,
    E_CHARGE,
)
from .nep_optimum import (
    power_optimal_isp,
    energy_balance_residual,
)
from .burns import (
    burn_from_wet,
    burn_from_dry_end,
)

__all__ = [
    "ion_exhaust_velocity_m_s",
    "dual_ion_isp_s",
    "dual_ion_thrust_per_kw",
    "delivery_fraction_chunk_fed",
    "power_optimal_isp",
    "energy_balance_residual",
    "burn_from_wet",
    "burn_from_dry_end",
    "MASS_FRAC_H_IN_WATER",
    "MASS_FRAC_O_IN_WATER",
    "AMU_KG",
    "H_MASS_AMU",
    "O_MASS_AMU",
    "H2_MASS_AMU",
    "E_CHARGE",
]
