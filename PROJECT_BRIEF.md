# ConsultX — Project Brief
*Phase Zero output — prepared August 14, 2026, from the pasted build prompt and 10 uploaded files.*

## 1. Company

- **Name:** ConsultX (spelling is inconsistent across sources — see Open Items).
- **What it is:** A newly founded engineering consultancy with no completed projects under its own corporate name yet. Positioned as an "Engineering Knowledge Company" — it markets the founders' individual expertise and methodology rather than a firm track record, closing that gap with a "credibility transfer" strategy.
- **Founder named in materials:** Eng. Ahmed H. Suleiman.
- **Tagline / core message:** "Engineering excellence, agile precision, global impact." No separate mission/vision statement appears anywhere in the source files — this tagline is the closest thing to one.
- **Markets:** Egypt (home market), UAE, KSA, wider MENA, and the EU, plus any future market approved by the firm's Partners Council. One source describes the entity as "Egypt + Sudan/Sweden-linked."
- **Agency of record:** GaaS ("Growth as a Service") is running branding, website, and social media for ConsultX.

## 2. Industry & Services

Structural engineering, water infrastructure, flood mitigation, hydraulic design, architecture, MEP, construction, and infrastructure studies. Two different service taxonomies appear across sources and should be reconciled before the sitemap is finalized:
- Wireframe filter tabs: Structural / MEP / Infrastructure / Environmental
- Company Profile Strategy's recommended grouping: Advisory & Feasibility · Design & Engineering · BIM & Digital Coordination · Approvals & Compliance · Project & Construction Management

## 3. Target Audience

- **Primary:** engineering firms, government agencies, and multilateral funding bodies; decision-makers in Egypt/UAE/KSA/MENA/EU.
- **Secondary:** contractors and developers (peer review, design, tender support); academic/research institutions.
- Purchase behavior is high-trust and relationship-driven — named experts and credentials matter more than a service list.

## 4. Tone of Voice

Professional, authoritative, clean, technical — no playful or casual treatment. Source files explicitly warn against generic copy ("a leading company providing high-quality services") in favor of specific, defensible language tied to method and outcome, and against overclaiming: no invented project values, client names, certifications, or rankings.

## 5. Site Structure

Home · Services (grid → detail pages) · Projects/Case Studies (grid → detail pages) · About · Team · Insights (blog/whitepapers) · Contact — footer with company/services/contact/social links plus privacy policy and terms.

**Projects/Case Studies needs special handling.** ConsultX has no projects under its own name yet — the delivery team's own discovery report describes this section as "pre-built... empty at launch, ready for immediate use once a contract is signed." That calls for an honest empty state, not filler standing in for real work.

## 6. CMS / Admin Requirements

Everything editable without touching code: site settings (logo, contact, social, SEO defaults), homepage sections, services, projects, team, testimonials, contact submissions, and per-page SEO. The admin dashboard should also surface a content-completeness checklist and recent inbound inquiries — both specifically called out in the delivery team's own discovery report, beyond what the build prompt itself asks for.

## 7. Language — overrides the build prompt's default

The build prompt defaults to Arabic-primary unless the files say otherwise. They do: the wireframe's navigation is English with an "AR" toggle, and the PM process-groups report specifies "a bilingual (AR/EN) public website" and calls out testing Arabic text expansion against the English layout as a real dependency. **English is primary; Arabic/RTL is a toggle**, not the base layout.

## 8. Brand Assets — real vs. placeholder

- Contact details in the creative brief (+123-456-7890, info@consultx.com) are placeholders, not real numbers.
- consultx.com is the intended domain but, per the build prompt's own task list, hasn't been purchased yet.
- Onboarding materials ask founders for a list of 15 prior projects (name, scale, structural system, budget) — that list isn't in any uploaded file.
- One readiness report asks for Professional Indemnity insurance verification to be "integrated into the website footer" — worth remembering alongside the standard copyright line.

## 9. Open Items

**Blocking — can't responsibly proceed without these:**
1. **Tech stack conflict.** The build prompt hard-codes Python/Django. But it also says the attached files should override its own defaults — and `Technology_Selection_Guide.pdf` never mentions Django. Its top pick is Next.js + Strapi + PostgreSQL; its fast-launch alternative is WordPress + Bootstrap. This decides nearly everything downstream.
2. **No real contact information supplied.** Everything available is a placeholder.
3. **No real project portfolio supplied.** The onboarding checklist calls for one; it never arrived. Filling this gap with invented case studies would misrepresent ConsultX's track record to exactly the audience — government agencies, funding bodies — least able to safely take a stated history at face value.

**Needs confirmation, doesn't block starting:**
4. **Color palette conflict** between two documents — the creative brief (navy/silver/amber-or-teal) is literally named `..._OLD_VERSION_2.pdf`; the Company Profile Strategy deck (graphite/warm white/orange) looks like the more current source. Shouldn't be assumed either way.
5. **Name spelling** varies: "ConsultX," "Consultx," "CONSULTIX," "Consultex." Standardizing on "ConsultX" (most frequent across the delivery team's own docs) pending confirmation.
6. **Timeline is inconsistent** — a 5-day full-launch schedule in one doc, "2 days" for planning only in another, and a ~3–4 week discovery-to-launch schedule in the most detailed one (PM Process Groups report).
7. `CamScanner_04-08-2026_15_11.pdf` is an Arabic internal training memo from an unrelated firm ("Hani Sahooly Engineering Consultancy," Yemen) — Yemen isn't among ConsultX's listed markets and the memo doesn't reference ConsultX. Treated as not applicable here; flag if that's wrong.

## 10. Sources Reviewed

| File | Content |
|---|---|
| `ConsultX_-_Kick-Off_Meeting.pdf` | Agency kickoff deck (GaaS): scope of work, challenges, timeframe |
| `Consulting_Website_Wireframes.pdf` | Full site wireframe + static/CMS content map |
| `consultx_launch_methodology_readiness_report.pdf` | Marketing/brand launch methodology, RACI, readiness checklist, KPIs |
| `CamScanner_04-08-2026_15_11.pdf` | Unrelated Arabic training memo (see Open Item 7) |
| `Consultx.pdf` | "Consultix" institutional framework one-pager — 5-day schedule, partner-input checklist |
| `ConsultX-Prework.pdf` | Pre-work & planning: industry research, task breakdown, approval gates |
| `ConsultX_PM_Process_Groups_Report.pdf` | PM process-groups mapping, master timeline, approval gates |
| `Technology_Selection_Guide.pdf` | Tech stack decision framework and recommendation |
| `consultx_company_profile_strategy.pdf` | Content strategy, competitive positioning, visual direction |
| `CREATIVE_BRIEF_ConsultX_Brand_Identity_OLD_VERSION_2.pdf` | Brand identity brief — flagged in its own filename as superseded |

## 11. Recommended Next Step

Settle the tech-stack question, then confirm (or consciously waive) real contact info and a project list before Phase 1 setup starts. Everything else above can be resolved in parallel without blocking the build.
