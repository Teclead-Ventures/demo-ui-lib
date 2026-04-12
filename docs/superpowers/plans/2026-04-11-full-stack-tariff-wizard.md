# Full-Stack Insurance Tariff Wizard — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a complete full-stack insurance tariff wizard with Next.js frontend, Supabase backend, analytics dashboard, and Vercel deployment — orchestrated by parallel agents with playwright-cli browser validation.

**Architecture:** Next.js App Router with client-side multi-step wizard form using an existing React UI component library. Server-side API route inserts submissions into Supabase. Dashboard is a server component reading directly from Supabase. Parallel agent development with worktree isolation, each agent running a compile→review→browser-test feedback loop.

**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS, Supabase (Postgres), Vercel, playwright-cli, existing demo-ui-lib component library (18 components).

---

## File Structure

```
tlv-tariff-wizard/                    (copied from next-demo-base)
├── src/
│   ├── app/
│   │   ├── layout.tsx                 # Root layout (modify: title, fonts)
│   │   ├── page.tsx                   # Landing (already done)
│   │   ├── wizard/
│   │   │   ├── page.tsx               # Phase 1: wire WizardProvider + WizardShell + pages
│   │   │   └── pages/
│   │   │       ├── index.ts           # Phase 3: assemble all exports
│   │   │       ├── BirthDatePage.tsx   # Agent A
│   │   │       ├── StartDatePage.tsx   # Agent B
│   │   │       ├── CoverageAmountPage.tsx  # Agent C
│   │   │       ├── PlanSelectionPage.tsx    # Agent D
│   │   │       ├── DynamicAdjustmentPage.tsx # Agent E
│   │   │       ├── PersonalDataPage.tsx     # Agent F
│   │   │       └── SummaryPage.tsx          # Agent G
│   │   ├── dashboard/
│   │   │   └── page.tsx               # Agent H
│   │   └── api/submit/
│   │       └── route.ts               # Phase 1: update for insurance_applications
│   ├── components/ui/                 # Phase 0: copied from demo-ui-lib
│   │   ├── Button/Button.tsx + .css
│   │   ├── Stepper/Stepper.tsx + .css
│   │   └── ... (18 components)
│   └── lib/
│       ├── supabase.ts                # Already done (base template)
│       ├── theme/                     # Phase 0: copied from demo-ui-lib
│       ├── data/
│       │   └── planData.ts            # Phase 1: pricing data
│       └── wizard/
│           ├── WizardContext.tsx       # Already done (base template)
│           ├── WizardShell.tsx         # Already done (base template)
│           ├── TariffContext.tsx       # Phase 1: tariff-specific form data
│           └── index.ts               # Update exports
├── tickets/                           # Phase 0: copied from demo-ui-lib
├── screenshots/reference/             # Phase 0: copied from demo-ui-lib
└── .env.local                         # Phase 0: Supabase credentials
```

---

## Task 0: Setup (Phase 0)

**Files:**
- Copy: `next-demo-base/` → `tlv-tariff-wizard/`
- Copy: `demo-ui-lib/src/components/*` → `tlv-tariff-wizard/src/components/ui/`
- Copy: `demo-ui-lib/src/theme/` → `tlv-tariff-wizard/src/lib/theme/`
- Copy: `demo-ui-lib/screenshots/reference/` → `tlv-tariff-wizard/screenshots/reference/`
- Copy: `demo-ui-lib/tickets/` → `tlv-tariff-wizard/tickets/`
- Create: `.env.local`

- [ ] **Step 1: Copy base template**
```bash
cp -r /Users/malte/Desktop/Repositories/tlv/next-demo-base /Users/malte/Desktop/Repositories/tlv/tlv-tariff-wizard
cd /Users/malte/Desktop/Repositories/tlv/tlv-tariff-wizard
npm install
```

- [ ] **Step 2: Copy UI library + theme**
```bash
cp -r /Users/malte/Desktop/Repositories/tlv/demo-ui-lib/src/components/* src/components/ui/
cp -r /Users/malte/Desktop/Repositories/tlv/demo-ui-lib/src/theme/ src/lib/theme/
```

- [ ] **Step 3: Copy reference screenshots + tickets**
```bash
cp -r /Users/malte/Desktop/Repositories/tlv/demo-ui-lib/screenshots/reference/ screenshots/reference/
cp -r /Users/malte/Desktop/Repositories/tlv/demo-ui-lib/tickets/ tickets/
```

- [ ] **Step 4: Create Supabase table**
Use `mcp__claude_ai_Supabase__execute_sql` with the SQL from `tickets/EXECUTE.md` Phase 0 Step 4.

- [ ] **Step 5: Set environment variables**
Use `mcp__claude_ai_Supabase__get_project_url` and `mcp__claude_ai_Supabase__get_publishable_keys` to get credentials. Write `.env.local`.

- [ ] **Step 6: Verify**
```bash
npm run dev
# Open http://localhost:3000 — landing page visible
```

- [ ] **Step 7: Initialize git + commit**
```bash
git init && git add -A && git commit -m "Initial setup: base template + UI library + Supabase config"
```

---

## Task 1: Foundation (Phase 1)

**Files:**
- Create: `src/lib/wizard/TariffContext.tsx`
- Create: `src/lib/data/planData.ts`
- Modify: `src/app/wizard/page.tsx`
- Create: `src/app/wizard/pages/index.ts`
- Modify: `src/app/api/submit/route.ts`
- Modify: `src/app/layout.tsx`

See `tickets/01-foundation.md` and `tickets/EXECUTE.md` Phase 1 for full details.

- [ ] **Step 1: Create TariffContext.tsx**
Extend the base WizardContext with `TariffFormData` interface matching all wizard fields.

- [ ] **Step 2: Create planData.ts**
Static pricing data for Grundschutz, Komfort, Premium tiers.

- [ ] **Step 3: Create placeholder pages + index.ts**
7 placeholder components that just render their name.

- [ ] **Step 4: Wire wizard/page.tsx**
Replace placeholder with `TariffProvider` + `WizardShell` + step/subStep routing.

- [ ] **Step 5: Update API route**
Change table name to `insurance_applications`, map TariffFormData to column names.

- [ ] **Step 6: Update layout.tsx**
Set title to "Sterbegeldversicherung — Tarifrechner", lang="de".

- [ ] **Step 7: Compile gate**
```bash
npx tsc --noEmit
```
Expected: exit 0

- [ ] **Step 8: Verify dev server**
```bash
npm run dev
# http://localhost:3000/wizard shows stepper with 4 steps + placeholder page
```

- [ ] **Step 9: Commit**
```bash
git add -A && git commit -m "feat: tariff wizard foundation — state, routing, API"
```

---

## Tasks 2-9: Parallel Page Development (Phase 2)

**Dispatch all 8 agents in ONE message using the Agent tool.**

Each agent uses `isolation: "worktree"` and `model: "opus"`.

See `tickets/EXECUTE.md` Phase 2 for the spawn prompt template and dispatch table.

| Task | Agent | Ticket | Creates |
|------|-------|--------|---------|
| 2 | A | `02-page-1a-birth-date.md` | `BirthDatePage.tsx` |
| 3 | B | `03-page-1b-start-date.md` | `StartDatePage.tsx` |
| 4 | C | `04-page-1c-coverage-amount.md` | `CoverageAmountPage.tsx` |
| 5 | D | `05-page-2a-plan-selection.md` | `PlanSelectionPage.tsx` |
| 6 | E | `06-page-2b-dynamic-adjustment.md` | `DynamicAdjustmentPage.tsx` |
| 7 | F | `07-page-3-personal-data.md` | `PersonalDataPage.tsx` |
| 8 | G | `08-page-4-summary.md` | `SummaryPage.tsx` |
| 9 | H | `10-dashboard.md` | `dashboard/page.tsx` |

Each agent internally runs: develop → compile-gate → review-gate → browser-gate (playwright-cli, --headed) → loop max 3.

- [ ] **Step 1: Dispatch all 8 agents simultaneously**
- [ ] **Step 2: Monitor agent completions**
- [ ] **Step 3: Handle any escalations**

---

## Task 10: Integration (Phase 3)

**Files:**
- Modify: `src/app/wizard/pages/index.ts` (assemble all exports)
- Modify: `src/app/wizard/page.tsx` (wire real pages)

- [ ] **Step 1: Extract page files from all worktrees**
```bash
# Copy each page component from its worktree into the main project
```

- [ ] **Step 2: Write pages/index.ts with all 7 exports**

- [ ] **Step 3: Update wizard/page.tsx routing with real page imports**

- [ ] **Step 4: Compile gate**
```bash
npx tsc --noEmit
```

- [ ] **Step 5: Full playwright-cli walkthrough (headed, visible)**
Use `playwright-cli` skill to navigate through the ENTIRE wizard, fill all fields, submit, and verify on dashboard. This is the demo moment.

- [ ] **Step 6: Commit**
```bash
git add -A && git commit -m "feat: complete tariff wizard with all pages + dashboard"
```

- [ ] **Step 7: Clean up worktrees**

---

## Task 11: Deploy + Production Validation (Phase 4)

- [ ] **Step 1: Deploy to Vercel**
Use `mcp__claude_ai_Vercel__deploy_to_vercel`. Set env vars on Vercel.

- [ ] **Step 2: Verify build succeeds**
Check with `mcp__claude_ai_Vercel__get_deployment`.

- [ ] **Step 3: Production playwright-cli walkthrough (headed)**
Navigate through wizard on production URL with DIFFERENT test data. Verify on dashboard.

- [ ] **Step 4: Report production URL to user**

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-11-full-stack-tariff-wizard.md`.

**To execute**: Open a new Claude Code session in the `demo-ui-lib` directory and paste:

```
Read tickets/EXECUTE.md and execute it. Read all tickets in tickets/ for full context. Use parallel agents with worktrees for Phase 2. Use the playwright-cli skill for all browser validation.
```

**Recommended execution approach**: Subagent-Driven Development — dispatch a fresh subagent per task with two-stage review. Use `superpowers:subagent-driven-development` or `superpowers:dispatching-parallel-agents` for Phase 2.
