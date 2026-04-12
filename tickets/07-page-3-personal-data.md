# Ticket 07: Page 3 — Personal Data Form

## Step: 3 (Persönliches) | Sub-step: 1

## Reference Screenshot
`screenshots/reference/Screenshot 2026-04-10 171607.png`

## Objective

Build the personal data form where users enter their personal information: salutation, name, address, birth details, and nationality.

## Visual Specification (from reference)

```
┌─────────────────────────────────────────────────┐
│  (1✓) Tarifdaten  (2✓) Beitrag  (3●) Persönl.  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Persönliche Daten des Versicherungs-           │  ← Bold heading, centered
│  nehmers und der zu versichernden Per-           │
│  son                                            │
│                                                 │
│  Bei der Verarbeitung von personenbezogenen     │  ← Privacy notice text block
│  Daten beachtet ERGO die Vorschriften der       │  ← (small, gray, bordered)
│  EU-Datenschutz-Grundverordnung...              │
│                                                 │
│  Anrede                                         │
│  ○ Herr  ○ Frau                                 │  ← InlineRadio
│                                                 │
│  Vorname                                        │
│  ┌──────────────────────────────────────┐       │  ← TextInput
│  │                                      │       │
│  └──────────────────────────────────────┘       │
│                                                 │
│  Nachname                                       │
│  ┌──────────────────────────────────────┐       │  ← TextInput
│  │                                      │       │
│  └──────────────────────────────────────┘       │
│                                                 │
│  Straße / Nr.                                   │
│  ┌──────────────────────────────────────┐       │  ← TextInput
│  │                                      │       │
│  └──────────────────────────────────────┘       │
│                                                 │
│  PLZ / Ort                                      │
│  ┌────────┐ ┌───────────────────────────┐       │  ← Two TextInputs side by side
│  │        │ │                           │       │
│  └────────┘ └───────────────────────────┘       │
│                                                 │
│  Geburtsdatum                                   │
│  ┌──────┐ ┌──────┐ ┌────────┐                   │  ← DateInput (pre-filled from 1a)
│  │  23  │ │  06  │ │  1982  │                   │
│  └──────┘ └──────┘ └────────┘                   │
│                                                 │
│  Geburtsort                                     │
│  ┌──────────────────────────────────────┐       │  ← TextInput
│  │                                      │       │
│  └──────────────────────────────────────┘       │
│                                                 │
│  Staatsangehörigkeit                            │
│  ┌──────────────────────────────────────┐       │  ← Select dropdown
│  │  Bitte wählen                    ▼   │       │
│  └──────────────────────────────────────┘       │
│                                                 │
│         ┌───────────────────┐                   │
│         │      weiter       │                   │
│         └───────────────────┘                   │
│              Zurück                             │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `demo/pages/PersonalDataPage.tsx`

Key form fields:
1. **Anrede**: InlineRadio (Herr / Frau)
2. **Vorname**: TextInput
3. **Nachname**: TextInput
4. **Straße / Nr.**: TextInput
5. **PLZ / Ort**: Two TextInputs side by side (PLZ ~30% width, Ort ~70% width)
6. **Geburtsdatum**: DateInput (pre-filled from step 1a `tariffState.birthDate`)
7. **Geburtsort**: TextInput
8. **Staatsangehörigkeit**: Select dropdown

### `demo/pages/index.ts` (MODIFY)
Export `PersonalDataPage` for step 3, sub-step 1.

## Component Usage

```tsx
import { InlineRadio } from "../../src/components/InlineRadio";
import { TextInput } from "../../src/components/TextInput";
import { DateInput } from "../../src/components/DateInput";
import { Select } from "../../src/components/Select";
import { Button } from "../../src/components/Button";
```

## Interaction Logic

- All form fields read from and write to the tariff context
- **Geburtsdatum** is pre-filled from `tariffState.birthDate` (entered in step 1a) but still editable
- **Anrede**: options "Herr" and "Frau" (values: "herr", "frau")
- **Staatsangehörigkeit**: Select with common nationalities ("deutsch", "österreichisch", "schweizerisch", etc.)
- "weiter" → step 4 (summary) — optionally validate required fields
- "Zurück" → step 2, sub-step 2

## Privacy Notice Text

```
Bei der Verarbeitung von personenbezogenen Daten beachtet ERGO die Vorschriften der EU-Datenschutz-Grundverordnung. Ausführliche Informationen finden Sie in unseren Datenschutzhinweisen. Für Anforderung eines Angebots erhalten Sie die Informationen in Ihren Vertragsunterlagen. Ihre Daten speichern wir und der Versicherer so mindestens 10 Tage, bei einer Angebotserstellung für 6 Monate. Das Formell ist für Sie kostenlos. Bei konkreter Interesse, wenn Sie nähere Informationen wünschen, fragen Sie einfach.
```

## Styling Notes

- Heading: same centered bold style as other pages
- Privacy notice: font-size 12px, color #737373, border 1px solid #e1e1e1, padding 16px, border-radius 4px
- Form fields: stacked vertically, gap 20px
- PLZ / Ort row: flex row, PLZ field ~120px, Ort fills remaining space, gap 12px
- Form max-width: ~480px, centered

---

## Agent Execution (see tickets/agent-contracts.md for full role definitions)

**This ticket is executed by a Page Agent (developer role) running in an isolated worktree.**

### Page Agent Actions
1. Read `screenshots/reference/Screenshot 2026-04-10 171607.png` carefully
2. Read `src/components/InlineRadio/InlineRadio.tsx`, `src/components/TextInput/TextInput.tsx`, `src/components/Select/Select.tsx` for APIs
3. Read `demo/context/TariffContext.tsx` for personal data fields in state
4. Create `demo/pages/PersonalDataPage.tsx` with all 8 form fields
5. Pre-fill Geburtsdatum from `tariffState.birthDate`
6. Add privacy notice text block
7. Update `demo/pages/index.ts`
8. Run quality gate loop (max 3 iterations):
   - **compile-gate**: `npx tsc --noEmit` must exit 0
   - **review-gate**: Spawn Reviewer subagent (opus) with this ticket + code files
   - **browser-gate**: Spawn Tester subagent (opus) with navigation sequence below
9. Escalate to orchestrator if any gate fails 3 times

### Reviewer Focus (in addition to standard checks)
- All 8 form fields present: Anrede, Vorname, Nachname, Straße/Nr., PLZ, Ort, Geburtsdatum, Geburtsort, Staatsangehörigkeit
- PLZ / Ort as side-by-side row (PLZ ~120px, Ort fills rest)
- Geburtsdatum pre-filled from `tariffState.birthDate` (step 1a)
- All fields write to context via dispatch
- Privacy notice text block with correct styling (small, gray, bordered)

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
playwright-cli click <accept-dynamic-ref>  # "auswählen und weiter"
playwright-cli snapshot
# Now at page 3 (this page), stepper shows step 3 "Persönliches" active
```

### Tester: Page-Specific Checks
```
[CHECK] Heading about personal data visible
[CHECK] Privacy notice text block visible
[CHECK] All 8 form fields render: Anrede, Vorname, Nachname, Straße, PLZ, Ort, Geburtsdatum, Geburtsort, Staatsangehörigkeit
[CHECK] Geburtsdatum pre-filled with 23/06/1982 from step 1a
[CHECK] InlineRadio toggles between Herr/Frau
[CHECK] Can fill text fields and select nationality
[CHECK] PLZ and Ort appear side-by-side (not stacked)
[CHECK] "weiter" navigates to summary page (step 4)
[CHECK] "Zurück" navigates back to dynamic adjustment page
```
