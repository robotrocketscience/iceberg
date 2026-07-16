#!/usr/bin/env python3
"""
R-mission-architecture-pivot-survey — desk-study triage.

Codes 32 candidate mission architectures and 8 kill criteria from existing
campaign evidence as data. Applies each criterion to each candidate using
cited source verdicts; produces per-cell verdict and per-candidate aggregate
classification.

No physics integration. Citation-based triage.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Literal


Verdict = Literal["PASS", "FAIL", "UNKNOWN"]
Aggregate = Literal["DEAD-ON-ARRIVAL", "REQUIRES-REFRAME", "WORTH-DEEP-DIVE"]


@dataclass
class CellResult:
    candidate_id: str
    criterion_id: str
    verdict: Verdict
    rationale: str
    cited_source: str


@dataclass
class CandidateResult:
    id: str
    name: str
    description: str
    cells: list[CellResult] = field(default_factory=list)
    aggregate: Aggregate = "WORTH-DEEP-DIVE"
    aggregate_rationale: str = ""


# =============================================================================
# Kill criteria — IDs match STUDY.md
# =============================================================================

CRITERIA = {
    "F1": {
        "name": "Inbound delta-velocity closure under continuous-thrust electric",
        "threshold": "<= 6.42 km/s impulsive-equivalent (matrix); 24.7-40.2 km/s continuous-thrust per R_inbound_dv_continuous_thrust",
        "source": "R_inbound_dv_continuous_thrust",
    },
    "F2": {
        "name": "B-ring crossing survivability for chunk-bearing vehicle",
        "threshold": "<= 1% per-pass extended-aperture intercept; phoebe 5-round chain confirms 0/4808 cells close",
        "source": "phoebe abdcd35/45869d4/8a31ba9/75ba925",
    },
    "F3": {
        "name": "L0-05 round-trip <= 14 yr strict (or <= 15 yr waiver)",
        "threshold": "<= 14 yr strict per L0-05",
        "source": "R12_lunar_GA_both_legs / R9_slow_trajectory_tof / R_cruise_time_optimization",
    },
    "F4": {
        "name": "Saturn-side delta-velocity compatible with chunk-as-propellant-tank lever",
        "threshold": "<= ~3.7 km/s Saturn-side maneuvering per pre-ram-scoop conops; +14.7 km/s residence-class kills lever",
        "source": "axis-19 2026-05-15 latest+6 project-owner direction; R_conops_chunk_vs_ram_scoop",
    },
    "F5": {
        "name": "Saturn-side process power feasible (~150 kWe for 1-yr electrolysis)",
        "threshold": "<= 200 kg/kW conservative; FSP-stretch 100 kg/kW",
        "source": "R_non_fission_baseline / R_saturn_side_solar_thermal",
    },
    "F6": {
        "name": "Reactor program / specific-power availability for demonstrator window 2032-2035",
        "threshold": "posterior on MWe-class fission delivery by 2035: 0.07-0.20 across 3 priors; FSP Phase 2 not awarded; 0-of-6 US base rate",
        "source": "R_megawatt_architecture_viability + locked beliefs (R-power-wonder findings 1-4)",
    },
    "F7": {
        "name": "Foundational-lever consistency: cargo serves as inbound propellant tank",
        "threshold": "project-owner-stated structural premise (axis-19 closure)",
        "source": "axis-19 history; R_conops_chunk_vs_ram_scoop",
    },
    "F8": {
        "name": "Capital-class threshold (tech-demonstrator OR better; NOT venture-required)",
        "threshold": "tech-demonstrator anchor per iapetus settlement; venture requires 5-fold >= 0.93 joint priors (1378x baseline lift)",
        "source": "iapetus 0516f70 + af8eb91",
    },
}


# =============================================================================
# Candidates — IDs match STUDY.md
#
# Per-cell verdict format: {criterion_id: (verdict, rationale, cited_source)}
# rationale is one sentence; cited_source is the round_id or belief reference.
# =============================================================================

CANDIDATES = [
    # -------- Baseline / chunk-rendezvous family --------
    {
        "id": "A",
        "name": "Held chunk-rendezvous",
        "description": "Bag-rendezvous with single B-ring chunk; matrix baseline before phoebe 5-round chain.",
        "cells": {
            "F1": ("FAIL", "Continuous-thrust inbound 24.7-40.2 km/s exceeds matrix 6.42 baseline by 3.8-6.3x; surviving 200-t cell at 24.1% delivered fraction only.", "R_inbound_dv_continuous_thrust"),
            "F2": ("FAIL", "Phoebe 5-round chain: 0 of 4,808 unique closure-checks pass extended-aperture survivability threshold at any (threshold, mesh, aperture, chunk-mass, q-exponent) combination.", "phoebe 5-round chain"),
            "F3": ("PASS", "14-yr ceiling achievable per R12 lunar-GA 13.91 yr at 70% delivery (different sub-architecture but same chunk capture).", "R12_lunar_GA_both_legs"),
            "F4": ("PASS", "Inbound chunk-rendezvous preserves chunk-as-propellant-tank lever (the foundational case).", "axis-19 closure"),
            "F5": ("UNKNOWN", "Saturn-side process power independent of capture-architecture; surface mining vs ring rendezvous changes the calculus.", "R_non_fission_baseline"),
            "F6": ("FAIL", "Variant-C closure requires reactor program at megawatt class; posterior 0.07-0.20; FSP Phase 2 not awarded; 0-of-6 US fission base rate.", "R_megawatt_architecture_viability + locked beliefs"),
            "F7": ("PASS", "Chunk-as-propellant-tank lever preserved.", "axis-19 closure"),
            "F8": ("PASS", "Tech-demonstrator anchor reachable conditional on engineering; iapetus settled program-class.", "iapetus chain"),
        },
    },
    {
        "id": "A_prime",
        "name": "Chunk-rendezvous + deployable drag-skirt aerocapture",
        "description": "Inflatable ballute / HIAD-class deployable drag-skirt for Earth aerocapture closure on chunk-bearing vehicle.",
        "cells": {
            "F1": ("FAIL", "Same as A; aerocapture closure does not change continuous-thrust inbound penalty during cruise.", "R_inbound_dv_continuous_thrust"),
            "F2": ("FAIL", "Same as A; drag-skirt addresses Earth aerocapture only, not B-ring rendezvous survivability.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "Drag-skirt enables aerocapture saves 1.5-3.5 km/s on Earth approach; could relax round-trip but doesn't change inbound cruise.", "R_megawatt_aerocapture_engineering_closure"),
            "F4": ("PASS", "Same as A.", "axis-19 closure"),
            "F5": ("UNKNOWN", "Same as A.", "R_non_fission_baseline"),
            "F6": ("FAIL", "Same as A.", "R_megawatt_architecture_viability + locked beliefs"),
            "F7": ("PASS", "Same as A.", "axis-19 closure"),
            "F8": ("FAIL", "R_deployable_drag_skirt: peak heat flux 1,431 kW/m^2 at best-case (beta=100, areal=15) is 3-4x HIAD-2 design and LOFTID demonstrated; thermal does not close.", "R_deployable_drag_skirt"),
        },
    },
    {
        "id": "A_doubleprime",
        "name": "Outer-ring chunk-rendezvous (A-ring or F-ring)",
        "description": "Same architecture as A but rendezvous with chunks in A-ring (tau~0.5) or F-ring (tau~0.1) rather than B-ring (tau~2.0).",
        "cells": {
            "F1": ("FAIL", "Same as A; inbound cruise penalty independent of ring location.", "R_inbound_dv_continuous_thrust"),
            "F2": ("UNKNOWN", "B-ring zone-averaged tau ~2.0 kills A; F-ring tau ~0.1 reduces per-pass intercept by ~20x, but F-ring chunk-population is much lower and constituent particles are micron-class.", "Cassini ring optical-depth data; needs new round"),
            "F3": ("UNKNOWN", "Outer-ring approach Δv differs marginally from B-ring; not directly tested.", "—"),
            "F4": ("PASS", "Preserves chunk-as-propellant-tank lever.", "axis-19 closure"),
            "F5": ("UNKNOWN", "Same as A.", "R_non_fission_baseline"),
            "F6": ("FAIL", "Same as A.", "R_megawatt_architecture_viability + locked beliefs"),
            "F7": ("PASS", "Same as A.", "axis-19 closure"),
            "F8": ("UNKNOWN", "Conditional on F2 closure; if F-ring chunk-population is too low, capital-class question is moot.", "—"),
        },
    },
    {
        "id": "H",
        "name": "Aerocapture-conditional chunk-rendezvous (single-pass)",
        "description": "Chunk-as-heat-shield single-pass aerocapture per R_megawatt_aerocapture_engineering_closure.",
        "cells": {
            "F1": ("PASS", "Aerocapture-conditional: round-trip 4.81 yr (continuous-thrust); delivered fraction 42.7% at 200-t chunk.", "R_megawatt_aerocapture_engineering_closure"),
            "F2": ("FAIL", "Same as A; aerocapture closure does not change B-ring rendezvous.", "phoebe 5-round chain"),
            "F3": ("PASS", "4.81 yr round-trip clears L0-05 by ~9 yr.", "R_megawatt_aerocapture_engineering_closure"),
            "F4": ("PASS", "Chunk-as-heat-shield is consistent with chunk-as-propellant-tank.", "axis-19 closure"),
            "F5": ("UNKNOWN", "Same as A.", "R_non_fission_baseline"),
            "F6": ("FAIL", "Required reactor still 1000 kWe (10x FSP Phase 2); posterior 0.10-0.30 by 2032-35.", "R_megawatt_aerocapture_engineering_closure"),
            "F7": ("PASS", "Same as A.", "axis-19 closure"),
            "F8": ("PASS", "Conditional on F6 closure; tech-demonstrator capital class reachable.", "iapetus chain"),
        },
    },

    # -------- Ram-scoop / residence-class family --------
    {
        "id": "B",
        "name": "Ram-scoop residence-class (B-ring)",
        "description": "Open-bag accretion at v_rel ~10 m/s during residence in B-ring; +14.7 km/s Saturn-side circularisation Δv.",
        "cells": {
            "F1": ("PASS", "Inbound continuous-thrust same penalty as A; not the binding constraint here.", "R_inbound_dv_continuous_thrust"),
            "F2": ("PASS", "Residence-class avoids the rendezvous-crossing problem (operates at orbital-matched velocity).", "R_bring_fine_structure_rendezvous"),
            "F3": ("UNKNOWN", "titan-2 Block 5/9 found composite steady-state delivered fraction 15.97% (Option-A-equivalent) at ~16 yr; Block 10 caught exit-burn-power audit showing 500-kWe nominal exit burn takes 8.92 yr (17.8x assumed 6-month dwell).", "titan-2 Blocks 4-11"),
            "F4": ("FAIL", "Residence-class +14.7 km/s Saturn-side Δv directly defeats chunk-as-propellant-tank lever; project-owner explicit retirement.", "axis-19 2026-05-15 latest+6"),
            "F5": ("PASS", "Bulk ring material provides electrolysis feedstock; same Saturn-side power class as chunk processing.", "R_non_fission_baseline"),
            "F6": ("FAIL", "Residence-class exit burn requires MWe-class power per titan-2 Block 10 (8.9 MWe at Isp 7000 for 6-month exit).", "titan-2 Block 10"),
            "F7": ("FAIL", "Bulk ring material is not coherent chunk; cannot serve as cohesive propellant tank.", "axis-19 closure"),
            "F8": ("PASS", "Tech-demonstrator capital-class reachable conditional on lever-reframe.", "iapetus chain"),
        },
    },
    {
        "id": "B_prime",
        "name": "Outer-ring residence-class (A-ring or F-ring)",
        "description": "Ram-scoop architecture in outer ring; same Δv penalty as B; lower particle density.",
        "cells": {
            "F1": ("PASS", "Same as B.", "—"),
            "F2": ("PASS", "Same as B; residence not rendezvous.", "—"),
            "F3": ("UNKNOWN", "Same as B; outer-ring fill time orders-of-magnitude longer at lower density.", "R_bring_fine_structure_rendezvous"),
            "F4": ("FAIL", "Same as B; circularisation penalty unchanged at outer-ring radius.", "axis-19 closure"),
            "F5": ("PASS", "Same as B.", "—"),
            "F6": ("FAIL", "Same as B.", "—"),
            "F7": ("FAIL", "Same as B; bulk material.", "—"),
            "F8": ("PASS", "Same as B.", "—"),
        },
    },

    # -------- Capture-physics alternatives --------
    {
        "id": "P1",
        "name": "Lunar-orbit catcher",
        "description": "Saturn-side chunk handoff to inbound-delivery stage; chunks intercepted at lunar orbit rather than LEO.",
        "cells": {
            "F1": ("FAIL", "Chunks still need to be moved from Saturn to lunar orbit; same inbound penalty as A unless capture-physics is different.", "R_inbound_dv_continuous_thrust"),
            "F2": ("FAIL", "Chunk acquisition at Saturn still requires B-ring rendezvous unless paired with a non-chunk-rendezvous source.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "Delivery to lunar orbit may relax Earth-arrival Δv by ~0.7-1.2 km/s but only ~5.2 pp delivered fraction per R_delivery_destination_altitude.", "R_delivery_destination_altitude"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same as A.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("PASS", "—", "—"),
        },
    },
    {
        "id": "P3",
        "name": "Tether-rendezvous (rotating tether passive grapple)",
        "description": "Spin-tether momentum-exchange grapple of chunk during B-ring crossing.",
        "cells": {
            "F1": ("FAIL", "Same as A.", "—"),
            "F2": ("FAIL", "Tether must transit B-ring twice (deploy + retract) at high relative velocity; same intercept problem.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same as A.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("PASS", "—", "—"),
        },
    },
    {
        "id": "P4",
        "name": "Active push-the-rock (lander + boost stage on chunk)",
        "description": "Land on chunk in B-ring; mount boost stage; thrust chunk into Earth-return trajectory.",
        "cells": {
            "F1": ("FAIL", "Same inbound penalty applies; chunk acceleration is mass-ratio-bound by chosen propellant class.", "R_inbound_dv_continuous_thrust"),
            "F2": ("FAIL", "Landing requires sustained relative-velocity matching in B-ring; transit problem unchanged.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same as A.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("PASS", "—", "—"),
        },
    },

    # -------- Source alternatives --------
    {
        "id": "S1",
        "name": "Enceladus plume sampling",
        "description": "Water from south-pole geysers (~200 kg/s aggregate plume mass flow); no ring crossing required.",
        "cells": {
            "F1": ("UNKNOWN", "Enceladus orbit (~4 R_S) is outside B-ring but inside E-ring; Saturn-side delta-velocity to Enceladus orbital insertion plus departure not in matrix; needs new round.", "—"),
            "F2": ("PASS", "Enceladus is at 4 Saturn radii; outside dense rings entirely. E-ring is diffuse ice-grain torus generated by plumes; tau is ~10^-5.", "Cassini E-ring data"),
            "F3": ("UNKNOWN", "Saturn-side dwell to collect 200-t-equivalent at ~0.1-1 kg/s effective capture from plume mass flow ~10^2-10^5 yr; needs new round.", "—"),
            "F4": ("UNKNOWN", "Enceladus orbital insertion adds Δv but bulk water acquisition replaces chunk-rendezvous; lever-consistency depends on collection rate.", "—"),
            "F5": ("UNKNOWN", "Saturn-side process power same class as A; not architecture-changing.", "R_non_fission_baseline"),
            "F6": ("FAIL", "Same reactor-program constraint as A unless inbound is solved differently.", "—"),
            "F7": ("UNKNOWN", "Conditional on collected mass packaging: if collected as ice slurry / aggregate, chunk-as-propellant-tank lever lost (similar to F2d/B); if as solid block, lever preserved.", "—"),
            "F8": ("UNKNOWN", "Conditional on F1, F3 closure.", "—"),
        },
    },
    {
        "id": "S2",
        "name": "Mimas surface ice mining",
        "description": "Land on Mimas (3.1 R_S, water-ice surface), surface-mine, ascend.",
        "cells": {
            "F1": ("UNKNOWN", "Saturn-side Δv to Mimas orbit + descent/ascent (~0.4-0.8 km/s surface escape) + return; not in matrix.", "—"),
            "F2": ("PASS", "Mimas is outside main ring system (just inside E-ring); ring crossing minimal.", "—"),
            "F3": ("UNKNOWN", "Mining cadence at ICEBERG-scale (200-t/yr to 200-t/decade) unknown; surface mining heritage zero at this mass scale.", "—"),
            "F4": ("UNKNOWN", "Surface-mined ice block could serve as chunk-as-propellant-tank if packaged cohesively; processing changes the calculus.", "—"),
            "F5": ("UNKNOWN", "Same as S1.", "—"),
            "F6": ("FAIL", "Same reactor-program constraint.", "—"),
            "F7": ("UNKNOWN", "Same as S1.", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },
    {
        "id": "S3",
        "name": "Iapetus surface ice mining",
        "description": "Land on Iapetus (59 R_S, dark/light hemisphere); surface ice abundant on light hemisphere.",
        "cells": {
            "F1": ("FAIL", "Iapetus orbit at 59 R_S is far outside Saturn's main system; Saturn-side cruise adds ~6 months one-way; mass-ratio cost not in matrix but adds Δv comparable to titan Block 9 finding (~10.49 yr powered cruise close-time).", "R9_slow_trajectory_tof analogy"),
            "F2": ("PASS", "Iapetus is well outside all rings.", "—"),
            "F3": ("FAIL", "Iapetus's 79-day orbital period + slow return synodic windows + mining cadence push round-trip to >>14 yr.", "—"),
            "F4": ("UNKNOWN", "Same as S2 packaging question.", "—"),
            "F5": ("UNKNOWN", "Same as S1.", "—"),
            "F6": ("FAIL", "Same reactor-program constraint.", "—"),
            "F7": ("UNKNOWN", "Same as S1.", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },
    {
        "id": "S4",
        "name": "Hyperion surface ice mining (porous body)",
        "description": "Hyperion is a porous tumbling body at 24.6 R_S; sponge-like surface may permit easy ice extraction.",
        "cells": {
            "F1": ("UNKNOWN", "Hyperion orbit at 24.6 R_S; Saturn-side cruise penalty intermediate.", "—"),
            "F2": ("PASS", "Outside main ring system.", "—"),
            "F3": ("UNKNOWN", "Mining cadence on porous chaotically-tumbling body unprecedented.", "—"),
            "F4": ("UNKNOWN", "Same as S2.", "—"),
            "F5": ("UNKNOWN", "Same as S1.", "—"),
            "F6": ("FAIL", "Same reactor-program constraint.", "—"),
            "F7": ("UNKNOWN", "Same as S1.", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },
    {
        "id": "S5",
        "name": "Tethys surface ice mining",
        "description": "Tethys (4.9 R_S, ~99% water-ice composition); shallow gravity well.",
        "cells": {
            "F1": ("UNKNOWN", "Tethys orbit close to Saturn (4.9 R_S); Saturn-side Δv modest.", "—"),
            "F2": ("PASS", "Just outside E-ring; minimal ring crossing.", "—"),
            "F3": ("UNKNOWN", "Same as S2 cadence question.", "—"),
            "F4": ("UNKNOWN", "Same as S2.", "—"),
            "F5": ("UNKNOWN", "Same as S1.", "—"),
            "F6": ("FAIL", "Same reactor-program constraint.", "—"),
            "F7": ("UNKNOWN", "Same as S1.", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },
    {
        "id": "S6",
        "name": "Phoebe surface ice (irregular satellite)",
        "description": "Phoebe at 215 R_S, retrograde orbit, comet-class composition (high water-ice fraction).",
        "cells": {
            "F1": ("FAIL", "Phoebe at 215 R_S in retrograde orbit; Saturn-side cruise and orbital insertion costs are enormous (functionally similar to S7 Trojans).", "—"),
            "F2": ("PASS", "Well outside ring system.", "—"),
            "F3": ("FAIL", "Saturn-side dwell + ~4-month one-way cruise + return synodic windows pushes round-trip > 20 yr.", "—"),
            "F4": ("UNKNOWN", "Same as S2.", "—"),
            "F5": ("UNKNOWN", "Same as S1.", "—"),
            "F6": ("FAIL", "Same reactor-program constraint.", "—"),
            "F7": ("UNKNOWN", "Same as S1.", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },
    {
        "id": "S7",
        "name": "Saturn-system Trojan / Hilda water-ice",
        "description": "Bodies at Saturn-Sun L4/L5 (or Hilda 2:3 with Jupiter); high water content but distant.",
        "cells": {
            "F1": ("FAIL", "Trojans at 5-9 AU; transit time + Saturn departure penalty vs current direct-to-Saturn architecture is strictly worse.", "—"),
            "F2": ("PASS", "No Saturn ring crossing.", "—"),
            "F3": ("FAIL", "Round-trip to Saturn-Trojan and back > 24 yr per R9 analogy.", "R9_slow_trajectory_tof"),
            "F4": ("UNKNOWN", "Same as S2.", "—"),
            "F5": ("UNKNOWN", "Same as S1.", "—"),
            "F6": ("FAIL", "Same reactor-program constraint.", "—"),
            "F7": ("UNKNOWN", "Same as S1.", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },

    # -------- Time-domain alternatives --------
    {
        "id": "T1",
        "name": "Very slow low-energy cruise",
        "description": "Trade transit time for delta-velocity (long Hohmann-class transfers).",
        "cells": {
            "F1": ("PASS", "Slow cruise relaxes inbound Δv requirement.", "—"),
            "F2": ("FAIL", "B-ring rendezvous problem unchanged (slow cruise doesn't affect ring transit).", "phoebe 5-round chain"),
            "F3": ("FAIL", "R9 slow trajectory: realistic round-trip ~24 yr; conops 13-yr triple internally inconsistent.", "R9_slow_trajectory_tof"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("UNKNOWN", "Lower power Kilopower-class might close if Δv is small enough; R9 shows it doesn't.", "R9_slow_trajectory_tof"),
            "F7": ("PASS", "—", "—"),
            "F8": ("PASS", "—", "—"),
        },
    },
    {
        "id": "T2",
        "name": "Chunk pre-staging at intermediate moon",
        "description": "Pre-stage chunks in Iapetus or Mimas parking orbit; phase-2 push to Earth-return.",
        "cells": {
            "F1": ("UNKNOWN", "Two-stage architecture: Saturn-side stage moves chunk to parking; phase-2 stage handles inbound. Each stage has lower Δv but stages don't compose linearly.", "—"),
            "F2": ("FAIL", "Chunk acquisition step still requires B-ring rendezvous.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "Pre-staging breaks the 14-yr cap into two-mission cycle; commit-timing problem changes (similar to R_heterogeneous_cadence's adjacent staged-commitment hypothesis).", "R_heterogeneous_cadence"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same reactor constraint.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("UNKNOWN", "—", "—"),
        },
    },

    # -------- Form-factor / delivery-target alternatives --------
    {
        "id": "F1d",
        "name": "Return propellant (H2/O2) not water (Architecture D)",
        "description": "Saturn-side electrolyse water into hydrogen + oxygen; return cryogenic propellant.",
        "cells": {
            "F1": ("UNKNOWN", "Electrolysed propellant changes inbound mass-ratio math.", "R_chemical_plus_small_reactor"),
            "F2": ("UNKNOWN", "Depends on coupled source architecture.", "—"),
            "F3": ("UNKNOWN", "—", "—"),
            "F4": ("UNKNOWN", "—", "—"),
            "F5": ("FAIL", "R_architecture_D_cost: requires 10 W/kg FSP Phase 1 STRETCH (not contracted 5 W/kg); 20-t reactor 200 kWe.", "R_architecture_D_cost"),
            "F6": ("FAIL", "Same reactor-program constraint, plus needs 200-kWe Saturn-side process power class.", "R_architecture_D_cost"),
            "F7": ("FAIL", "Returning propellant not water means cargo is not the propellant tank; lever lost.", "axis-19 closure"),
            "F8": ("FAIL", "R_architecture_D_cost: 0 of 48 cells return defined IRR. R_architecture_D_L1007_relaxation: program-NPV negative across 168 cells (D-fission $-15.6B, D-solar $-14.1B at best cell vs Variant B $+42.3B).", "R_architecture_D_cost + R_architecture_D_L1007_relaxation"),
        },
    },
    {
        "id": "F2d",
        "name": "Return as bulk ring material aggregate",
        "description": "Collect bulk ring material at Saturn (ram-scoop output) and return as aggregate.",
        "cells": {
            "F1": ("PASS", "—", "—"),
            "F2": ("PASS", "Same as B (residence-class avoids rendezvous).", "—"),
            "F3": ("UNKNOWN", "Same as B.", "—"),
            "F4": ("FAIL", "Same as B (+14.7 km/s Saturn-side).", "axis-19 closure"),
            "F5": ("PASS", "—", "—"),
            "F6": ("FAIL", "Same as B.", "—"),
            "F7": ("FAIL", "Bulk material lever-inconsistent (same as B).", "axis-19 closure"),
            "F8": ("PASS", "—", "—"),
        },
    },
    {
        "id": "F3d",
        "name": "Many small chunks instead of one big",
        "description": "Heterogeneous cadence with chunk_1 << 200 t to lower mission-1 commit cost.",
        "cells": {
            "F1": ("FAIL", "Same as A; inbound penalty unchanged.", "—"),
            "F2": ("FAIL", "Same as A; rendezvous problem multiplies per chunk.", "phoebe 5-round chain"),
            "F3": ("FAIL", "Same as A.", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same reactor constraint.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("FAIL", "R_heterogeneous_cadence: all chunk_1 < 200 t lose $30M-$113M NPV in regime D, sacrificed $484M in regime R. R_cadence_multiship: compressed N>=3 collapses IRR to -1.45%.", "R_heterogeneous_cadence + R_cadence_multiship"),
        },
    },
    {
        "id": "F4d",
        "name": "Deliver to L4/L5/GEO/lunar-orbit instead of LEO",
        "description": "Different terminal delivery altitude.",
        "cells": {
            "F1": ("FAIL", "Same inbound problem.", "—"),
            "F2": ("FAIL", "Same as A.", "phoebe 5-round chain"),
            "F3": ("PASS", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same reactor constraint.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("FAIL", "R_delivery_destination_altitude: only 5.2 pp gain LEO -> GEO; not architecture-changing per IRR/NPV.", "R_delivery_destination_altitude"),
        },
    },

    # -------- Commercial-model alternatives --------
    {
        "id": "C2c",
        "name": "Precursor mission (smaller water + sell heritage)",
        "description": "Smaller target water mass; revenue model leans on heritage value to follow-on architectures.",
        "cells": {
            "F1": ("UNKNOWN", "Smaller chunk relaxes mass-ratio; could close inbound.", "—"),
            "F2": ("FAIL", "Even small chunk requires B-ring rendezvous.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "Smaller chunk could fly faster (lower mass-ratio).", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("UNKNOWN", "Smaller chunk reduces reactor-power requirement; Kilopower-class may close.", "R_chunk_fed_chemical"),
            "F7": ("PASS", "—", "—"),
            "F8": ("UNKNOWN", "Capital structure depends on heritage revenue model not water-revenue.", "—"),
        },
    },
    {
        "id": "C3c",
        "name": "Shared launch / cost-split with other Saturn customers",
        "description": "Outbound launch costs split with science / NASA missions; reduces 6.9x launch-mass multiplier impact.",
        "cells": {
            "F1": ("FAIL", "Same A inbound.", "—"),
            "F2": ("FAIL", "Same A.", "phoebe 5-round chain"),
            "F3": ("PASS", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same reactor constraint.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("UNKNOWN", "Shared-launch could rescue per-mission economics conditional on actual co-customer existing.", "R_outbound_architecture"),
        },
    },
    {
        "id": "C4c",
        "name": "Data-resource mode (smaller water + sensor-data primary revenue)",
        "description": "Smaller water mass; revenue from in-situ science + heritage data sales; water as proof-of-concept.",
        "cells": {
            "F1": ("UNKNOWN", "Same as C2c.", "—"),
            "F2": ("FAIL", "B-ring rendezvous unchanged.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("UNKNOWN", "Smaller water target relaxes reactor power.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("UNKNOWN", "Capital structure: science revenue is not subject to launch-cost displacement competition (per existing belief 'parallel science revenue stream').", "—"),
        },
    },

    # -------- Mission-architecture alternatives --------
    {
        "id": "M2m",
        "name": "One-way ships (no return)",
        "description": "Deliver chunk and abandon vehicle in cislunar / Earth-vicinity; no Saturn-return mission cycle.",
        "cells": {
            "F1": ("UNKNOWN", "One-way Tsiolkovsky drops mass-ratio significantly; could close at lower Isp.", "—"),
            "F2": ("FAIL", "Acquisition unchanged.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "Round-trip not applicable; only one-way transit time.", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("UNKNOWN", "Lower mass-ratio = lower reactor requirement.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("UNKNOWN", "Vehicle disposal cost vs reuse cost not yet modeled; outbound launch cost unchanged.", "R_outbound_architecture"),
        },
    },
    {
        "id": "M3m",
        "name": "Tug-and-go fleet (one tug per chunk; tug stays at Saturn)",
        "description": "Dedicated Saturn-side tug per chunk-acquisition; tugs never return.",
        "cells": {
            "F1": ("UNKNOWN", "Tug doesn't perform inbound; separate inbound stage required.", "—"),
            "F2": ("FAIL", "B-ring rendezvous unchanged per tug.", "phoebe 5-round chain"),
            "F3": ("UNKNOWN", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Per-mission reactor cost multiplied by tug count; cadence-economics collapse per R_cadence_multiship.", "R_cadence_multiship"),
            "F7": ("PASS", "—", "—"),
            "F8": ("FAIL", "R_cadence_multiship: N=5 fleet drops IRR to -1.45%; compressed cadence is anti-optimal at N>=3.", "R_cadence_multiship"),
        },
    },

    # -------- L0-reframe alternatives --------
    {
        "id": "L1r",
        "name": "Drop 14-yr round-trip cap (relax L0-05)",
        "description": "L0-05 waiver opens architectures with > 14 yr round-trip.",
        "cells": {
            "F1": ("PASS", "Slow cruise becomes admissible.", "—"),
            "F2": ("FAIL", "B-ring rendezvous problem orthogonal to L0-05.", "phoebe 5-round chain"),
            "F3": ("PASS", "By construction (L0-05 relaxed).", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same reactor constraint applies.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("UNKNOWN", "Capital-class implications of longer round-trip not in iapetus framework.", "—"),
        },
    },
    {
        "id": "L2r",
        "name": "Drop chunk-as-propellant-tank premise (relax F7)",
        "description": "Foundational lever relaxation; enables ram-scoop B / F2d / S1-aggregate variants.",
        "cells": {
            "F1": ("PASS", "—", "—"),
            "F2": ("PASS", "Residence-class avoids rendezvous.", "—"),
            "F3": ("UNKNOWN", "Same as B.", "titan-2 Blocks 4-11"),
            "F4": ("PASS", "By construction.", "—"),
            "F5": ("PASS", "—", "—"),
            "F6": ("FAIL", "Residence-class exit-burn requires MWe-class.", "titan-2 Block 10"),
            "F7": ("PASS", "By construction.", "—"),
            "F8": ("PASS", "—", "—"),
        },
    },
    {
        "id": "L3r",
        "name": "Drop 100% Earth-delivery target",
        "description": "Allow inbound mass-ratio to leave residual in-flight propellant; deliver less to Earth.",
        "cells": {
            "F1": ("PASS", "Mass-ratio closes more easily.", "—"),
            "F2": ("FAIL", "Rendezvous problem unchanged.", "phoebe 5-round chain"),
            "F3": ("PASS", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("UNKNOWN", "Lower delivered mass relaxes reactor power per R_chunk_fed_chemical mapping.", "R_chunk_fed_chemical"),
            "F7": ("PASS", "Chunk-as-propellant-tank preserved (the chunk is the propellant supply).", "—"),
            "F8": ("UNKNOWN", "Revenue model implications; partial-delivery economics not yet modeled.", "—"),
        },
    },
    {
        "id": "L4r",
        "name": "Drop 'Earth orbit' delivery target (lunar / L4-L5 only)",
        "description": "Deliver to cislunar depot, not LEO; serves propellant-economy customers not water-end-users.",
        "cells": {
            "F1": ("PASS", "Slight Δv relief.", "R_delivery_destination_altitude"),
            "F2": ("FAIL", "Acquisition unchanged.", "phoebe 5-round chain"),
            "F3": ("PASS", "—", "—"),
            "F4": ("PASS", "—", "—"),
            "F5": ("UNKNOWN", "—", "—"),
            "F6": ("FAIL", "Same reactor constraint.", "—"),
            "F7": ("PASS", "—", "—"),
            "F8": ("FAIL", "R_delivery_destination_altitude: only 5.2 pp delta LEO->GEO; cislunar marginally better; not architecture-saving on capital-class.", "R_delivery_destination_altitude"),
        },
    },
]


# =============================================================================
# Aggregation logic — matches STUDY.md decision rules
# =============================================================================


def classify(cells: dict[str, tuple[str, str, str]]) -> tuple[Aggregate, str]:
    """Aggregate per-candidate verdict from per-criterion verdicts.

    Rules (from STUDY.md):
        - 1+ FAIL on F1, F2, F3, F5, F6, F8 -> DEAD-ON-ARRIVAL.
        - FAIL only on F4 or F7 (and no other FAILs) -> REQUIRES-REFRAME.
        - No FAILs -> WORTH-DEEP-DIVE.
    """
    physical_killers = {"F1", "F2", "F3", "F5", "F6", "F8"}
    reframe_killers = {"F4", "F7"}

    fails = {cid for cid, (v, _, _) in cells.items() if v == "FAIL"}

    physical_fails = fails & physical_killers
    reframe_fails = fails & reframe_killers

    if physical_fails:
        reasons = ", ".join(sorted(physical_fails))
        return "DEAD-ON-ARRIVAL", f"Fails {reasons} (physical-kill criteria)"
    if reframe_fails:
        reasons = ", ".join(sorted(reframe_fails))
        return "REQUIRES-REFRAME", f"Fails only {reasons} (project-owner-stated framing constraints)"
    return "WORTH-DEEP-DIVE", "No FAILs against any criterion; surviving for follow-on deep-dive"


def main():
    results: list[CandidateResult] = []
    for cand in CANDIDATES:
        cell_results = [
            CellResult(
                candidate_id=cand["id"],
                criterion_id=cid,
                verdict=v,
                rationale=rationale,
                cited_source=src,
            )
            for cid, (v, rationale, src) in cand["cells"].items()
        ]
        aggregate, agg_reason = classify(cand["cells"])
        results.append(CandidateResult(
            id=cand["id"],
            name=cand["name"],
            description=cand["description"],
            cells=cell_results,
            aggregate=aggregate,
            aggregate_rationale=agg_reason,
        ))

    summary = {
        "n_candidates": len(results),
        "n_dead": sum(1 for r in results if r.aggregate == "DEAD-ON-ARRIVAL"),
        "n_reframe": sum(1 for r in results if r.aggregate == "REQUIRES-REFRAME"),
        "n_deep_dive": sum(1 for r in results if r.aggregate == "WORTH-DEEP-DIVE"),
    }

    output = {
        "round": "R-mission-architecture-pivot-survey",
        "criteria": CRITERIA,
        "candidates": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "aggregate": r.aggregate,
                "aggregate_rationale": r.aggregate_rationale,
                "cells": [asdict(c) for c in r.cells],
            }
            for r in results
        ],
        "summary": summary,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "R_mission_architecture_pivot_survey.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"Wrote {out_path}")

    print("\nSummary counts:")
    print(f"  Candidates: {summary['n_candidates']}")
    print(f"  DEAD-ON-ARRIVAL: {summary['n_dead']}")
    print(f"  REQUIRES-REFRAME: {summary['n_reframe']}")
    print(f"  WORTH-DEEP-DIVE: {summary['n_deep_dive']}")

    print("\nPer-candidate verdicts:")
    for r in results:
        print(f"  {r.id:18s}  {r.aggregate:18s}  {r.name}")


if __name__ == "__main__":
    main()
