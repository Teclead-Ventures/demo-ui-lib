# Ticket 08: Page 4 — Zusammenfassung (Summary)

## Step: 7 (Zusammenfassung) | Sub-step: 1 | Agent: G

## Reference Screenshot
None available.

## Objective

Review all entered data grouped by wizard section. Two consent checkboxes (AVB + Datenschutz). Submit button posts to /api/submit. Success toast after submission.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│                                                  │
│     Zusammenfassung Ihres Antrags               │  ← H1
│     Bitte überprüfen Sie Ihre Angaben           │  ← subtitle
│                                                  │
│  ┌─────────────────────────────────────────┐   │
│  │  Risikoprofil                       ✎  │   │  ← section card
│  │  Beruf:      Bürotätigkeit               │   │
│  │  Alter:      35 Jahre                    │   │
│  │  BU-Rente:   2.000 €/Monat              │   │
│  │  Laufzeit:   32 Jahre (bis 67)          │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │  Tarifauswahl                       ✎  │   │
│  │  Tarif:      Komfort                    │   │
│  │  Beitrag:    58,37 €/Monat             │   │
│  │  Karenzzeit: 3 Monate                  │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │  Gesundheit                         ✎  │   │
│  │  Raucher:         Nein                  │   │
│  │  Vorerkrankungen: Nein                  │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │  Persönliche Daten                  ✎  │   │
│  │  Name:    Herr Markus Weber             │   │
│  │  Adresse: Friedrichstraße 22, 10117 Berlin│ │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  ☐ Ich stimme den AVB zu.                       │
│  ☐ Ich habe die Datenschutzerklärung gelesen.   │
│                                                  │
│        [ Jetzt verbindlich abschließen ]        │  ← disabled until both checked
│                                                  │
│    ← Zurück                                     │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Files to Create/Modify

### `src/app/wizard/pages/SummaryPage.tsx`

```tsx
"use client";
import { useState } from "react";
import { useTariff } from "@/lib/wizard/TariffContext";
import { Checkbox } from "@/components/ui/Checkbox/Checkbox";
import { Button } from "@/components/ui/Button/Button";
import { useToast } from "@/components/ui/Toast/Toast";
import {
  calculateAge, calculateMonthlyPrice, calculatePaymentDuration,
  formatPrice, formatCoverage
} from "@/lib/data/pricing";
import { OCCUPATION_LABELS } from "@/lib/data/planData";

export function SummaryPage() {
  const { data, goTo, goPrev } = useTariff();
  const { showToast } = useToast();
  const [avb, setAvb] = useState(false);
  const [datenschutz, setDatenschutz] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const age = calculateAge(data.birthDate);
  const paymentDuration = calculatePaymentDuration(age);
  const price = calculateMonthlyPrice(age, data.coverageAmount, data.plan, data.occupation);

  const PLAN_LABELS: Record<string, string> = {
    grundschutz: "Grundschutz", komfort: "Komfort", premium: "Premium"
  };
  const KARENZ: Record<string, string> = {
    grundschutz: "6 Monate", komfort: "3 Monate", premium: "keine"
  };
  const SAL_LABELS: Record<string, string> = { herr: "Herr", frau: "Frau" };

  const handleSubmit = async () => {
    if (!avb || !datenschutz || submitting) return;
    setSubmitting(true);
    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          occupation: data.occupation,
          birth_date: `${data.birthDate.day}.${data.birthDate.month}.${data.birthDate.year}`,
          monthly_income: String(data.monthlyIncome),
          coverage_amount: String(data.coverageAmount),
          plan: data.plan,
          monthly_price: formatPrice(price),
          payment_duration_years: paymentDuration,
          smoker: data.smoker,
          pre_existing_conditions: data.preExistingConditions,
          salutation: data.salutation,
          first_name: data.firstName,
          last_name: data.lastName,
          street: data.street,
          zip: data.zip,
          city: data.city,
        }),
      });
      if (!res.ok) throw new Error("Submit failed");
      showToast("Ihr Antrag wurde erfolgreich eingereicht!");
    } catch {
      showToast("Fehler beim Einreichen. Bitte versuchen Sie es erneut.");
    } finally {
      setSubmitting(false);
    }
  };

  const SectionCard = ({ title, step, rows }: { title: string; step: number; rows: [string, string][] }) => (
    <div style={{ backgroundColor: "#fff", border: "1px solid #e5e5e5", borderRadius: 8, padding: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <span style={{ fontWeight: 700, color: "#333", fontSize: 16 }}>{title}</span>
        <button onClick={() => goTo(step)} style={{ background: "none", border: "none", cursor: "pointer", color: "#8e0038", fontSize: 18 }}>✎</button>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {rows.map(([label, value], i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
            <span style={{ color: "#737373" }}>{label}</span>
            <span style={{ color: "#333", fontWeight: 500 }}>{value}</span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      <div style={{ textAlign: "center" }}>
        <h1 style={{
          fontFamily: "var(--font-family-heading, 'Source Serif 4', Georgia, serif)",
          fontSize: 28, fontWeight: 700, color: "#333", margin: "0 0 8px",
        }}>
          Zusammenfassung Ihres Antrags
        </h1>
        <p style={{ color: "#737373", fontSize: 14, margin: 0 }}>Bitte überprüfen Sie Ihre Angaben</p>
      </div>

      <SectionCard title="Risikoprofil" step={1} rows={[
        ["Beruf", OCCUPATION_LABELS[data.occupation] ?? data.occupation],
        ["Alter", `${age} Jahre`],
        ["BU-Rente", formatCoverage(data.coverageAmount)],
        ["Laufzeit", `${paymentDuration} Jahre (bis 67)`],
      ]} />

      <SectionCard title="Tarifauswahl" step={4} rows={[
        ["Tarif", PLAN_LABELS[data.plan] ?? data.plan],
        ["Monatlicher Beitrag", `${formatPrice(price)} €`],
        ["Karenzzeit", KARENZ[data.plan] ?? "–"],
      ]} />

      <SectionCard title="Gesundheit" step={5} rows={[
        ["Raucher", data.smoker === "ja" ? "Ja" : "Nein"],
        ["Vorerkrankungen", data.preExistingConditions === "ja" ? "Ja" : "Nein"],
      ]} />

      <SectionCard title="Persönliche Daten" step={6} rows={[
        ["Name", `${SAL_LABELS[data.salutation] ?? ""} ${data.firstName} ${data.lastName}`.trim()],
        ["Adresse", `${data.street}, ${data.zip} ${data.city}`],
      ]} />

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <Checkbox
          label="Ich stimme den Allgemeinen Versicherungsbedingungen (AVB) zu."
          checked={avb}
          onChange={setAvb}
        />
        <Checkbox
          label="Ich habe die Datenschutzerklärung gelesen und stimme der Verarbeitung meiner Daten zu."
          checked={datenschutz}
          onChange={setDatenschutz}
        />
      </div>

      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
        <Button
          label={submitting ? "Wird eingereicht..." : "Jetzt verbindlich abschließen"}
          onClick={handleSubmit}
          variant="primary"
          disabled={!avb || !datenschutz || submitting}
          style={{ minWidth: 300 }}
        />
        <button onClick={goPrev} style={{ background: "none", border: "none", color: "#8e0038", fontWeight: 700, cursor: "pointer", fontSize: 16 }}>
          ← Zurück
        </button>
      </div>
    </div>
  );
}
```

### `src/app/wizard/pages/index.ts` (MODIFY)
Add: `export { SummaryPage } from "./SummaryPage";`

## Component Usage
```tsx
import { Checkbox } from "@/components/ui/Checkbox/Checkbox";
import { Button } from "@/components/ui/Button/Button";
import { useToast } from "@/components/ui/Toast/Toast";
```
Read all source files before implementing.

## Interaction Logic
- Submit button disabled until both checkboxes checked
- POST to /api/submit with all snake_case fields
- Success: show toast "Ihr Antrag wurde erfolgreich eingereicht!"
- Edit pencil (✎) → goTo(step) to go back to that section
- goTo(1) for Risikoprofil, goTo(4) for Tarifauswahl, goTo(5) for Gesundheit, goTo(6) for Persönliches

---

## Agent Execution

### Page Agent Actions
1. Read `src/components/ui/Checkbox/` source
2. Read `src/components/ui/Button/` source
3. Read `src/components/ui/Toast/` source
4. Read `src/lib/data/pricing.ts` and `src/lib/data/planData.ts`
5. Create `src/app/wizard/pages/SummaryPage.tsx`
6. Update `src/app/wizard/pages/index.ts`
7. Run quality gate loop

### Tester: Navigation Sequence
```bash
playwright-cli open http://localhost:3000/wizard?demo=true --headed
# Click weiter through all 6 steps to reach step 7
playwright-cli snapshot
```

### Tester: Page-Specific Checks
```
[CHECK] Heading "Zusammenfassung Ihres Antrags" visible
[CHECK] 4 section cards: Risikoprofil / Tarifauswahl / Gesundheit / Persönliche Daten
[CHECK] Risikoprofil shows occupation, age, BU-Rente, Laufzeit
[CHECK] Tarifauswahl shows tarif name, price, karenzzeit
[CHECK] Gesundheit shows Raucher + Vorerkrankungen answers
[CHECK] Persönliche Daten shows name + address
[CHECK] Edit pencil on each card navigates back to that step
[CHECK] Submit button disabled until both checkboxes checked
[CHECK] After checking both boxes, button becomes active
[CHECK] Clicking submit shows success toast
[CHECK] "← Zurück" returns to step 6
```
