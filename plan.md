# Improvement Plan — AI Marketing Suite

This document tracks proposed improvements to the project, organized by priority and effort.

---

## 🔴 High Impact, Manageable Effort

### 1. Playwright/Selenium Fallback for JS-Rendered Sites
**Status:** Not started  
**Problem:** `urllib` cannot execute JavaScript. Modern sites (React, Angular, Shopify, Next.js) return an empty HTML shell, making the analyzer useless on ~60% of the web including Expedia, Amazon, and most SaaS platforms.  
**Solution:** When `urllib` returns an empty or suspiciously short response, retry with a headless browser (Playwright recommended over Selenium for performance).  
**Implementation steps:**
- [ ] `pip install playwright` and `playwright install chromium`
- [ ] Add a `fetch_page_headless(url)` fallback in `analyze_page.py` and `competitor_scanner.py`
- [ ] Detect JS-rendered pages by checking if parsed word count < 100 after initial fetch
- [ ] Route to headless fetch automatically on failure
- [ ] Add a `"fetch_method": "urllib | playwright"` field to the output JSON
- [ ] Add Playwright to `requirements.txt` as an optional dependency

---

### 2. LLM-Powered Scoring via API
**Status:** Not started  
**Problem:** Current scores are simple rule-based deductions (`-2 if no H1`). They produce deterministic but shallow results — no understanding of context, tone, industry, or actual copy quality.  
**Solution:** After parsing, send the structured data + raw text snippets to Claude or OpenAI API to produce contextual, nuanced scores and recommendations.  
**Implementation steps:**
- [ ] Add `anthropic` or `openai` to `requirements.txt`
- [ ] Create `scripts/llm_scorer.py` with a `score_with_llm(parsed_data, api_key)` function
- [ ] Build a prompt template that feeds parsed SEO/content/conversion data to the LLM
- [ ] Return structured JSON scores + written recommendations from the LLM
- [ ] Add an API key input field in the Streamlit app (stored in `st.session_state`, never persisted)
- [ ] Fall back to rule-based scoring if no API key is provided
- [ ] Add a toggle in the UI: "Basic Analysis" vs "AI-Powered Analysis"

---

### 3. Analysis History & Session Persistence
**Status:** Not started  
**Problem:** The Streamlit app is completely stateless — every result disappears on rerun. Users cannot track improvements over time or compare before/after states.  
**Solution:** Store analysis results locally in a SQLite database or JSON file.  
**Implementation steps:**
- [ ] Create `history.db` (SQLite) with schema: `id, url, timestamp, score_global, scores_json, full_result_json`
- [ ] After every successful analysis, auto-save to the database
- [ ] Add a "History" page to the Streamlit app showing past analyses per domain
- [ ] Add a "Compare" view: select two analyses of the same URL and diff the scores
- [ ] Add a "Delete" button per record
- [ ] Export history as CSV

---

## 🟠 Medium Impact

### 4. Multi-Page Analysis (Homepage + Key Pages)
**Status:** Not started  
**Problem:** All scripts currently only fetch the homepage. A real marketing audit covers the pricing page, about page, product/feature pages, and blog — as described in the agent instructions but not implemented in the Python scripts.  
**Solution:** Crawl a configurable set of pages per domain and aggregate scores.  
**Implementation steps:**
- [ ] Auto-detect key pages from the sitemap or internal links: `/pricing`, `/about`, `/features`, `/blog`
- [ ] Run `MarketingPageParser` on each discovered page
- [ ] Aggregate scores with page-level weighting (homepage > pricing > about)
- [ ] Add per-page breakdown in the Streamlit UI
- [ ] Add a `--pages` CLI argument to `analyze_page.py`

---

### 5. Integrated Competitor Comparison in Page Analyzer
**Status:** Not started  
**Problem:** The Page Analyzer and Competitor Scanner are separate, disconnected tools. Analyzing your own site alongside competitors requires two separate workflows.  
**Solution:** Add an optional "Compare with competitors" step at the bottom of the Page Analyzer.  
**Implementation steps:**
- [ ] Add a "Add competitor URLs" expander below the Page Analyzer results
- [ ] When submitted, run `scan_multiple()` on the competitor URLs
- [ ] Render a unified side-by-side comparison table: target vs. each competitor
- [ ] Highlight gaps (e.g. competitor has pricing page, target doesn't)

---

### 6. Export Improvements
**Status:** Not started  
**Problem:** Social calendar exports as JSON only; PDF reports have a generic cover; the app can't save or share reports.  
**Sub-tasks:**
- [ ] **Social Calendar CSV export:** Convert the calendar DataFrame to CSV/Excel with `pandas.to_excel()`
- [ ] **PDF branded cover:** Allow users to upload a logo in the Streamlit app; embed it on the PDF cover page using reportlab's `Image` element
- [ ] **Email report:** Add a "Send report by email" option using `smtplib` with configurable SMTP settings
- [ ] **Share link:** Generate a shareable static HTML export of the analysis results

---

### 7. Translate Skills and Agents to English
**Status:** Not started  
**Problem:** All 15 `skills/market-*/SKILL.md` files and all 5 `agents/*.md` files are written in French. Claude Code will produce French-language audit reports, copy suggestions, and strategies even for English-speaking users.  
**Solution:** Translate all skill and agent files to English, or add a language toggle in `market/SKILL.md`.  
**Implementation steps:**
- [ ] Translate `market/SKILL.md` (orchestrator)
- [ ] Translate `agents/market-content.md`
- [ ] Translate `agents/market-conversion.md`
- [ ] Translate `agents/market-competitive.md`
- [ ] Translate `agents/market-technical.md`
- [ ] Translate `agents/market-strategy.md`
- [ ] Translate all 15 `skills/market-*/SKILL.md` files
- [ ] Remove the `IMPORTANT: Tu dois toujours répondre en français` directive from all files (or make it configurable)

---

## 🟡 Lower Effort, Nice to Have

### 8. Add `.gitignore`
**Status:** Not started  
**Problem:** `.venv/`, `__pycache__/`, generated output files (`AUDIT-MARKETING.md`, `RAPPORT-MARKETING.pdf`, etc.), and `*.pdf` are untracked and will pollute the repo.  
**Implementation steps:**
- [ ] Create `.gitignore` with: `.venv/`, `__pycache__/`, `*.pyc`, `*.pdf`, `AUDIT-*.md`, `RAPPORT-*.md`, `CALENDRIER-*.md`, `history.db`, `.env`

---

### 9. Fix `requirements.txt` to Cover All Dependencies
**Status:** Not started  
**Problem:** `requirements.txt` only lists `reportlab`. Running `pip install -r requirements.txt` does not install `streamlit` or `pandas`, so the Streamlit app won't work out of the box.  
**Implementation steps:**
- [ ] Update `requirements.txt`:
  ```
  reportlab>=4.0
  streamlit>=1.30
  pandas>=2.0
  # Optional — for JS-rendered site support:
  # playwright>=1.40
  # Optional — for LLM scoring:
  # anthropic>=0.20
  # openai>=1.0
  ```

---

### 10. Caching Layer
**Status:** Not started  
**Problem:** Analyzing the same URL twice fetches and re-parses everything. Slow sites (5–15 second load) make iteration painful.  
**Solution:** Add a simple TTL cache (1 hour default) using `functools.lru_cache` or a file-based cache.  
**Implementation steps:**
- [ ] Add a `cache/` directory to store fetched HTML keyed by URL hash
- [ ] Add a `--no-cache` flag to bypass it
- [ ] Show "Cached result from X minutes ago" indicator in the Streamlit UI
- [ ] Auto-expire cache entries after 1 hour

---

### 11. Better Error Messages
**Status:** Not started  
**Problem:** When a site fails to fetch, the app just shows "Impossible de récupérer la page" with no context on why or what to do.  
**Solution:** Detect the failure reason and show a specific, actionable message.  
**Implementation steps:**
- [ ] Catch `HTTPError` codes: 403 → "Bot protection detected (Cloudflare/anti-scraping)", 404 → "Page not found", 429 → "Rate limited — try again later", 5xx → "Server error"
- [ ] Detect timeout separately: "Site took too long to respond (>15s)"
- [ ] Detect SSL errors: "SSL certificate issue — site may have expired cert"
- [ ] Detect likely JS-only pages: "Page appears to be JavaScript-rendered — content not accessible without a browser"
- [ ] Show these messages in the Streamlit UI with a suggested action

---

## 🔵 Bigger Vision

### 12. Full Standalone Web App (No Claude Code Required)
**Status:** Not started  
**Problem:** The most powerful features (`/market copy`, `/market emails`, `/market social` content generation) only work inside Claude Code. Non-technical users can't access them.  
**Solution:** Expose all 15 commands as Streamlit pages, calling Claude or OpenAI API directly.  
**Implementation steps:**
- [ ] Add API key configuration page in the Streamlit sidebar
- [ ] Implement `/market copy` as a Streamlit page: fetch URL → extract content → send to LLM → display rewritten copy
- [ ] Implement `/market emails` as a Streamlit page: topic input → LLM generates email sequence → export as `.md` or `.docx`
- [ ] Implement `/market social` backed by LLM to enhance `social_calendar.py` output with actual post content (not just format templates)
- [ ] Implement `/market proposal` and `/market launch` as form-driven LLM pages
- [ ] Add a "Generate with AI" button to the existing Page Analyzer and Competitor Scanner results

---

### 13. Scheduled Monitoring & Alerts
**Status:** Not started  
**Problem:** The tool is point-in-time only. There is no way to know if a site's marketing score improves or degrades after changes.  
**Solution:** Add a scheduler that re-runs analyses on a configurable interval and alerts on score changes.  
**Implementation steps:**
- [ ] Add a "Monitor this URL" option in the Streamlit app
- [ ] Store monitored URLs in `history.db` with a `monitor_interval` column
- [ ] Use `schedule` or APScheduler to run background analyses
- [ ] Compare new score to previous score and flag regressions (score drop > 1 point)
- [ ] Send email/webhook alert on significant score change
- [ ] Add a "Monitoring Dashboard" page showing score trends over time with a line chart

---

## Priority Matrix

| # | Improvement | Impact | Effort | Priority |
|---|-------------|--------|--------|----------|
| 2 | LLM-powered scoring | 🔴 High | 🟡 Medium | **1st** |
| 4 | Multi-page analysis | 🔴 High | 🟡 Medium | **2nd** |
| 1 | Playwright fallback | 🔴 High | 🟠 Medium-High | **3rd** |
| 3 | Analysis history | 🟠 Medium | 🟡 Medium | **4th** |
| 5 | Integrated competitor comparison | 🟠 Medium | 🟡 Medium | **5th** |
| 7 | Translate skills/agents to English | 🟠 Medium | 🟡 Medium | **6th** |
| 9 | Fix requirements.txt | 🟡 Low | 🟢 Low | **7th** |
| 8 | Add .gitignore | 🟡 Low | 🟢 Low | **8th** |
| 11 | Better error messages | 🟡 Low | 🟢 Low | **9th** |
| 6 | Export improvements | 🟡 Low | 🟡 Medium | **10th** |
| 10 | Caching layer | 🟡 Low | 🟡 Medium | **11th** |
| 12 | Full standalone web app | 🔴 High | 🔴 High | **Long term** |
| 13 | Scheduled monitoring | 🟠 Medium | 🔴 High | **Long term** |
