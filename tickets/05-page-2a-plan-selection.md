# Ticket 05: Page 2a — Tarifauswahl (Plan Selection)

## Step: 4 (Tarifauswahl) | Sub-step: 1 | Agent: D

## Reference Screenshot
None available.

## Objective

The most important page. User selects between Grundschutz, Komfort, and Premium. Live price updates as they switch tier or (on re-entry) when risk class / coverage changes. Benefits listed per tier.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│     Wählen Sie Ihren passenden Schutz           │  ← H1, serif, centered
│                                                  │
│  BU-Rente: 2.000 €/Monat · Laufzeit: 32 Jahre  │  ← sub-info, gray, centered
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  [Grundschutz]  [Komfort ★]  [Premium]  │  │  ← SegmentedControl
│  └──────────────────────────────────────────┘  │
│                                                  │
│     Sie zahlen                                   │
│     58,37 € monatlich                           │  ← large, red
│     Komfort · 32 Jahre Laufzeit                 │  ← subtitle, gray
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │ ✓ BU-Definition        ≥ 50 % arbeitsunf│   │
│  │ ✓ Leistungsdauer       bis Endalter 67  │   │
│  │ ✓ Karenzzeit           3 Monate         │   │
│  │ ✓ Nachversicherungsg.  ✓                │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  ▼ Alle Leistungen anzeigen                     │
│                                                  │
│    ← Zurück    [ weiter zum Online-Antrag → ]   │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/PlanSelectionPage.tsx`

```tsx
"use client";
import { useState } from "react";
import { useTariff } from "@/lib/wizard/TariffContext";
import { SegmentedControl } from "@/components/ui/SegmentedControl/SegmentedControl";
import { Button } from "@/components/ui/Button/Button";
import { calculateAge, calculateMonthlyPrice, calculatePaymentDuration, formatPrice } from "@/lib/data/pricing";
import { PLANS, getPlan, type PlanId } from "@/lib/data/planData";

export function PlanSelectionPage() {
  const { data, update, goNext, goPrev } = useTariff();
  const [showAll, setShowAll] = useState(false);

  const age = calculateAge(data.birthDate);
  const paymentDuration = calculatePaymentDuration(age);
  const price = calculateMonthlyPrice(age, data.coverageAmount, data.plan, data.occupation);
  const plan = getPlan(data.plan);

  const segmentOptions = PLANS.map((p) => ({
    value: p.id,
    label: p.highlight ? `${p.name} ★` : p.name,
  }));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
      <h1 style={{
        fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
        fontSize: 28, fontWeight: 700, color: "#333", textAlign: "center", margin: 0,
      }}>
        Wählen Sie Ihren passenden Schutz
      </h1>

      <p style={{ textAlign: "center", color: "#737373", fontSize: 14, margin: 0 }}>
        BU-Rente: {data.coverageAmount.toLocaleString("de-DE")} €/Monat · Laufzeit: {paymentDuration} Jahre
      </p>

      <SegmentedControl
        options={segmentOptions}
        value={data.plan}
        onChange={(val) => update({ plan: val as PlanId })}
      />

      {/* Price display */}
      <div style={{ textAlign: "center" }}>
        <p style={{ fontSize: 14, color: "#737373", margin: "0 0 4px" }}>Sie zahlen</p>
        <p style={{ fontSize: 36, fontWeight: 700, color: "#8e0038", margin: "0 0 4px" }}>
          {formatPrice(price)} € monatlich
        </p>
        <p style={{ fontSize: 14, color: "#737373", margin: 0 }}>
          {plan.name} · {paymentDuration} Jahre Laufzeit
        </p>
      </div>

      {/* Benefits */}
      <div style={{ backgroundColor: "#fff", border: "1px solid #e5e5e5", borderRadius: 8, padding: 24 }}>
        <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 12 }}>
          {plan.benefits.map((b, i) => (
            <li key={i} style={{ display: "flex", justifyContent: "space-between", gap: 16 }}>
              <span style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <span style={{ color: "#5de38e", fontWeight: 700, flexShrink: 0 }}>✓</span>
                <span style={{ color: "#333", fontSize: 16 }}>{b.label}</span>
              </span>
              <span style={{ color: "#333", fontSize: 16, fontWeight: 600, flexShrink: 0 }}>{b.value}</span>
            </li>
          ))}
        </ul>

        {showAll && (
          <ul style={{ listStyle: "none", padding: "16px 0 0", margin: 0, borderTop: "1px solid #e5e5e5", marginTop: 16, display: "flex", flexDirection: "column", gap: 12 }}>
            {plan.extendedBenefits.map((b, i) => (
              <li key={i} style={{ display: "flex", justifyContent: "space-between", gap: 16 }}>
                <span style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                  <span style={{ color: "#5de38e", fontWeight: 700, flexShrink: 0 }}>✓</span>
                  <span style={{ color: "#333", fontSize: 16 }}>{b.label}</span>
                </span>
                <span style={{ color: "#333", fontSize: 16, fontWeight: 600, flexShrink: 0 }}>{b.value}</span>
              </li>
            ))}
          </ul>
        )}

        <button
          onClick={() => setShowAll((v) => !v)}
          style={{ background: "none", border: "none", color: "#8e0038", fontWeight: 700, cursor: "pointer", fontSize: 14, marginTop: 16, padding: 0 }}
        >
          {showAll ? "▲ Weniger anzeigen" : "▼ Alle Leistungen anzeigen"}
        </button>
      </div>

      <div style={{ display: "flex", justifyContent: "center", gap: 16, alignItems: "center" }}>
        <button onClick={goPrev} style={{ background: "none", border: "none", color: "#8e0038", fontWeight: 700, cursor: "pointer", fontSize: 16 }}>
          ← Zurück
        </button>
        <Button label="weiter zum Online-Antrag" onClick={goNext} variant="primary" style={{ minWidth: 240 }} />
      </div>
    </div>
  );
}
```

### `src/app/wizard/pages/index.ts` (MODIFY)
Add: `export { PlanSelectionPage } from "./PlanSelectionPage";`

## Component Usage
```tsx
import { SegmentedControl } from "@/components/ui/SegmentedControl/SegmentedControl";
import { Button } from "@/components/ui/Button/Button";
```
Read both source files before implementing.

## Interaction Logic
- Switching plans: updates `data.plan`, price recalculates instantly
- Price depends on: age (from birthDate), coverageAmount, plan, occupation (risk class)
- "Alle Leistungen anzeigen" toggles extended benefits
- No validation needed — always valid

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/SegmentedControl/` source
2. Read `src/components/ui/Button/` source
3. Read `src/lib/data/pricing.ts` and `src/lib/data/planData.ts`
4. Create `src/app/wizard/pages/PlanSelectionPage.tsx`
5. Update `src/app/wizard/pages/index.ts`
6. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard --headed
# Navigate through steps 1-3 to reach step 4
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Wählen Sie Ihren passenden Schutz" visible
[CHECK] Sub-info shows BU-Rente and Laufzeit
[CHECK] SegmentedControl shows 3 tabs: Grundschutz / Komfort ★ / Premium
[CHECK] "Komfort" pre-selected
[CHECK] Price displayed in red (e.g. "58,37 € monatlich" for 35yo Büro €2k Komfort)
[CHECK] 4 benefit rows visible with green checkmarks
[CHECK] "Alle Leistungen anzeigen" toggles extended benefits
[CHECK] Switching to Grundschutz changes price and karenzzeit to "6 Monate"
[CHECK] Switching to Premium changes price and karenzzeit to "keine"
[CHECK] "weiter zum Online-Antrag" advances to step 5
[CHECK] "← Zurück" returns to step 3
```
