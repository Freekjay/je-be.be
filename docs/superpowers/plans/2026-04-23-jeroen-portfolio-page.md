# Interactive Portfolio Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an interactive, data-driven portfolio page at `je-be.be/jeroen` with cross-filtered charts, bilingual support, and a modern dark theme.

**Architecture:** A single-page static site using Alpine.js for reactive state management and Chart.js for interactive visualizations. All portfolio data lives in a single JSON file that powers charts, content, and bilingual text. A central Alpine.js store manages filter state; when any chart element is clicked, all other charts re-render with filtered data.

**Tech Stack:** HTML5, CSS3, Alpine.js (CDN), Chart.js (CDN), Intersection Observer API

**Spec:** `docs/superpowers/specs/2026-04-23-jeroen-portfolio-page-design.md`

---

## Task 1: Foundation — File Structure & HTML Boilerplate

**Files:**
- Create: `jeroen/index.html`
- Create: `jeroen/style.css`
- Create: `jeroen/app.js`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p jeroen/data jeroen/img/clients
```

- [ ] **Step 2: Create HTML boilerplate**

Create `jeroen/index.html`:

```html
<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jeroen Beunckens — Data Expert</title>
  <meta name="description" content="Interactive portfolio of Jeroen Beunckens — Data Engineer, Architect & Consultant with 8 years of experience.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
</head>
<body x-data="portfolio()" x-init="init()">

  <!-- Sections will be added in subsequent tasks -->

  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 3: Create CSS foundation with variables and reset**

Create `jeroen/style.css`:

```css
/* ── Reset & Base ── */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --bg-primary: #222831;
  --bg-surface: #393E46;
  --accent: #3DAC7B;
  --accent-bright: #41FFB0;
  --text-secondary: #E8E8E8;
  --text-primary: #FBFBFB;
  --font: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

  --accent-10: rgba(61, 172, 123, 0.1);
  --accent-15: rgba(61, 172, 123, 0.15);
  --accent-20: rgba(61, 172, 123, 0.2);
  --accent-30: rgba(61, 172, 123, 0.3);
  --bright-30: rgba(65, 255, 176, 0.3);
  --bright-50: rgba(65, 255, 176, 0.5);
}

html {
  scroll-behavior: smooth;
  font-size: 16px;
}

body {
  font-family: var(--font);
  color: var(--text-primary);
  line-height: 1.6;
  background: var(--bg-primary);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

img {
  max-width: 100%;
  display: block;
}

a {
  color: inherit;
  text-decoration: none;
}

/* ── Section base ── */
.section {
  padding: 80px 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--accent);
  margin-bottom: 8px;
  font-weight: 600;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 32px;
}
```

- [ ] **Step 4: Create Alpine.js app shell**

Create `jeroen/app.js`:

```javascript
function portfolio() {
  return {
    lang: 'nl',
    data: null,
    loading: true,
    filters: {
      yearRange: [2018, 2026],
      technology: null,
      industry: null,
      client: null,
    },
    charts: {},

    async init() {
      const params = new URLSearchParams(window.location.search);
      if (params.get('lang') === 'en') this.lang = 'en';

      const resp = await fetch('data/jeroen.json');
      this.data = await resp.json();
      this.loading = false;
    },

    t(obj) {
      if (!obj) return '';
      if (typeof obj === 'string') return obj;
      return obj[this.lang] || obj['nl'] || '';
    },

    toggleLang() {
      this.lang = this.lang === 'nl' ? 'en' : 'nl';
      const url = new URL(window.location);
      if (this.lang === 'en') {
        url.searchParams.set('lang', 'en');
      } else {
        url.searchParams.delete('lang');
      }
      window.history.replaceState({}, '', url);
    },

    get hasActiveFilter() {
      return this.filters.technology !== null
        || this.filters.industry !== null
        || this.filters.client !== null
        || this.filters.yearRange[0] !== 2018
        || this.filters.yearRange[1] !== 2026;
    },

    clearFilters() {
      this.filters.technology = null;
      this.filters.industry = null;
      this.filters.client = null;
      this.filters.yearRange = [2018, 2026];
      this.updateAllCharts();
    },

    setFilter(type, value) {
      if (this.filters[type] === value) {
        this.filters[type] = null;
      } else {
        this.filters[type] = value;
      }
      this.updateAllCharts();
    },

    matchesFilter(item) {
      const f = this.filters;
      if (f.technology && item.technologies && !item.technologies.includes(f.technology)) return false;
      if (f.industry && item.industry && item.industry !== f.industry) return false;
      if (f.client && item.client && item.client !== f.client) return false;
      const year = item.startYear || item.year;
      if (year && (year < f.yearRange[0] || year > f.yearRange[1])) return false;
      return true;
    },

    updateAllCharts() {
      // Will be implemented as charts are added
    },
  };
}
```

- [ ] **Step 5: Verify foundation loads**

Run: `cd jeroen && python3 -m http.server 8080`

Open `http://localhost:8080` in browser. Expected: blank dark page (#222831 background), no console errors, Alpine.js initialized (check with browser dev tools — `document.querySelector('[x-data]').__x` should exist).

- [ ] **Step 6: Commit**

```bash
git add jeroen/index.html jeroen/style.css jeroen/app.js
git commit -m "feat(jeroen): foundation — HTML boilerplate, CSS variables, Alpine.js shell"
```

---

## Task 2: JSON Data Source

**Files:**
- Create: `jeroen/data/jeroen.json`

- [ ] **Step 1: Create the complete JSON data file**

Create `jeroen/data/jeroen.json`:

```json
{
  "profile": {
    "name": "Jeroen Beunckens",
    "title": { "nl": "Data Expert", "en": "Data Expert" },
    "subtitles": {
      "nl": ["Engineering", "Architecture", "Analytics", "Consulting"],
      "en": ["Engineering", "Architecture", "Analytics", "Consulting"]
    },
    "intro": {
      "nl": "Hands-on data consultant die complexe problemen omzet in eenvoudige, impactvolle dataoplossingen. 8 jaar ervaring bij zowel KMO's als multinationals, altijd met een praktische aanpak die resultaat oplevert.",
      "en": "Hands-on data consultant who turns complex problems into simple, impactful data solutions. 8 years of experience in both SMEs and multinational enterprises, always delivering with a practical approach that gets results."
    },
    "email": "jeroen.beunckens@gmail.com",
    "linkedin": "https://www.linkedin.com/in/jeroenbeunckens/"
  },
  "stats": [
    { "value": 8, "label": { "nl": "Jaar ervaring", "en": "Years of experience" } },
    { "value": 7, "label": { "nl": "Langetermijnprojecten", "en": "Long-term projects" } },
    { "value": 74, "label": { "nl": "Projecten (kort & lang)", "en": "Projects (short & long-term)" } },
    { "value": 8, "label": { "nl": "Certificaten", "en": "Certifications" } },
    { "value": 6, "label": { "nl": "Industrie\u00ebn", "en": "Industries" } }
  ],
  "skills": [
    { "name": "Power BI", "level": "Expert", "value": 95, "category": "BI Tools", "years": [2020,2021,2022,2023,2024,2025,2026] },
    { "name": "SQL", "level": "Expert", "value": 95, "category": "Other", "years": [2018,2019,2020,2021,2022,2023,2024,2025,2026] },
    { "name": "Databricks", "level": "Very good", "value": 85, "category": "Data Platform", "years": [2023,2024,2025,2026] },
    { "name": "Qlik", "level": "Very good", "value": 85, "category": "BI Tools", "years": [2018,2019,2020,2021,2022,2023] },
    { "name": "Fabric", "level": "Very good", "value": 85, "category": "Data Platform", "years": [2024,2025] },
    { "name": "Data Modeling", "level": "Very good", "value": 85, "category": "Other", "years": [2018,2019,2020,2021,2022,2023,2024,2025,2026] },
    { "name": "DAX", "level": "Very good", "value": 80, "category": "BI Tools", "years": [2020,2021,2022,2023,2024,2025,2026] },
    { "name": "Synapse DWH", "level": "Very good", "value": 80, "category": "Data Platform", "years": [2023,2024,2025,2026] },
    { "name": "Paginated Reports", "level": "Very good", "value": 80, "category": "BI Tools", "years": [2020,2021,2022,2023,2024] },
    { "name": "dbt", "level": "Good", "value": 70, "category": "Data Platform", "years": [2024,2025,2026] },
    { "name": "Python", "level": "Good", "value": 70, "category": "Other", "years": [2023,2024,2025,2026] },
    { "name": "Data Factory", "level": "Good", "value": 70, "category": "Data Platform", "years": [2023,2024,2025,2026] },
    { "name": "Azure DevOps", "level": "Good", "value": 70, "category": "DevOps", "years": [2023,2024,2025,2026] },
    { "name": "SQL Server", "level": "Good", "value": 70, "category": "Data Platform", "years": [2023,2024] },
    { "name": "Informatica iDMC", "level": "Good", "value": 65, "category": "Data Platform", "years": [2023,2024] },
    { "name": "Power Platform", "level": "Moderate", "value": 55, "category": "BI Tools", "years": [2022,2023,2024] },
    { "name": "CI/CD GitHub", "level": "Moderate", "value": 55, "category": "DevOps", "years": [2023,2024,2025] }
  ],
  "radarSkills": ["Power BI", "Databricks", "SQL", "Qlik", "Python", "Azure DevOps"],
  "projects": [
    {
      "id": "etex-ems",
      "name": "Energy Monitoring System (EMS)",
      "client": "Etex",
      "industry": "Construction",
      "role": { "nl": "Data Engineer", "en": "Data Engineer" },
      "period": "2025 — heden",
      "startYear": 2025,
      "endYear": 2026,
      "current": true,
      "via": "Aivix / Intellus Group",
      "phase": "freelance",
      "description": {
        "nl": "Combinatie van IoT-sensordata uit productieplants met handmatige kwaliteitsmetingen en metadata-formules. Near-real-time inzichten in energieverbruik en productieperformantie via Power BI.",
        "en": "Combining IoT sensor data from production plants with manual quality samples and formula-driven metadata. Near-real-time insights on production performance and energy consumption via Power BI."
      },
      "technologies": ["Databricks", "Azure Data Factory", "Azure Synapse", "Azure DevOps", "Power BI"]
    },
    {
      "id": "atlas-copco-platform",
      "name": "Databricks Platform Architect",
      "client": "Atlas Copco",
      "industry": "Manufacturing",
      "role": { "nl": "Data Architect", "en": "Data Architect" },
      "period": "2024 — 2025",
      "startYear": 2024,
      "endYear": 2025,
      "current": false,
      "via": "Aivix / Intellus Group",
      "phase": "credon",
      "description": {
        "nl": "Opzetten en beheren van de Databricks-omgeving voor PT-domeinteams. Richtlijnen opstellen, training geven en governance waarborgen voor de hele organisatie.",
        "en": "Overseeing the Databricks environment for PT domain teams. Establishing guidelines, conducting training, and ensuring governance across the organization."
      },
      "technologies": ["Azure Databricks", "Azure DevOps"]
    },
    {
      "id": "atlas-copco-sustainability",
      "name": { "nl": "Duurzame Data Transformatie", "en": "Sustainable Data Transformation" },
      "client": "Atlas Copco",
      "industry": "Manufacturing",
      "role": { "nl": "Data Engineer", "en": "Data Engineer" },
      "period": "2024 — 2025",
      "startYear": 2024,
      "endYear": 2025,
      "current": false,
      "via": "Aivix / Intellus Group",
      "phase": "credon",
      "description": {
        "nl": "Omzetten en verbeteren van Python-oplossingen naar Databricks dbt voor duurzaamheidsrapportage. Brondata standaardiseren en toegankelijk maken voor het hele PT-businessgebied.",
        "en": "Converting and improving Python solutions to Databricks dbt for sustainability reporting. Standardizing source data and making it accessible across the entire PT business area."
      },
      "technologies": ["Azure Databricks", "dbt", "Azure Functions", "Data Factory"]
    },
    {
      "id": "allimex-fabric",
      "name": "Fabric Lakehouse Integration",
      "client": "Allimex Green Power",
      "industry": "Manufacturing",
      "role": { "nl": "Data Engineer / Analyst", "en": "Data Engineer / Analyst" },
      "period": "2024",
      "startYear": 2024,
      "endYear": 2024,
      "current": false,
      "via": "Credon",
      "phase": "credon",
      "description": {
        "nl": "Opbouwen van een BI-platform met Microsoft Fabric Lakehouse. ETL-logica in Fabric Notebooks (Python/PySpark), Power BI-rapporten voor Sales en Supply Chain, deployment pipelines en Data Quality-rapporten.",
        "en": "Building a BI platform using Microsoft Fabric Lakehouse. ETL logic in Fabric Notebooks (Python/PySpark), Power BI reports for Sales and Supply Chain, deployment pipelines, Data Quality reports."
      },
      "technologies": ["Microsoft Fabric", "Power BI", "Azure DevOps"]
    },
    {
      "id": "vanmoer-seveso",
      "name": "SEVESO Compliance Data Platform",
      "client": "Van Moer Logistics",
      "industry": "Logistics",
      "role": { "nl": "Data Engineer / Analyst / Functional Analyst", "en": "Data Engineer / Analyst / Functional Analyst" },
      "period": "2023 — 2024",
      "startYear": 2023,
      "endYear": 2024,
      "current": false,
      "via": "Credon",
      "phase": "credon",
      "description": {
        "nl": "Ontwerp van een Data Vault Medallion-architectuur dataplatform. Data Quality-framework en Power BI-dashboards voor monitoring van gevaarlijke goederen (SEVESO-compliance).",
        "en": "Designing a Data Vault Medallion architecture data platform. Data Quality framework, Power BI dashboards for hazardous goods stock monitoring (SEVESO compliance)."
      },
      "technologies": ["Informatica Cloud", "Azure Databricks", "Azure Synapse", "GitHub Actions", "Power BI"]
    },
    {
      "id": "baronie-platform",
      "name": "Data Platform",
      "client": "Baronie",
      "industry": "Food",
      "role": { "nl": "Data Engineer", "en": "Data Engineer" },
      "period": "2023",
      "startYear": 2023,
      "endYear": 2023,
      "current": false,
      "via": "Credon",
      "phase": "credon",
      "description": {
        "nl": "Vanaf nul opbouwen van een dataplatform voor Power BI-rapportage over finance, sales en logistiek. Kimball-datamodel met DBT-methodologie, data uit meerdere ERP-systemen.",
        "en": "Building a data platform from scratch for Power BI reporting across finance, sales, and logistics. Kimball data model with DBT methodology, data from multiple ERP systems."
      },
      "technologies": ["Data Factory", "Data Lake Gen2", "SQL Server", "Azure DevOps"]
    },
    {
      "id": "atlas-copco-qlik",
      "name": "Qlik-Power BI Transition",
      "client": "Atlas Copco",
      "industry": "Manufacturing",
      "role": { "nl": "Qlik & Power BI Lead", "en": "Qlik & Power BI Lead" },
      "period": "2020 — 2023",
      "startYear": 2020,
      "endYear": 2023,
      "current": false,
      "via": "Credon",
      "phase": "credon",
      "description": {
        "nl": "Beheer van QlikView-omgeving voor 2.000+ gebruikers. Rapporten herontworpen, monitoring-rapporten gebouwd voor kostenverdeling en gebruikstracking. Volledige migratie naar Power BI als nieuwe organisatiestandaard.",
        "en": "Managing QlikView environment serving 2,000+ users. Redesigning reports, building monitoring reports for cost allocation and usage tracking. Migrating the entire reporting environment to Power BI as the new organizational standard."
      },
      "technologies": ["QlikView", "NPrinting", "Power BI", "Paginated Reports"]
    }
  ],
  "clients": [
    { "name": "Atlas Copco", "industry": "Manufacturing", "technologies": ["Qlik", "Power BI", "Databricks", "dbt", "Azure DevOps"], "startYear": 2019, "featured": true, "logo": true },
    { "name": "Etex", "industry": "Construction", "technologies": ["Databricks", "Azure Data Factory", "Azure Synapse", "Power BI"], "startYear": 2025, "featured": true, "logo": true },
    { "name": "Van Moer Logistics", "industry": "Logistics", "technologies": ["Informatica Cloud", "Azure Databricks", "Azure Synapse", "Power BI"], "startYear": 2023, "featured": true, "logo": true },
    { "name": "AB InBev", "industry": "Food & Beverage", "technologies": ["Qlik"], "startYear": 2022, "featured": true, "logo": true },
    { "name": "Baronie", "industry": "Food", "technologies": ["Data Factory", "SQL Server", "Power BI"], "startYear": 2023, "featured": true, "logo": true },
    { "name": "Allimex Green Power", "industry": "Manufacturing", "technologies": ["Microsoft Fabric", "Power BI"], "startYear": 2024, "featured": true, "logo": true },
    { "name": "Delvaux", "industry": "Luxury Goods", "technologies": ["Qlik"], "startYear": 2019, "featured": true, "logo": false },
    { "name": "Heraeus Electro-Nite", "industry": "Manufacturing", "technologies": ["Qlik"], "startYear": 2019, "featured": true, "logo": false },
    { "name": "Tosoh", "industry": "Chemical", "technologies": ["Qlik"], "startYear": 2018, "featured": true, "logo": false },
    { "name": "Arvesta", "industry": "Agriculture", "technologies": ["Qlik"], "startYear": 2018, "featured": true, "logo": false },
    { "name": "ED&A", "industry": "Electronics", "technologies": ["Qlik"], "startYear": 2019, "featured": true, "logo": false },
    { "name": "Astra Sweets", "industry": "Food", "technologies": ["Qlik"], "startYear": 2019, "featured": true, "logo": false },
    { "name": "Interalu", "industry": "Construction", "technologies": ["Qlik"], "startYear": 2018, "featured": false, "logo": false },
    { "name": "Baldewijns", "industry": "Unknown", "technologies": ["Qlik"], "startYear": 2019, "featured": false, "logo": false },
    { "name": "Deusjevoo", "industry": "Events", "technologies": ["Qlik"], "startYear": 2023, "featured": false, "logo": false },
    { "name": "Het Gielsbos", "industry": "Healthcare", "technologies": ["Qlik"], "startYear": 2021, "featured": false, "logo": false },
    { "name": "Hogeschool PXL", "industry": "Education", "technologies": ["Qlik"], "startYear": 2020, "featured": false, "logo": false },
    { "name": "Chillafish", "industry": "Consumer Goods", "technologies": ["Qlik"], "startYear": 2018, "featured": false, "logo": false }
  ],
  "careerPhases": [
    { "label": "Credon", "startYear": 2018, "endYear": 2025, "description": { "nl": "Data Consultant bij Credon", "en": "Data Consultant at Credon" } },
    { "label": "Freelancer / JEBE", "startYear": 2025, "endYear": 2026, "description": { "nl": "Freelance via JEBE Consultancy", "en": "Freelance via JEBE Consultancy" } }
  ],
  "certifications": [
    { "name": "Databricks Data Engineer Professional", "vendor": "Databricks", "year": 2025, "technologies": ["Databricks"] },
    { "name": "Databricks Data Engineer Associate", "vendor": "Databricks", "year": 2025, "technologies": ["Databricks"] },
    { "name": "Azure Solutions Architect Expert", "vendor": "Microsoft", "year": 2023, "technologies": ["Azure DevOps", "Azure Synapse"] },
    { "name": "Azure Administrator Associate", "vendor": "Microsoft", "year": 2023, "technologies": ["Azure DevOps"] },
    { "name": "Azure Data Engineer Associate", "vendor": "Microsoft", "year": 2023, "technologies": ["Data Factory", "Azure Synapse", "Azure Databricks"] },
    { "name": "Fabric Analytics Engineer Associate", "vendor": "Microsoft", "year": 2024, "technologies": ["Microsoft Fabric", "Power BI"] },
    { "name": "Power BI Data Analyst Associate", "vendor": "Microsoft", "year": 2022, "technologies": ["Power BI", "DAX"] },
    { "name": "Qlik Data Architect", "vendor": "Qlik", "year": 2020, "technologies": ["Qlik"] }
  ],
  "education": [
    { "name": { "nl": "Bachelor Toegepaste Informatica", "en": "Bachelor Computer Science" }, "institution": "PXL Hasselt", "period": "2015 — 2018" },
    { "name": "Leadership Transition Program", "institution": "Vlerick Business School", "period": "2022" }
  ],
  "techTimeline": {
    "labels": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    "datasets": [
      { "label": "Qlik", "data": [90, 85, 60, 55, 50, 20, 0, 0, 0], "color": "#3DAC7B" },
      { "label": "Power BI / Fabric", "data": [0, 0, 30, 35, 40, 40, 50, 30, 20], "color": "#41FFB0" },
      { "label": "Databricks / dbt", "data": [0, 0, 0, 0, 0, 30, 40, 55, 65], "color": "#2a8a62" },
      { "label": "Other", "data": [10, 15, 10, 10, 10, 10, 10, 15, 15], "color": "#4a5568" }
    ]
  },
  "ui": {
    "statsBar": { "nl": "Kerncijfers", "en": "Key figures" },
    "skills": { "nl": "Expertise", "en": "Expertise" },
    "skillsTitle": { "nl": "Skills & Technologies", "en": "Skills & Technologies" },
    "timeline": { "nl": "Carri\u00e8re", "en": "Career" },
    "timelineTitle": { "nl": "Professioneel Traject", "en": "Professional Journey" },
    "projects": { "nl": "Projecten", "en": "Projects" },
    "projectsTitle": { "nl": "Uitgelichte Projecten", "en": "Featured Projects" },
    "clientsHeader": { "nl": "Klanten", "en": "Clients" },
    "clientsTitle": { "nl": "Klantenportfolio", "en": "Client Portfolio" },
    "credentials": { "nl": "Referenties", "en": "Credentials" },
    "credentialsTitle": { "nl": "Certificaten & Opleiding", "en": "Certifications & Education" },
    "contact": { "nl": "Contact", "en": "Contact" },
    "contactTitle": { "nl": "Klaar om samen te werken?", "en": "Ready to collaborate?" },
    "contactSub": { "nl": "Op zoek naar een data consultant? Neem gerust contact op.", "en": "Looking for a data consultant? Feel free to reach out." },
    "filterClear": { "nl": "Filters wissen", "en": "Clear filters" },
    "yearRange": { "nl": "Periode", "en": "Period" },
    "moreClients": { "nl": "meer", "en": "more" },
    "present": { "nl": "heden", "en": "present" },
    "via": { "nl": "via", "en": "via" },
    "clickExpand": { "nl": "Klik voor details", "en": "Click for details" },
    "radarTitle": { "nl": "Skills Radar", "en": "Skills Radar" },
    "barsTitle": { "nl": "Vaardigheidsniveaus", "en": "Proficiency Levels" },
    "industryTitle": { "nl": "Industrie Verdeling", "en": "Industry Breakdown" },
    "techTimelineTitle": { "nl": "Technologie Evolutie", "en": "Technology Evolution" }
  }
}
```

Note: The `clients` array is a subset. The full list will be populated from the finalized CSV. The `stats.value` fields are placeholders — update after CSV review.

- [ ] **Step 2: Verify JSON loads**

Open browser dev tools console at `http://localhost:8080`:

```javascript
fetch('data/jeroen.json').then(r => r.json()).then(d => console.log(d.profile.name))
```

Expected: logs "Jeroen Beunckens".

- [ ] **Step 3: Commit**

```bash
git add jeroen/data/jeroen.json
git commit -m "feat(jeroen): add portfolio JSON data source"
```

---

## Task 3: Hero Section

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`

- [ ] **Step 1: Add hero HTML to index.html**

In `jeroen/index.html`, replace `<!-- Sections will be added in subsequent tasks -->` with:

```html
  <!-- Language Toggle -->
  <div class="lang-toggle" @click="toggleLang()">
    <span :class="{ active: lang === 'nl' }">NL</span>
    <span :class="{ active: lang === 'en' }">EN</span>
  </div>

  <!-- Hero -->
  <section class="hero" id="hero">
    <div class="hero-bg">
      <div class="hero-grid"></div>
    </div>
    <div class="hero-content">
      <div class="hero-photo">
        <span>JB</span>
      </div>
      <div class="hero-text">
        <h1>Jeroen <span class="accent">Beunckens</span></h1>
        <div class="hero-title" x-text="data ? t(data.profile.title) : ''"></div>
        <div class="hero-subtitle-wrapper">
          <template x-if="data">
            <div class="hero-subtitle-cycle">
              <template x-for="(sub, i) in t(data.profile.subtitles)" :key="i">
                <span class="hero-subtitle-item" :style="`animation-delay: ${i * 2.5}s`" x-text="sub"></span>
              </template>
            </div>
          </template>
        </div>
        <p class="hero-intro" x-text="data ? t(data.profile.intro) : ''"></p>
      </div>
    </div>
    <div class="scroll-hint">
      <span>&darr;</span>
    </div>
  </section>

  <!-- Remaining sections will be added in subsequent tasks -->
```

- [ ] **Step 2: Add hero CSS**

Append to `jeroen/style.css`:

```css
/* ── Language Toggle ── */
.lang-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
  display: flex;
  background: var(--bg-surface);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--accent-20);
}

.lang-toggle span {
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.3s;
}

.lang-toggle span.active {
  background: var(--accent);
  color: var(--bg-primary);
  border-radius: 20px;
}

/* ── Hero ── */
.hero {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 30% 50%, rgba(61,172,123,0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 50%, rgba(65,255,176,0.05) 0%, transparent 50%);
}

.hero-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(var(--accent-10) 1px, transparent 1px),
    linear-gradient(90deg, var(--accent-10) 1px, transparent 1px);
  background-size: 60px 60px;
  opacity: 0.5;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 60px;
  max-width: 1000px;
  padding: 0 40px;
}

.hero-photo {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-bright));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 0 40px var(--accent-30);
}

.hero-photo span {
  font-size: 64px;
  font-weight: 700;
  color: var(--bg-primary);
}

.hero-photo img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.hero-text h1 {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 4px;
}

.hero-text .accent {
  color: var(--accent);
}

.hero-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.hero-subtitle-wrapper {
  height: 32px;
  overflow: hidden;
  margin-bottom: 20px;
}

.hero-subtitle-cycle {
  position: relative;
  height: 32px;
}

.hero-subtitle-item {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 20px;
  color: var(--accent-bright);
  font-weight: 500;
  opacity: 0;
  animation: subtitleCycle 10s infinite;
}

@keyframes subtitleCycle {
  0%, 5% { opacity: 0; transform: translateY(10px); }
  8%, 20% { opacity: 1; transform: translateY(0); }
  23%, 25% { opacity: 0; transform: translateY(-10px); }
  100% { opacity: 0; }
}

.hero-intro {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 500px;
  opacity: 0.85;
}

.scroll-hint {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 24px;
  color: var(--accent);
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}
```

- [ ] **Step 3: Verify hero renders**

Refresh `http://localhost:8080`. Expected: full-viewport hero with green grid background, "JB" photo placeholder, "Jeroen Beunckens" heading, "Data Expert" title, cycling subtitles, intro text in Dutch, bouncing scroll arrow, NL/EN toggle in top-right. Click the toggle — text should switch to English.

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css
git commit -m "feat(jeroen): add hero section with cycling subtitle and language toggle"
```

---

## Task 4: Stats Bar

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`
- Modify: `jeroen/app.js`

- [ ] **Step 1: Add stats bar HTML**

In `jeroen/index.html`, after the hero `</section>` and before `<!-- Remaining sections -->`, add:

```html
  <!-- Stats Bar -->
  <div class="stats-bar" id="stats">
    <template x-if="data">
      <template x-for="stat in data.stats" :key="t(stat.label)">
        <div class="stat-item">
          <div class="stat-number" x-data="{ shown: false, current: 0 }"
               x-intersect:enter.once="shown = true; let target = stat.value; let step = Math.ceil(target / 40); let interval = setInterval(() => { current += step; if (current >= target) { current = target; clearInterval(interval); } }, 30)"
               x-text="shown ? current : 0">
          </div>
          <div class="stat-label" x-text="t(stat.label)"></div>
        </div>
      </template>
    </template>
  </div>
```

- [ ] **Step 2: Add stats bar CSS**

Append to `jeroen/style.css`:

```css
/* ── Stats Bar ── */
.stats-bar {
  display: flex;
  justify-content: center;
  gap: 48px;
  padding: 40px 20px;
  background: var(--bg-surface);
  border-top: 1px solid var(--accent-20);
  border-bottom: 1px solid var(--accent-20);
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--accent-bright);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 4px;
}
```

- [ ] **Step 3: Verify stats bar**

Refresh browser, scroll past hero. Expected: stats bar appears with numbers counting up from 0 to their target values. Numbers should be green (#41FFB0). Toggle language — labels should switch.

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css
git commit -m "feat(jeroen): add stats bar with count-up animation"
```

---

## Task 5: Scroll Progress Bar

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`
- Modify: `jeroen/app.js`

- [ ] **Step 1: Add progress bar HTML**

In `jeroen/index.html`, directly after `<body x-data="portfolio()" x-init="init()">`, add:

```html
  <!-- Scroll Progress Bar -->
  <nav class="scroll-nav" x-data="scrollNav()" x-init="initScrollNav()" @scroll.window="onScroll()">
    <div class="scroll-nav-track">
      <div class="scroll-nav-fill" :style="`height: ${progress}%`"></div>
    </div>
    <template x-for="(section, i) in sections" :key="section.id">
      <a class="scroll-nav-dot"
         :class="{ active: activeSection === section.id }"
         :style="`top: ${section.position}%`"
         :href="'#' + section.id"
         @click.prevent="scrollTo(section.id)"
         @mouseenter="hoveredSection = section.id"
         @mouseleave="hoveredSection = null">
        <span class="scroll-nav-label" x-show="hoveredSection === section.id" x-text="t(section.label)"></span>
      </a>
    </template>
  </nav>
```

- [ ] **Step 2: Add scrollNav function to app.js**

Append to `jeroen/app.js`:

```javascript
function scrollNav() {
  return {
    progress: 0,
    activeSection: 'hero',
    hoveredSection: null,
    sections: [
      { id: 'hero', label: { nl: 'Start', en: 'Start' }, position: 5 },
      { id: 'stats', label: { nl: 'Cijfers', en: 'Stats' }, position: 15 },
      { id: 'dashboard', label: { nl: 'Skills', en: 'Skills' }, position: 30 },
      { id: 'timeline', label: { nl: 'Tijdlijn', en: 'Timeline' }, position: 48 },
      { id: 'projects', label: { nl: 'Projecten', en: 'Projects' }, position: 62 },
      { id: 'clients', label: { nl: 'Klanten', en: 'Clients' }, position: 75 },
      { id: 'credentials', label: { nl: 'Certificaten', en: 'Certs' }, position: 86 },
      { id: 'contact', label: { nl: 'Contact', en: 'Contact' }, position: 95 },
    ],

    t(obj) {
      const lang = document.querySelector('[x-data]').__x.$data.lang || 'nl';
      return typeof obj === 'string' ? obj : (obj[lang] || obj['nl']);
    },

    initScrollNav() {
      this.onScroll();
    },

    onScroll() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      this.progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

      const sectionEls = this.sections.map(s => document.getElementById(s.id)).filter(Boolean);
      for (let i = sectionEls.length - 1; i >= 0; i--) {
        if (sectionEls[i].getBoundingClientRect().top <= window.innerHeight * 0.4) {
          this.activeSection = this.sections[i].id;
          break;
        }
      }
    },

    scrollTo(id) {
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    },
  };
}
```

- [ ] **Step 3: Add progress bar CSS**

Append to `jeroen/style.css`:

```css
/* ── Scroll Progress Nav ── */
.scroll-nav {
  position: fixed;
  right: 24px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 90;
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.scroll-nav-track {
  position: absolute;
  width: 2px;
  height: 100%;
  background: var(--accent-20);
  border-radius: 1px;
}

.scroll-nav-fill {
  width: 100%;
  background: linear-gradient(180deg, var(--accent), var(--accent-bright));
  border-radius: 1px;
  transition: height 0.1s linear;
}

.scroll-nav-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--bg-surface);
  border: 2px solid var(--accent-20);
  transform: translateX(-50%);
  left: 1px;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 1;
}

.scroll-nav-dot:hover,
.scroll-nav-dot.active {
  background: var(--accent);
  border-color: var(--accent-bright);
  box-shadow: 0 0 8px var(--bright-50);
}

.scroll-nav-label {
  position: absolute;
  right: 24px;
  top: 50%;
  transform: translateY(-50%);
  background: var(--bg-surface);
  color: var(--text-primary);
  padding: 4px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  border: 1px solid var(--accent-20);
  pointer-events: none;
}
```

- [ ] **Step 4: Verify progress bar**

Refresh browser. Expected: vertical dots on the right side of the page. As you scroll, the green fill line grows. Active section dot glows. Hover on a dot shows a label tooltip. Click a dot scrolls to that section (only "hero" and "stats" exist so far — others will scroll to approximate positions).

- [ ] **Step 5: Commit**

```bash
git add jeroen/index.html jeroen/style.css jeroen/app.js
git commit -m "feat(jeroen): add vertical scroll progress bar with section navigation"
```

---

## Task 6: Dashboard Zone — Layout, Year Range Filter, and Radar Chart

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`
- Modify: `jeroen/app.js`

- [ ] **Step 1: Add dashboard zone HTML**

In `jeroen/index.html`, after the stats bar `</div>` and before `<!-- Remaining sections -->`, add:

```html
  <!-- Dashboard Zone -->
  <div class="dashboard-zone" id="dashboard">
    <div class="section">
      <div class="section-header" x-text="data ? t(data.ui.skills) : ''"></div>
      <div class="section-title" x-text="data ? t(data.ui.skillsTitle) : ''"></div>

      <!-- Year Range Filter -->
      <div class="year-filter" x-show="data">
        <label class="year-filter-label" x-text="data ? t(data.ui.yearRange) : ''"></label>
        <div class="year-filter-controls">
          <span class="year-filter-value" x-text="filters.yearRange[0]"></span>
          <input type="range" min="2018" max="2026" x-model.number="filters.yearRange[0]"
                 @input="if(filters.yearRange[0] > filters.yearRange[1]) filters.yearRange[1] = filters.yearRange[0]; updateAllCharts()">
          <input type="range" min="2018" max="2026" x-model.number="filters.yearRange[1]"
                 @input="if(filters.yearRange[1] < filters.yearRange[0]) filters.yearRange[0] = filters.yearRange[1]; updateAllCharts()">
          <span class="year-filter-value" x-text="filters.yearRange[1]"></span>
        </div>
        <button class="filter-clear-btn" x-show="hasActiveFilter" @click="clearFilters()" x-text="data ? t(data.ui.filterClear) : ''"></button>
      </div>

      <!-- Active filter badges -->
      <div class="filter-badges" x-show="hasActiveFilter">
        <span class="filter-badge" x-show="filters.technology" @click="setFilter('technology', filters.technology)">
          <span x-text="filters.technology"></span> &times;
        </span>
        <span class="filter-badge" x-show="filters.industry" @click="setFilter('industry', filters.industry)">
          <span x-text="filters.industry"></span> &times;
        </span>
        <span class="filter-badge" x-show="filters.client" @click="setFilter('client', filters.client)">
          <span x-text="filters.client"></span> &times;
        </span>
      </div>

      <!-- Widget Grid -->
      <div class="dash-grid">
        <!-- Radar Chart -->
        <div class="dash-widget">
          <h3 x-text="data ? t(data.ui.radarTitle) : ''"></h3>
          <div class="chart-container">
            <canvas id="radarChart"></canvas>
          </div>
        </div>

        <!-- Proficiency Bars -->
        <div class="dash-widget dash-widget-large">
          <h3 x-text="data ? t(data.ui.barsTitle) : ''"></h3>
          <div id="proficiencyBars"></div>
        </div>

        <!-- Industry Donut -->
        <div class="dash-widget">
          <h3 x-text="data ? t(data.ui.industryTitle) : ''"></h3>
          <div class="chart-container">
            <canvas id="donutChart"></canvas>
          </div>
        </div>

        <!-- Tech Timeline -->
        <div class="dash-widget dash-widget-large">
          <h3 x-text="data ? t(data.ui.techTimelineTitle) : ''"></h3>
          <div class="chart-container chart-container-wide">
            <canvas id="techTimelineChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
```

- [ ] **Step 2: Add dashboard zone CSS**

Append to `jeroen/style.css`:

```css
/* ── Dashboard Zone ── */
.dashboard-zone {
  padding: 60px 0;
  background: linear-gradient(180deg, rgba(57,62,70,0.3) 0%, rgba(34,40,49,0) 100%);
}

.dash-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.dash-widget {
  background: var(--bg-surface);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--accent-10);
  transition: border-color 0.3s;
}

.dash-widget:hover {
  border-color: var(--accent-30);
}

.dash-widget-large {
  grid-column: span 1;
}

.dash-widget h3 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--accent);
}

.chart-container {
  position: relative;
  width: 100%;
  max-height: 280px;
}

.chart-container-wide {
  max-height: 200px;
}

.chart-container canvas {
  width: 100% !important;
  height: 100% !important;
}

/* ── Year Filter ── */
.year-filter {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 12px 20px;
  background: var(--bg-surface);
  border-radius: 8px;
  border: 1px solid var(--accent-10);
}

.year-filter-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--accent);
  font-weight: 600;
  flex-shrink: 0;
}

.year-filter-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.year-filter-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-bright);
  min-width: 36px;
  text-align: center;
}

.year-filter input[type="range"] {
  flex: 1;
  -webkit-appearance: none;
  height: 4px;
  background: var(--accent-20);
  border-radius: 2px;
  outline: none;
}

.year-filter input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid var(--accent-bright);
}

.filter-clear-btn {
  background: transparent;
  border: 1px solid var(--accent-30);
  color: var(--accent);
  padding: 6px 16px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  font-family: var(--font);
  transition: all 0.2s;
  flex-shrink: 0;
}

.filter-clear-btn:hover {
  background: var(--accent);
  color: var(--bg-primary);
}

.filter-badges {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: var(--accent-15);
  border: 1px solid var(--accent-30);
  border-radius: 16px;
  font-size: 12px;
  color: var(--accent-bright);
  cursor: pointer;
  font-weight: 500;
}

.filter-badge:hover {
  background: var(--accent-30);
}
```

- [ ] **Step 3: Add chart initialization to app.js**

In `jeroen/app.js`, replace the `updateAllCharts()` method and add chart methods inside the `portfolio()` function, before the closing `};`:

```javascript
    initCharts() {
      if (!this.data) return;
      this.registerCenterTextPlugin();
      this.initRadarChart();
      this.initProficiencyBars();
      this.initDonutChart();
      this.initTechTimelineChart();
    },

    updateAllCharts() {
      this.updateRadarChart();
      this.updateProficiencyBars();
      this.updateDonutChart();
      this.updateTechTimelineChart();
    },

    getFilteredSkills() {
      if (!this.data) return [];
      return this.data.skills.filter(skill => {
        if (this.filters.technology && skill.name !== this.filters.technology) return false;
        const inRange = skill.years.some(y => y >= this.filters.yearRange[0] && y <= this.filters.yearRange[1]);
        if (!inRange) return false;
        return true;
      });
    },

    getFilteredClients() {
      if (!this.data) return [];
      return this.data.clients.filter(c => this.matchesFilter(c));
    },

    getFilteredProjects() {
      if (!this.data) return [];
      return this.data.projects.filter(p => {
        if (this.filters.technology && !p.technologies.includes(this.filters.technology)) return false;
        if (this.filters.industry && p.industry !== this.filters.industry) return false;
        if (this.filters.client && p.client !== this.filters.client) return false;
        if (p.startYear > this.filters.yearRange[1] || p.endYear < this.filters.yearRange[0]) return false;
        return true;
      });
    },

    // ── Chart.js Center Text Plugin (for donut) ──
    registerCenterTextPlugin() {
      const plugin = {
        id: 'centerText',
        afterDraw(chart) {
          if (chart.config.type !== 'doughnut') return;
          const { ctx, width, height } = chart;
          const total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
          ctx.save();
          ctx.font = 'bold 24px Space Grotesk';
          ctx.fillStyle = '#41FFB0';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(total, width / 2, height / 2 - 8);
          ctx.font = '11px Space Grotesk';
          ctx.fillStyle = '#E8E8E8';
          ctx.fillText('clients', width / 2, height / 2 + 12);
          ctx.restore();
        }
      };
      Chart.register(plugin);
    },

    // ── Radar Chart ──
    initRadarChart() {
      const ctx = document.getElementById('radarChart');
      if (!ctx) return;
      const radarSkills = this.data.radarSkills;
      const values = radarSkills.map(name => {
        const skill = this.data.skills.find(s => s.name === name);
        return skill ? skill.value : 0;
      });

      this.charts.radar = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: radarSkills,
          datasets: [{
            data: values,
            backgroundColor: 'rgba(61, 172, 123, 0.2)',
            borderColor: '#41FFB0',
            borderWidth: 2,
            pointBackgroundColor: '#3DAC7B',
            pointBorderColor: '#41FFB0',
            pointRadius: 4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: { legend: { display: false } },
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: { display: false, stepSize: 25 },
              grid: { color: 'rgba(61, 172, 123, 0.1)' },
              angleLines: { color: 'rgba(61, 172, 123, 0.1)' },
              pointLabels: {
                color: '#E8E8E8',
                font: { family: 'Space Grotesk', size: 11, weight: 500 },
              },
            }
          },
          onClick: (e, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              this.setFilter('technology', this.data.radarSkills[idx]);
            }
          },
        }
      });
    },

    updateRadarChart() {
      if (!this.charts.radar) return;
      const radarSkills = this.data.radarSkills;
      const filteredSkills = this.getFilteredSkills();
      const values = radarSkills.map(name => {
        const skill = filteredSkills.find(s => s.name === name);
        return skill ? skill.value : 0;
      });
      this.charts.radar.data.datasets[0].data = values;
      this.charts.radar.update();
    },

    // ── Proficiency Bars ──
    initProficiencyBars() {
      this.renderProficiencyBars();
    },

    renderProficiencyBars() {
      const container = document.getElementById('proficiencyBars');
      if (!container) return;
      const skills = this.getFilteredSkills().sort((a, b) => b.value - a.value);
      container.innerHTML = skills.map(skill => `
        <div class="bar-row ${this.filters.technology === skill.name ? 'bar-active' : ''}"
             onclick="document.querySelector('[x-data]').__x.$data.setFilter('technology', '${skill.name}')">
          <span class="bar-label">${skill.name}</span>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${skill.value}%"></div>
          </div>
          <span class="bar-value">${skill.level}</span>
        </div>
      `).join('');
    },

    updateProficiencyBars() {
      this.renderProficiencyBars();
    },

    // ── Donut Chart ──
    initDonutChart() {
      const ctx = document.getElementById('donutChart');
      if (!ctx) return;
      const industries = this.getIndustryCounts();
      const colors = ['#3DAC7B', '#41FFB0', '#2a8a62', '#1a6b4a', '#4a5568', '#2d6a4f', '#52b788'];

      this.charts.donut = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: industries.map(i => i.name),
          datasets: [{
            data: industries.map(i => i.count),
            backgroundColor: colors.slice(0, industries.length),
            borderColor: '#393E46',
            borderWidth: 2,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          cutout: '55%',
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#E8E8E8',
                font: { family: 'Space Grotesk', size: 11 },
                padding: 8,
                usePointStyle: true,
                pointStyleWidth: 8,
              },
            },
            // Center text plugin — shows total/filtered client count
            centerText: {
              display: true,
            },
          },
          onClick: (e, elements) => {
            if (elements.length > 0) {
              const idx = elements[0].index;
              this.setFilter('industry', industries[idx].name);
            }
          },
        }
      });
    },

    getIndustryCounts() {
      const counts = {};
      const clients = this.filters.technology || this.filters.client
        ? this.getFilteredClients()
        : this.data.clients;
      clients.forEach(c => {
        if (c.industry && c.industry !== 'Unknown') {
          counts[c.industry] = (counts[c.industry] || 0) + 1;
        }
      });
      return Object.entries(counts)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
    },

    updateDonutChart() {
      if (!this.charts.donut) return;
      const industries = this.getIndustryCounts();
      const colors = ['#3DAC7B', '#41FFB0', '#2a8a62', '#1a6b4a', '#4a5568', '#2d6a4f', '#52b788'];
      this.charts.donut.data.labels = industries.map(i => i.name);
      this.charts.donut.data.datasets[0].data = industries.map(i => i.count);
      this.charts.donut.data.datasets[0].backgroundColor = colors.slice(0, industries.length);
      this.charts.donut.update();
    },

    // ── Tech Timeline Chart ──
    initTechTimelineChart() {
      const ctx = document.getElementById('techTimelineChart');
      if (!ctx || !this.data.techTimeline) return;
      const tl = this.data.techTimeline;

      this.charts.techTimeline = new Chart(ctx, {
        type: 'line',
        data: {
          labels: tl.labels,
          datasets: tl.datasets.map(ds => ({
            label: ds.label,
            data: ds.data,
            borderColor: ds.color,
            backgroundColor: ds.color + '33',
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointBackgroundColor: ds.color,
          }))
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: {
                color: '#E8E8E8',
                font: { family: 'Space Grotesk', size: 11 },
                usePointStyle: true,
              },
            },
          },
          scales: {
            x: {
              grid: { color: 'rgba(61,172,123,0.1)' },
              ticks: { color: '#E8E8E8', font: { family: 'Space Grotesk', size: 11 } },
            },
            y: {
              stacked: true,
              grid: { color: 'rgba(61,172,123,0.1)' },
              ticks: { display: false },
            },
          },
        }
      });
    },

    updateTechTimelineChart() {
      // Tech timeline is static data — no dynamic filtering needed
    },
```

Also update the `init()` method to call `initCharts` after data loads. Replace the existing `init()`:

```javascript
    async init() {
      const params = new URLSearchParams(window.location.search);
      if (params.get('lang') === 'en') this.lang = 'en';

      const resp = await fetch('data/jeroen.json');
      this.data = await resp.json();
      this.loading = false;

      this.$nextTick(() => {
        this.initCharts();
      });
    },
```

- [ ] **Step 4: Add proficiency bars CSS**

Append to `jeroen/style.css`:

```css
/* ── Proficiency Bars ── */
.bar-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.bar-row:hover {
  background: rgba(61,172,123,0.08);
}

.bar-row.bar-active {
  background: rgba(61,172,123,0.15);
}

.bar-label {
  font-size: 12px;
  width: 110px;
  text-align: right;
  color: var(--text-secondary);
  flex-shrink: 0;
  font-weight: 500;
}

.bar-track {
  flex: 1;
  height: 18px;
  background: rgba(34,40,49,0.6);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--accent), var(--accent-bright));
  transition: width 0.6s ease;
}

.bar-value {
  font-size: 11px;
  color: var(--accent-bright);
  width: 65px;
  flex-shrink: 0;
}
```

- [ ] **Step 5: Verify dashboard zone**

Refresh browser, scroll to dashboard zone. Expected: section header "Expertise / Skills & Technologies", year range slider with two thumbs, 4 widget cards in a 2x2 grid. Radar chart shows 6-axis spider plot. Proficiency bars show all skills sorted by value. Donut chart shows industry breakdown. Tech timeline shows stacked area chart. Click a radar point or bar to filter — other charts should update. Click "Filters wissen" to reset.

- [ ] **Step 6: Commit**

```bash
git add jeroen/index.html jeroen/style.css jeroen/app.js
git commit -m "feat(jeroen): add dashboard zone with radar, bars, donut, and timeline charts"
```

---

## Task 7: Career Timeline

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`

- [ ] **Step 1: Add career timeline HTML**

In `jeroen/index.html`, after the dashboard zone closing `</div>` tags, add:

```html
  <!-- Career Timeline -->
  <div class="section" id="timeline">
    <div class="section-header" x-text="data ? t(data.ui.timeline) : ''"></div>
    <div class="section-title" x-text="data ? t(data.ui.timelineTitle) : ''"></div>

    <!-- Career phases -->
    <div class="timeline-phases" x-show="data">
      <template x-for="phase in data.careerPhases" :key="phase.label">
        <div class="timeline-phase"
             :style="`left: ${((phase.startYear - 2015) / (2026 - 2015)) * 100}%; width: ${((phase.endYear - phase.startYear) / (2026 - 2015)) * 100}%`">
          <span class="timeline-phase-label" x-text="phase.label"></span>
        </div>
      </template>
    </div>

    <!-- Timeline -->
    <div class="timeline-horizontal" x-show="data">
      <div class="timeline-line"></div>

      <!-- Featured projects (large dots) -->
      <template x-for="project in data.projects" :key="project.id">
        <div class="tl-item tl-item-major"
             :class="{ current: project.current, dimmed: hasActiveFilter && !matchesFilter(project) }"
             :style="`left: ${((project.startYear - 2015) / (2026 - 2015)) * 100}%`"
             @click="document.getElementById(project.id)?.scrollIntoView({ behavior: 'smooth' })">
          <div class="tl-dot"></div>
          <div class="tl-tooltip">
            <div class="tl-tooltip-role" x-text="t(project.role)"></div>
            <div class="tl-tooltip-client" x-text="project.client"></div>
            <div class="tl-tooltip-period" x-text="project.period"></div>
          </div>
          <div class="tl-label">
            <div class="tl-date" x-text="project.period"></div>
            <div class="tl-title" x-text="typeof project.name === 'string' ? project.name : t(project.name)"></div>
            <div class="tl-company" x-text="project.client"></div>
          </div>
        </div>
      </template>

      <!-- Minor clients (small dots) -->
      <template x-for="client in data.clients.filter(c => !c.featured)" :key="client.name">
        <div class="tl-item tl-item-minor"
             :class="{ dimmed: hasActiveFilter && !matchesFilter(client) }"
             :style="`left: ${((client.startYear - 2015) / (2026 - 2015)) * 100}%`">
          <div class="tl-dot-small"></div>
          <div class="tl-tooltip">
            <div class="tl-tooltip-client" x-text="client.name"></div>
            <div class="tl-tooltip-period" x-text="client.startYear"></div>
          </div>
        </div>
      </template>

      <!-- Year markers -->
      <template x-for="year in [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]" :key="year">
        <div class="tl-year-marker" :style="`left: ${((year - 2015) / (2026 - 2015)) * 100}%`">
          <span x-text="year"></span>
        </div>
      </template>
    </div>
  </div>
```

- [ ] **Step 2: Add timeline CSS**

Append to `jeroen/style.css`:

```css
/* ── Career Timeline ── */
.timeline-phases {
  position: relative;
  height: 28px;
  margin-bottom: 8px;
}

.timeline-phase {
  position: absolute;
  height: 24px;
  background: var(--accent-10);
  border: 1px solid var(--accent-20);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-phase-label {
  font-size: 10px;
  color: var(--accent);
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.timeline-horizontal {
  position: relative;
  height: 200px;
  margin-top: 16px;
  overflow-x: auto;
  overflow-y: visible;
  min-width: 100%;
}

.timeline-line {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent-bright), var(--accent), transparent);
}

.tl-item {
  position: absolute;
  top: 46px;
  cursor: pointer;
  z-index: 2;
}

.tl-item.dimmed {
  opacity: 0.2;
  pointer-events: none;
}

.tl-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--accent-bright);
  margin: 0 auto;
  transition: all 0.3s;
}

.tl-item.current .tl-dot {
  background: var(--accent-bright);
  box-shadow: 0 0 12px var(--bright-50);
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { box-shadow: 0 0 8px var(--bright-50); }
  50% { box-shadow: 0 0 16px var(--bright-50); }
}

.tl-dot-small {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-30);
  margin: 4px auto;
}

.tl-tooltip {
  display: none;
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg-surface);
  border: 1px solid var(--accent-20);
  border-radius: 8px;
  padding: 8px 12px;
  white-space: nowrap;
  z-index: 10;
}

.tl-item:hover .tl-tooltip {
  display: block;
}

.tl-tooltip-role { font-size: 11px; color: var(--accent); font-weight: 600; }
.tl-tooltip-client { font-size: 12px; font-weight: 600; }
.tl-tooltip-period { font-size: 10px; color: var(--text-secondary); }

.tl-label {
  text-align: center;
  margin-top: 8px;
  max-width: 120px;
  transform: translateX(-50%);
  margin-left: 7px;
}

.tl-date { font-size: 10px; color: var(--accent); font-weight: 600; }
.tl-title { font-size: 12px; font-weight: 600; white-space: nowrap; }
.tl-company { font-size: 11px; color: var(--text-secondary); }

.tl-item-minor .tl-label { display: none; }

.tl-year-marker {
  position: absolute;
  top: 70px;
  transform: translateX(-50%);
}

.tl-year-marker span {
  font-size: 10px;
  color: var(--text-secondary);
  opacity: 0.5;
}
```

- [ ] **Step 3: Verify timeline**

Refresh browser, scroll to timeline section. Expected: career phases bar at top ("Credon" and "Freelancer / JEBE"), horizontal timeline with large dots for featured projects and small dots for minor clients, year markers along the bottom, current projects have glowing dots, hover shows tooltip, items dim when filters are active.

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css
git commit -m "feat(jeroen): add horizontal career timeline with major/minor project dots"
```

---

## Task 8: Featured Projects

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`

- [ ] **Step 1: Add featured projects HTML**

In `jeroen/index.html`, after the timeline section, add:

```html
  <!-- Featured Projects -->
  <div class="section" id="projects">
    <div class="section-header" x-text="data ? t(data.ui.projects) : ''"></div>
    <div class="section-title" x-text="data ? t(data.ui.projectsTitle) : ''"></div>
    <div class="projects-grid" x-show="data">
      <template x-for="project in data.projects" :key="project.id">
        <div class="project-card"
             :id="project.id"
             :class="{ dimmed: hasActiveFilter && !matchesFilter(project), expanded: expandedProject === project.id }"
             @click="expandedProject = expandedProject === project.id ? null : project.id; setFilter('client', project.client)">
          <div class="project-card-header">
            <div>
              <div class="project-period" x-text="project.period"></div>
              <div class="project-name" x-text="typeof project.name === 'string' ? project.name : t(project.name)"></div>
              <div class="project-client">
                <span x-text="project.client"></span>
                <span class="project-via" x-text="'(' + t(data.ui.via) + ' ' + project.via + ')'"></span>
              </div>
            </div>
            <div class="project-current-badge" x-show="project.current" x-text="t(data.ui.present)"></div>
          </div>
          <div class="tech-tags">
            <template x-for="tech in project.technologies" :key="tech">
              <span class="tech-tag" x-text="tech"></span>
            </template>
          </div>
          <div class="project-details" x-show="expandedProject === project.id" x-collapse>
            <div class="project-role">
              <strong>Role:</strong> <span x-text="t(project.role)"></span>
            </div>
            <p class="project-description" x-text="t(project.description)"></p>
          </div>
        </div>
      </template>
    </div>
  </div>
```

Add `expandedProject: null,` to the `portfolio()` return object in `app.js`, after `charts: {},`.

- [ ] **Step 2: Add project card CSS**

Append to `jeroen/style.css`:

```css
/* ── Featured Projects ── */
.projects-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.project-card {
  background: var(--bg-surface);
  border-radius: 12px;
  padding: 24px;
  border-left: 4px solid var(--accent);
  cursor: pointer;
  transition: all 0.3s;
}

.project-card:hover {
  transform: translateY(-2px);
  border-left-color: var(--accent-bright);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.project-card.dimmed {
  opacity: 0.2;
  pointer-events: none;
}

.project-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.project-period { font-size: 11px; color: var(--accent); font-weight: 600; margin-bottom: 2px; }
.project-name { font-size: 18px; font-weight: 700; margin-bottom: 4px; }
.project-client { font-size: 13px; color: var(--text-secondary); }
.project-via { font-size: 11px; opacity: 0.6; }

.project-current-badge {
  background: var(--accent);
  color: var(--bg-primary);
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.tech-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 8px; }

.tech-tag {
  padding: 3px 10px;
  background: var(--accent-15);
  border-radius: 12px;
  font-size: 11px;
  color: var(--accent-bright);
  border: 1px solid var(--accent-20);
}

.project-details {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--accent-10);
}

.project-role {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.project-role strong { color: var(--accent); }

.project-description {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}
```

- [ ] **Step 3: Add Alpine.js collapse plugin**

In `jeroen/index.html`, add this script tag before the Alpine.js CDN script:

```html
  <script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
```

- [ ] **Step 4: Verify projects**

Refresh browser. Expected: 2-column grid of project cards. Each shows period, name, client, via, and tech tags. Click to expand — description and role slide down. Current project (Etex EMS) shows a "heden" badge. Cards dim when cross-filter is active.

- [ ] **Step 5: Commit**

```bash
git add jeroen/index.html jeroen/style.css jeroen/app.js
git commit -m "feat(jeroen): add expandable featured project cards with cross-filtering"
```

---

## Task 9: Client Portfolio

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`

- [ ] **Step 1: Add client portfolio HTML**

After the projects section, add:

```html
  <!-- Client Portfolio -->
  <div class="section section-center" id="clients">
    <div class="section-header" x-text="data ? t(data.ui.clientsHeader) : ''"></div>
    <div class="section-title" x-text="data ? t(data.ui.clientsTitle) : ''"></div>
    <div class="client-grid" x-show="data">
      <template x-for="client in data.clients.filter(c => c.featured)" :key="client.name">
        <div class="client-chip"
             :class="{ active: filters.client === client.name, dimmed: hasActiveFilter && !matchesFilter(client) }"
             @click="setFilter('client', client.name)">
          <img x-show="client.logo" :src="'img/clients/' + client.name.toLowerCase().replace(/[^a-z0-9]/g, '-') + '.svg'"
               :alt="client.name" class="client-logo" @error="$el.style.display='none'; $el.nextElementSibling.style.display='inline'">
          <span x-text="client.name"></span>
        </div>
      </template>
      <div class="client-chip client-chip-more">
        <span>+</span>
        <span x-text="data.clients.filter(c => !c.featured).length"></span>
        <span x-text="t(data.ui.moreClients)"></span>
      </div>
    </div>
  </div>
```

- [ ] **Step 2: Add client portfolio CSS**

Append to `jeroen/style.css`:

```css
/* ── Client Portfolio ── */
.section-center { text-align: center; }

.client-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.client-chip {
  padding: 10px 20px;
  background: var(--bg-surface);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid var(--accent-10);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.client-chip:hover, .client-chip.active {
  border-color: var(--accent);
  background: var(--accent-10);
}

.client-chip.dimmed {
  opacity: 0.2;
  pointer-events: none;
}

.client-chip-more {
  color: var(--accent);
  font-weight: 600;
  cursor: default;
}

.client-logo {
  height: 20px;
  width: auto;
  filter: grayscale(100%) brightness(2);
  transition: filter 0.3s;
}

.client-chip:hover .client-logo {
  filter: none;
}
```

- [ ] **Step 3: Verify clients**

Refresh browser. Expected: centered grid of client name chips. Featured clients shown. "+X more" chip at the end. Clicking a chip filters other sections. Logo images will show broken (no files yet) — the `@error` handler hides the img and shows the text fallback.

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css
git commit -m "feat(jeroen): add client portfolio section with cross-filter chips"
```

---

## Task 10: Credentials & Contact

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`

- [ ] **Step 1: Add credentials HTML**

After the clients section, add:

```html
  <!-- Credentials -->
  <div class="section section-center" id="credentials">
    <div class="section-header" x-text="data ? t(data.ui.credentials) : ''"></div>
    <div class="section-title" x-text="data ? t(data.ui.credentialsTitle) : ''"></div>
    <div class="cert-grid" x-show="data">
      <template x-for="cert in data.certifications" :key="cert.name">
        <div class="cert-card"
             :class="{ active: filters.technology && cert.technologies.includes(filters.technology) }"
             @click="setFilter('technology', cert.technologies[0])">
          <div class="cert-icon" x-text="cert.vendor[0]"></div>
          <div class="cert-name" x-text="cert.name"></div>
          <div class="cert-year" x-text="cert.year"></div>
        </div>
      </template>
      <template x-for="edu in data.education" :key="t(edu.name)">
        <div class="cert-card cert-card-edu">
          <div class="cert-icon cert-icon-edu">&#x1F393;</div>
          <div class="cert-name" x-text="t(edu.name)"></div>
          <div class="cert-institution" x-text="edu.institution"></div>
          <div class="cert-year" x-text="edu.period"></div>
        </div>
      </template>
    </div>
  </div>

  <!-- Contact -->
  <div class="contact-section" id="contact">
    <h2 x-text="data ? t(data.ui.contactTitle) : ''"></h2>
    <p x-text="data ? t(data.ui.contactSub) : ''"></p>
    <div class="contact-links" x-show="data">
      <a :href="data ? data.profile.linkedin : '#'" target="_blank" class="contact-btn primary">LinkedIn</a>
      <a :href="data ? 'mailto:' + data.profile.email : '#'" class="contact-btn secondary">E-mail</a>
    </div>
  </div>
```

- [ ] **Step 2: Add credentials and contact CSS**

Append to `jeroen/style.css`:

```css
/* ── Credentials ── */
.cert-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.cert-card {
  background: var(--bg-surface);
  border-radius: 10px;
  padding: 20px 12px;
  text-align: center;
  border: 1px solid var(--accent-10);
  cursor: pointer;
  transition: all 0.2s;
}

.cert-card:hover, .cert-card.active {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.cert-card-edu { cursor: default; }

.cert-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin: 0 auto 12px;
  background: linear-gradient(135deg, var(--accent), var(--accent-bright));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: var(--bg-primary);
}

.cert-icon-edu {
  background: linear-gradient(135deg, #4a5568, #718096);
  font-size: 24px;
}

.cert-name {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 4px;
}

.cert-institution {
  font-size: 11px;
  color: var(--accent);
  margin-bottom: 2px;
}

.cert-year {
  font-size: 11px;
  color: var(--accent);
  font-weight: 600;
}

/* ── Contact ── */
.contact-section {
  text-align: center;
  padding: 80px 40px;
  background: linear-gradient(180deg, transparent, rgba(57,62,70,0.3));
}

.contact-section h2 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.contact-section p {
  color: var(--text-secondary);
  margin-bottom: 24px;
  font-size: 16px;
}

.contact-links {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.contact-btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  font-family: var(--font);
  transition: all 0.2s;
  display: inline-block;
}

.contact-btn.primary {
  background: var(--accent);
  color: var(--bg-primary);
}

.contact-btn.primary:hover {
  background: var(--accent-bright);
}

.contact-btn.secondary {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
}

.contact-btn.secondary:hover {
  background: var(--accent-10);
}
```

- [ ] **Step 3: Verify credentials and contact**

Refresh browser. Expected: certification cards in a 5-column grid with vendor initial icons, names, and years. Education cards with graduation cap icon. Contact section at bottom with heading, subtitle, and two buttons. Language toggle switches all text. Clicking a cert card filters the dashboard to related technologies.

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css
git commit -m "feat(jeroen): add credentials grid and contact section"
```

---

## Task 11: Scroll Animations

**Files:**
- Modify: `jeroen/style.css`
- Modify: `jeroen/app.js`

- [ ] **Step 1: Add reveal animation CSS**

Append to `jeroen/style.css`:

```css
/* ── Scroll Reveal Animations ── */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

.reveal-delay-1 { transition-delay: 0.1s; }
.reveal-delay-2 { transition-delay: 0.2s; }
.reveal-delay-3 { transition-delay: 0.3s; }
.reveal-delay-4 { transition-delay: 0.4s; }
```

- [ ] **Step 2: Add Intersection Observer to app.js**

Append to `jeroen/app.js` (outside the `portfolio()` function):

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  // Re-observe when Alpine finishes rendering
  setTimeout(() => {
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }, 500);
});
```

- [ ] **Step 3: Add reveal classes to HTML sections**

In `jeroen/index.html`, add `class="reveal"` to key elements. Specifically:

- Add `reveal` to the `.hero-content` div
- Add `reveal` to each `.stat-item` template wrapper
- Add `reveal` to the `.year-filter` div
- Add `reveal` to each `.dash-widget` div
- Add `reveal` to the `.timeline-horizontal` div
- Add `reveal` to the `.projects-grid` div
- Add `reveal` to the `.client-grid` div
- Add `reveal` to the `.cert-grid` div
- Add `reveal` to the `.contact-section` div

For staggered grid items, add `reveal-delay-1`, `reveal-delay-2`, etc. to the `.dash-widget` divs:

```html
<div class="dash-widget reveal">           <!-- radar -->
<div class="dash-widget dash-widget-large reveal reveal-delay-1">  <!-- bars -->
<div class="dash-widget reveal reveal-delay-2">           <!-- donut -->
<div class="dash-widget dash-widget-large reveal reveal-delay-3">  <!-- tech timeline -->
```

- [ ] **Step 4: Verify animations**

Refresh browser. Expected: sections are invisible initially. As you scroll down, each section fades in and slides up. Dashboard widgets appear with staggered delays. Stats bar items appear together.

- [ ] **Step 5: Commit**

```bash
git add jeroen/index.html jeroen/style.css jeroen/app.js
git commit -m "feat(jeroen): add scroll-triggered reveal animations"
```

---

## Task 12: Responsive Design

**Files:**
- Modify: `jeroen/style.css`

- [ ] **Step 1: Add responsive breakpoints**

Append to `jeroen/style.css`:

```css
/* ── Responsive: Tablet ── */
@media (max-width: 1024px) {
  .hero-content { flex-direction: column; text-align: center; gap: 32px; }
  .hero-text h1 { font-size: 36px; }
  .hero-intro { max-width: 100%; }
  .hero-subtitle-wrapper { display: flex; justify-content: center; }

  .dash-grid { grid-template-columns: 1fr; }
  .dash-widget-large { grid-column: span 1; }

  .projects-grid { grid-template-columns: 1fr; }

  .cert-grid { grid-template-columns: repeat(3, 1fr); }

  .stats-bar { gap: 24px; }
  .stat-number { font-size: 28px; }

  .section { padding: 60px 24px; }
}

/* ── Responsive: Mobile ── */
@media (max-width: 768px) {
  .hero-text h1 { font-size: 28px; }
  .hero-title { font-size: 18px; }
  .hero-photo { width: 140px; height: 140px; }
  .hero-photo span { font-size: 48px; }

  .scroll-nav { display: none; }

  /* Mobile progress bar at top */
  .mobile-progress {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    z-index: 90;
    background: var(--accent-20);
  }

  .mobile-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent-bright));
    transition: width 0.1s linear;
  }

  .stats-bar { gap: 16px; padding: 24px 16px; flex-wrap: wrap; }
  .stat-item { min-width: 80px; }
  .stat-number { font-size: 24px; }

  .year-filter { flex-direction: column; align-items: stretch; }
  .year-filter-controls { flex-wrap: wrap; }

  .cert-grid { grid-template-columns: repeat(2, 1fr); }

  .client-chip { padding: 8px 14px; font-size: 13px; }

  .section { padding: 48px 16px; }
  .section-title { font-size: 22px; }

  .contact-links { flex-direction: column; align-items: center; }

  .timeline-horizontal { overflow-x: scroll; -webkit-overflow-scrolling: touch; scroll-snap-type: x proximity; }
  .tl-item-major { scroll-snap-align: center; }

  .lang-toggle { top: 12px; right: 12px; }
}

/* Hide mobile progress on desktop */
@media (min-width: 769px) {
  .mobile-progress { display: none; }
}
```

- [ ] **Step 2: Add mobile progress bar HTML**

In `jeroen/index.html`, after the `<body>` tag, add:

```html
  <!-- Mobile Progress Bar -->
  <div class="mobile-progress" x-data="{ progress: 0 }" @scroll.window="progress = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100">
    <div class="mobile-progress-fill" :style="`width: ${progress}%`"></div>
  </div>
```

- [ ] **Step 3: Verify responsive design**

Open browser dev tools, toggle device toolbar. Test at:
- **1024px width:** Hero stacks vertically, dashboard widgets single column, project cards single column
- **768px width:** Scroll nav disappears, mobile progress bar appears at top, smaller fonts, cert grid 2 columns
- **375px width (iPhone SE):** Everything readable, no horizontal overflow, timeline horizontally scrollable

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css
git commit -m "feat(jeroen): add responsive design for tablet and mobile"
```

---

## Task 13: Final Integration & Polish

**Files:**
- Modify: `jeroen/index.html`
- Modify: `jeroen/style.css`
- Modify: `jeroen/app.js`

- [ ] **Step 1: Add x-cloak to prevent flash of unstyled content**

In `jeroen/style.css`, add at the top after the reset:

```css
[x-cloak] { display: none !important; }
```

In `jeroen/index.html`, add `x-cloak` to the body tag:

```html
<body x-data="portfolio()" x-init="init()" x-cloak>
```

And add a loading state that shows while data loads:

```html
  <!-- Loading -->
  <div x-show="loading" class="loading-screen">
    <div class="loading-text">JB<span class="accent">.</span></div>
  </div>
```

Add loading screen CSS:

```css
.loading-screen {
  position: fixed;
  inset: 0;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-text {
  font-size: 48px;
  font-weight: 700;
  color: var(--text-primary);
  animation: pulse 1.5s infinite;
}
```

- [ ] **Step 2: Update HTML lang attribute reactively**

In `jeroen/index.html`, update the `<html>` tag:

```html
<html :lang="lang || 'nl'">
```

- [ ] **Step 3: Verify full page end-to-end**

Refresh browser. Run through the complete user flow:
1. Page loads with loading screen, then reveals hero
2. NL content is default. Click NL/EN toggle — all text switches
3. Add `?lang=en` to URL — page opens in English
4. Scroll through all sections — animations trigger
5. Progress bar tracks scroll position
6. Adjust year range slider — charts update
7. Click a radar chart point — bars, donut, timeline, projects filter
8. Click an industry donut slice — other charts filter
9. Click a proficiency bar — other charts filter
10. Click a project card — it expands with details
11. Click a client chip — dashboard highlights that client's data
12. Click a certification — highlights related technologies
13. Click "Filters wissen" — everything resets
14. Test on mobile viewport — layout adapts

- [ ] **Step 4: Commit**

```bash
git add jeroen/index.html jeroen/style.css jeroen/app.js
git commit -m "feat(jeroen): add loading state, x-cloak, and final polish"
```

- [ ] **Step 5: Update .gitignore for placeholder assets**

The `jeroen/img/` directory will have placeholder images later. No action needed now, but ensure the directory exists:

```bash
touch jeroen/img/.gitkeep jeroen/img/clients/.gitkeep
git add jeroen/img/.gitkeep jeroen/img/clients/.gitkeep
git commit -m "chore(jeroen): add placeholder directories for images"
```

---

## Open Items (Post-Implementation)

These items depend on user input and can be addressed after the core implementation:

1. **Client classification CSV** — User reviews and fills in `info/cv/client_classification.csv`. Then update `jeroen/data/jeroen.json` with full client list, correct industries, technologies, and exact stat figures.
2. **Professional photo** — User provides photo, save as `jeroen/img/photo.jpg`. Update hero to use `<img>` instead of initials placeholder.
3. **Client logos** — Source SVG logos for featured clients, save in `jeroen/img/clients/`. Filenames should match the slugified client name (e.g., `atlas-copco.svg`).
4. **Dutch project descriptions** — Review and refine the NL translations in `jeroen.json`.
5. **Exact stats** — Update `stats` values in JSON after CSV is finalized.
