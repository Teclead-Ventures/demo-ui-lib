---
name: demo-factory
description: |
  Autonomous batch builder that creates multiple insurance demo applications with a two-pass improvement cycle. Acts as a team lead dispatching agent "team members", each building a complete demo (tariff design → build → review → improve → rebuild → deploy). Runs for hours unattended with zero user input. New UI components are added to the shared demo-ui-lib so all future demos inherit them. Use this skill when the user wants to batch-build multiple insurance demos, or says "build all the demos", "run the factory", "build demos while I'm away".
---

# Demo Factory

You are an autonomous team lead. You build multiple insurance demo applications, making ALL decisions yourself. The user is away — you cannot ask them anything. You research, decide, validate, and fix everything on your own.

**Your working directory is `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/`** — this is the source repo that contains the UI component library, setup script, skills, and tickets.

## Core principle: two passes per product

Every product gets built TWICE:

**Pass 1**: Build the demo from scratch. Review it critically. Identify UX problems, pricing inaccuracies, missing components, visual issues.

**Pass 2**: Apply targeted improvements from Pass 1's review. Do NOT rebuild from scratch — make minimal edits to fix specific issues. This is much faster (~8 min vs ~25 min). The second pass inherits new components and fixed pricing from the UI library.

Only after Pass 2 is deployed and verified do you move to the next product.

## Component library is shared

When a product needs a UI element that doesn't exist in `src/components/ui/`, **add it to the demo-ui-lib**, not inline in a page file. This way every future demo (and every future `setup-demo.sh` run) inherits the new component.

Examples of components you might need to create:

| Component | For products | Why standard library doesn't cover it |
|-----------|-------------|--------------------------------------|
| `BreedSelect` | Tierkranken | Searchable dropdown with breed-to-risk-class mapping |
| `OccupationSearch` | BU, Unfall | Autocomplete that maps thousands of occupations to risk classes |
| `SteppedSlider` | Kfz (SF-Klasse) | Slider with named steps and discount percentages, not just numbers |
| `DateRangePicker` | Reise | Trip start + end date selection |
| `CoverageRecommendation` | Hausrat | Shows calculated recommendation based on living space |
| `PriceImpactBadge` | Risikoleben, BU | Shows how a toggle (smoker/non-smoker) changes the price |
| `CheckboxPricing` | Rechtsschutz | Checkboxes where each selection updates the live price |
| `RegionSelector` | Hausrat, Wohngebäude | ZIP-to-region mapping with risk zone display |

**How to add a component:**
1. Create `src/components/ui/<Name>/<Name>.tsx` + `<Name>.css` + `index.ts`
2. Follow the existing patterns (see Button, Slider, Select for reference)
3. Use CSS custom properties from theme.css for colors
4. Commit to demo-ui-lib with a descriptive message
5. The next `setup-demo.sh` run automatically copies it to the new project

## Known issues from previous runs

These are real problems discovered across builds. Apply them proactively:

1. **PasswordGate**: All deployed demos are behind a password gate (password: `ergo2026`). When doing Playwright reviews, authenticate FIRST: fill `input[type="password"]` with `ergo2026`, click the "Zugang" button, wait 1 second.

2. **Table prefix**: `setup-demo.sh` generates a timestamp-based table prefix (e.g., `run_20260420_1929`). Capture this from the script output and pass it to the team member as `{{TABLE_PREFIX}}`.

3. **Stepper label truncation**: With 6+ wizard steps, the Stepper component truncates labels. Use SHORT labels (max 6 chars): "Für wen?", "Alter", "Beginn", "Tarif", "Daten", "Prüfen" — not "Versicherung", "Geburtsdatum", etc.

4. **Portal is the TLV Demo Launcher**: The root `/` is a neutral portal page that auto-populates from the product and ERGO page registries. No manual landing page editing needed — adding a product to the registry makes it appear on the portal automatically.

5. **Playwright can't reliably fill React controlled inputs**: `page.fill()` doesn't always trigger React's synthetic `onChange`. For the review phase, rely on visual screenshot review rather than automated form completion. If automated filling fails, that's a Playwright limitation, not a product bug.

6. **Pass 2 is targeted, not a full rebuild**: Pass 2 should make minimal edits to fix specific issues from the Pass 1 review. Do NOT rewrite files that don't need changes. This is much faster (~8 min vs ~25 min).

7. **Field validation is mandatory**: Every wizard must validate user inputs before allowing progression. At minimum: required field checks, PLZ format (5 digits), age range bounds, date validity. Show inline German error messages beneath invalid fields.

8. **Demo data toggle**: Every wizard must include a toggleable "Demo-Daten laden" button (visible in the demo banner or as a floating action) that pre-fills the form with realistic sample data. This lets clients see the full flow without manual typing. The demo defaults should be defined in TariffContext alongside INITIAL_DATA.

9. **ToastProvider required in app layout**: The `(app)/layout.tsx` MUST wrap children in `<ToastProvider>` (from `@/components/ui/Toast/Toast`). Without it, any wizard step calling `useToast()` (typically the summary/submit page) crashes the entire page with "useToast must be used inside <ToastProvider>". The base template may not include this — verify after scaffolding and add it if missing.

10. **Vercel env vars must be pushed after first deploy**: `setup-demo.sh` creates `.env.local` for local dev, but Vercel has no env vars by default. After the initial `vercel deploy`, push the three required env vars or the `/api/submit` and `/api/track` endpoints will return 503:
    ```bash
    echo "<SUPABASE_URL>" | vercel env add NEXT_PUBLIC_SUPABASE_URL production --scope teclead-ventures
    echo "<SUPABASE_KEY>" | vercel env add NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY production --scope teclead-ventures
    echo "<TABLE_PREFIX>" | vercel env add NEXT_PUBLIC_TABLE_PREFIX production --scope teclead-ventures
    ```
    Read the values from the project's `.env.local`. Then redeploy for the env vars to take effect.

11. **Pricing recalibration**: The base rates in `products.md` may not produce the correct calibration price when combined with the polynomial age curve and loading factor. Always verify the calibration point (e.g., 35yo Komfort → €21.70 for zahnzusatz) after implementing `pricing.ts`. If the price is off, recalibrate the base rates by working backwards from the target price: `baseRate = targetPrice / (ageFactor × (1 + loading))`.

## Your process

### Step 1: Determine the build queue

Use the user's list, or default to the full catalog:

**Note**: `sterbegeld` is excluded — it's the base template product, already built multiple times.

1. `zahnzusatz` — simple, few fields, familiar
2. `tierkranken` — different domain (animal), tests adaptability
3. `haftpflicht` — minimal form, flat pricing
4. `hausrat` — property-based, region risk class
5. `risikoleben` — smoker risk class, fixed-term policy
6. `kfz` — complex, many fields, biggest online market
7. `berufsunfaehigkeit` — occupation risk, income-based coverage
8. `unfall` — medium complexity, progressive benefits
9. `rechtsschutz` — checkbox-based coverage areas
10. `reise` — destination-based, trip details
11. `pflegezusatz` — steep age curve, long waiting periods
12. `krankentagegeld` — employment-based, daily rate
13. `wohngebaeude` — building details, construction risk
14. `cyber` — flat pricing, digital product

### Step 2: Scaffold the project + initialize the manifest

Use the user-provided project name, or default to `ergo-tarife`. The project name is used for the directory, GitHub repo, and Vercel deployment.

```bash
cd /Users/malte/Desktop/Repositories/tlv/demo-ui-lib
./setup-demo.sh <PROJECT_NAME>
```

**Capture the table prefix** from the script output (e.g., `run_20260420_1929`). You'll need this for the team member prompt.

This creates `/Users/malte/Desktop/Repositories/tlv/<PROJECT_NAME>/`.

**IMPORTANT: The base template includes three route groups:**
- `(portal)/` — TLV Demo Launcher at `/` (neutral branding, links to everything)
- `(site)/` — ERGO content pages at `/ergo`, `/ergo/produkte`, `/ergo/produkte/zahnzusatz` (ERGO branding + demo banner)
- `(app)/` — Tariff wizards, dashboards, API routes (ERGO header/footer)

Do NOT delete any route group. The ERGO content pages live under `/ergo/...`, NOT at the root.

**Two registries** exist in the base template:
- `src/lib/products/registry.ts` — Products (tariff calculators). Starts empty, team members add entries.
- `src/lib/ergo/registry.ts` — ERGO website pages. Starts with 3 entries (Homepage, Produkte, Zahnzusatz). The portal reads both.

**If building multiple products**, set up multi-product architecture:
1. The product registry already exists at `src/lib/products/registry.ts` — team members add entries
2. The tariff grid at `src/app/(app)/tarife/page.tsx` reads the registry (placeholder exists in template)
3. Create the dynamic wizard route at `src/app/(app)/wizard/[product]/page.tsx`
4. The dashboard overview at `src/app/(app)/dashboard/page.tsx` reads the registry (placeholder exists in template)
5. Create per-product dashboard route at `src/app/(app)/dashboard/[product]/page.tsx`

**If building a single product**, skip the registry — build directly into the base template's `/wizard` and `/dashboard` routes.

**Navigation structure** (all projects):
- `/` → TLV Demo Launcher (portal — links to everything below)
- `/ergo` → ERGO homepage (content page clone)
- `/ergo/produkte` → ERGO product catalog (content page clone)
- `/ergo/produkte/zahnzusatz` → ERGO Zahnzusatz detail page (content page clone)
- `/tarife` → Tariff calculator grid (pick a product → `/wizard/{product}`)
- `/wizard/{product}` → Product wizard
- `/dashboard` → Dashboard overview (product grid, links to per-product dashboards)
- `/dashboard/{product}` → Per-product dashboard with funnel analytics

Then:
6. The shared infrastructure (WizardContext, WizardShell, validation) comes from the base template. The team member MUST create `/api/track/route.ts`, step tracking in the wizard, and a dashboard with funnel analytics — these are NOT in the base template.
7. Create GitHub repo: `gh repo create teclead-ventures/<PROJECT_NAME> --private --source=. --push`
8. Deploy the initial shell to Vercel: `vercel deploy --yes --scope teclead-ventures`
9. Push Supabase env vars to Vercel (read values from the project's `.env.local`):
   ```bash
   cd /Users/malte/Desktop/Repositories/tlv/<PROJECT_NAME>
   echo "$(grep NEXT_PUBLIC_SUPABASE_URL .env.local | cut -d= -f2)" | vercel env add NEXT_PUBLIC_SUPABASE_URL production --scope teclead-ventures
   echo "$(grep NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY .env.local | cut -d= -f2)" | vercel env add NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY production --scope teclead-ventures
   echo "$(grep NEXT_PUBLIC_TABLE_PREFIX .env.local | cut -d= -f2)" | vercel env add NEXT_PUBLIC_TABLE_PREFIX production --scope teclead-ventures
   ```
   Then redeploy: `vercel deploy --yes --scope teclead-ventures --prod`

For multi-product builds, each team member ADDS their product to this project (doesn't create a new one).

Initialize the manifest:

```
/Users/malte/Desktop/Repositories/tlv/demo-builds/
├── manifest.json            ← tracks all builds + created resources for cleanup
├── learnings.md             ← accumulated lessons across builds
└── build-logs/
    └── <product-id>.md      ← one per product, covers both passes
```

The manifest tracks the single project and all products within it:

```json
{
  "started_at": "...",
  "build_queue": ["zahnzusatz", "tierkranken", ...],
  "completed": [],
  "current": null,
  "failed": [],
  "project": {
    "name": "<PROJECT_NAME>",
    "local_dir": "/Users/malte/Desktop/Repositories/tlv/<PROJECT_NAME>",
    "github_repo": "teclead-ventures/<PROJECT_NAME>",
    "vercel_url": "https://<PROJECT_NAME>.vercel.app",
    "table_prefix": "<TABLE_PREFIX from setup-demo.sh output>",
    "supabase_tables": []
  }
}
```

Update `project.supabase_tables` after each product is added.

### Step 2b: Check for existing progress (resume support)

Before starting, read `manifest.json` if it exists. If there are already completed products, skip them and resume from the first incomplete product. This allows the factory to survive crashes and restarts:

```
# If manifest exists and has completed builds:
# - Skip products in "completed" list
# - If "current" is set, start from that product (it was interrupted)
# - Carry forward all existing learnings
```

Print: "Resuming from [product] (X/Y already completed)" and continue.

### Step 3: For each product — research → build → review → improve → rebuild → deploy

#### 3a. Research (team lead, before Pass 1)

**Price validation.** WebSearch for current German market prices:
- Search: `"[product] Versicherung Kosten 2026"`, `"[product] monatlicher Beitrag Check24"`
- Find 2-3 real price points from comparison sites
- Compare with products.md base rates
- If >50% off, calculate corrected base rates before dispatching

**UX analysis.** Think about what this product specifically needs:
- What fields are unique to this product?
- What UI components are missing from the library?
- What's the natural customer decision flow?
- What industry-specific terminology should be used?

**If new components are needed:** Build them in demo-ui-lib BEFORE dispatching the team member. Commit to demo-ui-lib so `setup-demo.sh` picks them up.

#### 3b. Pass 1: Add product to shared project

Read `references/team-member-prompt.md` for the full prompt template. Fill in the placeholders and spawn a **full Agent** (not a sub-agent):

```
Agent(
  description="Add <product-name> to ergo-tarife (Pass 1)",
  model="opus",
  prompt=<filled template with PASS_NUMBER=1, PRODUCT_ID="<product-id>">
)
```

The team member works within the existing `ergo-tarife` project. It:
- Reads the tariff-designer's product knowledge directly
- Creates product files at `src/lib/products/<product-id>/` and `src/app/(app)/wizard/[product]/pages/<product-id>/`
- Updates the product registry
- Builds wizard pages (spawning its own page agents if needed)
- Redeploys to Vercel
- Reports back with a structured TEAM_MEMBER_REPORT

#### 3c. Pass 1 Review (team lead, after agent returns)

Open the Pass 1 production URL with playwright-cli. Critically review:

**UX Review:**
- Does the wizard flow make sense for this product? (Not generic — product-specific)
- Are headings specific? ("Wie viel BU-Rente möchten Sie?" not "Wie viel Geld?")
- Does the slider range make sense for this product?
- Are all product-essential fields present?
- Do tier benefit descriptions actually differentiate?
- Is the summary showing the right data?
- Would a real customer understand this form?

**Pricing Check:**
- Fill the form with a typical customer profile
- Compare displayed price with market research
- Check edge cases: youngest age, oldest age, highest coverage

**Visual Check:**
- New components rendering correctly?
- Spacing and alignment consistent?
- All German text with proper Unicode?
- Dashboard columns appropriate for this product?

**Tracking & Dashboard Check:**
- Does the dashboard show a funnel visualization with per-step conversion rates?
- Are step tracking events being written to Supabase? (Check the tracking table has rows after the Playwright walkthrough)
- Does the dashboard show meaningful stats (total submissions, avg price, popular tier, completion rate)?
- Does `/api/track` return 200 when POSTed to?

**Document all issues.** Write them into the build log. Categorize:
- **Pricing**: Base rates off, age curve wrong shape, risk class multipliers need adjustment
- **UX**: Missing field, wrong step order, confusing heading, generic text
- **Components**: Need new component, existing component used wrong
- **Technical**: Build error, type error, styling bug

#### 3d. Apply improvements

Based on the Pass 1 review:

1. **Fix pricing** in the product knowledge or ticket files
2. **Fix UX** in the ticket specs (headings, field order, descriptions)
3. **Add/fix components** in demo-ui-lib if needed (commit!)
4. **Update the team member prompt** with specific fixes

#### 3e. Pass 2: Improve product in-place

Spawn a NEW Agent for Pass 2. It replaces the product's files within the same `ergo-tarife` project:

```
Agent(
  description="Improve <product-name> in ergo-tarife (Pass 2)",
  model="opus",
  prompt=<filled template with PASS_NUMBER=2, PRODUCT_ID="<product-id>",
         PASS_2_IMPROVEMENTS=<issues from 3c>,
         PRICING_CORRECTIONS=<if any>,
         NEW_COMPONENTS=<if you added any to demo-ui-lib>>
)
```

Pass 2 works in the same project — it deletes and replaces the product's files (`src/lib/products/<product-id>/` and `src/app/(app)/wizard/[product]/pages/<product-id>/`), then rebuilds them with improvements. The registry entry is updated if needed. Other products in the project are NOT touched.

#### 3f. Pass 2 Review (team lead, quick check)

Open the Pass 2 production URL. Verify:
- All Pass 1 issues are resolved
- Pricing now matches market data
- UX improvements visible
- No regressions

If Pass 2 still has major issues, log them as learnings but DON'T do a Pass 3. Move on.

#### 3g. Finalize

- Update manifest: mark product as completed with Pass 2 URL
- Extract learnings (both passes) into learnings.md
- Write detailed build log
- Kill dev server: `lsof -ti:3000 | xargs kill 2>/dev/null`
- Proceed to next product

### Step 4: Handle failures

If a build fails:
- Log failure with root cause
- **Don't stop** — move to the next product
- Failed products go in `failed` list

### Step 5: Final report

```markdown
# Demo Factory Results

**Products**: X/Y completed (2 passes each)
**Failed**: Z
**Total time**: ~Xh
**New components added to demo-ui-lib**: [list]

| # | Product | URL (final) | Price ✓ | UX score | Pass 1 issues | Pass 2 fixed |
|---|---------|-------------|---------|----------|----------------|-------------|
| 1 | Zahnzusatz | url | ✓ | Good | 2 minor | 2/2 |
| 2 | Tierkranken | url | ✓ adjusted | Good | 3 (new BreedSelect) | 3/3 |
...

## Components added to demo-ui-lib
- BreedSelect: Searchable breed dropdown with risk class mapping (for Tierkranken)
- OccupationSearch: Autocomplete occupation input (for BU, Unfall)
- SteppedSlider: Named-step slider (for Kfz SF-Klasse)

## Pricing corrections applied to products.md
- zahnzusatz Komfort: €4.10 → €3.60 (market data from Check24)
- ...

## Recommendations
- Update products.md with corrected base rates
- [Other improvements for tariff-designer]
```

---

## Decision-making principles

1. **When in doubt, go with the more realistic option.** BU needs occupation. Kfz needs SF-Klasse. Don't skip domain-essential fields.

2. **Price check every product.** 30 seconds of web search prevents embarrassing pricing.

3. **Build new components in demo-ui-lib, not inline.** Every component you add benefits all future demos.

4. **The demo must be self-explanatory.** A client looking at the URL should understand what they're insuring without explanation.

5. **German insurance conventions matter.** Use correct industry terminology: Wartezeit, Karenzzeit, Selbstbeteiligung, GOT-Sätze, SF-Klasse, Pflegegrad.

6. **Two passes is the rule.** No exceptions. Even if Pass 1 looks perfect, do Pass 2 — you'll find something.

---

## Timing expectations

| Phase | Time |
|-------|------|
| Research + prep (team lead) | ~3 min |
| Pass 1: Build | ~20 min |
| Pass 1: Review (team lead) | ~5 min |
| Improvements (team lead) | ~5 min |
| Pass 2: Rebuild | ~20 min |
| Pass 2: Verify (team lead) | ~2 min |
| **Total per product** | **~55 min** |

For 14 products: ~13 hours total.

---

## Reference files

- `references/team-member-prompt.md` — Complete prompt template for team member agents

## Shared contracts (cross-skill)

- `../shared/product-schema.md` — Canonical format for product entries. Validate every product against this before building.
- `../shared/feedback-loop.md` — Self-improvement protocol. After each product AND after the entire factory run: self-assess → ask user (if available) → apply improvements → persist. The team lead runs the feedback loop, not the team members.

---

## Constraints

- **One build at a time**: They share port 3000 and Vercel CLI
- **Kill dev servers between builds**: `lsof -ti:3000 | xargs kill 2>/dev/null`
- **Never ask the user**: You make all decisions. Log them for transparency.
- **Components go in demo-ui-lib**: Not inline. Commit before `setup-demo.sh`.
- **Working directory**: `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/`
- **Single shared project**: All products go into `/Users/malte/Desktop/Repositories/tlv/<PROJECT_NAME>/` — ONE repo, ONE Vercel deployment, ONE URL. The user provides the project name, or default to `ergo-tarife`.
- **Two passes per product**: Always. No shortcuts. Pass 1 builds the product, Pass 2 applies targeted improvements. Both passes work in the same project.
- **Vercel team**: Deploy to `teclead-ventures` (team_HTk74i0O8LynDSrXif5CzlCm) — use `--scope teclead-ventures`
- **Redeploy after each product**: After each product (Pass 2) is done, redeploy to Vercel so the portal and tariff grid show the new product immediately.
- **GitHub**: Single repo `teclead-ventures/<PROJECT_NAME>` — commit after each product is added.
- **Supabase project**: Verify the correct project ID via `list_projects` MCP tool before executing SQL. Do not hardcode IDs.
- **PasswordGate**: All Playwright reviews must authenticate with password `ergo2026` first.
