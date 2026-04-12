# Ticket 09: Integration & End-to-End Testing

## Priority: FINAL — Execute after all page tickets (02-08) are merged

## Objective

Verify the complete wizard works end-to-end. Run full integration tests, fix any cross-page issues, and create a comprehensive Playwright E2E test suite that validates the entire user journey.

## Prerequisites

- All tickets 01-08 must be completed and merged
- Dev server must start without errors: `npm run demo`
- No TypeScript compilation errors: `npx tsc --noEmit`

## Playwright Setup

### `playwright.config.ts` (CREATE at project root)

```typescript
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  use: {
    baseURL: "http://localhost:5173",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "npm run demo",
    port: 5173,
    reuseExistingServer: true,
  },
});
```

### `e2e/full-flow.spec.ts` (CREATE)

Complete user journey test:

```typescript
// Full flow: Fill out the entire insurance application

// 1. PAGE 1a — Birth Date
//    - Verify stepper shows "Tarifdaten" as active
//    - Enter birth date: 23 / 06 / 1982
//    - Click "weiter"

// 2. PAGE 1b — Insurance Start Date
//    - Verify three radio options visible
//    - Select middle option
//    - Click "weiter"

// 3. PAGE 1c — Coverage Amount
//    - Verify slider is visible
//    - Adjust slider to 10,000 €
//    - Verify benefit bullets visible
//    - Click "weiter"

// 4. PAGE 2a — Plan Selection
//    - Verify stepper now shows "Beitrag" as active
//    - Verify SegmentedControl with 3 options
//    - Select "Premium"
//    - Verify price updates
//    - Click "weiter zum Online-Antrag"

// 5. PAGE 2b — Dynamic Adjustment
//    - Verify plan summary bar shows "Premium" with correct price
//    - Click "auswählen und weiter" (accept dynamic adjustment)

// 6. PAGE 3 — Personal Data
//    - Verify stepper shows "Persönliches" as active
//    - Fill: Anrede=Herr, Vorname=Max, Nachname=Mustermann
//    - Fill: Straße=Musterstraße 1, PLZ=10115, Ort=Berlin
//    - Fill: Geburtsort=Hamburg
//    - Select: Staatsangehörigkeit=deutsch
//    - Click "weiter"

// 7. PAGE 4 — Summary
//    - Verify stepper shows "Zusammenfassung" as active
//    - Verify all entered data is displayed correctly
//    - Verify coverage amount shows "10.000 €"
//    - Verify plan shows "Premium"
//    - Check both consent checkboxes
//    - Click "Jetzt verbindlich abschließen"
//    - Verify success toast appears
```

### `e2e/navigation.spec.ts` (CREATE)

Navigation-specific tests:

```typescript
// Test back navigation through all steps
// Test edit links on summary page (jump to specific steps)
// Test that data persists when navigating back and forth
// Test stepper state at each step
```

### `e2e/visual-regression.spec.ts` (CREATE)

Screenshot comparison tests:

```typescript
// Take full-page screenshots at each step
// Compare against reference screenshots in screenshots/reference/
// Allow threshold for minor differences (fonts, anti-aliasing)
// Save actual screenshots to screenshots/e2e-actual/ for manual review
```

## Agent Execution (see tickets/agent-contracts.md → Integration Verifier)

**This ticket is executed by the orchestrator directly (not in a worktree).**

The orchestrator:
1. Merges all worktree branches from page agents
2. Resolves any merge conflicts (primarily in `demo/pages/index.ts`)
3. Runs the integration gate (see `tickets/quality-gates.md` → Gate: Integration)

### Integration Gate Loop (max 3 iterations)

```
1. npx tsc --noEmit — fix any import/type errors from merge
2. npm run demo — verify dev server starts
3. Spawn Integration Verifier subagent (opus)
   → Provides: list of all page files, context state shape, wizard step mapping
   → Expects: structured GATE_RESULT (see agent-contracts.md)
4. If GATE_RESULT: FAIL → fix BLOCKING_ISSUES, re-run
5. If GATE_RESULT: PASS → done
6. After 3 failures → present ESCALATION_REPORT to user
```

### Common Merge Issues to Watch For
- `demo/pages/index.ts` — all pages need to be exported (each worktree only added its own)
- `demo/data/planData.ts` — tickets 05, 06, and 08 all reference this file, ensure it exists once
- `demo/TariffWizard.tsx` — page imports may need updating if worktree agents added imports
- Navigation step/subStep mapping — verify all pages are reachable via the wizard's routing logic

### Full E2E Test Suite
The Integration Verifier creates and runs `e2e/full-flow.spec.ts` covering:
- Complete wizard flow (all 7 pages, realistic data entry)
- Back navigation preserving data
- Edit links from summary
- Stepper state at each step
- Final submit with success toast

### Escalation
If integration fails 3 times, present to user:
- Which pages cause issues
- Merge conflicts encountered
- Test failures with screenshots
- Recommended manual fixes
