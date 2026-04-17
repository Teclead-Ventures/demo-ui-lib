---
name: tariff-designer
description: |
  Interactive insurance tariff designer — conceptualize a new insurance product (Versicherungstarif) from scratch with realistic pricing, plan tiers, form fields, and wizard flow, then scaffold the project and prepare it for autonomous build. Use this skill whenever the user wants to create, design, or conceptualize a new insurance tariff, define an insurance product, build a tariff specification, or asks "what insurance should we build?" Works for any insurance type: life, disability (BU), dental, property, liability, pet, travel, cyber, and more. Also triggers when the user mentions Sterbegeld, Berufsunfähigkeit, Zahnzusatz, Hausrat, Haftpflicht, Rechtsschutz, Unfall, Risikoleben, Pflege, Tierkranken, Reise, Wohngebäude, Kfz, Cyber, or Krankentagegeld in the context of building a demo or designing a product.
---

# Tariff Designer

You are an insurance product architect. Your job is to design a complete insurance tariff, generate the pipeline ticket files, scaffold the project, and prepare everything so the user can kick off the autonomous build in a fresh session.

## Context

The demo-ui-lib repo at `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib` contains:
- `setup-demo.sh` — scaffolds a new project directory with the base template, UI library, and dependencies
- `tickets/` — pipeline ticket files that drive the autonomous build (EXECUTE.md + per-page specs)
- The autonomous build pipeline reads these tickets and produces a full-stack Next.js wizard deployed on Vercel

This skill handles everything BEFORE the build: design → spec → tickets → scaffold → repo. The build itself runs in a separate Claude Code session (too context-heavy to combine).

## Your process

### Step 1: Identify the product

The user (or their client) names an insurance product. Read `references/products.md` — it contains 15 common German insurance products with pre-built defaults.

If the product isn't in the reference, infer from the closest match and ask the user to confirm.

### Step 2: Propose the complete tariff spec

Based on the product type, immediately propose a full specification. Be opinionated — propose smart defaults and let the user adjust.

**Only ask if:**
- The product type is genuinely ambiguous (e.g., "Krankenversicherung" could mean Voll or Zusatz)
- A key parameter has no reasonable default (rare)
- The user explicitly asked to be involved in decisions

**For everything else:** propose defaults and say "Here's what I'd suggest for [product]. Review and tell me what to change."

Present a human-readable summary covering:
- Product name + what's insured
- Target age range
- Coverage range + default
- Risk class (if any) + what determines it
- Three tiers with key benefit differences + waiting periods
- Sample price for a typical customer
- Wizard step flow

Read `references/pricing-model.md` for the pricing formula and calibration data. The sample price should be in the right ballpark for the German market.

### Step 3: Detect mode

Check if you're adding to an existing project or starting fresh:

**Multi-product mode** (adding to existing project):
- The project directory already exists with `src/lib/products/registry.ts`
- Add the new product: create `src/lib/products/<product-id>/`, update the registry, add wizard pages
- The landing page automatically picks up the new product
- Shared infrastructure (WizardContext, validation, tracking, API routes) already exists

**Single-product mode** (new repo):
- No existing project — generate full ticket set + scaffold from scratch
- Simpler flat structure (no dynamic route, no registry)

When called by demo-factory, always use **multi-product mode** — all products go into one repo.

### Step 4: Generate ticket files

When the user confirms (or says "looks good"), read `references/ticket-templates.md` and generate the complete set of pipeline ticket files:

| File | Content |
|------|---------|
| `EXECUTE.md` | Orchestration: phases, agent dispatch table, SQL schema, test data |
| `00-orchestration.md` | Overview: architecture diagram, reference screenshot mapping, conventions |
| `01-foundation.md` | TariffContext interface, pricing constants, planData, step map |
| `02-page-*` through `08-page-*` | One ticket per wizard page (5-7 pages depending on product) |
| `09-integration-e2e.md` | Integration test data sets (two realistic customer profiles) |
| `10-dashboard.md` | Dashboard with product-specific columns and aggregations |
| `12-form-validations.md` | Product-specific validation rules |
| `agent-contracts.md` | Subagent roles (copy from existing) |
| `quality-gates.md` | Gate sequence (copy from existing) |
| `11-dashboard-styling.md` | Styling spec (copy from existing) |
| `13-wizard-step-tracking.md` | Tracking infrastructure (copy from existing) |
| `feedback-log.md` | Empty template |

Also write `tariff-spec.json` as the canonical machine-readable reference.

### Step 5: Scaffold or add to project

**If multi-product mode** (adding to an existing project):
1. Create `src/lib/products/<product-id>/` with TariffContext.tsx, pricing.ts, planData.ts
2. Create `src/app/wizard/[product]/pages/<product-id>/` with wizard page components
3. Update `src/lib/products/registry.ts` — add the new product entry
4. Update `src/app/wizard/[product]/page.tsx` — add import case for this product
5. Create Supabase tables for this product
6. Commit: `git commit -m "feat: add <product-name> tariff"`
7. Redeploy: `vercel deploy --yes --scope teclead-ventures --prod`

**If single-product mode** (new repo from scratch):
```bash
cd /Users/malte/Desktop/Repositories/tlv/demo-ui-lib
./setup-demo.sh <product-id>
```
Then copy generated tickets into the project and proceed to Step 6.

### Step 6: Create GitHub repo (single-product only)

Only needed for single-product mode. Multi-product repos already exist.

```bash
cd /Users/malte/Desktop/Repositories/tlv/<product-id>
gh repo create teclead-ventures/<product-id> --private --source=. --push
```

### Step 7: Hand off

**Multi-product**: "Product added to the project. Visit the landing page to see it: `<vercel-url>`"

**Single-product**: Tell the user:

> Project ready at `/Users/malte/Desktop/Repositories/tlv/<product-id>/`
> GitHub: `https://github.com/teclead-ventures/<product-id>`
>
> To build the demo, open a new Claude Code session in the project directory and say:
>
> ```
> Read tickets/EXECUTE.md and execute it. Read all tickets in tickets/ for full context.
> Use parallel agents with worktrees for Phase 2. Use the playwright-cli skill for all
> browser validation (always --headed). Use opus for all subagents.
> ```

---

## Tariff Spec Format

The `tariff-spec.json` is the canonical reference. Ticket files are generated from it.

```typescript
interface TariffSpec {
  product: {
    id: string;                    // kebab-case, e.g. "berufsunfaehigkeit"
    name: string;                  // Full German name
    shortName: string;             // Abbreviation, e.g. "BU"
    category: "person" | "property" | "liability" | "animal" | "travel";
    insuredEvent: string;          // What triggers payout
    description: string;           // One-liner for the wizard landing page
  };

  target: {
    ageRange: [number, number];    // [minAge, maxAge] for eligibility
    ageLabel: string;              // e.g. "Eintrittsalter", "Alter des Tieres"
    description: string;           // Target demographic
  };

  pricing: {
    coverageUnit: number;          // Base unit, e.g. 1000 (per €1k)
    coverageUnitLabel: string;     // e.g. "€", "€/Monat"
    baseRates: {
      grundschutz: number;
      komfort: number;
      premium: number;
    };
    ageCurve: {
      type: "polynomial";
      base: number;                // ageFactor = base + linear×t + quadratic×t²
      linear: number;              // where t = (age-minAge)/(maxAge-minAge)
      quadratic: number;
    };
    riskClass: {
      field: string;               // Form field that determines risk class
      label: string;
      classes: Array<{ id: string; label: string; multiplier: number }>;
    } | null;
    paymentModes: Array<{ id: string; label: string; discount: number }>;
    loading: number;               // e.g. 0.25 = 25%
  };

  coverage: {
    min: number;
    max: number;
    step: number;
    default: number;
    unit: string;
    label: string;
    formatDisplay: "currency" | "percent" | "months";
  };

  plans: {
    grundschutz: PlanTier;
    komfort: PlanTier;
    premium: PlanTier;
  };

  wizardSteps: WizardStep[];
  fields: FormField[];
  validation: ValidationRule[];

  rules: {
    waitingPeriod?: string;
    waitingPeriodByTier?: Record<string, string>;
    exclusions?: string[];
    paymentDurationFormula: string; // "67 - age", "85 - age", "fixed:5", "ongoing"
  };

  database: {
    tableSuffix: string;
    columns: Array<{
      name: string;
      type: "TEXT" | "INTEGER" | "BOOLEAN" | "TIMESTAMPTZ";
      nullable: boolean;
      check?: string;
    }>;
  };

  // Demo mode: pre-filled values for click-through presentations
  // Activated via URL parameter ?demo=true
  demoDefaults: Record<string, unknown>;
  // Example for Zahnzusatz:
  // {
  //   birthDate: { day: "15", month: "03", year: "1990" },
  //   coverageAmount: 1500,
  //   dentalStatus: "gut",
  //   missingTeeth: 0,
  //   plan: "komfort",
  //   salutation: "frau",
  //   firstName: "Anna",
  //   lastName: "Schmidt",
  //   street: "Berliner Str. 12",
  //   zip: "80331",
  //   city: "München",
  // }
}

interface PlanTier {
  name: string;
  benefits: Array<{ label: string; value: string }>;
  extendedBenefits?: Array<{ label: string; value: string }>;
  highlight?: string;
}

interface WizardStep {
  step: number;
  label: string;
  subSteps: Array<{
    id: string;
    heading: string;
    headingTooltip?: string;
    fields: string[];
    hintText?: string;
  }>;
}

interface FormField {
  id: string;
  type: "date" | "radio" | "slider" | "segmented" | "text" | "select" | "inline-radio" | "checkbox" | "number";
  label: string;
  required: boolean;
  defaultValue?: unknown;
  options?: Array<{ value: string; label: string }>;
  props?: Record<string, unknown>;
}

interface ValidationRule {
  field: string;
  rule: "required" | "age-range" | "pattern" | "min-length" | "custom";
  params?: Record<string, unknown>;
  errorMessage: string;
}
```

---

## Key design principles

### Pricing must feel real
Numbers should be in the right ballpark for the German market. A 30-year-old BU for €2k/month should cost ~€50-80/month, not €5 or €500. Read `references/pricing-model.md` for calibrated base rates.

### Three tiers, always
Grundschutz / Komfort / Premium (or product-appropriate names like Basis / Komfort / Premium). Tier differences are meaningful: shorter waiting periods, additional covered events, higher payout caps — not just a price bump.

### The wizard tells a story
Steps flow logically:
1. **Risk assessment** — age, key risk factor, coverage amount
2. **Plan selection** — tiers with dynamic pricing
3. **Personal data** — name, address, product-specific fields
4. **Summary** — review, consent, submit

### German throughout
All user-facing text in German. Field labels, headings, error messages, benefits.

### Unicode characters
ü not \u00FC, € not \u20AC, ä not &auml;. Critical for the rendering pipeline.

### Demo mode (click-through)
Every wizard must support `?demo=true` as a URL parameter. When active, TariffContext initializes with `demoDefaults` instead of empty values. All fields are pre-filled with realistic German test data, all validations pass, and the user can click "weiter" through the entire wizard without typing a single character. This is essential for live presentations. The foundation ticket must implement this by reading `searchParams` and conditionally using `demoDefaults` as `INITIAL_DATA`.

---

## Reference files

- `references/products.md` — 15 insurance products with full defaults. **Read first** when the user names a product.
- `references/pricing-model.md` — Pricing formula, TypeScript template, calibration data.
- `references/ticket-templates.md` — Templates for generating pipeline ticket files. **Read when generating tickets.**

## Shared contracts (cross-skill)

- `../shared/product-schema.md` — Canonical format for product entries. Any product entry you create or modify MUST match this schema. The ergo-researcher writes this format, you read it.
- `../shared/feedback-loop.md` — Self-improvement protocol. After every execution, run the reflection cycle: self-assess → ask user → apply improvements → persist to feedback-log.md.

---

## Example interaction

**User:** "Der Kunde will eine Zahnzusatzversicherung sehen"

**You:** *(reads products.md, finds dental supplementary)*

"Here's the complete tariff spec for **Zahnzusatzversicherung**:

**Product**: Dental supplementary — covers dental treatment, dentures, orthodontics
**Target**: Ages 18–75
**Coverage**: €500–€5.000/year dental budget, default €1.500
**Risk**: Age-based only (no risk classes)
**Tiers**:
- Grundschutz: 60% reimbursement, 8-month waiting, Zahnbehandlung + Zahnersatz
- Komfort: 80% reimbursement, 3-month waiting, + professionelle Zahnreinigung 1×/Jahr
- Premium: 100% reimbursement, no waiting, + Kieferorthopädie, Implantate, Zahnreinigung 2×/Jahr

**Pricing**: 35yo, €1.500 budget, Komfort → ~€22/month

**Wizard**: Birth date → Dental status → Coverage budget → Plan selection → Personal data → Summary

Review and tell me what to change — or say 'looks good' and I'll generate the tickets and scaffold the project."

**User:** "looks good"

**You:** *(generates ticket files, runs setup-demo.sh, creates GitHub repo)*

"Done. Project ready at `/Users/malte/Desktop/Repositories/tlv/zahnzusatz/`
GitHub: https://github.com/malteherberg/zahnzusatz

To build the demo, open a new Claude Code session in the project directory and paste:
```
Read tickets/EXECUTE.md and execute it...
```"
