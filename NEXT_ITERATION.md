# Next Iteration Planning

These are ideas to execute AFTER the current demo-factory run completes. Do NOT act on these during the ongoing factory session.

---

## 1. Consolidated Showcase App

Instead of 14+ separate repos/Vercel projects, build ONE repository with all insurance products. A single hosted app with a menu where the client can switch between tariffs. This is the final deliverable — one URL, all products.

- Landing page with product grid (cards for each insurance type)
- Clicking a card opens that product's wizard
- Shared dashboard across all products (or per-product dashboard tabs)
- Single Vercel deployment, single GitHub repo

---

## 2. Reverse-Engineer ERGO's Actual Forms

Send a swarm of agent teams to crawl ERGO's real online tariff wizards:
- Click through each product on ergo.de
- Document every field, every step, every option
- Reverse-engineer their pricing logic (enter different ages/coverages, record prices, fit curves)
- Compare their actual flow to our generated flow
- Identify gaps: fields we're missing, steps we have wrong, pricing discrepancies

Feed findings back into the tariff-designer skill's products.md to make our defaults match reality.

---

## 3. Pricing Logic Documentation

Create a visual, client-reviewable document explaining the pricing engine for each product:
- How the formula works (with examples)
- What each parameter means in plain German
- Comparison table: our calculated prices vs real market prices
- Interactive pricing explorer (input age/coverage, see how price builds up)

Purpose: the client can send this to their actuaries/employees to validate our model before presenting.

---

## 4. Security Review

Audit all generated demos for:
- Input validation (XSS, injection)
- Supabase RLS policies
- API route protection
- Client-side data exposure (env vars, keys)
- GDPR compliance of form data handling

---

## 5. Full Work Analysis & Visualization

Build a comprehensive analysis of the entire project for the client presentation:

### Data to collect:
- **Claude Code sessions**: Number of sessions, total tokens consumed, duration per session
- **GitHub metrics**: Total commits across all repos, lines of code generated, lines accepted, PRs created
- **Build metrics**: Number of demos built, success rate, average build time, total build time
- **Cost analysis**: Token costs, compute time, developer time saved estimate
- **Iteration metrics**: How many v1→v2 improvements, what percentage of v1 issues were fixed in v2

### Sources:
- Claude Code session history / conversation logs
- `gh` CLI for GitHub stats across all teclead-ventures repos
- `demo-builds/manifest.json` for factory metrics
- `tickets/feedback-log.md` for iteration history
- Vercel deployment logs for deploy metrics

### Visualization:
- Timeline of the entire project (from first session to final deployment)
- Sankey diagram: effort flow from design → tickets → build → deploy
- Bar chart: time per product (v1 vs v2)
- Token usage breakdown by phase
- Code generation stats: total lines written, by language (TSX, TS, CSS, MD)
- The "thought process" narrative: what decisions were made and why

### Format:
- Interactive web page (could be a Next.js app itself)
- Or a polished PDF/presentation
- Must be client-facing — professional, visual, explainable

---

## 6. Unicode Escape Bug — STILL NOT FIXED

The `\u20ac` / `\u00e4` problem persists. Spotted in the Reise v1 build (screenshot evidence):
- Heading: "W\u00e4hlen Sie Ihren Reiseschutz" instead of "Wählen Sie Ihren Reiseschutz"
- Price: "14,15 \u20ac" instead of "14,15 €"
- Also: "5.000 \u20ac" in the subtitle

This has been documented in learnings since run 2 but agents STILL do it. The instruction "use actual Unicode characters" is not strong enough. Possible fixes:
- Add a post-build grep check: `grep -r '\\u20' src/` — if found, auto-replace before deploy
- Add a git pre-commit hook that rejects `\u00` patterns in .tsx files
- Add an explicit find-and-replace step in Phase 3 integration: `sed -i '' 's/\\u20ac/€/g; s/\\u00e4/ä/g; s/\\u00f6/ö/g; s/\\u00fc/ü/g; s/\\u00df/ß/g'`
- Make it a quality gate: tsc passes → then Unicode check → then review

The sed approach is the most reliable since it doesn't rely on the agent remembering. Add it as a mandatory Phase 3 step.

---

## 7. ERGO Font Check

The current demos use `"FS Me", Arial, Helvetica, sans-serif` for body and `"Fedra Serif", Georgia, serif` for headings (from theme.css). These are the correct ERGO brand fonts, but we're falling back to system fonts since FS Me and Fedra Serif aren't loaded.

To do:
- Crawl ergo.de and check which web fonts they actually serve (WOFF2 files, @font-face rules)
- Check if they use a CDN or self-host
- Either source the fonts (if publicly available) or find the closest Google Fonts match
- Update theme.css with proper @font-face declarations or font loading
- This will significantly improve visual fidelity of all demos

---

## Execution order

1. Wait for demo-factory to complete all 14 products
2. Security review
3. Reverse-engineer ERGO forms (parallel with #4)
4. Consolidated showcase app (one repo, one URL)
5. Pricing documentation
6. Full work analysis & visualization (last — needs all data)
