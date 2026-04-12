# Ticket 05: Page 2a — Plan Selection

## Step: 2 (Beitrag) | Sub-step: 1

## Reference Screenshot
`screenshots/reference/Screenshot 2026-04-10 171511.png`

## Objective

Build the plan selection page where users choose between Grundschutz, Komfort, and Premium tiers. This is the most complex page — it displays pricing, a benefit breakdown, and payment details.

## Visual Specification (from reference)

```
┌─────────────────────────────────────────────────┐
│  (1) Tarifdaten  (2●) Beitrag  (3) ...          │
├─────────────────────────────────────────────────┤
│                                                 │
│  Wählen Sie Ihren passenden Schutz              │  ← Bold heading, centered
│                                                 │
│  Garantierte Versicherungssumme:                │
│  7.000 €                                        │  ← Large, bold amount
│  bei monatlicher Beitragszahlung und einer      │
│  Beitragszahlungsdauer von 44 Jahren            │  ← Small gray text
│                                                 │
│  ┌────────────┬────────────┬────────────┐       │
│  │Grundschutz │  Komfort●  │  Premium   │       │  ← SegmentedControl
│  └────────────┴────────────┴────────────┘       │
│                                                 │
│  Sie zahlen   24,25 €  monatlich                │  ← Large price display
│                                                 │
│  ◉ Garantierte Todesfallleistung: 7.000,00 €   │  ← Benefit list with checkmarks
│  ◉ Gesamtleistung inkl. Überschussbeteiligung:  │
│    10.534,69 €                                  │
│  ◉ Aufsicht ab Vertragsbeginn: 18 Monate       │
│                                                 │
│  Sie zahlen Beitrag ab 01.06.2073. Danach sind  │
│  Sie beitragsfrei und die Leistung versichert.  │
│                                                 │
│  ▼ Alle Leistungen anzeigen                     │  ← Expandable link
│                                                 │
│  Zahlweise:             monatlich     ▼         │  ← Details row
│  Todesfallsumme:        7.000 €                 │
│  Beitragszahlungsdauer: 44 Jahre                │
│                                                 │
│         ┌───────────────────────────┐           │
│         │  weiter zum Online-Antrag │           │
│         └───────────────────────────┘           │
│              Zurück                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `demo/pages/PlanSelectionPage.tsx`

This is the most content-rich page. Key sections:

1. **Header**: Heading + guaranteed sum display
2. **Plan Selector**: SegmentedControl (Grundschutz / Komfort / Premium)
3. **Price Display**: Monthly amount, prominently shown
4. **Benefits List**: Checkmark items that change per plan
5. **Details Section**: Zahlweise, Todesfallsumme, Beitragszahlungsdauer
6. **"Alle Leistungen anzeigen"**: Expandable section (toggle visibility)
7. **Navigation**: "weiter zum Online-Antrag" + "Zurück"

### `demo/data/planData.ts` (CREATE)
Static plan data for the three tiers:

```typescript
export const planData = {
  grundschutz: {
    monthlyPrice: 19.85,
    benefits: [
      { label: "Garantierte Todesfallleistung", value: "7.000,00 €" },
      { label: "Gesamtleistung inkl. Überschussbeteiligung", value: "9.245,30 €" },
      { label: "Aufsicht ab Vertragsbeginn", value: "18 Monate" },
    ],
    paymentEndNote: "Sie zahlen Beitrag bis 01.06.2073. Danach sind Sie beitragsfrei und die Leistung versichert.",
  },
  komfort: {
    monthlyPrice: 24.25,
    benefits: [
      { label: "Garantierte Todesfallleistung", value: "7.000,00 €" },
      { label: "Gesamtleistung inkl. Überschussbeteiligung", value: "10.534,69 €" },
      { label: "Aufsicht ab Vertragsbeginn", value: "18 Monate" },
    ],
    paymentEndNote: "Sie zahlen Beitrag bis 01.06.2073. Danach sind Sie beitragsfrei und die Leistung versichert.",
  },
  premium: {
    monthlyPrice: 29.90,
    benefits: [
      { label: "Garantierte Todesfallleistung", value: "7.000,00 €" },
      { label: "Gesamtleistung inkl. Überschussbeteiligung", value: "12.180,42 €" },
      { label: "Schwere Krankheiten: Sofortleistung", value: "Ja" },
      { label: "Aufsicht ab Vertragsbeginn", value: "3 Monate" },
    ],
    paymentEndNote: "Sie zahlen Beitrag bis 01.06.2073. Danach sind Sie beitragsfrei und die Leistung versichert.",
  },
};
```

### `demo/pages/index.ts` (MODIFY)
Export `PlanSelectionPage` for step 2, sub-step 1.

## Component Usage

```tsx
import { SegmentedControl } from "../../src/components/SegmentedControl";
import { Button } from "../../src/components/Button";
import { Link } from "../../src/components/Link";
```

## Interaction Logic

- SegmentedControl value from `tariffState.plan` (default: "komfort")
- Switching plan updates displayed price and benefits immediately
- Guaranteed sum = `tariffState.coverageAmount` (from previous step), formatted as "X.XXX €"
- Payment duration calculated: ~44 years (can be hardcoded for demo)
- "Alle Leistungen anzeigen": local toggle state, reveals extended benefit list
- "weiter zum Online-Antrag" → step 2, sub-step 2
- "Zurück" → step 1, sub-step 3

## Styling Notes

- Guaranteed sum: font-size 28px, font-weight 700
- Monthly price: font-size 32px, font-weight 700, inline with "Sie zahlen" and "monatlich"
- Benefit checkmarks: green circle icons (same style as coverage page)
- Details section: subtle border-top, label-value pairs in a grid
- "Alle Leistungen anzeigen": styled as a link with down-arrow indicator

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `screenshots/reference/Screenshot 2026-04-10 171511.png` carefully — this is the densest page
2. Read `src/components/SegmentedControl/SegmentedControl.tsx` for the API
3. Create `demo/data/planData.ts` with pricing data for all three tiers
4. Create `demo/pages/PlanSelectionPage.tsx` with all sections
5. Wire SegmentedControl to context, display `tariffState.coverageAmount` as guaranteed sum
6. Implement collapsible "Alle Leistungen anzeigen" section
7. Update `demo/pages/index.ts`
8. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence below
9. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- All three plan tiers display DIFFERENT prices and benefits
- Guaranteed sum reflects `tariffState.coverageAmount` from step 1c (not hardcoded)
- Price format: XX,XX € monatlich (German comma for decimals)
- "Alle Leistungen anzeigen" expand/collapse works
- Details section present: Zahlweise, Todesfallsumme, Beitragszahlungsdauer
- Layout density matches reference (this is the most complex page)

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
# Accept default slider (8.000)
playwright-cli click <weiter-ref>
playwright-cli snapshot
# Now at page 2a (this page), stepper shows step 2 "Beitrag" active
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Wählen Sie Ihren passenden Schutz" visible
[CHECK] SegmentedControl shows Grundschutz / Komfort / Premium
[CHECK] Default selection is "Komfort"
[CHECK] Switching to "Grundschutz" updates price display to different value
[CHECK] Switching to "Premium" updates price and shows additional benefits
[CHECK] "Alle Leistungen anzeigen" toggles content visibility
[CHECK] Guaranteed sum shows value from step 1c (e.g. "8.000 €")
[CHECK] "weiter zum Online-Antrag" navigates to dynamic adjustment page
[CHECK] "Zurück" navigates back to coverage amount page
```
