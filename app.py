#!/usr/bin/env python3
"""
AI Marketing Suite — Streamlit App
Full UI for the claude-mark2 marketing toolkit.
"""

import streamlit as st
import sys
import os
import json
import tempfile
from datetime import datetime

# Add scripts directory to path so we can import the modules directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from analyze_page import analyze
from competitor_scanner import scan_competitor, scan_multiple
from social_calendar import generate_calendar, POSTING_FREQUENCY

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Marketing Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .score-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .score-high   { background:#d4edda; color:#155724; }
    .score-medium { background:#fff3cd; color:#856404; }
    .score-low    { background:#f8d7da; color:#721c24; }
    .score-critical { background:#f5c6cb; color:#491217; }
    .section-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1B2A4A;
        border-bottom: 2px solid #2D5BFF;
        padding-bottom: 4px;
        margin-bottom: 8px;
    }
    .tag {
        display: inline-block;
        background: #e8eaf6;
        color: #3949ab;
        border-radius: 4px;
        padding: 2px 8px;
        margin: 2px;
        font-size: 0.85rem;
    }
    .tag-green { background: #e8f5e9; color: #2e7d32; }
    .tag-red   { background: #fce4ec; color: #c62828; }
    .tag-orange { background: #fff3e0; color: #e65100; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def score_badge(score: float, out_of: float = 10.0):
    pct = (score / out_of) * 100
    if pct >= 70:
        cls = "score-high"
    elif pct >= 45:
        cls = "score-medium"
    else:
        cls = "score-low"
    return f'<span class="score-badge {cls}">{score} / {int(out_of)}</span>'


def score_color(score: float, out_of: float = 10.0):
    pct = (score / out_of) * 100
    if pct >= 70:
        return "normal"
    elif pct >= 45:
        return "off"
    else:
        return "inverse"


def severity_icon(sev: str):
    return {"Critique": "🔴", "Haute": "🟠", "Moyenne": "🟡", "Basse": "🔵"}.get(sev, "⚪")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart--v2.png", width=64)
    st.title("AI Marketing Suite")
    st.caption("Powered by claude-mark2")
    st.divider()
    page = st.radio(
        "Navigation",
        [
            "🔍 Page Analyzer",
            "🕵️ Competitor Scanner",
            "📅 Social Calendar",
            "📄 PDF Report",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("All analysis runs locally.\nNo data is sent to external APIs.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PAGE ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🔍 Page Analyzer":
    st.title("🔍 Marketing Page Analyzer")
    st.caption("Analyze any webpage for SEO, conversion, trust signals, and tracking quality.")

    with st.form("analyze_form"):
        url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            help="Full URL including https://",
        )
        submitted = st.form_submit_button("Analyze Page", type="primary", use_container_width=True)

    if submitted and url:
        if not url.startswith("http"):
            url = "https://" + url
        with st.spinner(f"Analyzing {url} …"):
            result = analyze(url)

        if result.get("statut") == "erreur":
            st.error(f"Could not fetch the page: {result.get('message', 'Unknown error')}")
        else:
            data = result["analyse"]
            seo = data["seo"]
            conv = data["conversion"]
            trust = data["confiance"]
            tracking = data["tracking"]
            tech = data["technique"]
            scores = data["scores"]
            global_score = data["score_global"]

            # ── Global score banner ───────────────────────────────────────────
            st.divider()
            col_score, col_url, col_date = st.columns([1, 2, 1])
            col_score.metric("Overall Score", f"{global_score} / 10", delta=None)
            col_url.markdown(f"**URL:** [{url}]({url})")
            col_date.markdown(f"**Date:** {datetime.now().strftime('%d %b %Y')}")

            # ── Score breakdown ───────────────────────────────────────────────
            st.subheader("Score Breakdown")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SEO", f"{scores['seo']} / 10", delta_color=score_color(scores["seo"]))
            c2.metric("CTAs", f"{scores['cta']} / 10", delta_color=score_color(scores["cta"]))
            c3.metric("Trust", f"{scores['confiance']} / 10", delta_color=score_color(scores["confiance"]))
            c4.metric("Tracking", f"{scores['tracking']} / 10", delta_color=score_color(scores["tracking"]))

            st.divider()

            # ── SEO ───────────────────────────────────────────────────────────
            with st.expander("🔎 SEO Analysis", expanded=True):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown('<div class="section-header">Page Title</div>', unsafe_allow_html=True)
                    if seo["titre"]:
                        st.write(f'"{seo["titre"]}"')
                        length_color = "🟢" if seo["titre_ok"] else "🔴"
                        st.caption(f"{length_color} {seo['longueur_titre']} chars (ideal: 30–60)")
                    else:
                        st.error("No title tag found!")

                    st.markdown('<div class="section-header">Meta Description</div>', unsafe_allow_html=True)
                    if seo["meta_description"]:
                        st.write(f'"{seo["meta_description"]}"')
                        length_color = "🟢" if seo["meta_description_ok"] else "🔴"
                        st.caption(f"{length_color} {seo['longueur_meta_description']} chars (ideal: 120–160)")
                    else:
                        st.error("No meta description found!")

                with col_b:
                    st.markdown('<div class="section-header">Heading Structure</div>', unsafe_allow_html=True)
                    if seo["problemes_titres"]:
                        for issue in seo["problemes_titres"]:
                            st.warning(f"⚠️ {issue}")
                    else:
                        st.success("✅ Heading structure looks good")

                    h2s = seo.get("titres", {}).get("h2", [])
                    if h2s:
                        st.caption(f"H2 tags ({len(h2s)}):")
                        for h in h2s[:6]:
                            st.markdown(f'<span class="tag">{h}</span>', unsafe_allow_html=True)
                        if len(h2s) > 6:
                            st.caption(f"… and {len(h2s) - 6} more")

                st.divider()
                ci, co, cv = st.columns(3)
                ci.metric("Total Images", seo["images_total"])
                co.metric("Missing Alt Text", seo["images_sans_alt"],
                          delta="needs fixing" if seo["images_sans_alt"] > 0 else None,
                          delta_color="inverse")
                cv.metric("Lazy-Loaded Images", seo["images_avec_lazy_loading"])

                st.caption(
                    f"{'✅' if seo['a_viewport'] else '❌'} Viewport meta tag  |  "
                    f"{'✅' if seo['canonique'] else '⚠️'} Canonical tag  |  "
                    f"{'✅' if seo['og_tags'] else '⚠️'} OG tags ({len(seo['og_tags'])})"
                )

            # ── Conversion ────────────────────────────────────────────────────
            with st.expander("🎯 Conversion Signals"):
                col_cta, col_forms, col_btns = st.columns(3)
                col_cta.metric("CTAs Found", conv["nombre_ctas"])
                col_forms.metric("Forms Found", conv["nombre_formulaires"])
                col_btns.metric("Buttons Found", len(conv["boutons"]))

                if conv["ctas"]:
                    st.markdown("**Detected CTAs:**")
                    for cta in conv["ctas"]:
                        st.markdown(f'<span class="tag tag-green">🎯 {cta["text"]}</span>', unsafe_allow_html=True)
                else:
                    st.error("🚨 No CTAs detected — this is a critical conversion issue!")

                if conv["formulaires"]:
                    st.markdown("**Forms:**")
                    for form in conv["formulaires"]:
                        fields = form.get("field_count", 0)
                        st.write(f"📋 Form ({form.get('method', 'GET')}) — {fields} field(s)")

            # ── Trust & Tracking ──────────────────────────────────────────────
            with st.expander("🛡️ Trust & Tracking"):
                col_t, col_tr = st.columns(2)

                with col_t:
                    st.markdown("**Social Media Links**")
                    if trust["liens_sociaux"]:
                        for link in trust["liens_sociaux"]:
                            st.markdown(f'<span class="tag">{link["platform"]}</span>', unsafe_allow_html=True)
                    else:
                        st.warning("No social links found")

                with col_tr:
                    st.markdown("**Analytics & Tracking Tools**")
                    if tracking["outils_detectes"]:
                        for tool in tracking["outils_detectes"]:
                            st.markdown(f'<span class="tag tag-green">✅ {tool}</span>', unsafe_allow_html=True)
                    else:
                        st.error("No tracking tools detected!")

                    if tracking["types_schema"]:
                        st.markdown("**Schema Markup**")
                        for schema in tracking["types_schema"]:
                            st.markdown(f'<span class="tag">{schema}</span>', unsafe_allow_html=True)

            # ── Technical ─────────────────────────────────────────────────────
            with st.expander("⚙️ Technical"):
                ct, ci2, ce, cs = st.columns(4)
                ct.metric("Total Links", tech["total_liens"])
                ci2.metric("Internal Links", tech["liens_internes"])
                ce.metric("External Links", tech["liens_externes"])
                cs.metric("Scripts", tech["nombre_scripts"])

                robots = data.get("robots", {})
                sitemap = data.get("sitemap", {})
                r1, r2 = st.columns(2)
                r1.markdown(f"**robots.txt:** {'✅ Found' if robots.get('existe') else '❌ Missing'}  \n"
                            f"Sitemap reference: {'✅' if robots.get('a_reference_sitemap') else '⚠️ Not referenced'}")
                r2.markdown(f"**sitemap.xml:** {'✅ Found' if sitemap.get('existe') else '❌ Missing'}  \n"
                            f"URLs indexed: {sitemap.get('nombre_urls', 'N/A')}")

            # ── Raw JSON ──────────────────────────────────────────────────────
            with st.expander("🗂️ Raw JSON Data"):
                st.json(result)

    elif submitted:
        st.warning("Please enter a URL.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COMPETITOR SCANNER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🕵️ Competitor Scanner":
    st.title("🕵️ Competitor Scanner")
    st.caption("Scan competitor websites to extract positioning, pricing, CTAs, and trust signals.")

    with st.form("competitor_form"):
        urls_input = st.text_area(
            "Competitor URLs (one per line)",
            placeholder="https://competitor1.com\nhttps://competitor2.com\nhttps://competitor3.com",
            height=120,
        )
        submitted = st.form_submit_button("Scan Competitors", type="primary", use_container_width=True)

    if submitted and urls_input:
        urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
        if not urls:
            st.warning("Please enter at least one URL.")
        else:
            with st.spinner(f"Scanning {len(urls)} competitor(s) …"):
                if len(urls) == 1:
                    results = [scan_competitor(urls[0])]
                else:
                    results = scan_multiple(urls)

            # ── Summary table ─────────────────────────────────────────────────
            st.subheader(f"Results: {len(results)} Competitor(s)")

            for i, res in enumerate(results):
                domain = res.get("domaine", res.get("url", f"Competitor {i+1}"))
                if res.get("statut") == "erreur":
                    st.error(f"❌ {domain}: {res.get('message', 'Could not fetch')}")
                    continue

                d = res.get("donnees", {})
                positioning = d.get("positionnement", {})
                tarif = d.get("tarification", {})
                trust = d.get("confiance", {})
                ctas = d.get("ctas", [])
                content = d.get("contenu", {})
                pricing_page = res.get("page_tarification", {})

                with st.expander(f"🏢 {domain}", expanded=True):
                    col_pos, col_trust = st.columns(2)

                    with col_pos:
                        st.markdown("**Positioning**")
                        title = positioning.get("titre_principal", "—")
                        if title:
                            st.write(f'**"{title}"**')
                        tagline = positioning.get("accroche", "")
                        if tagline:
                            st.caption(tagline)

                        sections = positioning.get("sections_cles", [])
                        if sections:
                            st.markdown("Key sections:")
                            for s in sections[:5]:
                                st.markdown(f'<span class="tag">{s}</span>', unsafe_allow_html=True)

                    with col_trust:
                        st.markdown("**Trust Signals**")
                        nb_social = trust.get("nombre_liens_sociaux", 0)
                        has_testimonials = trust.get("a_temoignages", False)
                        logos = trust.get("nombre_logos_estimes", 0)
                        platforms = trust.get("plateformes_sociales", [])

                        if platforms:
                            for p in platforms:
                                st.markdown(f'<span class="tag tag-green">📲 {p}</span>', unsafe_allow_html=True)
                        else:
                            st.warning("No social links")

                        st.caption(
                            f"{'✅' if has_testimonials else '❌'} Testimonials  |  "
                            f"~{logos} client/partner logos  |  "
                            f"{content.get('nombre_mots', 0)} words"
                        )

                    st.divider()
                    col_cta, col_price = st.columns(2)

                    with col_cta:
                        st.markdown("**CTAs**")
                        if ctas:
                            for cta in ctas[:6]:
                                st.markdown(f'<span class="tag tag-green">🎯 {cta}</span>', unsafe_allow_html=True)
                        else:
                            st.warning("No CTAs detected")

                    with col_price:
                        st.markdown("**Pricing**")
                        if tarif.get("a_info_tarification"):
                            for mention in tarif.get("mentions_tarification", [])[:5]:
                                st.markdown(f'<span class="tag tag-orange">💰 {mention}</span>', unsafe_allow_html=True)
                        else:
                            st.warning("No pricing info found on homepage")

                        if pricing_page.get("trouvee"):
                            st.success(f"✅ Pricing page found: {pricing_page.get('url', '')}")
                            for m in pricing_page.get("mentions_tarification", [])[:3]:
                                st.caption(f"  • {m}")
                        else:
                            st.caption("No dedicated pricing page found")

            # ── Comparison table (multiple competitors) ───────────────────────
            if len([r for r in results if r.get("statut") == "succès"]) > 1:
                st.divider()
                st.subheader("Side-by-Side Comparison")
                import pandas as pd
                rows = []
                for res in results:
                    if res.get("statut") != "succès":
                        continue
                    d = res["donnees"]
                    rows.append({
                        "Domain": res.get("domaine", ""),
                        "CTAs": len(d.get("ctas", [])),
                        "Social Links": d["confiance"].get("nombre_liens_sociaux", 0),
                        "Has Testimonials": "✅" if d["confiance"].get("a_temoignages") else "❌",
                        "Has Pricing": "✅" if d["tarification"].get("a_info_tarification") else "❌",
                        "Pricing Page": "✅" if res.get("page_tarification", {}).get("trouvee") else "❌",
                        "Word Count": d["contenu"].get("nombre_mots", 0),
                    })
                st.dataframe(pd.DataFrame(rows).set_index("Domain"), use_container_width=True)

    elif submitted:
        st.warning("Please enter at least one URL.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: SOCIAL CALENDAR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Social Calendar":
    st.title("📅 Social Media Content Calendar")
    st.caption("Generate a structured 30-day content plan for any topic and platform mix.")

    with st.form("social_form"):
        topic = st.text_input(
            "Topic / Brand / Product",
            placeholder="e.g. GPS fleet tracking software, eco skincare brand …",
        )

        all_platforms = list(POSTING_FREQUENCY.keys())
        selected_platforms = st.multiselect(
            "Platforms",
            options=all_platforms,
            default=["linkedin", "instagram", "twitter"],
        )

        days = st.slider("Number of days", min_value=7, max_value=60, value=30, step=7)

        submitted = st.form_submit_button("Generate Calendar", type="primary", use_container_width=True)

    if submitted:
        if not topic:
            st.warning("Please enter a topic.")
        elif not selected_platforms:
            st.warning("Please select at least one platform.")
        else:
            with st.spinner("Generating content calendar …"):
                calendar = generate_calendar(topic, selected_platforms, days)

            st.success(f"✅ {days}-day calendar generated for **{topic}**")

            # ── Posting frequency summary ────────────────────────────────────
            st.subheader("Recommended Posting Frequency")
            freq_cols = st.columns(len(selected_platforms))
            for i, platform in enumerate(selected_platforms):
                freq = POSTING_FREQUENCY.get(platform, {})
                freq_cols[i].markdown(
                    f"**{platform.capitalize()}**  \n"
                    f"🎯 Ideal: {freq.get('ideal', '—')}  \n"
                    f"⏰ Best times: {freq.get('meilleurs_horaires', '—')}"
                )

            # ── Content pillar distribution ───────────────────────────────────
            st.subheader("Content Pillar Distribution")
            dist = calendar.get("distribution_piliers", {})
            pcols = st.columns(len(dist))
            pillar_names = {
                "educatif": "📚 Educational",
                "coulisses": "🎬 Behind the Scenes",
                "preuve_sociale": "⭐ Social Proof",
                "engagement": "💬 Engagement",
                "promotionnel": "📢 Promotional",
            }
            for i, (pillar, pct) in enumerate(dist.items()):
                pcols[i].metric(pillar_names.get(pillar, pillar), pct)

            st.divider()

            # ── Calendar table ────────────────────────────────────────────────
            st.subheader("Day-by-Day Calendar")

            import pandas as pd
            rows = []
            for entry in calendar["calendrier"]:
                platform_list = ", ".join(entry["plateformes"].keys())
                rows.append({
                    "Day": entry["jour"],
                    "Date": entry["date"],
                    "Weekday": entry["jour_semaine"],
                    "Pillar": entry["pilier"],
                    "Format": entry["format"],
                    "Angle": entry["angle_sujet"],
                    "Platforms": platform_list,
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, height=500)

            # ── Hook formulas ─────────────────────────────────────────────────
            st.divider()
            st.subheader("Hook Formulas by Platform")
            for platform in selected_platforms:
                hooks = calendar.get("formules_accroche", {}).get(platform, [])
                if hooks:
                    with st.expander(f"✍️ {platform.capitalize()} Hooks"):
                        for hook in hooks:
                            st.markdown(f"- {hook}")

            # ── Repurposing strategy ──────────────────────────────────────────
            st.divider()
            st.subheader("♻️ Content Repurposing Strategy")
            repurpose = calendar.get("strategie_reutilisation", {})
            if repurpose:
                st.caption(repurpose.get("description", ""))
                for step in repurpose.get("workflow", []):
                    st.markdown(f"- {step}")

            # ── Download ──────────────────────────────────────────────────────
            st.divider()
            st.download_button(
                label="⬇️ Download Calendar as JSON",
                data=json.dumps(calendar, indent=2, ensure_ascii=False),
                file_name=f"social-calendar-{topic[:30].replace(' ', '-')}.json",
                mime="application/json",
                use_container_width=True,
            )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PDF REPORT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📄 PDF Report":
    st.title("📄 PDF Marketing Report Generator")
    st.caption("Run a page analysis and generate a professional, client-ready PDF report.")

    with st.form("pdf_form"):
        url = st.text_input(
            "Website URL to analyze",
            placeholder="https://example.com",
        )
        brand_name = st.text_input(
            "Brand / Company name",
            placeholder="e.g. Geotrack BV",
        )
        submitted = st.form_submit_button("Analyze & Generate PDF", type="primary", use_container_width=True)

    if submitted and url:
        if not url.startswith("http"):
            url = "https://" + url

        with st.spinner("Analyzing website …"):
            result = analyze(url)

        if result.get("statut") == "erreur":
            st.error(f"Could not fetch: {result.get('message')}")
        else:
            data = result["analyse"]
            scores = data["scores"]
            seo = data["seo"]
            conv = data["conversion"]
            trust = data["confiance"]
            tracking = data["tracking"]

            # ── Build report data structure ───────────────────────────────────
            overall = round(data["score_global"] * 10)  # scale 0-10 → 0-100

            issues = []
            if not seo.get("titres", {}).get("h1"):
                issues.append({"severity": "Critique", "finding": "Missing H1 tag — critical for SEO and user clarity"})
            if conv["nombre_ctas"] == 0:
                issues.append({"severity": "Critique", "finding": "No CTAs detected — visitors have no clear next step"})
            if conv["nombre_formulaires"] == 0:
                issues.append({"severity": "Haute", "finding": "No lead capture forms found — no way to collect prospects"})
            if trust["nombre_liens_sociaux"] == 0:
                issues.append({"severity": "Haute", "finding": "No social media links — missed trust and traffic signals"})
            if tracking["nombre_outils"] == 0:
                issues.append({"severity": "Haute", "finding": "No analytics/tracking tools detected — flying blind on performance"})
            if seo["images_sans_alt"] > 0:
                issues.append({"severity": "Moyenne", "finding": f"{seo['images_sans_alt']} images missing alt text — hurts SEO and accessibility"})
            if not seo["meta_description_ok"]:
                issues.append({"severity": "Moyenne", "finding": f"Meta description length ({seo['longueur_meta_description']} chars) is outside ideal range"})
            if not seo["titre_ok"]:
                issues.append({"severity": "Basse", "finding": f"Title tag length ({seo['longueur_titre']} chars) is outside ideal 30–60 char range"})

            quick_wins = [
                "Add a clear H1 tag that states your core value proposition",
                "Add 2–3 prominent CTAs: 'Request Demo', 'Start Free Trial', or 'Get a Quote'",
                "Install Google Analytics 4 + Google Tag Manager for tracking",
                "Add links to your LinkedIn, Facebook, and Instagram pages",
            ]
            medium_term = [
                "Create a dedicated 'Pricing' page with transparent plans or a quote request flow",
                "Add customer testimonials with name, company, and specific results",
                "Set up a contact/lead capture form with email automation",
                "Add schema markup (Organization, Product, FAQ) for rich search results",
            ]
            strategic = [
                "Build landing pages targeting competitor brand keywords",
                "Launch a monthly newsletter to nurture leads not yet ready to buy",
                "Create a case study library showcasing real customer ROI",
                "Implement retargeting campaigns on Meta and Google for site visitors",
            ]

            report_data = {
                "url": url,
                "date": datetime.now().strftime("%d %B %Y"),
                "brand_name": brand_name or url,
                "overall_score": overall,
                "executive_summary": (
                    f"This marketing audit of {brand_name or url} reveals key opportunities to improve "
                    f"conversion rates, SEO visibility, and trust signals. The site scores {overall}/100 overall, "
                    f"with the most critical gaps in {'conversion (no CTAs)' if conv['nombre_ctas'] == 0 else 'tracking'} "
                    f"and {'analytics (no tracking tools)' if tracking['nombre_outils'] == 0 else 'social proof'}."
                ),
                "categories": {
                    "SEO & Visibility":          {"score": scores["seo"] * 10, "weight": "25%"},
                    "Conversion Optimization":   {"score": scores["cta"] * 10, "weight": "20%"},
                    "Brand & Trust":             {"score": scores["confiance"] * 10, "weight": "20%"},
                    "Analytics & Tracking":      {"score": scores["tracking"] * 10, "weight": "15%"},
                    "Content & Messaging":       {"score": min(100, data["contenu"]["nombre_mots"] // 10), "weight": "10%"},
                    "Technical Health":          {"score": 60 if data["sitemap"]["existe"] else 30, "weight": "10%"},
                },
                "findings": issues,
                "quick_wins": quick_wins,
                "medium_term": medium_term,
                "strategic": strategic,
                "competitors": [],
            }

            # ── Show summary before generating PDF ────────────────────────────
            st.success(f"Analysis complete — Overall Score: **{overall} / 100**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SEO", f"{scores['seo'] * 10}/100")
            c2.metric("Conversion", f"{scores['cta'] * 10}/100")
            c3.metric("Trust", f"{scores['confiance'] * 10}/100")
            c4.metric("Tracking", f"{scores['tracking'] * 10}/100")

            if issues:
                st.subheader("Key Findings")
                for issue in issues:
                    icon = severity_icon(issue["severity"])
                    st.markdown(f"{icon} **{issue['severity']}** — {issue['finding']}")

            # ── Generate PDF ──────────────────────────────────────────────────
            st.divider()
            try:
                from generate_pdf_report import generate_report

                with st.spinner("Generating PDF …"):
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        pdf_path = tmp.name
                    generate_report(report_data, pdf_path)

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                safe_name = (brand_name or "report").replace(" ", "-").lower()
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"marketing-report-{safe_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                )
                os.unlink(pdf_path)

            except Exception as e:
                st.error(f"PDF generation failed: {e}")
                st.info("Make sure reportlab is installed: `.venv\\Scripts\\pip install reportlab`")

    elif submitted:
        st.warning("Please enter a URL.")
