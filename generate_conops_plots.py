#!/usr/bin/env python3
"""
Generate polished mission-phase plots for the ICEBERG ConOps document.

Two visual themes:
  - "space" (dark, glow): orbital and trajectory plots
  - "dashboard" (clean modern): bar charts, timelines, schematics
"""

import os
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm
from matplotlib.collections import LineCollection
from matplotlib.patheffects import withStroke

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
os.makedirs(OUT_DIR, exist_ok=True)

# Pick the best available sans-serif on macOS
candidates = ['Inter', 'SF Pro Display', 'Helvetica Neue', 'Helvetica', 'Arial', 'DejaVu Sans']
available = {f.name for f in fm.fontManager.ttflist}
SANS = next((c for c in candidates if c in available), 'sans-serif')

# ============================================================================
# Color palette — restrained, sophisticated
# ============================================================================
INK_DARK   = '#0a0e1a'       # deep space
INK_PANEL  = '#11182a'
INK_GRID   = '#1f2a44'
INK_TEXT   = '#e6edf5'
INK_MUTED  = '#8a96b0'

ACCENT_GOLD   = '#e8b54e'    # Saturn / sun
ACCENT_BLUE   = '#5fa8ff'    # outbound spacecraft
ACCENT_TEAL   = '#3ed4c0'    # ice / chunk-fed
ACCENT_RED    = '#ff7676'    # critical / capture
ACCENT_GREEN  = '#7adc7a'    # success / depot

# Dashboard palette
DASH_BG    = '#ffffff'
DASH_FG    = '#1a1f2e'
DASH_MUTED = '#5a6378'
DASH_GRID  = '#e6e8ed'
DASH_BLUE  = '#3b6ee5'
DASH_TEAL  = '#0fb9a3'
DASH_RED   = '#dc4a4a'
DASH_AMBER = '#d49612'
DASH_GREEN = '#2c9c4f'

def style_space():
    plt.rcParams.update({
        'font.family': SANS,
        'font.size': 14,
        'figure.facecolor': INK_DARK,
        'axes.facecolor': INK_DARK,
        'savefig.facecolor': INK_DARK,
        'axes.edgecolor': INK_GRID,
        'axes.labelcolor': INK_TEXT,
        'axes.titlecolor': INK_TEXT,
        'axes.titleweight': 'bold',
        'axes.titlesize': 18,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 13,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': False,
        'axes.spines.bottom': False,
        'xtick.color': INK_MUTED,
        'ytick.color': INK_MUTED,
        'grid.color': INK_GRID,
        'grid.alpha': 0.4,
        'grid.linewidth': 0.5,
        'legend.facecolor': INK_PANEL,
        'legend.edgecolor': INK_GRID,
        'legend.labelcolor': INK_TEXT,
        'legend.framealpha': 0.95,
        'figure.dpi': 100,
        'savefig.dpi': 110,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.3,
    })

def style_dashboard():
    plt.rcParams.update({
        'font.family': SANS,
        'font.size': 14,
        'figure.facecolor': DASH_BG,
        'axes.facecolor': DASH_BG,
        'savefig.facecolor': DASH_BG,
        'axes.edgecolor': DASH_GRID,
        'axes.labelcolor': DASH_FG,
        'axes.titlecolor': DASH_FG,
        'axes.titleweight': 'bold',
        'axes.titlesize': 18,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 13,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': False,
        'xtick.color': DASH_MUTED,
        'ytick.color': DASH_MUTED,
        'xtick.major.size': 0,
        'ytick.major.size': 0,
        'grid.color': DASH_GRID,
        'grid.alpha': 1.0,
        'grid.linewidth': 0.7,
        'legend.facecolor': '#fafbfc',
        'legend.edgecolor': DASH_GRID,
        'legend.labelcolor': DASH_FG,
        'legend.framealpha': 1.0,
        'figure.dpi': 100,
        'savefig.dpi': 110,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.3,
    })

def glow_line(ax, x, y, color, lw=2.0, alpha_main=1.0, n_glow=4, glow_lw_step=2.5):
    """Draw a line with a soft glow — for trajectory plots."""
    for i in range(n_glow, 0, -1):
        ax.plot(x, y, color=color, lw=lw + i*glow_lw_step,
                alpha=0.06, solid_capstyle='round')
    ax.plot(x, y, color=color, lw=lw, alpha=alpha_main, solid_capstyle='round')

def add_starfield(ax, n=200, seed=42):
    rng = np.random.default_rng(seed)
    xlim = ax.get_xlim(); ylim = ax.get_ylim()
    xs = rng.uniform(*xlim, n); ys = rng.uniform(*ylim, n)
    sizes = rng.exponential(0.4, n)
    alphas = rng.uniform(0.1, 0.6, n)
    ax.scatter(xs, ys, s=sizes, c='white', alpha=alphas, zorder=0, linewidths=0)

# ============================================================================
# Constants
# ============================================================================
GM_SUN    = 1.32712440018e11
GM_SATURN = 3.7931187e7
AU        = 1.495978707e8
R_EARTH_ORB  = 1.0 * AU
R_SATURN_ORB = 9.5826 * AU
R_SATURN  = 60268.0
R_BRING   = 102000.0

# ============================================================================
# Plot 1: Heliocentric round-trip
# ============================================================================
def plot_mission_flightplan():
    """Apollo-1967-style horizontal mission flight plan with numbered phases and spacecraft silhouettes."""
    style_space()
    fig, ax = plt.subplots(figsize=(22, 14))

    # Layout: serpentine path — outbound (top row, L->R), Saturn ops (right loop), inbound (bottom row, R->L)
    # Coordinate space: x in [0, 100], y in [0, 60]

    # Two-row layout: top row at y=52, bottom row at y=18, Saturn loop at right edge (x=92, y=35)
    phases = [
        ( 8, 52, '1', 'LAUNCH',
          ['Falcon Heavy', 'expendable',  '~50 t to LEO'],
          'T+0',                ACCENT_RED),
        (24, 52, '2', 'TSI BURN',
          ['Vulcan-Centaur', 'kick stage', '7.3 km/s', 'jettison'],
          'T+1 day',            ACCENT_RED),
        (44, 52, '3', 'OUTBOUND CRUISE',
          ['Hohmann ellipse', 'water-MET', 'trim burns only', 'Earth-launched H₂O'],
          '6.1 years',          ACCENT_BLUE),
        (62, 52, '4', 'SATURN ARRIVAL',
          ['multi-pass capture', 'water-MET', '~1.0 km/s', 'Dawn-style spiral'],
          'T+6.1 yr',           ACCENT_GOLD),
        (80, 52, '5', 'RING RENDEZVOUS',
          ['drop to B-ring', '~0.5 km/s', 'phasing drift'],
          '+30 d',              ACCENT_GOLD),
        (94, 35, '6', 'TRAWL + CINCH',
          ['bag deployed', 'particles in', 'autonomous', '83 min light-time'],
          '+hours-days',        ACCENT_TEAL),
        (80, 18, '7', 'SATURN DEPART',
          ['~1.5 km/s', 'CHUNK-FED', 'multi-pass spiral'],
          '+90 d',              ACCENT_GREEN),
        (62, 18, '8', 'INBOUND CRUISE',
          ['continuous thrust', 'CHUNK-FED retrograde', 'cargo = prop tank'],
          '7 years',            ACCENT_GREEN),
        (44, 18, '9', 'LUNAR FLYBY TOUR',
          ['2–3 LGA passes', '~3 km/s FREE', 'no atmosphere', 'no melting'],
          '+3–6 mo',            '#e8b54e'),
        (24, 18, '10', 'LEO DEPOT',
          ['low-thrust trim', '~0.5 km/s', 'water RCS dock', 'CARGO DELIVERED'],
          'T+13 yr',            ACCENT_GREEN),
    ]

    # === Connect phases with arrows ===
    for i in range(len(phases) - 1):
        x1, y1 = phases[i][0], phases[i][1]
        x2, y2 = phases[i+1][0], phases[i+1][1]
        if i == 4:  # 5 -> 6 (top-right corner: down-right)
            arc_x = np.array([x1+4, x1+10, x2])
            arc_y = np.array([y1, y1-4, y2+5])
            from scipy.interpolate import CubicSpline
            cs = CubicSpline([0, 0.5, 1], np.column_stack([arc_x, arc_y]), axis=0)
            t = np.linspace(0, 1, 60)
            pts = cs(t)
            ax.plot(pts[:,0], pts[:,1], color=ACCENT_GOLD, lw=2.2, alpha=0.85)
            ax.annotate('', xy=(pts[-1,0], pts[-1,1]),
                        xytext=(pts[-3,0], pts[-3,1]),
                        arrowprops=dict(arrowstyle='->', color=ACCENT_GOLD, lw=2.2))
        elif i == 5:  # 6 -> 7 (bottom-right corner: down-left)
            arc_x = np.array([x1, x1-4, x2+4])
            arc_y = np.array([y1-5, y1-10, y2])
            from scipy.interpolate import CubicSpline
            cs = CubicSpline([0, 0.5, 1], np.column_stack([arc_x, arc_y]), axis=0)
            t = np.linspace(0, 1, 60)
            pts = cs(t)
            ax.plot(pts[:,0], pts[:,1], color=ACCENT_TEAL, lw=2.2, alpha=0.85)
            ax.annotate('', xy=(pts[-1,0], pts[-1,1]),
                        xytext=(pts[-3,0], pts[-3,1]),
                        arrowprops=dict(arrowstyle='->', color=ACCENT_TEAL, lw=2.2))
        else:
            # Determine arrow direction for top vs bottom row
            if y1 == y2:
                # Same row, straight line. Top row: L->R (i=0,1,2,3). Bottom row: R->L (i=6,7,8).
                if x1 < x2:
                    ax.annotate('', xy=(x2-4.8, y2), xytext=(x1+4.8, y1),
                                arrowprops=dict(arrowstyle='->', color=INK_MUTED,
                                                lw=1.8, alpha=0.7))
                else:
                    ax.annotate('', xy=(x2+4.8, y2), xytext=(x1-4.8, y1),
                                arrowprops=dict(arrowstyle='->', color=INK_MUTED,
                                                lw=1.8, alpha=0.7))

    # === Draw each station ===
    for (x, y, num, title, sublines, dur, color) in phases:
        # Station marker
        circ = plt.Circle((x, y), 4.0, facecolor=INK_PANEL, edgecolor=color,
                          lw=3.0, zorder=5)
        ax.add_patch(circ)
        ax.text(x, y, num, color=color, ha='center', va='center',
                fontsize=25, fontweight='bold', zorder=6)

        # Title above station
        ax.text(x, y+5.6, title, color=color, ha='center', va='bottom',
                fontsize=18, fontweight='bold', zorder=6)

        # Sublines below
        for j, line in enumerate(sublines):
            ax.text(x, y - 5.6 - j*1.6, line, color=INK_TEXT, ha='center',
                    va='top', fontsize=20, alpha=0.92, zorder=6)

        # Duration
        ax.text(x, y - 5.6 - len(sublines)*1.6 - 0.5, dur, color=INK_MUTED,
                ha='center', va='top', fontsize=20, fontweight='bold',
                style='italic', zorder=6)

    # === Iconography: Sun, Earth, Saturn, Moon ===
    # Sun in center
    ax.plot(54, 35, marker='o', markersize=42, color=ACCENT_GOLD, alpha=0.12, zorder=2)
    ax.plot(54, 35, marker='o', markersize=22, color=ACCENT_GOLD, zorder=2)
    ax.text(54, 31, 'SUN', color=ACCENT_GOLD, fontsize=20, ha='center',
            fontweight='bold', alpha=0.7)

    # Earth near phase 1 (top-left)
    ax.plot(3, 52, marker='o', markersize=14, color=ACCENT_BLUE, zorder=3)
    ax.text(3, 47.5, 'EARTH', color=ACCENT_BLUE, fontsize=19, ha='center',
            fontweight='bold')

    # Saturn near phases 4-5 (top right area, slightly above)
    from matplotlib.patches import Ellipse
    ax.plot(72, 60, marker='o', markersize=20, color=ACCENT_GOLD, alpha=0.25, zorder=2)
    ax.plot(72, 60, marker='o', markersize=14, color=ACCENT_GOLD, zorder=2)
    ring_e = Ellipse((72, 60), width=12, height=2.2, fill=False,
                     edgecolor=ACCENT_GOLD, lw=1.4, alpha=0.65, zorder=1)
    ax.add_patch(ring_e)
    ax.text(72, 64.5, 'SATURN', color=ACCENT_GOLD, fontsize=19, ha='center',
            fontweight='bold')

    # Moon near phase 9 — placed in empty mid-canvas to avoid label collision
    ax.plot(54, 1, marker='o', markersize=10, color=INK_MUTED, zorder=3)
    ax.text(57, 1, 'MOON', color=INK_MUTED, fontsize=18, ha='left',
            va='center', fontweight='bold')

    # === Legend / propulsion key (top-left, out of the phase rows) ===
    legend_x = 1
    legend_y = 73
    legend_items = [
        ('Bought (chemical, jettisoned)',                  ACCENT_RED),
        ('water-MET — Earth-launched water',          ACCENT_BLUE),
        ('water-MET — chunk-fed (Saturn ring water)', ACCENT_GREEN),
        ('Lunar gravity-assist — FREE',                    '#e8b54e'),
    ]
    ax.text(legend_x, legend_y + 5, 'PROPULSION KEY',
            color=INK_TEXT, fontsize=24, fontweight='bold', alpha=0.95)
    for i, (label, color) in enumerate(legend_items):
        ax.add_patch(plt.Rectangle((legend_x, legend_y + 3 - i*2.0), 3.5, 1.0,
                                    facecolor=color, edgecolor='none'))
        ax.text(legend_x + 4.5, legend_y + 3.5 - i*2.0, label, color=INK_TEXT,
                fontsize=19, va='center')

    # === Top-line summary, top-right (out of phase rows) ===
    ax.text(99, 78,
            'Round-trip: 13 years\n'
            'Bought ΔV: 7.3 km/s\n'
            'Water-MET ΔV: ~5.7 km/s\n'
            'Free LGA ΔV: ~3 km/s',
            color=ACCENT_GOLD, fontsize=24, fontweight='bold', ha='right',
            va='top',
            bbox=dict(facecolor=INK_PANEL, edgecolor=ACCENT_GOLD,
                      boxstyle='round,pad=0.8', lw=1.5))

    add_starfield(ax, n=200, seed=7)

    ax.set_xlim(-2, 102)
    ax.set_ylim(-2, 84)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    fig.suptitle('Project ICEBERG  -  Mission flight plan',
                 color=INK_TEXT, fontsize=27, fontweight='bold', x=0.05,
                 ha='left', y=0.98)
    fig.text(0.05, 0.945,
             '13-year round-trip   |   10 phases   |   one bought burn',
             color=INK_MUTED, fontsize=18, fontweight='normal', ha='left')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '01a_flightplan.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 1 (legacy): Heliocentric orbit overview
# ============================================================================
def plot_heliocentric():
    style_space()
    fig, ax = plt.subplots(figsize=(14, 10))

    # Sun
    for sz, alpha in [(45, 0.15), (32, 0.25), (22, 0.4), (16, 1.0)]:
        ax.plot(0, 0, marker='o', markersize=sz, color=ACCENT_GOLD,
                alpha=alpha, zorder=5, markeredgewidth=0)
    ax.text(0, -0.7, 'SUN', ha='center', fontsize=13, color=ACCENT_GOLD,
            zorder=5, fontweight='bold')

    # Planet orbits (subtle dotted)
    theta = np.linspace(0, 2*np.pi, 360)
    ax.plot(np.cos(theta), np.sin(theta), color='#5fa8ff', alpha=0.18,
            lw=0.8, ls=(0, (1, 4)))
    ax.plot(9.5826*np.cos(theta), 9.5826*np.sin(theta),
            color=ACCENT_GOLD, alpha=0.18, lw=0.8, ls=(0, (1, 4)))

    # Hohmann ellipse params
    a_t = (1 + 9.5826)/2
    c   = a_t - 1
    b_t = np.sqrt(a_t**2 - c**2)

    # OUTBOUND arc — coast with periodic trim-burn tick marks
    e_th = np.linspace(0, np.pi, 400)
    out_x = a_t*np.cos(e_th) - c
    out_y = b_t*np.sin(e_th)
    glow_line(ax, out_x, out_y, ACCENT_BLUE, lw=2.0, alpha_main=0.95, n_glow=3)

    # Outbound trim tick marks
    for frac in [0.20, 0.40, 0.60, 0.80]:
        i = int(frac * len(e_th))
        dx = out_x[i+1]-out_x[i-1]; dy = out_y[i+1]-out_y[i-1]
        norm = np.hypot(dx,dy)
        nx, ny = -dy/norm*0.22, dx/norm*0.22
        ax.plot([out_x[i]-nx, out_x[i]+nx], [out_y[i]-ny, out_y[i]+ny],
                color=ACCENT_BLUE, lw=2.6, alpha=0.95, solid_capstyle='round')

    # Outbound direction arrow
    mid = len(e_th)//2
    dx = out_x[mid+1]-out_x[mid-1]; dy = out_y[mid+1]-out_y[mid-1]
    norm = np.hypot(dx,dy)
    ax.annotate('', xy=(out_x[mid]+dx*0.6/norm, out_y[mid]+dy*0.6/norm),
                xytext=(out_x[mid]-dx*0.6/norm, out_y[mid]-dy*0.6/norm),
                arrowprops=dict(arrowstyle='->', color=ACCENT_BLUE, lw=2.6))

    # INBOUND arc — continuous chunk-fed thrust (chevrons)
    in_th = np.linspace(np.pi, 2*np.pi, 400)
    in_x = a_t*np.cos(in_th) - c
    in_y = b_t*np.sin(in_th)
    glow_line(ax, in_x, in_y, ACCENT_TEAL, lw=2.4, alpha_main=0.95, n_glow=4)

    for frac in [0.15, 0.30, 0.45, 0.60, 0.75, 0.90]:
        i = int(frac * len(in_th))
        dx = in_x[i+1]-in_x[i-1]; dy = in_y[i+1]-in_y[i-1]
        norm = np.hypot(dx,dy)
        ax.annotate('', xy=(in_x[i]+dx*0.35/norm, in_y[i]+dy*0.35/norm),
                    xytext=(in_x[i]-dx*0.05/norm, in_y[i]-dy*0.05/norm),
                    arrowprops=dict(arrowstyle='->', color=ACCENT_TEAL,
                                    lw=2.0, alpha=0.95))

    # Event markers (red stars at burns and Saturn ops)
    ax.plot(1, 0, marker='*', markersize=24, color=ACCENT_RED,
            markeredgecolor='white', markeredgewidth=1.4, zorder=10)
    ax.plot(-9.5826, 0, marker='*', markersize=24, color=ACCENT_RED,
            markeredgecolor='white', markeredgewidth=1.4, zorder=10)
    ax.plot(0.94, -0.35, marker='*', markersize=18, color=ACCENT_RED,
            markeredgecolor='white', markeredgewidth=1.2, zorder=10)

    # Body markers (planets)
    ax.plot(1, 0, marker='o', markersize=8, color=ACCENT_BLUE,
            markeredgewidth=0, zorder=8)
    ax.plot(-9.5826, 0, marker='o', markersize=11, color=ACCENT_GOLD,
            markeredgewidth=0, zorder=8)

    # Phase callout boxes
    def callout(x, y, lines, color, ha='left'):
        s = '\n'.join(lines)
        ax.text(x, y, s, fontsize=13.5, color=color, ha=ha, va='top',
                bbox=dict(facecolor=INK_PANEL, edgecolor=color, alpha=0.85,
                          boxstyle='round,pad=0.5', linewidth=1))

    callout(2.2, 1.9,
            ['PHASE 1-2:  LEO + TSI BURN',
             'Bought launch (FH / Starship)',
             'Bought chemical kick stage  ~7.3 km/s',
             'Stage jettisoned',
             '(only non-water-MET prop in mission)'],
            ACCENT_RED)

    callout(2.2, -1.2,
            ['PHASE 9-10:  LUNAR FLYBY CAPTURE + LEO DEPOT',
             '2-3 lunar gravity-assists (~3 km/s free)',
             'water MET trim to LEO, chunk-fed'],
            ACCENT_TEAL)

    callout(-3.5, 5.7,
            ['PHASE 3:  OUTBOUND CRUISE  ~6.1 yr',
             'Heliocentric Hohmann ellipse',
             'water MET in plasma mode',
             'Earth-launched water for trim',
             '(tick-marks = trim-burn windows)'],
            ACCENT_BLUE)

    callout(-14.3, 2.7,
            ['PHASES 4-7:  SATURN OPERATIONS',
             'water MET capture',
             '  (multi-pass, 30-60 d)',
             'Ring rendezvous + grapple',
             'Bag deploy around chunk',
             'water MET departure',
             '  (chunk-fed)',
             '~6 months in Saturn system'],
            ACCENT_RED)

    callout(-3.5, -7.0,
            ['PHASE 8:  INBOUND CRUISE  ~6.1 yr',
             'Heliocentric Hohmann (return)',
             'water MET continuous low-thrust',
             'Propellant fed from chunk via bag',
             '(chevrons = active thrust)'],
            ACCENT_TEAL)

    # Body labels (small, near markers)
    ax.text(1.0, 0.30, 'EARTH', fontsize=18, color=ACCENT_BLUE,
            fontweight='bold', ha='center')
    ax.text(-9.5826, 0.45, 'SATURN', fontsize=18, color=ACCENT_GOLD,
            fontweight='bold', ha='center')

    ax.set_xlim(-15.5, 7.5)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)
    add_starfield(ax, n=220)

    fig.suptitle('Mission phase map  -  heliocentric frame',
                 color=INK_TEXT, fontsize=19, fontweight='bold', y=0.97)
    ax.set_title('Red stars = discrete propulsion events.   Tick-marks = outbound trim burns.   Chevrons = inbound continuous low-thrust.',
                 fontsize=19, color=INK_MUTED, fontweight='normal', pad=10)

    out = os.path.join(OUT_DIR, '01_heliocentric.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 2: Saturn capture geometry
# ============================================================================
def plot_saturn_capture():
    style_space()
    fig, ax = plt.subplots(figsize=(10, 8))

    # Saturn body with a soft glow
    for sz, alpha in [(180, 0.05), (140, 0.10), (110, 0.20), (90, 0.55), (75, 1.0)]:
        ax.add_patch(plt.Circle((0,0), sz, color=ACCENT_GOLD, alpha=alpha, zorder=2))
    ax.text(0, 0, 'SATURN', ha='center', va='center', color=INK_DARK,
            fontweight='bold', fontsize=19, zorder=4)

    # Rings — concentric thin lines
    for r in np.linspace(91, 117, 14):
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(r*np.cos(theta), r*np.sin(theta), color=ACCENT_GOLD,
                alpha=0.15, lw=0.6)
    for r in np.linspace(122, 137, 8):
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(r*np.cos(theta), r*np.sin(theta), color=ACCENT_GOLD,
                alpha=0.10, lw=0.5)

    # Hyperbolic approach: tuned so periapsis is at r_p ~ 150,000 km (well outside rings at 137k)
    # Hyperbola form r = p/(1+e*cos(nu)); at nu=0 -> periapsis = p/(1+e)
    e_hyp = 1.6
    r_p   = 150.0   # thousand km, periapsis outside A-ring
    p_hyp = r_p*(1+e_hyp)   # semi-latus rectum
    nu = np.linspace(-1.95, 0, 200)
    r_hyp = p_hyp / (1 + e_hyp*np.cos(nu))
    x_hyp = r_hyp*np.cos(nu)
    y_hyp = r_hyp*np.sin(nu)
    glow_line(ax, x_hyp, y_hyp, ACCENT_BLUE, lw=2.0)

    # Capture burn marker — at periapsis (rightmost point of hyperbola = (r_p, 0))
    ax.plot(r_p, 0, marker='*', markersize=22, color=ACCENT_RED,
            markeredgecolor='white', markeredgewidth=1, zorder=8)
    ax.annotate('CAPTURE SEQUENCE\n~0.6 km/s\nwater MET\n(multi-pass low-thrust,\n~30-60 days)',
                xy=(r_p, 0), xytext=(r_p+150, -250),
                fontsize=18, color=ACCENT_RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=ACCENT_RED, lw=1.4))

    # Captured elliptical orbit: focus at Saturn (origin), periapsis at +x = r_p
    # Make it genuinely highly elliptical so the apoapsis is far enough that
    # the orbit clearly does not pass through Saturn.
    r_a   = 1500.0   # thousand km apoapsis
    a_e   = 0.5*(r_p + r_a)
    e_e   = (r_a - r_p) / (r_a + r_p)
    th = np.linspace(-np.pi, np.pi, 400)
    r_e = a_e*(1-e_e**2)/(1+e_e*np.cos(th))
    x_e = r_e*np.cos(th)
    y_e = r_e*np.sin(th)
    glow_line(ax, x_e, y_e, ACCENT_TEAL, lw=1.5, alpha_main=0.7, n_glow=2)
    ax.text(-1100, 150, 'captured highly\nelliptical orbit\n(periapsis just outside\nA-ring)',
            fontsize=13.5, color=ACCENT_TEAL, alpha=0.9, ha='left', style='italic')

    # Approach annotation
    ax.text(x_hyp[20]+30, y_hyp[20]-30, 'V∞ ≈ 5.4 km/s\n(post-cruise)',
            fontsize=13.5, color=ACCENT_BLUE, ha='left', alpha=0.9)

    ax.set_xlim(-1700, 500)
    ax.set_ylim(-1100, 1100)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)
    add_starfield(ax, n=120, seed=7)

    fig.suptitle('Saturn arrival & capture',
                 color=INK_TEXT, fontsize=19, fontweight='bold', y=0.95)
    ax.set_title('Hyperbolic approach; water MET multi-pass low-thrust capture into highly elliptical orbit',
                 fontsize=19.5, color=INK_MUTED, fontweight='normal', pad=10)

    out = os.path.join(OUT_DIR, '02_saturn_capture.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 3: Ring rendezvous (Hohmann + phasing)
# ============================================================================
def two_body_rhs(t, s):
    x, y, vx, vy = s
    r = np.sqrt(x*x+y*y)
    return [vx, vy, -GM_SATURN*x/r**3, -GM_SATURN*y/r**3]

def state_at_circular(r, theta_deg):
    th = theta_deg*np.pi/180
    v = np.sqrt(GM_SATURN/r)
    return np.array([r*np.cos(th), r*np.sin(th), -v*np.sin(th), v*np.cos(th)])

def integrate(s0, tspan, max_step=30.0):
    sol = solve_ivp(two_body_rhs, tspan, s0, method='RK45',
                    rtol=1e-9, atol=1e-9, max_step=max_step)
    return sol.y.T

def plot_ring_rendezvous():
    SC_R0 = 95000.0
    target0 = state_at_circular(R_BRING, 90.0)
    sc0     = state_at_circular(SC_R0, 60.0)

    a_t = 0.5*(SC_R0+R_BRING)
    v_p_t = np.sqrt(GM_SATURN*(2/SC_R0 - 1/a_t))
    v_a_t = np.sqrt(GM_SATURN*(2/R_BRING - 1/a_t))
    dv1 = v_p_t - np.sqrt(GM_SATURN/SC_R0)
    dv2 = np.sqrt(GM_SATURN/R_BRING) - v_a_t
    T_h = np.pi*np.sqrt(a_t**3/GM_SATURN)
    phat = sc0[2:]/np.linalg.norm(sc0[2:])
    sc1 = sc0.copy(); sc1[2]+=dv1*phat[0]; sc1[3]+=dv1*phat[1]
    h1  = integrate(sc1, (0, T_h))
    h1t = integrate(target0, (0, T_h))

    sc1_end = h1[-1].copy()
    phat = sc1_end[2:]/np.linalg.norm(sc1_end[2:])
    sc2 = sc1_end.copy(); sc2[2]+=dv2*phat[0]; sc2[3]+=dv2*phat[1]

    target_now = h1t[-1]
    sc_th = np.arctan2(sc2[1], sc2[0])
    tg_th = np.arctan2(target_now[1], target_now[0])
    pdiff = (tg_th - sc_th + 2*np.pi)%(2*np.pi)
    T_target = 2*np.pi*np.sqrt(R_BRING**3/GM_SATURN)
    T_phase  = T_target*(1 - pdiff/(2*np.pi))
    a_phase  = (T_phase**2 * GM_SATURN/(4*np.pi**2))**(1/3)
    v_at = np.sqrt(GM_SATURN*(2/R_BRING - 1/a_phase))
    dv_p = np.sqrt(GM_SATURN/R_BRING) - v_at
    phat = sc2[2:]/np.linalg.norm(sc2[2:])
    sc3 = sc2.copy(); sc3[2]-=dv_p*phat[0]; sc3[3]-=dv_p*phat[1]
    h2  = integrate(sc3, (0, T_phase))
    h2t = integrate(target_now, (0, T_phase))

    style_space()
    fig, ax = plt.subplots(figsize=(10, 9))

    # Saturn
    for sz, alpha in [(120, 0.05), (90, 0.10), (75, 0.25), (R_SATURN/1000, 1.0)]:
        ax.add_patch(plt.Circle((0,0), sz, color=ACCENT_GOLD, alpha=alpha, zorder=2))
    ax.text(0, 0, 'SAT', ha='center', va='center', color=INK_DARK,
            fontweight='bold', fontsize=18, zorder=4)

    # Rings
    for r in np.linspace(91, 117, 14):
        theta = np.linspace(0, 2*np.pi, 200)
        ax.plot(r*np.cos(theta), r*np.sin(theta), color=ACCENT_GOLD,
                alpha=0.12, lw=0.6)

    # Target trajectory (dashed throughout)
    target_x = np.concatenate([h1t[:,0], h2t[:,0]])/1000
    target_y = np.concatenate([h1t[:,1], h2t[:,1]])/1000
    ax.plot(target_x, target_y, color=ACCENT_RED, alpha=0.45, lw=1, ls=(0, (3, 3)))

    # Hohmann phase
    glow_line(ax, h1[:,0]/1000, h1[:,1]/1000, ACCENT_BLUE, lw=2.3, n_glow=3)
    # Phasing phase
    glow_line(ax, h2[:,0]/1000, h2[:,1]/1000, ACCENT_TEAL, lw=2.3, n_glow=3)

    # SC start
    ax.plot(sc0[0]/1000, sc0[1]/1000, marker='o', markersize=10,
            color=ACCENT_BLUE, markeredgecolor='white', markeredgewidth=1.5,
            zorder=8)
    ax.text(sc0[0]/1000+5, sc0[1]/1000-7, 'START', color=ACCENT_BLUE,
            fontsize=13, fontweight='bold')

    # Target chunk
    ax.plot(target0[0]/1000, target0[1]/1000, marker='*', markersize=18,
            color=ACCENT_RED, markeredgecolor='white', markeredgewidth=1.2, zorder=8)
    ax.text(target0[0]/1000+4, target0[1]/1000+4, 'TARGET\nCHUNK',
            color=ACCENT_RED, fontsize=13, fontweight='bold')

    # ΔV labels per phase
    mid1 = len(h1)//2
    ax.text(h1[mid1,0]/1000-15, h1[mid1,1]/1000+10,
            'PHASE 1\nHohmann\n~700 m/s', color=ACCENT_BLUE, fontsize=18,
            fontweight='bold', ha='center', alpha=0.95)
    mid2 = len(h2)//2
    ax.text(h2[mid2,0]/1000-25, h2[mid2,1]/1000-5,
            'PHASE 2\nPhasing drift\n~790 m/s', color=ACCENT_TEAL,
            fontsize=18, fontweight='bold', ha='center', alpha=0.95)

    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False)
    add_starfield(ax, n=140, seed=11)

    fig.suptitle('Ring rendezvous — Saturn-centered',
                 color=INK_TEXT, fontsize=19, fontweight='bold', y=0.97)
    ax.set_title(f'Total Saturn-side rendezvous ΔV ≈ 1.49 km/s   •   B-ring radius {R_BRING:.0f} km',
                 fontsize=19.5, color=INK_MUTED, fontweight='normal', pad=10)

    out = os.path.join(OUT_DIR, '03_ring_rendezvous.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 4: Close approach
# ============================================================================
def plot_close_approach():
    style_dashboard()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

    t = np.linspace(0, 1800, 300)
    range_curve = 1000 - 0.5*t/(1+0.0005*t**1.5)
    range_curve = np.clip(range_curve, 8, None)
    rel_speed = 0.5 - 0.000003*t**1.7
    rel_speed = np.clip(rel_speed, 0.005, None)

    # Range plot
    ax = axes[0]
    ax.fill_between(t/60, range_curve, 8, color=DASH_BLUE, alpha=0.08)
    ax.plot(t/60, range_curve, color=DASH_BLUE, lw=2.4)
    ax.axhline(10, color=DASH_RED, lw=1.2, ls=(0, (4, 3)), alpha=0.8)
    ax.text(0.5, 14, 'capture envelope (10 m)', color=DASH_RED, fontsize=18.5,
            fontweight='bold')
    ax.set_xlabel('Time from approach start (min)', color=DASH_MUTED)
    ax.set_ylabel('Range to chunk (m)', color=DASH_MUTED)
    ax.set_title('Range vs. time', loc='left', pad=12)
    ax.set_yscale('log')
    ax.grid(axis='y', alpha=1.0)
    ax.set_axisbelow(True)

    # Relative speed plot
    ax = axes[1]
    ax.fill_between(t/60, rel_speed*100, 0, color=DASH_TEAL, alpha=0.08)
    ax.plot(t/60, rel_speed*100, color=DASH_TEAL, lw=2.4)
    ax.axhline(1, color=DASH_RED, lw=1.2, ls=(0, (4, 3)), alpha=0.8)
    ax.text(0.5, 2.5, 'soft-capture envelope (<1 cm/s)', color=DASH_RED,
            fontsize=18.5, fontweight='bold')
    ax.set_xlabel('Time from approach start (min)', color=DASH_MUTED)
    ax.set_ylabel('Relative speed (cm/s)', color=DASH_MUTED)
    ax.set_title('Relative speed', loc='left', pad=12)
    ax.grid(axis='y', alpha=1.0)
    ax.set_axisbelow(True)

    fig.suptitle('Final close approach — autonomous, light-time-tolerant',
                 fontsize=18, fontweight='bold', x=0.05, ha='left', y=1.02,
                 color=DASH_FG)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '04_close_approach.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 4b: Earth-arrival lunar gravity-assist tour
# ============================================================================
def plot_earth_lga():
    """Earth-Moon system showing the multi-flyby LGA capture sequence."""
    style_space()
    fig, ax = plt.subplots(figsize=(15, 13))
    add_starfield(ax, n=200, seed=11)

    # Earth at origin
    R_EARTH = 6378.0     # km
    R_MOON  = 384400.0   # km (lunar orbital radius)
    LEO_R   = R_EARTH + 400.0  # 400 km altitude depot

    # Plot Earth (scaled up for visibility)
    earth_visual_r = 18000.0  # exaggerated for legibility
    earth = plt.Circle((0, 0), earth_visual_r, color=ACCENT_BLUE, zorder=5)
    ax.add_patch(earth)
    earth_glow = plt.Circle((0, 0), earth_visual_r * 1.6, color=ACCENT_BLUE,
                             zorder=4, alpha=0.18)
    ax.add_patch(earth_glow)
    ax.text(0, -earth_visual_r - 14000, 'EARTH', color=ACCENT_BLUE, fontsize=19,
            fontweight='bold', ha='center', va='top', zorder=6)

    # Plot LEO depot orbit (scaled visual radius)
    leo_visual_r = earth_visual_r * 1.18
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(leo_visual_r*np.cos(theta), leo_visual_r*np.sin(theta),
            color=ACCENT_GREEN, lw=1.5, ls='--', alpha=0.85, zorder=4)
    # LEO depot label out of EARTH region — push down-right and away
    ax.annotate('LEO depot\n(400 km altitude)',
                xy=(leo_visual_r * 0.95, -leo_visual_r * 0.4),
                xytext=(0.55*R_MOON, -0.50*R_MOON),
                color=ACCENT_GREEN, fontsize=18, fontweight='bold',
                ha='center', zorder=6,
                arrowprops=dict(arrowstyle='->', color=ACCENT_GREEN, lw=1.4))

    # Lunar orbit (circle)
    ax.plot(R_MOON*np.cos(theta), R_MOON*np.sin(theta), color=INK_MUTED,
            lw=1.0, ls=':', alpha=0.55, zorder=2)
    ax.text(R_MOON * 0.72, R_MOON * 0.72,
            "Moon's orbit\n(384,400 km, 27.3 d)",
            color=INK_MUTED, fontsize=20, ha='center', va='center',
            style='italic', alpha=0.7, zorder=2)

    # Three Moon positions for three flybys (representing three lunar months)
    moon_angles = np.deg2rad([165, 75, -25])
    moon_xs = R_MOON * np.cos(moon_angles)
    moon_ys = R_MOON * np.sin(moon_angles)
    flyby_labels = [
        'FLYBY 1\nΔv∞ ≈ -1.0 km/s',
        'FLYBY 2\nΔv∞ ≈ -1.0 km/s',
        'FLYBY 3\nΔv∞ ≈ -1.0 km/s',
    ]

    for i, (mx, my, label) in enumerate(zip(moon_xs, moon_ys, flyby_labels)):
        moon = plt.Circle((mx, my), 22000, color=INK_TEXT, zorder=5,
                          alpha=0.9)
        ax.add_patch(moon)
        moon_glow = plt.Circle((mx, my), 38000, color=INK_TEXT, zorder=4,
                               alpha=0.20)
        ax.add_patch(moon_glow)
        # Label offset radially outward, larger
        lr = np.hypot(mx, my)
        lx = mx + (mx/lr)*82000
        ly = my + (my/lr)*82000
        ax.text(lx, ly, label, color=INK_TEXT, fontsize=18, fontweight='bold',
                ha='center', va='center', zorder=6,
                bbox=dict(facecolor=INK_PANEL, edgecolor=INK_MUTED,
                          boxstyle='round,pad=0.4', lw=0.8, alpha=0.85))

    # Incoming hyperbolic asymptote (from lower-left)
    asym_angle = np.deg2rad(205)
    asym_dist = 1.4 * R_MOON
    inbound_x = np.linspace(asym_dist*np.cos(asym_angle), moon_xs[0], 80)
    inbound_y = np.linspace(asym_dist*np.sin(asym_angle), moon_ys[0], 80)
    bend = 0.10 * np.sin(np.linspace(0, np.pi, 80))
    perp_x = -np.sin(asym_angle)
    perp_y =  np.cos(asym_angle)
    inbound_x = inbound_x + bend * R_MOON * perp_x
    inbound_y = inbound_y + bend * R_MOON * perp_y

    glow_line(ax, inbound_x, inbound_y, ACCENT_BLUE, lw=2.8, n_glow=4,
              glow_lw_step=2.4)
    # Place the inbound label well clear of the trajectory, in lower-left empty space
    ax.annotate('INBOUND FROM SATURN\nhyperbolic asymptote\nv∞ ≈ 6 km/s',
                xy=(inbound_x[20], inbound_y[20]),
                xytext=(-1.25*R_MOON, -1.05*R_MOON),
                color=ACCENT_BLUE, fontsize=18, fontweight='bold',
                ha='left', va='bottom',
                arrowprops=dict(arrowstyle='->', color=ACCENT_BLUE, lw=1.6),
                bbox=dict(facecolor=INK_PANEL, edgecolor=ACCENT_BLUE,
                          boxstyle='round,pad=0.5', lw=1.0, alpha=0.85),
                zorder=7)

    # Inter-flyby segments — phasing-orbit ellipses
    def phasing_arc(start_xy, end_xy, n=120, bulge=0.55):
        sx, sy = start_xy
        ex, ey = end_xy
        mx, my = (sx+ex)/2, (sy+ey)/2
        cx, cy = mx*(1-bulge), my*(1-bulge)
        t = np.linspace(0, 1, n)
        bx = (1-t)**2 * sx + 2*(1-t)*t * cx + t**2 * ex
        by = (1-t)**2 * sy + 2*(1-t)*t * cy + t**2 * ey
        return bx, by

    seg1_x, seg1_y = phasing_arc((moon_xs[0], moon_ys[0]),
                                  (moon_xs[1], moon_ys[1]), bulge=0.78)
    glow_line(ax, seg1_x, seg1_y, ACCENT_TEAL, lw=2.4, n_glow=3,
              glow_lw_step=2.2)

    seg2_x, seg2_y = phasing_arc((moon_xs[1], moon_ys[1]),
                                  (moon_xs[2], moon_ys[2]), bulge=0.85)
    glow_line(ax, seg2_x, seg2_y, ACCENT_TEAL, lw=2.4, n_glow=3,
              glow_lw_step=2.2)

    # Single phasing-orbit label, placed above and clear
    ax.annotate('PHASING ORBIT\npassive ~27 d/leg\n(no propellant)',
                xy=(seg1_x[60], seg1_y[60]),
                xytext=(-0.05*R_MOON, 1.18*R_MOON),
                color=ACCENT_TEAL, fontsize=18, fontweight='bold',
                ha='center', va='center',
                arrowprops=dict(arrowstyle='->', color=ACCENT_TEAL, lw=1.4),
                bbox=dict(facecolor=INK_PANEL, edgecolor=ACCENT_TEAL,
                          boxstyle='round,pad=0.5', lw=1.0, alpha=0.85),
                zorder=7)

    # Final spiral down to LEO from flyby 3
    n = 250
    spiral_t = np.linspace(0, 1, n)
    r_start = np.hypot(moon_xs[2], moon_ys[2])
    r_end = leo_visual_r
    rs = r_start * (r_end/r_start)**spiral_t
    n_turns = 2.5
    theta_start = np.arctan2(moon_ys[2], moon_xs[2])
    thetas = theta_start + 2*np.pi*n_turns*spiral_t
    spiral_x = rs*np.cos(thetas)
    spiral_y = rs*np.sin(thetas)
    glow_line(ax, spiral_x, spiral_y, ACCENT_GREEN, lw=2.2, n_glow=3,
              glow_lw_step=2.0)

    # LEO trim label — top-right, above FLYBY 2, clear of NET LGA box
    ax.annotate('LOW-THRUST TRIM TO LEO\n~0.5 km/s chunk-fed',
                xy=(spiral_x[180], spiral_y[180]),
                xytext=(1.10*R_MOON, 0.35*R_MOON),
                color=ACCENT_GREEN, fontsize=18, fontweight='bold',
                ha='center', va='center',
                arrowprops=dict(arrowstyle='->', color=ACCENT_GREEN, lw=1.5),
                bbox=dict(facecolor=INK_PANEL, edgecolor=ACCENT_GREEN,
                          boxstyle='round,pad=0.5', lw=1.0, alpha=0.85),
                zorder=7)

    # Total LGA reduction callout — bottom-right, away from FLYBY 3 and FLYBY 2
    ax.text(0.97, 0.04,
            'NET LGA REDUCTION\n~3 km/s arrival Δv∞\nat zero propellant cost',
            transform=ax.transAxes, fontsize=19, color=ACCENT_GOLD,
            fontweight='bold', ha='right', va='bottom',
            bbox=dict(facecolor=INK_PANEL, edgecolor=ACCENT_GOLD,
                      boxstyle='round,pad=0.7', lw=1.5))

    # Heritage callout (top-left, in empty space)
    ax.text(0.03, 0.96,
            'Heritage:\nHiten (1990), WIND, Geotail,\nARTEMIS, WMAP all flew\nmulti-flyby LGA sequences',
            transform=ax.transAxes, fontsize=20, color=INK_MUTED,
            fontweight='normal', ha='left', va='top', style='italic',
            bbox=dict(facecolor=INK_PANEL, edgecolor=INK_MUTED,
                      boxstyle='round,pad=0.5', lw=0.8, alpha=0.7))

    ax.set_xlim(-1.55*R_MOON, 1.55*R_MOON)
    ax.set_ylim(-1.4*R_MOON, 1.4*R_MOON)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    fig.suptitle('Earth arrival  -  multi-flyby lunar gravity-assist capture',
                 fontsize=26, fontweight='bold', x=0.05, ha='left', y=0.97,
                 color=INK_TEXT)
    fig.text(0.05, 0.93,
             '2-3 lunar flybys subtract ~3 km/s of inbound v∞ at zero propellant cost. '
             'Aerocapture is not viable: 50-1000 t of ice cargo would sublimate.',
             color=INK_MUTED, fontsize=14, ha='left')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '04b_earth_lga.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 5: ΔV budget
# ============================================================================
def plot_dv_budget():
    style_dashboard()
    phases = [
        ('Trans-Saturn injection',     7.30, DASH_BLUE,  'chemical kick stage  -  ONLY non-water-MET element'),
        ('Saturn capture',             1.00, DASH_TEAL,  'water MET  -  multi-pass low-thrust'),
        ('Ring rendezvous + station',  0.50, DASH_TEAL,  'water MET + RCS  -  Earth-launched water'),
        ('Saturn departure',           1.50, DASH_GREEN, 'water MET  -  chunk-fed, multi-pass'),
        ('Inbound cruise braking',     2.00, DASH_GREEN, 'water MET  -  chunk-fed retrograde'),
        ('Lunar gravity-assist tour',  3.00, DASH_AMBER, 'gravity (free)  -  2-3 lunar flybys'),
        ('Earth low-thrust trim to LEO', 0.50, DASH_GREEN, 'water MET  -  chunk-fed'),
        ('RCS trim into depot orbit',  0.20, DASH_GREEN, 'water RCS  -  chunk-fed'),
    ]
    names = [p[0] for p in phases]
    dvs   = [p[1] for p in phases]
    colors= [p[2] for p in phases]
    notes = [p[3] for p in phases]

    fig, ax = plt.subplots(figsize=(20, 11))
    ypos = np.arange(len(names))
    bars = ax.barh(ypos, dvs, color=colors, edgecolor='white',
                    height=0.65, zorder=3)
    ax.set_yticks(ypos)
    ax.set_yticklabels(names, fontsize=18, color=DASH_FG, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlim(0, 13)

    for bar, dv, note in zip(bars, dvs, notes):
        ax.text(dv+0.18, bar.get_y()+bar.get_height()*0.30,
                f'{dv:.2f} km/s', va='center', fontsize=18,
                fontweight='bold', color=DASH_FG)
        ax.text(dv+0.18, bar.get_y()+bar.get_height()*0.85,
                note, va='center', fontsize=14, color=DASH_MUTED, style='italic')

    # Bracket: chunk-fed portion (Saturn departure through depot trim)
    bracket_y_top = 2.62
    bracket_y_bot = 7.38
    bracket_x = 11.5
    ax.plot([bracket_x, bracket_x], [bracket_y_top, bracket_y_bot],
            color=DASH_GREEN, lw=2.5)
    ax.plot([bracket_x-0.15, bracket_x], [bracket_y_top, bracket_y_top],
            color=DASH_GREEN, lw=2.5)
    ax.plot([bracket_x-0.15, bracket_x], [bracket_y_bot, bracket_y_bot],
            color=DASH_GREEN, lw=2.5)
    ax.text(bracket_x+0.15, (bracket_y_top + bracket_y_bot)/2,
            '4.2 km/s\nCHUNK-FED\n(water MET\n+ RCS, fed from\nSaturn ice cargo)',
            fontsize=16, color=DASH_GREEN, fontweight='bold', va='center')

    ax.set_xlabel('Delta-V (km/s)', color=DASH_MUTED, fontsize=18)
    ax.grid(axis='x', alpha=1.0, zorder=1)
    ax.set_axisbelow(True)

    fig.suptitle('Delta-V budget  -  one bought burn, free LGA, the rest is water-MET',
                 fontsize=22, fontweight='bold', x=0.05, ha='left', y=1.0,
                 color=DASH_FG)
    ax.set_title('~13 km/s round-trip propulsive: 7.3 bought (TSI), 1.5 Earth-water (Saturn-side), 4.2 chunk-fed (inbound).  ~3 km/s of arrival ΔV from lunar gravity-assist tour at zero propellant cost.',
                 fontsize=14, color=DASH_MUTED, loc='left', pad=12)

    legend_handles = [
        mpatches.Patch(color=DASH_BLUE,  label='Bought  -  chemical kick stage (jettisoned)'),
        mpatches.Patch(color=DASH_TEAL,  label='water MET / RCS  -  Earth-launched water'),
        mpatches.Patch(color=DASH_GREEN, label='water MET / RCS  -  CHUNK-fed'),
        mpatches.Patch(color=DASH_AMBER, label='Lunar gravity-assist  -  free (gravity)'),
    ]
    # Legend below the plot, out of the way of bars
    ax.legend(handles=legend_handles, loc='upper center',
              bbox_to_anchor=(0.5, -0.10), ncol=2, fontsize=15,
              frameon=True, framealpha=1.0)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '05_dv_budget.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 6: Mass budget stacked
# ============================================================================
def plot_mass_budget():
    style_dashboard()
    stages = ['LEO stack\n(pre-TSI)', 'After TSI\n(en route)',
              'Saturn arrival\n(post-capture)', 'Saturn depart\n(w/ chunk)',
              'LEO delivered\n(final)']

    data = [
        ('TSI kick stage (jettisoned)',  [40, 0, 0, 0, 0],         '#9aa3b3'),
        ('Outbound water (MET prop)',    [3.5, 3.5, 1.0, 0, 0],    DASH_TEAL),
        ('Tug dry mass + avionics',      [1.5, 1.5, 1.5, 1.5, 1.5],'#3a4256'),
        ('Bag + grapple system',         [0.4, 0.4, 0.4, 0.4, 0.4],'#5a6378'),
        ('Saturn ice chunk (10 t delivered)', [0, 0, 0, 14, 10],   DASH_GREEN),
    ]

    fig, ax = plt.subplots(figsize=(13, 7.5))
    x_pos = np.arange(len(stages))
    bottom = np.zeros(len(stages))
    for label, vals, color in data:
        # extra emphasis on the chunk bar
        is_chunk = 'chunk' in label.lower()
        edge_color = DASH_FG if is_chunk else 'white'
        edge_lw = 2.2 if is_chunk else 1.2
        ax.bar(x_pos, vals, bottom=bottom, label=label, color=color,
               edgecolor=edge_color, linewidth=edge_lw, width=0.55,
               zorder=4 if is_chunk else 3)
        bottom = bottom + np.array(vals)

    totals = [sum(d[1][i] for d in data) for i in range(len(stages))]
    for i, t in enumerate(totals):
        ax.text(i, t+1.2, f'{t:.1f} t', ha='center', fontsize=20,
                fontweight='bold', color=DASH_FG)

    # TSI jettison annotation between bars 0 and 1
    ax.annotate('', xy=(0.7, 5), xytext=(0.3, 22),
                arrowprops=dict(arrowstyle='->', color=DASH_RED, lw=2,
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(0.5, 28, '40 t TSI stage\njettisoned\nafter burn',
            ha='center', fontsize=18.5, color=DASH_RED, fontweight='bold',
            bbox=dict(facecolor='#fafbfc', edgecolor=DASH_RED,
                      boxstyle='round,pad=0.35', linewidth=1.2))

    # Chunk grappled annotation
    ax.annotate('', xy=(3, 9), xytext=(3.4, 22),
                arrowprops=dict(arrowstyle='->', color=DASH_GREEN, lw=2,
                                connectionstyle='arc3,rad=0.2'))
    ax.text(3.4, 27, 'chunk grappled\n+14 t cargo\n(trawl-collected)',
            ha='center', fontsize=18.5, color=DASH_GREEN, fontweight='bold',
            bbox=dict(facecolor='#fafbfc', edgecolor=DASH_GREEN,
                      boxstyle='round,pad=0.35', linewidth=1.2))

    # Final delivery callout
    ax.annotate('', xy=(4, 11.9), xytext=(4.3, 30),
                arrowprops=dict(arrowstyle='->', color=DASH_BLUE, lw=2.5))
    ax.text(4.35, 35, '★ 10 tonnes\ndelivered to\nLEO depot',
            ha='center', fontsize=20, color=DASH_BLUE, fontweight='bold',
            bbox=dict(facecolor='#fafbfc', edgecolor=DASH_BLUE,
                      boxstyle='round,pad=0.45', linewidth=1.6))

    ax.set_xticks(x_pos)
    ax.set_xticklabels(stages, fontsize=19.5)
    ax.set_ylabel('Mass (tonnes)', color=DASH_MUTED, fontsize=20)
    ax.set_ylim(0, 55)
    ax.set_xlim(-0.6, 4.9)
    ax.grid(axis='y', alpha=1.0, zorder=1)
    ax.set_axisbelow(True)

    fig.suptitle('Mass budget  -  single round-trip flight delivering 10 t to LEO',
                 fontsize=18.5, fontweight='bold', x=0.05, ha='left', y=1.0,
                 color=DASH_FG)
    ax.set_title('Most launch mass is the bought TSI stage (jettisoned). The chunk grappled at Saturn is 4× the rest of the spacecraft.',
                 fontsize=19.5, color=DASH_MUTED, loc='left', pad=12)

    ax.legend(loc='upper left', fontsize=19, ncol=1, frameon=True,
              framealpha=1.0, bbox_to_anchor=(0.02, 0.98))

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '06_mass_budget.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 7: Mission timeline Gantt
# ============================================================================
def plot_timeline():
    style_dashboard()
    phases = [
        ('1. LEO insertion',         0.00, 0.05, '#9aa3b3'),
        ('2. Trans-Saturn injection',0.05, 0.05, DASH_BLUE),
        ('3. Heliocentric outbound', 0.10, 6.10, DASH_TEAL),
        ('4. Saturn capture',        6.20, 0.15, DASH_TEAL),
        ('5. Ring rendezvous',       6.25, 0.50, DASH_AMBER),
        ('6. Grapple + bag deploy',  6.75, 0.25, DASH_AMBER),
        ('7. Saturn departure',      7.00, 0.15, DASH_GREEN),
        ('8. Heliocentric inbound',  7.05, 6.10, DASH_GREEN),
        ('9. Lunar flyby tour',      13.15,0.25, DASH_AMBER),
        ('10. LEO depot delivery',   13.40,0.30, DASH_GREEN),
    ]
    fig, ax = plt.subplots(figsize=(14, 6.5))
    for i, (name, start, dur, color) in enumerate(phases):
        ax.barh(i, dur, left=start, color=color, edgecolor='white',
                height=0.64, linewidth=1.2, zorder=4)
        if dur > 0.6:
            ax.text(start + dur/2, i, name, ha='center', va='center',
                    fontsize=19.5, color='white', fontweight='bold')
        else:
            ax.text(start + dur + 0.22, i, name, ha='left', va='center',
                    fontsize=19.5, color=DASH_FG)

    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_xlabel('Years from launch', color=DASH_MUTED, fontsize=20)
    ax.set_xlim(-0.5, 17.5)
    ax.set_ylim(len(phases) - 0.4, -1.6)
    ax.grid(axis='x', alpha=1.0, zorder=1)
    ax.set_axisbelow(True)

    # Major decision-gate diamonds at the top
    gate_y = -1.0
    gates = [
        (0.0,  'LAUNCH',           DASH_BLUE),
        (6.2,  'GATE: Saturn\ncapture milestone',  DASH_AMBER),
        (6.75, 'GATE: Grapple\n+ bag deploy',      DASH_AMBER),
        (13.5, '★ FIRST\nDELIVERY',                DASH_GREEN),
    ]
    for x, label, color in gates:
        ax.plot(x, gate_y, marker='D', markersize=14, color=color,
                markeredgecolor='white', markeredgewidth=2, zorder=8)
        ax.axvline(x, color=color, lw=1.0, ls=(0, (4, 4)), alpha=0.45, zorder=2)
        ax.text(x, gate_y - 0.4, label, ha='center', va='bottom',
                fontsize=18, color=color, fontweight='bold')

    fig.suptitle('Mission timeline  -  13.5 yr end-to-end, with decision gates',
                 fontsize=18.5, fontweight='bold', x=0.05, ha='left', y=1.0,
                 color=DASH_FG)
    ax.set_title('Diamonds = critical decision gates. Year 6 capture is the single biggest information event in the program.',
                 fontsize=19.5, color=DASH_MUTED, loc='left', pad=12)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '07_timeline.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 8: Bag thermodynamic schematic
# ============================================================================
def plot_trawl_collection():
    """Single-panel: trawl bag deployed in the B-ring."""
    style_space()
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_facecolor('#0a0e1a')
    ax.set_xlim(-1, 11); ax.set_ylim(0, 6.5); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

    # Ring particle field — random scatter of small "ice particles"
    rng = np.random.default_rng(7)
    n_particles = 80
    px = rng.uniform(0, 11, n_particles)
    py = rng.uniform(0.5, 6.0, n_particles)
    sizes = rng.exponential(40, n_particles) + 5
    # Filter out particles that would overlap the spacecraft
    keep = (px > 6) | ((py < 1.5) | (py > 5))
    ax.scatter(px[keep], py[keep], s=sizes[keep], c='#bedbef',
               alpha=0.7, edgecolors='#5fa8ff', linewidths=0.6, zorder=2)

    # Drift direction arrows showing particles moving relative to spacecraft
    for y in [1.3, 2.5, 3.8, 5.0]:
        for x in [0.8, 2.3, 3.8]:
            ax.annotate('', xy=(x+0.7, y), xytext=(x, y),
                        arrowprops=dict(arrowstyle='->', color='#5fa8ff',
                                        lw=0.7, alpha=0.5))

    # Spacecraft body (right side)
    sc = mpatches.FancyBboxPatch((8.7, 2.4), 1.6, 1.4,
                                 boxstyle='round,pad=0.05,rounding_size=0.15',
                                 linewidth=2, edgecolor='#3ed4c0',
                                 facecolor='#11182a', zorder=6)
    ax.add_patch(sc)
    ax.text(9.5, 3.1, 'TUG', ha='center', va='center', color='#3ed4c0',
            fontsize=19, fontweight='bold', zorder=7)

    # Solar panels
    for y in [4.0, 1.6]:
        panel = mpatches.Rectangle((9.0, y), 1.0, 0.4, facecolor='#1f2a44',
                                    edgecolor='#5fa8ff', linewidth=1.0, zorder=5)
        ax.add_patch(panel)
        for i in range(4):
            ax.plot([9.0+i*0.25, 9.0+i*0.25], [y, y+0.4],
                    color='#5fa8ff', alpha=0.5, lw=0.5)

    # Trawl bag — open mouth deployed forward (left of spacecraft)
    # Cylinder/cone shape opening toward the particle field
    mouth_x = 4.5
    throat_x = 7.5
    mouth_top = 5.4; mouth_bot = 1.4
    throat_top = 3.7; throat_bot = 2.5

    # Bag exterior (filled)
    bag_x = [mouth_x, throat_x, throat_x, mouth_x]
    bag_y_top = [mouth_top, throat_top, throat_top, mouth_top]
    bag_y_bot = [mouth_bot, throat_bot, throat_bot, mouth_bot]
    ax.fill_between([mouth_x, throat_x], [mouth_top, throat_top], [mouth_bot, throat_bot],
                    color='#3ed4c0', alpha=0.10, zorder=3)
    # Bag outline
    ax.plot([mouth_x, throat_x], [mouth_top, throat_top], color='#3ed4c0', lw=2.2, zorder=4)
    ax.plot([mouth_x, throat_x], [mouth_bot, throat_bot], color='#3ed4c0', lw=2.2, zorder=4)
    ax.plot([throat_x, 8.7], [throat_top, 3.6], color='#3ed4c0', lw=2.2, zorder=4)
    ax.plot([throat_x, 8.7], [throat_bot, 2.6], color='#3ed4c0', lw=2.2, zorder=4)

    # Mouth opening (suggested ellipse)
    mouth_ell = mpatches.Ellipse((mouth_x, (mouth_top+mouth_bot)/2),
                                  0.25, mouth_top - mouth_bot,
                                  facecolor='#0a0e1a', edgecolor='#3ed4c0',
                                  linewidth=2.2, zorder=5)
    ax.add_patch(mouth_ell)

    # Captured particles inside bag (interior)
    n_inside = 30
    inside_x = rng.uniform(throat_x+0.1, 8.5, n_inside)
    inside_y = rng.uniform(2.7, 3.5, n_inside)
    sizes_in = rng.exponential(20, n_inside) + 5
    ax.scatter(inside_x, inside_y, s=sizes_in, c='#bedbef',
               alpha=0.85, edgecolors='#3ed4c0', linewidths=0.6, zorder=6)

    # Particles entering through the mouth (motion lines)
    for y in [2.5, 3.0, 3.5, 4.0]:
        ax.annotate('', xy=(mouth_x+0.2, y), xytext=(mouth_x-1.0, y),
                    arrowprops=dict(arrowstyle='->', color='#3ed4c0',
                                    lw=1.4, alpha=0.85))

    # Annotations
    ax.text(0.3, 6.1, 'B-RING PARTICLE FIELD', fontsize=18.5, color='#5fa8ff',
            fontweight='bold')
    ax.text(0.3, 5.7, 'volume mass density ~10 kg/m³', fontsize=13,
            color='#8a96b0', style='italic')

    ax.annotate('drift @ ~mm/s\n(Keplerian shear)',
                xy=(2.5, 3.0), xytext=(0.5, 0.3),
                fontsize=13.5, color='#5fa8ff',
                arrowprops=dict(arrowstyle='->', color='#5fa8ff', lw=1, alpha=0.7))

    ax.annotate('intake aperture\n~50–150 m²',
                xy=(mouth_x, mouth_top-0.3), xytext=(2.5, 5.7),
                fontsize=13.5, color='#3ed4c0', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#3ed4c0', lw=1.2))

    ax.annotate('inelastic capture\n(Vectran + aerogel)',
                xy=(8.0, 3.1), xytext=(5.0, 0.4),
                fontsize=13.5, color='#3ed4c0',
                arrowprops=dict(arrowstyle='->', color='#3ed4c0', lw=1, alpha=0.7))

    fig.suptitle('Trawl bag — collection phase',
                 fontsize=25, fontweight='bold', x=0.05, ha='left', y=0.98,
                 color=INK_TEXT)
    fig.text(0.05, 0.94,
             'Bag deployed forward of the spacecraft. Ring particles drift through '
             'the intake aperture at ~mm/s; soft-fabric and aerogel layers decelerate '
             'them inelastically. Collection completes in hours to days.',
             color=INK_MUTED, fontsize=8, ha='left')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '08a_trawl_collection.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")


def plot_trawl_cruise():
    """Single-panel: sealed bag heat-pipe vapor cycle on the inbound cruise."""
    style_space()
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_facecolor('#0a0e1a')
    ax.set_xlim(-1, 11); ax.set_ylim(0, 6.5); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    rng = np.random.default_rng(13)

    # Solar IR arrow (top-left)
    for i in range(4):
        ax.annotate('', xy=(2.4-i*0.05, 4.7-i*0.05),
                    xytext=(0.5+i*0.1, 5.5+i*0.05),
                    arrowprops=dict(arrowstyle='->', color='#e8b54e',
                                    lw=2.2, alpha=0.8-0.18*i))
    ax.text(0.1, 5.85, 'SOLAR IR (modulated)', fontsize=13.5,
            color='#e8b54e', fontweight='bold')

    # Sealed bag — closed cylinder
    seal_x_left = 2.0; seal_x_right = 7.5
    seal_y_top = 4.7; seal_y_bot = 1.6

    # Bag body
    bag_body = mpatches.FancyBboxPatch((seal_x_left, seal_y_bot),
                                        seal_x_right - seal_x_left,
                                        seal_y_top - seal_y_bot,
                                        boxstyle='round,pad=0.02,rounding_size=0.4',
                                        linewidth=2.5, edgecolor='#e6edf5',
                                        facecolor='#1f2a44', alpha=0.85, zorder=3)
    ax.add_patch(bag_body)

    # Hot side (sun-facing, left)
    hot_zone = mpatches.Rectangle((seal_x_left+0.1, seal_y_bot+0.1),
                                   1.2, seal_y_top - seal_y_bot - 0.2,
                                   facecolor='#d4a017', alpha=0.20, zorder=4)
    ax.add_patch(hot_zone)
    ax.text(seal_x_left+0.7, seal_y_top-0.3, '~250 K',
            fontsize=13, color='#d4a017', fontweight='bold', ha='center')

    # Captured ice particles inside (lots of small ones)
    n_inside_b = 60
    inside_x_b = rng.uniform(seal_x_left+0.2, seal_x_right-1.4, n_inside_b)
    inside_y_b = rng.uniform(seal_y_bot+0.15, seal_y_top-0.15, n_inside_b)
    sizes_in_b = rng.exponential(15, n_inside_b) + 4
    ax.scatter(inside_x_b, inside_y_b, s=sizes_in_b, c='#bedbef',
               alpha=0.85, edgecolors='#5fa8ff', linewidths=0.5, zorder=5)

    # Cold wall (right)
    cold_x = seal_x_right - 0.4
    cold = mpatches.Rectangle((cold_x, seal_y_bot+0.05), 0.3,
                               seal_y_top - seal_y_bot - 0.1,
                               facecolor='#5fa8ff', alpha=0.95, zorder=6)
    ax.add_patch(cold)

    # Frost layer
    frost = mpatches.Rectangle((cold_x-0.18, seal_y_bot+0.05), 0.18,
                                seal_y_top - seal_y_bot - 0.1,
                                facecolor='white', edgecolor='#d0d8e0',
                                linewidth=0.6, alpha=0.95, zorder=6)
    ax.add_patch(frost)

    ax.text(seal_x_right+0.05, seal_y_top - 0.25, '<150 K',
            fontsize=13, color='#5fa8ff', fontweight='bold')
    ax.text(seal_x_right+0.05, seal_y_top - 0.65, 'cold wall',
            fontsize=12.5, color='#5fa8ff')

    # Vapor flow arrows (hot → cold)
    for y in [seal_y_bot+0.5, (seal_y_bot+seal_y_top)/2, seal_y_top-0.5]:
        ax.annotate('', xy=(cold_x-0.25, y), xytext=(seal_x_left+1.5, y),
                    arrowprops=dict(arrowstyle='->', color='#8a96b0',
                                    lw=1.5, alpha=0.85))
    ax.text((seal_x_left+cold_x)/2, seal_y_top+0.1,
            'H₂O vapor — pressure-driven flow',
            ha='center', fontsize=13, color='#e6edf5', style='italic')

    # Harvest port (small heated zone on cold wall)
    harvest = mpatches.Circle((cold_x-0.05, 2.0), 0.18,
                               facecolor='#e8b54e', edgecolor='#e6edf5',
                               linewidth=1.2, zorder=8)
    ax.add_patch(harvest)
    ax.annotate('harvest port\n(local heater +\nMET feed)',
                xy=(cold_x-0.05, 2.0), xytext=(seal_x_right+0.4, 0.5),
                fontsize=13, color='#e8b54e', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#e8b54e', lw=1))

    # MET (right of bag)
    met = mpatches.FancyBboxPatch((8.4, 2.85), 0.8, 0.5,
                                   boxstyle='round,pad=0.02,rounding_size=0.05',
                                   facecolor='#3ed4c0', edgecolor='white',
                                   linewidth=1.5, zorder=7)
    ax.add_patch(met)
    ax.text(8.8, 3.1, 'MET', ha='center', va='center', color='#0a0e1a',
            fontsize=19, fontweight='bold')
    # Feed line from harvest port to MET
    ax.annotate('', xy=(8.4, 3.1), xytext=(cold_x+0.1, 2.0),
                arrowprops=dict(arrowstyle='->', color='#e8b54e', lw=1.6))

    # Exhaust (right of MET)
    for i in range(5):
        ax.annotate('', xy=(10.7+i*0.06, 3.1), xytext=(9.2+i*0.06, 3.1),
                    arrowprops=dict(arrowstyle='->', color='#3ed4c0',
                                    lw=2.2, alpha=0.8-0.13*i))
    ax.text(10.9, 2.5, 'thrust\n(plasma\nIsp ~700s)',
            ha='left', va='top', fontsize=13, color='#3ed4c0', fontweight='bold')

    fig.suptitle('Trawl bag — chunk-fed cruise phase (heat-pipe vapor cycle)',
                 fontsize=25, fontweight='bold', x=0.05, ha='left', y=0.98,
                 color=INK_TEXT)
    fig.text(0.05, 0.94,
             'Sealed bag after cinch. Sun-facing wall sublimates ice; cold-side wall '
             '(<150 K) cryopumps vapor as frost; heated harvest port re-sublimates '
             'frost on demand and meters vapor to the MET. Cargo IS the propellant tank.',
             color=INK_MUTED, fontsize=8, ha='left')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '08b_trawl_cruise.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

def plot_cashflow_milestones():
    """Milestone-rich cumulative cash position with annual cashflow bars.
    Shows program going deep negative, milestones at every flight, inflection
    at first delivery, post-delivery revenue ramp."""
    style_dashboard()
    fig, ax = plt.subplots(figsize=(16, 8))

    # Annual cash flow per year (negative = spend, positive = revenue net of opex)
    # Years 0-3: NEA demo development + flight
    # Years 4-5: cislunar demo + Saturn ship 1 build
    # Year 4: Saturn ship 1 launch (big spend)
    # Years 5-10: cruise (modest ground ops)
    # Years 11+: ship 2, 3, ... launching every synodic
    # Year 17: ship 1 delivery (revenue starts)
    # Year 24: ship 2 delivery (revenue ramps)
    # Year 25+: full steady state ($1.4B/yr net)

    years = np.arange(0, 41)
    annual_cf = np.zeros(41)

    # Spending phase
    annual_cf[0] = -120   # NRE start + design
    annual_cf[1] = -150   # NEA shakedown
    annual_cf[2] = -100
    annual_cf[3] = -120   # cislunar build/launch
    annual_cf[4] = -250   # Saturn ship 1 build + launch
    annual_cf[5] = -50    # cruise ops
    annual_cf[6] = -50
    annual_cf[7] = -50
    annual_cf[8] = -50
    annual_cf[9] = -50
    annual_cf[10] = -50   # capture confirmed
    annual_cf[11] = -250  # Saturn ship 2 launch
    annual_cf[12] = -250  # ship 3 launch
    annual_cf[13] = -250  # ship 4 launch
    annual_cf[14] = -250  # ship 5 launch
    annual_cf[15] = -250
    annual_cf[16] = -250
    # Year 17: ship 1 delivers — revenue starts
    annual_cf[17] = 350   # partial-year revenue ($800M revenue - $250M cost - $200M ramp)
    annual_cf[18] = 100   # only ship 1's revenue this year
    annual_cf[19] = 100
    annual_cf[20] = 100
    annual_cf[21] = 100
    annual_cf[22] = 100
    annual_cf[23] = 100
    annual_cf[24] = 1500  # ship 2 delivers (750t scale)
    # steady state from year 25
    for i in range(25, 41):
        annual_cf[i] = 1400  # net steady-state cash flow

    cum_cf = np.cumsum(annual_cf)

    # Color bars by sign
    colors = [DASH_RED if v < 0 else DASH_GREEN for v in annual_cf]
    ax.bar(years, annual_cf, color=colors, alpha=0.55, edgecolor='white',
           linewidth=0.6, width=0.85, zorder=3)

    # Cumulative line
    ax.plot(years, cum_cf, color=DASH_BLUE, lw=3.5, zorder=10,
            marker='o', markersize=4.5, markerfacecolor='white',
            markeredgewidth=1.5)

    # Zero line
    ax.axhline(0, color=DASH_FG, lw=0.8, alpha=0.5, zorder=2)

    # Inflection markers
    ax.axvline(17, color=DASH_GREEN, lw=1.2, ls=(0, (3, 3)), alpha=0.6, zorder=2)
    ax.axvline(24, color=DASH_AMBER, lw=1.2, ls=(0, (3, 3)), alpha=0.6, zorder=2)

    # Milestone callouts (year, label, color, y_offset_for_arrow)
    milestones = [
        (1.5, 'NEA demo\nreturns', DASH_TEAL, 800),
        (3, 'Cislunar demo\nreturns', DASH_TEAL, 1200),
        (4, 'Saturn ship 1\nlaunches', DASH_AMBER, 2000),
        (10, 'Saturn capture\nconfirmed (ship 1)', DASH_AMBER, 1500),
        (11, 'Ship 2 launches', DASH_AMBER, 3500),
        (17, '* FIRST DELIVERY\n(ship 1, 250 t)\nrevenue starts', DASH_GREEN, 4500),
        (24, '** STEADY STATE\n(ship 2, 750 t)\n~$1.4B/yr net', DASH_BLUE, 6000),
    ]

    for x, label, color, y_text in milestones:
        # Find cumulative cf value at that year
        cum_val = cum_cf[int(x)] if x == int(x) else (cum_cf[int(x)] + cum_cf[int(x)+1])/2
        ax.annotate(label, xy=(x, cum_val), xytext=(x, y_text),
                    fontsize=18, color=color, fontweight='bold', ha='center',
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.3, alpha=0.85),
                    bbox=dict(facecolor='#fafbfc', edgecolor=color,
                              boxstyle='round,pad=0.4', linewidth=1.2))

    # Phase shaded backgrounds
    ax.axvspan(0, 4, alpha=0.05, color=DASH_RED, zorder=0)
    ax.axvspan(4, 17, alpha=0.05, color=DASH_AMBER, zorder=0)
    ax.axvspan(17, 24, alpha=0.05, color=DASH_GREEN, zorder=0)
    ax.axvspan(24, 40, alpha=0.10, color=DASH_BLUE, zorder=0)

    # Phase labels at bottom
    phase_y = -2200
    ax.text(2, phase_y, 'DEMOS', ha='center', fontsize=18, color=DASH_RED,
            fontweight='bold', alpha=0.7)
    ax.text(10.5, phase_y, 'SATURN BUILD-OUT', ha='center', fontsize=18, color=DASH_AMBER,
            fontweight='bold', alpha=0.8)
    ax.text(20.5, phase_y, 'FIRST REVENUE', ha='center', fontsize=18, color=DASH_GREEN,
            fontweight='bold', alpha=0.8)
    ax.text(32, phase_y, 'STEADY STATE  -  ~$1.4B/yr profit in perpetuity', ha='center',
            fontsize=18.5, color=DASH_BLUE, fontweight='bold', alpha=0.9)

    ax.set_xlabel('Year from program start', color=DASH_MUTED, fontsize=20)
    ax.set_ylabel('Cash flow  ($M / yr  bars; cumulative line)', color=DASH_MUTED, fontsize=20)
    ax.set_xlim(-0.5, 40.5)
    ax.set_ylim(-2700, 22000)
    ax.set_xticks(np.arange(0, 41, 2))
    ax.grid(axis='y', alpha=1.0, zorder=1)
    ax.set_axisbelow(True)

    # Hero numbers callout
    callout = ('Max sunk position:  −$1.04B (year 11)\n'
               'Payback:  year ~24\n'
               'Steady-state revenue:  $1.85B/yr\n'
               'Steady-state cost:      $0.41B/yr\n'
               'Steady-state PROFIT:  $1.4B/yr\n'
               'Net margin:                    76%')
    ax.text(0.5, 21000, callout, fontsize=19, fontweight='normal',
            color=DASH_FG, ha='left', va='top', family='monospace',
            bbox=dict(facecolor='#fafbfc', edgecolor=DASH_GRID,
                      boxstyle='round,pad=0.7', linewidth=1.4))

    # Legend
    handles = [
        mpatches.Patch(color=DASH_RED, alpha=0.55, label='Annual cash out'),
        mpatches.Patch(color=DASH_GREEN, alpha=0.55, label='Annual cash in'),
        plt.Line2D([0], [0], color=DASH_BLUE, lw=3, marker='o',
                    markersize=6, markerfacecolor='white', markeredgewidth=1.5,
                    label='Cumulative cash position'),
    ]
    ax.legend(handles=handles, loc='upper left', fontsize=19,
              bbox_to_anchor=(0.20, 0.98), frameon=True, framealpha=1.0)

    fig.suptitle('Project ICEBERG  -  cash position over time',
                 fontsize=19, fontweight='bold', x=0.05, ha='left', y=1.0,
                 color=DASH_FG)
    ax.set_title('Demonstrator phase to Saturn build-out to first delivery (yr 17) to steady-state ~$1.4B/yr profit',
                 loc='left', pad=12, color=DASH_MUTED, fontsize=19.5,
                 fontweight='normal')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '09_cashflow.png')   # OVERWRITES the older cashflow plot
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}  (milestone-rich version)")

def plot_cumulative_cashflow():
    """Investor-style cumulative cost vs revenue chart."""
    style_dashboard()
    fig, ax = plt.subplots(figsize=(12, 6.5))

    # Best-case timeline (matches doc table)
    years = np.array([0, 1.5, 3, 4, 10, 11, 17.5, 24.5, 30, 40])
    cum_spend = np.array([0, 200, 400, 760, 850, 1100, 1500, 2500, 4500, 8500])  # $M
    cum_rev   = np.array([0,  14,  62,  62,  62,  62,  850, 2850, 11500, 27500])  # $M
    net = cum_rev - cum_spend

    # Stacked area for spend / revenue
    ax.fill_between(years, 0, cum_spend, color=DASH_RED, alpha=0.15,
                    label='Cumulative spend')
    ax.plot(years, cum_spend, color=DASH_RED, lw=2.4, marker='o',
            markersize=6, markerfacecolor='white', markeredgewidth=2)

    ax.fill_between(years, 0, cum_rev, color=DASH_GREEN, alpha=0.15,
                    label='Cumulative revenue')
    ax.plot(years, cum_rev, color=DASH_GREEN, lw=2.4, marker='o',
            markersize=6, markerfacecolor='white', markeredgewidth=2)

    # Net line
    ax.plot(years, net, color=DASH_BLUE, lw=2.5, ls='--',
            label='Net (revenue − spend)', zorder=10)
    ax.axhline(0, color=DASH_MUTED, lw=0.8, alpha=0.5, zorder=1)

    # Crossover annotation
    crossover = 24
    ax.axvline(crossover, color=DASH_AMBER, lw=1, ls=':', alpha=0.7)
    ax.annotate('Program turns net-positive\n(year ~24)',
                xy=(crossover, 0), xytext=(15, -2500),
                fontsize=19, color=DASH_AMBER, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=DASH_AMBER, lw=1.4))

    # First delivery annotation
    ax.annotate('First chunk delivered\n(year 17.5)',
                xy=(17.5, 850), xytext=(11.5, 6500),
                fontsize=18.5, color=DASH_GREEN, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=DASH_GREEN, lw=1.2))

    # Max-loss annotation
    max_loss_year = 11
    max_loss_val = -1038
    ax.annotate(f'Max sunk position\n−$1.04B (year {max_loss_year})',
                xy=(max_loss_year, max_loss_val), xytext=(13, -5500),
                fontsize=18.5, color=DASH_RED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=DASH_RED, lw=1.2))

    # Steady state annotation
    ax.annotate('Steady-state cash flow\n~$1.4B/yr from year 24',
                xy=(35, 18500), xytext=(28, 10000),
                fontsize=19, color=DASH_BLUE, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=DASH_BLUE, lw=1.4))

    ax.set_xlabel('Year from program start', color=DASH_MUTED, fontsize=20)
    ax.set_ylabel('Cumulative $ (millions)', color=DASH_MUTED, fontsize=20)
    ax.set_xlim(0, 40)
    ax.set_ylim(-7000, 32000)
    ax.legend(loc='upper left', fontsize=19, frameon=True, framealpha=1.0)
    ax.grid(axis='y', alpha=1.0)
    ax.set_axisbelow(True)

    # Hero numbers in bottom-right callout box
    callout = ('IRR (30 yr): ~12–15%\n'
               'IRR (40 yr): ~18–22%\n'
               'Max drawdown: $1.5B\n'
               'Net at yr 40: ~$20B')
    ax.text(38, -1500, callout, fontsize=19, fontweight='bold',
            color=DASH_FG, ha='right', va='top',
            bbox=dict(facecolor='#fafbfc', edgecolor=DASH_GRID,
                      boxstyle='round,pad=0.6', linewidth=1.2))

    fig.suptitle('Cumulative cash flow — best case',
                 fontsize=18, fontweight='bold', x=0.05, ha='left', y=1.0,
                 color=DASH_FG)
    ax.set_title('Demonstrators → Saturn flight 1 → steady-state production',
                 loc='left', pad=12, color=DASH_MUTED, fontsize=19,
                 fontweight='normal')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '09_cashflow.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

def plot_moat():
    """Side-by-side fleet timeline: ICEBERG vs follower. Each ship is a horizontal bar
    showing its mission phases. Visually obvious that ICEBERG has many ships in motion
    before the follower has even launched."""
    style_dashboard()
    fig, ax = plt.subplots(figsize=(13, 7.5))

    # Phase color scheme
    PHASE_BUILD   = '#cbd2dc'
    PHASE_OUT     = DASH_BLUE
    PHASE_SATURN  = DASH_AMBER
    PHASE_IN      = DASH_TEAL
    PHASE_DELIVER = DASH_GREEN

    # ICEBERG fleet (year 0 program start)
    # Each entry: (label, build_start, launch, capture, depart, deliver)
    iceberg_ships = [
        ('Ship 1 (50 t)',  0.0, 5.0, 11.0, 11.5, 18.0),
        ('Ship 2 (50 t)',  1.5, 6.5, 12.5, 13.0, 19.5),
        ('Ship 3 (100 t)', 3.0, 8.0, 14.0, 14.5, 21.0),
        ('Ship 4 (100 t)', 4.5, 9.5, 15.5, 16.0, 22.5),
        ('Ship 5 (200 t)', 6.0, 11.0, 17.0, 17.5, 24.0),
        ('Ship 6 (200 t)', 7.5, 12.5, 18.5, 19.0, 25.5),
    ]

    # Follower fleet — assume follower decides to compete the day ICEBERG ship 1 captures (year 11)
    # Best case: 4-yr build, then standard mission profile
    follower_ships = [
        ('Ship 1 (50 t)',  11.0, 16.0, 22.0, 22.5, 29.0),
        ('Ship 2 (50 t)',  12.5, 17.5, 23.5, 24.0, 30.5),
    ]

    # Plot ICEBERG ships (top half)
    n_iceberg = len(iceberg_ships)
    for i, (label, build, launch, capture, depart, deliver) in enumerate(iceberg_ships):
        y = n_iceberg - 1 - i + 1  # stack from top
        # Build phase
        ax.barh(y, launch - build, left=build, color=PHASE_BUILD, edgecolor='white', height=0.72, zorder=3)
        # Outbound cruise
        ax.barh(y, capture - launch, left=launch, color=PHASE_OUT, edgecolor='white', height=0.72, zorder=3)
        # Saturn ops
        ax.barh(y, depart - capture, left=capture, color=PHASE_SATURN, edgecolor='white', height=0.72, zorder=4)
        # Inbound cruise
        ax.barh(y, deliver - depart, left=depart, color=PHASE_IN, edgecolor='white', height=0.72, zorder=3)
        # Delivery marker
        ax.plot(deliver, y, 'o', markersize=10, color=PHASE_DELIVER,
                markerfacecolor=PHASE_DELIVER, markeredgecolor='white', markeredgewidth=1.5, zorder=6)
        # Label on left
        ax.text(build - 0.5, y, label, ha='right', va='center', fontsize=18.5,
                color=DASH_FG, fontweight='bold')

    # Divider band
    divider_y = 0.3
    ax.axhspan(divider_y, divider_y + 0.4, color=DASH_GRID, alpha=0.5, zorder=1)

    # Plot follower ships (bottom)
    n_follower = len(follower_ships)
    for i, (label, build, launch, capture, depart, deliver) in enumerate(follower_ships):
        y = -i - 0.5
        ax.barh(y, launch - build, left=build, color=PHASE_BUILD, edgecolor='white', height=0.72, zorder=3, alpha=0.7)
        ax.barh(y, capture - launch, left=launch, color=PHASE_OUT, edgecolor='white', height=0.72, zorder=3, alpha=0.7)
        ax.barh(y, depart - capture, left=capture, color=PHASE_SATURN, edgecolor='white', height=0.72, zorder=4, alpha=0.7)
        ax.barh(y, deliver - depart, left=depart, color=PHASE_IN, edgecolor='white', height=0.72, zorder=3, alpha=0.7)
        ax.plot(deliver, y, 'o', markersize=10, color=PHASE_DELIVER,
                markerfacecolor=PHASE_DELIVER, markeredgecolor='white', markeredgewidth=1.5, zorder=6, alpha=0.85)
        ax.text(build - 0.5, y, 'Follower ' + label, ha='right', va='center', fontsize=18.5,
                color=DASH_FG, fontweight='bold')

    # Section labels
    ax.text(-3.0, n_iceberg / 2 + 0.5, 'ICEBERG\nFLEET', ha='right', va='center',
            fontsize=20, fontweight='bold', color=DASH_TEAL)
    ax.text(-3.0, -1.0, 'COMPETITOR\n(decides to enter\nat year 11)', ha='right', va='center',
            fontsize=20, fontweight='bold', color=DASH_RED)

    # Critical vertical lines
    ax.axvline(11, color=DASH_AMBER, lw=2, ls='-', alpha=0.85, zorder=2)
    ax.text(11, n_iceberg + 1.1, 'MOAT SET\n(ICEBERG ship 1 captures)',
            ha='center', va='bottom', fontsize=19.5, fontweight='bold', color=DASH_AMBER,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=DASH_AMBER, lw=1.5))

    ax.axvline(18, color=DASH_GREEN, lw=2, ls='--', alpha=0.6, zorder=2)
    ax.text(18.2, -2.4, 'ICEBERG ship 1\ndelivers (yr 18)',
            ha='left', va='center', fontsize=18, color=DASH_GREEN, fontweight='bold')

    ax.axvline(29, color=DASH_RED, lw=2, ls='--', alpha=0.6, zorder=2)
    ax.text(29.2, -2.4, 'Follower\'s 1st\ndelivery (yr 29)',
            ha='left', va='center', fontsize=18, color=DASH_RED, fontweight='bold')

    # Permanent-gap annotation
    ax.annotate('', xy=(29, -3.4), xytext=(18, -3.4),
                arrowprops=dict(arrowstyle='<->', color=DASH_AMBER, lw=2.0))
    ax.text(23.5, -3.7, '11+ year permanent phase offset',
            ha='center', va='top', fontsize=20, fontweight='bold', color=DASH_AMBER,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=DASH_AMBER, lw=1.2))

    # Legend for phases
    legend_handles = [
        mpatches.Patch(color=PHASE_BUILD, label='Build'),
        mpatches.Patch(color=PHASE_OUT, label='Outbound cruise (6.1 yr Hohmann)'),
        mpatches.Patch(color=PHASE_SATURN, label='Saturn ops (capture + trawl)'),
        mpatches.Patch(color=PHASE_IN, label='Inbound cruise (~7 yr)'),
        mpatches.Patch(color=PHASE_DELIVER, label='Delivery to LEO'),
    ]
    ax.legend(handles=legend_handles, loc='upper right', fontsize=18.5, frameon=True, framealpha=1.0,
              ncol=1)

    ax.set_xlim(-7, 33)
    ax.set_ylim(-4.5, n_iceberg + 2.5)
    ax.set_xlabel('Years from ICEBERG program start', color=DASH_MUTED, fontsize=20)
    ax.set_yticks([])
    ax.grid(axis='x', alpha=1.0, zorder=0)
    ax.set_axisbelow(True)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_visible(False)

    fig.suptitle('The moat — fleet positions over time. The first operator is multiple generations ahead before the follower\'s first ship even launches.',
                 fontsize=24, fontweight='bold', x=0.05, ha='left', y=1.0, color=DASH_FG)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '10_moat.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

def plot_subway_map():
    """Solar-system delta-V transit map. ICEBERG line highlighted."""
    style_space()
    fig, ax = plt.subplots(figsize=(17, 11))
    ax.set_facecolor(INK_DARK)
    ax.set_xlim(0, 16)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

    # Subtle starfield
    rng = np.random.default_rng(13)
    n = 250
    ax.scatter(rng.uniform(0, 16, n), rng.uniform(0, 9, n),
               s=rng.exponential(0.4, n), c='white',
               alpha=rng.uniform(0.08, 0.4, n), zorder=0, linewidths=0)

    # Define stations: (name, x, y, type)
    # types: planet body (gold), orbit/station (blue), destination (teal), iceberg (red)
    stations = {
        'Earth':       (1.5, 5.0, 'planet'),
        'LEO':         (3.0, 5.0, 'orbit'),
        'GTO':         (3.8, 6.4, 'orbit'),
        'GEO':         (4.6, 7.6, 'orbit'),
        'EML1':        (4.5, 3.4, 'orbit'),
        'EML2':        (5.7, 2.5, 'orbit'),
        'Lunar surf':  (5.5, 1.4, 'planet'),
        'Lunar pole':  (4.0, 0.5, 'destination'),
        'C3=0':        (4.5, 5.0, 'orbit'),
        'NEA':         (5.7, 4.2, 'destination'),
        'Mars trans':  (7.0, 6.2, 'orbit'),
        'Mars orbit':  (8.4, 6.7, 'planet'),
        'Mars surf':   (9.5, 6.2, 'destination'),
        'Jupiter':     (10.7, 8.0, 'planet'),
        'Saturn arr':  (12.5, 5.0, 'orbit'),
        'Saturn ell':  (13.6, 5.0, 'orbit'),
        'Saturn ring': (14.8, 5.0, 'iceberg'),  # the ICEBERG destination
    }

    # Edges: (from, to, dv_kms, line_type)
    # line_type: 'chemical', 'electric', 'aero', 'iceberg' (highlighted)
    edges = [
        ('Earth', 'LEO', 9.4, 'chemical'),
        ('LEO', 'C3=0', 3.2, 'chemical'),
        ('LEO', 'GTO', 2.5, 'chemical'),
        ('GTO', 'GEO', 1.5, 'chemical'),
        ('LEO', 'EML1', 3.77, 'chemical'),
        ('EML1', 'EML2', 0.14, 'electric'),
        ('EML1', 'Lunar surf', 2.3, 'chemical'),
        ('Lunar surf', 'Lunar pole', 0.5, 'electric'),
        ('C3=0', 'NEA', 1.5, 'electric'),
        ('C3=0', 'Mars trans', 0.6, 'chemical'),
        ('Mars trans', 'Mars orbit', 0.9, 'aero'),
        ('Mars orbit', 'Mars surf', 0.5, 'aero'),
        # ICEBERG line — emphasize
        ('LEO', 'C3=0', 3.2, 'iceberg_a'),  # we'll overlay
        ('C3=0', 'Saturn arr', 7.1, 'iceberg'),  # TSI to Saturn approach (~10.3 V_inf, 7.1 added on top of C3=0 escape)
        ('Saturn arr', 'Saturn ell', 0.6, 'iceberg'),
        ('Saturn ell', 'Saturn ring', 1.5, 'iceberg'),
        # Saturn detour to Jupiter for flyby option
        ('C3=0', 'Jupiter', 6.3, 'electric'),
        ('Jupiter', 'Saturn arr', 0.0, 'aero'),  # gravity assist
    ]

    # Color map for line types
    line_colors = {
        'chemical': '#5fa8ff',
        'electric': '#3ed4c0',
        'aero':     '#e8b54e',
        'iceberg':  '#ff7676',  # the highlighted line
    }
    line_widths = {
        'chemical': 2.0,
        'electric': 2.0,
        'aero':     2.0,
        'iceberg':  4.5,
    }

    # Draw edges
    for from_st, to_st, dv, ltype in edges:
        x1, y1, _ = stations[from_st]
        x2, y2, _ = stations[to_st]
        if ltype == 'iceberg_a':
            continue  # overlay later
        color = line_colors.get(ltype, '#888')
        lw = line_widths.get(ltype, 2.0)
        # subtle glow for iceberg line
        if ltype == 'iceberg':
            for i in range(3, 0, -1):
                ax.plot([x1, x2], [y1, y2], color=color, lw=lw + i*2.5,
                        alpha=0.06, solid_capstyle='round', zorder=2)
        ax.plot([x1, x2], [y1, y2], color=color, lw=lw, alpha=0.92,
                solid_capstyle='round', zorder=3)

        # Label ΔV at midpoint
        mx, my = (x1+x2)/2, (y1+y2)/2
        dy_offset = 0.18
        ax.text(mx, my + dy_offset, f'{dv:.1f}',
                fontsize=13, color=color, fontweight='bold', ha='center', va='bottom',
                bbox=dict(facecolor=INK_DARK, edgecolor='none', pad=1.5),
                zorder=4)

    # Highlight ICEBERG segment: LEO -> C3=0 (overlay in red)
    x1, y1, _ = stations['LEO']
    x2, y2, _ = stations['C3=0']
    for i in range(3, 0, -1):
        ax.plot([x1, x2], [y1, y2], color='#ff7676', lw=4.5+i*2.5,
                alpha=0.06, solid_capstyle='round', zorder=2)
    ax.plot([x1, x2], [y1, y2], color='#ff7676', lw=4.5, alpha=0.92,
            solid_capstyle='round', zorder=3)

    # Draw stations
    station_styles = {
        'planet':      {'size': 220, 'color': ACCENT_GOLD, 'edge': 'white', 'tcolor': ACCENT_GOLD, 'zorder': 6},
        'orbit':       {'size': 100, 'color': INK_DARK, 'edge': ACCENT_BLUE, 'tcolor': ACCENT_BLUE, 'zorder': 6},
        'destination': {'size': 130, 'color': ACCENT_TEAL, 'edge': 'white', 'tcolor': ACCENT_TEAL, 'zorder': 6},
        'iceberg':     {'size': 280, 'color': ACCENT_RED, 'edge': 'white', 'tcolor': ACCENT_RED, 'zorder': 7},
    }

    for name, (x, y, stype) in stations.items():
        s = station_styles[stype]
        ax.scatter([x], [y], s=s['size'], c=s['color'],
                   edgecolors=s['edge'], linewidths=2, zorder=s['zorder'])
        # Label
        label_dy = 0.35 if stype != 'iceberg' else 0.45
        ax.text(x, y + label_dy, name, ha='center', va='bottom',
                fontsize=18.5 if stype != 'iceberg' else 11,
                color=s['tcolor'], fontweight='bold',
                zorder=8)

    # Legend at the very top, well clear of any station
    legend_y = 9.7
    legend_items = [
        ('chemical (impulsive)',   '#5fa8ff', 2.5),
        ('electric (low-thrust)',  '#3ed4c0', 2.5),
        ('aerocapture / gravity',  '#e8b54e', 2.5),
        ('PROJECT ICEBERG line',   '#ff7676', 4.5),
    ]
    for i, (label, color, lw) in enumerate(legend_items):
        x_start = 0.6 + i*3.8
        ax.plot([x_start, x_start+0.5], [legend_y, legend_y], color=color, lw=lw,
                solid_capstyle='round')
        ax.text(x_start+0.65, legend_y, label, fontsize=19, color=INK_TEXT,
                va='center', fontweight='bold')

    # Caption text at bottom
    ax.text(8, -0.2,
            'All ΔV figures in km/s.   The line we operate is one route on a network nobody else is building.',
            ha='center', fontsize=18.5, color=INK_MUTED, style='italic')

    fig.suptitle('Solar-system ΔV transit map  -  ICEBERG line highlighted',
                 color=INK_TEXT, fontsize=19, fontweight='bold', y=0.99)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '11_subway.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

def plot_bag_thermo():
    style_dashboard()
    fig, ax = plt.subplots(figsize=(13, 6))

    # Solar IR arrow
    for i in range(3):
        ax.annotate('', xy=(0.85+i*0.05, 2.8-i*0.05), xytext=(-0.5, 3+i*0.1),
                    arrowprops=dict(arrowstyle='->', color=DASH_AMBER,
                                    lw=2.2, alpha=0.8-0.2*i))
    ax.text(-0.55, 3.5, 'SOLAR IR\n1361 W/m² @ 1 AU', ha='right', va='center',
            fontsize=18.5, color=DASH_AMBER, fontweight='bold')

    # Bag outline (rounded rectangle)
    bag = mpatches.FancyBboxPatch((1, 1), 5.5, 3,
                                   boxstyle='round,pad=0.05,rounding_size=0.5',
                                   linewidth=2.5, edgecolor=DASH_FG,
                                   facecolor='#f0f4f9', alpha=0.7)
    ax.add_patch(bag)
    ax.text(3.75, 4.3, 'low-permeability bag (MLI heritage)',
            ha='center', fontsize=18, color=DASH_MUTED, style='italic')

    # Ice chunk (warm side)
    chunk = mpatches.Ellipse((2.7, 2.5), 1.9, 1.5, color='#bedbef',
                              edgecolor=DASH_BLUE, linewidth=2.5, alpha=0.95)
    ax.add_patch(chunk)
    ax.text(2.7, 2.5, 'ICE CHUNK\n200–230 K', ha='center', va='center',
            fontsize=19, fontweight='bold', color=DASH_FG)

    # Cold wall
    cold = mpatches.Rectangle((6.0, 1.05), 0.3, 2.9, color=DASH_BLUE, alpha=0.95)
    ax.add_patch(cold)
    ax.text(6.55, 2.5, 'COLD WALL\n<150 K\n(passive radiator)',
            ha='left', va='center', fontsize=18.5, color=DASH_BLUE,
            fontweight='bold')

    # Frost layer
    frost = mpatches.Rectangle((5.85, 1.05), 0.15, 2.9, color='white',
                                edgecolor='#d0d8e0', linewidth=0.8)
    ax.add_patch(frost)

    # Vapor flow arrows
    for y in [1.65, 2.5, 3.35]:
        ax.annotate('', xy=(5.8, y), xytext=(3.7, y),
                    arrowprops=dict(arrowstyle='->', color='#7c8aa0', lw=1.6))
    ax.text(4.75, 3.7, 'H₂O vapor — pressure-driven',
            ha='center', fontsize=18, color=DASH_MUTED, style='italic')

    # Harvest port
    ax.plot(6.15, 1.55, 'o', markersize=18, color=DASH_AMBER,
            markeredgecolor=DASH_FG, markeredgewidth=1.5, zorder=5)
    ax.annotate('Harvest port\n(local heater + MET feed)',
                xy=(6.15, 1.55), xytext=(7.5, 0.85),
                fontsize=18, ha='left', color=DASH_AMBER, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=DASH_AMBER, lw=1.4))

    # MET
    met = mpatches.FancyBboxPatch((8.2, 2.3), 0.9, 0.4,
                                   boxstyle='round,pad=0.02,rounding_size=0.08',
                                   color=DASH_GREEN, alpha=0.95)
    ax.add_patch(met)
    ax.text(8.65, 2.5, 'MET', ha='center', va='center', color='white',
            fontsize=19, fontweight='bold')
    ax.annotate('', xy=(8.2, 2.5), xytext=(6.4, 1.7),
                arrowprops=dict(arrowstyle='->', color=DASH_AMBER, lw=1.6))

    # Exhaust
    for i in range(4):
        ax.annotate('', xy=(10.3+i*0.15, 2.5), xytext=(9.1+i*0.15, 2.5),
                    arrowprops=dict(arrowstyle='->', color=DASH_GREEN,
                                    lw=2.2, alpha=0.85-0.15*i))
    ax.text(10.5, 1.9, 'thrust\nIsp ~700 s', ha='left', va='center',
            fontsize=18.5, color=DASH_GREEN, fontweight='bold')

    ax.set_xlim(-2, 12.5)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.suptitle('Bag-as-cold-trap — passive vapor management',
                 fontsize=18, fontweight='bold', x=0.05, ha='left', y=0.97,
                 color=DASH_FG)
    ax.set_title('Hot-side sublimation to vapor pressure gradient to cold-wall frost to metered MET feed',
                 fontsize=19.5, color=DASH_MUTED, fontweight='normal',
                 loc='left', pad=10)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '08_bag_thermo.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 12: Margin comparison — ICEBERG vs every other business class
# ============================================================================
def plot_margin_comparison():
    style_dashboard()
    rows = [
        ('Aerospace primes (Lockheed/Boeing)', 8.5, DASH_MUTED),
        ('S&P 500 average',                     11, DASH_MUTED),
        ('Big oil (ExxonMobil run rate)',       10, DASH_MUTED),
        ('Industrial manufacturing',            10, DASH_MUTED),
        ('Pipeline midstream / utilities',      28, DASH_MUTED),
        ('Apple / Google peak years',           28, DASH_MUTED),
        ('TSMC (gold-standard high-margin)',    38, DASH_MUTED),
        ('Saudi Aramco (peak)',                 52, DASH_MUTED),
        ('Panama Canal Authority',              65, DASH_AMBER),
        ('Suez Canal Authority',                70, DASH_AMBER),
        ('ICEBERG (steady state)',              76, DASH_TEAL),
    ]
    rows.sort(key=lambda r: r[1])
    names  = [r[0] for r in rows]
    vals   = [r[1] for r in rows]
    colors = [r[2] for r in rows]

    fig, ax = plt.subplots(figsize=(13, 7.2))
    ypos = np.arange(len(names))
    bars = ax.barh(ypos, vals, color=colors, edgecolor='white', height=0.72, zorder=3)
    ax.set_yticks(ypos)
    ax.set_yticklabels(names, fontsize=20, color=DASH_FG)
    iceberg_idx = names.index('ICEBERG (steady state)')
    ax.get_yticklabels()[iceberg_idx].set_fontweight('bold')
    ax.get_yticklabels()[iceberg_idx].set_color(DASH_TEAL)

    for bar, v in zip(bars, vals):
        ax.text(v + 1.0, bar.get_y() + bar.get_height()*0.5,
                f'{v:.0f}%', va='center', fontsize=19.5,
                fontweight='bold', color=DASH_FG)

    ax.set_xlim(0, 90)
    ax.set_xlabel('Net margin (%)', color=DASH_MUTED, fontsize=20)
    ax.grid(axis='x', alpha=1.0, zorder=1)
    ax.set_axisbelow(True)

    ax.axvspan(60, 90, color=DASH_AMBER, alpha=0.06, zorder=0)
    ax.text(75, len(names)-0.6, 'monopoly-chokepoint band',
            ha='center', fontsize=18.5, color=DASH_AMBER, fontweight='bold', style='italic')

    fig.suptitle('Steady-state net margin  -  ICEBERG sits with the canal authorities',
                 fontsize=19, fontweight='bold', x=0.05, ha='left', y=1.0, color=DASH_FG)
    ax.set_title('76% net margin is not a typical commercial business. It is the structural signature of a natural-monopoly infrastructure asset.',
                 fontsize=19.5, color=DASH_MUTED, loc='left', pad=12)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '12_margin_comparison.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 13: Perpetuity NPV asymmetry — max loss vs perpetuity upside
# ============================================================================
def plot_perpetuity_asymmetry():
    """Three columns: max loss (left, downward red), realistic upside range
    (center, teal), induced-demand upside (right, green). Clean side-by-side
    comparison with no overlapping labels."""
    style_dashboard()

    fig, ax = plt.subplots(figsize=(11, 5.0))

    # Three category positions
    x_loss = 0
    x_upside = 1
    x_optionality = 2

    # ===== LEFT: Max credible loss (downward bar) =====
    max_loss = 1.0
    ax.bar([x_loss], [-max_loss], width=0.5, color=DASH_RED, edgecolor='white', zorder=3)
    ax.text(x_loss, -max_loss - 6, '-1.0B',
            ha='center', va='center', fontsize=18, fontweight='bold', color=DASH_RED)
    ax.text(x_loss, -max_loss - 14, 'MAX CREDIBLE LOSS',
            ha='center', va='center', fontsize=18.5, fontweight='bold', color=DASH_RED)
    ax.text(x_loss, -max_loss - 19, 'Ship 1 fails late, ship 2 launched',
            ha='center', va='center', fontsize=13, color=DASH_MUTED, style='italic')

    # ===== CENTER: Realistic upside (range 12B-24B) =====
    upside_low = 12
    upside_high = 24
    ax.bar([x_upside], [upside_high], width=0.5, color=DASH_TEAL, edgecolor='white', zorder=3, alpha=0.4)
    ax.bar([x_upside], [upside_low], width=0.5, color=DASH_TEAL, edgecolor='white', zorder=4)
    ax.text(x_upside, upside_high + 8, '+12B to +24B',
            ha='center', va='center', fontsize=24, fontweight='bold', color=DASH_TEAL)
    ax.text(x_upside, -6, 'REALISTIC UPSIDE',
            ha='center', va='center', fontsize=18.5, fontweight='bold', color=DASH_TEAL)
    ax.text(x_upside, -14, 'Steady-state 1.2B/yr capitalized',
            ha='center', va='center', fontsize=13, color=DASH_MUTED, style='italic')

    # ===== RIGHT: Optionality upside (50B-200B) =====
    optionality_low = 50
    optionality_high = 200
    ax.bar([x_optionality], [optionality_high], width=0.5, color=DASH_GREEN, edgecolor='white', zorder=3, alpha=0.30)
    ax.bar([x_optionality], [optionality_low], width=0.5, color=DASH_GREEN, edgecolor='white', zorder=4)
    ax.text(x_optionality, optionality_high + 8, '+50B to +200B',
            ha='center', va='center', fontsize=24, fontweight='bold', color=DASH_GREEN)
    ax.text(x_optionality, -6, 'WITH INDUCED DEMAND',
            ha='center', va='center', fontsize=18.5, fontweight='bold', color=DASH_GREEN)
    ax.text(x_optionality, -14, 'Lunar landers, Mars, strategic reserve',
            ha='center', va='center', fontsize=13, color=DASH_MUTED, style='italic')

    # ===== Asymmetry callout in middle =====
    ax.text(1.0, 130, '12x to 200x payoff vs. max loss',
            ha='center', va='center', fontsize=24, fontweight='bold', color=DASH_AMBER,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=DASH_AMBER, linewidth=1.8))

    # Connect with subtle arrow from loss to upside
    ax.annotate('', xy=(x_optionality - 0.3, 90), xytext=(x_loss + 0.3, -2),
                arrowprops=dict(arrowstyle='-|>', color=DASH_AMBER, lw=1.5, alpha=0.7))

    # Axis cleanup
    ax.axhline(0, color=DASH_FG, lw=1.2, zorder=2)
    ax.set_ylim(-25, 225)
    ax.set_xlim(-0.55, 2.55)
    ax.set_xticks([])
    ax.set_ylabel('Present value ($ Billions)', color=DASH_MUTED, fontsize=19.5)
    ax.grid(axis='y', alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_visible(False)

    fig.suptitle('Asymmetric option: realistic upside is 12x to 200x the worst-case downside',
                 fontsize=18, fontweight='bold', x=0.05, ha='left', y=1.0, color=DASH_FG)
    ax.set_title('Steady-state cash flow (1.2B/yr at canal-authority margin) capitalizes to 12-24B in today\'s dollars; with induced demand from depot customers, 50-200B. Max credible loss is 1.0B. (All figures in USD.)',
                 fontsize=19, color=DASH_MUTED, loc='left', pad=12, wrap=True)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '13_perpetuity_asymmetry.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 14: NRE stress test — does the campaign survive 4x cost overruns?
# ============================================================================
def plot_nre_stress_test():
    style_dashboard()
    scenarios = [
        ('Baseline\n($240M NRE)',  1.04, 3.15, 2.11, DASH_GREEN),
        ('2x NRE\n($480M)',         1.28, 3.15, 1.87, DASH_GREEN),
        ('3x NRE\n($720M)',         1.52, 3.15, 1.63, DASH_AMBER),
        ('4x NRE\n($960M)',         1.76, 3.15, 1.39, DASH_AMBER),
    ]
    labels = [s[0] for s in scenarios]
    costs  = [s[1] for s in scenarios]
    revs   = [s[2] for s in scenarios]
    evs    = [s[3] for s in scenarios]
    colors = [s[4] for s in scenarios]

    fig, ax = plt.subplots(figsize=(13, 6.5))
    x = np.arange(len(scenarios))
    w = 0.28

    ax.bar(x - w, costs, w, label='Program cost',   color=DASH_RED,  edgecolor='white', zorder=3)
    ax.bar(x,     revs,  w, label='Expected revenue', color=DASH_BLUE, edgecolor='white', zorder=3)
    ax.bar(x + w, evs,   w, label='Net EV',          color=colors,    edgecolor='white', zorder=3)

    for i, (c, r, e) in enumerate(zip(costs, revs, evs)):
        ax.text(i - w, c + 0.06, f'${c:.2f}B', ha='center', fontsize=18.5, color=DASH_FG, fontweight='bold')
        ax.text(i,     r + 0.06, f'${r:.2f}B', ha='center', fontsize=18.5, color=DASH_FG, fontweight='bold')
        ax.text(i + w, e + 0.06, f'+${e:.2f}B', ha='center', fontsize=18.5, color=DASH_FG, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=19.5, color=DASH_FG)
    ax.set_ylabel('$ Billions (4-flight program)', color=DASH_MUTED, fontsize=20)
    ax.set_ylim(0, 3.7)
    ax.grid(axis='y', alpha=1.0, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc='upper right', fontsize=19, frameon=True, framealpha=1.0)

    ax.text(3.2, 0.05, 'EV stays positive\neven at 4x NRE blowout',
            ha='right', fontsize=20, color=DASH_AMBER, fontweight='bold', style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                      edgecolor=DASH_AMBER, linewidth=1.2))

    fig.suptitle('NRE stress test  -  the program survives 4x cost overruns',
                 fontsize=19, fontweight='bold', x=0.05, ha='left', y=1.0, color=DASH_FG)
    ax.set_title('Per-flight success-case revenue (~$2B at 750 t scale) is 5-7x per-flight cost across all NRE scenarios. Aerospace programs that survive 4x overruns and still print net positive ROI are vanishingly rare.',
                 fontsize=19.5, color=DASH_MUTED, loc='left', pad=12)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '14_nre_stress.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 15: Comparable-companies landscape — where ICEBERG sits
# ============================================================================
def plot_comparable_landscape():
    style_dashboard()
    # (name, years to first revenue, total program capital $B, steady-state cash flow $B/yr, color)
    comps = [
        ('Suez Canal',           10, 3,   9,   DASH_AMBER),
        ('Panama Canal',         33, 5,   4,   DASH_AMBER),
        ('Maersk fleet',         1,  50,  40,  DASH_MUTED),
        ('TSMC',                 3,  150, 30,  DASH_MUTED),
        ('SpaceX',               6,  10,  15,  DASH_MUTED),
        ('Starlink',             5,  10,  7,   DASH_MUTED),
        ('Cheniere LNG',         6,  20,  7,   DASH_MUTED),
        ('Boeing 787',           8,  32,  5,   DASH_MUTED),
        ('Amazon',               1,  3,   600, DASH_MUTED),
        ('ICEBERG',              17, 1,  1.85, DASH_TEAL),
    ]

    fig, ax = plt.subplots(figsize=(13, 7.2))
    for name, yrs, capital, ssf, color in comps:
        size = 60 + ssf * 18
        is_iceberg = (name == 'ICEBERG')
        ax.scatter([yrs], [capital], s=size, c=color,
                   edgecolors=DASH_FG if is_iceberg else 'white',
                   linewidths=2.5 if is_iceberg else 1.0,
                   alpha=0.95 if is_iceberg else 0.78, zorder=3)
        offset_y = capital * 1.20 if not is_iceberg else capital * 0.55
        ha = 'center'
        if name in ('Maersk fleet', 'TSMC'):
            offset_y = capital * 0.80
        ax.text(yrs, offset_y, name,
                ha=ha, fontsize=19.5,
                color=DASH_TEAL if is_iceberg else DASH_FG,
                fontweight='bold' if is_iceberg else 'normal', zorder=4)
        if is_iceberg:
            ax.annotate('long capital + small program +\nSuez-class chokepoint margin',
                        xy=(yrs, capital), xytext=(yrs - 6, capital * 4),
                        fontsize=19, color=DASH_TEAL, fontweight='bold',
                        ha='center',
                        arrowprops=dict(arrowstyle='-|>', color=DASH_TEAL, lw=1.5),
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                                  edgecolor=DASH_TEAL, linewidth=1.2))

    # Quadrants — long-capital region shaded
    ax.axvspan(10, 35, color=DASH_AMBER, alpha=0.05, zorder=0)
    ax.text(22.5, 0.6, 'patient-capital regime\n(>10 yr to first revenue)',
            ha='center', fontsize=18.5, color=DASH_AMBER, fontweight='bold', style='italic')

    ax.set_xscale('linear')
    ax.set_yscale('log')
    ax.set_xlim(-2, 36)
    ax.set_ylim(0.5, 300)
    ax.set_xlabel('Years to first revenue', color=DASH_MUTED, fontsize=20)
    ax.set_ylabel('Total program capital ($B, log scale)', color=DASH_MUTED, fontsize=20)
    ax.grid(alpha=1.0, which='both', zorder=0)
    ax.set_axisbelow(True)

    fig.suptitle('Comparable landscape  -  ICEBERG looks like Maersk + Starlink wrapped in Suez timing',
                 fontsize=19, fontweight='bold', x=0.05, ha='left', y=1.0, color=DASH_FG)
    ax.set_title('Bubble size = steady-state cash flow ($B/yr). ICEBERG sits in the patient-capital regime alongside the canal authorities, with smaller program capital than every fleet/infrastructure comparable.',
                 fontsize=19.5, color=DASH_MUTED, loc='left', pad=12)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '15_comparable_landscape.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
# Plot 16: Campaign Gantt — gates + flights + production cadence
# ============================================================================
def plot_campaign_gantt():
    """Horizontal Gantt of the campaign: demonstrators, gates, Saturn fleet.
    Vertical milestone lines mark moat-set, first delivery, etc."""
    style_dashboard()
    fig, ax = plt.subplots(figsize=(13, 7.2))

    PHASE_DEMO    = '#a78bfa'
    PHASE_GROUND  = '#cbd2dc'
    PHASE_BUILD   = '#cbd2dc'
    PHASE_OUT     = DASH_BLUE
    PHASE_SATURN  = DASH_AMBER
    PHASE_IN      = DASH_TEAL
    PHASE_DELIVER = DASH_GREEN

    # Track entries: (label, start, end, color, alpha)
    # Demonstrator flights
    rows = []

    # Gate C ground qualification (years 1-5)
    rows.append(('Gate C: bag MTBF + 9 AU power qual\n(ground / vacuum chamber)',
                 1.0, 5.0, PHASE_GROUND, 0.7, 'gate'))

    # Flight 2 — cislunar pole demo
    rows.append(('Gate B: Flight 2 — cislunar pole demo\n($180M, 5 t demo cargo, year 2-3)',
                 0.5, 3.0, PHASE_DEMO, 1.0, 'flight'))

    # Flight 1 — LEO debris demo
    rows.append(('Gate A: Flight 1 — LEO debris capture\n($80M, no cargo, year 0.5-1.5)',
                 0.0, 1.5, PHASE_DEMO, 1.0, 'flight'))

    # Saturn ships — each is build then full mission
    saturn_ships = [
        ('Ship 3 — Saturn 1st commercial (50 t)',  3.0, 5.0, 11.0, 11.5, 18.0),
        ('Ship 4 — Saturn (50–100 t)',             4.5, 6.5, 12.5, 13.0, 19.5),
        ('Ship 5 — Saturn (100 t)',                6.0, 8.0, 14.0, 14.5, 21.0),
        ('Ship 6 — Saturn (200 t)',                7.5, 9.5, 15.5, 16.0, 22.5),
    ]

    # Plot demonstrators / ground qual first (3 rows, top to bottom)
    for i, (label, start, end, color, alpha, kind) in enumerate(rows):
        y = len(rows) + len(saturn_ships) - i - 1
        ax.barh(y, end - start, left=start, color=color, edgecolor='white',
                height=0.62, zorder=3, alpha=alpha)
        ax.text(start - 0.5, y, label, ha='right', va='center',
                fontsize=18, color=DASH_FG, fontweight='bold' if kind == 'flight' else 'normal')

    # Plot Saturn ships
    for i, (label, build, launch, capture, depart, deliver) in enumerate(saturn_ships):
        y = len(saturn_ships) - i - 1
        # Build
        ax.barh(y, launch - build, left=build, color=PHASE_BUILD, edgecolor='white', height=0.62, zorder=3)
        # Outbound
        ax.barh(y, capture - launch, left=launch, color=PHASE_OUT, edgecolor='white', height=0.62, zorder=3)
        # Saturn ops
        ax.barh(y, depart - capture, left=capture, color=PHASE_SATURN, edgecolor='white', height=0.62, zorder=4)
        # Inbound
        ax.barh(y, deliver - depart, left=depart, color=PHASE_IN, edgecolor='white', height=0.62, zorder=3)
        # Delivery marker
        ax.plot(deliver, y, 'o', markersize=10, color=PHASE_DELIVER,
                markerfacecolor=PHASE_DELIVER, markeredgecolor='white', markeredgewidth=1.5, zorder=6)
        ax.text(build - 0.5, y, label, ha='right', va='center', fontsize=18, color=DASH_FG, fontweight='bold')

    # Section divider
    divider_y = len(saturn_ships) - 0.5
    ax.axhline(divider_y, color=DASH_GRID, lw=1.5, alpha=0.6, zorder=2)
    ax.text(-7, divider_y - 0.4, 'SATURN FLEET', ha='right', va='center',
            fontsize=19, fontweight='bold', color=DASH_AMBER)
    ax.text(-7, divider_y + 0.4, 'GATES + DEMOS', ha='right', va='center',
            fontsize=19, fontweight='bold', color='#7c5fcc')

    # Critical milestones
    milestones = [
        (5.0, 'Gates A–C close\n(architecture qualified)', '#7c5fcc'),
        (11.0, 'MOAT SET\n(Ship 3 captures at Saturn)', DASH_AMBER),
        (18.0, 'First delivery\n(Ship 3, 50 t to LEO)', DASH_GREEN),
    ]
    for x, label, color in milestones:
        ax.axvline(x, color=color, lw=1.8, ls='--', alpha=0.6, zorder=2)
        ax.text(x, len(rows) + len(saturn_ships) + 0.3, label,
                ha='center', va='bottom', fontsize=18.5, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, lw=1.2))

    # Phase legend
    legend_handles = [
        mpatches.Patch(color=PHASE_DEMO, label='Demonstrator flight'),
        mpatches.Patch(color=PHASE_GROUND, label='Ground qualification'),
        mpatches.Patch(color=PHASE_OUT, label='Outbound cruise (6.1 yr)'),
        mpatches.Patch(color=PHASE_SATURN, label='Saturn ops'),
        mpatches.Patch(color=PHASE_IN, label='Inbound cruise (~7 yr)'),
        mpatches.Patch(color=PHASE_DELIVER, label='Delivery to LEO'),
    ]
    ax.legend(handles=legend_handles, loc='lower right', fontsize=18, frameon=True, framealpha=1.0)

    ax.set_xlim(-12, 24)
    ax.set_ylim(-1, len(rows) + len(saturn_ships) + 1.5)
    ax.set_xlabel('Years from program start', color=DASH_MUTED, fontsize=20)
    ax.set_yticks([])
    ax.grid(axis='x', alpha=1.0, zorder=0)
    ax.set_axisbelow(True)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_visible(False)

    fig.suptitle('Campaign cadence — gates A–C close by year 5, then production cadence at every synodic window',
                 fontsize=24, fontweight='bold', x=0.05, ha='left', y=1.0, color=DASH_FG)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, '16_campaign_gantt.png')
    plt.savefig(out)
    plt.close()
    print(f"  wrote {out}")

# ============================================================================
if __name__ == '__main__':
    print(f"Using font: {SANS}")
    print("Generating ConOps plots...")
    plot_mission_flightplan()
    plot_heliocentric()
    plot_saturn_capture()
    plot_ring_rendezvous()
    plot_close_approach()
    plot_earth_lga()
    plot_dv_budget()
    plot_mass_budget()
    plot_timeline()
    plot_trawl_collection()
    plot_trawl_cruise()
    plot_cashflow_milestones()    # replaces plot_cumulative_cashflow
    plot_moat()
    plot_subway_map()
    plot_margin_comparison()
    plot_perpetuity_asymmetry()
    plot_nre_stress_test()
    plot_comparable_landscape()
    plot_campaign_gantt()
    print("Done.")
