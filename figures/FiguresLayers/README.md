# FM–BLG–SC junction figure — package README

Two-panel figure comparing the two junction geometries:

- **(a) Geometry 1→1** — left (FM) and right (SC) monolayer leads connect
  to the **same** graphene layer of the central bilayer.
- **(b) Geometry 1→2** — the left and right leads connect to **different**
  graphene layers.

This was built from the two supplied Blender renders. Their correspondence
to 1→1 / 1→2 was determined by inspecting the FM|BLG and BLG|SC atomic
interfaces pixel-by-pixel (which lattice color is bonded continuously across
each interface):

- `graphenesystem1para1.png` → both interfaces connect through the **same**
  (magenta) layer → **Geometry 1→1** → used as panel (a).
- `graphenesystem1para2.png` → the FM lead connects to the magenta layer,
  the SC lead connects to the **cyan** layer → **Geometry 1→2** → used as
  panel (b).

If this pairing is wrong for your convention, swap the two input filenames
in `build_figure.py` (see "Replacing a render" below) — everything else
(labels, dimension lines, layer legend) is generated programmatically and
will stay correct.

## Transparency

The Blender renders are true RGBA PNGs with a transparent background (not a
black one). The white journal page shows through directly wherever the
render's alpha channel is 0, and the translucent FM/BLG/SC region volumes
render as actual soft-edged glass rather than opaque tinted blocks. Panel
labels `(a)`/`(b)` and the geometry subtitles are set in dark ink
(`#1a1a1a`) rather than white, since they now sit on the transparent/white
corner of each panel instead of an opaque black one. The thin wireframe
visible at the edges of each translucent volume is part of the source
render (a backdrop/bounding-box wireframe) and is intentionally left as-is.

An earlier version of this package showed a black rectangle behind each
render. That was traced to the uploaded PNGs having been transcoded to
baseline JPEG in transit (JPEG has no alpha channel at all, so the
transparent regions were flattened to black before the files ever reached
this pipeline) — confirmed by inspecting the raw file header bytes
(`ff d8 ff e0...`, a JPEG/JFIF marker, instead of the PNG signature
`89 50 4e 47...`). Once genuine RGBA PNGs were supplied (via a zip archive,
which passes through without being re-encoded as an image), the fix was
just to stop forcing an RGB conversion anywhere in the pipeline and let
Matplotlib's `imshow`/SVG/PDF path carry the alpha channel through
untouched — verified end-to-end with a synthetic RGBA round-trip test
before being applied to the real renders.

## Files in this package

| File | Description |
|---|---|
| `figure_bilayer_junction.pdf` | Vector PDF, ready for journal submission. Fonts embedded (TrueType, `pdf.fonttype=42`). |
| `figure_bilayer_junction.svg` | Vector SVG, fully editable (Illustrator / Inkscape). Text is kept as real `<text>` elements, not outlined paths. |
| `figure_preview.png` | High-resolution flattened raster preview (450 dpi at 180 mm width). |
| `figure_preview_web.png` | Small raster preview for quick viewing / sharing. |
| `build_figure.py` | The editable source. Re-run this script (`python3 build_figure.py`) to regenerate all three outputs above from scratch. |
| `geom_1to1.png`, `geom_1to2.png` | The two Blender renders, pre-cropped to an identical bounding box and downsampled to 3200 px width, **saved as RGBA** with the original transparency intact. These are what `build_figure.py` actually loads. |

## Figure specifications

- **Overall width:** 180 mm (two-column journal width), height ≈ 109.5 mm.
- **Layout:** panels stacked vertically (not side-by-side), since each
  render is strongly horizontal — this keeps the atomic lattice legible at
  print size.
- **Fonts:** DejaVu Sans for all plain-text labels (a clean, license-free
  sans-serif in the spirit of Helvetica/Arial/Source Sans — swap
  `plt.rcParams["font.family"]` in `build_figure.py` if your production
  workflow has Helvetica/Nimbus Sans available). Mathematical symbols
  ($\vec h$, $\Delta$, $\Lambda$, $N$) are set with Matplotlib's `cm`
  mathtext font set, which follows Computer Modern / LaTeX math
  conventions.
- **Background:** pure white, no panel border boxes other than a thin
  (0.6 pt) neutral-gray frame directly around each Blender render.

## Annotation conventions

- **Panel labels** `(a)`, `(b)` — bold white, upper-left corner of each
  render, with the geometry name (`Geometry 1 → 1` / `Geometry 1 → 2`) set
  immediately beside it in the same corner.
- **Region labels** `FM`, `BLG`, `SC` — bold, centered above each region,
  connected to the render by a short thin leader line. Placement is driven
  by three constants at the top of the script (`FM_CENTER`, `BLG_CENTER`,
  `SC_CENTER`), given as a fraction of the cropped image width.
- **Physics labels** — $\vec h$ (FM exchange field) and $\Delta$ (SC pairing
  potential) sit directly above their region label. Neither implies a
  numerical value, direction, or phase — none was supplied, per the
  original brief.
- **`(AB-stacked)`** — small italic note under the `BLG` label.
- **$N$ dimension indicator** — a double-headed arrow spanning the
  interface-to-interface extent of the coupled bilayer region, i.e. the
  number of longitudinal unit cells used elsewhere in the manuscript for
  conductance-vs-$N$ plots. No length scale or unit conversion is implied.
- **Transport direction** — a small `x →` arrow under panel (b) only (shared
  convention for both panels, kept to a single instance to avoid clutter).
- **Layer legend** — a single shared legend at the very bottom of the
  figure (cyan = Layer 1 / $\Lambda=1$, magenta = Layer 2 / $\Lambda=2$),
  since direct per-atom labeling would obscure the lattice. This legend
  applies to both panels; the layer *colors* are identical in (a) and (b) —
  only which lead each layer connects to differs.
- Interlayer coupling ($t_\perp$) is **not** annotated — per the "if it
  crowds the figure, omit it" instruction, it was dropped as the lowest
  item on the stated annotation-priority list.

No numerical values, length scales, exchange-field direction, or SC phase
were invented; none were supplied in the brief.

## Replacing a render

1. Put the new Blender PNG somewhere accessible and crop/downsample it the
   same way the originals were processed:
   ```python
   from PIL import Image
   im = Image.open("new_render.png").convert("RGB")
   crop = im.crop((140, 0, 7900, im.size[1]))   # same box used for the originals
   crop.resize((2600, int(2600 * crop.size[1] / crop.size[0])), Image.LANCZOS).save("geom_1to1.png")
   ```
   (Use whatever crop box actually bounds your new render's device — the
   values above match the specific camera framing of the two renders
   supplied for this figure.)
2. Overwrite `geom_1to1.png` or `geom_1to2.png` in this folder.
3. If the new render's device is *not* at the same longitudinal position
   as before, update `FM_CENTER`, `BLG_CENTER`, `SC_CENTER`, `BLG_X0`,
   `BLG_X1` in `build_figure.py` (these are measured, as fractions of the
   cropped image width, from where each atom color begins/ends — see the
   pixel-scanning approach used to derive the original values, or simply
   eyeball them against the new render).
4. Re-run:
   ```bash
   python3 build_figure.py
   ```
   This regenerates the PDF, SVG, and PNG preview together.

## Exporting for journal production

- **PDF** (`figure_bilayer_junction.pdf`) is already production-ready:
  vector arrows/text/lines, embedded raster renders at ≈450 dpi effective
  resolution at final print size, embedded (non-outlined) TrueType fonts.
- **SVG** (`figure_bilayer_junction.svg`) is the best format for manual
  touch-ups (nudging a label, changing a leader line) in Inkscape or
  Illustrator, since all text remains live/editable. Re-export to PDF from
  there if your production system requires a PDF touched up outside
  Python.
- If a journal specifically requires embedded/outlined fonts instead of
  live text, open the SVG in Inkscape and use *Path → Object to Path* on
  the text objects before the final PDF export.
