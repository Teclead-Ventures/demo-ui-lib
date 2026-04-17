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

**Pass 2**: Apply all improvements from Pass 1's review. Rebuild from scratch (fresh `setup-demo.sh`). The second build inherits everything the first build taught you — fixed pricing, new components in the UI library, better ticket specs.

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

### Step 2: Scaffold the shared project + initialize the manifest

Create ONE project for all products. This is the multi-product architecture:

```bash
cd /Users/malte/Desktop/Repositories/tlv/demo-ui-lib
./setup-demo.sh ergo-tarife
```

This creates `/Users/malte/Desktop/Repositories/tlv/ergo-tarife/`. Then set up the multi-product structure:

1. Create `src/lib/products/registry.ts` with an empty `PRODUCTS` array
2. Create a landing page at `src/app/page.tsx` that reads the registry and shows a product grid
3. Create the dynamic wizard route at `src/app/wizard/[product]/page.tsx`
4. Create a dashboard overview at `src/app/dashboard/page.tsx` (shows all products)
5. Create per-product dashboard route at `src/app/dashboard/[product]/page.tsx`
6. The shared infrastructure (WizardContext, WizardShell, validation, tracking, API routes) comes from the base template
7. Create GitHub repo: `gh repo create teclead-ventures/ergo-tarife --private --source=. --push`
8. Deploy the initial shell to Vercel: `vercel deploy --yes --scope teclead-ventures`

Each team member then ADDS their product to this project (doesn't create a new one).

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
    "name": "ergo-tarife",
    "local_dir": "/Users/malte/Desktop/Repositories/tlv/ergo-tarife",
    "github_repo": "teclead-ventures/ergo-tarife",
    "vercel_url": "https://ergo-tarife.vercel.app",
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
- Creates product files at `src/lib/products/<product-id>/` and `src/app/wizard/[product]/pages/<product-id>/`
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

Pass 2 works in the same project — it deletes and replaces the product's files (`src/lib/products/<product-id>/` and `src/app/wizard/[product]/pages/<product-id>/`), then rebuilds them with improvements. The registry entry is updated if needed. Other products in the project are NOT touched.

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
- **Single shared project**: All products go into `/Users/malte/Desktop/Repositories/tlv/ergo-tarife/` — ONE repo, ONE Vercel deployment, ONE URL
- **Two passes per product**: Always. No shortcuts. Pass 1 adds the product, Pass 2 improves it. Both passes work in the same project.
- **Vercel team**: Deploy to `teclead-ventures` (team_HTk74i0O8LynDSrXif5CzlCm) — use `--scope teclead-ventures`
- **Redeploy after each product**: After each product (Pass 2) is done, redeploy to Vercel so the landing page shows the new product immediately.
- **GitHub**: Single repo `teclead-ventures/ergo-tarife` — commit after each product is added.
