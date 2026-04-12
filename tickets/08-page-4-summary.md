# Ticket 08: Page 4 — Summary (Zusammenfassung)

## Step: 4 (Zusammenfassung) | Sub-step: 1

## Reference Screenshot
**None available.** This page is implied by the stepper but not captured in reference screenshots. Design based on standard insurance summary page patterns and the ERGO design tokens used in all other pages.

**Impact on review/test loop**: Reviewer should mark `VISUAL_FIDELITY: N/A` and skip the "German text matches reference screenshot exactly" check. Tester should mark `VISUAL_COMPARISON: Assessment: N/A — no reference screenshot` and focus on functional checks instead.

## Objective

Build the summary page that displays all collected data from previous steps for review before final submission. This is the last step of the wizard.

## Visual Specification (inferred from design system)

```
┌─────────────────────────────────────────────────┐
│  (1✓) Tarifd.  (2✓) Beitrag  (3✓) Pers.  (4●)  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Zusammenfassung Ihres Antrags                  │  ← Bold heading, centered
│                                                 │
│  Bitte überprüfen Sie Ihre Angaben              │  ← Subtitle, gray
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Tarifdaten                        ✎   │    │  ← Section card with edit link
│  │  Geburtsdatum:      23.06.1982          │    │
│  │  Versicherungsbeginn: 01.06.2026        │    │
│  │  Versicherungssumme: 8.000 €            │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Ihr Tarif                         ✎   │    │
│  │  Tarif:             Komfort             │    │
│  │  Monatlicher Beitrag: 24,25 €           │    │
│  │  Beitragsdynamik:  Ja / Nein            │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Persönliche Daten                 ✎   │    │
│  │  Anrede:            Herr                │    │
│  │  Name:              Max Mustermann      │    │
│  │  Adresse:           Musterstr. 1        │    │
│  │                     12345 Berlin        │    │
│  │  Geburtsdatum:      23.06.1982          │    │
│  │  Geburtsort:        Berlin              │    │
│  │  Staatsangehörigkeit: deutsch           │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ☐ Ich stimme den Allgemeinen Versicherungs-    │  ← Checkbox
│    bedingungen zu.                              │
│  ☐ Ich habe die Datenschutzhinweise zur         │  ← Checkbox
│    Kenntnis genommen.                           │
│                                                 │
│         ┌───────────────────────────┐           │
│         │  Jetzt verbindlich        │           │  ← Primary button
│         │  abschließen              │           │
│         └───────────────────────────┘           │
│              Zurück                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `demo/pages/SummaryPage.tsx`

Key sections:
1. **Heading**: "Zusammenfassung Ihres Antrags"
2. **Subtitle**: "Bitte überprüfen Sie Ihre Angaben"
3. **Tarifdaten Card**: Birth date, insurance start, coverage amount — with edit link (✎) navigating back to step 1
4. **Tarif Card**: Selected plan, monthly price, dynamic adjustment — with edit link to step 2
5. **Personal Data Card**: All personal info — with edit link to step 3
6. **Consent Checkboxes**: Two checkboxes (AVB + Datenschutz)
7. **Submit Button**: "Jetzt verbindlich abschließen" — shows success toast on click
8. **"Zurück"**: Navigate back to step 3

### `demo/pages/index.ts` (MODIFY)
Export `SummaryPage` for step 4, sub-step 1.

## Component Usage

```tsx
import { Card } from "../../src/components/Card";
import { Checkbox } from "../../src/components/Checkbox";
import { Button } from "../../src/components/Button";
import { useToast } from "../../src/components/Toast";
```

## Interaction Logic

- All data read from `tariffState` (read-only display)
- Edit links (✎) navigate back to the corresponding step (using `wizardNav.goTo(step, subStep)`)
- Two consent checkboxes — local state, both must be checked to enable submit button
- "Jetzt verbindlich abschließen" → shows success toast: "Ihr Antrag wurde erfolgreich eingereicht!"
- "Zurück" → step 3, sub-step 1

## Summary Data Display

Format data from context:
- Birth date: `${birthDate.day}.${birthDate.month}.${birthDate.year}`
- Coverage: `${coverageAmount.toLocaleString("de-DE")} €`
- Plan name: capitalize first letter (grundschutz → Grundschutz)
- Monthly price: from planData lookup
- Dynamic adjustment: "Ja" or "Nein"
- Personal name: `${firstName} ${lastName}`
- Address: `${street}\n${zipCity}`

## Styling Notes

- Summary cards: border 1px solid #e1e1e1, border-radius 8px, padding 20px
- Card header: flex row, title bold + edit link right-aligned
- Edit link (✎): color #8e0038, cursor pointer, font-size 14px
- Data rows: label-value pairs, label color #737373, value color #333
- Gap between cards: 16px
- Consent section: margin-top 24px
- Submit button: full-width, primary, max-width ~360px, centered

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `demo/context/TariffContext.tsx` for the full state shape
2. Read `demo/data/planData.ts` for plan pricing (may need to create from ticket 05 spec if not in worktree)
3. Read `src/components/Card/Card.tsx`, `src/components/Checkbox/Checkbox.tsx`, `src/components/Toast/Toast.tsx` for APIs
4. Create `demo/pages/SummaryPage.tsx` with three summary cards + consent + submit
5. Implement edit links navigating to specific steps via `wizardNav.goTo(step, subStep)`
6. Update `demo/pages/index.ts`
7. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence below
8. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- Three summary cards: Tarifdaten, Tarif, Persönliche Daten — with correct data grouping
- Edit links (pencil icon) navigate to correct step/subStep for each section
- Data formatting: German locale (dots in numbers, DD.MM.YYYY dates, comma for decimals)
- Monthly price looked up from planData, not hardcoded
- Submit button DISABLED until both consent checkboxes checked
- Success toast shown on submit: "Ihr Antrag wurde erfolgreich eingereicht!"

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
playwright-cli click <weiter-ref>  # accept default plan
playwright-cli snapshot
playwright-cli click <accept-dynamic-ref>
playwright-cli snapshot
# Fill personal data
playwright-cli click <herr-radio-ref>
playwright-cli fill <vorname-ref> "Max"
playwright-cli fill <nachname-ref> "Mustermann"
playwright-cli fill <strasse-ref> "Musterstraße 1"
playwright-cli fill <plz-ref> "10115"
playwright-cli fill <ort-ref> "Berlin"
playwright-cli fill <geburtsort-ref> "Hamburg"
playwright-cli select <staatsangehoerigkeit-ref> "deutsch"
playwright-cli click <weiter-ref>
playwright-cli snapshot
# Now at page 4 (this page), stepper shows step 4 "Zusammenfassung" active
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Zusammenfassung Ihres Antrags" visible
[CHECK] Three summary cards visible (Tarifdaten, Tarif, Persönliche Daten)
[CHECK] Tarifdaten card shows birth date "23.06.1982", start date, coverage "8.000 €"
[CHECK] Tarif card shows "Komfort" and monthly price
[CHECK] Personal data card shows "Herr Max Mustermann", address, birth details
[CHECK] Edit link on Tarifdaten card navigates back to step 1
[CHECK] Edit link on Tarif card navigates back to step 2
[CHECK] Submit button is disabled when checkboxes unchecked
[CHECK] Checking both checkboxes enables submit button
[CHECK] Clicking submit shows success toast
[CHECK] "Zurück" navigates to personal data page
```
