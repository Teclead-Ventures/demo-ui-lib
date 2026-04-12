# Ticket 04: Page 1c — Coverage Amount

## Step: 1 (Tarifdaten) | Sub-step: 3

## Reference Screenshot
`screenshots/reference/Screenshot 2026-04-10 111525.png`

## Objective

Build the coverage amount selection page. The user selects how much money should be available for the funeral using a slider and numeric input, with benefit descriptions below.

## Visual Specification (from reference)

```
┌─────────────────────────────────────────────┐
│  (1) Tarifdaten  (2) Beitrag  (3) ...       │
├─────────────────────────────────────────────┤
│                                             │
│  Wie viel Geld soll für die Beerdigung      │  ← Bold heading, centered
│  verfügbar sein?                            │
│                   ⓘ                         │  ← Info tooltip
│                                             │
│  ●━━━━━━━━━━━━━━━━━━━━━━━━━  ┌──────┐  €   │  ← Slider + number input + unit
│  1.000 € bis 20.000 €       │ 8.000│      │  ← Range labels
│                              └──────┘      │
│                                             │
│         ┌───────────────────┐               │
│         │      weiter       │               │
│         └───────────────────┘               │
│              Zurück                         │
│                                             │
│  ✓ Diese Summe steht für die Bestattung     │  ← Green checkmark benefit bullets
│    zur Verfügung. Ihre Hinterbliebenen      │
│    werden so entlastet.                     │
│                                             │
│  ✓ Nur bei Premium: Bei einer schweren      │
│    Krankheit bekommt die versicherte        │
│    Person das Geld auf Wunsch direkt.       │
│                                             │
│  ✓ Nur bei Premium: Versicherungssummen     │
│    auch über 15.000 € möglich.              │
│                                             │
└─────────────────────────────────────────────┘
```

## Files to Create/Modify

### `demo/pages/CoverageAmountPage.tsx`

Key elements:
- Heading: "Wie viel Geld soll für die Beerdigung verfügbar sein?"
- Info tooltip (ⓘ) below heading
- Slider component: min=1000, max=20000, step=1000, with € unit
- Number input synced with slider
- Range label: "1.000 € bis 20.000 €"
- "weiter" button + "Zurück" link
- Three benefit bullet points with green checkmark icons (✓)

### `demo/pages/index.ts` (MODIFY)
Export `CoverageAmountPage` for step 1, sub-step 3.

## Component Usage

```tsx
import { Slider } from "../../src/components/Slider";
import { Button } from "../../src/components/Button";
import { Tooltip } from "../../src/components/Tooltip";
```

## Interaction Logic

- Slider value from `tariffState.coverageAmount` (default: 8000)
- Slider: min=1000, max=20000, step=1000
- Format: German locale number format with € suffix
- "weiter" → step 2, sub-step 1 (also advances the stepper to step 2)
- "Zurück" → step 1, sub-step 2

## Benefit Bullets Data

```typescript
const benefits = [
  "Diese Summe steht für die Bestattung zur Verfügung. Ihre Hinterbliebenen werden so entlastet.",
  "Nur bei Premium: Bei einer schweren Krankheit bekommt die versicherte Person das Geld auf Wunsch direkt.",
  "Nur bei Premium: Versicherungssummen auch über 15.000 € möglich.",
];
```

## Styling Notes

- Green checkmark: color #4CAF50 or similar green, rendered as a circle with checkmark icon
- Benefit text: font-size 14px, color #333, line-height 1.5
- Benefits section: below the buttons, with 16px gap between items
- Each benefit: flex row with checkmark icon (24px) + text

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `screenshots/reference/Screenshot 2026-04-10 111525.png` for visual reference
2. Read `src/components/Slider/Slider.tsx` — note: already has `min`, `max`, `step`, `value`, `onChange`, `unit`, `formatLabel`
3. Create `demo/pages/CoverageAmountPage.tsx` with slider + benefit bullets
4. Update `demo/pages/index.ts`
5. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence below
6. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- Slider range: 1,000–20,000 €, step 1,000, default 8,000
- German number formatting (dots not commas: 8.000)
- Three benefit bullets with green checkmarks, text matches reference exactly
- "weiter" advances stepper to Step 2 (not just sub-step)

### Tester: Navigation Sequence (playwright-cli)
```bash
playwright-cli open http://localhost:3000/wizard --headed
playwright-cli snapshot
playwright-cli fill <day-ref> "23"
playwright-cli fill <month-ref> "06"
playwright-cli fill <year-ref> "1982"
playwright-cli click <weiter-ref>
playwright-cli snapshot
playwright-cli click <middle-radio-ref>
playwright-cli click <weiter-ref>
playwright-cli snapshot
# Now at page 1c (this page)
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Wie viel Geld soll für die Beerdigung verfügbar sein?" visible
[CHECK] Slider visible with range labels "1.000 €" and "20.000 €"
[CHECK] Default value displays "8.000" in number input
[CHECK] Moving slider updates number input
[CHECK] Three benefit bullets with green checkmarks visible
[CHECK] "weiter" navigates to plan selection (stepper shows step 2)
[CHECK] "Zurück" navigates back to start date page
```
