# Design Spec: je-be.be/jeroen — Interactive Portfolio Page

## Overview

An interactive, data-driven portfolio page for Jeroen Beunckens at `je-be.be/jeroen`. The page uses a hybrid scroll + dashboard layout with full cross-filtering between charts, bilingual support (Dutch/English), and a modern dark theme. It serves both potential clients and recruiters.

## Tech Stack

- **HTML5 / CSS3 / JavaScript** — no build tools, static file deployment (GitHub Pages)
- **Alpine.js** (via CDN) — reactive state management, filter logic, language switching
- **Chart.js** (via CDN) — interactive charts (radar, bars, donut, area)
- **CSS Intersection Observer** — scroll-triggered animations
- **Single JSON data source** — generated from `info/cv/client_classification.csv`, powers all charts, content, and bilingual text

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| bg-primary | `#222831` | Page background |
| bg-surface | `#393E46` | Cards, widgets, stats bar |
| accent-primary | `#3DAC7B` | Primary green, borders, labels |
| accent-highlight | `#41FFB0` | Neon green, glows, chart highlights, active states |
| text-secondary | `#E8E8E8` | Secondary text, descriptions |
| text-primary | `#FBFBFB` | Primary text, headings |

Font: **Space Grotesk** (Google Fonts) — consistent with main je-be.be site.

## Language Support

- **Default language:** Dutch
- **URL parameter:** `?lang=en` opens page in English (shareable link)
- **Toggle:** Small fixed NL/EN toggle in the top-right corner, always visible
- **Implementation:** Alpine.js reactive `lang` state. All text content stored in a translations object with `nl` and `en` keys. Toggle swaps the `lang` property; all bound text updates reactively.

## Navigation

- **No top navbar** — site-wide navigation will be added separately later
- **Vertical scroll progress bar** on the right side of the page:
  - Thin vertical line with dot markers for each section
  - Progress line fills as the user scrolls down
  - Active dot highlights when its section is in view
  - Clickable dots to jump to sections
  - Labels appear on hover (e.g., "Skills", "Timeline")
  - On mobile: transforms into a thin horizontal progress bar at the top

## Data Architecture

### Central Data Source (`data/jeroen.json`)

Single JSON file containing all portfolio data:

```json
{
  "profile": {
    "name": "Jeroen Beunckens",
    "title": { "nl": "Data Expert", "en": "Data Expert" },
    "subtitles": {
      "nl": ["Engineering", "Architecture", "Analytics", "Consulting"],
      "en": ["Engineering", "Architecture", "Analytics", "Consulting"]
    },
    "intro": { "nl": "...", "en": "..." },
    "email": "jeroen.beunckens@gmail.com",
    "linkedin": "https://www.linkedin.com/in/jeroenbeunckens/"
  },
  "stats": { ... },
  "skills": [ { "name": "Power BI", "level": "Expert", "value": 95, "category": "BI" }, ... ],
  "clients": [ { "name": "Atlas Copco", "industry": "Manufacturing", "technologies": [...], "startYear": 2019, "logo": "...", "featured": true }, ... ],
  "projects": [ ... ],
  "certifications": [ ... ],
  "education": [ ... ]
}
```

### Filter State Manager (Alpine.js `x-data`)

Central reactive state object:

```javascript
{
  lang: 'nl',                    // active language
  filters: {
    yearRange: [2018, 2026],     // time range slider
    technology: null,            // selected technology filter
    industry: null,              // selected industry filter
    client: null                 // selected client filter
  },
  // Computed: filtered data based on active filters
}
```

All charts and sections bind to this state. When any filter changes, all components re-render with filtered data.

### Cross-Filter Interactions

| User action | Effect on other components |
|---|---|
| Adjust year range slider | All charts, timeline, projects filter to that period |
| Click industry slice in donut | Radar, bars, timeline, projects filter to that industry's clients |
| Click technology in radar/bars | Timeline, projects, client chips filter to that technology |
| Click client chip/logo | Dashboard charts highlight that client's tech/industry, timeline highlights their projects |
| Click project card | Highlights related tech in dashboard, client in portfolio, position on timeline |
| Click certification | Highlights related technologies in dashboard |
| Clear/reset | All filters reset, everything shows |

Active filters should be visually indicated (e.g., a small filter badge or highlighted state). A "clear filters" button appears when any filter is active.

## Page Sections

### 1. Hero (Full Viewport)

- **Background:** Subtle CSS grid pattern with radial green glows (`#3DAC7B` and `#41FFB0` at low opacity). No heavy 3D libraries.
- **Layout:** Photo on the left (circular, with green gradient border/glow), text on the right.
- **Photo:** Placeholder initially (`JB` initials in green gradient circle). Will be replaced with actual photo later. Image path: `jeroen/img/photo.jpg`.
- **Content:**
  - Name: "Jeroen Beunckens" (large, bold)
  - Static title: "Data Expert"
  - Cycling subtitle: "Engineering" → "Architecture" → "Analytics" → "Consulting" (smooth fade or typing animation, CSS-based preferred)
  - Intro paragraph (personality through tone):
    - NL: "Hands-on data consultant die complexe problemen omzet in eenvoudige, impactvolle dataoplossingen. 8 jaar ervaring bij zowel KMO's als multinationals, altijd met een praktische aanpak die resultaat oplevert."
    - EN: Equivalent English version
- **Scroll hint:** Animated down arrow at the bottom of viewport.

### 2. Stats Bar

Horizontal strip directly below the hero. Dark surface background (`#393E46`) with top and bottom border accents.

- Numbers animate in with a count-up effect when scrolled into view
- Exact figures to be determined after CSV review
- Planned stats:
  - Years of experience
  - Long-term projects count
  - Total projects (short & long-term)
  - Certifications count
  - Industries count

All labels bilingual.

### 3. Dashboard Zone (Skills & Charts)

Background: Subtle gradient from `#393E46` to transparent. Section header with uppercase label.

**Global time range filter** at the top of the zone — a styled range slider for year selection (2018-2026).

**Widget grid (2x2 on desktop, stacked on mobile):**

#### 3a. Skills Radar Chart (Chart.js radar)
- 6 axes: Power BI, Databricks, SQL, Qlik, Azure, Python (or adjusted based on what makes sense)
- Filled polygon with `#3DAC7B` fill, `#41FFB0` border
- Interactive: hover for tooltips, click axis to filter by that technology
- Responds to year range filter (shows only skills relevant to the selected period)

#### 3b. Proficiency Bars (Chart.js horizontal bar or CSS)
- All technologies with self-assessed levels:
  - Expert: Power BI, SQL
  - Very good: Databricks, Qlik, Fabric, Data Modeling, DAX, Synapse DWH, Paginated Reports/SSRS
  - Good: dbt, Python, Data Factory, Azure DevOps, SQL Server, Informatica iDMC
  - Moderate: Power Platform, CI/CD GitHub
- Animated fill on scroll entry
- Click a bar to filter other charts by that technology
- Gradient fill: `#3DAC7B` → `#41FFB0`

#### 3c. Industry Breakdown (Chart.js doughnut)
- Segments colored with variations of the green palette
- Based on client count per industry from the finalized CSV
- Click a segment to filter all other charts by that industry
- Center text shows total client count (or filtered count when filter active)

#### 3d. Technology Timeline (Chart.js line/area)
- X-axis: years (2018-2026)
- Stacked area showing technology usage over time
- Categories: Qlik, Power BI / Fabric, Databricks / dbt, Other
- Shows the evolution from Qlik-heavy early career to modern data stack
- Responds to all cross-filters

### 4. Career Timeline (Horizontal)

Full-width horizontal scrollable timeline with a connecting line.

- **Major projects:** Large dots with labels below (7 featured projects)
- **Minor projects:** Small dots on the same line (short-term clients from CSV)
- **Current projects:** Glowing pulse effect on the dot
- **Connecting line:** Gradient from `#3DAC7B` to `#41FFB0`
- **Hover:** Tooltip showing role, client, period, and technologies
- **Click:** Scrolls down to the detailed project card in Section 5
- **Cross-filter integration:** When a filter is active, matching items stay highlighted, others fade to low opacity
- **Career phases labeled:** "Credon" (2018-mid 2025), "Freelancer / JEBE" (June 2025+), "via Aivix" where applicable
- On mobile: touch-swipeable

### 5. Featured Projects (Expandable Cards)

Grid of project cards (2 columns desktop, 1 column mobile).

**7 featured projects (newest first):**

1. **Energy Monitoring System (EMS)** — Etex (2025-present)
   - Role: Data Engineer
   - Description: Combining IoT sensor data from production plants with manual quality samples and formula-driven metadata. Outputs a data model consumed by Power BI for near-real-time insights on production performance and energy consumption.
   - Tech: Databricks, Azure Data Factory, Azure Synapse, Azure DevOps, Power BI

2. **Databricks Platform Architect** — Atlas Copco PT (2024-2025)
   - Role: Data Architect
   - Description: Overseeing the Databricks environment for PT domain teams. Establishing guidelines, conducting training, and ensuring governance across the organization.
   - Tech: Azure Databricks, Azure DevOps

3. **Sustainable Data Transformation** — Atlas Copco PT (2024-2025)
   - Role: Data Engineer
   - Description: Converting and improving Python solutions to Databricks dbt for sustainability reporting. Standardizing source data and making it accessible across the entire PT business area.
   - Tech: Azure Databricks, dbt, Azure Functions (Python), Data Factory

4. **Fabric Lakehouse Integration** — Allimex Green Power (2024)
   - Role: Data Engineer / Analyst
   - Description: Building a BI platform using Microsoft Fabric Lakehouse. ETL logic in Fabric Notebooks (Python/PySpark), Power BI reports for Sales and Supply Chain, deployment pipelines, Data Quality reports.
   - Tech: Microsoft Fabric, Power BI, Azure DevOps

5. **SEVESO Compliance Data Platform** — Van Moer Logistics (2023-2024)
   - Role: Data Engineer / Analyst / Functional Analyst
   - Description: Designing a Data Vault Medallion architecture data platform. Data Quality framework, Power BI dashboards for hazardous goods stock monitoring (SEVESO compliance).
   - Tech: Informatica Cloud, Azure Databricks, Azure Synapse, GitHub Actions, Power BI

6. **Data Platform** — Baronie (2023)
   - Role: Data Engineer
   - Description: Building a data platform from scratch for Power BI reporting across finance, sales, and logistics. Kimball data model with DBT methodology, data from multiple ERP systems.
   - Tech: Data Factory, Data Lake Gen2, SQL Server, DevOps GIT & Pipelines

7. **Qlik-Power BI Transition** — Atlas Copco CT (2020-2023)
   - Role: Qlik & Power BI Lead
   - Description: Managing QlikView environment serving 2,000+ users. Redesigning reports, building monitoring reports for cost allocation and usage tracking. Migrating the entire reporting environment to Power BI as the new organizational standard.
   - Tech: QlikView, NPrinting, Power BI, Paginated Reports

**Card behavior:**
- Default: compact (name, client, period, tech tags)
- Click to expand: full description, role, impact
- Cross-filter: clicking a card highlights its tech/industry/timeline position
- Left border accent (`#3DAC7B`), hover changes to `#41FFB0` with lift effect

All descriptions bilingual (NL and EN in JSON).

### 6. Client Portfolio

Centered section with client logos and name chips.

- **Clients with logos:** Displayed as logo images (grayscale by default, color on hover). Logos to be sourced/provided later. Path: `jeroen/img/clients/`
- **Clients without logos:** Styled text chips with border
- **"+ X more" chip** in accent color showing remaining count
- **Cross-filter:** Clicking a client filters dashboard charts, timeline, and projects
- **Hover tooltip:** Industry and period
- **Notable clients to feature** (final list from CSV `show_on_page` column): Atlas Copco, Etex, Van Moer, AB InBev, Baronie, Allimex, Delvaux, Heraeus, Tosoh, Arvesta, ED&A, Astra Sweets (and others marked in CSV)

### 7. Credentials (Certifications + Education)

Card grid (4 columns desktop, 2 columns mobile).

**Certifications (8):**
1. Databricks Data Engineer Professional (2025)
2. Databricks Data Engineer Associate (2025)
3. Azure Solutions Architect Expert (2023)
4. Azure Administrator Associate (2023)
5. Azure Data Engineer Associate (2023)
6. Fabric Analytics Engineer Associate (2024)
7. Power BI Data Analyst Associate (2022)
8. Qlik Data Architect (2020)

**Education (2):**
1. Bachelor Computer Science — PXL Hasselt (2015-2018)
2. Leadership Transition Program — Vlerick Business School (2022)

Each card: vendor icon/logo, cert name, year. Cross-filter: clicking a cert highlights related technologies in the dashboard zone.

### 8. Contact

Centered CTA section at the bottom.

- Heading: "Klaar om samen te werken?" / "Ready to collaborate?"
- Subtext: Brief bilingual line
- Two buttons:
  - LinkedIn (primary green button) → https://www.linkedin.com/in/jeroenbeunckens/
  - Email (outline button) → mailto:jeroen.beunckens@gmail.com

## File Structure

```
jeroen/
├── index.html              # Main page
├── style.css               # All styles
├── app.js                  # Alpine.js app, filter logic, chart initialization
├── data/
│   └── jeroen.json         # All portfolio data (generated from CSV)
└── img/
    ├── photo.jpg           # Professional photo (placeholder initially)
    └── clients/            # Client logos
        ├── atlas-copco.svg
        ├── etex.svg
        └── ...
```

## Animations & Performance

- **Scroll-triggered animations:** CSS transitions triggered via Intersection Observer. Elements fade in and slide up as they enter the viewport. Staggered delays for grid items.
- **Count-up stats:** JavaScript counter animation on the stats bar, triggered once when scrolled into view.
- **Cycling subtitle:** CSS keyframe animation cycling through the subtitle options with a fade effect.
- **Chart animations:** Chart.js built-in animations on initial render (triggered by Intersection Observer).
- **Hover effects:** CSS transitions on cards (lift, border color change), chart tooltips via Chart.js.
- **Progress bar:** Updated via scroll event listener with `requestAnimationFrame`.
- **Performance:** No heavy 3D libraries. All animations CSS-based where possible. Chart.js is the only significant JS dependency besides Alpine.js.

## Responsive Design

| Breakpoint | Changes |
|---|---|
| Desktop (>1024px) | Full layout as designed. 2-column widget grid, horizontal timeline, 2-column project cards, 4-column cert grid. |
| Tablet (768-1024px) | Widget grid stacks to single column. Project cards single column. Cert grid 3 columns. Timeline remains horizontal. |
| Mobile (<768px) | Everything single column. Vertical progress bar becomes thin horizontal progress bar at top. Timeline is touch-swipeable. Dashboard cross-filtering adapts to tap interactions. Collapsible filter panel instead of inline controls. Cert grid 2 columns. |

## Career Context

For timeline and "about" sections:

- **2018 - mid 2025:** Data Consultant at Credon
- **June 2025 onwards:** Freelancer (JEBE Consultancy)
- **October 2025 onwards:** Current client Etex (through Aivix / Intellus Group)
- **Atlas Copco PT:** ended 2025 (not ongoing)

## Open Items (Pre-Implementation)

1. **Client classification CSV:** Jeroen to review and fill in `info/cv/client_classification.csv` (industry, technology, show_on_page for all clients)
2. **Exact stats figures:** To be calculated after CSV is finalized
3. **Professional photo:** Jeroen to provide, placeholder until then
4. **Client logos:** To be sourced/provided for featured clients
5. **Project descriptions in Dutch:** NL translations of all project descriptions
6. **Intro paragraph:** Final bilingual copy for the hero section
