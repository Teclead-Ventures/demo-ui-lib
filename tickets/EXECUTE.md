# Execute: Build Full-Stack Insurance Tariff Wizard — Berufsunfähigkeitsversicherung

**Paste this into a new Claude Code session in the project directory to start autonomous development.**

ultrathink

---

## Mission

Build a complete full-stack insurance tariff wizard (Berufsunfähigkeitsversicherung):
- **Frontend**: Next.js app with multi-step wizard using the `demo-ui-lib` component library
- **Backend**: Supabase database storing submissions
- **Dashboard**: Analytics page showing all submissions
- **Deployment**: Vercel production URL
- **Validation**: playwright-cli browser interaction (headed, visible on desktop)

The UI component library is at `src/components/ui/`.
Reference screenshots are at `screenshots/reference/`.

## Architecture

```
Orchestrator (you)
  │
  ├─ Phase 0: Setup (~2 min)
  │   Copy UI lib, create Supabase table, set env vars
  │
  ├─ Phase 1: Foundation (~3 min)
  │   TariffContext, pricing engine, planData, API routes, page routing
  │   Gate: npx tsc --noEmit + npm run dev works
  │
  ├─ Phase 2: 7 Agents in parallel (~8 min)
  │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
  │   │ Agent A │ │ Agent B │ │ Agent C │ │ Agent D │
  │   │Beruf    │ │Geburts- │ │Coverage │ │PlanSel. │
  │   │         │ │datum    │ │         │ │         │
  │   └─────────┘ └─────────┘ └─────────┘ └─────────┘
  │   ┌─────────┐ ┌─────────┐ ┌─────────┐
  │   │ Agent E │ │ Agent F │ │ Agent G │
  │   │Gesund-  │ │Personal │ │Summary  │
  │   │heit     │ │Data     │ │         │
  │   └─────────┘ └─────────┘ └─────────┘
  │
  ├─ Phase 3: Integration (~5 min)
  │   Merge all worktrees, playwright full walkthrough, fix issues
  │
  ├─ Phase 4: Deploy (~3 min)
  │   Vercel deploy, production playwright walkthrough
  │
  └─ Phase 5: Retrospective (~1 min)
      Write feedback-log.md
```

## Agent Dispatch Table

| Agent | Ticket | Page | Type |
|-------|--------|------|------|
| A | 02-page-1a-birth-date.md | Berufsgruppe | radio-selection |
| B | 03-page-1b-start-date.md | Geburtsdatum | date-entry |
| C | 04-page-1c-coverage-amount.md | Einkommen & BU-Rente | slider+number |
| D | 05-page-2a-plan-selection.md | Tarifauswahl | segmented-plan |
| E | 06-page-2b-dynamic-adjustment.md | Gesundheitsfragen | form |
| F | 07-page-3-personal-data.md | Persönliche Daten | form |
| G | 08-page-4-summary.md | Zusammenfassung | summary |

## Phase 0: Setup

```bash
# 1. Verify UI components are already in src/components/ui/
# 2. Create Supabase table (use prefix from .env.local)
```

```sql
CREATE TABLE IF NOT EXISTS {PREFIX}_bu_applications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  occupation TEXT NOT NULL CHECK (occupation IN ('buero','handwerk','koerperlich','gefahren')),
  birth_date TEXT NOT NULL,
  monthly_income TEXT NOT NULL,
  coverage_amount TEXT NOT NULL,
  plan TEXT NOT NULL CHECK (plan IN ('grundschutz','komfort','premium')),
  monthly_price TEXT NOT NULL,
  payment_duration_years INTEGER NOT NULL,
  smoker TEXT NOT NULL,
  pre_existing_conditions TEXT NOT NULL,
  salutation TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  street TEXT NOT NULL,
  zip TEXT NOT NULL,
  city TEXT NOT NULL
);
```

```bash
# 3. Verify .env.local has Supabase credentials + TABLE_PREFIX
# 4. npm install && npm run dev → verify it compiles
```

## Phase 1: Foundation

Read and implement `tickets/01-foundation.md`.

Gate before Phase 2:
- `npx tsc --noEmit` → zero errors
- `npm run dev` → server starts, `/wizard` renders without crash
- Navigation between steps works

## Phase 2: Parallel Build

Dispatch all 7 agents simultaneously using worktrees.

**Agent prompt template** (fill in ticket number/name):
```
Read tickets/EXECUTE.md for context.
Read tickets/agent-contracts.md for your return format.
Read tickets/quality-gates.md for the gate loop.
Read tickets/[NN-ticket-name].md — this is your specific ticket.
Implement it. Run the quality gate loop (max 3 iterations).
Return your result in the exact format from agent-contracts.md.
```

## Phase 3: Integration

1. Merge all worktrees into main
2. `npx tsc --noEmit` → fix any type errors
3. `npm run dev` → playwright-cli full walkthrough:

```bash
playwright-cli open http://localhost:3000/wizard --headed
# Step through entire wizard with demo data:
# Schritt 1: Bürotätigkeit → weiter
# Schritt 2: 15 / 03 / 1990 → weiter
# Schritt 3: Einkommen 3.500 € / BU-Rente 2.000 € → weiter
# Schritt 4: Komfort auswählen → weiter
# Schritt 5: Raucher Nein / Vorerkrankungen Nein → weiter
# Schritt 6: Herr / Markus / Weber / Friedrichstraße 22 / 10117 / Berlin → weiter
# Schritt 7: check both boxes → Jetzt verbindlich abschließen
# Verify: success toast appears
```

4. Verify `/dashboard` shows the new submission.
5. Test demo mode: `http://localhost:3000/wizard?demo=true` — all fields pre-filled.

## Phase 4: Deploy

```bash
vercel --prod
playwright-cli open https://[project].vercel.app/wizard?demo=true --headed
# Full walkthrough on production
```

## Phase 5: Retrospective

Write to `tickets/feedback-log.md`.

---

## Integration Test Data

**Set 1** (localhost):
- occupation: buero, birthDate: 15.03.1990 (35 J.), plan: komfort
- monthlyIncome: 3.500 €, coverageAmount: 2.000 €/Monat
- expectedPrice: ~58,37 €/Monat
- smoker: nein, preExistingConditions: nein
- Herr Markus Weber, Friedrichstraße 22, 10117 Berlin

**Set 2** (production):
- occupation: handwerk, birthDate: 22.07.1978 (47 J.), plan: premium
- monthlyIncome: 2.800 €, coverageAmount: 1.800 €/Monat
- expectedPrice: ~100,63 €/Monat
- smoker: nein, preExistingConditions: nein
- Frau Sandra Hoffmann, Karlsplatz 7, 80335 München

---

## Key constraints

- All user-facing text in **German**
- Use actual Unicode: ä ö ü ß € — NEVER escape sequences
- Components from `src/components/ui/` — read source before using
- Pricing calculated client-side from `src/lib/data/pricing.ts`
- Form data in snake_case for DB, camelCase in TypeScript
- Demo mode via `?demo=true` — pre-fills all fields
- Coverage validation: coverageAmount ≤ 75% of monthlyIncome
- Age validation: birthDate must result in age 18–55
