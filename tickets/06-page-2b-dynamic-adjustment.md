# Ticket 06: Page 2b — Dynamic Adjustment (Beitragsdynamik)

## Step: 2 (Beitrag) | Sub-step: 2

## Reference Screenshot
`screenshots/reference/Screenshot 2026-04-10 171544.png`

## Objective

Build the dynamic contribution adjustment page. The user decides whether their insurance contributions should increase over time to keep pace with inflation.

## Visual Specification (from reference)

```
┌─────────────────────────────────────────────────┐
│  (1) Tarifdaten  (2●) Beitrag  (3) ...          │
├─────────────────────────────────────────────────┤
│                                                 │
│  ◉ Grundschutz    23,80 €  monatlich            │  ← Plan summary bar (from 2a)
│  ▼ Mehr Details zeigen                          │  ← Collapsible detail link
│                                                 │
│  Soll sich die Absicherung der Zukunft          │  ← Bold heading, centered
│  anpassen?                                      │
│                                                 │
│  Wählen Sie eine Dynamik:                       │  ← Subheading
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Beitragsdynamik                        │    │
│  │                                         │    │
│  │  Die Lebenshaltungskosten steigen        │    │  ← Explanation text block
│  │  stetig, so verliert das Geld über die   │    │
│  │  Zeit an Wert. Mit einer freiwilligen    │    │
│  │  Beitragserhöhung um 5 % erhöhen Sie    │    │
│  │  jährlich Ihren Versicherungsschutz...   │    │
│  │                                         │    │
│  │  Eine Erhöhung kann auch nachträglich    │    │
│  │  abgeschlossen werden. Auf die Erhöhung │    │
│  │  kann auch noch verzichtet werden.       │    │
│  │                                         │    │
│  │        ┌──────────────────────┐         │    │
│  │        │ auswählen und weiter │         │    │  ← Primary button
│  │        └──────────────────────┘         │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Ich möchte keine Beitragsdynamik.      │    │  ← Alternative option
│  │                             weiter →    │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│         Angebot anfordern                       │  ← Secondary action link
│              Zurück                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `demo/pages/DynamicAdjustmentPage.tsx`

Key elements:
1. **Plan summary bar**: Shows selected plan name + monthly price (from context)
2. **"Mehr Details zeigen"**: Collapsible detail link
3. **Heading**: "Soll sich die Absicherung der Zukunft anpassen?"
4. **Sub-heading**: "Wählen Sie eine Dynamik:"
5. **Beitragsdynamik card**: Explanation text + "auswählen und weiter" button
6. **No-dynamic option**: "Ich möchte keine Beitragsdynamik." with "weiter →" link
7. **"Angebot anfordern"**: Secondary link (non-functional for demo, or shows toast)
8. **"Zurück"**: Navigate back to plan selection

### `demo/pages/index.ts` (MODIFY)
Export `DynamicAdjustmentPage` for step 2, sub-step 2.

## Component Usage

```tsx
import { Button } from "../../src/components/Button";
import { Card } from "../../src/components/Card";
import { Link } from "../../src/components/Link";
```

## Interaction Logic

- Plan summary reads from `tariffState.plan` + planData pricing
- "auswählen und weiter" → sets `dynamicAdjustment: "standard"`, navigates to step 3
- "weiter" (no dynamic) → sets `dynamicAdjustment: "none"`, navigates to step 3
- "Angebot anfordern" → show info toast or no-op for demo
- "Zurück" → step 2, sub-step 1

## Styling Notes

- Plan summary bar: background #f5f5f5, padding 16px, border-radius 8px
- Price: font-size 24px, font-weight 700
- Beitragsdynamik card: border 1px solid #e1e1e1, padding 24px, border-radius 8px
- Explanation text: font-size 14px, color #555, line-height 1.6
- "auswählen und weiter": primary button, centered within card
- No-dynamic row: lighter card style, with "weiter →" as a link on the right
- "Angebot anfordern": secondary link style, centered

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `screenshots/reference/Screenshot 2026-04-10 171544.png` carefully
2. Read `demo/data/planData.ts` for plan pricing (created in ticket 05, may need to create if not present in worktree — copy the data from ticket 05 spec)
3. Create `demo/pages/DynamicAdjustmentPage.tsx`
4. Implement plan summary bar, explanation card, and no-dynamic alternative
5. Wire both navigation paths to set `dynamicAdjustment` and advance to step 3
6. Update `demo/pages/index.ts`
7. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence below
8. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- Plan summary bar shows selected plan name + price from context (not hardcoded)
- Two distinct paths: "auswählen und weiter" sets `dynamicAdjustment: "standard"`, "weiter" (no dynamic) sets `"none"`
- Both paths navigate to step 3
- Explanation text matches Beitragsdynamik reference content
- "Mehr Details zeigen" collapsible works

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
playwright-cli click <weiter-ref>  # accept default slider
playwright-cli snapshot
playwright-cli click <weiter-ref>  # accept default plan (Komfort)
playwright-cli snapshot
# Now at page 2b (this page)
```

### Tester: Page-Specific Checks
```
[CHECK] Plan summary shows "Komfort" with correct price from planData
[CHECK] Heading "Soll sich die Absicherung der Zukunft anpassen?" visible
[CHECK] Beitragsdynamik explanation card visible with descriptive text
[CHECK] "auswählen und weiter" navigates to personal data page (step 3)
[CHECK] Navigate back, select "Ich möchte keine Beitragsdynamik" + "weiter" also reaches step 3
[CHECK] "Zurück" navigates back to plan selection page
```
