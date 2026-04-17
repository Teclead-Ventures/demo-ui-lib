# Orchestration Plan: Berufsunfähigkeitsversicherung Wizard

## Overview

Build a fully functional full-stack insurance tariff wizard (BU) with 7 pages across 5 wizard steps. The pipeline uses parallel agents for all page components, with a shared TariffContext for state management.

## Wizard Flow

```
Step 1: Risikoprofil
  1a → OccupationPage     — Berufsgruppe auswählen (4 radio options)
  1b → BirthDatePage      — Geburtsdatum eingeben
  1c → CoveragePage       — Einkommen + BU-Rente konfigurieren

Step 2: Tarifauswahl
  2a → PlanSelectionPage  — Grundschutz / Komfort / Premium wählen (live pricing)

Step 3: Gesundheit
  3a → HealthQuestionsPage — Raucher? + Vorerkrankungen? (inline radio)

Step 4: Persönliches
  4a → PersonalDataPage   — Name, Adresse

Step 5: Zusammenfassung
  5a → SummaryPage        — Review + Consent + Submit
```

## File Structure

```
src/
├── app/
│   ├── wizard/
│   │   ├── page.tsx              ← TariffProvider + step routing
│   │   └── pages/
│   │       ├── OccupationPage.tsx
│   │       ├── BirthDatePage.tsx
│   │       ├── CoveragePage.tsx
│   │       ├── PlanSelectionPage.tsx
│   │       ├── HealthQuestionsPage.tsx
│   │       ├── PersonalDataPage.tsx
│   │       ├── SummaryPage.tsx
│   │       └── index.ts
│   ├── dashboard/
│   │   └── page.tsx
│   └── api/
│       ├── submit/route.ts
│       └── track/route.ts
└── lib/
    ├── wizard/
    │   └── TariffContext.tsx
    └── data/
        ├── pricing.ts
        └── planData.ts
```

## Pricing Formula (Template A)

```
units = coverageAmount / 100
t = (age - 18) / (55 - 18)
ageFactor = 0.70 + 0.50×t + (−0.15)×t²
riskMult: buero=1.0, handwerk=1.4, koerperlich=1.8, gefahren=2.2
netPremium = baseRate × units × ageFactor × riskMult
gross = netPremium × 1.28
```

Calibration: 30yo Bürotätigkeit, €2k/Monat, Komfort → ~€55/Monat ✓

## Agent Assignments

| Agent | Ticket file | Page component |
|-------|-------------|----------------|
| A | 02-page-1a-birth-date.md | OccupationPage |
| B | 03-page-1b-start-date.md | BirthDatePage |
| C | 04-page-1c-coverage-amount.md | CoveragePage |
| D | 05-page-2a-plan-selection.md | PlanSelectionPage |
| E | 06-page-2b-dynamic-adjustment.md | HealthQuestionsPage |
| F | 07-page-3-personal-data.md | PersonalDataPage |
| G | 08-page-4-summary.md | SummaryPage |

## TARIFF_STEPS (7 steps)

```typescript
export const TARIFF_STEPS = [
  { label: "Risikoprofil" },     // steps 1-3 (substeps of Risikoprofil)
  { label: "Tarifauswahl" },
  { label: "Gesundheit" },
  { label: "Persönliches" },
  { label: "Zusammenfassung" },
];
// Note: The stepper shows 5 labels but the wizard has 7 internal steps.
// Steps 1/2/3 all display under "Risikoprofil" in the stepper.
// Internal step routing: 1=Occupation, 2=BirthDate, 3=Coverage, 4=PlanSelection,
//                         5=HealthQuestions, 6=PersonalData, 7=Summary
```

## Design Reference

- Background: #f8f8f8
- Content maxWidth: 640px, padding: 48px 24px
- Headings: Source Serif 4, 28px, #333, centered
- Primary color: #8e0038 (ERGO red)
- Stepper circles: active=red, completed=red+✓, inactive=gray
- Buttons: primary variant, maxWidth 360px, centered
- Back link: plain text "← Zurück", color #8e0038
- Card border: 1px solid #e5e5e5, radius 8px, white bg
- Benefit checkmarks: color #5de38e
