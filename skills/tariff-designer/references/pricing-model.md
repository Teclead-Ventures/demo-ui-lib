# Pricing Engine Model

This document defines the pricing formulas used across insurance products. There are **7 pricing templates** depending on the product type:

- **Template A** (polynomial): Person products with moderate age curves — `baseRate × units × ageFactor × riskClass × (1+loading)`
- **Template A+step**: Variant of A with step-function age bands instead of polynomial — Unfall (binary 1.0×/2.0× at age 65)
- **Template B** (lookup table): Products with exponential/steep age curves — lookup + interpolation
- **Template C** (property/additive): Property products — `(rate × m² + intercept) × regionMult × factors`
- **Template D** (flat-rate configurator): Products with no age curve and additive module pricing — Rechtsschutz, Haftpflicht
- **Template E** (motor): Additive component model — `HP_base × ageFactor × HP_SF% + VK_base × ageFactor × VK_SF% + tierAddon`
- **Template F** (travel): Trip-cost-based — percentage of trip cost or sqrt curve with age-band multipliers

## Template A: The Standard Formula

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

Products using Template A: Zahnzusatz (age-band approximation, R²=0.997). The only verified Template A product.

Products using Template A+step: Unfall (binary 1.0×/2.0× at age 65).

Products using Template B: Risikoleben, Sterbegeld, Pflegezusatz/PTG, Krankentagegeld (quadratic with plateau, separate AN/SE tariff tables).

Products using Template C: Hausrat, Wohngebäude (per-m², construction year bands instead of age).

Products using Template D: Rechtsschutz (Baustein toggles, no age curve), Haftpflicht (Baustein toggles, binary <36 Startbonus).

Products using Template E: Kfz (no age curve, 51 SF levels), Motorrad (WITH U-shaped age curve, 22 SF levels).

Products using Template F: Reise (trip-cost-based, 3 product categories, age bands, external ERV domain).

Products with no online calculator: Tierkranken (agent-only), BU (advisor-only), Cyber (404).

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
| Sterbegeld | ~~1.00~~ | ~~−1.62~~ | ~~5.47~~ | **Template B — DO NOT use polynomial**. Lookup table in products.md. | Age-dependent tier multipliers + fixed fee make polynomial inaccurate |
| BU | 0.70 | 0.50 | −0.15 | Bell curve ~45-50 | Disability risk peaks mid-career, drops near retirement |
| Zahnzusatz | 0.13 | 3.08 | −0.52 | Steep near-linear | ERGO uses discrete age bands; polynomial is smooth approximation (R²=0.997) |
| Risikoleben | N/A | N/A | N/A | **Lookup table required** (quadratic R²=0.958 inadequate) | 60yo pays 31× of 25yo; smoker multiplier is age-dependent (1.87-3.92×) — polynomial cannot model this |
| Pflege (PTG) | N/A | N/A | N/A | **Lookup table required** (exponential ~5.4%/year, quadratic R²=0.956) | 82 per-year rates ages 0-99; PZU/KFP are fixed-price separate products |
| Tierkranken | 0.60 | 0.10 | 0.90 | Very steep after 7-8 | ⚠ UNVERIFIED — no online calculator |
| Motorrad | 2.566 | -0.0698 | 0.000750 | U-curve (raw age, not normalized) | Min at ~47, young riders +34%, elderly +21% |
| Krankentagegeld | N/A | N/A | N/A | **Lookup table** (quadratic with plateau at 67+) | Separate AN/SE tables, MAPE<1% |
| Wohngebäude | N/A | N/A | N/A | **No age field** — construction year bands instead | Pre-2000=1.07×, 2010=0.83×, 2020=0.66× |
| Reise | N/A | N/A | N/A | **Age bands** (3 bands: ≤40, 41-64, 65+) | ≤40=1.0, 41-64=1.10, 65+=2.09 |
| Unfall | N/A | N/A | N/A | **Step function**: 1.0× (age <65), 2.0× (age ≥65) | Binary age band, not polynomial |
| Krankentagegeld | 0.70 | 0.35 | 0.20 | Steady increase | Illness duration increases with age |
| Hausrat | N/A | N/A | N/A | **Binary** (under-36: 0.87×, else 1.0) | ERGO uses 13% Startbonus for under-36, additive tier model, per-m² pricing |
| Haftpflicht | N/A | N/A | N/A | **Binary band**: <36 = ×0.87 (Startbonus), 36+ = ×1.0 | Template D — no polynomial age curve |
| Cyber | 1.00 | 0.00 | 0.00 | Flat | Not age-dependent |
| Kfz | N/A | N/A | N/A | **NONE** — age has zero effect on pricing | Template E — SF-Klasse is the primary driver, not age |
| Reise | 0.75 | 0.10 | 0.30 | Gentle U | Young adventurers + elderly travelers |

## Flat-Rate Products

Some products (Haftpflicht, Rechtsschutz, Kfz, Cyber) have flat-rate pricing where the coverage amount affects the payout cap but not the premium significantly. For these products, set `coverageUnit = defaultCoverage` so that `coverageUnits = 1`. The base rate then IS the monthly net premium for the reference customer.

| Product | coverageUnit | Why |
|---------|-------------|-----|
| Haftpflicht | N/A — uses Template D | No coverage unit; coverage fixed by tier (Smart=€10M, Best=€50M), pricing is per-Baustein toggle |
| Rechtsschutz | N/A — uses Template D | No coverage unit; pricing is per-Baustein toggle, not per-coverage-amount |
| Kfz | N/A — uses Template E | No coverage unit; pricing is per-vehicle via HSN/TSN + SF-Klasse lookup |
| Cyber | = defaultCoverage (€25k) | Premium is flat, coverage sets the max payout |
| Zahnzusatz | = 1 (flat rate) | Tariff name (DS75/DS90/DS100) IS the coverage level (reimbursement %). No user-selectable coverage amount. |

The formula still works: `baseRate × 1 × ageFactor × riskClass × paymentMode × (1 + loading)`.

## Age-Band Pricing (discovered via ERGO research)

Some products (e.g., Zahnzusatz) use **discrete age bands** rather than a smooth polynomial. ERGO's Zahnzusatz has 6 bands with flat monthly prices per band. Our polynomial age curve is a smooth approximation that fits band midpoints with R²≈0.997 but deviates at band boundaries.

For products where the product entry includes a "Note — Age bands" section, the polynomial is an approximation. The actual ERGO pricing uses a step function. The demo should use the polynomial for smooth UX (slider-reactive pricing), but the prices won't match ERGO exactly at every age — they match at band midpoints and deviate up to ±20-30% at band edges. This is acceptable for demo purposes.

## Lookup Table Pricing (discovered via ERGO research, 2026-04-13)

Some products have age curves too steep for a single polynomial (R² < 0.96). For these, use a **lookup table with linear interpolation** instead of the polynomial formula:

- **Risikoleben**: 60yo pays 31× of 25yo. Quadratic R²=0.958 (inadequate). Cubic R²=0.995 (better but still loses accuracy at extremes). Additionally, the smoker multiplier is age-dependent (1.87× at 25 to 3.92× at 50), which the simple `riskClassMultiplier` parameter cannot model. Use the lookup table from products.md and interpolate between sampled ages.

- **Sterbegeld**: Cubic fits well (R²=0.997) but tier multipliers are age-dependent (Komfort/Grundschutz ranges 1.02-1.11×). The lookup table in products.md gives exact per-age rates. Has a fixed fee component (~€1.80/month) independent of coverage.

For demo purposes, the TypeScript implementation can use the lookup table with `Array.find()` for the nearest ages and linear interpolation between them. This is more accurate than the polynomial and just as fast.

## Additive Tier Models (discovered via ERGO research, 2026-04-13)

ERGO Hausrat uses an **additive** tier model where Best = Smart + ~€3.39/month (fixed amount), NOT a multiplicative ratio. This is fundamentally different from the `baseRate × tier` model used by other products. The per-m² rate (0.1114 EUR/m²/month) is the same for both tiers — only the fixed base differs (Smart: €0.25, Best: €3.64).

For products with additive tier models, the pricing formula becomes:
```
price = (ratePerUnit × units + tierFixedBase) × regionMult × otherFactors
```

Currently only Hausrat uses this model. Other property products should be verified when researched.

## Per-m² Coverage Model (discovered via ERGO research, 2026-04-13)

ERGO Hausrat derives coverage automatically from living space: `coverage = 650 EUR/m² × m²`. The user enters m², not a coverage amount. This means `coverageUnits` is actually `m²` for this product, not `coverage / coverageUnit`.

## TypeScript Implementation Templates

The demo pipeline uses one of these templates depending on the product's pricing model. The tariff-designer picks the right template and fills in the constants.

### Template A: Polynomial age curve (most person products)

Used by: BU, Zahnzusatz (age-band approx.), Tierkranken, Krankentagegeld. NOT Unfall (uses A+step) or Pflege (uses B).

```typescript
// src/lib/data/pricing.ts — Template A (polynomial)

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
```

### Template B: Lookup table with interpolation (steep/complex age curves)

Used by: Risikoleben, Sterbegeld, Pflegezusatz/PTG. Each has a different function signature — the TypeScript below is Risikoleben-specific. For Sterbegeld, use the per-age base rate table from products.md + fixed fee. For Pflegezusatz, use `price = ageRate(age) × dailyBenefit` with the per-year rate table from products.md (no tiers, no risk class).

```typescript
// src/lib/data/pricing.ts — Template B (lookup table)

// Lookup table: age → monthly price for reference case
// Reference: €200k coverage, 20yr term, Nichtraucher 10+
const PRICE_TABLE: Record<string, Record<number, number>> = {
  grundschutz: { 25: 3.94, 30: 5.15, 35: 7.54, 40: 12.16, 45: 20.32, 50: 34.34, 55: 60.94, 60: 121.61 },
  komfort:     { 25: 4.97, 30: 6.51, 35: 9.54, 40: 15.42, 45: 25.82, 50: 43.65, 55: 77.48, 60: 154.68 },
  premium:     { 25: 7.50, 30: 9.54, 35: 13.54, 40: 21.30, 45: 35.02, 50: 58.53, 55: 103.11, 60: 204.46 },
};

// Smoker multipliers are age-dependent (applied to Nichtraucher 10+ base)
const SMOKER_MULTIPLIERS: Record<number, number> = {
  25: 1.87, 30: 2.23, 35: 2.65, 40: 3.02, 45: 3.46, 50: 3.92, 55: 3.83, 60: 3.19,
};
const NS1_MULTIPLIER = 1.17; // Nichtraucher 1+ (approximately constant)

// Term scaling relative to 20yr reference
const TERM_FACTORS: Record<number, number> = {
  10: 0.63, 15: 0.77, 20: 1.00, 25: 1.38, 30: 1.95,
};

const REFERENCE_COVERAGE = 200000;

// Note: ERGO has a small fixed fee component (~€0.91/month for Komfort at age 35)
// that makes coverage scaling slightly non-linear. This template uses pure linear
// scaling for simplicity, which introduces ~5% error at low coverage (€50k) and
// ~1% error at high coverage (€500k). Acceptable for demo purposes.
const FIXED_FEE = 0; // Set to ~0.91 for more accurate low-coverage pricing

function interpolate(table: Record<number, number>, age: number): number {
  const ages = Object.keys(table).map(Number).sort((a, b) => a - b);
  if (age <= ages[0]) return table[ages[0]];
  if (age >= ages[ages.length - 1]) return table[ages[ages.length - 1]];
  const upper = ages.find((a) => a >= age)!;
  const lower = ages[ages.indexOf(upper) - 1];
  const t = (age - lower) / (upper - lower);
  return table[lower] + t * (table[upper] - table[lower]);
}

function interpolateTerm(termYears: number): number {
  const terms = Object.keys(TERM_FACTORS).map(Number).sort((a, b) => a - b);
  if (termYears <= terms[0]) return TERM_FACTORS[terms[0]];
  if (termYears >= terms[terms.length - 1]) return TERM_FACTORS[terms[terms.length - 1]];
  const upper = terms.find((t) => t >= termYears)!;
  const lower = terms[terms.indexOf(upper) - 1];
  const t = (termYears - lower) / (upper - lower);
  return TERM_FACTORS[lower] + t * (TERM_FACTORS[upper] - TERM_FACTORS[lower]);
}

export function calculateMonthlyPrice(
  age: number,
  coverageAmount: number,
  plan: "grundschutz" | "komfort" | "premium",
  smokerClass: "ns10" | "ns1" | "raucher" = "ns10",
  termYears: number = 20,
  paymentModeDiscount: number = 1.0,
): number {
  const basePrice = interpolate(PRICE_TABLE[plan], age);
  const coverageFactor = coverageAmount / REFERENCE_COVERAGE;
  const termFactor = interpolateTerm(termYears);
  const smokerFactor =
    smokerClass === "raucher" ? interpolate(SMOKER_MULTIPLIERS, age) :
    smokerClass === "ns1" ? NS1_MULTIPLIER : 1.0;
  const price = (basePrice * coverageFactor + FIXED_FEE) * termFactor * smokerFactor * paymentModeDiscount;
  return Math.round(price * 100) / 100;
}
```

### Template C: Property product (additive tiers, per-m² pricing)

Used by: Hausrat (and potentially Wohngebäude after research)

```typescript
// src/lib/data/pricing.ts — Template C (property / additive tiers)

// ERGO Hausrat has 2 tiers with ADDITIVE pricing (not multiplicative)
// The per-m² rate is the same for both tiers; only the fixed base differs
// Tier name mapping: smart → grundschutz, best → komfort (for UI/database)
// The plan parameter uses ERGO's native names; the UI layer maps to internal names
type HausratPlan = "smart" | "best";
const PLAN_DISPLAY_NAMES: Record<HausratPlan, string> = { smart: "Smart", best: "Best" };
const PLAN_INTERNAL_NAMES: Record<HausratPlan, string> = { smart: "grundschutz", best: "komfort" };

const TIER_CONFIG: Record<HausratPlan, { ratePerM2: number; fixedBase: number }> = {
  smart:  { ratePerM2: 0.1114, fixedBase: 0.254 },
  best:   { ratePerM2: 0.1114, fixedBase: 3.642 },
};

const COVERAGE_PER_M2 = 650; // EUR coverage per m²

// Regional multipliers (ZIP-specific, München = 1.0 reference)
const REGION_MULTIPLIERS: Record<string, number> = {
  "54290": 0.768,  // Trier
  "90402": 0.788,  // Nürnberg
  "01067": 0.966,  // Dresden
  "80331": 1.000,  // München (reference)
  "24103": 1.078,  // Kiel
  "50667": 1.312,  // Köln
  "20095": 1.365,  // Hamburg
  "10117": 1.365,  // Berlin
};
const DEFAULT_REGION_MULTIPLIER = 1.0;

// Factor multipliers
const FLOOR_FACTORS: Record<string, number> = {
  keller: 1.104, erdgeschoss: 1.104,
  "1og": 1.0, "2og": 1.0, "3og_plus": 1.0,
};
const BUILDING_TYPE_FACTORS: Record<string, number> = {
  mehrfamilienhaus: 1.0, einfamilienhaus: 1.060,
};
const AGE_FACTOR = { under36: 0.870, default: 1.0 };
const DEDUCTIBLE_FACTORS: Record<string, number> = {
  none: 1.0, "300": 0.927,
};
const CONTRACT_DURATION_FACTORS: Record<string, number> = {
  "1": 1.111, "3": 1.0,
};

export function calculateMonthlyPrice(
  livingSpaceM2: number,
  plan: "smart" | "best",
  zip: string,
  floor: string = "2og",
  buildingType: string = "mehrfamilienhaus",
  age: number = 40,
  deductible: string = "none",
  contractYears: string = "3",
  paymentModeDiscount: number = 1.0,
): number {
  const tier = TIER_CONFIG[plan];
  const basePrice = tier.ratePerM2 * livingSpaceM2 + tier.fixedBase;
  const regionMult = REGION_MULTIPLIERS[zip] ?? DEFAULT_REGION_MULTIPLIER;
  const floorMult = FLOOR_FACTORS[floor] ?? 1.0;
  const buildingMult = BUILDING_TYPE_FACTORS[buildingType] ?? 1.0;
  const ageMult = age < 36 ? AGE_FACTOR.under36 : AGE_FACTOR.default;
  const deductibleMult = DEDUCTIBLE_FACTORS[deductible] ?? 1.0;
  const contractMult = CONTRACT_DURATION_FACTORS[contractYears] ?? 1.0;
  const price = basePrice * regionMult * floorMult * buildingMult * ageMult * deductibleMult * contractMult * paymentModeDiscount;
  return Math.round(price * 100) / 100;
}

export function getCoverageFromM2(m2: number): number {
  return m2 * COVERAGE_PER_M2;
}
```

### Template A+step: Step-function age bands (Unfall)

Used by: Unfall (binary 1.0×/2.0× at age 65)

Template A formula with age factor replaced by a step function instead of polynomial.

```typescript
// src/lib/data/pricing.ts — Template A+step (step-function age bands)

const BASE_RATES: Record<"basic" | "smart" | "best", number> = {
  basic: 0.754,  // EUR/month per 10k coverage, Gruppe A, under-65
  smart: 1.524,
  best: 1.954,
};

const COVERAGE_UNIT = 10000;

// Step-function age bands (NOT polynomial)
const AGE_BANDS: Array<{ maxAge: number; multiplier: number }> = [
  { maxAge: 64, multiplier: 1.0 },
  { maxAge: 75, multiplier: 2.0 },
];

function getAgeBandMultiplier(age: number): number {
  const band = AGE_BANDS.find((b) => age <= b.maxAge);
  return band?.multiplier ?? AGE_BANDS[AGE_BANDS.length - 1].multiplier;
}

// Occupation risk groups — mapped from autocomplete job titles
const OCCUPATION_MULTIPLIERS: Record<string, number> = {
  A: 1.0,   // Büro, Verwaltung, Lehrer
  B: 1.55,  // Dachdecker, Maurer, Polizist
  C: 3.10,  // Berufskraftfahrer (Güterverkehr)
};

export function calculateMonthlyPrice(
  age: number,
  coverageAmount: number,
  plan: "basic" | "smart" | "best",
  occupationGroup: "A" | "B" | "C" = "A",
): number {
  const units = coverageAmount / COVERAGE_UNIT;
  const ageMult = getAgeBandMultiplier(age);
  const occMult = OCCUPATION_MULTIPLIERS[occupationGroup];
  const price = BASE_RATES[plan] * units * ageMult * occMult;
  return Math.round(price * 100) / 100;
}
```

### Template D: Flat-rate additive configurator (Rechtsschutz)

Used by: Rechtsschutz (no age curve, no coverage slider, additive Baustein modules)

```typescript
// src/lib/data/pricing.ts — Template D (flat-rate additive configurator)

type RechtsschutzPlan = "smart" | "best";
type Baustein = "privat" | "beruf" | "wohnen" | "verkehr";

// Baustein base rates (Single, SB €150, monthly)
const BAUSTEIN_RATES: Record<RechtsschutzPlan, Record<Baustein, number>> = {
  smart: { privat: 16.71, beruf: 7.83, wohnen: 1.31, verkehr: 8.30 },
  best:  { privat: 24.84, beruf: 9.10, wohnen: 1.83, verkehr: 14.59 },
};

const FAMILY_MULTIPLIERS: Record<string, number> = {
  single: 1.0,
  alleinerziehend: 1.0,
  paar: 1.12,
  familie: 1.12,
};

const SB_DISCOUNTS: Record<string, number> = {
  "150": 1.0,
  "250": 0.911,
  "500": 0.779,
};

const CONTRACT_DISCOUNTS: Record<string, number> = {
  "1": 1.0,
  "3": 0.90,
};

export function calculateMonthlyPrice(
  plan: RechtsschutzPlan,
  bausteine: Baustein[],
  familyStatus: string = "single",
  sb: string = "150",
  contractYears: string = "1",
  age: number = 30,
  paymentModeDiscount: number = 1.0,
): number {
  // Sum selected Bausteine (additive, verified 0.00 error)
  const bausteinSum = bausteine.reduce((sum, b) => sum + BAUSTEIN_RATES[plan][b], 0);
  const familyMult = FAMILY_MULTIPLIERS[familyStatus] ?? 1.0;
  const sbMult = SB_DISCOUNTS[sb] ?? 1.0;
  const contractMult = CONTRACT_DISCOUNTS[contractYears] ?? 1.0;
  const youthMult = age < 25 ? 0.90 : 1.0;
  const price = bausteinSum * familyMult * sbMult * contractMult * youthMult * paymentModeDiscount;
  return Math.round(price * 100) / 100;
}
```

### Template E: Kfz-specific additive component model

Used by: Kfz (additive HP+VK components, separate SF lookup tables, no age curve)

```typescript
// src/lib/data/pricing.ts — Template E (Kfz additive components)

type KfzPlan = "smart" | "best";
type CoverageType = "hp_only" | "hp_tk" | "hp_vk";

// Base rates at 100% SF (VW Golf VIII reference, München, 12k km, VK500/TK150)
const HP_BASE: Record<KfzPlan, number> = { smart: 82.48, best: 91.85 };
const VK_BASE: Record<KfzPlan, number> = { smart: 156.82, best: 208.15 };
const TK_RATE: Record<KfzPlan, number> = { smart: 24.50, best: 34.87 }; // No SF for TK
const TIER_ADDON: Record<KfzPlan, number> = { smart: 0, best: 1.73 };

// SF lookup tables (percentage applied to base, 51 levels)
const HP_SF: Record<number, number> = {
  0: 86, 0.5: 66, 1: 53, 2: 50, 3: 47, 4: 44, 5: 42, 6: 40, 7: 38, 8: 36, 9: 35,
  10: 33, 11: 32, 12: 31, 13: 30, 14: 29, 15: 28, 16: 27, 17: 26, 18: 26, 19: 25,
  20: 24, 21: 24, 22: 23, 23: 23, 24: 22, 25: 22, 26: 21, 27: 21, 28: 21, 29: 20,
  30: 20, 31: 19, 32: 19, 33: 19, 34: 18, 35: 18, 36: 18, 37: 18, 38: 17, 39: 17,
  40: 17, 41: 17, 42: 16, 43: 16, 44: 16, 45: 16, 46: 16, 47: 16, 48: 15, 49: 15, 50: 15,
};

const VK_SF: Record<number, number> = {
  0: 54, 0.5: 49, 1: 44, 2: 42, 3: 41, 4: 39, 5: 38, 6: 37, 7: 36, 8: 34, 9: 33,
  10: 33, 11: 32, 12: 31, 13: 30, 14: 29, 15: 28, 16: 28, 17: 27, 18: 27, 19: 26,
  20: 25, 21: 25, 22: 24, 23: 24, 24: 23, 25: 23, 26: 23, 27: 22, 28: 22, 29: 21,
  30: 21, 31: 21, 32: 20, 33: 20, 34: 20, 35: 19, 36: 19, 37: 19, 38: 19, 39: 18,
  40: 18, 41: 18, 42: 18, 43: 17, 44: 17, 45: 17, 46: 17, 47: 16, 48: 16, 49: 16, 50: 15,
};

// SB impact on VK (multiplier relative to VK500/TK150 base)
const SB_FACTORS: Record<string, number> = {
  "vk_ohne_tk_ohne": 1.654,
  "vk_300_tk_150": 1.070,
  "vk_500_tk_150": 1.000,
  "vk_1000_tk_150": 0.863,
};

function getSFPercent(table: Record<number, number>, sf: number): number {
  if (sf >= 50) return table[50];
  return table[sf] ?? table[Math.floor(sf)];
}

export function calculateMonthlyPrice(
  plan: KfzPlan,
  coverageType: CoverageType,
  sfHP: number,
  sfVK: number = 10,
  sb: string = "vk_500_tk_150",
): number {
  const hpPct = getSFPercent(HP_SF, sfHP) / 100;
  const hpComponent = HP_BASE[plan] * hpPct;

  let kaskoComponent = 0;
  if (coverageType === "hp_vk") {
    const vkPct = getSFPercent(VK_SF, sfVK) / 100;
    const sbFactor = SB_FACTORS[sb] ?? 1.0;
    kaskoComponent = VK_BASE[plan] * vkPct * sbFactor;
  } else if (coverageType === "hp_tk") {
    kaskoComponent = TK_RATE[plan]; // TK has no SF
  }

  const price = hpComponent + kaskoComponent + TIER_ADDON[plan];
  return Math.round(price * 100) / 100;
}
```

### Common utilities (all templates)

```typescript
export function calculatePaymentDuration(age: number): number {
  // Formula varies by product:
  // Funeral: 90 - age (min 5)
  // Life/BU/Pflege: 67 - age
  // Property/Liability: 1 (annual renewal) or 3 (3-year contract)
  // Term life: policyTerm (1-50 years)
  // Pet: Ongoing (display "laufend")
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
| Sterbegeld | 44yo, €8k | ~€27.45/mo | ✓ ERGO charges exactly €27.45 (researched 2026-04-13) |
| BU | 30yo desk worker, €2k/mo | ~€55/mo | ✓ Market range €40-80 |
| Zahnzusatz | 35yo, flat rate | ~€21.70/mo | ✓ ERGO DS90 charges exactly €21.70 |
| Hausrat | 80m², München, MFH 2.OG | Smart €9.01, Best €12.40 | ✓ ERGO exact (researched 2026-04-13, additive tier model) |
| Haftpflicht | Single, Smart, 3yr, ohne SB, age ≥36 | €6.05/mo | ✓ ERGO exact (researched 2026-04-13, Template D) |
| Risikoleben | 35yo NS 10+, €200k, 20yr | ~€9.54/mo | ✓ ERGO charges exactly €9.54 Komfort (researched 2026-04-13) |
| Tierkranken | Dog age 3 | ~€20-30/mo | ⚠ UNVERIFIED — no online calculator (agent-only product) |
| Kfz | VW Golf VIII, München, 12k km, SF 10, VK500, Best | €100.73/mo (HP €30.31 + VK €68.69 + addon €1.73) | ✓ ERGO exact (researched 2026-04-13, Template E) |
| Motorrad | Honda CBF 500, München, 6k km, SF 10, VK150, Smart, age 36 | ~€33.53/mo | ✓ ERGO verified (researched 2026-04-13, Template E variant) |
| Krankentagegeld | AN, age 30, 43.Tag, €15/day | €8.01/mo (0.534×15) | ✓ ERGO exact (researched 2026-04-13, Template B variant) |
| Reise | Storno Einmal, 1 adult ≤40, €5k trip, Flug, mit SB | €250 (5%×5000) | ✓ ERGO exact (researched 2026-04-13, Template F) |
| Wohngebäude | EFH, 120m², München, Baujahr 2000, SB €500, Smart | ~€47.51/mo | ✓ ERGO verified (researched 2026-04-13, Template C variant) |
| Rechtsschutz | Single, all 4 Bausteine, Smart, SB €150 | €34.15/mo | ✓ ERGO exact (researched 2026-04-13, Template D) |
| Unfall | 36yo, Büro (A), €50k, Smart | €7.62/mo | ✓ ERGO exact (researched 2026-04-13, step-function age) |
| Pflegezusatz (PTG) | 30yo, €10/day | €9.03/mo | ✓ ERGO exact (researched 2026-04-13, Template B) |

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

**Exception — Risikoleben**: The smoker multiplier is **age-dependent** (1.87× at age 25 to 3.92× at age 50), not constant. This product uses Template B (lookup table) which handles this via interpolation. There are also 3 smoker classes (Nichtraucher 10+, Nichtraucher 1+, Raucher), not just 2.

## Payment Duration

The payment duration affects how long the customer pays, which appears on the plan selection page. It varies by product:

| Product type | Formula | Example |
|-------------|---------|---------|
| Funeral | 90 − age (min 5) | 44yo → 46 years |
| BU / Pflege / Krankentagegeld | 67 − age | 30yo → 37 years |
| Term life | Fixed term (1-50 years) | 20 years → 20 years |
| Property / Liability / Travel | 1 (annual) | Always 1 year |
| Pet | Ongoing (no fixed end) | Display "laufend" |
