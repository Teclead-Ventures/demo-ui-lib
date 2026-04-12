# Pricing Engine Model

This document defines the universal pricing formula used across all insurance products. Every tariff uses the same structure — only the parameters change.

## The Formula

```
monthlyPremium = netPremium × (1 + loading)

netPremium = baseRate × coverageUnits × ageFactor × riskClassMultiplier × paymentModeDiscount
```

Where:
- **baseRate**: Cost per coverage unit per month, varies by plan tier. Defined per product in `products.md`.
- **coverageUnits**: `coverageAmount / coverageUnit` (e.g., €8.000 coverage / €1.000 unit = 8 units)
- **ageFactor**: Risk multiplier based on insured person's age. See age curve below.
- **riskClassMultiplier**: Risk multiplier based on the product's primary risk differentiator (occupation, smoker status, region, etc.). 1.0 if product has no risk classes.
- **paymentModeDiscount**: Monthly=1.0, Quarterly=0.98, Semi-annual=0.96, Annual=0.95
- **loading**: Insurer's margin covering acquisition costs, admin, safety, profit. Typically 0.20–0.30.

## Age Factor Calculation

The age factor uses a quadratic polynomial that can model different risk shapes:

```typescript
function calculateAgeFactor(
  age: number,
  minAge: number,
  maxAge: number,
  curve: { base: number; linear: number; quadratic: number }
): number {
  const t = (age - minAge) / (maxAge - minAge); // Normalize to 0-1
  return curve.base + curve.linear * t + curve.quadratic * t * t;
}
```

### Curve shapes by product type

| Product | base | linear | quadratic | Shape | Why |
|---------|------|--------|-----------|-------|-----|
| Sterbegeld | 0.65 | 0.15 | 0.55 | Exponential after 60 | Mortality rises steeply with age |
| BU | 0.70 | 0.50 | −0.15 | Bell curve ~45-50 | Disability risk peaks mid-career, drops near retirement |
| Zahnzusatz | 0.80 | 0.35 | 0.10 | Gentle linear | Dental issues increase gradually |
| Risikoleben | 0.40 | 0.20 | 0.80 | Steep exponential | Mortality doubles every ~8 years |
| Pflege | 0.50 | 0.25 | 0.65 | Steep growth | Care need rises sharply after 70 |
| Tierkranken | 0.60 | 0.10 | 0.90 | Very steep after 7-8 | Pets age fast, vet costs spike |
| Unfall | 0.85 | 0.10 | 0.15 | Moderate increase | Accident risk fairly constant, slight age effect |
| Krankentagegeld | 0.70 | 0.35 | 0.20 | Steady increase | Illness duration increases with age |
| Hausrat/Haftpflicht/Cyber | 1.00 | 0.00 | 0.00 | Flat | Not age-dependent |
| Kfz | 1.80 | −1.20 | 0.50 | U-curve | Young drivers high risk, drops, slight rise for elderly |
| Reise | 0.75 | 0.10 | 0.30 | Gentle U | Young adventurers + elderly travelers |

## Flat-Rate Products

Some products (Haftpflicht, Rechtsschutz, Kfz, Cyber) have flat-rate pricing where the coverage amount affects the payout cap but not the premium significantly. For these products, set `coverageUnit = defaultCoverage` so that `coverageUnits = 1`. The base rate then IS the monthly net premium for the reference customer.

| Product | coverageUnit | Why |
|---------|-------------|-----|
| Haftpflicht | = defaultCoverage (€10M) | Premium is flat, coverage just sets the liability cap |
| Rechtsschutz | = defaultCoverage (€300k) | Premium depends on legal areas covered, not the cap |
| Kfz | = 1 | Premium is per vehicle, not per coverage euro |
| Cyber | = defaultCoverage (€25k) | Premium is flat, coverage sets the max payout |

The formula still works: `baseRate × 1 × ageFactor × riskClass × paymentMode × (1 + loading)`.

## TypeScript Implementation Template

This is the template the demo pipeline uses. The tariff-designer fills in the constants.

```typescript
// src/lib/data/pricing.ts

// These values come from tariff-spec.json — filled in by tariff-designer
const BASE_RATES: Record<"grundschutz" | "komfort" | "premium", number> = {
  grundschutz: __BASE_RATE_GRUND__,
  komfort: __BASE_RATE_KOMFORT__,
  premium: __BASE_RATE_PREMIUM__,
};

const AGE_CURVE = {
  base: __AGE_CURVE_BASE__,
  linear: __AGE_CURVE_LINEAR__,
  quadratic: __AGE_CURVE_QUADRATIC__,
};

const MIN_AGE = __MIN_AGE__;
const MAX_AGE = __MAX_AGE__;
const COVERAGE_UNIT = __COVERAGE_UNIT__;
const LOADING = __LOADING__;

function calculateAgeFactor(age: number): number {
  const t = Math.max(0, Math.min(1, (age - MIN_AGE) / (MAX_AGE - MIN_AGE)));
  return AGE_CURVE.base + AGE_CURVE.linear * t + AGE_CURVE.quadratic * t * t;
}

export function calculateMonthlyPrice(
  age: number,
  coverageAmount: number,
  plan: "grundschutz" | "komfort" | "premium",
  riskClassMultiplier: number = 1.0,
  paymentModeDiscount: number = 1.0
): number {
  const units = coverageAmount / COVERAGE_UNIT;
  const ageFactor = calculateAgeFactor(age);
  const netPremium = BASE_RATES[plan] * units * ageFactor * riskClassMultiplier * paymentModeDiscount;
  const grossPremium = netPremium * (1 + LOADING);
  return Math.round(grossPremium * 100) / 100;
}

export function calculatePaymentDuration(age: number): number {
  // Formula varies by product:
  // Life/BU/Pflege: retirementAge - age (e.g., 67 - age)
  // Funeral: 85 - age
  // Property/Liability: 1 (annual renewal)
  // Fixed term: policyTerm
  return __PAYMENT_DURATION_FORMULA__;
}

export function getAgeFromBirthYear(birthYear: number, startYear?: number): number {
  const year = startYear ?? new Date().getFullYear();
  return year - birthYear;
}
```

## Calibration Notes

The base rates are calibrated so that a "typical" customer sees realistic-looking prices:

| Product | Typical customer | Komfort price | Reality check |
|---------|-----------------|---------------|---------------|
| Sterbegeld | 44yo, €8k | ~€30/mo | ✓ ERGO charges €25-35 |
| BU | 30yo desk worker, €2k/mo | ~€55/mo | ✓ Market range €40-80 |
| Zahnzusatz | 35yo, €1.5k budget | ~€22/mo | ✓ Market range €15-40 |
| Hausrat | 50m² urban, €50k | ~€8/mo | ✓ Market range €5-15 |
| Haftpflicht | Single, €10M | ~€6/mo | ✓ Market range €4-10 |
| Risikoleben | 35yo non-smoker, €200k | ~€12/mo | ✓ Market range €8-20 |
| Tierkranken | Dog age 3, €5k budget | ~€35/mo | ✓ Market range €25-60 |
| Kfz | 35yo, midsize, SF 10 | ~€65/mo | ✓ Market range €40-100 |

These are intentionally center-of-market. The risk class and age adjustments create variance around this center.

## Risk Class Multipliers

Products that have risk classes use multipliers that shift the base rate:

```
0.70–0.85 = Low risk (desk job, non-smoker, rural area, massiv building)
1.00      = Standard / reference risk
1.20–1.40 = Elevated risk (manual labor, suburban, family status)
1.50–2.20 = High risk (hazardous job, smoker, urban, heavy breed dog)
```

The multiplier applies uniformly across all tiers. So if a smoker pays 1.8× the non-smoker rate, that applies to Grundschutz, Komfort, and Premium equally.

## Payment Duration

The payment duration affects how long the customer pays, which appears on the plan selection page. It varies by product:

| Product type | Formula | Example |
|-------------|---------|---------|
| Funeral | 85 − age | 44yo → 41 years |
| BU / Pflege / Krankentagegeld | 67 − age | 30yo → 37 years |
| Term life | Fixed term (10-30 years) | 20 years → 20 years |
| Property / Liability / Travel | 1 (annual) | Always 1 year |
| Pet | Ongoing (no fixed end) | Display "laufend" |
