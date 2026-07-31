# JEBE logo- en faviconbestanden

Gegenereerd vanuit Space Grotesk (gewicht 700), met alle letters omgezet naar paden.
De bestanden zien er dus overal identiek uit, ook zonder dat het font geïnstalleerd is.
Kleurcodes en gebruiksregels: zie [../brand-styleguide.md](../brand-styleguide.md), hoofdstuk 05.

## Logo (SVG = bron, PNG = 2000px breed)

| Bestand | Variant | Gebruik |
|---------|---------|---------|
| `jebe-logo-a-hoofdvariant.svg/.png` | A · inkt + groene punt | **Standaard.** Website-navigatie, offertes, documenten. |
| `jebe-logo-b-groen-geel.svg/.png` | B · groen + gele punt | Groot formaat: hero, drukwerk. |
| `jebe-logo-c-inkt-geel.svg/.png` | C · inkt + gele punt | Als geel de blikvanger van het scherm mag zijn. |
| `jebe-logo-d-invers-geel.svg/.png` | D · papier + geel op groen vlak | Banners, covers, voetbalk. |
| `jebe-logo-e-invers-mono.svg/.png` | E · monochroom papier op groen vlak | Stempels, watermerken. |
| `jebe-logo-f-op-geel.svg/.png` | F · inkt + groen op geel vlak | Social posts, stickers, beurs. Spaarzaam. |

Varianten A-C hebben een transparante achtergrond; D-F dragen hun eigen vlak (radius 16).

## Geanimeerd headerlogo

`jebe-logo-anim.svg` laat "JEROEN BEUNCKENS" samenklappen tot "JEBE." (zelfde viewBox en eindbeeld als variant A).
Zonder de klasse `play` op het root-element toont de SVG het statische logo.
Het generatiescript kopieert deze SVG ook inline naar `index.html`, tussen de markers `<!-- jebe-logo-anim:start -->` en `<!-- jebe-logo-anim:end -->`.
Ontwerp en choreografie: zie [../../docs/superpowers/specs/2026-07-11-jebe-logo-animation-design.md](../../docs/superpowers/specs/2026-07-11-jebe-logo-animation-design.md).

## Favicon & avatar

| Bestand | Gebruik |
|---------|---------|
| `favicon.svg` | Bron: groene tegel, papieren "J", gele punt. |
| `favicon-16.png`, `favicon-32.png` | Browser-favicon. |
| `favicon-180.png` | Apple touch icon. |
| `favicon-512.png` | LinkedIn-avatar, app-icoon, PWA. |
| `favicon-light.svg` + PNG's | Alternatief voor lichte dragers (papieren tegel, hairline-rand). |

## Website-snippet

```html
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/favicon-180.png">
```

## Social-share afbeelding

`og-image.png` (1200x630) is de Open Graph/Twitter-preview, gebruikt in `<meta property="og:image">` in `index.html`.
Hergebruikt logo-variant D en het stippenpatroon van de kaartcomponent op dennengroen.
Genereren met `generate_og.py` (zie hieronder).

## Opnieuw genereren

De logo- en faviconbestanden zijn gemaakt met fontTools (outlines uit het variabele font op wght=700, tracking 0.025em) en cairosvg (PNG-rasterisatie).
Draaien zonder eigen venv kan met: `uv run --with fonttools --with brotli python generate.py` (brotli is nodig om het woff2-font te lezen).

`og-image.png` wordt apart opgebouwd met Pillow: `uv run --with fonttools --with brotli --with pillow python generate_og.py`.

Bij een wijziging: pas de kleuren of maten aan in het generatiescript en genereer alles opnieuw, nooit handmatig bijwerken in een editor zonder de bron mee te veranderen.
