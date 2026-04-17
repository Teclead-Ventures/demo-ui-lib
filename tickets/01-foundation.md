# Ticket 01: Foundation — Wizard Shell, State & Navigation

## Priority: BLOCKING — Must complete before all other tickets

## Objective

Create the complete wizard infrastructure for Berufsunfähigkeitsversicherung (BU): TariffContext, pricing engine, plan data, API routes, and page routing.

---

## Files to Create

### `src/lib/wizard/TariffContext.tsx`

```typescript
"use client";
import React, { createContext, useContext, useState, useCallback } from "react";
import { useSearchParams } from "next/navigation";

export interface DateValue {
  day: string;
  month: string;
  year: string;
}

export type OccupationType = "buero" | "handwerk" | "koerperlich" | "gefahren";
export type PlanId = "grundschutz" | "komfort" | "premium";

export interface TariffFormData {
  occupation: OccupationType;
  birthDate: DateValue;
  monthlyIncome: number;
  coverageAmount: number;
  plan: PlanId;
  smoker: "nein" | "ja";
  preExistingConditions: "nein" | "ja";
  salutation: string;
  firstName: string;
  lastName: string;
  street: string;
  zip: string;
  city: string;
}

const INITIAL_DATA: TariffFormData = {
  occupation: "buero",
  birthDate: { day: "", month: "", year: "" },
  monthlyIncome: 3000,
  coverageAmount: 2000,
  plan: "komfort",
  smoker: "nein",
  preExistingConditions: "nein",
  salutation: "",
  firstName: "",
  lastName: "",
  street: "",
  zip: "",
  city: "",
};

const DEMO_DEFAULTS: TariffFormData = {
  occupation: "buero",
  birthDate: { day: "15", month: "03", year: "1990" },
  monthlyIncome: 3500,
  coverageAmount: 2000,
  plan: "komfort",
  smoker: "nein",
  preExistingConditions: "nein",
  salutation: "herr",
  firstName: "Markus",
  lastName: "Weber",
  street: "Friedrichstraße 22",
  zip: "10117",
  city: "Berlin",
};

// 7 internal wizard steps
export const TOTAL_STEPS = 7;

// Stepper label mapping (which internal step belongs to which stepper label)
// Stepper: 1=Risikoprofil (steps 1-3), 2=Tarifauswahl (4), 3=Gesundheit (5),
//          4=Persönliches (6), 5=Zusammenfassung (7)
export const TARIFF_STEPS = [
  { label: "Risikoprofil" },
  { label: "Tarifauswahl" },
  { label: "Gesundheit" },
  { label: "Persönliches" },
  { label: "Zusammenfassung" },
];

export function getStepperIndex(internalStep: number): number {
  if (internalStep <= 3) return 0;
  if (internalStep === 4) return 1;
  if (internalStep === 5) return 2;
  if (internalStep === 6) return 3;
  return 4;
}

interface TariffContextValue {
  data: TariffFormData;
  update: (patch: Partial<TariffFormData>) => void;
  currentStep: number;
  goTo: (step: number) => void;
  goNext: () => void;
  goPrev: () => void;
  isDemo: boolean;
}

const TariffContext = createContext<TariffContextValue | null>(null);

export function TariffProvider({ children }: { children: React.ReactNode }) {
  const searchParams = useSearchParams();
  const isDemo = searchParams?.get("demo") === "true";

  const [data, setData] = useState<TariffFormData>(isDemo ? DEMO_DEFAULTS : INITIAL_DATA);
  const [currentStep, setCurrentStep] = useState(1);

  const update = useCallback((patch: Partial<TariffFormData>) => {
    setData((prev) => ({ ...prev, ...patch }));
  }, []);

  const goTo = useCallback((step: number) => {
    setCurrentStep(Math.max(1, Math.min(TOTAL_STEPS, step)));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  const goNext = useCallback(() => {
    setCurrentStep((s) => Math.min(TOTAL_STEPS, s + 1));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  const goPrev = useCallback(() => {
    setCurrentStep((s) => Math.max(1, s - 1));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  return (
    <TariffContext.Provider value={{ data, update, currentStep, goTo, goNext, goPrev, isDemo }}>
      {children}
    </TariffContext.Provider>
  );
}

export function useTariff(): TariffContextValue {
  const ctx = useContext(TariffContext);
  if (!ctx) throw new Error("useTariff must be used within TariffProvider");
  return ctx;
}
```

---

### `src/lib/data/pricing.ts`

```typescript
// Berufsunfähigkeitsversicherung — Template A (polynomial age curve)
// Calibration: 30yo Bürotätigkeit, €2k/Monat, Komfort → ~€55/Monat ✓

const BASE_RATES: Record<"grundschutz" | "komfort" | "premium", number> = {
  grundschutz: 2.08,
  komfort: 2.54,
  premium: 3.12,
};

const AGE_CURVE = { base: 0.70, linear: 0.50, quadratic: -0.15 };
const MIN_AGE = 18;
const MAX_AGE = 55;
const COVERAGE_UNIT = 100; // per €100/month
const LOADING = 0.28;

export const RISK_MULTIPLIERS: Record<string, number> = {
  buero: 1.0,
  handwerk: 1.4,
  koerperlich: 1.8,
  gefahren: 2.2,
};

function calculateAgeFactor(age: number): number {
  const t = Math.max(0, Math.min(1, (age - MIN_AGE) / (MAX_AGE - MIN_AGE)));
  return AGE_CURVE.base + AGE_CURVE.linear * t + AGE_CURVE.quadratic * t * t;
}

export function calculateAge(birthDate: { day: string; month: string; year: string }): number {
  const today = new Date();
  const birth = new Date(parseInt(birthDate.year), parseInt(birthDate.month) - 1, parseInt(birthDate.day));
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  return age;
}

export function calculatePaymentDuration(age: number): number {
  return Math.max(1, 67 - age);
}

export function calculateMonthlyPrice(
  age: number,
  coverageAmount: number,
  plan: "grundschutz" | "komfort" | "premium",
  occupation: string = "buero"
): number {
  const clampedAge = Math.max(MIN_AGE, Math.min(MAX_AGE, age));
  const units = coverageAmount / COVERAGE_UNIT;
  const ageFactor = calculateAgeFactor(clampedAge);
  const riskMult = RISK_MULTIPLIERS[occupation] ?? 1.0;
  const netPremium = BASE_RATES[plan] * units * ageFactor * riskMult;
  return Math.round(netPremium * (1 + LOADING) * 100) / 100;
}

export function formatPrice(price: number): string {
  return price.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function formatCoverage(amount: number): string {
  return amount.toLocaleString("de-DE") + " €/Monat";
}
```

---

### `src/lib/data/planData.ts`

```typescript
export type PlanId = "grundschutz" | "komfort" | "premium";

export interface Benefit { label: string; value: string; }

export interface PlanInfo {
  id: PlanId;
  name: string;
  highlight?: string;
  benefits: Benefit[];
  extendedBenefits: Benefit[];
}

export const PLANS: PlanInfo[] = [
  {
    id: "grundschutz",
    name: "Grundschutz",
    benefits: [
      { label: "BU-Definition",            value: "≥ 50 % arbeitsunfähig" },
      { label: "Leistungsdauer",            value: "bis Endalter 67" },
      { label: "Karenzzeit",                value: "6 Monate" },
      { label: "Nachversicherungsgarantie", value: "–" },
    ],
    extendedBenefits: [
      { label: "Infektionsklausel",          value: "–" },
      { label: "Dienstunfähigkeitsklausel",  value: "–" },
      { label: "Weltweiter Schutz",          value: "–" },
    ],
  },
  {
    id: "komfort",
    name: "Komfort",
    highlight: "Beliebtester Tarif",
    benefits: [
      { label: "BU-Definition",            value: "≥ 50 % arbeitsunfähig" },
      { label: "Leistungsdauer",            value: "bis Endalter 67" },
      { label: "Karenzzeit",                value: "3 Monate" },
      { label: "Nachversicherungsgarantie", value: "✓" },
    ],
    extendedBenefits: [
      { label: "Infektionsklausel",          value: "✓" },
      { label: "Dienstunfähigkeitsklausel",  value: "–" },
      { label: "Weltweiter Schutz",          value: "–" },
    ],
  },
  {
    id: "premium",
    name: "Premium",
    benefits: [
      { label: "BU-Definition",            value: "≥ 50 % arbeitsunfähig" },
      { label: "Leistungsdauer",            value: "bis Endalter 67" },
      { label: "Karenzzeit",                value: "keine" },
      { label: "Nachversicherungsgarantie", value: "✓" },
    ],
    extendedBenefits: [
      { label: "Infektionsklausel",          value: "✓" },
      { label: "Dienstunfähigkeitsklausel",  value: "✓" },
      { label: "Umorganisationsverzicht",    value: "✓" },
      { label: "Weltweiter Schutz",          value: "✓" },
    ],
  },
];

export const OCCUPATION_LABELS: Record<string, string> = {
  buero: "Bürotätigkeit / kaufmännisch",
  handwerk: "Handwerk / Techniker",
  koerperlich: "Schwere körperliche Arbeit",
  gefahren: "Gefahrenberufe",
};

export function getPlan(id: PlanId): PlanInfo {
  return PLANS.find((p) => p.id === id)!;
}
```

---

### `src/app/wizard/page.tsx`

Wraps `TariffProvider` (with Suspense for useSearchParams), renders stepper + routes to the correct page component based on `currentStep`.

- Steps 1 → OccupationPage
- Step 2 → BirthDatePage
- Step 3 → CoveragePage
- Step 4 → PlanSelectionPage
- Step 5 → HealthQuestionsPage
- Step 6 → PersonalDataPage
- Step 7 → SummaryPage
- Stepper: 5 circles (Risikoprofil/Tarifauswahl/Gesundheit/Persönliches/Zusammenfassung)
- Active stepper index: `getStepperIndex(currentStep)`
- Full page background: #f8f8f8
- Content centered, maxWidth 640px, padding 48px 24px

---

### `src/app/api/submit/route.ts`

POST → inserts body into `${PREFIX}_bu_applications`.
Use `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_TABLE_PREFIX` from env.

Fields to insert (snake_case):
occupation, birth_date, monthly_income, coverage_amount, plan, monthly_price,
payment_duration_years, smoker, pre_existing_conditions, salutation,
first_name, last_name, street, zip, city

---

## Gate

```bash
npx tsc --noEmit   # 0 errors
npm run dev        # starts without crash
# http://localhost:3000/wizard → stepper visible, OccupationPage renders (step 1)
```
