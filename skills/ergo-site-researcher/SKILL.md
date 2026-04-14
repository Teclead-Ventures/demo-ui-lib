---
name: ergo-site-researcher
description: |
  Reverse-engineers ERGO's website design system and content pages. Crawls ergo.de using Firecrawl (content) and playwright-cli (visuals) to identify UI component patterns, extract styling, and document page structures. Produces a component catalog and build spec for recreating the pages. Use this skill when the user wants to clone ERGO's website, recreate their pages, extract their UI components, analyze their design system, or says "clone the ERGO site", "recreate their pages", "extract their UI", "rebuild ergo.de". NOT for tariff pricing research — use ergo-researcher for that.
---

# ERGO Site Researcher

You reverse-engineer ERGO's website to extract its design system, component patterns, and page content. Your output feeds into a builder skill that recreates the pages as Next.js components in the `ergo-tarife` project.

## What this produces

1. **Raw content** — every page's text, links, and structure (via Firecrawl)
2. **Visual analysis** — screenshots, computed styles, DOM structure (via playwright-cli)
3. **Component catalog** — every unique UI pattern identified, with specs and reference screenshots
4. **Build spec** — instructions for the builder skill to recreate each page

All output goes to `research/ergo-site/`. New components will eventually live at `src/components/ergo/` — separate from the existing `src/components/ui/` tariff wizard components. Ergo components CAN import from ui/ (reuse the Button, etc.) but NOT vice versa.

## Important constraints

- **Don't download images** — reference ERGO's URLs. The rebuilt pages will link to their CDN.
- **Don't modify existing ui/ components** — you can suggest making them more dynamic (adding variants) but never change their current behavior.
- **Firecrawl free tier** — stay within limits. The curated page list below is ~15-20 pages. Don't crawl beyond depth 2.
- **Same Next.js project** — the rebuilt pages go into `ergo-tarife` alongside the tariff wizards. The homepage becomes the ERGO clone, product cards link to `/wizard/<product>`.

## Prerequisites

- Firecrawl SDK: `npm install @mendable/firecrawl-js` (install in demo-ui-lib)
- Firecrawl API key: `fc-cb511026bba74923800cb349d220ba9c`
- playwright-cli available
- Working directory: `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/`

## Operating modes

### Mode A: Single-page iteration (default)
Analyze ONE page fully (crawl → visual analysis → component extraction). Present results, get feedback, refine approach. Use for the first 2-3 pages.

### Mode B: Batch
After the methodology is proven, analyze remaining pages in parallel batches.

## Your process

### Step 0: Read previous learnings

Read `tickets/feedback-log.md` and any previous `research/ergo-site/` directory. Apply all lessons.

### Step 1: Setup

Install Firecrawl in the project if not already present:

```bash
cd /Users/malte/Desktop/Repositories/tlv/demo-ui-lib
npm install @mendable/firecrawl-js
```

Ensure `FIRECRAWL_API_KEY` is set in `.env.local`:
```bash
echo 'FIRECRAWL_API_KEY=fc-cb511026bba74923800cb349d220ba9c' >> .env.local
```

Create a helper script at `scripts/firecrawl-page.ts`:

```typescript
// Usage: npx tsx scripts/firecrawl-page.ts <url> <output-path>
import Firecrawl from '@mendable/firecrawl-js';
import { writeFileSync, mkdirSync, appendFileSync, readFileSync } from 'fs';
import { dirname } from 'path';
import { config } from 'dotenv';

config({ path: '.env.local' });

const apiKey = process.env.FIRECRAWL_API_KEY;
if (!apiKey) { console.error("Set FIRECRAWL_API_KEY in .env.local"); process.exit(1); }

const app = new Firecrawl({ apiKey });
const url = process.argv[2];
const outputPath = process.argv[3];

if (!url || !outputPath) { console.error("Usage: npx tsx scripts/firecrawl-page.ts <url> <output-path>"); process.exit(1); }

// Budget check: warn if >20 scrapes this month
const usageLog = 'research/ergo-site/firecrawl-usage.log';
try {
  const lines = readFileSync(usageLog, 'utf-8').split('\n').filter(Boolean);
  if (lines.length >= 20) {
    console.warn(`WARNING: ${lines.length} Firecrawl scrapes already logged. Free tier is ~500/month.`);
  }
} catch {}

const result = await app.scrapeUrl(url, { formats: ['markdown', 'html'] });

if (!result.success) {
  console.error(`Firecrawl error for ${url}:`, result.error || 'unknown error');
  process.exit(1);
}

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath + '.md', result.data?.markdown || '');
writeFileSync(outputPath + '.html', result.data?.html || '');
writeFileSync(outputPath + '.json', JSON.stringify(result.data, null, 2));

// Log usage
mkdirSync('research/ergo-site', { recursive: true });
appendFileSync(usageLog, `${new Date().toISOString()} ${url} SUCCESS\n`);

console.log(`Saved: ${outputPath}.md, .html, .json (${result.data?.markdown?.length || 0} chars)`);
```

### Step 2: Analyze pages (Firecrawl + playwright per page)

In **Mode A**, process one page at a time — run BOTH Firecrawl and playwright for each page before moving to the next. This way each page gets a complete analysis and you can iterate on methodology.

In **Mode B**, batch Firecrawl for all pages first (fast), then playwright analysis in parallel.

**Per-page pipeline (Mode A):**
1. Firecrawl scrape → raw content
2. Playwright visual analysis → screenshots + styles
3. Component identification → page documentation
4. Feedback loop → present to user, get input

**Firecrawl:**
```bash
npx tsx scripts/firecrawl-page.ts "<page-url>" "research/ergo-site/raw/<page-name>"
```
Wait 3 seconds between Firecrawl requests. The curated list (~15 pages) is well within the free tier.

**Playwright visual analysis:**

For each page, spawn an analysis agent. In Mode A: one at a time. In Mode B: up to 3 parallel (named sessions).

Each agent does:

#### 3a. Full-page screenshot + viewport analysis
```bash
playwright-cli -s=<page> open <url> --headed
playwright-cli -s=<page> resize 1440 900
playwright-cli -s=<page> eval "await new Promise(r => setTimeout(r, 3000))"  # wait for load
playwright-cli -s=<page> screenshot --filename=research/ergo-site/pages/<page>/full-page.png
```

#### 3b. Cookie consent + lazy loading
Before analysis:
```bash
playwright-cli -s=<page> snapshot
# Find and click cookie consent ("Alle akzeptieren" or similar)
playwright-cli -s=<page> click <accept-button-ref>
# Scroll to bottom to trigger lazy-loaded content
playwright-cli -s=<page> eval "window.scrollTo(0, document.body.scrollHeight)"
playwright-cli -s=<page> eval "await new Promise(r => setTimeout(r, 3000))"
# Scroll back to top
playwright-cli -s=<page> eval "window.scrollTo(0, 0)"
playwright-cli -s=<page> eval "await new Promise(r => setTimeout(r, 1000))"
```

#### 3c. Component identification (use the SCREENSHOT, not just the snapshot)
The full-page screenshot from 3a is the primary tool for identifying visual components. The LLM can visually identify layout sections, cards, CTAs, etc. from the PNG.

Read the screenshot, then cross-reference with:
1. The **Firecrawl HTML dump** from Step 2 (gives you the actual DOM structure, CSS class names)
2. A **playwright-cli snapshot** (gives you accessibility tree refs for interaction)

Identify:
- **Layout**: Header, Footer, Hero, Section containers, Grid layouts
- **Content**: Product cards, Feature lists, Trust badges, Testimonials, CTAs
- **Navigation**: Main nav, Mega menu, Breadcrumbs, Footer nav
- **Interactive**: Accordions, Tabs, Carousels, Modals, Search (open menus/carousels to reveal full structure)
- **Typography**: Heading styles, Body text styles, Label styles

For interactive components: trigger them to reveal hidden content:
```bash
# Open mega menu items
playwright-cli -s=<page> hover <nav-item-ref>
playwright-cli -s=<page> screenshot --filename=research/ergo-site/pages/<page>/screenshots/mega-menu.png
# Advance carousels
playwright-cli -s=<page> click <carousel-next-ref>
```

#### 3d. Style extraction per component
For each identified component, extract styles using CSS selectors (not element refs):

```bash
# Extract computed styles for a component by CSS selector
playwright-cli -s=<page> eval "(() => {
  const el = document.querySelector('.hero-banner');
  if (!el) return null;
  const s = getComputedStyle(el);
  return {
    className: el.className,
    tagName: el.tagName,
    fontSize: s.fontSize, fontWeight: s.fontWeight, fontFamily: s.fontFamily,
    color: s.color, backgroundColor: s.backgroundColor,
    padding: s.padding, margin: s.margin,
    borderRadius: s.borderRadius, boxShadow: s.boxShadow, border: s.border,
    lineHeight: s.lineHeight, display: s.display, gap: s.gap, maxWidth: s.maxWidth,
  };
})()"
```

**Important style extraction notes:**
- Computed styles are resolved values at 1440px viewport — treat as approximate reference, not exact spec
- Also extract CSS class names (`el.className`) — the builder can look up original CSS rules in the Firecrawl HTML dump
- Extract CSS custom properties (design tokens) from the page root:
  ```bash
  playwright-cli -s=<page> eval "(() => {
    const s = getComputedStyle(document.documentElement);
    const vars = {};
    for (const sheet of document.styleSheets) {
      try { for (const rule of sheet.cssRules) {
        if (rule.selectorText === ':root') {
          for (const prop of rule.style) {
            if (prop.startsWith('--')) vars[prop] = rule.style.getPropertyValue(prop).trim();
          }
        }
      }} catch {}
    }
    return vars;
  })()"
  ```
- Note which web fonts ERGO uses — the builder will need equivalent Google Fonts or fallbacks
- For responsive behavior: resize to 768px and 375px and note layout changes:
  ```bash
  playwright-cli -s=<page> resize 768 1024
  playwright-cli -s=<page> screenshot --filename=research/ergo-site/pages/<page>/screenshots/tablet.png
  playwright-cli -s=<page> resize 375 812
  playwright-cli -s=<page> screenshot --filename=research/ergo-site/pages/<page>/screenshots/mobile.png
  playwright-cli -s=<page> resize 1440 900  # restore
  ```

#### 3d. Document the page
Write `research/ergo-site/pages/<page>/structure.md`:

```markdown
# ERGO <Page Name> — Structure Analysis

**URL**: <url>
**Viewport**: 1440×900
**Analyzed**: <date>

## Layout overview
[ASCII art or description of the page layout]

## Components identified

### 1. [Component Name]
- **Location**: [where on the page]
- **Type**: [header/card/cta/form/nav/etc.]
- **Content**: [what text/images it contains]
- **Variants**: [if different instances have variations]
- **Styling**: [key CSS properties extracted]
- **Screenshot**: [path to component screenshot]
- **Reuses existing ui/ component?**: [yes — Button, or no — new ergo/ component needed]

### 2. [Component Name]
...
```

#### 3e. Per-product feedback loop (Mode A)
After analyzing each page:
1. Present findings to the user
2. Self-assess: "Did I capture all components? Are the style extractions accurate?"
3. Ask: "Anything I missed? Any components you'd classify differently?"
4. Apply methodology improvements before the next page

### Step 4: Component catalog (Phase 3)

After all pages are analyzed, spawn a catalog agent that:

1. **Reads all page analyses** — every `structure.md` and extracted styles
2. **Deduplicates** — the header appears on every page, but it's one component
3. **Groups by type**: layout, content, navigation, interactive, typography
4. **Creates specs** for each unique component

Write `research/ergo-site/components/CATALOG.md`:

```markdown
# ERGO Design System — Component Catalog

## Summary
- Total unique components: N
- Can reuse from ui/: N (Button, Link, ...)
- Need to create in ergo/: N

## Design tokens (global)
- Primary color: #8e0038 (verified: [extracted value])
- Secondary color: #bf1528
- Font family (body): [extracted]
- Font family (heading): [extracted]
- Border radius: [extracted]
- Spacing scale: [extracted]
- Shadow values: [extracted]

## Components

### ErgoHeader
- **Type**: Layout / Global
- **Pages**: All
- **Description**: Sticky header with logo, tagline, navigation, phone number
- **Variants**: Default, Scrolled (compact)
- **Reuses**: None (custom component)
- **Props**: currentPage (for active nav state)
- **Reference**: pages/homepage/screenshots/header.png
- **Styles**: [extracted CSS object]

### HeroBanner
- **Type**: Content / Landing
- **Pages**: Homepage
- **Description**: Full-width hero with background image, headline, subline, CTA
...
```

For each component, also write a detailed spec at `research/ergo-site/components/<ComponentName>/spec.md`:

```markdown
# ErgoHeader — Component Spec

## Visual reference
[screenshot path]

## HTML structure (simplified)
```html
<header>
  <div class="logo-section">
    <div class="logo">ERGO</div>
    <div class="tagline">Einfach, weil's wichtig ist.</div>
  </div>
  <nav>...</nav>
  <div class="contact">...</div>
</header>
```

## Extracted styles
[JSON of all computed CSS properties]

## Props interface (proposed)
```typescript
interface ErgoHeaderProps {
  currentPage?: string;
  variant?: "default" | "compact";
}
```

## Implementation notes
- Sticky positioning with z-50
- Logo is text (not image) — "ERGO" in #8e0038, 900 weight, 32px
- Tagline italic, same color, 13px
- Collapse to compact on scroll (reduce padding)
- Phone number section hidden on mobile
```

### Step 5: Build spec (Phase 4)

Produce `research/ergo-site/BUILD_SPEC.md` — the instructions for the builder skill:

```markdown
# ERGO Site — Build Specification

## Project structure
All new files go in the ergo-tarife Next.js project:
- `src/components/ergo/` — new ERGO website components
- `src/app/(site)/` — content pages (using route groups to separate from wizard)
- `src/app/(site)/page.tsx` — homepage (ERGO clone)
- `src/app/(site)/produkte/page.tsx` — products overview
- `src/app/(site)/produkte/[product]/page.tsx` — product detail pages
- `src/app/wizard/[product]/` — tariff wizards (already built, untouched)

## Component build order
1. Design tokens (CSS variables in theme-ergo.css)
2. ErgoHeader (used on every page)
3. ErgoFooter (used on every page)
4. Layout shell (header + footer + main content area)
5. Page-specific components (Hero, ProductCard, etc.)
6. Assemble pages

## Per-component build instructions
[One section per component from the catalog, with:
- Reference screenshot
- Exact styles to apply
- Props interface
- Content to populate
- Which existing ui/ components to reuse]

## Per-page assembly instructions
[One section per page, with:
- Component composition (which components, in what order)
- Content from Firecrawl dumps
- Image URLs (reference ERGO CDN)
- Links: product cards → /wizard/<product> for tariff demos]

## Per-component responsive behavior
For each component, document at 3 breakpoints:
- **Desktop (1440px)**: [layout description]
- **Tablet (768px)**: [what changes — column collapse, hidden elements, font reduction]
- **Mobile (375px)**: [what changes — hamburger menu, stacked cards, full-width CTAs]

## Interaction states
For interactive components (buttons, cards, nav items, accordions):
- **Hover**: [color change, shadow, underline, etc.]
- **Focus**: [outline, ring, etc.]
- **Active/Open**: [expanded state, selected state]

## Image strategy
- Reference ERGO's CDN URLs for `<img>` tags
- For CSS background images: extract the URL, reference it
- For SVG icons: extract inline if small, reference URL if large
- For the logo: use text ("ERGO") styled to match — it's not an image

## Link mapping
| ERGO URL pattern | Our URL | Notes |
|-----------------|---------|-------|
| /de/Produkte/<product> | /(site)/produkte/<product> | Content page |
| /de/Produkte/<product>/abschluss | /wizard/<product> | Tariff wizard |
| /de/Ratgeber/* | External link to ergo.de | Not recreating |
| /de/Service/* | External link to ergo.de | Not recreating |

## Validation checklist
For each rebuilt page:
1. Screenshot the rebuilt page at 1440px, 768px, 375px
2. Screenshot the real ERGO page at same widths
3. Side-by-side comparison — flag major deviations
4. All links work (especially product → wizard links)
5. Interactive elements work (menu open/close, accordion toggle, carousel)
```

### Step 6: Final feedback loop

Execute `shared/feedback-loop.md`:
- Self-assess: completeness of the catalog, accuracy of style extraction
- Present to user: "Here are the N components I found. Here's what I can reuse from ui/. Here's what needs to be new."
- Apply improvements
- Propose: "Ready for the builder skill to start? Here's the build order I recommend."

---

## Reference files

- `references/page-list.md` — Curated list of pages to crawl

## Shared contracts

- `../shared/feedback-loop.md` — Self-improvement protocol
