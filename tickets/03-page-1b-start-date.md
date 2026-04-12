# Ticket 03: Page 1b — Insurance Start Date

## Step: 1 (Tarifdaten) | Sub-step: 2

## Reference Screenshot
`screenshots/reference/Screenshot 2026-04-10 111815.png`

## Objective

Build the insurance start date selection page. The user picks when their insurance policy should begin from three pre-defined date options using radio buttons.

## Visual Specification (from reference)

```
┌─────────────────────────────────────────────┐
│  (1) Tarifdaten  (2) Beitrag  (3) ...       │
├─────────────────────────────────────────────┤
│                                             │
│  Wann soll die Versicherung beginnen?       │  ← Bold heading, centered
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  ○  01.05.2026                      │    │  ← RadioButton, card-style
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │  ◉  01.06.2026                      │    │  ← Selected, highlighted bg
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │  ○  01.07.2026                      │    │  ← RadioButton
│  └─────────────────────────────────────┘    │
│                                             │
│         ┌───────────────────┐               │
│         │      weiter       │               │
│         └───────────────────┘               │
│              Zurück                         │  ← Ghost link, centered
│                                             │
└─────────────────────────────────────────────┘
```

## Files to Create/Modify

### `demo/pages/StartDatePage.tsx`

Key elements:
- Heading: "Wann soll die Versicherung beginnen?"
- Three RadioButton options with dates (dynamically generated: 1st of next 3 months)
- Selected radio has light pink background highlight
- "weiter" button → navigate to sub-step 3
- "Zurück" link → navigate back to sub-step 1

### `demo/pages/index.ts` (MODIFY)
Export `StartDatePage` and wire it for step 1, sub-step 2.

## Component Usage

```tsx
import { RadioButton } from "../../src/components/RadioButton";
import { Button } from "../../src/components/Button";
```

## Interaction Logic

- Three date options: 1st of the next 3 upcoming months from today
- Selected value stored in `tariffState.insuranceStart`
- Default: middle option (2nd month)
- "weiter" → step 1, sub-step 3
- "Zurück" → step 1, sub-step 1

## Styling Notes

- Heading: same style as other pages (bold, centered, ~24px)
- RadioButtons: full-width, card-style (the RadioButton component already renders as cards)
- Gap between radio options: 8-12px
- "weiter" button: max-width ~360px, centered
- "Zurück": centered text link below button, color #333, font-size 14px

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `screenshots/reference/Screenshot 2026-04-10 111815.png` for visual reference
2. Read `src/components/RadioButton/RadioButton.tsx` for the API
3. Read `demo/context/TariffContext.tsx` for state and navigation
4. Create `demo/pages/StartDatePage.tsx`
5. Generate date options dynamically (1st of next 3 months)
6. Update `demo/pages/index.ts`
7. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence below
8. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- Dates dynamically calculated (not hardcoded to specific months)
- Default selection is middle option
- Radio selected state has pink highlight matching reference

### Tester: Navigation Sequence (playwright-cli)
```bash
playwright-cli open http://localhost:3000/wizard --headed
playwright-cli snapshot
# Fill birth date fields (use snapshot refs)
playwright-cli fill <day-ref> "23"
playwright-cli fill <month-ref> "06"
playwright-cli fill <year-ref> "1982"
playwright-cli click <weiter-ref>
playwright-cli snapshot
# Now at page 1b (this page)
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Wann soll die Versicherung beginnen?" visible
[CHECK] Three radio options visible with DD.MM.YYYY date labels
[CHECK] Middle option selected by default
[CHECK] Clicking different option changes selection
[CHECK] "weiter" navigates to coverage amount page
[CHECK] "Zurück" navigates back to birth date page
```
