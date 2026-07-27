#!/usr/bin/env python3
"""ICEBERG bag-dynamics 6-DOF coupled slosh + ACS sim (Basilisk).

The R191 (`R_bag_dynamics_envelope`) named follow-on: the lumped desk model
LOCATED a narrow viable corner (T_s in 100-180 s AND zeta >= 0.1) but explicitly
could NOT verify coupled stability inside it. This sim does.

Model: a mothership hub (host + rigid half of the 40 t bag) with a
linearSpringMassDamper slosh particle (the other 20 t, f_s=0.5) offset r_off from
the hub, coupled to a reaction-wheel ACS running MRP feedback trying to hold
inertial attitude. A soft-capture berth impulse seeds the slosh (rhoDot = v_c).
We integrate 2 h and measure, per (T_s, zeta, host) cell:
  - peak hub attitude excursion (deg)
  - settling time to < 0.5 deg sustained (s); INF if never
  - peak reaction-wheel momentum (N m s) and whether it SATURATES the wheels
  - verdict: RW-VIABLE (settles in the 30-min berth window AND no RW saturation)

Slosh mapping (SMD): omega = 2 pi / T_s ; k = m_s omega^2 ; c = 2 zeta m_s omega.
Runs on archon (bsk 2.10.2). Deterministic.
"""
import json
import math
from pathlib import Path

import numpy as np

from Basilisk.simulation import spacecraft, reactionWheelStateEffector, simpleNav
from Basilisk.simulation import linearSpringMassDamper
from Basilisk.fswAlgorithms import mrpFeedback, attTrackingError, inertial3D, rwMotorTorque
from Basilisk.utilities import (SimulationBaseClass, macros, simIncludeRW,
                                RigidBodyKinematics)
from Basilisk.architecture import messaging

RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

# --- physical anchors (R191) ---
BAG_T = 40_000.0          # kg, full bag load
F_SLOSH = 0.5             # sloshing fraction
M_SLOSH = BAG_T * F_SLOSH  # 20 t slosh particle
M_RIGID_BAG = BAG_T * (1 - F_SLOSH)  # 20 t rigid half in the hub
R_OFF = 5.0               # m, bag arm (slosh particle offset from hub CoM)
V_CAPTURE = 0.05          # m/s, soft-capture closing rate (R191 H1)
HOSTS = {"monolithic_20t": 20_000.0, "relay_4t": 4_000.0}

# --- ACS anchors (R191) ---
RW_UMAX = 5.0             # N m per-wheel torque authority (R191 "~5 N m")
RW_MAXMOM = 100.0         # N m s per-wheel momentum capacity (large-vehicle RW/CMG)
BERTH_WINDOW = 30 * 60.0  # s (30 min)
SETTLE_DEG = 0.5          # deg, "settled" attitude threshold

SIM_TIME = 2 * 3600.0     # s
DT = 0.5                  # s

# --- grid (spans R191's viable corner and its edges) ---
TS_GRID = [60.0, 100.0, 140.0, 180.0]
ZETA_GRID = [0.02, 0.05, 0.10, 0.20]


def hub_inertia(m_hub):
    # ~ solid box, char length 8 m: I ~ m * L^2 * k
    L = 8.0
    return [m_hub * L * L / 6.0 * s for s in (0.8, 1.0, 1.0)]


def run_case(T_s, zeta, host_name, seed_mode="capture_impulse", disp_amp=0.10):
    """seed_mode:
      'capture_impulse' -> slosh seeded with rhoDot=v_c (injects NET angular
         momentum L = m_s*v_c*r_off; conserved, RWs can only store it).
      'displacement'    -> slosh seeded with rhoInit=disp_amp, rhoDot=0 (NET L=0;
         mean-zero oscillation, R191's picture)."""
    m_host = HOSTS[host_name]
    m_hub = m_host + M_RIGID_BAG
    Ihub = hub_inertia(m_hub)

    scSim = SimulationBaseClass.SimBaseClass()
    proc = scSim.CreateNewProcess("proc")
    task = "task"
    proc.addTask(scSim.CreateNewTask(task, macros.sec2nano(DT)))

    # --- spacecraft hub ---
    scObject = spacecraft.Spacecraft()
    scObject.ModelTag = "bagHost"
    scObject.hub.mHub = m_hub
    scObject.hub.r_BcB_B = [[0.0], [0.0], [0.0]]
    scObject.hub.IHubPntBc_B = [[Ihub[0], 0., 0.],
                                [0., Ihub[1], 0.],
                                [0., 0., Ihub[2]]]
    scObject.hub.sigma_BNInit = [[0.0], [0.0], [0.0]]
    scObject.hub.omega_BN_BInit = [[0.0], [0.0], [0.0]]
    scSim.AddModelToTask(task, scObject)

    # --- slosh particle (linear spring-mass-damper) ---
    omega = 2 * math.pi / T_s
    k = M_SLOSH * omega ** 2
    c = 2 * zeta * M_SLOSH * omega
    lsmd = linearSpringMassDamper.LinearSpringMassDamper()
    lsmd.ModelTag = "slosh"
    lsmd.k = k
    lsmd.c = c
    lsmd.massInit = M_SLOSH
    lsmd.r_PB_B = [[0.0], [0.0], [R_OFF]]     # 5 m along +z from hub CoM
    lsmd.pHat_B = [[1.0], [0.0], [0.0]]        # slosh along x -> torque about y
    if seed_mode == "capture_impulse":
        lsmd.rhoInit = 0.0
        lsmd.rhoDotInit = V_CAPTURE            # injects net angular momentum
    else:  # displacement (mean-zero, net L = 0)
        lsmd.rhoInit = disp_amp
        lsmd.rhoDotInit = 0.0
    lsmd.nameOfRhoState = "sloshRho"
    lsmd.nameOfRhoDotState = "sloshRhoDot"
    scObject.addStateEffector(lsmd)

    # --- reaction wheels (3 orthogonal) ---
    rwFactory = simIncludeRW.rwFactory()
    for gs in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
        rwFactory.create("Honeywell_HR16", gs, maxMomentum=RW_MAXMOM,
                         u_max=RW_UMAX, Omega=0.0)
    rwEff = reactionWheelStateEffector.ReactionWheelStateEffector()
    rwFactory.addToSpacecraft("rw", rwEff, scObject)
    numRW = rwFactory.getNumOfDevices()
    scSim.AddModelToTask(task, rwEff, 5)

    # --- navigation ---
    sNav = simpleNav.SimpleNav()
    sNav.ModelTag = "nav"
    sNav.scStateInMsg.subscribeTo(scObject.scStateOutMsg)
    scSim.AddModelToTask(task, sNav)

    # --- FSW: inertial hold -> tracking error -> MRP feedback -> RW motor torque ---
    inertialRef = inertial3D.inertial3D()
    inertialRef.ModelTag = "inertialRef"
    inertialRef.sigma_R0N = [0.0, 0.0, 0.0]
    scSim.AddModelToTask(task, inertialRef)

    attErr = attTrackingError.attTrackingError()
    attErr.ModelTag = "attErr"
    scSim.AddModelToTask(task, attErr)

    mrpControl = mrpFeedback.mrpFeedback()
    mrpControl.ModelTag = "mrpFeedback"
    mrpControl.K = 3.5
    mrpControl.Ki = -1.0        # negative disables integral
    mrpControl.P = 30.0
    mrpControl.integralLimit = 0.0
    scSim.AddModelToTask(task, mrpControl)

    rwMotor = rwMotorTorque.rwMotorTorque()
    rwMotor.ModelTag = "rwMotor"
    rwMotor.controlAxes_B = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    scSim.AddModelToTask(task, rwMotor)

    # --- config messages ---
    vehConfig = messaging.VehicleConfigMsgPayload()
    vehConfig.ISCPntB_B = [Ihub[0], 0., 0., 0., Ihub[1], 0., 0., 0., Ihub[2]]
    vcMsg = messaging.VehicleConfigMsg().write(vehConfig)

    fswRwParams = rwFactory.getConfigMessage()

    # --- wiring ---
    attErr.attNavInMsg.subscribeTo(sNav.attOutMsg)
    attErr.attRefInMsg.subscribeTo(inertialRef.attRefOutMsg)
    mrpControl.guidInMsg.subscribeTo(attErr.attGuidOutMsg)
    mrpControl.vehConfigInMsg.subscribeTo(vcMsg)
    mrpControl.rwParamsInMsg.subscribeTo(fswRwParams)
    mrpControl.rwSpeedsInMsg.subscribeTo(rwEff.rwSpeedOutMsg)
    rwMotor.vehControlInMsg.subscribeTo(mrpControl.cmdTorqueOutMsg)
    rwMotor.rwParamsInMsg.subscribeTo(fswRwParams)
    rwEff.rwMotorCmdInMsg.subscribeTo(rwMotor.rwMotorTorqueOutMsg)

    # --- logging ---
    scLog = scObject.scStateOutMsg.recorder()
    rwLog = rwEff.rwSpeedOutMsg.recorder()
    scSim.AddModelToTask(task, scLog)
    scSim.AddModelToTask(task, rwLog)
    rwItemLogs = []
    for i in range(numRW):
        il = rwEff.rwOutMsgs[i].recorder()
        scSim.AddModelToTask(task, il)
        rwItemLogs.append(il)

    scSim.InitializeSimulation()
    scSim.ConfigureStopTime(macros.sec2nano(SIM_TIME))
    scSim.ExecuteSimulation()

    # --- metrics ---
    sigma = np.array(scLog.sigma_BN)               # Nx3 MRP
    omega = np.array(scLog.omega_BN_B)             # Nx3 rad/s
    t = np.array(scLog.times()) * macros.NANO2SEC
    # attitude angle from MRP norm: theta = 4 atan(|sigma|); cap at 180
    ang_deg = np.degrees(4.0 * np.arctan(np.linalg.norm(sigma, axis=1)))
    peak_deg = float(min(np.max(ang_deg), 180.0))
    # residual body angular momentum at sim end (I_hub . omega_end)
    L_body_end = float(np.linalg.norm(np.array(Ihub) * omega[-1]))

    # settling: last time it EXCEEDS threshold; settled after that
    over = np.where(ang_deg > SETTLE_DEG)[0]
    settle_s = float(t[over[-1]]) if len(over) else 0.0
    if len(over) and over[-1] >= len(t) - 2:
        settle_s = float("inf")                    # still ringing at sim end

    # RW momentum: h_i = Js * Omega_i  (per wheel)
    Js = 0.025  # HR16 spin inertia ~ used only if item logs lack useful field
    peak_h = 0.0
    saturated = False
    for il in rwItemLogs:
        Omega = np.array(il.Omega)                 # rad/s
        h = np.array(il.Js)[0] * Omega if hasattr(il, "Js") else Js * Omega
        peak_h = max(peak_h, float(np.max(np.abs(h))))
        if np.max(np.abs(h)) >= RW_MAXMOM * 0.999:
            saturated = True

    settles_in_window = settle_s <= BERTH_WINDOW
    rw_viable = settles_in_window and not saturated

    injected_L = M_SLOSH * V_CAPTURE * R_OFF if seed_mode == "capture_impulse" else 0.0
    return {
        "T_s": T_s, "zeta": zeta, "host": host_name, "seed_mode": seed_mode,
        "k_N_per_m": round(k, 3), "c_Ns_per_m": round(c, 2),
        "mass_ratio_slosh_to_host": round(M_SLOSH / m_host, 2),
        "peak_attitude_deg": round(peak_deg, 2),
        "settle_s": settle_s if math.isinf(settle_s) else round(settle_s),
        "settles_in_30min": settles_in_window,
        "peak_rw_momentum_Nms": round(peak_h, 1),
        "rw_saturates": saturated,
        "rw_viable": rw_viable,
        "injected_angular_momentum_Nms": round(injected_L, 1),
        "residual_body_L_end_Nms": round(L_body_end, 1),
    }


def run_grid(seed_mode):
    cells = []
    for host in HOSTS:
        for T_s in TS_GRID:
            for zeta in ZETA_GRID:
                try:
                    c = run_case(T_s, zeta, host, seed_mode=seed_mode)
                    cells.append(c)
                    print(f"[{seed_mode:16}|{host:14}] T_s={T_s:5.0f} z={zeta:.2f} "
                          f"-> peak {c['peak_attitude_deg']:6.2f} deg, settle "
                          f"{c['settle_s']}, h_rw {c['peak_rw_momentum_Nms']:6.1f} "
                          f"{'SAT' if c['rw_saturates'] else '   '} "
                          f"{'VIABLE' if c['rw_viable'] else ''}")
                except Exception as e:
                    print(f"[{seed_mode}|{host}] T_s={T_s} z={zeta} FAILED: {e!r}")
                    cells.append({"T_s": T_s, "zeta": zeta, "host": host,
                                  "seed_mode": seed_mode, "error": repr(e)})
    return cells


def summarize(cells):
    ok = [c for c in cells if "error" not in c]
    n = len(ok) or 1
    return {
        "n_cells": len(ok),
        "n_settle_in_window": sum(c["settles_in_30min"] for c in ok),
        "n_rw_saturates": sum(c["rw_saturates"] for c in ok),
        "n_rw_viable": sum(c["rw_viable"] for c in ok),
        "pct_rw_viable": round(100 * sum(c["rw_viable"] for c in ok) / n),
    }


def main():
    out = {
        "anchors": {
            "m_slosh_kg": M_SLOSH, "r_off_m": R_OFF, "v_capture_m_s": V_CAPTURE,
            "rw_umax_Nm": RW_UMAX, "rw_maxmom_Nms": RW_MAXMOM,
            "berth_window_s": BERTH_WINDOW,
            "capture_injected_L_Nms": round(M_SLOSH * V_CAPTURE * R_OFF, 1),
            "thruster_dump_time_s": round(M_SLOSH * V_CAPTURE * R_OFF / 50.0, 1),
        },
    }
    for mode in ("capture_impulse", "displacement"):
        cells = run_grid(mode)
        out[mode] = {"summary": summarize(cells), "cells": cells}
        print(f"\n== {mode} summary:", out[mode]["summary"])
    (RESULTS / "bag_6dof_findings.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
