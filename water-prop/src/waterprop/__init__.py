"""waterprop — physics models for water propulsion R&D.

Module layout:
  thermo/     nozzle expansion, chamber thermochemistry (Cantera-backed)
  trajectory/ astrodynamics, low-thrust transfers (poliastro-backed, future)
  lifetime/   sputter and erosion models for thruster components (future)
  storage/    cryogenic / high-pressure tank thermal models (future)

All modules export pure functions (no I/O, no plotting). Study runners under
../studies/ import from here and own their own CLI, plotting, and output paths.
"""

__version__ = "0.1.0"
