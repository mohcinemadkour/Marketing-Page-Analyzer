# Architecture — AI Marketing Suite (claude-mark2)

## Overview

The AI Marketing Suite is a two-interface marketing analysis toolkit:

1. **CLI layer** — Python scripts callable directly from the terminal or by Claude Code slash commands
2. **Web UI layer** — A Streamlit single-page app (`app.py`) that wraps the same scripts behind a browser interface

Both interfaces share the same core Python modules in `scripts/`. There is no backend server, database, or external API — all analysis runs locally by fetching target websites over HTTP.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interfaces                          │
├──────────────────────────┬──────────────────────────────────────┤
│   CLI / Claude Code      │        Streamlit App (app.py)        │
│  /market <command> <url> │        http://localhost:8501         │
└──────────────┬───────────┴──────────────────┬───────────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Core Python Modules (scripts/)              │
│                                                                 │
│  analyze_page.py   competitor_scanner.py   social_calendar.py  │
│  generate_pdf_report.py                                         │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│              HTTP Layer (Python stdlib only)                     │
│  urllib.request · ssl · html.parser · urllib.parse              │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     External Target Websites                     │
│            (fetched directly, no proxy, no caching)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Breakdown

### `scripts/analyze_page.py`

**Purpose:** Full marketing page analysis — SEO, conversion signals, trust indicators, and tracking tools.

**Entry point:** `analyze(url: str) -> dict`

**Internal pipeline:**

```
analyze(url)
    │
    ├── fetch_page(url)              HTTP GET with Chrome User-Agent
    │       └── urllib.request.urlopen (SSL verification disabled)
    │
    ├── MarketingPageParser.feed(html)  SAX-style HTML parsing
    │       ├── handle_starttag()    Extracts meta, OG tags, headings,
    │       │                        links, images, forms, buttons, scripts
    │       ├── handle_endtag()      Finalizes CTAs, forms, schema JSON-LD
    │       └── handle_data()        Accumulates text content
    │
    ├── parser.get_results()         Compiles structured dict:
    │       ├── seo{}                Title, meta, headings, images, canonical
    │       ├── contenu{}            Word count, heading counts
    │       ├── conversion{}         CTAs, forms, buttons
    │       ├── confiance{}          Social links
    │       └── tracking{}           Analytics tools, schema types
    │
    ├── fetch_robots_txt(url)        Checks /robots.txt existence
    ├── fetch_sitemap(url)           Checks /sitemap.xml, counts <url> tags
    │
    └── Scoring engine
            ├── seo_score    /10     Title + meta + H1 + img alt + viewport
            ├── cta_score    /10     CTA count + value-CTA bonus
            ├── trust_score  /10     Social links + schema bonus
            └── track_score  /10     Number of analytics tools detected
```

**Output schema:**
```json
{
  "url": "https://...",
  "statut": "succès | erreur",
  "analyse": {
    "seo": { "titre", "longueur_titre", "titre_ok", "meta_description", ... },
    "contenu": { "nombre_mots", "h1", "h2" },
    "conversion": { "ctas", "formulaires", "boutons" },
    "confiance": { "liens_sociaux" },
    "tracking": { "outils_detectes", "types_schema" },
    "technique": { "total_liens", "liens_internes", "liens_externes" },
    "robots": { "existe", "a_reference_sitemap", "apercu_contenu" },
    "sitemap": { "existe", "nombre_urls" },
    "scores": { "seo", "cta", "confiance", "tracking" },
    "score_global": 0.0
  }
}
```

---

### `scripts/competitor_scanner.py`

**Purpose:** Extract positioning, pricing, CTAs, and trust signals from competitor websites.

**Entry points:**
- `scan_competitor(url: str) -> dict` — single URL
- `scan_multiple(urls: list[str]) -> list[dict]` — batch scan

**Internal pipeline:**

```
scan_competitor(url)
    │
    ├── fetch_page(url)
    │
    ├── CompetitorPageParser.feed(html)
    │       ├── Extracts: title, H1, H2, meta description, OG tags
    │       ├── Detects: social platforms, CTAs, pricing patterns (regex)
    │       └── Counts: testimonial signals, logo images
    │
    ├── parser.get_results()
    │       ├── positionnement{}     H1/title, tagline, key sections (H2s)
    │       ├── tarification{}       Pricing mentions via regex patterns
    │       ├── confiance{}          Social links, logo count, testimonials
    │       ├── ctas[]               Action-oriented link/button text
    │       └── contenu{}            Word count, section count
    │
    └── Pricing page probe
            Tries /tarifs, /pricing, /plans, /prix
            Returns pricing mentions from first successful hit
```

**Pricing detection regex patterns:**
`\$\d+`, `€\d+`, `/mois`, `/month`, `/year`, `free plan`, `free trial`, `enterprise`

**Output schema:**
```json
{
  "url": "...",
  "domaine": "...",
  "statut": "succès | erreur",
  "donnees": {
    "positionnement": { "titre_principal", "accroche", "sections_cles" },
    "tarification": { "a_info_tarification", "mentions_tarification" },
    "confiance": { "plateformes_sociales", "nombre_liens_sociaux", "a_temoignages" },
    "ctas": [],
    "contenu": { "nombre_mots", "nombre_sections" }
  },
  "page_tarification": { "trouvee", "url", "mentions_tarification" }
}
```

---

### `scripts/social_calendar.py`

**Purpose:** Generate a structured day-by-day content calendar for social media.

**Entry point:** `generate_calendar(topic: str, platforms: list[str], days: int) -> dict`

**Data model:**

```
Content Pillars (CONTENT_PILLARS)
    ├── educatif         (40%) — How-tos, tips, frameworks, data
    ├── coulisses        (15%) — Behind the scenes, process, tools
    ├── preuve_sociale   (15%) — Testimonials, case studies, results
    ├── engagement       (20%) — Questions, polls, opinions
    └── promotionnel     (10%) — Product demos, offers, events

Posting Frequencies (POSTING_FREQUENCY)
    linkedin / twitter / instagram / tiktok / youtube / facebook

Hook Formulas (HOOK_FORMULAS)
    Per-platform templates for opening lines
```

**Calendar generation algorithm:**
- Rotates through a fixed 10-pillar sequence repeated over `days`
- For each day: assigns pillar → selects format (round-robin on pillar's format list) → maps to platform-specific guidance
- Appends a repurposing strategy (1 piece → 10+ posts workflow)

**Output schema:**
```json
{
  "sujet": "...",
  "plateformes": [],
  "duree_jours": 30,
  "date_debut": "YYYY-MM-DD",
  "planning_publication": {},
  "piliers_contenu": {},
  "distribution_piliers": {},
  "formules_accroche": {},
  "calendrier": [
    {
      "jour": 1, "date": "...", "jour_semaine": "...",
      "pilier": "...", "format": "...", "angle_sujet": "...",
      "plateformes": { "linkedin": { "conseils": "...", "publier": true } }
    }
  ],
  "strategie_reutilisation": {}
}
```

---

### `scripts/generate_pdf_report.py`

**Purpose:** Generate a professional, client-ready PDF marketing report from structured data.

**Entry point:** `generate_report(data: dict, output_path: str) -> str`

**Dependencies:** `reportlab` (external), `pillow`, `charset-normalizer`

**PDF structure:**

```
Page 1 — Cover
    Logo placeholder · Brand name · Report title · Date · URL

Page 2 — Executive Summary
    Overall score gauge (circular SVG via reportlab Drawing)
    Score category breakdown (VerticalBarChart)
    Summary paragraph

Page 3 — Findings
    Severity-coded findings table (Critique / Haute / Moyenne / Basse)

Page 4 — Action Plan
    Quick Wins · Medium-Term · Strategic (3-column prioritized tables)

Page 5 — Competitor Comparison (if data provided)
    Competitor table: name, positioning, pricing, social proof, content

Page 6 — Methodology
    Category weights table

Footer — "Generated by claude-mark2"
```

**Input data contract:**
```json
{
  "url": "...",
  "date": "DD Month YYYY",
  "brand_name": "...",
  "overall_score": 0,
  "executive_summary": "...",
  "categories": {
    "Category Name": { "score": 0, "weight": "25%" }
  },
  "findings": [{ "severity": "Critique|Haute|Moyenne|Basse", "finding": "..." }],
  "quick_wins": [],
  "medium_term": [],
  "strategic": [],
  "competitors": []
}
```

---

## Streamlit App (`app.py`)

**Purpose:** Browser-based UI over the four core scripts.

**Architecture pattern:** Single-file multi-page app using sidebar radio navigation (no `st.Page` / multi-file routing — all pages in one file, conditionally rendered).

```
app.py
    │
    ├── sys.path.insert(scripts/)     Direct module import (no subprocess)
    ├── from analyze_page import analyze
    ├── from competitor_scanner import scan_competitor, scan_multiple
    ├── from social_calendar import generate_calendar, POSTING_FREQUENCY
    │   (generate_pdf_report imported lazily inside PDF page to avoid
    │    hard-failing if reportlab is not installed)
    │
    ├── Page: 🔍 Page Analyzer
    │       Form → analyze() → scored dashboard + expandable sections
    │       Sections: SEO · Conversion · Trust & Tracking · Technical · Raw JSON
    │
    ├── Page: 🕵️ Competitor Scanner
    │       Textarea (multi-URL) → scan_competitor() / scan_multiple()
    │       Per-competitor expanders + side-by-side pandas DataFrame comparison
    │
    ├── Page: 📅 Social Calendar
    │       Topic + platform multiselect + day slider
    │       → generate_calendar() → frequency table, pillar metrics,
    │         day-by-day DataFrame, hook formulas, repurposing steps
    │       + JSON download button
    │
    └── Page: 📄 PDF Report
            URL + brand name → analyze() → build report_data dict
            → generate_report() → tempfile → st.download_button (PDF bytes)
```

**State management:** Stateless — each form submission reruns the full script (standard Streamlit model, no `st.session_state` used).

---

## HTTP Fetch Layer

All four scripts use an identical internal `fetch_page(url)` function:

| Property | Value |
|----------|-------|
| Library | `urllib.request` (Python stdlib) |
| SSL | Verification disabled (`ssl.CERT_NONE`) |
| Timeout | 15 seconds |
| User-Agent | Chrome 120 on macOS |
| Redirects | Followed automatically by urllib |
| Encoding | UTF-8 with `errors="replace"` |
| No-JS | Raw HTML only — no JavaScript execution |

### Compatibility Constraints

| Site Type | Result | Reason |
|-----------|--------|--------|
| Server-rendered (WordPress, PHP, static) | ✅ Works | Full HTML returned |
| SPA / JS-rendered (React, Vue, Angular) | ❌ Empty shell | Content injected by JS |
| Cloudflare / bot-protected | ❌ 403 or CAPTCHA | Anti-bot fingerprinting |
| Enterprise (Expedia, Amazon) | ❌ Blocked | IP/session-based blocking |
| Sites with strict HSTS/pinning | ⚠️ May fail | SSL verification disabled but urllib may still reject |

---

## Scoring Model (`analyze_page.py`)

Scores are computed on a 0–10 scale per dimension, then averaged for the global score.

### SEO Score (starts at 10, deductions applied)

| Condition | Deduction |
|-----------|-----------|
| No title tag | −3 |
| Title outside 30–60 chars | −1 |
| No meta description | −3 |
| Meta description outside 120–160 chars | −1 |
| No H1 tag | −2 |
| Images without alt text (max −2) | −1 per image |
| Heading hierarchy issues | −1 |
| No viewport meta tag | −1 |

### CTA Score

| Condition | Score |
|-----------|-------|
| 0 CTAs | 1 |
| 1 CTA | 5 |
| 2–3 CTAs | 7 |
| 4+ CTAs | 8 |
| +1 bonus for CTAs with >10 char text | max 10 |

### Trust Score (starts at 5)

| Condition | Bonus |
|-----------|-------|
| 1–2 social links | +1 |
| 3+ social links | +2 |
| Schema markup present | +1 |

### Tracking Score

| Tools detected | Score |
|----------------|-------|
| 0 | 3 |
| 1 | 5 |
| 2 | 7 |
| 3+ | 9 |

**Global score** = `(seo + cta + trust + tracking) / 4`

---

## Claude Code Integration (Skills & Agents)

The `market/SKILL.md` orchestrator defines a routing layer for Claude Code's slash command system. When `/market <command>` is invoked:

```
/market audit <url>
    └── Spawns 5 parallel sub-agents:
            market-content.md     → Content quality, copywriting
            market-conversion.md  → CRO, CTAs, landing pages
            market-competitive.md → Positioning, competitors
            market-technical.md   → SEO technical, site speed
            market-strategy.md    → Pricing, growth strategy

/market <other command>
    └── Routes to skills/market-<command>/SKILL.md
            Each skill file contains:
            - Role definition
            - Analysis methodology
            - Output format specification
            - Scoring criteria
```

Skills and agents use Claude's context window as their "runtime" — they do not call Python scripts directly. The Python scripts are complementary tools invoked manually or via the Streamlit app.

---

## Dependency Map

```
app.py
├── streamlit          (pip)
├── pandas             (pip)
├── analyze_page       (local)
├── competitor_scanner (local)
├── social_calendar    (local)
└── generate_pdf_report (local, lazy import)
        ├── reportlab  (pip)
        └── pillow     (pip, transitive via reportlab)

analyze_page.py
    stdlib only: sys, json, re, urllib, ssl, html.parser

competitor_scanner.py
    stdlib only: sys, json, re, urllib, ssl, html.parser

social_calendar.py
    stdlib only: sys, json, datetime

generate_pdf_report.py
    └── reportlab (required)
            └── pillow (required)
            └── charset-normalizer (required)
```

**Zero external runtime dependencies** for the three analysis scripts — they run on any Python 3.8+ installation with no `pip install`.

---

## Data Flow Diagram — PDF Report Generation

```
User provides URL + brand name
        │
        ▼
analyze(url)  ────────────────────────────────────────────┐
        │                                                  │
        ▼                                                  │
scores = { seo, cta, trust, tracking }                    │
seo_data, conv_data, trust_data, tracking_data            │
        │                                                  │
        ▼                                                  │
app.py builds report_data dict                            │
        ├── overall_score  (avg × 10, scaled 0–100)       │
        ├── executive_summary (generated string)           │
        ├── categories (6 dimensions with weights)         │
        ├── findings (auto-generated from score gaps)      │
        ├── quick_wins / medium_term / strategic (fixed)   │
        └── competitors [] (empty unless pre-populated)    │
                │                                          │
                ▼                                          │
generate_report(report_data, tmp_path)                    │
        │                                                  │
        ├── reportlab SimpleDocTemplate                    │
        ├── Draw score gauges (Drawing + Circle + String)  │
        ├── Draw bar chart (VerticalBarChart)              │
        ├── Build findings table (TableStyle severity rows)│
        ├── Build action plan tables                       │
        └── doc.build(elements) → PDF bytes               │
                │                                          │
                ▼                                          │
st.download_button(pdf_bytes) ◄───────────────────────────┘
```

---

## Agent System — How Each Agent Works

The `/market audit <url>` command is the only command that uses agents. It spawns all 5 agents **in parallel** inside Claude Code's context, each independently fetching and evaluating the target site, then their outputs are merged into a single composite audit report.

```
/market audit https://example.com
        │
        ├── agent market-content     ──► Contenu & Messages score  (25% weight)
        ├── agent market-conversion  ──► Optimisation Conversion    (20% weight)
        ├── agent market-competitive ──► Positionnement Concurrent  (15% weight)
        ├── agent market-technical   ──► SEO & Visibilité           (20% weight)
        └── agent market-strategy   ──► Marque & Stratégie          (20% weight)
                                                │
                                                ▼
                                    Composite Marketing Score 0–100
                                    Written to AUDIT-MARKETING.md
```

Each agent follows the same inner loop independently:
1. **Fetch** — uses Claude's WebFetch tool to retrieve real live HTML from the target URL
2. **Analyze** — scores its assigned dimensions on a 0–10 scale using its own rubric
3. **Generate** — produces a structured Markdown section with scores, findings, before/afters, and prioritized recommendations

---

### Agent 1 — `market-content` (Content & Messaging)

**File:** `agents/market-content.md`  
**Audit weight:** 25%  
**Role:** Evaluates whether the site's copy actually persuades and converts.

**Pages it fetches:**
- Homepage
- About page
- Pricing page
- One feature/product page
- One blog post (if a blog exists)

**5 scoring dimensions (each 0–10):**

| Dimension | What it measures |
|-----------|-----------------|
| Title Clarity | Does the homepage title communicate value in under 5 seconds? Is it specific (not generic)? |
| Value Proposition Strength | Is there a clear, differentiated "why choose us" with proof (numbers, results, timeframes)? |
| Copy Persuasion | Benefits over features, customer language, emotional triggers, objection handling |
| Content Depth | Enough content to inform purchase decisions; educational content (blog, guides, resources) |
| CTA Effectiveness | Value-oriented button text, strategic placement, clear primary vs secondary CTA hierarchy |

**Key output — Before/After rewrites:**  
For the 3 biggest problems found, the agent generates exact current copy ("Before") alongside a corrected rewrite ("After") with an explanation — not just abstract advice.

**Output written to:** `AUDIT-MARKETING.md` (merged section)

---

### Agent 2 — `market-conversion` (Conversion Rate Optimization)

**File:** `agents/market-conversion.md`  
**Audit weight:** 20%  
**Role:** Finds every point of friction that stops visitors from converting.

**Conversion journey it maps:**
- Homepage → What is the primary CTA?
- Landing/feature pages → Where do they send traffic?
- Pricing page → How is price presented?
- Signup/contact page → What is the conversion mechanism?
- Any visible forms, modals, or popups

**5 scoring dimensions (each 0–10):**

| Dimension | What it measures |
|-----------|-----------------|
| CTA Strategy | Primary vs secondary clarity, value-oriented text, visual hierarchy, mobile accessibility |
| Social Proof | Testimonials with names/photos, client logos, case studies, user counts, third-party review badges |
| Friction Analysis | Number of conversion steps, form fields, account creation requirements, payment UX |
| Trust Signals | SSL badges, privacy policy visibility, money-back guarantee, contact accessibility, design quality |
| Urgency & Scarcity | Time-limited offers, social proof urgency ("X people viewing"), waitlist messaging |

**Key output — Funnel leak detection:**  
Maps the full awareness→interest→consideration→intent→conversion funnel and identifies where prospects most likely abandon, with severity (Critical / High / Medium / Low) and estimated revenue impact per fix.

**Key output — A/B test hypotheses:**  
Generates 3–5 testable hypotheses in the format: *"If we [change], then [metric] will [improve] because [reason]."*

---

### Agent 3 — `market-competitive` (Competitive Intelligence)

**File:** `agents/market-competitive.md`  
**Audit weight:** 15%  
**Role:** Finds the market gaps and positioning angles competitors aren't using.

**Discovery process:**
1. Fetches the target homepage to identify the product/service category
2. Uses WebSearch with queries like `"[category] alternatives"`, `"[brand] vs"`, `"best [category] tools"` to find 3–5 real competitors
3. Fetches each competitor's homepage directly to extract live data

**Data extracted from each competitor:**
- Main positioning statement
- Pricing (if public)
- Key features highlighted
- Social proof (customer counts, notable logos)
- Content strategy (blog, podcast, YouTube, newsletter)
- Unique angles the target site doesn't use

**5 scoring dimensions (each 0–10):**

| Dimension | What it measures |
|-----------|-----------------|
| Positioning Clarity | Can you distinguish them from competitors in under 10 seconds? |
| Pricing Competitiveness | Transparent, competitive, aligned with buyer expectations |
| Feature Messaging | Key differentiating features communicated prominently |
| Market Awareness | Do they have comparison/alternative pages? Do they address "why us"? |
| Content Authority | Blog depth, guides, thought leadership vs just a product page |

**Key output — 5 opportunity types:**
1. **Positioning gaps** — angles no competitor owns yet
2. **Content gaps** — topics competitors cover but the target doesn't
3. **Messaging gaps** — features the target has but doesn't promote
4. **Alternative page opportunities** — "[Competitor] Alternative" pages to capture high-intent switcher traffic
5. **Switching narrative** — story to convince competitor users to switch

---

### Agent 4 — `market-technical` (Technical SEO & Infrastructure)

**File:** `agents/market-technical.md`  
**Audit weight:** 20%  
**Role:** Audits the technical foundations that determine whether the site can be found and trusted by search engines.

**What it fetches:**
- Target URL (HTML source)
- `/robots.txt`
- `/sitemap.xml`
- A blog/content page (if found)

**Analysis areas:**

**On-page structure:**  
Title tag (50–60 chars, keyword-rich), meta description (150–160 chars, includes CTA), single H1, logical H2–H6 hierarchy, image alt text, clean URL structure, canonical tag.

**Crawlability & Indexability:**  
robots.txt directives, sitemap existence, accidental noindex tags, internal link structure, orphan pages.

**Performance indicators:**  
Page weight estimation, render-blocking resources in HTML, lazy loading implementation, CDN usage signals, compression headers.

**Mobile compatibility:**  
Viewport meta tag, responsive design indicators, touch-target sizing.

**Tracking & Analytics:**  
Scans HTML source for: Google Analytics (gtag), Google Tag Manager, Meta Pixel (fbq), LinkedIn Insight Tag, Hotjar, FullStory, Mixpanel, HubSpot, cookie consent mechanism, UTM parameter usage.

**Schema / Structured Data:**  
Checks for JSON-LD or microdata: Organization, Website+SearchAction, Product/Service, FAQ, Review/Rating, Breadcrumb, Article.

**Scoring weights within this agent:**

| Sub-dimension | Weight |
|--------------|--------|
| Page Structure | 25% |
| Crawlability | 20% |
| Performance | 15% |
| Content Architecture | 20% |
| Schema & Tracking | 20% |

**Key output:** A filled tracking configuration table (✅/❌ per tool) and a schema markup table, plus specific corrective examples — e.g. *"Add meta description: 'Geotrack helps fleet managers track vehicles in real time and reduce fuel costs by 30%...'"*

---

### Agent 5 — `market-strategy` (Brand, Trust & Growth Strategy)

**File:** `agents/market-strategy.md`  
**Audit weight:** 20% (covers two of the 6 composite dimensions: Brand & Trust 10% + Growth & Strategy 10%)  
**Role:** Evaluates whether the business has a credible brand and a scalable growth strategy.

**Pages it fetches:**
- Homepage
- About page
- Pricing page
- Blog (if present)

**Part A — Brand & Trust (3 dimensions):**

| Dimension | What it measures |
|-----------|-----------------|
| Brand Consistency | Visual coherence (colors, typography, images) and messaging consistency across all pages |
| Trust Architecture | About page quality (team photos, story, mission), contact visibility, privacy messaging, certifications |
| Authority Signals | Thought leadership content, media mentions, industry awards, social following, conference appearances |

**Part B — Growth Strategy (3 dimensions):**

| Dimension | What it measures |
|-----------|-----------------|
| Pricing Strategy | Transparency, friction-free entry point, Good-Better-Best tier structure, upsell paths |
| Acquisition Channels | Number of active channels, content marketing maturity, SEO investment, paid ads indicators, referral/affiliate program |
| Retention & Expansion | Onboarding indicators, community features, upgrade paths, newsletter, help documentation quality |

**Key output — Revenue opportunity matrix:**  
Every recommendation is tagged with Effort (Low/Medium/High), Impact (Low/Medium/High), Timeline (1 week / 1 month / 3 months / 6 months), and a conservative revenue impact estimate.

**Revenue opportunity tiers:**
- **Quick wins (1–2 weeks):** Pricing page optimizations, CTA copy changes, adding social proof above the fold
- **Medium term (1–3 months):** Content marketing expansion, email nurturing sequences, competitor positioning pages, referral program
- **Strategic (3–6 months):** New acquisition channel development, product-led growth features, partnership strategy, community building

---

### Agent Orchestration — Composite Score Calculation

After all 5 agents complete, their individual scores are combined into a **Marketing Score 0–100**:

```
Composite Score = Weighted Average of 6 categories

┌──────────────────────────────┬────────┬─────────────────────────┐
│ Category                     │ Weight │ Measured by             │
├──────────────────────────────┼────────┼─────────────────────────┤
│ Content & Messaging          │  25%   │ market-content agent    │
│ Conversion Optimization      │  20%   │ market-conversion agent │
│ SEO & Visibility             │  20%   │ market-technical agent  │
│ Competitive Positioning      │  15%   │ market-competitive agent│
│ Brand & Trust                │  10%   │ market-strategy agent   │
│ Growth & Strategy            │  10%   │ market-strategy agent   │
└──────────────────────────────┴────────┴─────────────────────────┘

Score interpretation:
  80–100  Strong — minor optimizations needed
  60–79   Good foundation — several clear improvement areas
  40–59   Significant gaps — conversion and/or SEO fundamentals missing
  0–39    Critical issues — fundamental marketing infrastructure absent
```

---

## File Reference

| File | Type | Purpose |
|------|------|---------|
| `app.py` | Python | Streamlit web UI |
| `scripts/analyze_page.py` | Python | Page marketing analyzer |
| `scripts/competitor_scanner.py` | Python | Competitor site scanner |
| `scripts/social_calendar.py` | Python | Social content calendar generator |
| `scripts/generate_pdf_report.py` | Python | PDF report renderer |
| `market/SKILL.md` | Markdown | Claude Code main orchestrator |
| `skills/market-*/SKILL.md` | Markdown | Per-command Claude Code skill definitions |
| `agents/market-content.md` | Markdown | Content & messaging audit agent |
| `agents/market-conversion.md` | Markdown | CRO audit agent |
| `agents/market-competitive.md` | Markdown | Competitive intelligence agent |
| `agents/market-technical.md` | Markdown | Technical SEO audit agent |
| `agents/market-strategy.md` | Markdown | Brand & growth strategy agent |
| `templates/*.md` | Markdown | Reusable document templates |
| `requirements.txt` | Text | Python dependencies (`reportlab>=4.0`) |
| `install.sh` / `uninstall.sh` | Bash | Claude Code skill installation scripts |
