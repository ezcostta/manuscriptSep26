import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from PIL import Image

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["axes.linewidth"] = 0.6

img_a = np.array(Image.open("geom_1to1.png"))
img_b = np.array(Image.open("geom_1to2.png"))
Him, Wim = img_a.shape[0], img_a.shape[1]
aspect = Him / Wim

FM_CENTER = 0.170
BLG_CENTER = 0.492
SC_CENTER = 0.867
BLG_X0, BLG_X1 = 0.251, 0.754

FIG_W_MM = 180.0
FIG_W_IN = FIG_W_MM / 25.4

PANEL_W = 0.86
LABEL_BAND_IN = 0.44
DIM_BAND_IN = 0.34
PANEL_GAP_IN = 0.16
TOP_MARGIN_IN = 0.06
BOTTOM_MARGIN_IN = 0.30

panel_w_in = FIG_W_IN * PANEL_W
panel_h_in = panel_w_in * aspect

FIG_H_IN = (
    TOP_MARGIN_IN
    + LABEL_BAND_IN + panel_h_in + DIM_BAND_IN
    + PANEL_GAP_IN
    + LABEL_BAND_IN + panel_h_in + DIM_BAND_IN
    + BOTTOM_MARGIN_IN
)

fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), facecolor="white")
x0 = (1 - PANEL_W) / 2.0


def frac(inches):
    return inches / panel_h_in


def add_panel(y_bottom_in, img, label, subtitle):
    ax_h = panel_h_in / FIG_H_IN
    ax_y = y_bottom_in / FIG_H_IN
    ax = fig.add_axes([x0, ax_y, PANEL_W, ax_h])
    ax.imshow(img, extent=[0, 1, 0, 1], aspect="auto", interpolation="lanczos")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    rect = Rectangle((0, 0), 1, 1, transform=ax.transAxes, fill=False,
                      edgecolor="#4a4a4a", linewidth=0.6, zorder=10)
    ax.add_patch(rect)

    ax.text(0.018, 0.90, label, transform=ax.transAxes, ha="left", va="top",
             fontsize=11, fontweight="bold", color="#1a1a1a", zorder=11)
    ax.text(0.075, 0.895, subtitle, transform=ax.transAxes, ha="left", va="top",
             fontsize=8.3, color="#1a1a1a", alpha=0.95, zorder=11)

    return ax


def add_region_labels(ax):
    line_top = frac(0.05)
    line_end = frac(0.13)
    main_y = frac(0.15)
    sub_y = frac(0.31)

    label_defs = [(FM_CENTER, "FM"), (BLG_CENTER, "BLG"), (SC_CENTER, "SC")]
    for xc, txt in label_defs:
        ax.plot([xc, xc], [1 + line_top, 1 + line_end], transform=ax.transAxes,
                color="#8a8a8a", lw=0.6, clip_on=False, zorder=11)
        ax.text(xc, 1 + main_y, txt, transform=ax.transAxes, ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", color="#1a1a1a", zorder=11)

    ax.text(BLG_CENTER, 1 + sub_y, "(AB-stacked)", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=6.3, style="italic", color="#5a5a5a")
    ax.text(FM_CENTER, 1 + sub_y, r"$\vec{h}$", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=9.5, color="#1a1a1a")
    ax.text(SC_CENTER, 1 + sub_y, r"$\Delta$", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=9.5, color="#1a1a1a")


def add_dimension(ax):
    y_arrow = -frac(0.15)
    y_tick = frac(0.045)
    y_text = -frac(0.30)

    ax.annotate("", xy=(BLG_X1, y_arrow), xytext=(BLG_X0, y_arrow),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="<->", color="#1a1a1a", lw=0.7,
                                 shrinkA=0, shrinkB=0),
                annotation_clip=False)
    for xv in (BLG_X0, BLG_X1):
        ax.plot([xv, xv], [y_arrow - y_tick, y_arrow + y_tick], transform=ax.transAxes,
                color="#1a1a1a", lw=0.7, clip_on=False)
    ax.text((BLG_X0 + BLG_X1) / 2, y_text, r"$N$", transform=ax.transAxes,
            ha="center", va="top", fontsize=9.5, color="#1a1a1a")


def add_transport_arrow(ax):
    y = -frac(0.15)
    ax.annotate("", xy=(0.135, y), xytext=(0.045, y),
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="#1a1a1a", lw=0.9,
                                 shrinkA=0, shrinkB=0, mutation_scale=8),
                annotation_clip=False)
    ax.text(0.09, -frac(0.30), r"$x$", transform=ax.transAxes, ha="center",
            va="top", fontsize=9, color="#1a1a1a")


y_b_bottom = BOTTOM_MARGIN_IN + DIM_BAND_IN
y_a_bottom = y_b_bottom + panel_h_in + LABEL_BAND_IN + PANEL_GAP_IN + DIM_BAND_IN

ax_a = add_panel(y_a_bottom, img_a, "(a)", "Geometry 1 \u2192 1")
add_region_labels(ax_a)
add_dimension(ax_a)

ax_b = add_panel(y_b_bottom, img_b, "(b)", "Geometry 1 \u2192 2")
add_region_labels(ax_b)
add_dimension(ax_b)
add_transport_arrow(ax_b)

leg_y_in = BOTTOM_MARGIN_IN * 0.50
leg_y = leg_y_in / FIG_H_IN
leg_ax = fig.add_axes([0, 0, 1, 1])
leg_ax.axis("off")
leg_ax.set_xlim(0, 1)
leg_ax.set_ylim(0, 1)

cx1, cx2 = 0.335, 0.605
sw = 0.014
leg_ax.add_patch(Rectangle((cx1, leg_y - sw/2), sw, sw, transform=leg_ax.transAxes,
                            facecolor="#33e6e6", edgecolor="none"))
leg_ax.text(cx1 + sw*1.6, leg_y, r"Layer 1 ($\Lambda=1$)", transform=leg_ax.transAxes,
            ha="left", va="center", fontsize=7.6, color="#1a1a1a")

leg_ax.add_patch(Rectangle((cx2, leg_y - sw/2), sw, sw, transform=leg_ax.transAxes,
                            facecolor="#ec1e8c", edgecolor="none"))
leg_ax.text(cx2 + sw*1.6, leg_y, r"Layer 2 ($\Lambda=2$)", transform=leg_ax.transAxes,
            ha="left", va="center", fontsize=7.6, color="#1a1a1a")

fig.savefig("figure_bilayer_junction.pdf", dpi=450)
fig.savefig("figure_bilayer_junction.svg", dpi=450)
fig.savefig("figure_preview.png", dpi=450)
print("Figure size (in):", FIG_W_IN, FIG_H_IN, " mm:", FIG_W_IN*25.4, FIG_H_IN*25.4)
