# Ticket Generation Templates

After producing the `tariff-spec.json`, generate the full set of ticket files the demo pipeline needs. Each ticket is a markdown file following the patterns below.

## Single-product vs multi-product mode

The pipeline supports two modes:

**Single-product mode** (new repo): Used when starting fresh. One product, one repo.
**Multi-product mode** (existing repo): Used when adding a product to an existing project. Multiple products share one repo with a landing page to switch between them.

The tariff-designer detects which mode based on whether the target directory already has products. The demo-factory always uses multi-product mode (one repo for the entire run).

### Multi-product file structure

```
src/
├── app/
│   ├── page.tsx                          ← Landing page: product grid with cards
│   ├── wizard/
│   │   └── [product]/                    ← Dynamic route: /wizard/zahnzusatz, /wizard/kfz
│   │       ├── page.tsx                  ← Dynamic wizard shell (loads product config + pages)
│   │       └── pages/
│   │           ├── zahnzusatz/           ← Each product gets its own subdirectory
│   │           │   ├── BirthDatePage.tsx
│   │           │   ├── PlanSelectionPage.tsx
│   │           │   └── ...
│   │           ├── kfz/
│   │           │   ├── VehiclePage.tsx
│   │           │   └── ...
│   │           └── ...
│   ├── dashboard/
│   │   ├── page.tsx                      ← Overview dashboard (all products combined)
│   │   └── [product]/
│   │       └── page.tsx                  ← Per-product dashboard
│   └── api/
│       ├── submit/route.ts               ← Shared, product field in request body
│       └── track/route.ts                ← Shared, wizard_name field distinguishes products
├── lib/
│   ├── products/
│   │   ├── registry.ts                   ← Product registry: maps ID → config
│   │   ├── zahnzusatz/
│   │   │   ├── TariffContext.tsx          ← Product-specific context + form data
│   │   │   ├── pricing.ts                ← Product-specific pricing engine
│   │   │   └── planData.ts               ← Product-specific tier benefits
│   │   ├── kfz/
│   │   │   ├── TariffContext.tsx
│   │   │   ├── pricing.ts
│   │   │   └── planData.ts
│   │   └── ...
│   ├── wizard/                           ← Shared wizard infrastructure (unchanged)
│   │   ├── WizardContext.tsx
│   │   ├── WizardShell.tsx
│   │   ├── WizardTrackingProvider.tsx
│   │   └── validation.ts
│   └── supabase.ts
```

### Product registry (`src/lib/products/registry.ts`)

```typescript
export interface ProductEntry {
  id: string;
  name: string;
  shortName: string;
  description: string;
  icon: string;          // Emoji or SVG identifier for the landing page card
  category: string;
  tableSuffix: string;
  wizardSteps: Array<{ label: string }>;
  enabled: boolean;
}

export const PRODUCTS: ProductEntry[] = [
  {
    id: "zahnzusatz",
    name: "Zahnzusatzversicherung",
    shortName: "Zahnzusatz",
    description: "Schutz für Zahnbehandlung, Zahnersatz und Kieferorthopädie",
    icon: "🦷",
    category: "Gesundheit",
    tableSuffix: "zahnzusatz_applications",
    wizardSteps: [{ label: "Versicherte Person" }, { label: "Geburtsdatum" }, { label: "Versicherungsbeginn" }, { label: "Tarifauswahl" }, { label: "Persönliches" }, { label: "Zusammenfassung" }],
    enabled: true,
  },
  // ... more products added as they're built
];

export function getProduct(id: string): ProductEntry | undefined {
  return PRODUCTS.find(p => p.id === id);
}
```

### Landing page (`src/app/page.tsx`)

Reads the product registry and renders a grid of clickable cards. Each card links to `/wizard/<product-id>`. Cards show: icon, product name, short description, category badge.

### Adding a product to an existing multi-product project

When a team member adds a new product:
1. Create `src/lib/products/<product-id>/` with TariffContext, pricing, planData
2. Create `src/app/wizard/[product]/pages/` with page components (in a product-specific subdirectory)
3. **Update `registry.ts`** — add the new product entry
4. Create product-specific Supabase tables
5. The landing page automatically shows the new product (reads registry)
6. The shared `/api/submit` and `/api/track` routes already work (product distinguished by table name / wizard_name)

### Dynamic wizard route (`src/app/wizard/[product]/page.tsx`)

```tsx
"use client";
import { use } from "react";
import { getProduct } from "@/lib/products/registry";
import { notFound } from "next/navigation";

export default function ProductWizardPage({ params }: { params: Promise<{ product: string }> }) {
  const { product } = use(params);
  const productEntry = getProduct(product);
  if (!productEntry) notFound();

  // Dynamically import the product's TariffContext and pages
  // Each product has its own TariffProvider, step map, and page components
  // ...
}
```

### Dynamic imports pattern

Each product exports a `productConfig` from its directory that contains everything the wizard page needs:

```typescript
// src/lib/products/zahnzusatz/index.ts
export { TariffProvider, TARIFF_STEPS, TARIFF_STEP_MAP, DEMO_DEFAULTS } from "./TariffContext";
export { default as renderPage } from "./renderPage";
// renderPage is a function: (step: number, subStep: number) => ReactNode
```

The wizard page uses dynamic `import()`:

```tsx
// src/app/wizard/[product]/page.tsx
"use client";
import { use, lazy, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { getProduct } from "@/lib/products/registry";
import { notFound } from "next/navigation";
import { WizardShell } from "@/lib/wizard/WizardShell";
import { WizardTrackingProvider } from "@/lib/wizard/WizardTrackingProvider";
import { ToastProvider } from "@/components/ui/Toast/Toast";
import { Stepper } from "@/components/ui/Stepper/Stepper";

// Product configs loaded dynamically — add new import lines as products are added
const PRODUCT_CONFIGS: Record<string, () => Promise<any>> = {
  zahnzusatz: () => import("@/lib/products/zahnzusatz"),
  kfz: () => import("@/lib/products/kfz"),
  // ... team members add their product here
};
```

Each team member adds ONE line to this map. This is simpler than a giant switch/case and each line is independent.

### Submit API routing (multi-product)

The submit API accepts a `product` field and uses the registry to determine the table:

```typescript
// src/app/api/submit/route.ts
import { supabase, isSupabaseConfigured, tableName } from "@/lib/supabase";
import { PRODUCTS } from "@/lib/products/registry";

export async function POST(request: Request) {
  const body = await request.json();
  const { product, ...data } = body;

  // Look up table suffix from registry
  const entry = PRODUCTS.find(p => p.id === product);
  const table = entry ? tableName(entry.tableSuffix) : tableName("applications");

  const { error } = await supabase.from(table).insert([data]);
  // ...
}
```

Each product's summary page sends `{ product: "<product-id>", ...formData }` in the POST body.

### Dashboard per-product routing

```typescript
// src/app/dashboard/[product]/page.tsx
// Reads the product ID from params, looks up tableSuffix from registry, queries that table
// Each product's dashboard knows its own column names from the registry or product config
```

### Type safety strategy

The submit API does NOT type-check the payload — it passes through to Supabase as `Record<string, unknown>`. Type safety is enforced at the wizard level: each product's `TariffProvider` is strongly typed with its own `TariffFormData` interface. The API is a thin pass-through.

---

## Single-product file structure (original)

When creating a brand-new repo with a single product, use the flat structure (no `[product]` dynamic route, no registry). This is simpler and matches the existing pipeline:

The pipeline expects these files in a `tickets/` directory:
```
tickets/
├── EXECUTE.md              ← orchestration (template, product name swapped)
├── 00-orchestration.md     ← reference overview
├── 01-foundation.md        ← TariffContext, pricing, validation, tracking
├── 02-page-1a-*.md         ← first wizard page
├── 03-page-1b-*.md         ← second wizard page
├── ...                     ← one ticket per wizard sub-step
├── 08-page-4-summary.md    ← always the summary page (last step)
├── 09-integration-e2e.md   ← integration test data
├── 10-dashboard.md         ← dashboard page
├── 11-dashboard-styling.md ← dashboard styling spec
├── 12-form-validations.md  ← validation rules
├── 13-wizard-step-tracking.md ← tracking infrastructure
├── agent-contracts.md      ← subagent role definitions (unchanged)
├── quality-gates.md        ← gate sequence (unchanged)
└── feedback-log.md         ← empty, populated after runs
```

## Numbering convention

Page tickets are numbered sequentially: `02` through `08` (max 7 pages). The number maps to the agent dispatch table in EXECUTE.md. The step/substep in the filename reflects the wizard position:

- `02-page-1a-*` → Step 1, Sub-step 1 (Agent A)
- `03-page-1b-*` → Step 1, Sub-step 2 (Agent B)
- `04-page-1c-*` → Step 1, Sub-step 3 (Agent C)
- `05-page-2a-*` → Step 2, Sub-step 1 (Agent D)
- `06-page-2b-*` → Step 2, Sub-step 2 (Agent E)
- `07-page-3-*`  → Step 3, Sub-step 1 (Agent F)
- `08-page-4-summary` → Step 4, Sub-step 1 (Agent G) — always summary

If a product has fewer steps (e.g., 5 pages instead of 7), use fewer tickets. The step map in the foundation adjusts accordingly.

---

## Template: Foundation Ticket (01-foundation.md)

Generate this from the tariff spec. The key product-specific parts are marked with `{{placeholders}}`.

```markdown
# Ticket 01: Foundation — Wizard Shell, State & Navigation

## Priority: BLOCKING — Must complete before all other tickets

## Objective

Create the multi-step wizard infrastructure for {{product.name}} ({{product.shortName}}).

## Files to Create

### Product files location

**Single-product mode**: `src/lib/wizard/TariffContext.tsx`, `src/lib/data/pricing.ts`, `src/lib/data/planData.ts`
**Multi-product mode**: `src/lib/products/{{product.id}}/TariffContext.tsx`, `src/lib/products/{{product.id}}/pricing.ts`, `src/lib/products/{{product.id}}/planData.ts`

### TariffContext

```typescript
export interface TariffFormData {
  {{#each fields}}
  {{id}}: {{tsType}};
  {{/each}}
}

const INITIAL_DATA: TariffFormData = {
  {{#each fields}}
  {{id}}: {{defaultValueTS}},
  {{/each}}
};

// Demo mode: pre-filled values for click-through presentations
// Activated via ?demo=true URL parameter
const DEMO_DEFAULTS: TariffFormData = {
  {{#each demoDefaults}}
  {{key}}: {{value}},
  {{/each}}
};

export const TARIFF_STEP_MAP: StepMap = { {{stepMap}} };

export const TARIFF_STEPS = [
  {{#each wizardSteps}}
  { label: "{{label}}" },
  {{/each}}
];
```

### `src/lib/data/pricing.ts`

```typescript
const BASE_RATES = {
  grundschutz: {{pricing.baseRates.grundschutz}},
  komfort: {{pricing.baseRates.komfort}},
  premium: {{pricing.baseRates.premium}},
};

const AGE_CURVE = {
  base: {{pricing.ageCurve.base}},
  linear: {{pricing.ageCurve.linear}},
  quadratic: {{pricing.ageCurve.quadratic}},
};

const MIN_AGE = {{target.ageRange[0]}};
const MAX_AGE = {{target.ageRange[1]}};
const COVERAGE_UNIT = {{pricing.coverageUnit}};
const LOADING = {{pricing.loading}};

{{#if pricing.riskClass}}
const RISK_CLASSES: Record<string, number> = {
  {{#each pricing.riskClass.classes}}
  "{{id}}": {{multiplier}},
  {{/each}}
};
{{/if}}
```

### `src/lib/data/planData.ts`

Plan benefit descriptions for each tier — copy directly from the tariff spec `plans` section.

### Other foundation files

Same as the existing pipeline:
- `src/lib/wizard/validation.ts` — generic validation utility (unchanged)
- `src/lib/wizard/WizardTrackingProvider.tsx` — step tracking (unchanged)
- `src/app/api/track/route.ts` — tracking API (unchanged)
- `src/app/api/submit/route.ts` — submission API (table name from spec)
- `src/app/wizard/page.tsx` — providers + page routing + demo mode detection
- `src/app/wizard/pages/index.ts` — barrel exports
- `src/app/globals.css` — theme CSS import

### Demo mode implementation

**Single-product**: `src/app/wizard/page.tsx` reads `?demo=true` and passes to `TariffProvider`.
**Multi-product**: `src/app/wizard/[product]/page.tsx` reads `?demo=true` and passes to the product-specific provider.

```tsx
// Works for both modes — the key is the TariffProvider accepting a demo prop:
export function TariffProvider({ children, demo = false }: { children: React.ReactNode; demo?: boolean }) {
  return (
    <WizardProvider<TariffFormData>
      initialData={demo ? DEMO_DEFAULTS : INITIAL_DATA}
      stepMap={TARIFF_STEP_MAP}
    >
      {children}
    </WizardProvider>
  );
}
```

Multi-product URL: `https://ergo-tarife.vercel.app/wizard/zahnzusatz?demo=true`
Single-product URL: `https://zahnzusatz-v2.vercel.app/wizard?demo=true`

When `?demo=true` is active:
- All fields pre-filled with realistic German test data from the product's DEMO_DEFAULTS
- All validations pass immediately (fields are non-empty)
- User can click "weiter" through the entire wizard without typing
- User can still edit any field to show interactivity
- Summary page has both checkboxes unchecked (must still be clicked — shows the consent step)

## Sub-step Map

```
{{#each wizardSteps}}
Step {{step}} ({{label}}): {{#each subSteps}}subStep {{@index+1}} = {{id}}{{#unless @last}}, {{/unless}}{{/each}}
{{/each}}
```
```

---

## Template: Page Tickets

Each page ticket follows the same structure. The content varies by **page type**. Identify the page type from the fields it contains.

### Page types and their UI patterns

| Page type | Primary component | When to use |
|-----------|------------------|-------------|
| **date-entry** | DateInput | Page collects a date (birth date, start date) |
| **radio-selection** | RadioButton | Page picks from 2-5 options (start date, destination, family status) |
| **slider** | Slider | Page selects a numeric range (coverage amount, daily rate) |
| **segmented-plan** | SegmentedControl + pricing | Plan selection page (always present) |
| **dynamic-choice** | Card + Button | Yes/no decision with explanation (dynamic adjustment) |
| **form** | TextInput + Select + InlineRadio | Multi-field data entry (personal data, vehicle details, pet details) |
| **summary** | Cards + Checkbox | Review + consent + submit (always the last page) |

### Universal page ticket structure

Every page ticket has these sections:

```markdown
# Ticket {{number}}: Page {{step}}{{substepLetter}} — {{pageTitle}}

## Step: {{step}} ({{stepLabel}}) | Sub-step: {{substep}}

## Reference Screenshot
`screenshots/reference/{{screenshotFile}}` (or "None available" if no reference)

## Objective
{{one-line description of what this page does}}

## Visual Specification
{{ASCII art layout matching the existing ticket style}}

## Files to Create/Modify

### `src/app/wizard/pages/{{PageName}}.tsx`
{{description of key elements, components used, state bindings}}

### `src/app/wizard/pages/index.ts` (MODIFY)
Export `{{PageName}}` for step {{step}}, sub-step {{substep}}.

## Component Usage
```tsx
{{import statements for UI components used on this page}}
```

## Interaction Logic
{{how fields bind to state, what navigation does, any calculations}}

## Styling Notes
{{inline style guidelines matching ERGO design}}

---

## Agent Execution

### Page Agent Actions
1. Read relevant UI component source files
2. Read `src/lib/wizard/TariffContext.tsx` for state shape
3. Create `src/app/wizard/pages/{{PageName}}.tsx`
4. Update `src/app/wizard/pages/index.ts`
5. Run quality gate loop (max 3 iterations)

### Tester: Navigation Sequence (playwright-cli)
```bash
playwright-cli open http://localhost:3000/wizard --headed
playwright-cli snapshot
{{navigation steps to reach this page from the beginning}}
```

### Tester: Page-Specific Checks
```
{{list of [CHECK] items specific to this page}}
```
```

---

## Page type details

### date-entry page

Used for birth date or similar date fields. Components: `DateInput`, `Button`, `Tooltip`.

Key elements:
- Heading (serif, centered)
- Optional tooltip with info about the date
- DateInput bound to a `{day, month, year}` field in state
- Hint text below (gray, small, centered)
- "weiter" button (primary, max-width 360px)
- "Zurück" link (if not the first page)
- Validation: all three parts filled, any product-specific age validation

### radio-selection page

Used when picking from a small set of options. Components: `RadioButton`, `Button`.

Key elements:
- Heading (serif, centered)
- 2-5 RadioButton options in a vertical list, card-style
- One option selected by default (usually the middle one)
- "weiter" button
- "Zurück" link

### slider page

Used for numeric ranges. Components: `Slider`, `Button`, `Tooltip`.

Key elements:
- Heading (serif, centered)
- Tooltip with explanation
- Slider with min/max/step/unit from the coverage spec
- Format labels with German locale (dots for thousands)
- Optional benefit bullets below (green checkmarks)
- "weiter" button
- "Zurück" link

### segmented-plan page (always present)

The plan selection page — most complex. Components: `SegmentedControl`, `Button`.

Key elements:
- Heading: "Wählen Sie Ihren passenden Schutz" (or product-specific)
- Guaranteed sum display (coverage amount from state)
- Payment duration sub-text
- SegmentedControl: 3 tiers (Grundschutz/Komfort/Premium)
- Dynamic price display: "Sie zahlen XX,XX € monatlich"
- Benefits list with green checkmarks (from planData)
- "Alle Leistungen anzeigen" expandable section
- Details row: Zahlweise, coverage summary, payment duration
- "weiter" button (text may be "weiter zum Online-Antrag")
- "Zurück" link

Price calculation: `calculateMonthlyPrice(age, coverageAmount, plan, riskClassMultiplier)`

### dynamic-choice page

Yes/no decision page for Beitragsdynamik or similar. Components: `Button`, `Card`.

Key elements:
- Plan summary bar (selected plan + price)
- "Mehr Details zeigen" collapsible
- Heading about the choice
- Explanation card with descriptive text + "auswählen und weiter" button
- Alternative: "Ich möchte keine ..." with "weiter →" link
- "Zurück" link

Note: Not all products need this page. Include only if the spec has a dynamic adjustment option or a similar binary choice.

### form page

Multi-field data entry. Components: `TextInput`, `Select`, `InlineRadio`, `DateInput`, `Button`.

Key elements:
- Heading (serif, centered)
- Optional privacy notice or info block
- Form fields stacked vertically, gap 20px
- Field types mapped from spec: text→TextInput, select→Select, inline-radio→InlineRadio, date→DateInput
- Special layouts: side-by-side for PLZ/Ort (120px + flex)
- Validation: required fields show error on blur, "weiter" disabled until valid
- "weiter" button
- "Zurück" link

### summary page (always the last page)

Review everything and submit. Components: `Checkbox`, `Button`, `useToast`.

Key elements:
- Heading: "Zusammenfassung Ihres Antrags"
- Subtitle: "Bitte überprüfen Sie Ihre Angaben"
- One card per wizard step section, each with:
  - Section title + edit pencil (✎) → `goTo(step, 1)`
  - Key data rows (label: value format)
  - Values formatted with German locale
- Two consent checkboxes (AVB + Datenschutz)
- Submit button "Jetzt verbindlich abschließen" (disabled until both checked)
- On submit: POST to `/api/submit` with all form data (snake_case keys)
- Success toast: "Ihr Antrag wurde erfolgreich eingereicht!"
- "Zurück" link

---

## Template: EXECUTE.md

The orchestration file is largely product-independent. Replace these values:

| Placeholder | Source |
|------------|--------|
| Product name | `product.name` |
| Product short name | `product.shortName` |
| Table name | `database.tableSuffix` |
| SQL CREATE TABLE | Generated from `database.columns` |
| Number of agents | Number of wizard pages (5-8) |
| Agent dispatch table | One row per page |
| Step map | From `wizardSteps` |
| Integration test data | Realistic sample values for all fields |
| Production test data | DIFFERENT realistic sample values |

The phase structure stays the same:
- Phase 0: Setup (Supabase tables, .gitignore, theme CSS, npm rebuild, tsconfig fix)
- Phase 1: Foundation (TariffContext, pricing, planData, validation, tracking)
- Phase 2: Parallel agents (one per page)
- Phase 3: Integration (merge + playwright walkthrough)
- Phase 4: Deploy (Vercel + production walkthrough)
- Phase 5: Retrospective

### SQL table generation

From `database.columns`, generate:
```sql
CREATE TABLE IF NOT EXISTS {PREFIX}_{{database.tableSuffix}} (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  {{#each database.columns}}
  {{name}} {{type}} {{#unless nullable}}NOT NULL{{/unless}}{{#if check}} CHECK ({{check}}){{/if}},
  {{/each}}
);
```

### Integration test data

Generate two sets of realistic test data for the product:

**Set 1** (integration, localhost): A "typical" customer with middle-of-the-road options.
**Set 2** (production): A different customer profile to verify both appear on the dashboard.

Example for BU:
- Set 1: 35yo software developer, €2.000/month, Komfort, with dynamic
- Set 2: 45yo electrician, €1.500/month, Premium, without dynamic

---

## Template: Dashboard (10-dashboard.md)

Adapt the dashboard for the product's data shape:

- Stat cards: total submissions, average coverage (formatted with product unit), most popular tier
- Plan distribution bars: always 3 tiers
- Wizard funnel: unchanged (tracks steps generically)
- Submissions table columns: # | Name | Tier | Coverage | Date
  - Name: `first_name + last_name` (or `petName + ownerLastName` for pet insurance)
  - Coverage: formatted with product unit (€, €/Monat, €/Jahr)

---

## Template: Validation (12-form-validations.md)

Generate validation rules from the spec's `validation` array. Common patterns:

| Rule type | Implementation |
|-----------|---------------|
| `age-range` | `startYear - birthYear` must be within `target.ageRange` |
| `required` | Field must not be empty. Error: "Dieses Feld ist erforderlich." |
| `pattern` | Regex match. Example: ZIP = `/^\d{5}$/` |
| `min-length` | String length check |
| `custom` | Product-specific. Example: BU coverage ≤ 75% of income |

Only pages with validation rules get instructions in the validation ticket. Pages where all fields are always valid (slider, radio selection) don't need validation.

---

## Template: Static tickets (copy unchanged)

These tickets are product-independent and can be copied verbatim:

- `agent-contracts.md` — subagent role definitions
- `quality-gates.md` — gate sequence
- `13-wizard-step-tracking.md` — tracking infrastructure (table schema adapts via prefix)
- `11-dashboard-styling.md` — styling guidelines
- `feedback-log.md` — empty template

---

## Generating tickets from a tariff spec

When the user confirms the tariff spec, generate tickets in this order:

1. **Count wizard pages** from `wizardSteps` (flatten all subSteps). This determines how many page tickets (02-08) and how many parallel agents.

2. **Map each subStep to a page type** based on its fields:
   - Contains a date field → date-entry
   - Contains radio options with 2-5 choices → radio-selection
   - Contains a slider/coverage field → slider
   - Is the plan selection step → segmented-plan
   - Is a yes/no choice → dynamic-choice
   - Contains multiple text/select fields → form
   - Is the last step → summary

3. **Generate each page ticket** using the page type template + the fields/options/validation from the spec.

4. **Generate the foundation ticket** with the full TariffFormData interface, pricing constants, step map.

5. **Generate EXECUTE.md** with the agent dispatch table, SQL schema, test data.

6. **Copy static tickets** unchanged.

7. **Write tariff-spec.json** as the canonical reference.
