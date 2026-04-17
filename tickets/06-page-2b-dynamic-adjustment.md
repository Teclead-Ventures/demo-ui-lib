# Ticket 06: Page 2b — Gesundheitsfragen (Health Questions)

## Step: 5 (Gesundheit) | Sub-step: 1 | Agent: E

## Reference Screenshot
None available.

## Objective

Simplified health questionnaire: two inline radio questions (Raucher? / Vorerkrankungen?). If user answers "Ja" to either, show an informational note — but do NOT block progression (demo flow).

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│     Gesundheitsfragen                           │  ← H1, serif, centered
│                                                  │
│  Für Ihre BU-Versicherung benötigen wir         │
│  einige gesundheitliche Angaben.                │  ← subtitle, gray
│                                                  │
│  Rauchen Sie?                                   │  ← label
│  ┌───────────────────────────────┐              │
│  │  ○ Nein    ○ Ja              │              │  ← InlineRadio
│  └───────────────────────────────┘              │
│                                                  │
│  Bestehen Vorerkrankungen?                      │  ← label
│  ┌───────────────────────────────┐              │
│  │  ○ Nein    ○ Ja              │              │  ← InlineRadio
│  └───────────────────────────────┘              │
│                                                  │
│  [ℹ️  Hinweis] (shown only if any "Ja")         │
│  Bei Risikofaktoren erfolgt im Antrag eine      │
│  individuelle Risikoprüfung durch unsere Berater│
│                                                  │
│    ← Zurück          [ weiter → ]               │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/HealthQuestionsPage.tsx`

```tsx
"use client";
import { useTariff } from "@/lib/wizard/TariffContext";
import { InlineRadio } from "@/components/ui/InlineRadio/InlineRadio";
import { Button } from "@/components/ui/Button/Button";

export function HealthQuestionsPage() {
  const { data, update, goNext, goPrev } = useTariff();

  const hasRisk = data.smoker === "ja" || data.preExistingConditions === "ja";

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
      <h1 style={{
        fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
        fontSize: 28, fontWeight: 700, color: "#333", textAlign: "center", margin: 0,
      }}>
        Gesundheitsfragen
      </h1>

      <p style={{ textAlign: "center", color: "#737373", fontSize: 14, margin: 0 }}>
        Für Ihre BU-Versicherung benötigen wir einige gesundheitliche Angaben.
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <label style={{ fontSize: 16, fontWeight: 600, color: "#333" }}>Rauchen Sie?</label>
          <InlineRadio
            options={[{ value: "nein", label: "Nein" }, { value: "ja", label: "Ja" }]}
            value={data.smoker}
            onChange={(val) => update({ smoker: val as "nein" | "ja" })}
          />
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <label style={{ fontSize: 16, fontWeight: 600, color: "#333" }}>Bestehen Vorerkrankungen?</label>
          <InlineRadio
            options={[{ value: "nein", label: "Nein" }, { value: "ja", label: "Ja" }]}
            value={data.preExistingConditions}
            onChange={(val) => update({ preExistingConditions: val as "nein" | "ja" })}
          />
        </div>
      </div>

      {hasRisk && (
        <div style={{
          backgroundColor: "#fff9e6", border: "1px solid #f0c040",
          borderRadius: 8, padding: 16,
        }}>
          <p style={{ margin: 0, fontSize: 14, color: "#555" }}>
            <strong>Hinweis:</strong> Bei Risikofaktoren erfolgt im Antrag eine individuelle
            Risikoprüfung. Unser Berater-Team meldet sich nach der Antragstellung bei Ihnen.
          </p>
        </div>
      )}

      <div style={{ display: "flex", justifyContent: "center", gap: 16, alignItems: "center" }}>
        <button onClick={goPrev} style={{ background: "none", border: "none", color: "#8e0038", fontWeight: 700, cursor: "pointer", fontSize: 16 }}>
          ← Zurück
        </button>
        <Button label="weiter" onClick={goNext} variant="primary" style={{ minWidth: 240 }} />
      </div>
    </div>
  );
}
```

### `src/app/wizard/pages/index.ts` (MODIFY)
Add: `export { HealthQuestionsPage } from "./HealthQuestionsPage";`

## Component Usage
```tsx
import { InlineRadio } from "@/components/ui/InlineRadio/InlineRadio";
import { Button } from "@/components/ui/Button/Button";
```
Read both source files before implementing.

## Interaction Logic
- Both questions default to "nein"
- If either is "ja" → show yellow info notice (non-blocking)
- "weiter" always enabled — no blocking validation
- Both fields stored in state for summary + DB

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/InlineRadio/` source
2. Read `src/components/ui/Button/` source
3. Create `src/app/wizard/pages/HealthQuestionsPage.tsx`
4. Update `src/app/wizard/pages/index.ts`
5. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard --headed
# Navigate through steps 1-4 to reach step 5
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Gesundheitsfragen" visible
[CHECK] Two InlineRadio groups: "Rauchen Sie?" and "Bestehen Vorerkrankungen?"
[CHECK] Both default to "Nein"
[CHECK] No warning shown when both "Nein"
[CHECK] Selecting "Ja" for smoker shows yellow info notice
[CHECK] Selecting "Ja" for Vorerkrankungen shows yellow info notice
[CHECK] "weiter" always enabled — navigates to step 6 regardless
[CHECK] "← Zurück" returns to step 4
```
