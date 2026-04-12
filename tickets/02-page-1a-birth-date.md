# Ticket 02: Page 1a — Birth Date Entry

## Step: 1 (Tarifdaten) | Sub-step: 1

## Reference Screenshot
`screenshots/reference/Screenshot 2026-04-10 111825.png`

## Objective

Build the birth date entry page — the first page of the tariff wizard. The user enters their date of birth using day/month/year spinner inputs.

## Visual Specification (from reference)

```
┌─────────────────────────────────────────────┐
│  (1) Tarifdaten  (2) Beitrag  (3) ...       │  ← Stepper (handled by wizard shell)
├─────────────────────────────────────────────┤
│                                             │
│     Geben Sie Ihr Geburtsdatum ein          │  ← Bold heading, centered
│                   ⓘ                         │  ← Info tooltip
│                                             │
│         ┌──────┐ ┌──────┐ ┌────────┐        │
│         │  23  │ │  06  │ │  1982  │        │  ← DateInput (day/month/year)
│         └──────┘ └──────┘ └────────┘        │
│                                             │
│  Die versicherte Person muss zwischen       │  ← Hint text, small, gray, centered
│  40 und 85 Jahre alt sein. Das Alter        │
│  berechnet sich so: Jahr des gewünschten    │
│  Versicherungsbeginns (z. B. 2026) -        │
│  Geburtsjahr.                               │
│                                             │
│         ┌───────────────────┐               │
│         │      weiter       │               │  ← Primary button, full-width (max ~360px)
│         └───────────────────┘               │
│                                             │
└─────────────────────────────────────────────┘
```

**Note:** This is the FIRST page — no "Zurück" (back) button.

## Files to Create/Modify

### `demo/pages/BirthDatePage.tsx`

```tsx
// Key elements:
// - Heading: "Geben Sie Ihr Geburtsdatum ein"
// - Tooltip icon (ⓘ) below heading with info about age calculation
// - DateInput component from src/components/DateInput
// - Hint text about age range (40-85 years)
// - "weiter" button → navigates to sub-step 2
// - Uses useTariff() to read/write birthDate
// - Uses useWizardNav() to navigate
```

### `demo/pages/index.ts` (MODIFY)
Export `BirthDatePage` and wire it into the wizard for step 1, sub-step 1.

## Component Usage

```tsx
import { DateInput } from "../../src/components/DateInput";
import { Button } from "../../src/components/Button";
import { Tooltip } from "../../src/components/Tooltip";
```

## Interaction Logic

- DateInput value comes from `tariffState.birthDate`
- onChange updates context via `dispatch({ type: "SET_BIRTH_DATE", payload })`
- "weiter" button calls `wizardNav.next()` → moves to step 1, sub-step 2
- Optional: basic validation (all 3 fields filled) before enabling "weiter"

## Styling Notes

- Heading: font-size ~24px, font-weight 700, text-align center, font-family: "Fedra Serif", Georgia, serif
- Tooltip icon: centered below heading, margin 8px
- DateInput: centered in page
- Hint text: font-size ~12px, color #737373, text-align center, max-width ~400px
- "weiter" button: max-width ~360px, centered, margin-top 32px
- Overall content: centered flex column, gap 24px

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `screenshots/reference/Screenshot 2026-04-10 111825.png` for visual reference
2. Read `src/components/DateInput/DateInput.tsx` for the DateInput API
3. Read `src/components/Tooltip/Tooltip.tsx` for the Tooltip API
4. Read `demo/context/TariffContext.tsx` for state shape and dispatch actions
5. Create `demo/pages/BirthDatePage.tsx` matching the visual spec
6. Update `demo/pages/index.ts` to export it
7. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence: page loads at step 1, subStep 1 (first page, no prior navigation needed)
8. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- No "Zurück" button on this first page
- DateInput wired to `tariffState.birthDate`
- Hint text matches reference: "40 und 85 Jahre alt" with age calculation formula
- Tooltip present below heading

### Tester: Navigation Sequence (playwright-cli)
```bash
playwright-cli open http://localhost:3000/wizard --headed
playwright-cli snapshot
# Page 1a is the default/first page — no prior navigation needed
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Geben Sie Ihr Geburtsdatum ein" visible
[CHECK] DateInput renders with day/month/year fields
[CHECK] Can enter birth date (23/06/1982)
[CHECK] Hint text about age range (40-85) visible
[CHECK] "weiter" button visible, no "Zurück" button
[CHECK] Clicking "weiter" navigates to insurance start date page
```
