# Execute: Build Full-Stack Insurance Tariff Wizard

**Paste this into a new Claude Code session to start autonomous development.**

ultrathink

---

## Mission

Build a complete full-stack insurance tariff wizard (Sterbegeldversicherung):
- **Frontend**: Next.js app with multi-step wizard using the `demo-ui-lib` component library
- **Backend**: Supabase database storing submissions
- **Dashboard**: Analytics page showing all submissions
- **Deployment**: Vercel production URL
- **Validation**: playwright-cli browser interaction (headed, visible on desktop)

The UI component library is at `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/src/components/`.
The Next.js base template is at `/Users/malte/Desktop/Repositories/tlv/next-demo-base/`.
Reference screenshots are at `/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/screenshots/reference/`.

## Required Reading (in this order)

1. This file (`tickets/EXECUTE.md`) — orchestration flow
2. `tickets/agent-contracts.md` — EXACT return formats for all subagent roles
3. `tickets/quality-gates.md` — gate sequence, pass/fail criteria, escalation rules
4. `tickets/00-orchestration.md` — reference screenshot mapping
5. Individual ticket files — read each before dispatching

## Architecture

```
Orchestrator (you)
  │
  ├─ Phase 0: Setup (~2 min)
  │   Copy base template, copy UI lib, create Supabase table, set env vars
  │
  ├─ Phase 1: Foundation (~3 min)
  │   Wizard state, page routing, API route, plan data
  │   Gate: npx tsc --noEmit + npm run dev works
  │
  ├─ Phase 2: 8 Agents in parallel (~8 min)
  │   Each in isolated worktree, each runs:
  │     develop → compile → review(opus) → browser-test(playwright-cli) → loop
  │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
  │   │ Agent A │ │ Agent B │ │ Agent C │ │ Agent D │
  │   │BirthDate│ │StartDate│ │Coverage │ │PlanSel. │
  │   └─────────┘ └─────────┘ └─────────┘ └─────────┘
  │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
  │   │ Agent E │ │ Agent F │ │ Agent G │ │ Agent H │
  │   │Dynamic  │ │Personal │ │Summary  │ │Dashboard│
  │   └─────────┘ └─────────┘ └─────────┘ └─────────┘
  │
  ├─ Phase 3: Integration (~5 min)
  │   Merge all pages, full playwright-cli walkthrough (headed, visible)
  │   Fill entire form, submit, verify on dashboard
  │
  └─ Phase 4: Deploy + Production validation (~3 min)
      Vercel deploy via MCP, playwright-cli on production URL
```

---

## Phase 0: Setup

**If the setup script was already run** (project directory exists with tickets/ and node_modules/), skip to Step 4.

**If starting fresh**, the user should have run the setup script beforehand:
```bash
cd /Users/malte/Desktop/Repositories/tlv/demo-ui-lib
./setup-demo.sh              # creates demo-run-YYYY-MM-DD-HHMM/
# or
./setup-demo.sh my-demo      # creates my-demo/
```

This copies the base template, UI library, theme, tickets, screenshots, installs deps, and initializes git. If you're already in the project directory, proceed directly to Step 4.

### Step 4: Create Supabase table (prefixed for this run)

Read the `NEXT_PUBLIC_TABLE_PREFIX` from `.env.local` — it was set by `setup-demo.sh` (e.g., `run_20260411_1530`).

Use `mcp__claude_ai_Supabase__execute_sql` to create the run-specific tables. The project ID is in `.env.local` (currently `zdklkvkutlmhlclcgtek`). If MCP cannot access that project, list available projects and switch to one that works.

```sql
-- Replace {PREFIX} with the actual table prefix from .env.local
CREATE TABLE IF NOT EXISTS {PREFIX}_insurance_applications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  birth_date TEXT NOT NULL,
  insurance_start TEXT NOT NULL,
  coverage_amount INTEGER NOT NULL,
  plan TEXT NOT NULL CHECK (plan IN ('grundschutz', 'komfort', 'premium')),
  dynamic_adjustment TEXT NOT NULL CHECK (dynamic_adjustment IN ('none', 'standard')),
  salutation TEXT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  street TEXT,
  zip TEXT,
  city TEXT,
  birth_place TEXT,
  nationality TEXT
);

ALTER TABLE {PREFIX}_insurance_applications ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public insert" ON {PREFIX}_insurance_applications FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read" ON {PREFIX}_insurance_applications FOR SELECT USING (true);

-- Wizard step tracking table (see ticket 13)
CREATE TABLE IF NOT EXISTS {PREFIX}_wizard_tracking_events (
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  session_id    UUID NOT NULL,
  wizard_name   TEXT NOT NULL,
  event_type    TEXT NOT NULL CHECK (event_type IN ('wizard_start', 'step_enter', 'step_leave', 'wizard_complete')),
  step          INTEGER NOT NULL,
  sub_step      INTEGER NOT NULL,
  direction     TEXT CHECK (direction IN ('forward', 'backward', 'jump') OR direction IS NULL),
  dwell_time_ms INTEGER,
  fields_filled INTEGER,
  fields_total  INTEGER,
  timestamp     TIMESTAMPTZ NOT NULL,
  metadata      JSONB,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_{PREFIX}_wte_session ON {PREFIX}_wizard_tracking_events (session_id);
ALTER TABLE {PREFIX}_wizard_tracking_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public insert" ON {PREFIX}_wizard_tracking_events FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read" ON {PREFIX}_wizard_tracking_events FOR SELECT USING (true);
```

**Note**: The Supabase credentials are already in `.env.local` (copied from the base template by `setup-demo.sh`). No need to fetch them.

### Step 5: Fix broken symlinks and tsconfig

Run `npm rebuild` to fix broken `.bin` symlinks (consistent issue across runs):
```bash
npm rebuild
```

Add test file exclusions to `tsconfig.json` (the pre-existing `Button.test.tsx` causes `tsc --noEmit` to fail):
```bash
# In tsconfig.json, change:
#   "exclude": ["node_modules"]
# To:
#   "exclude": ["node_modules", "**/*.test.tsx", "**/*.test.ts"]
```

**Verify**: `npm run dev` starts, `http://localhost:3000` shows landing page.

---

## Phase 1: Foundation (BLOCKING)

Execute `tickets/01-foundation.md` directly. Adapt for Next.js:

### What to create in the Next.js project:

1. **`src/lib/wizard/TariffContext.tsx`** — Extend the base WizardContext with tariff-specific form data:
   ```typescript
   export interface TariffFormData {
     birthDate: { day: string; month: string; year: string };
     insuranceStart: string;
     coverageAmount: number;
     plan: "grundschutz" | "komfort" | "premium";
     dynamicAdjustment: "none" | "standard";
     salutation: string;
     firstName: string;
     lastName: string;
     street: string;
     zip: string;
     city: string;
     birthPlace: string;
     nationality: string;
   }
   ```

2. **`src/lib/data/planData.ts`** — Plan pricing data for all 3 tiers (from ticket 05 spec)

3. **`src/app/wizard/page.tsx`** — Replace placeholder with TariffProvider + WizardShell + placeholder pages

4. **`src/app/wizard/pages/index.ts`** — Barrel export for all page components (placeholders initially)

5. **`src/app/api/submit/route.ts`** — Update to insert into `insurance_applications` table

6. **`src/app/dashboard/page.tsx`** — Update table name to `insurance_applications`

7. **`src/app/globals.css`** — **CRITICAL**: Import the theme CSS so UI component colors work:
   ```css
   @import "../../src/lib/theme/theme.css";
   ```
   Add this import at the top of globals.css (after the tailwindcss import). Without this, all CSS custom properties (`--color-primary`, `--color-border`, etc.) are undefined and UI components render with no colors.

8. **`src/lib/data/pricing.ts`** — Dynamic pricing module (see `tickets/feedback-log.md` pre-run feedback):
   ```typescript
   export function calculateMonthlyPrice(age: number, coverageAmount: number, plan: "grundschutz" | "komfort" | "premium"): number
   export function calculatePaymentDuration(age: number): number
   export function getAgeFromBirthYear(birthYear: number, startYear?: number): number
   ```

9. **`src/lib/wizard/validation.ts`** — Generic validation utility (see `tickets/12-form-validations.md`):
   ```typescript
   export function validateStep(config: StepValidationConfig, formData: Record<string, unknown>): Record<string, string>
   export function isStepValid(config: StepValidationConfig, formData: Record<string, unknown>): boolean
   ```

10. **`src/lib/wizard/WizardTrackingProvider.tsx`** — Generic step tracking provider (see `tickets/13-wizard-step-tracking.md`):
    - Observes step/subStep changes via useEffect
    - Fires events to `/api/track` (fire-and-forget)
    - Tracks dwell time, field completion, navigation direction

11. **`src/app/api/track/route.ts`** — Tracking API route, inserts into `wizard_tracking_events` table

12. **`src/app/wizard/page.tsx`** — Wrap WizardShell inside WizardTrackingProvider:
    ```tsx
    <TariffProvider>
      <WizardTrackingProvider wizardName="tariff" stepMap={TARIFF_STEP_MAP}>
        <WizardShell ... />
      </WizardTrackingProvider>
    </TariffProvider>
    ```

**Gate**: `npx tsc --noEmit` must exit 0. `npm run dev` must start. Wizard page shows stepper with colored active step circle.

**Commit**: `git add -A && git commit -m "feat: tariff wizard foundation"`

Do NOT proceed to Phase 2 until this gate passes.

---

## Phase 2: Parallel Page Development

After Phase 1 passes, dispatch ALL 8 page agents simultaneously using the Agent tool.

### Spawn Prompt Template

For each agent, use this template. Replace `{TICKET_FILE}` and `{PAGE_NAME}`:

```
You are building a single page of a Next.js insurance tariff wizard. Your job is to implement the page, then validate it through a review + playwright-cli browser testing loop.

## Your Ticket
Read `tickets/{TICKET_FILE}` for the full specification including visual layout, components to use, interaction logic, and styling.

## Contracts & Gates
Read `tickets/agent-contracts.md` for the EXACT return formats your Reviewer and Tester subagents must use.
Read `tickets/quality-gates.md` for the gate sequence and escalation rules.

## Foundation Code (read these to understand integration points)
- `src/lib/wizard/TariffContext.tsx` — tariff-specific state shape, dispatch actions
- `src/lib/wizard/WizardContext.tsx` — generic wizard navigation (next, back, goTo, setField)
- `src/app/wizard/page.tsx` — how pages are routed based on step/subStep
- `src/app/wizard/pages/index.ts` — where to export your page component

## UI Components
Import from `@/components/ui/<ComponentName>/<ComponentName>`. The library provides:
Button, Link, TextInput, Textarea, Select, Checkbox, RadioButton, Toggle, Stepper, DateInput, Slider, Tooltip, Modal, Toast, SegmentedControl, Card, Alert, InlineRadio

## Your Execution Loop (max 3 iterations)

1. Create your page component file at `src/app/wizard/pages/{PAGE_NAME}.tsx`
   - Add `"use client"` at the top (all wizard pages are client components)
   - Import UI components from `@/components/ui/...`
   - Use `useWizard<TariffFormData>()` for state and navigation
2. Run `npx tsc --noEmit` — must exit 0
3. Spawn a Reviewer subagent (model: opus) — must return STATUS: PASS
4. Spawn a Tester subagent (model: opus) that uses the `playwright-cli` skill:
   - Must use `playwright-cli open http://localhost:3000/wizard --headed`
   - Follow the navigation sequence from the ticket
   - Take screenshots with `playwright-cli screenshot`
   - Must return GATE_RESULT: PASS
5. If either fails → fix issues, go to step 2
6. After 3 failures → ESCALATE

## Critical Rules
- Add `"use client"` to all page components
- NEVER modify files outside your page component
- NEVER modify `src/app/wizard/page.tsx` or `src/app/wizard/pages/index.ts`
- Use the `playwright-cli` skill for browser testing — do NOT write Playwright test files
- The browser must be --headed (visible on desktop)
- All UI text in German, all code comments in English
- CRITICAL: Use ACTUAL Unicode characters (ü, ä, ö, ß, €) in JSX — NEVER use HTML entities (&uuml;), JS unicode escapes (\u20AC), or template literal escapes. They render as literal text in JSX. Write € not \u20AC, write ü not \u00FC.
- If `npx tsc` fails with MODULE_NOT_FOUND, use the full path: `node_modules/typescript/bin/tsc --noEmit`
- playwright-cli CANNOT click hidden `<input>` elements (checkbox, radio). UI components use CSS visually-hidden inputs. Always click the parent `<label>` container (the element with `[cursor=pointer]` in the snapshot), NOT the `getByRole('checkbox')` or `getByRole('radio')` locator.
```

### Dispatch Table

| Agent | description | Ticket File | Page Name |
|-------|-------------|-------------|-----------|
| A | "Build birth date page" | `02-page-1a-birth-date.md` | BirthDatePage |
| B | "Build start date page" | `03-page-1b-start-date.md` | StartDatePage |
| C | "Build coverage page" | `04-page-1c-coverage-amount.md` | CoverageAmountPage |
| D | "Build plan selection page" | `05-page-2a-plan-selection.md` | PlanSelectionPage |
| E | "Build dynamic adjustment page" | `06-page-2b-dynamic-adjustment.md` | DynamicAdjustmentPage |
| F | "Build personal data page" | `07-page-3-personal-data.md` | PersonalDataPage |
| G | "Build summary page" | `08-page-4-summary.md` | SummaryPage |
| H | "Build dashboard page" | `10-dashboard.md` | DashboardPage |

All agents use `isolation: "worktree"` and `model: "opus"`.

---

## Phase 3: Merge + Integration

After all 8 agents complete:

### Step 1: Extract page files from worktrees
```bash
# For each worktree, copy ONLY the page component file:
cp <worktree-path>/src/app/wizard/pages/<PageName>.tsx src/app/wizard/pages/
# For the dashboard agent:
cp <worktree-path>/src/app/dashboard/page.tsx src/app/dashboard/page.tsx
```

### Step 2: Assemble `src/app/wizard/pages/index.ts`
Write this file fresh with all 7 page exports.

### Step 3: Update `src/app/wizard/page.tsx`
Replace placeholder page components with real imports. Wire each page to its correct step/subStep.

### Step 4: Fix Unicode escapes (MANDATORY)

Agents produce `\u20ac` instead of `€` despite instructions. This step auto-corrects them:

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

### Step 5: Compile check
```bash
npx tsc --noEmit
```

### Step 5: Full playwright-cli walkthrough (THE DEMO MOMENT)

This is the integration gate — visible on the user's desktop:

```bash
# Use the playwright-cli skill to:
# 1. Open http://localhost:3000/wizard --headed
# 2. Fill out the ENTIRE wizard with realistic data:
#    - Birth date: 23.06.1982
#    - Insurance start: middle option
#    - Coverage: 8.000 €
#    - Plan: Komfort
#    - Dynamic: accept
#    - Personal: Max Mustermann, Musterstr. 1, 10115 Berlin, Hamburg, deutsch
# 3. Submit the form (check both checkboxes, click submit)
# 4. Verify success toast
# 5. Navigate to http://localhost:3000/dashboard
# 6. Verify "Max Mustermann" appears in the submissions table
# 7. Screenshot everything
```

Spawn Integration Verifier subagent per `agent-contracts.md`. Max 3 iterations.

### Step 6: Commit
```bash
git add -A && git commit -m "feat: complete tariff wizard with all pages + dashboard"
```

### Step 7: Clean up worktrees
```bash
git worktree list
# Remove each completed worktree
```

---

## Phase 4: Deploy + Production Validation

### Step 1: Deploy to Vercel
Use `mcp__claude_ai_Vercel__deploy_to_vercel` to deploy the project.

Set environment variables on Vercel:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Step 2: Verify deployment
Use `mcp__claude_ai_Vercel__get_deployment` to check build status.
If build fails, check logs with `mcp__claude_ai_Vercel__get_deployment_build_logs`.

### Step 3: Production playwright-cli walkthrough
```bash
# Use playwright-cli skill to:
# 1. Open <production-url>/wizard --headed
# 2. Fill out the wizard with DIFFERENT data than integration test
#    (e.g., Erika Musterfrau, Premium plan, 15.000 € coverage)
# 3. Submit
# 4. Navigate to <production-url>/dashboard
# 5. Verify BOTH submissions visible (from integration + production)
# 6. Screenshot the final dashboard
```

### Step 4: Done
Report the production URL to the user.

---

## Success Criteria

- [ ] `npx tsc --noEmit` exits 0
- [ ] `npm run dev` starts without errors
- [ ] All 7 wizard pages render correctly
- [ ] Forward navigation works through entire flow
- [ ] Back navigation preserves entered data
- [ ] Stepper indicator correct at every step
- [ ] Form submission writes to Supabase
- [ ] Dashboard shows submissions with stats
- [ ] Vercel deployment succeeds
- [ ] Production URL works end-to-end
- [ ] playwright-cli walkthrough passes on production

## Session Handoff

If interrupted, write to `temp/tariff-wizard-session-report.md`:

```markdown
# Tariff Wizard Build — Session Report

**To continue**: Paste `tickets/EXECUTE.md` and tell Claude to resume from current state.

## Current State
- **Phase**: <0 | 1 | 2 | 3 | 4>
- **Foundation**: <done | in progress>
- **Page agents completed**: <list>
- **Page agents still running**: <list>
- **Page agents escalated**: <list>
- **Integration**: <not started | in progress | done>
- **Deployment**: <not started | in progress | done>

## What Was Done
- <bullet list>

## What's Next
- <specific next steps>

## Worktrees Still Active
- <path> — <ticket> — <status>
```

## Phase 5: Retrospective & Continuous Improvement

**This phase runs EVERY time, even if earlier phases failed.**

### Step 1: Read previous feedback
At the very START of this execution (before Phase 0), read `tickets/feedback-log.md`.
Apply all lessons from previous runs. If a previous run noted "Agent D always fails on SegmentedControl import path", proactively fix that before dispatching agents.

### Step 2: Self-assessment
After Phase 4 completes (or after any phase that fails/escalates), write a structured self-assessment:

```
RUN_ASSESSMENT:
  DATE: <ISO date>
  DURATION: <total time from start to finish>
  RESULT: SUCCESS | PARTIAL | FAILED

  PHASE_RESULTS:
    Phase 0 (Setup):       PASS | FAIL — <notes>
    Phase 1 (Foundation):  PASS | FAIL — <notes>
    Phase 2 (Parallel):    PASS | FAIL — <X/8 agents succeeded, Y escalated>
    Phase 3 (Integration): PASS | FAIL — <notes>
    Phase 4 (Deploy):      PASS | FAIL — <notes>

  WHAT_WENT_WELL:
  - <concrete thing that worked>
  - <concrete thing that worked>

  WHAT_WENT_WRONG:
  - <concrete failure> — ROOT_CAUSE: <why> — FIX: <what to change>
  - <concrete failure> — ROOT_CAUSE: <why> — FIX: <what to change>

  AGENTS_THAT_STRUGGLED:
  - Agent <X> (ticket <N>): <what happened, how many iterations, what the issue was>

  TIME_BOTTLENECKS:
  - <which phase/agent took longest and why>

  TICKET_IMPROVEMENTS:
  - Ticket <N>: <specific change to make> — REASON: <why>
  - ...

  ARCHITECTURAL_IMPROVEMENTS:
  - <any changes to agent-contracts.md, quality-gates.md, or EXECUTE.md>
```

### Step 3: Ask user for feedback
Present the self-assessment to the user and ask:
- "What looked good? What looked wrong?"
- "Anything I missed in my assessment?"
- "Should I apply the fixes now?"

### Step 4: Append to feedback log
Append the self-assessment AND the user's feedback to `tickets/feedback-log.md` in the ORIGINAL demo-ui-lib repo (not the demo run copy):

```bash
# Write to the source repo so it persists across runs
cat >> /Users/malte/Desktop/Repositories/tlv/demo-ui-lib/tickets/feedback-log.md << 'ENTRY'

## Run: <DATE>
<self-assessment + user feedback>

### Applied Fixes
- [ ] <fix 1 — checked off when applied to tickets>
- [ ] <fix 2>
ENTRY
```

### Step 5: Apply fixes to source tickets
If the user approves, update the ticket files in the ORIGINAL `demo-ui-lib/tickets/` directory (not the demo run copy). This way the next `./setup-demo.sh` run inherits the improvements.

Changes to apply:
- Fix ticket specs that caused agent failures
- Update navigation sequences that didn't work
- Adjust agent contracts if return formats were problematic
- Update EXECUTE.md if phase transitions were unclear

---

## Key Commands

```bash
npm run dev                    # Start Next.js dev server (port 3000)
npx tsc --noEmit               # TypeScript check
playwright-cli open <url> --headed  # Open browser (visible on desktop)
playwright-cli snapshot        # Get page element refs
playwright-cli close           # Close browser
```
