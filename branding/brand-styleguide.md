# JEBE Consultancy - Brand Style Guide

**Merk- en visuele-identiteitsreferentie voor alle uitingen: website, offertes, infographics, decks en social.**

Dit is de opvolger van de vorige (donkere) styleguide.
De stijl is licht en nuchter: warm papier als canvas, dennengroen als stem, honinggeel als blikvanger.
Ontworpen tijdens werf 2 van het [uitrolplan](../plans/2026-07-07-uitrolplan.md), op basis van de positionering in het [design-document](../specs/2026-07-06-jebe-kmo-positionering-design.md).

Typeface: **Space Grotesk** (Google Fonts) · Site: **je-be.be** · Tagline: **"Data- en AI-oplossingen van Limburgse makelij"**

---

## 01 - Kleur

Negen rollen dragen de hele identiteit.
Dennengroen is de stem van het merk, honinggeel de blikvanger, en het detailgroen een spaarzame knipoog naar het oude merkgroen.

### Kernpalet

| Rol | Hex | Gebruik |
|------|-----|---------|
| **Achtergrond** | `#F5F4EF` | Pagina-canvas. Warm gebroken wit ("papier"), geen klinisch wit. |
| **Oppervlak** | `#ECEBE2` | Kaarten, panelen, sectiebanden, voetbalk. Eén tint dieper dan het canvas. |
| **Lijnen** | `#E2E0D6` | Hairlines, borders, dividers. Altijd 1px. |
| **Accent · dennengroen** | `#1F6B4A` | Knoppen, links, eyebrow-labels, logo-punt, kaarttitels, cijfers. De stem van het merk. |
| **Detailgroen** | `#3DAC7B` | Spaarzaam: kleine details, datapunten in grafieken, hover-verloop. |
| **Accent · honinggeel** | `#E9B53E` | De blikvanger: markeringen en badges. Maximaal één aandachtstrekker per scherm. |
| **Tekst** | `#20261F` | Koppen en kerntekst. Groengetint near-black, geen puur zwart. |
| **Tekst gedempt** | `#565D54` | Lopende tekst, bijschriften, ondersteunende copy. |
| **Tekst op accent** | `#F5F4EF` | Tekst in knoppen en vlakken op dennengroen (= achtergrondkleur). |

### Groene tinten

Afgeleiden van het dennengroen voor vullingen en subtiele vlakken.
Gebruik deze in plaats van nieuwe kleuren.

| Token | Waarde | Typisch gebruik |
|-------|--------|-----------------|
| Groen 7% | `rgba(31, 107, 74, 0.07)` | Getinte kaartachtergrond (als vlak: `#EAEDE7`) |
| Groen 10% | `rgba(31, 107, 74, 0.10)` | Tag-achtergronden, zachte vullingen |
| Groen 22% | `rgba(31, 107, 74, 0.22)` | Tag-borders |
| Groen 24% | `rgba(31, 107, 74, 0.24)` | Stippenpatroon op kaarten |

### Geel accent

Honinggeel `#E9B53E` trekt de aandacht en bestaat in precies twee vormen:

1. **De markeerstift**: gele arcering achter één zin of zinsdeel.
   CSS: `background: linear-gradient(180deg, transparent 56%, rgba(233, 181, 62, 0.55) 56%)`.
2. **De badge**: geel blokje met inkttekst (`#20261F`), uppercase, radius 6px.

Regels: maximaal één gele aandachtstrekker per scherm, en kies per scherm één van de twee vormen.
Nooit voor lopende tekst, titels of knoppen.

---

## 02 - Typografie

**Space Grotesk**, één typeface voor alles, in vier gewichten: **400, 500, 600, 700**.
Geometrisch en licht technisch: leest als modern vakmanschap zonder koud te worden.

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

### Typeschaal

| Stijl | Grootte | Gewicht | Opmerkingen |
|-------|---------|---------|-------------|
| **H1 / Hero** | 40-48px | 700 | Line-height 1.1, letter-spacing -0.01em |
| **H2 / Sectie** | 28-32px | 700 | Letter-spacing -0.01em |
| **H3 / Subkop** | 20-24px | 600 | |
| **Eyebrow / Label** | 11-12px | 600 | UPPERCASE, letter-spacing 3px, dennengroen |
| **Body** | 15-16px | 400 | Line-height 1.6-1.7, tekst gedempt |
| **Caption** | 11-12px | 500 | UPPERCASE, letter-spacing 1.5px |

Koppen krijgen een subtiele negatieve letter-spacing (-0.01em), consistent over H1 en H2; verder geen variatie.

**Eyebrow-behandeling** (het signatuurlabel): uppercase, 11-12px, gewicht 600, `letter-spacing: 3px`, in dennengroen `#1F6B4A`.
Elke sectie opent ermee.

---

## 03 - Componenten

### Knoppen

- **Primair**: gevuld dennengroen `#1F6B4A`, tekst in achtergrondkleur `#F5F4EF`. Radius `8px`, padding `12px 26px`, gewicht 600.
- **Secundair**: transparant, dennengroene tekst, 1px dennengroene border. Zelfde radius en padding.

### De stippenkaart (het signatuurcomponent)

Kaart met een subtiel stippenpatroon dat vanuit de rechterbovenhoek aanwezig is en wegvloeit waar de tekst staat (de "leeszone").
Radius `12px`, padding `20px 22px`.
De titel is **altijd dennengroen** `#1F6B4A`, 600 gewicht; de bodytekst is gedempt `#565D54`.

De achtergrondkleur hangt af van de ondergrond:

| Context | Kaartachtergrond |
|---------|------------------|
| Op papier-sectie (`#F5F4EF`) | Groentint `#EAEDE7` of oppervlak `#ECEBE2` |
| Op oppervlakte-band (`#ECEBE2`) | Papier `#F5F4EF` (de kaart licht op in plaats van weg te zakken) |

Het stippenpatroon en de leeszone:

```css
.card {
  position: relative;
  z-index: 0;
  overflow: hidden;
  border-radius: 12px;
}
.card::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  background-image: radial-gradient(rgba(31, 107, 74, 0.24) 1.2px, transparent 1.2px);
  background-size: 16px 16px;
  mask-image: radial-gradient(130% 140% at 100% 0%, black 0%, rgba(0, 0, 0, 0.4) 34%, transparent 62%);
  -webkit-mask-image: radial-gradient(130% 140% at 100% 0%, black 0%, rgba(0, 0, 0, 0.4) 34%, transparent 62%);
}
```

### Tags

Groen 10% achtergrond, groen 22% border, dennengroene tekst, radius `14px`, 11px, gewicht 600.

### Badge (geel)

Honinggeel `#E9B53E` gevuld, inkttekst `#20261F`, uppercase, 10px, letter-spacing 1.5px, radius `6px`, padding `4px 10px`.
Dit is een blikvanger: zie de gele regels onder 01.

### Statistieken

- Cijfer: 26-36px, 700, **dennengroen** `#1F6B4A`.
- Label: 11px uppercase, letter-spacing 1.5px, gedempt.

### Invoervelden

Wit `#FFFFFF`, 1px border in lijnkleur `#E2E0D6`, radius `8px`, padding `11px 14px`.
Placeholder in `#9AA096`.

### Sectieopbouw

Secties wisselen af tussen papier (`#F5F4EF`) en oppervlakte-banden (`#ECEBE2`), gescheiden door 1px hairlines.
Elke sectie opent met een eyebrow-label, dan de H2, dan een korte gedempte intro.

### Radii

| Element | Radius |
|---------|--------|
| Kaarten / panelen | `12px` |
| Knoppen / invoervelden | `8px` |
| Badges | `6px` |
| Tags | `14px` |

---

## 04 - Look & feel

### ✅ Doen

- Papier als basis: grote vlakken blijven `#F5F4EF` of `#ECEBE2`.
- Groen als stem, niet als behang: dennengroen op maximaal ±10% van een oppervlak.
- Hairlines en witruimte structureren de pagina, geen schaduwen of gradients.
- Eyebrow-labels openen elke sectie.
- Cijfers krijgen het accent: stats en datapunten in dennengroen, 700 gewicht.
- Geel is de blikvanger: maximaal één gele aandachtstrekker (markering of badge) per scherm.
- Kaarttitels altijd in dennengroen, op elke achtergrond.

### ❌ Niet doen

- Geen donkere achtergronden meer; het merk leeft op licht.
- Geen puur wit (`#FFF`) en geen puur zwart (`#000`) als vlak.
- Geen glows, neon (`#41FFB0`) of gradients uit de oude stijl.
- Geen geel voor lopende tekst, titels of knoppen; alleen markeringen en badges.
- Geen derde accentkleur naast groen en geel.
- Geen andere typefaces of decoratieve fonts.
- Stippenpatroon nooit onder tekst: de leeszone is verplicht.

---

## 05 - Logo

### Het woordmerk

Het logo is het woordmerk **"JEBE."**: Space Grotesk, gewicht 700, letter-spacing licht positief (0.025em), met de punt als accentdrager.
Geen beeldmerk, geen extra vormen.

**Gebruik altijd de bestanden uit [assets/](assets/README.md)**: daar staan alle varianten als SVG (letters omgezet naar paden, dus font-onafhankelijk) en als PNG.
Zet het logo nooit zelf in tekst; dat geeft afwijkingen zodra het font ontbreekt of anders rendert.

### Kleurvarianten

| Variant | Letters | Punt | Ondergrond | Gebruik |
|---------|---------|------|------------|---------|
| **A · Hoofdvariant** | Inkt `#20261F` | Dennengroen `#1F6B4A` | Papier | Website-navigatie, offertes, documenten. De standaard. |
| B | Dennengroen `#1F6B4A` | Honinggeel `#E9B53E` | Papier | Groot formaat: hero, drukwerk. Niet klein gebruiken. |
| C | Inkt `#20261F` | Honinggeel `#E9B53E` | Papier | Als het geel de blikvanger van het scherm mag zijn. |
| D | Papier `#F5F4EF` | Honinggeel `#E9B53E` | Dennengroen | Banners, presentatie-covers, voetbalk. |
| E | Papier `#F5F4EF` | Papier `#F5F4EF` | Dennengroen | Monochrome fallback: stempels, watermerken. |
| F | Inkt `#20261F` | Dennengroen `#1F6B4A` | Honinggeel | Schreeuwvariant: social posts, stickers, beurs. Spaarzaam. |

### Favicon & avatar

De favicon is de verkorte vorm **"J."** op een dennengroene tegel met afgeronde hoeken (radius ±22% van de tegelbreedte):

- Tegel: dennengroen `#1F6B4A`.
- "J": papier `#F5F4EF`, Space Grotesk 700.
- Punt: honinggeel `#E9B53E` (geel = blikvanger; groen zou wegvallen op de groene tegel).

Dezelfde tegel dient ongewijzigd als LinkedIn-avatar en app-icoon.
Op lichte dragers waar een tegel niet past: papieren tegel met inkt-"J" en dennengroene punt, met een hairline-rand `#E2E0D6`.

Bestanden: `assets/favicon.svg` (bron) plus PNG's op 16, 32, 180 en 512 pixels; zie [assets/README.md](assets/README.md) voor het html-snippet.

---

## Snelle referentie (design tokens)

```css
:root {
  --bg: #F5F4EF;
  --surface: #ECEBE2;
  --line: #E2E0D6;
  --accent: #1F6B4A;
  --accent-detail: #3DAC7B;
  --accent-attention: #E9B53E;
  --text: #20261F;
  --text-muted: #565D54;
  --text-on-accent: #F5F4EF;
  --font: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

  --green-07: rgba(31, 107, 74, 0.07);
  --green-10: rgba(31, 107, 74, 0.10);
  --green-22: rgba(31, 107, 74, 0.22);
  --green-24: rgba(31, 107, 74, 0.24);
  --card-tint: #EAEDE7;

  --radius-card: 12px;
  --radius-button: 8px;
  --radius-badge: 6px;
  --radius-tag: 14px;
}
```

---

*JEBE Consultancy · Jeroen Beunckens · Hasselt · je-be.be*
*Data- en AI-oplossingen van Limburgse makelij.*
