"""Genereer JEBE logo- en favicon-SVG's met geoutlinede Space Grotesk-paden."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.transform import Transform

FONT = os.path.join(os.path.dirname(__file__), "space-grotesk-variable.woff2")
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

font = TTFont(FONT)
upem = font["head"].unitsPerEm
glyph_set = font.getGlyphSet(location={"wght": 700})
cmap = font.getBestCmap()

TRACKING = 0.025  # em, = 1px op 40px


def glyph_name(ch):
    return cmap[ord(ch)]


def glyph_path(ch, transform):
    pen = SVGPathPen(glyph_set)
    tpen = TransformPen(pen, transform)
    glyph_set[glyph_name(ch)].draw(tpen)
    return pen.getCommands()


def glyph_metrics(ch):
    g = glyph_set[glyph_name(ch)]
    bp = BoundsPen(glyph_set)
    g.draw(bp)
    return g.width, bp.bounds  # advance, (xMin, yMin, xMax, yMax)


def layout(text, size):
    """Return list of (char, x_px) plus totale breedte en verticale bbox in px."""
    s = size / upem
    x = 0.0
    placements = []
    ymin, ymax = 0.0, 0.0
    for i, ch in enumerate(text):
        adv, bounds = glyph_metrics(ch)
        placements.append((ch, x))
        if bounds:
            ymin = min(ymin, bounds[1] * s)
            ymax = max(ymax, bounds[3] * s)
        x += adv * s
        if i < len(text) - 1:
            x += TRACKING * size
    # trailing bearing van laatste glyph niet afknippen: gebruik advance-breedte
    return placements, x, ymin, ymax


def wordmark_svg(letter_fill, dot_fill, bg=None, size=80, pad=None, radius=16):
    text = "JEBE."
    placements, width, ymin, ymax = layout(text, size)
    if pad is None:
        pad = round(size * 0.2) if bg else round(size * 0.1)
    W = width + 2 * pad
    H = (ymax - ymin) + 2 * pad
    baseline = pad + ymax
    s = size / upem
    parts = []
    if bg:
        parts.append(
            f'<rect width="{W:.1f}" height="{H:.1f}" rx="{radius}" fill="{bg}"/>'
        )
    for ch, x in placements:
        fill = dot_fill if ch == "." else letter_fill
        t = Transform(s, 0, 0, -s, pad + x, baseline)
        d = glyph_path(ch, t)
        parts.append(f'<path d="{d}" fill="{fill}"/>')
    body = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" '
        f'width="{W:.1f}" height="{H:.1f}" role="img" aria-label="JEBE.">\n  {body}\n</svg>\n'
    )


def favicon_svg(tile_fill, letter_fill, dot_fill, stroke=None):
    """64x64 tegel met gecentreerde 'J.'"""
    size = 40
    placements, width, ymin, ymax = layout("J.", size)
    W = H = 64.0
    x0 = (W - width) / 2
    baseline = (H + (ymax - ymin)) / 2 + ymin * 0  # centreer op bbox
    baseline = (H - (ymax - ymin)) / 2 + ymax
    s = size / upem
    parts = []
    stroke_attr = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    parts.append(f'<rect x="0.5" y="0.5" width="63" height="63" rx="14" fill="{tile_fill}"{stroke_attr}/>')
    for ch, x in placements:
        fill = dot_fill if ch == "." else letter_fill
        t = Transform(s, 0, 0, -s, x0 + x, baseline)
        d = glyph_path(ch, t)
        parts.append(f'<path d="{d}" fill="{fill}"/>')
    body = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" '
        f'width="64" height="64" role="img" aria-label="JEBE favicon">\n  {body}\n</svg>\n'
    )


def wordmark_anim_svg(letter_fill, muted_fill, dot_fill, size=80):
    """Geanimeerd headerlogo: 'JEROEN BEUNCKENS' klapt samen tot 'JEBE.'.

    Zelfde viewBox, maat en tracking als logo A; de extra letters steken
    rechts buiten de viewBox en zijn zichtbaar via overflow: visible.
    Zonder .play op de root toont de SVG exact het eindbeeld (= logo A).
    """
    frame_text = "JEBE."
    placements, width, ymin, ymax = layout(frame_text, size)
    pad = round(size * 0.1)
    W = width + 2 * pad
    H = (ymax - ymin) + 2 * pad
    baseline = pad + ymax
    s = size / upem

    full_text = "JEROEN BEUNCKENS"
    full_placements, _, _, _ = layout(full_text, size)
    # BE schuift van zijn plek in de volle naam naar zijn plek in "JEBE."
    slide = full_placements[7][1] - placements[2][1]  # index 7 = B
    drop_dx = 0.55 * size  # vallende letters schuiven ~0.55em naar links
    dot_x = placements[4][1] + slide  # punt op eindpositie relatief aan BE

    def path_at(ch, x, fill=None):
        t = Transform(s, 0, 0, -s, pad + x, baseline)
        fill_attr = f' fill="{fill}"' if fill else ""
        return f'<path d="{glyph_path(ch, t)}"{fill_attr}/>'

    style = f"""<style>
    .jebe-logo-anim {{ overflow: visible; }}
    .jebe-logo-anim .ja-drop {{ opacity: 0; }}
    .jebe-logo-anim .ja-be {{ transform: translateX(-{slide:.2f}px); }}
    .jebe-logo-anim .ja-dot {{ transform-box: fill-box; transform-origin: center; }}
    .jebe-logo-anim.play .ja-drop {{
      animation:
        jebe-mute 600ms linear 750ms both,
        jebe-drop 600ms cubic-bezier(0.65, 0, 0.35, 1) calc(1350ms + var(--ja-i) * 45ms) both;
    }}
    .jebe-logo-anim.play .ja-be {{
      animation: jebe-slide 1050ms cubic-bezier(0.65, 0, 0.35, 1) 1350ms both;
    }}
    .jebe-logo-anim.play .ja-dot {{
      animation: jebe-pop 450ms cubic-bezier(0.34, 1.56, 0.64, 1) 2400ms both;
    }}
    @keyframes jebe-mute {{
      from {{ fill: {letter_fill}; }}
      to {{ fill: {muted_fill}; }}
    }}
    @keyframes jebe-drop {{
      from {{ opacity: 1; transform: translateX(0); }}
      to {{ opacity: 0; transform: translateX(-{drop_dx:.2f}px); }}
    }}
    @keyframes jebe-slide {{
      from {{ transform: translateX(0); }}
      to {{ transform: translateX(-{slide:.2f}px); }}
    }}
    @keyframes jebe-pop {{
      from {{ transform: scale(0); }}
      to {{ transform: scale(1); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .jebe-logo-anim.play .ja-drop,
      .jebe-logo-anim.play .ja-be,
      .jebe-logo-anim.play .ja-dot {{ animation: none; }}
    }}
  </style>"""

    parts = [style]
    stagger = 0
    for i, (ch, x) in enumerate(full_placements):
        if i in (0, 1):  # JE: statisch
            parts.append(path_at(ch, x, letter_fill))
        elif ch == " ":  # spatie telt alleen mee in de layout
            continue
        elif i in (7, 8):  # BE: schuift samen met de punt
            if i == 7:
                parts.append(
                    f'<g class="ja-be" fill="{letter_fill}">\n  '
                    + path_at("B", x)
                    + "\n  "
                    + path_at("E", full_placements[8][1])
                    + f'\n  <g class="ja-dot" fill="{dot_fill}">{path_at(".", dot_x)}</g>\n  </g>'
                )
        else:  # ROEN + UNCKENS: vervagen en vallen weg, links naar rechts
            parts.append(
                f'<g class="ja-drop" fill="{letter_fill}" style="--ja-i:{stagger}">{path_at(ch, x)}</g>'
            )
            stagger += 1
    body = "\n  ".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" class="jebe-logo-anim" '
        f'viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.1f}" height="{H:.1f}" '
        f'role="img" aria-label="JEBE.">\n  {body}\n</svg>\n'
    )


INK = "#20261F"
GREEN = "#1F6B4A"
YELLOW = "#E9B53E"
PAPER = "#F5F4EF"
LINE = "#E2E0D6"
INK_MUTED = "rgba(32, 38, 31, 0.32)"

variants = {
    "jebe-logo-a-hoofdvariant.svg": wordmark_svg(INK, GREEN),
    "jebe-logo-b-groen-geel.svg": wordmark_svg(GREEN, YELLOW),
    "jebe-logo-c-inkt-geel.svg": wordmark_svg(INK, YELLOW),
    "jebe-logo-d-invers-geel.svg": wordmark_svg(PAPER, YELLOW, bg=GREEN),
    "jebe-logo-e-invers-mono.svg": wordmark_svg(PAPER, PAPER, bg=GREEN),
    "jebe-logo-f-op-geel.svg": wordmark_svg(INK, GREEN, bg=YELLOW),
    "favicon.svg": favicon_svg(GREEN, PAPER, YELLOW),
    "favicon-light.svg": favicon_svg(PAPER, INK, GREEN, stroke=LINE),
    "jebe-logo-anim.svg": wordmark_anim_svg(INK, INK_MUTED, GREEN),
}

for name, svg in variants.items():
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print("wrote", name)


# Inline kopie van het geanimeerde logo in index.html, tussen markercommentaren.
SITE_INDEX = os.path.normpath(os.path.join(OUT, "..", "..", "index.html"))
ANIM_START = "<!-- jebe-logo-anim:start -->"
ANIM_END = "<!-- jebe-logo-anim:end -->"

with open(SITE_INDEX) as f:
    html = f.read()
start = html.find(ANIM_START)
end = html.find(ANIM_END)
if start == -1 or end == -1:
    raise SystemExit(f"markers {ANIM_START} / {ANIM_END} niet gevonden in {SITE_INDEX}")
inline_svg = variants["jebe-logo-anim.svg"].strip()
html = html[: start + len(ANIM_START)] + "\n        " + inline_svg + "\n        " + html[end:]
with open(SITE_INDEX, "w") as f:
    f.write(html)
print("updated", SITE_INDEX)
