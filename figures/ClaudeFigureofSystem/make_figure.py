#!/usr/bin/env python3
# =============================================================================
#  FM | AB-BLG | SC device -- publication figure
#
#  (a),(b) Blender renders, put at a COMMON scale and aligned on the FM lead.
#          No text is baked into the images: every label in the figure is set
#          in the same LaTeX font as the manuscript.
#  (c),(d) true vector art, same palette as the renders.
#
#  Output: system_v2.pdf   (vector text/line art + embedded raster renders)
#
#  If you re-render in Blender, export transparent-background PNGs with the
#  same camera for both cases and drop them in as renderA.png / renderB.png.
# =============================================================================
import numpy as np
import matplotlib
matplotlib.use("pgf")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from PIL import Image

# ------------------------------------------------------------------ typography
PRE = "\n".join([r"\usepackage{amsmath}",
                 r"\usepackage{amssymb}",
                 r"\usepackage{bm}"])
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "pgf.rcfonts": False,
    "pgf.preamble": PRE,
    "font.size": 8,
    "axes.linewidth": 0.6,
    "figure.dpi": 330,          # ~1:1 with the source renders (no resampling loss)
})

FS_PANEL, FS_MAIN, FS_SMALL, FS_TINY = 9, 8, 7, 6.2

# ---------------------------------------------------------------------- palette
L1_LIGHT, L1_DARK = "#E8419E", "#7B2E56"     # layer 1 : A1 (dimer) / B1
L2_LIGHT, L2_DARK = "#33BFD1", "#2E7B82"     # layer 2 : B2 (dimer) / A2
FM_LIGHT, FM_DARK = "#8C8C8C", "#3E3E3E"
SC_LIGHT, SC_DARK = "#6E93DC", "#2B4577"
ACCENT, INK, MUTED = "#8B2E5C", "#1A1A1A", "#666666"


def tint(c, f):
    v = np.array(mcolors.to_rgb(c))
    return tuple(v + (1.0 - v) * f)


# ------------------------------------------------------------------ page layout
W, H = 7.0, 5.70                              # inches; PRB figure* = 7.0 in


def ax_in(fig, x, y, w, h):
    a = fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])
    a.set_axis_off()
    return a


def fig_text(x, y, s, **kw):
    return fig.text(x / W, 1 - y / H, s, **kw)


fig = plt.figure(figsize=(W, H))

# =============================================================================
#  (a) and (b)  --  Blender renders
# =============================================================================
imgs = {k: np.array(Image.open(f"render{k}.png")) for k in "AB"}


def fm_top(img):
    """Row of the topmost pixel of the (grey) FM lead."""
    rgb = img[..., :3] / 255.0
    al = img[..., 3] > 0
    mx, mn = rgb.max(2), rgb.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    g = al & (sat < 0.12) & (mx < 0.82)
    g[:, int(0.28 * img.shape[1]):] = False
    return np.where(g.any(1))[0].min()


SCALE = 6.28 / max(i.shape[1] for i in imgs.values())   # inches per pixel
X0 = 0.62                                               # left edge of renders
ROW_TOP = {"A": 0.42, "B": 1.95}                        # top of each render row

geom = {}
for k, img in imgs.items():
    y_in = ROW_TOP[k] - (fm_top(img) - fm_top(imgs["A"])) * SCALE
    w_in, h_in = img.shape[1] * SCALE, img.shape[0] * SCALE
    ax = ax_in(fig, X0, y_in, w_in, h_in)
    ax.imshow(img, interpolation="lanczos")
    geom[k] = (w_in, h_in, y_in)

# ---- headers ---------------------------------------------------------------
HEAD = {"A": (0.13, "a", r"$1\!\to\!1$", r"SC lead on layer 1"),
        "B": (1.66, "b", r"$1\!\to\!2$", r"SC lead on layer 2")}
REGIONS = [(0.135, "FM", FM_DARK, r"monolayer, $\bm{h}$"),
           (0.510, "BLG", L2_DARK, r"AB-stacked bilayer"),
           (0.880, "SC", SC_DARK, r"$s$-wave, $\Delta$")]

for k, (yb, letter, arrow, cap) in HEAD.items():
    fig_text(0.04, yb, r"\textbf{(%s)}" % letter, fontsize=FS_PANEL,
             ha="left", va="baseline", color=INK)
    fig_text(0.30, yb, arrow, fontsize=FS_PANEL, ha="left",
             va="baseline", color=ACCENT)
    fig_text(0.30, yb + 0.165, cap, fontsize=FS_TINY, ha="left",
             va="baseline", color=MUTED)
    w_in = geom[k][0]
    for fx, name, col, sub in REGIONS:
        x = X0 + fx * w_in
        fig_text(x, yb, r"\textbf{%s}" % name, fontsize=FS_MAIN,
                 ha="center", va="baseline", color=col)
        fig_text(x, yb + 0.165, sub, fontsize=FS_TINY, ha="center",
                 va="baseline", color=col)

# ---- m / n index arrows ----------------------------------------------------
for k, ytop in (("A", 0.72), ("B", 2.20)):
    axi = ax_in(fig, 0.05, ytop, 0.54, 0.66)
    axi.set_xlim(0, 1)
    axi.set_ylim(0, 1)
    axi.add_patch(FancyArrowPatch((0.05, 0.16), (0.93, 0.16), arrowstyle="-|>",
                                  mutation_scale=6, lw=0.8, color=INK))
    axi.text(0.49, 0.00, r"$m$", fontsize=FS_MAIN, ha="center",
             va="bottom", color=INK)
    axi.add_patch(FancyArrowPatch((0.05, 0.46), (0.87, 0.96), arrowstyle="-|>",
                                  mutation_scale=6, lw=0.8, color=INK))
    axi.text(0.26, 0.74, r"$n$", fontsize=FS_MAIN, ha="center",
             va="bottom", color=INK)

# =============================================================================
#  (c)  --  AB (Bernal) stacking, top view
# =============================================================================
axc = ax_in(fig, 0.10, 3.22, 2.30, 2.30)
axc.set_aspect("equal")
LIM = 2.30
LAT_TOP = 1.02                       # lattice is drawn only below this line
axc.set_xlim(-LIM, LIM)
axc.set_ylim(-LIM, LIM)

a1 = np.array([1.0, 0.0])
a2 = np.array([0.5, np.sqrt(3) / 2])
d = [np.array([0.0, 1 / np.sqrt(3)]),
     np.array([-0.5, -1 / (2 * np.sqrt(3))]),
     np.array([0.5, -1 / (2 * np.sqrt(3))])]
Rs = [n1 * a1 + n2 * a2 for n1 in range(-8, 9) for n2 in range(-8, 9)]


def inside(p, pad=0.30):
    return (-LIM - pad < p[0] < LIM + pad) and (-LIM - pad < p[1] < LAT_TOP)


def honeycomb(shift):
    bonds, A, B = [], [], []
    for R in Rs:
        P = R + shift
        if not inside(P):
            continue
        A.append(P)
        for dd in d:
            Q = P + dd
            if inside(Q):
                bonds.append((P, Q))
                B.append(Q)
    return bonds, np.array(A), np.array(B)


def draw(bonds, col, lw, z, halo=False):
    for P, Q in bonds:
        if halo:
            axc.add_line(Line2D([P[0], Q[0]], [P[1], Q[1]], color="white",
                                lw=lw + 1.8, solid_capstyle="round",
                                zorder=z - 0.1))
        axc.add_line(Line2D([P[0], Q[0]], [P[1], Q[1]], color=col, lw=lw,
                            solid_capstyle="round", zorder=z))


def dots(P, r, fc, z, ec="white", lw=0.6):
    for p in P:
        axc.add_patch(Circle(p, r, fc=fc, ec=ec, lw=lw, zorder=z))


bonds1, A1, B1 = honeycomb(np.zeros(2))          # layer 1 (below)
bonds2, A2, B2 = honeycomb(-d[0])                # layer 2 (above); B2 == A1
draw(bonds1, tint(L1_DARK, 0.30), 1.9, 2)
dots(B1, 0.115, L1_DARK, 3)
draw(bonds2, tint(L2_DARK, 0.10), 1.9, 4, halo=True)
dots(A2, 0.115, L2_DARK, 5)
dots(A1, 0.140, L1_LIGHT, 6)                     # A1 underneath ...
dots(A1, 0.072, L2_LIGHT, 7, ec="none")          # ... with B2 sitting on it


# ---- direct sublattice labels ---------------------------------------------
def nearest(P, target):
    return P[np.argmin(np.linalg.norm(P - np.array(target), axis=1))]


def tag(p, txt, col, dx, dy, ha="left"):
    axc.text(p[0] + dx, p[1] + dy, txt, fontsize=FS_SMALL, color=col,
             ha=ha, va="center", zorder=12,
             bbox=dict(fc="white", ec="none", pad=0.9, alpha=0.95))


tag(nearest(B1, (-1.75, -1.45)), r"$B_1$", L1_DARK, 0.18, -0.02, ha="left")
tag(nearest(A2, (1.5, -1.55)), r"$A_2$", L2_DARK, 0.16, -0.02)
tag(nearest(A1, (-1.9, 0.05)), r"$A_1\!/\!B_2$", ACCENT, 0.20, 0.02, ha="left")

# ---- lattice vectors -------------------------------------------------------
org = nearest(A1, (-0.10, -1.85))
for v, nm, off in ((a1, r"$\bm{a}_1$", (0.00, -0.28)),
                   (a2, r"$\bm{a}_2$", (-0.30, 0.02))):
    axc.add_patch(FancyArrowPatch(org, org + v, arrowstyle="-|>",
                                  mutation_scale=5, lw=0.7, color=INK, zorder=12))
    m = org + 0.58 * v + np.array(off)
    axc.text(m[0], m[1], nm, fontsize=FS_TINY, color=INK, zorder=12,
             ha="center", va="center",
             bbox=dict(fc="white", ec="none", pad=0.6, alpha=0.95))

# ---- dimer call-out (side view), in the clear strip above the lattice ------
dm = nearest(A1, (-0.55, 0.90))
axc.add_patch(Circle(dm, 0.26, fc="none", ec=MUTED, lw=0.7,
                     ls=(0, (2, 1.6)), zorder=13))
BX, BY, BW, BH = -2.25, 1.22, 4.50, 1.00
axc.add_patch(FancyBboxPatch((BX, BY), BW, BH,
                             boxstyle="round,pad=0.02,rounding_size=0.10",
                             fc="#FAFAFA", ec="#CCCCCC", lw=0.6, zorder=14))
axc.add_line(Line2D([dm[0], dm[0] + 0.30], [dm[1] + 0.26, BY - 0.02],
                    color=MUTED, lw=0.6, ls=(0, (2, 1.6)), zorder=13))
sx, sy = BX + 0.45, BY + BH / 2
axc.add_line(Line2D([sx, sx], [sy - 0.22, sy + 0.22], color=INK, lw=1.0, zorder=15))
axc.add_patch(Circle((sx, sy + 0.24), 0.10, fc=L2_LIGHT, ec="white", lw=0.6, zorder=16))
axc.add_patch(Circle((sx, sy - 0.24), 0.10, fc=L1_LIGHT, ec="white", lw=0.6, zorder=16))
axc.text(sx - 0.13, sy, r"$t_\perp$", fontsize=FS_SMALL, color=INK,
         va="center", ha="right", zorder=16)
axc.text(sx + 0.20, sy + 0.24, r"$B_2$, layer 2", fontsize=FS_TINY,
         color=L2_DARK, va="center", ha="left", zorder=16)
axc.text(sx + 0.20, sy - 0.24, r"$A_1$, layer 1", fontsize=FS_TINY,
         color=L1_DARK, va="center", ha="left", zorder=16)
axc.text(sx + 1.35, sy + 0.24, r"dimer sites lie on top of each other",
         fontsize=FS_TINY, color=INK, va="center", ha="left", zorder=16)
axc.text(sx + 1.35, sy - 0.24, r"and are coupled by $t_\perp$",
         fontsize=FS_TINY, color=INK, va="center", ha="left", zorder=16)

fig_text(0.06, 3.06, r"\textbf{(c)}", fontsize=FS_PANEL, ha="left", va="baseline")
fig_text(0.32, 3.06, r"AB (Bernal) stacking, top view", fontsize=FS_MAIN,
         ha="left", va="baseline", color=INK)

# =============================================================================
#  (d)  --  layer connectivity along the transport direction
# =============================================================================
axd = ax_in(fig, 2.62, 3.22, 4.30, 2.30)
axd.set_xlim(0, 10.6)
axd.set_ylim(0, 6.35)

LH = 0.60                                  # lane height
XF0, XF1 = 0.62, 3.45                      # FM lead
XC0, XC1 = 3.45, 7.15                      # central region
XS0, XS1 = 7.15, 10.05                     # SC lead


def lane(y, x0, x1, edge, face, label, sub=None):
    axd.add_patch(FancyBboxPatch((x0, y), x1 - x0, LH,
                                 boxstyle="round,pad=0,rounding_size=0.10",
                                 fc=face, ec=edge, lw=0.9, zorder=3))
    axd.text((x0 + x1) / 2, y + LH / 2 + (0.10 if sub else 0), label,
             ha="center", va="center", fontsize=FS_SMALL, color=edge, zorder=4)
    if sub:
        axd.text((x0 + x1) / 2, y + LH / 2 - 0.15, sub, ha="center",
                 va="center", fontsize=FS_TINY, color=edge, zorder=4)


def case(y1, title, sc_on_top):
    y2 = y1 + LH + 0.58
    lane(y1, XF0, XF1, FM_DARK, tint(FM_LIGHT, 0.74), r"FM monolayer", r"$\bm{h}$")
    lane(y1, XC0, XC1, L1_DARK, tint(L1_LIGHT, 0.80), r"central layer 1")
    lane(y2, XC0, XC1, L2_DARK, tint(L2_LIGHT, 0.80), r"central layer 2")
    lane(y2 if sc_on_top else y1, XS0, XS1, SC_DARK, tint(SC_LIGHT, 0.74),
         r"$s$-wave SC lead", r"$\Delta e^{i\varphi}$")

    for x in np.linspace(XC0 + 0.30, XC1 - 0.55, 8):
        axd.add_line(Line2D([x, x], [y1 + LH, y2], color=INK, lw=0.7,
                            alpha=0.7, zorder=2))
    axd.text(XC1 - 0.30, (y1 + LH + y2) / 2, r"$t_\perp$", fontsize=FS_SMALL,
             color=INK, ha="left", va="center", zorder=5)

    axd.text(0.20, (y1 + y2 + LH) / 2, title, fontsize=FS_PANEL, color=ACCENT,
             ha="center", va="center", rotation=90)

    ya = y1 - 0.46
    axd.add_patch(FancyArrowPatch((XC0, ya), (XC1, ya), arrowstyle="<|-|>",
                                  mutation_scale=5, lw=0.7, color=INK,
                                  shrinkA=0, shrinkB=0))
    axd.text((XC0 + XC1) / 2, ya - 0.02, r"$N$ transfer steps", ha="center",
             va="center", fontsize=FS_TINY, color=INK,
             bbox=dict(fc="white", ec="none", pad=1.0))
    axd.text(XC0 + 0.06, ya - 0.30, r"$m\!=\!1$", ha="left", va="center",
             fontsize=FS_TINY, color=MUTED)
    axd.text(XC1 - 0.06, ya - 0.30, r"$m\!=\!N$", ha="right", va="center",
             fontsize=FS_TINY, color=MUTED)
    axd.text(XF1 - 0.14, ya, r"$m\!\leq\!0$", ha="right", va="center",
             fontsize=FS_TINY, color=FM_DARK)
    axd.text(XS0 + 0.14, ya, r"$m\!\geq\!N\!+\!1$", ha="left", va="center",
             fontsize=FS_TINY, color=SC_DARK)
    for x in (XC0, XC1):
        axd.add_line(Line2D([x, x], [ya - 0.16, y2 + LH + 0.06], color="#BBBBBB",
                            lw=0.5, ls=(0, (1.6, 1.8)), zorder=1))


case(4.05, r"$1\!\to\!1$", sc_on_top=False)
case(0.95, r"$1\!\to\!2$", sc_on_top=True)

fig_text(2.62, 3.06, r"\textbf{(d)}", fontsize=FS_PANEL, ha="left", va="baseline")
fig_text(2.88, 3.06, r"Layer connectivity along the transport direction",
         fontsize=FS_MAIN, ha="left", va="baseline", color=INK)

fig.savefig("system_v2.pdf")
fig.savefig("system_v2.png", dpi=600)
print("written system_v2.pdf / .png")
