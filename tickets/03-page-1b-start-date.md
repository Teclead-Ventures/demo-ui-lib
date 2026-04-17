# Ticket 03: Page 1b — Geburtsdatum (Birth Date Entry)

## Step: 2 (Risikoprofil) | Sub-step: 2 | Agent: B

## Reference Screenshot
None available — same DateInput pattern as other wizard pages.

## Objective

User enters their birth date (day/month/year). Validates that the resulting age is between 18 and 55. Price and payment duration (67 − age) are derived from this.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│     Wann wurden Sie geboren?             [?]    │  ← H1 serif + Tooltip
│                                                  │
│  ┌────────────────────────────────────┐         │
│  │  Tag    Monat    Jahr              │         │  ← DateInput spinbutton
│  └────────────────────────────────────┘         │
│                                                  │
│  Das Alter bestimmt Ihren Beitrag und            │
│  die Laufzeit bis Rentenalter 67.               │  ← hint text, gray, small
│                                                  │
│    ← Zurück          [ weiter → ]               │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/BirthDatePage.tsx`

```tsx
"use client";
import { useState } from "react";
import { useTariff } from "@/lib/wizard/TariffContext";
import { DateInput } from "@/components/ui/DateInput/DateInput";
import { Button } from "@/components/ui/Button/Button";
import { Tooltip } from "@/components/ui/Tooltip/Tooltip";
import { calculateAge } from "@/lib/data/pricing";

export function BirthDatePage() {
  const { data, update, goNext, goPrev } = useTariff();
  const [error, setError] = useState("");

  const handleNext = () => {
    const { day, month, year } = data.birthDate;
    if (!day || !month || !year) {
      setError("Bitte geben Sie Ihr vollständiges Geburtsdatum an.");
      return;
    }
    const age = calculateAge(data.birthDate);
    if (age < 18 || age > 55) {
      setError("Wir versichern Personen zwischen 18 und 55 Jahren.");
      return;
    }
    setError("");
    goNext();
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
        <h1 style={{
          fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
          fontSize: 28, fontWeight: 700, color: "#333", margin: 0,
        }}>
          Wann wurden Sie geboren?
        </h1>
        <Tooltip content="Das Alter bestimmt Ihren monatlichen Beitrag und die Vertragslaufzeit bis Rentenalter 67." />
      </div>

      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
        <DateInput
          value={data.birthDate}
          onChange={(val) => { update({ birthDate: val }); setError(""); }}
        />
        {error && (
          <p style={{ color: "#d32f2f", fontSize: 14, margin: 0 }}>{error}</p>
        )}
      </div>

      <p style={{ textAlign: "center", color: "#737373", fontSize: 14, margin: 0 }}>
        Das Alter bestimmt Ihren Beitrag und die Laufzeit bis Rentenalter 67.
      </p>

      <div style={{ display: "flex", justifyContent: "center", gap: 16, alignItems: "center" }}>
        <button onClick={goPrev} style={{ background: "none", border: "none", color: "#8e0038", fontWeight: 700, cursor: "pointer", fontSize: 16 }}>
          ← Zurück
        </button>
        <Button label="weiter" onClick={handleNext} variant="primary" style={{ minWidth: 240 }} />
      </div>
    </div>
  );
}
```

### `src/app/wizard/pages/index.ts` (MODIFY)
Add: `export { BirthDatePage } from "./BirthDatePage";`

## Component Usage
```tsx
import { DateInput } from "@/components/ui/DateInput/DateInput";
import { Button } from "@/components/ui/Button/Button";
import { Tooltip } from "@/components/ui/Tooltip/Tooltip";
```
Read all source files before implementing.

## Interaction Logic
- DateInput bound to `data.birthDate` ({day, month, year})
- Validation on "weiter" click: all parts filled + age 18–55
- Error shown inline below DateInput
- "← Zurück" → step 1

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/DateInput/` source
2. Read `src/components/ui/Button/` source
3. Read `src/components/ui/Tooltip/` source
4. Read `src/lib/data/pricing.ts` for `calculateAge`
5. Create `src/app/wizard/pages/BirthDatePage.tsx`
6. Update `src/app/wizard/pages/index.ts`
7. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard --headed
# Click weiter on step 1 to reach step 2
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Wann wurden Sie geboren?" visible with tooltip icon
[CHECK] DateInput with three fields (Tag/Monat/Jahr) rendered
[CHECK] Clicking "weiter" with empty fields shows error message
[CHECK] Entering age <18 shows age range error
[CHECK] Entering age >55 shows age range error
[CHECK] Valid birth date (e.g. 15/03/1990) proceeds to step 3
[CHECK] "← Zurück" returns to step 1
```
