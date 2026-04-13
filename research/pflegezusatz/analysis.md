# ERGO Pflegezusatzversicherung — Pricing Analysis

## Key Findings

### 1. Product Structure is Fundamentally Different from Assumptions

**Assumed**: 3 tiers of one product (Grundschutz, Komfort, Premium) with monthly Pflegegeld
**Actual**: 3 separate products with completely different pricing models

| Product | Price Model | Coverage Model |
|---------|-------------|---------------|
| PTG (Tagegeld) | Age-dependent, per EUR/day | 5-160 EUR/day, perfectly linear |
| PZU (Zuschuss) | Fixed 29.70/59.40 EUR | 50%/100% of statutory benefits |
| KFP (Foerder) | Fixed 25.72 EUR | State-subsidized, standardized |

### 2. PTG Coverage Linearity — PERFECT

Coverage is perfectly linear (verified at ages 20, 50, 65):
```
monthlyPremium = ratePerEurDaily(age) * dailyBenefitAmount
```

Examples:
- Age 20: rate = 0.591 EUR per 1 EUR/day
- Age 50: rate = 2.136 EUR per 1 EUR/day
- Age 65: rate = 4.332 EUR per 1 EUR/day

### 3. PTG Age Curve — Exponential Growth

The price grows approximately 5.4%/year compounded:
- Age 20: 5.91 EUR to Age 99: 373.48 EUR (63x ratio at 10 EUR/day)
- Ages 0-15: flat band at 4.51 EUR
- Ages 16-19: flat band at 4.62 EUR
- Age 65 anomaly: only 1.48% growth (vs ~5% typical), likely regulatory adjustment

### 4. Model Fitting Results

| Model | R-squared | Max Error | Mean Error |
|-------|-----------|-----------|------------|
| Power | 0.998976 | 5.61 EUR | 2.70 EUR |
| Exponential | 0.998967 | 11.85 EUR | 2.20 EUR |
| Cubic | 0.997291 | 12.08 EUR | 4.39 EUR |
| Log-linear | 0.962741 | 64.72 EUR | 9.96 EUR |
| Quadratic | 0.955938 | 54.54 EUR | 17.25 EUR |

For restricted ranges (ages 25-60 or 30-65), quadratic R-squared improves to ~0.998.

### 5. Recommendation: Template B (Lookup Table)

The full age range (0-99) with 82.8x price ratio cannot be accurately modeled by a simple polynomial.

## Assumptions vs Reality

| Parameter | Assumed | Actual | Delta |
|-----------|---------|--------|-------|
| Product type | 3 tiers | 3 separate products | WRONG |
| Coverage | 250-3000 EUR/month | 5-160 EUR/day (=150-4800/month) | Different unit |
| Age range | 20-65 | 0-99 | Much wider |
| Risk class | None | None | CORRECT |
| Age curve | quadratic (0.50/0.25/0.65) | Exponential ~5.4%/year | WRONG shape |
| Loading | 25% | N/A (included in rates) | N/A |
| Waiting period | 5y/3y/1y by tier | None (PTG/PZU), Yes (KFP) | Partially wrong |

## Confidence: HIGH
