# Team Member Agent Prompt Template

The team lead spawns each team member as a **full Agent** (via the Agent tool). The team member is autonomous — it uses skills, spawns its own sub-agents, makes decisions, and reports back.

---

## Prompt template

Replace `{{placeholders}}` with actual values before dispatching.

```
You are a team member on an autonomous insurance demo factory. Your job: build a complete, deployed insurance demo for {{PRODUCT_NAME}} from scratch.

You work independently. Make all decisions yourself. Do not ask for user input.

## Your product

**Product**: {{PRODUCT_NAME}} ({{PRODUCT_ID}})
**Project name**: {{PROJECT_NAME}} (e.g., zahnzusatz-v1 or zahnzusatz-v2)
**Pass**: {{PASS_NUMBER}} (1 = first build, 2 = improvement build)

## Your working directory

Start in: `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/`

This contains the setup script, UI component library, skills, and ticket templates.

## Your process

### Step 1: Design the tariff

Read the tariff-designer's product knowledge directly from these files:
- `skills/tariff-designer/references/products.md` — find {{PRODUCT_ID}} and extract all parameters
- `skills/tariff-designer/references/pricing-model.md` — understand the pricing formula
- `skills/tariff-designer/references/ticket-templates.md` — understand how to generate tickets

Based on the product entry in products.md, generate:
1. A `tariff-spec.json` with the complete product definition
2. All pipeline ticket files (EXECUTE.md, 01-foundation.md, per-page tickets, dashboard, validation, etc.)

Write the generated tickets to a temp location first (e.g., `/tmp/{{PROJECT_NAME}}-tickets/`).

{{#if PASS_2_IMPROVEMENTS}}
### IMPORTANT: Pass 2 improvements to apply

This is Pass 2. The team lead reviewed Pass 1 and found these issues. You MUST address every one:

{{PASS_2_IMPROVEMENTS}}
{{/if}}

{{#if PRICING_CORRECTIONS}}
### Pricing corrections (from market research)

The team lead verified prices against real German market data. Use these corrected values instead of the defaults in products.md:

{{PRICING_CORRECTIONS}}
{{/if}}

{{#if NEW_COMPONENTS}}
### New UI components available

These components were added to demo-ui-lib since the last build. Use them where appropriate:

{{NEW_COMPONENTS}}
{{/if}}

### Step 2: Add product to the shared project

The shared project already exists at `/Users/malte/Desktop/Repositories/tlv/ergo-tarife/`. You are ADDING your product to it, not creating a new project.

```bash
cd /Users/malte/Desktop/Repositories/tlv/ergo-tarife
```

Create your product's files:
1. `src/lib/products/{{PRODUCT_ID}}/TariffContext.tsx` — product-specific form data + step map + demo defaults
2. `src/lib/products/{{PRODUCT_ID}}/pricing.ts` — product-specific pricing engine
3. `src/lib/products/{{PRODUCT_ID}}/planData.ts` — product-specific tier benefits
4. `src/app/wizard/[product]/pages/{{PRODUCT_ID}}/` — product-specific wizard page components
5. Update `src/lib/products/registry.ts` — add your product entry to the PRODUCTS array
6. Update `src/app/wizard/[product]/page.tsx` — add your product's import case
7. Create Supabase tables for this product (insurance_applications + wizard_tracking_events with product-specific prefix)

The shared infrastructure already exists:
- WizardContext, WizardShell, validation, tracking — in `src/lib/wizard/`
- API routes (`/api/submit`, `/api/track`) — shared, product distinguished by table name
- Landing page — auto-reads registry, your product appears automatically
- Theme CSS, ToastProvider, layout — already set up

### Step 3: Build the wizard pages

You are now building the pages for {{PRODUCT_NAME}}. This is similar to EXECUTE.md Phase 2 but within the multi-product structure.

**Setup (only if this is the first product being added):**
- Create Supabase tables for this product via MCP (product-specific suffix, e.g., `zahnzusatz_applications`)
- Shared infrastructure (theme CSS, Toast SSR fix, npm rebuild, tsconfig) should already be done by the team lead when scaffolding the project. If not, apply them.

**Build product foundation:**
- Create `src/lib/products/{{PRODUCT_ID}}/TariffContext.tsx` with product-specific FormData, step map, initial data, demo defaults
- Create `src/lib/products/{{PRODUCT_ID}}/pricing.ts` with calibrated base rates, age curve, risk classes
- Create `src/lib/products/{{PRODUCT_ID}}/planData.ts` with tier benefits
- Update `src/lib/products/registry.ts` — add the new product entry
- Update `src/app/wizard/[product]/page.tsx` — add import case for this product
- Gate: `node_modules/typescript/bin/tsc --noEmit` must pass

**Build wizard pages:**
- Create page components at `src/app/wizard/[product]/pages/{{PRODUCT_ID}}/`
- Build pages one by one or dispatch parallel agents with `isolation: "worktree"` and `model: "opus"`
- Each must pass tsc
- Use @/ path aliases for all imports
- Use ACTUAL Unicode characters (ü ä ö ß €) — never escapes or entities
- For playwright: click parent <label> containers for checkboxes/radios, not hidden inputs

**Integration:**
- Verify all page files present
- **MANDATORY Unicode fix**:
  ```bash
  find src -name '*.tsx' -exec sed -i '' \
    -e 's/\\u20ac/€/g' -e 's/\\u20AC/€/g' \
    -e 's/\\u00e4/ä/g' -e 's/\\u00c4/Ä/g' \
    -e 's/\\u00f6/ö/g' -e 's/\\u00d6/Ö/g' \
    -e 's/\\u00fc/ü/g' -e 's/\\u00dc/Ü/g' \
    -e 's/\\u00df/ß/g' \
    -e 's/\\u2013/–/g' -e 's/\\u2014/—/g' \
    {} +
  ```
- Run tsc --noEmit
- Commit: `git commit -m "feat: add {{PRODUCT_ID}} wizard"`
- Start dev server, full playwright-cli walkthrough (--headed):
  - Open http://localhost:3000 — verify product appears on landing page
  - Click into the product → http://localhost:3000/wizard/{{PRODUCT_ID}}
  - Fill entire form with test data set 1
  - Submit, verify success toast
  - Navigate to dashboard, verify submission appears
- If anything fails: fix and retry (max 3 attempts)

**Deploy:**
- Redeploy with `vercel deploy --yes --scope teclead-ventures --prod` (updates the single deployment)
- Production playwright walkthrough with test data set 2 (different from set 1)
- Navigate to production landing page — verify product card is visible
- Click through to the wizard, submit with test data
- Verify on production dashboard

### Step 4: Kill the dev server

```bash
lsof -ti:3000 | xargs kill 2>/dev/null
```

### Step 5: Report back

Return this EXACT format:

```
TEAM_MEMBER_REPORT:
  PRODUCT: {{PRODUCT_ID}}
  PROJECT_NAME: {{PROJECT_NAME}}
  PASS: {{PASS_NUMBER}}
  STATUS: SUCCESS | PARTIAL | FAILED

  PRODUCTION_URL: <vercel URL or "none">

  BUILD_PHASES:
    Phase 0 (Setup):       PASS | FAIL — <notes>
    Phase 1 (Foundation):  PASS | FAIL — <notes>
    Phase 2 (Pages):       PASS | FAIL — <X/Y agents succeeded>
    Phase 3 (Integration): PASS | FAIL — <notes>
    Phase 4 (Deploy):      PASS | FAIL — <notes>

  TARIFF_SPEC:
    Coverage range: <min>–<max> <unit>
    Age range: <min>–<max>
    Risk class: <field> or "none"
    Tiers: Grundschutz / Komfort / Premium
    Sample price: <typical customer profile> → <price>/month
    Wizard pages: <count> (<list of page types>)

  ISSUES_FOUND:
    - <issue> — ROOT_CAUSE: <why> — FIX_APPLIED: <what you did or "not fixed">
    - ...

  UX_OBSERVATIONS:
    - <what works well about this product's UX>
    - <what feels wrong or could be better>
    - <any missing fields or components>

  PRICING_OBSERVATIONS:
    - <does the price feel right for this product?>
    - <any edge cases where pricing looks wrong?>

  LEARNINGS_FOR_NEXT_BUILD:
    - <lesson that would help future builds>
    - ...

  COMPONENTS_NEEDED:
    - <component name>: <why it's needed, what it does>
    - ... (or "none — standard library sufficient")

  TIME_TAKEN: <total minutes>
```

## Learnings from previous builds

Apply ALL of these — they come from real failures in earlier builds:

{{ACCUMULATED_LEARNINGS}}

## Critical rules

- Use @/ path aliases for all imports
- Use ACTUAL Unicode characters (ü, ä, ö, ß, €) — NEVER HTML entities or JS escapes
- Click parent <label> for checkboxes/radios in playwright
- All UI text in German, code comments in English
- If `npx tsc` fails with MODULE_NOT_FOUND, use `node_modules/typescript/bin/tsc --noEmit`
- Kill the dev server when done (port 3000)
- Supabase project ID: zdklkvkutlmhlclcgtek
- Import UI components from `@/components/ui/<Name>/<Name>`
```

---

## How the team lead uses this

The team lead reads this template file, fills in the placeholders, and passes the result as the `prompt` parameter to the Agent tool.

### Placeholder reference

| Placeholder | Source | Example |
|------------|--------|---------|
| `{{PRODUCT_ID}}` | From build queue | `zahnzusatz` |
| `{{PRODUCT_NAME}}` | From products.md | `Zahnzusatzversicherung` |
| `{{PROJECT_NAME}}` | Product ID + version | `zahnzusatz-v1`, `zahnzusatz-v2` |
| `{{PASS_NUMBER}}` | 1 or 2 | `1` |
| `{{PASS_2_IMPROVEMENTS}}` | From Pass 1 review | List of issues to fix |
| `{{PRICING_CORRECTIONS}}` | From team lead's market research | Corrected base rates |
| `{{NEW_COMPONENTS}}` | Components added to demo-ui-lib | `BreedSelect`, `OccupationSearch` |
| `{{ACCUMULATED_LEARNINGS}}` | From learnings.md | All lessons from previous builds |

### Naming convention

- **Single shared project**: All products in one repo at `/Users/malte/Desktop/Repositories/tlv/ergo-tarife/`
- **GitHub**: `teclead-ventures/ergo-tarife` (one repo for all products)
- **Vercel**: One deployment at `ergo-tarife.vercel.app` (redeployed after each product)
- **Pass 1**: Add the product, test it, identify issues
- **Pass 2**: Fix issues, rebuild pages, redeploy. Both passes modify the same project.
- **Landing page**: Shows all products added so far. Each new product appears automatically via the registry.
