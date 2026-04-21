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

### Step 1: Read the product specification

Read the tariff-designer's product knowledge directly:
- `skills/tariff-designer/references/products.md` — find {{PRODUCT_ID}} and extract ALL parameters (base rates, age curve, risk classes, tiers, fields, wizard steps, validation)
- `skills/tariff-designer/references/pricing-model.md` — understand the pricing formula and how to implement pricing.ts

You do NOT generate separate ticket files. You build directly into the shared project using products.md as your specification.

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

### Step 2: Add product to the project

The project already exists at `{{PROJECT_DIR}}`. You are ADDING your product to it, not creating a new project.

```bash
cd {{PROJECT_DIR}}
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
- WizardContext, WizardShell — in `src/lib/wizard/`
- API route `/api/submit` — shared, product distinguished by table name
- ERGO content pages at `(site)/` — homepage (`/`), `/produkte`, `/produkte/zahnzusatz` — do NOT delete these
- Tariff grid at `(app)/tarife/page.tsx` — reads registry, your product appears automatically
- Theme CSS, ToastProvider, layout — already set up

You MUST also create (if not already present):
- `src/app/(app)/api/track/route.ts` — POST endpoint that writes step events to the product's `_tracking` Supabase table
- Step tracking in your wizard component — fire a POST to `/api/track` on each step change with sessionId, product, step, stepLabel

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

**Build tracking + dashboard (MANDATORY — not optional, do this before integration):**
- Create `src/app/(app)/api/track/route.ts` if it doesn't exist — POST endpoint writing to `{{TABLE_PREFIX}}_{{PRODUCT_ID}}_tracking` Supabase table
- Create Supabase table `{{TABLE_PREFIX}}_{{PRODUCT_ID}}_tracking` with columns: id (uuid), session_id (text), product (text), step (integer), step_label (text), timestamp (timestamptz), created_at (timestamptz default now())
- In your product's main wizard component, generate a `sessionId` via `crypto.randomUUID()` on mount and POST to `/api/track` on each step change (useEffect watching state.step)
- The product dashboard at `/dashboard/[product]` MUST include:
  1. **Funnel section**: for each wizard step, count distinct sessions that reached that step, render horizontal bars with conversion rates (e.g., "Für wen? — 100% → Beginn — 85% → ... → Submitted — 42%"). Read from the `_tracking` table.
  2. **Submissions table**: name, tier, price, date (read from `_applications` table)
  3. **Stats cards**: total submissions, average monthly price, most popular tier, wizard completion rate
- Tracking failures must NEVER block the wizard UX — wrap all fetch calls in .catch(() => {})
- See `tickets/13-wizard-step-tracking.md` for copy-pasteable SQL schema and route code

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
  - Open http://localhost:3000 — verify ERGO homepage loads (content page)
  - Navigate to http://localhost:3000/tarife — verify product appears in the tariff grid
  - Click into the product → http://localhost:3000/wizard/{{PRODUCT_ID}}
  - Fill entire form with test data set 1
  - Submit, verify success toast
  - Navigate to dashboard, verify:
    - Submission appears in the submissions table
    - Funnel section shows step tracking data (at least the steps you walked through should appear)
    - Stats cards show correct aggregation (1 submission, correct price, correct tier)
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
  PROJECT: ergo-tarife
  PASS: {{PASS_NUMBER}}
  STATUS: SUCCESS | PARTIAL | FAILED

  WIZARD_URL: <vercel URL>/wizard/{{PRODUCT_ID}}
  DASHBOARD_URL: <vercel URL>/dashboard/{{PRODUCT_ID}}

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
- Supabase project ID: Verify via `list_projects` MCP tool — do NOT hardcode
- Import UI components from `@/components/ui/<Name>/<Name>`
- **Content pages**: Do NOT delete the `(site)/` route group — it contains ERGO homepage and product content pages
- **Tariff grid**: Lives at `/tarife` (not `/`) — update `src/app/(app)/tarife/page.tsx` to read the product registry
- **No route conflicts**: The homepage at `/` is the ERGO content page from `(site)/`. The tariff grid at `/tarife` is in `(app)/`. They must coexist.
- **Stepper labels**: Keep labels SHORT (max 6 chars) when there are 6+ steps — e.g., "Für wen?", "Alter", "Tarif", not "Versicherung", "Geburtsdatum"
- **Supabase table prefix**: Use `{{TABLE_PREFIX}}` for table names (e.g., `{{TABLE_PREFIX}}_insurance_applications`)
- **PasswordGate**: Deployed demos use password `ergo2026` — handle this in Playwright walkthroughs

## Field validation (mandatory)

Every wizard step that collects data MUST validate before allowing the user to proceed:
- **Required fields**: Show inline German error message ("Vorname ist erforderlich") below invalid fields
- **PLZ**: Must be exactly 5 digits — show "Bitte geben Sie eine gültige Postleitzahl ein (5 Ziffern)"
- **Age range**: Validate against the product's allowed age range from products.md
- **Date fields**: Validate day (1-31), month (1-12), year (reasonable range)
- **Email/phone** (if applicable): Pattern validation with German error messages
- Validation runs on "Weiter" click — prevent navigation if validation fails
- Clear individual errors when the field is corrected (onChange)

## Demo data toggle (mandatory)

Every wizard MUST include a "Demo-Daten laden" feature so clients can see the full flow without typing:

1. Define `DEMO_DEFAULTS` in TariffContext alongside INITIAL_DATA:
```typescript
export const DEMO_DEFAULTS: TariffFormData = {
  birthDate: { day: "15", month: "06", year: "1990" },
  plan: "komfort",
  salutation: "Herr",
  firstName: "Max",
  lastName: "Mustermann",
  street: "Musterstraße 1",
  zip: "40213",
  city: "Düsseldorf",
  // ... product-specific fields with realistic values
};
```

2. Add a button in the DemoBanner or as a floating action button that calls:
```typescript
dispatch({ type: "SET_FIELDS", fields: DEMO_DEFAULTS });
```

3. The button should be visually distinct (e.g., small pill button in the demo banner area) and labeled "Demo-Daten laden". It should be toggleable — clicking again resets to empty INITIAL_DATA.
```

---

## How the team lead uses this

The team lead reads this template file, fills in the placeholders, and passes the result as the `prompt` parameter to the Agent tool.

### Placeholder reference

| Placeholder | Source | Example |
|------------|--------|---------|
| `{{PRODUCT_ID}}` | From build queue | `zahnzusatz` |
| `{{PRODUCT_NAME}}` | From products.md | `Zahnzusatzversicherung` |
| `{{PROJECT_NAME}}` | User-provided or default | `tlv-ergo-tarriffs`, `ergo-tarife` |
| `{{PROJECT_DIR}}` | Computed from PROJECT_NAME | `/Users/malte/Desktop/Repositories/tlv/tlv-ergo-tarriffs` |
| `{{TABLE_PREFIX}}` | From setup-demo.sh output | `run_20260420_1929` |
| `{{PASS_NUMBER}}` | 1 or 2 | `1` |
| `{{PASS_2_IMPROVEMENTS}}` | From Pass 1 review | List of issues to fix |
| `{{PRICING_CORRECTIONS}}` | From team lead's market research | Corrected base rates |
| `{{NEW_COMPONENTS}}` | Components added to demo-ui-lib | `BreedSelect`, `OccupationSearch` |
| `{{ACCUMULATED_LEARNINGS}}` | From learnings.md | All lessons from previous builds |

### Naming convention

- **Project directory**: `/Users/malte/Desktop/Repositories/tlv/{{PROJECT_NAME}}/`
- **GitHub**: `teclead-ventures/{{PROJECT_NAME}}`
- **Vercel**: Deployed at `{{PROJECT_NAME}}.vercel.app` (redeployed after each product)
- **Pass 1**: Add the product, test it, identify issues
- **Pass 2**: Apply targeted fixes to specific files. Do NOT rewrite files that don't need changes.
- **Landing page**: Must be German and product-specific (NEVER leave the generic English template).
