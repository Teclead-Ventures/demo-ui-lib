# Ticket 02: Page 1a — Berufsgruppe (Occupation Selection)

## Step: 1 (Risikoprofil) | Sub-step: 1 | Agent: A

## Reference Screenshot
None available — design from spec below.

## Objective

User selects their occupation group. This determines the risk class multiplier for pricing. 4 options presented as radio card buttons.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│     Was ist Ihr Beruf?                          │  ← H1, serif, centered
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │ ○  Bürotätigkeit / kaufmännisch         │   │  ← RadioButton card
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ ○  Handwerk / Techniker                 │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ ○  Schwere körperliche Arbeit           │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ ○  Gefahrenberufe                       │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│              [ weiter → ]                       │  ← Button, primary
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/OccupationPage.tsx`

```tsx
"use client";
import { useTariff, type OccupationType } from "@/lib/wizard/TariffContext";
import { RadioButton } from "@/components/ui/RadioButton/RadioButton";
import { Button } from "@/components/ui/Button/Button";

const OPTIONS: Array<{ value: OccupationType; label: string }> = [
  { value: "buero",       label: "Bürotätigkeit / kaufmännisch" },
  { value: "handwerk",    label: "Handwerk / Techniker" },
  { value: "koerperlich", label: "Schwere körperliche Arbeit" },
  { value: "gefahren",    label: "Gefahrenberufe" },
];

export function OccupationPage() {
  const { data, update, goNext } = useTariff();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
      <h1 style={{
        fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
        fontSize: 28, fontWeight: 700, color: "#333", textAlign: "center", margin: 0,
      }}>
        Was ist Ihr Beruf?
      </h1>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {OPTIONS.map((opt) => (
          <RadioButton
            key={opt.value}
            label={opt.label}
            checked={data.occupation === opt.value}
            onChange={() => update({ occupation: opt.value })}
          />
        ))}
      </div>

      <div style={{ display: "flex", justifyContent: "center" }}>
        <Button label="weiter" onClick={goNext} variant="primary" style={{ minWidth: 240 }} />
      </div>
    </div>
  );
}
```

### `src/app/wizard/pages/index.ts` (MODIFY)
Add: `export { OccupationPage } from "./OccupationPage";`

## Component Usage
```tsx
import { RadioButton } from "@/components/ui/RadioButton/RadioButton";
import { Button } from "@/components/ui/Button/Button";
```
Read both source files before implementing.

## Interaction Logic
- One option selected at a time, default: "buero"
- Selecting an option immediately updates `data.occupation`
- No validation needed — always has a value
- "weiter" always enabled

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/RadioButton/` source
2. Read `src/components/ui/Button/` source
3. Read `src/lib/wizard/TariffContext.tsx` for OccupationType
4. Create `src/app/wizard/pages/OccupationPage.tsx`
5. Update `src/app/wizard/pages/index.ts`
6. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard --headed
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Was ist Ihr Beruf?" visible
[CHECK] 4 radio options rendered as cards
[CHECK] "Bürotätigkeit / kaufmännisch" pre-selected
[CHECK] Clicking another option selects it and deselects previous
[CHECK] "weiter" button navigates to step 2 (Geburtsdatum)
```
