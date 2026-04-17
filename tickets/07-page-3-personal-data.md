# Ticket 07: Page 3 — Persönliche Daten (Personal Data Form)

## Step: 6 (Persönliches) | Sub-step: 1 | Agent: F

## Reference Screenshot
None available — standard personal data form.

## Objective

Collect name and address. Standard form with Select (Anrede), TextInputs, and PLZ/Ort side-by-side layout.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│     Ihre persönlichen Daten                     │  ← H1, serif, centered
│                                                  │
│  Anrede                                          │
│  ┌──────────────────────────────────────────┐  │
│  │  Bitte wählen ▼                          │  │  ← Select
│  └──────────────────────────────────────────┘  │
│  Vorname                                         │
│  ┌──────────────────────────────────────────┐  │
│  │                                          │  │  ← TextInput
│  └──────────────────────────────────────────┘  │
│  Nachname                                        │
│  ┌──────────────────────────────────────────┐  │
│  └──────────────────────────────────────────┘  │
│  Straße und Hausnummer                           │
│  ┌──────────────────────────────────────────┐  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────┐  ┌─────────────────────┐    │
│  │ PLZ          │  │ Ort                 │    │  ← side-by-side
│  └──────────────┘  └─────────────────────┘    │
│                                                  │
│    ← Zurück          [ weiter → ]               │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/PersonalDataPage.tsx`

```tsx
"use client";
import { useState } from "react";
import { useTariff } from "@/lib/wizard/TariffContext";
import { Select } from "@/components/ui/Select/Select";
import { TextInput } from "@/components/ui/TextInput/TextInput";
import { Button } from "@/components/ui/Button/Button";

export function PersonalDataPage() {
  const { data, update, goNext, goPrev } = useTariff();
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const e: Record<string, string> = {};
    if (!data.salutation) e.salutation = "Bitte wählen Sie eine Anrede.";
    if (data.firstName.trim().length < 2) e.firstName = "Bitte geben Sie Ihren Vornamen ein.";
    if (data.lastName.trim().length < 2) e.lastName = "Bitte geben Sie Ihren Nachnamen ein.";
    if (!data.street.trim()) e.street = "Bitte geben Sie Ihre Straße und Hausnummer ein.";
    if (!/^\d{5}$/.test(data.zip)) e.zip = "Bitte geben Sie eine gültige Postleitzahl ein.";
    if (!data.city.trim()) e.city = "Bitte geben Sie Ihren Ort ein.";
    return e;
  };

  const handleNext = () => {
    const e = validate();
    if (Object.keys(e).length > 0) { setErrors(e); return; }
    setErrors({});
    goNext();
  };

  const field = (id: keyof typeof data) => ({
    error: errors[id],
    onChange: (val: string) => { update({ [id]: val } as any); setErrors((e) => ({ ...e, [id]: "" })); },
  });

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
      <h1 style={{
        fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
        fontSize: 28, fontWeight: 700, color: "#333", textAlign: "center", margin: 0,
      }}>
        Ihre persönlichen Daten
      </h1>

      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <Select
          label="Anrede"
          value={data.salutation}
          options={[
            { value: "herr", label: "Herr" },
            { value: "frau", label: "Frau" },
          ]}
          placeholder="Bitte wählen"
          {...field("salutation")}
        />
        <TextInput label="Vorname" value={data.firstName} {...field("firstName")} />
        <TextInput label="Nachname" value={data.lastName} {...field("lastName")} />
        <TextInput label="Straße und Hausnummer" value={data.street} {...field("street")} />

        <div style={{ display: "flex", gap: 12 }}>
          <div style={{ width: 140, flexShrink: 0 }}>
            <TextInput
              label="Postleitzahl"
              value={data.zip}
              maxLength={5}
              {...field("zip")}
            />
          </div>
          <div style={{ flex: 1 }}>
            <TextInput label="Ort" value={data.city} {...field("city")} />
          </div>
        </div>
      </div>

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
Add: `export { PersonalDataPage } from "./PersonalDataPage";`

## Component Usage
```tsx
import { Select } from "@/components/ui/Select/Select";
import { TextInput } from "@/components/ui/TextInput/TextInput";
import { Button } from "@/components/ui/Button/Button";
```
Read all source files before implementing. Check exact prop signatures.

## Interaction Logic
- Validation fires on "weiter" click, not on blur
- Errors shown per-field below each input
- PLZ max 5 digits, pattern /^\d{5}$/
- All fields required

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/Select/` source
2. Read `src/components/ui/TextInput/` source
3. Read `src/components/ui/Button/` source
4. Create `src/app/wizard/pages/PersonalDataPage.tsx`
5. Update `src/app/wizard/pages/index.ts`
6. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard --headed
# Navigate through steps 1-5 to reach step 6
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Ihre persönlichen Daten" visible
[CHECK] Select for Anrede with Herr/Frau options
[CHECK] 5 text inputs: Vorname, Nachname, Straße, PLZ, Ort
[CHECK] PLZ and Ort side-by-side
[CHECK] Clicking "weiter" with empty fields shows per-field errors
[CHECK] PLZ "1234" (4 digits) shows validation error
[CHECK] Valid data → proceeds to step 7 (Zusammenfassung)
[CHECK] "← Zurück" returns to step 5
[CHECK] Demo mode: all fields pre-filled with Markus Weber data
```
