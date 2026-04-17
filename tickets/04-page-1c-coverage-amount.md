# Ticket 04: Page 1c — Einkommen & BU-Rente (Coverage Configuration)

## Step: 3 (Risikoprofil) | Sub-step: 3 | Agent: C

## Reference Screenshot
None available.

## Objective

User enters their monthly gross income and configures their desired BU monthly pension via a slider. The coverage amount is capped at 75% of monthly income. Shows live pricing preview.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│   Wie hoch soll Ihre BU-Rente sein?      [?]   │  ← H1 serif + Tooltip
│                                                  │
│   Monatliches Bruttoeinkommen                   │
│  ┌─────────────────────────────────────────┐   │
│  │  3.500 €                                │   │  ← number input
│  └─────────────────────────────────────────┘   │
│                                                  │
│   Gewünschte BU-Rente (max. 75 % des Einkommens)│
│  ────────────────●───────────────────────────   │  ← Slider
│       500 €/Monat      2.000 €/Monat            │
│                                                  │
│   ✓ Karenzzeit: 3 Monate                        │  ← preview bullets
│   ✓ Laufzeit: bis Endalter 67 (32 Jahre)        │
│                                                  │
│    ← Zurück          [ weiter → ]               │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/CoveragePage.tsx`

```tsx
"use client";
import { useTariff } from "@/lib/wizard/TariffContext";
import { Slider } from "@/components/ui/Slider/Slider";
import { Button } from "@/components/ui/Button/Button";
import { Tooltip } from "@/components/ui/Tooltip/Tooltip";
import { calculateAge, calculatePaymentDuration } from "@/lib/data/pricing";

export function CoveragePage() {
  const { data, update, goNext, goPrev } = useTariff();

  const age = calculateAge(data.birthDate);
  const paymentDuration = calculatePaymentDuration(age);
  const maxCoverage = Math.floor((data.monthlyIncome * 0.75) / 100) * 100;

  const handleIncomeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const income = Math.max(500, parseInt(e.target.value) || 0);
    const newMax = Math.floor((income * 0.75) / 100) * 100;
    update({
      monthlyIncome: income,
      coverageAmount: Math.min(data.coverageAmount, newMax),
    });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
        <h1 style={{
          fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
          fontSize: 28, fontWeight: 700, color: "#333", margin: 0,
        }}>
          Wie hoch soll Ihre BU-Rente sein?
        </h1>
        <Tooltip content="Die BU-Rente ersetzt Ihr Einkommen im Leistungsfall. Empfohlen: 70–80 % Ihres Nettoeinkommens." />
      </div>

      {/* Income input */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <label style={{ fontSize: 14, fontWeight: 600, color: "#333" }}>
          Monatliches Bruttoeinkommen
        </label>
        <div style={{ position: "relative", maxWidth: 360, margin: "0 auto" }}>
          <input
            type="number"
            value={data.monthlyIncome}
            onChange={handleIncomeChange}
            min={500}
            max={20000}
            step={100}
            style={{
              width: "100%", padding: "12px 40px 12px 16px",
              border: "1px solid #e5e5e5", borderRadius: 8, fontSize: 16,
              boxSizing: "border-box",
            }}
          />
          <span style={{ position: "absolute", right: 16, top: "50%", transform: "translateY(-50%)", color: "#737373", fontSize: 16 }}>€</span>
        </div>
      </div>

      {/* Coverage slider */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <label style={{ fontSize: 14, fontWeight: 600, color: "#333" }}>
          Gewünschte BU-Rente{" "}
          <span style={{ color: "#737373", fontWeight: 400 }}>(max. 75 % des Einkommens)</span>
        </label>
        <Slider
          min={500}
          max={maxCoverage || 5000}
          step={100}
          value={data.coverageAmount}
          onChange={(val) => update({ coverageAmount: val })}
          label={`${data.coverageAmount.toLocaleString("de-DE")} €/Monat`}
        />
      </div>

      {/* Preview bullets */}
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <p style={{ color: "#5de38e", fontWeight: 700, margin: 0, fontSize: 14 }}>
          ✓ Laufzeit: bis Endalter 67 ({paymentDuration} Jahre)
        </p>
        <p style={{ color: "#737373", fontSize: 14, margin: 0 }}>
          Rente bei BU: {data.coverageAmount.toLocaleString("de-DE")} €/Monat
        </p>
      </div>

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
Add: `export { CoveragePage } from "./CoveragePage";`

## Component Usage
```tsx
import { Slider } from "@/components/ui/Slider/Slider";
import { Button } from "@/components/ui/Button/Button";
import { Tooltip } from "@/components/ui/Tooltip/Tooltip";
```
Read all source files before implementing.

## Interaction Logic
- Income input: number field, min 500, max 20000, step 100
- Coverage slider: max = floor(income × 0.75 / 100) × 100
- When income changes, coverageAmount is capped to new max
- paymentDuration = 67 − age (from birthDate state)
- No further validation needed — slider enforces bounds

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/Slider/` source
2. Read `src/components/ui/Button/` source
3. Read `src/components/ui/Tooltip/` source
4. Read `src/lib/data/pricing.ts` for `calculatePaymentDuration`
5. Create `src/app/wizard/pages/CoveragePage.tsx`
6. Update `src/app/wizard/pages/index.ts`
7. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard --headed
# Navigate through steps 1-2 to reach step 3
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Wie hoch soll Ihre BU-Rente sein?" visible
[CHECK] Income input shows default 3.000 (or 3.500 in demo mode)
[CHECK] Slider renders with value 2.000 €/Monat
[CHECK] Slider max = income × 0.75 (for 3.500 € income → max 2.625)
[CHECK] Changing income adjusts slider max and caps coverage if needed
[CHECK] Payment duration preview shows correct years (e.g. "32 Jahre" for 35yo)
[CHECK] "weiter" navigates to step 4 (PlanSelection)
[CHECK] "← Zurück" returns to step 2
```
