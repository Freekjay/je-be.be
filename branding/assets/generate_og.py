"""Genereer de Open Graph / social-share afbeelding (1200x630) voor je-be.be.

Hergebruikt logo-variant D (papier + geel op dennengroen) en Space Grotesk
op de gewichten uit de styleguide. Draaien zonder eigen venv kan met:
uv run --with fonttools --with brotli --with pillow python branding/assets/generate_og.py
"""
import math
import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "space-grotesk-variable.woff2")
LOGO = os.path.join(HERE, "jebe-logo-d-invers-geel-2000w.png")
OUT = os.path.join(HERE, "og-image.png")

GREEN = (31, 107, 74)
PAPER = (245, 244, 239)
MUTED_ON_GREEN = (200, 214, 205)

W, H = 1200, 630
MARGIN = 88


def instantiated_font(weight, size):
    f = TTFont(FONT)
    f.flavor = None
    inst = instantiateVariableFont(f, {"wght": weight})
    path = os.path.join(HERE, f".sg-{weight}.ttf")
    inst.save(path)
    font = ImageFont.truetype(path, size)
    os.remove(path)
    return font


def dot_pattern_overlay():
    """Zelfde signatuur-stippenpatroon als de kaarten: vanuit rechtsboven,
    wegvloeiend naar de leeszone (hier linksonder, waar de tekst staat)."""
    ss = 4  # supersample voor gladde, anti-aliased stippen
    overlay = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    spacing = 28 * ss
    r = 2.4 * ss
    for gx in range(0, W * ss + spacing, spacing):
        for gy in range(0, H * ss + spacing, spacing):
            dx = (gx - W * ss) / (W * ss)
            dy = gy / (H * ss)
            dist = math.sqrt(dx * dx + dy * dy)
            alpha = max(0.0, 1 - dist * 1.15)
            if alpha <= 0.02:
                continue
            odraw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(*PAPER, int(80 * alpha)))
    return overlay.resize((W, H), Image.LANCZOS)


def build():
    img = Image.new("RGB", (W, H), GREEN).convert("RGBA")
    img = Image.alpha_composite(img, dot_pattern_overlay()).convert("RGB")
    draw = ImageDraw.Draw(img)

    logo = Image.open(LOGO).convert("RGBA")
    logo_w = 300
    logo_h = int(logo.height * logo_w / logo.width)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo, (MARGIN, MARGIN), logo)

    tagline_font = instantiated_font(700, 54)
    foot_font = instantiated_font(500, 24)

    y = MARGIN + logo_h + 56
    for line in ["Data- en AI-oplossingen", "van Limburgse makelij"]:
        draw.text((MARGIN, y), line, font=tagline_font, fill=PAPER)
        y += 64

    draw.text(
        (MARGIN, H - MARGIN - 24),
        "JEBE Consultancy  ·  Hasselt, Limburg  ·  je-be.be",
        font=foot_font,
        fill=MUTED_ON_GREEN,
    )

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    build()
