# ERGO Rechtsschutzversicherung -- Pricing Analysis

## Derived Parameters

- **Pricing model**: Flat rate, age-independent, additive Baustein configurator
- **Tiers**: Smart (2M EUR coverage) and Best (unlimited coverage)
- **Age curve**: NONE -- pricing is flat regardless of age
- **Under-25 discount**: 10% Startbonus (exact, displayed in UI)
- **Tier relationship**: NOT multiplicative -- each tier has independent Baustein prices with variable ratios (1.16x to 1.76x per Baustein)
- **Baustein model**: Perfectly additive (0.00 EUR error across all combinations)
- **Family multiplier**: Single = 1.0, Familie/Paar ~1.11-1.12x

## Smart Baustein Rates (Single, SB 150, monthly)

| Baustein | Smart | Best | Best/Smart Ratio |
|----------|-------|------|-----------------|
| Privat (base) | 16.71 | 24.84 | 1.487 |
| + Beruf | 7.83 | 9.10 | 1.162 |
| + Wohnen | 1.31 | 1.83 | 1.397 |
| + Verkehr | 8.30 | 14.59 | 1.758 |
| **All 4** | **34.15** | **50.36** | **1.475** |

## Comparison with Our Assumptions

| Parameter | Our value | ERGO actual | Delta | Severity |
|-----------|-----------|-------------|-------|----------|
| **Pricing model** | Coverage-based polynomial | **Flat rate additive** | Structural mismatch | **CRITICAL** |
| **Tiers** | Grundschutz/Komfort/Premium | **Smart/Best** | Different tier names | **HIGH** |
| **Number of tiers** | 3 | **2** | Wrong count | **HIGH** |
| **Coverage selection** | 100K-1M slider | **None** (tier determines coverage) | Structural mismatch | **CRITICAL** |
| **Age curve** | Quadratic (base=0.90, linear=0.15, quad=0.05) | **NONE (flat rate)** | Structural mismatch | **CRITICAL** |
| **Age range** | 18-75 | No practical limit (20-70+ tested) | Over-constrained | MEDIUM |
| **Risk class** | None | None | Match | -- |
| **Waiting period** | 3 months for all tiers | **None** (many areas without Wartezeit) | Wrong | MEDIUM |
| **Base rate (monthly)** | Grundschutz 12.50 / Komfort 22.00 / Premium 35.00 | Smart P+B 24.54 / Best P+B 33.94 | Wrong basis | **CRITICAL** |
| **Loading** | 23% | Unknown/embedded in prices | N/A | N/A |

## Critical Structural Mismatches

### 1. No Age-Based Pricing
Our model applies a quadratic age factor. ERGO Rechtsschutz pricing is completely flat -- a 25-year-old and a 65-year-old pay exactly the same (except the under-25 youth bonus). This makes economic sense: legal risk doesn't correlate with age the way health risk does.

### 2. No Coverage Amount
Our model has a coverage slider (100K-1M EUR). ERGO doesn't offer this -- coverage is fixed by tier:
- Smart: 2 million EUR
- Best: unlimited

### 3. Bausteine Instead of Tiers
Our model uses three benefit tiers. ERGO uses TWO tiers (Smart/Best) combined with FOUR toggleable legal area modules (Privat, Beruf, Wohnen, Verkehr). These are independently priced and additive.

### 4. Family Status Affects Pricing
Our model doesn't account for family status. ERGO charges ~12% more for Familie/Paar vs Single/Alleinerziehend.

### 5. Vital (Senior) Variant
Retirees get a different product variant ("Vital") with different base rates and no Beruf Baustein.

## Discount Structure

| Discount | Amount | Notes |
|----------|--------|-------|
| Under-25 Startbonus | -10% | Always applies (SB always present) |
| SB 250 | -8.9% | vs SB 150 base |
| SB 500 | -22.1% | vs SB 150 base |
| 3-year contract | -10.0% | Exact 10% Dauernachlass |
| Quarterly payment | -0.9% | vs monthly |
| Semi-annual payment | -2.8% | vs monthly |
| Annual payment | -5.7% | vs monthly |

## Data Quality

- **Total data points**: 42
- **Baustein additivity error**: 0.00 EUR (perfect)
- **Age independence verified**: At ages 20, 35, 60, 70
- **Family status verified**: Single, Alleinerziehend, Paar, Familie
- **Employment types verified**: Arbeitnehmer, Beamter, Selbststandig, Ruhestand
- **Confidence**: **HIGH** -- clear, deterministic pricing with no ambiguity

## Recommended Template

This product does NOT fit Templates A, B, or C. It requires a new template:

**Template D: Flat Rate Additive Configurator**

    monthlyPremium = baustein_sum * familyMultiplier * sbDiscount * contractDiscount * youthDiscount * paymentModeDiscount

    baustein_sum = sum of selected Baustein base rates for the chosen tier

No age factor. No coverage factor. No per-unit pricing. Pure configurator.
