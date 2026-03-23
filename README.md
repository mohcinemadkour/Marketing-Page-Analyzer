# AI Marketing Suite

A complete suite of marketing skills, agents, scripts, and a Streamlit web UI designed for Claude Code.

**GitHub:** https://github.com/mohcinemadkour/Marketing-Page-Analyzer

## Quick Install

```bash
git clone https://github.com/mohcinemadkour/Marketing-Page-Analyzer.git
cd Marketing-Page-Analyzer
bash install.sh
```

Or in a single command from anywhere:

```bash
curl -fsSL https://raw.githubusercontent.com/mohcinemadkour/Marketing-Page-Analyzer/main/install.sh | bash
```

## What Gets Installed

| Component | Count | Description |
|-----------|-------|-------------|
| Skills | 15 | Slash commands for every marketing task |
| Agents | 5 | Specialized sub-agents for full audits |
| Scripts | 4 | Python scripts for analysis and generation |
| Templates | 4 | Ready-to-use document templates |

## Available Commands

```
/market audit <url>        Full marketing audit (5 parallel agents)
/market quick <url>        60-second marketing snapshot
/market copy <url>         Generate optimized copywriting
/market emails <topic>     Generate email sequences
/market social <topic>     Social media content calendar
/market ads <url>          Ad creatives and copy
/market funnel <url>       Sales funnel analysis
/market competitors <url>  Competitive intelligence
/market landing <url>      Landing page CRO analysis
/market launch <product>   Product launch plan
/market proposal <client>  Commercial proposal generator
/market report <url>       Full marketing report (Markdown)
/market report-pdf <url>   Full marketing report (PDF)
/market seo <url>          SEO content audit
/market brand <url>        Brand voice analysis
```

## Command Details

### 1. Master Audit Commands

**`/market audit <url>`**
A complete scanner for your website. Analyzes everything: the buying journey, SEO, design, and trust signals using 5 AI agents running in parallel.
> *E-commerce example: Before spending thousands on Black Friday Facebook ads, run this on your store URL. It will flag: "Customer reviews are missing on product pages" or "The Add to Cart button isn't visible enough on mobile."*

**`/market quick <url>`**
The flash version of the audit — homepage analysis at a glance.
> *E-commerce example: You just updated your homepage banner with a new promotion. Run this to check if the offer ("-20% on the summer collection") is understandable within 3 seconds.*

### 2. Sales Funnel & Conversion

**`/market funnel <url>`**
Analyze the customer journey from ad click to checkout.
> *E-commerce example: You have 10,000 visitors/month but only 50 sales. This command finds where the drop-off occurs — e.g. customers abandoning at the shipping cost step.*

**`/market landing <url>`**
Optimize a specific page to convert better.
> *E-commerce example: Your best-seller product page gets traffic but poor conversion. The command tells you to add Before/After photos, move benefits above the price, and add urgency signals.*

### 3. Content & Copywriting

**`/market copy <url>`**
Rewrite bland product descriptions into persuasive copy.
> *E-commerce example: Transforms "100% cotton T-shirt, round neck, black" into "The perfect black tee that won't shrink in the wash and flatters your frame."*

**`/market brand <url>`**
Define your brand tone for consistent communication.
> *E-commerce example: Creates your brand bible — the exact vocabulary to use across your site and social channels, tailored to your audience.*

**`/market seo <url>`**
Optimize product pages and collections for Google rankings.
> *E-commerce example: Launching a "waterproof backpack" range? This checks if you're using the right keywords in H1/H2 headings, image alt text, and descriptions.*

### 4. Advertising & Social Media

**`/market ads <url>`**
Generate ad copy and video script ideas for paid campaigns.
> *E-commerce example: Provide your hero product link and get 3 short-video scripts (Unboxing, Problem/Solution, UGC Testimonial) ready to shoot for TikTok or Meta Ads.*

**`/market social <topic/url>`**
Build a complete posting plan for Instagram, TikTok, LinkedIn, etc.
> *E-commerce example: No content ideas for December? Get a full month planned: "Monday: How to use the product in winter", "Wednesday: Social proof post", "Friday: Eco-friendly packaging focus."*

**`/market competitors <url>`**
Scan competitor websites and find differentiation opportunities.
> *E-commerce example: You sell insulated water bottles. Run this on the market leader's site to reveal their best offers and get strategies to stand out.*

### 5. Email & Retention

**`/market emails <topic/url>`**
Write complete automated email sequences.
> *E-commerce example: "Create a 3-email abandoned cart sequence for my jewelry brand" → generates the 4-hour email, the next-day social proof email, and the 48-hour last-chance discount email.*

**`/market launch <product>`**
Build the action plan for a new product release.
> *E-commerce example: Launching a limited-edition supplement flavor? Get the full calendar: how to tease the VIP list first, what to send on launch day, and the "last hours" urgency email.*

### 6. Agency & Reporting

**`/market proposal <client>`**
Generate a structured commercial proposal.
> *B2B example: Selling wholesale to a distributor? The command generates the full pitch and structured quote to convince them to list your products.*

**`/market report <url>` and `/market report-pdf <url>`**
Generate a complete marketing report in Markdown or PDF.
> *Use case: Share a professional, client-ready audit with partners or a new agency to brief them on your site's current state.*

## ⚠️ Website Compatibility

The Python scripts use a standard HTTP fetcher. They work well on most traditional websites but **will not work** on:

| Site Type | Why It Fails |
|-----------|-------------|
| **Bot-protected sites** (Cloudflare, Expedia, Amazon) | Anti-bot systems block non-browser requests with 403 errors or CAPTCHAs |
| **JavaScript-rendered SPAs** (React, Vue, Angular) | The fetcher gets an empty HTML shell — real content only loads via JS |
| **Rate-limited / IP-blocked sites** | Enterprise sites block requests missing cookies or browser fingerprints |

**Works best on:** Traditional server-rendered websites (WordPress, PHP, static HTML), most SMB/agency/SaaS marketing sites.

## Streamlit App

A full browser UI is available in addition to the command-line scripts:

```powershell
pip install streamlit pandas
streamlit run app.py
```

Opens at `http://localhost:8501` with 4 sections: Page Analyzer, Competitor Scanner, Social Calendar, and PDF Report Generator.

## Prerequisites

- **Claude Code** installed and configured
- **Python 3.8+** for the analysis scripts
- **reportlab** (optional, for PDF reports): `pip install reportlab`

## Project Structure

```
claude-mark2/
├── market/
│   └── SKILL.md              # Main orchestrator
├── skills/
│   ├── market-audit/         # Full marketing audit
│   ├── market-brand/         # Brand voice
│   ├── market-copy/          # Optimized copywriting
│   ├── market-emails/        # Email sequences
│   ├── market-competitors/   # Competitive analysis
│   ├── market-social/        # Social media calendar
│   ├── market-funnel/        # Funnel analysis
│   ├── market-ads/           # Ad campaigns
│   ├── market-proposal/      # Commercial proposal
│   ├── market-landing/       # Landing page CRO
│   ├── market-launch/        # Product launch plan
│   ├── market-report/        # Marketing report (MD)
│   ├── market-report-pdf/    # Marketing report (PDF)
│   └── market-seo/           # SEO audit
├── agents/
│   ├── market-content.md     # Content & messaging agent
│   ├── market-conversion.md  # Conversion optimization agent
│   ├── market-competitive.md # Competitive analysis agent
│   ├── market-technical.md   # Technical & SEO agent
│   └── market-strategy.md    # Strategy & growth agent
├── scripts/
│   ├── analyze_page.py       # Web page analyzer
│   ├── competitor_scanner.py # Competitor scanner
│   ├── social_calendar.py    # Social calendar generator
│   └── generate_pdf_report.py# PDF report generator
├── templates/
│   ├── email-welcome.md      # Welcome email sequence
│   ├── proposal-template.md  # Client proposal template
│   ├── content-calendar.md   # 30-day content calendar
│   └── launch-checklist.md   # Product launch checklist
├── app.py                    # Streamlit web UI
├── install.sh                # Installer
├── uninstall.sh              # Uninstaller
└── requirements.txt          # Python dependencies
```

## Generated Files

Each command creates a report file in your working directory:

| Command | Output File |
|---------|-------------|
| `/market audit` | `AUDIT-MARKETING.md` |
| `/market brand` | `VOIX-DE-MARQUE.md` |
| `/market copy` | `SUGGESTIONS-COPY.md` |
| `/market emails` | `SEQUENCES-EMAILS.md` |
| `/market competitors` | `RAPPORT-CONCURRENTS.md` |
| `/market social` | `CALENDRIER-SOCIAL.md` |
| `/market funnel` | `ANALYSE-FUNNEL.md` |
| `/market ads` | `CAMPAGNES-PUB.md` |
| `/market proposal` | `PROPOSITION-CLIENT.md` |
| `/market landing` | `ANALYSE-LANDING.md` |
| `/market launch` | `PLAN-LANCEMENT.md` |
| `/market report` | `RAPPORT-MARKETING.md` |
| `/market report-pdf` | `RAPPORT-MARKETING-<domain>.pdf` |
| `/market seo` | `AUDIT-SEO.md` |

## Uninstall

```bash
bash uninstall.sh
```

## License

MIT License — see [LICENSE](LICENSE)
