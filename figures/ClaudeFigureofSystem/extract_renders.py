#!/usr/bin/env python3
"""
Pull the two Blender renders out of the original bitmap figure, discarding the
baked-in text labels.

The renders are each a single 8-connected ink component, and every label is a
separate component, so a connected-component analysis separates them cleanly.
Small interior holes (specular highlights on the spheres) are filled back in so
the spheres keep their shading; large holes (the hexagon interiors) are kept.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/mnt/user-data/uploads/system.png"
COMPONENTS = {"renderA": 12, "renderB": 32}
MAX_HOLE = 400          # px^2 -- larger holes are real hexagons, keep them

im = Image.open(SRC).convert("RGBA")
flat = np.array(Image.alpha_composite(
    Image.new("RGBA", im.size, (255, 255, 255, 255)), im).convert("RGB"))
gray = np.array(Image.fromarray(flat).convert("L"))

ink = gray < 250
lab, _ = ndimage.label(ink, structure=np.ones((3, 3)))

for name, comp in COMPONENTS.items():
    m = lab == comp

    # fill only the small holes (sphere highlights)
    filled = ndimage.binary_fill_holes(m)
    holes = filled & ~m
    hl, nh = ndimage.label(holes)
    if nh:
        sizes = ndimage.sum(holes, hl, range(1, nh + 1))
        small = np.isin(hl, np.where(sizes < MAX_HOLE)[0] + 1)
        m = m | small

    # a couple of pixels of dilation recovers the anti-aliased outline
    m = ndimage.binary_dilation(m, np.ones((3, 3)), iterations=2)

    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([flat[y0:y1, x0:x1],
                      (m[y0:y1, x0:x1] * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(name + ".png")
    print(f"{name}: {x1-x0} x {y1-y0} px  (bbox {x0},{y0})")
