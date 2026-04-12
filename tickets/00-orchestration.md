# Orchestration Plan: Full-Stack Insurance Tariff Wizard

## Overview

Build a fully functional full-stack insurance tariff wizard (Sterbegeldversicherung):
- **Frontend**: Next.js App Router with multi-step wizard using the `demo-ui-lib` component library
- **Backend**: Supabase database for storing submissions
- **Dashboard**: Server-rendered analytics page showing submissions + stats
- **Deployment**: Vercel production URL
- **Validation**: playwright-cli browser interaction (headed, visible on desktop)

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  ORCHESTRATOR                        │
│  Reads EXECUTE.md, dispatches phases sequentially    │
└──────────┬──────────────┬───────────────┬────────────┘
           │              │               │
   Phase 0+1          Phase 2          Phase 3+4
   (Setup +           (8 parallel      (Merge +
    Foundation)        agents)          Deploy)
           │              │               │
           │     ┌────────┴────────┐      │
           │     │  Per-Agent Loop │      │
           │     │                 │      │
           │     │  Developer      │      │
           │     │    ↓            │      │
           │     │  compile-gate   │      │
           │     │    ↓            │      │
           │     │  Reviewer (opus)│      │
           │     │    ↓            │      │
           │     │  Tester         │      │
           │     │  (playwright-cli│      │
           │     │   --headed)     │      │
           │     │    ↓            │      │
           │     │  Loop or PASS   │      │
           │     └─────────────────┘      │
```

## Execution Order & Dependencies

```
Phase 0: Setup (~2 min)
  - Copy base template, UI library, reference screenshots
  - Create Supabase table via MCP
  - Set environment variables

Phase 1: Foundation (BLOCKING, ~3 min)
  - TariffContext, planData, wizard page routing, API route

Phase 2: Parallel development (~8 min)
  - 8 agents in isolated worktrees:
    - Agents A-G: 7 wizard pages (tickets 02-08)
    - Agent H: Dashboard page (ticket 10)
  - Each runs: develop → compile → review → playwright-cli → loop

Phase 3: Integration (~5 min)
  - Merge worktree files
  - Full playwright-cli walkthrough (headed, visible)
  - Submit form, verify on dashboard

Phase 4: Deploy (~3 min)
  - Vercel deploy via MCP
  - Production playwright-cli walkthrough
```

## Key Files

| File | Purpose |
|------|---------|
| `EXECUTE.md` | Single entry point — paste into new session |
| `agent-contracts.md` | Structured return formats for Reviewer, Tester, Verifier |
| `quality-gates.md` | Gate sequence: compile → review → browser → integration → deploy → production |
| `01-foundation.md` | Wizard state, routing, API |
| `02-08` | Individual wizard pages |
| `10-dashboard.md` | Dashboard with analytics |

## Reference Screenshots Mapping

| Screenshot | Ticket | Description |
|---|---|---|
| `Screenshot 2026-04-10 111825.png` | 02 | Birth date entry (Step 1, Sub-step 1) |
| `Screenshot 2026-04-10 111815.png` | 03 | Insurance start date (Step 1, Sub-step 2) |
| `Screenshot 2026-04-10 111525.png` | 04 | Coverage amount slider (Step 1, Sub-step 3) |
| `Screenshot 2026-04-10 171511.png` | 05 | Plan selection (Step 2, Sub-step 1) |
| `Screenshot 2026-04-10 171544.png` | 06 | Dynamic adjustment (Step 2, Sub-step 2) |
| `Screenshot 2026-04-10 171607.png` | 07 | Personal data form (Step 3) |
| *(no reference)* | 08 | Summary page (Step 4) |
| *(no reference)* | 10 | Dashboard |

## Shared Conventions

- **UI Components**: Import from `@/components/ui/<ComponentName>/<ComponentName>`
- **State**: Use `useWizard<TariffFormData>()` from `@/lib/wizard`
- **Styling**: Inline styles for wizard pages (matching ERGO design), Tailwind for dashboard
- **Theme**: primary: #8e0038, secondary: #bf1528
- **Language**: All UI text in German, code comments in English
- **Testing**: playwright-cli with `--headed` flag (visible on desktop)
- **Base URL**: `http://localhost:3000` (Next.js default port)
