# Ticket 10: Dashboard Page

## Priority: Phase 2 (parallel with wizard pages)

## Objective

Build the dashboard page that displays submitted insurance applications from Supabase. Shows summary statistics (total submissions, average coverage, most popular plan) and a table of recent submissions.

## Visual Specification

```
┌──────────────────────────────────────────────────────┐
│  Antragsübersicht                                     │  ← Bold heading
│  Alle eingegangenen Versicherungsanträge              │  ← Subtitle, gray
│                                                       │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────┐│
│  │    12      │  │   8.450 €    │  │  Komfort (67%) ││  ← Stat cards
│  │  Anträge   │  │ Ø Deckung    │  │beliebtester    ││
│  │            │  │              │  │    Tarif       ││
│  └────────────┘  └──────────────┘  └────────────────┘│
│                                                       │
│  Tarif-Verteilung                                     │
│  ┌────────────────────────────────────────────────┐  │
│  │ Grundschutz  ████████░░░░░░░░░░░░░  25%       │  │  ← CSS bar chart
│  │ Komfort      ████████████████░░░░░  50%       │  │
│  │ Premium      ████████░░░░░░░░░░░░░  25%       │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  Letzte Anträge                                       │
│  ┌────┬──────────────┬─────────┬────────┬──────────┐ │
│  │ #  │ Name         │ Tarif   │ Summe  │ Datum    │ │  ← Table
│  ├────┼──────────────┼─────────┼────────┼──────────┤ │
│  │ 1  │ Max Muster.. │ Komfort │ 8.000€ │ 11.04.  │ │
│  │ 2  │ ...          │ ...     │ ...    │ ...      │ │
│  └────┴──────────────┴─────────┴────────┴──────────┘ │
└──────────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/dashboard/page.tsx` (REPLACE placeholder)

A **server component** that:
1. Queries Supabase `insurance_applications` table
2. Computes aggregations (count, avg coverage, plan distribution)
3. Renders stat cards, plan distribution bars, and submissions table

### Components Used

Use Tailwind CSS for styling (no UI library components needed for the dashboard — it's a different context than the wizard).

## Data Schema

The dashboard reads from the Supabase table using the `tableName()` helper from `@/lib/supabase`:
```typescript
import { supabase, tableName } from "@/lib/supabase";
const { data } = await supabase.from(tableName("insurance_applications")).select("*");
```

This resolves to e.g. `run_20260411_1530_insurance_applications` — unique per demo run but sharing one Supabase instance.

Columns:
```
id, created_at, birth_date, insurance_start, coverage_amount,
plan, dynamic_adjustment, salutation, first_name, last_name,
street, zip, city, birth_place, nationality
```

## Aggregations

```typescript
// Total submissions
const total = submissions.length;

// Average coverage
const avgCoverage = submissions.reduce((sum, s) => sum + s.coverage_amount, 0) / total;

// Plan distribution
const planCounts = { grundschutz: 0, komfort: 0, premium: 0 };
submissions.forEach(s => planCounts[s.plan]++);
const mostPopular = Object.entries(planCounts).sort((a, b) => b[1] - a[1])[0];

// Plan distribution as percentages for bar chart
const planPercent = Object.fromEntries(
  Object.entries(planCounts).map(([k, v]) => [k, Math.round((v / total) * 100)])
);
```

## Styling Notes

- Max-width: 1024px, centered
- Stat cards: grid 3 columns, bg-gray-50, rounded-lg, centered text
- Big number: text-3xl font-bold
- Label: text-sm text-gray-500
- Plan bars: simple div with percentage width, bg-[#8e0038], rounded
- Table: bordered, striped rows on hover
- German locale for numbers and dates

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read the dashboard placeholder at `src/app/dashboard/page.tsx`
2. Read `tickets/13-wizard-step-tracking.md` section "Dashboard: Funnel Analytics Section" — the dashboard MUST include the wizard funnel visualization
3. Replace it with a full server component that queries BOTH Supabase tables (`insurance_applications` AND `wizard_tracking_events`) using `Promise.all`
4. Compute aggregations from query results (submissions stats + funnel analytics)
5. Render stat cards + plan distribution bars + **wizard funnel section** + submissions table
6. Handle empty state gracefully (no submissions yet)
6. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus)
   - **browser-gate**: Spawn Tester subagent (opus) with playwright-cli
7. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- Server component (no "use client") — Supabase query runs on server
- Handles empty state (0 submissions) without errors
- German locale for numbers (8.450 €) and dates (11.04.2026)
- Plan distribution bars use correct percentage widths
- `force-dynamic` export to prevent static rendering

### Tester: Navigation Sequence (playwright-cli)
```bash
playwright-cli open http://localhost:3000/dashboard --headed
playwright-cli snapshot
# Dashboard loads directly — no wizard navigation needed
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Antragsübersicht" visible
[CHECK] Three stat cards render (even with 0 data — shows "0" or "—")
[CHECK] Plan distribution section renders
[CHECK] Wizard-Funnel section renders (if tracking data exists)
[CHECK] Funnel shows 3 summary cards (Sessions gestartet, Abgeschlossen, Abschlussrate)
[CHECK] Funnel shows step-by-step bars with dwell times
[CHECK] Submissions table renders (empty state if no data)
[CHECK] No console errors
[CHECK] Page loads within 3 seconds
```
