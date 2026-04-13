# Rechtsschutz -- Updated Products Entry

## Product: rechtsschutz

| Parameter | Value |
|-----------|-------|
| **ID** | rechtsschutz |
| **Category** | liability |
| **Age range** | 18+ (no upper limit in calculator) |
| **Coverage** | Fixed by tier: Smart = 2M EUR, Best = unlimited |
| **Coverage unit** | N/A (no coverage selection) |
| **Risk class** | None |
| **Payment duration** | 1 year or 3 years (10% Dauernachlass) |
| **Waiting period** | None for most legal areas |

### Tiers (2 only, not 3)

| ERGO Name | Our Mapping | Coverage Limit |
|-----------|-------------|---------------|
| Smart | Grundschutz | 2,000,000 EUR |
| Best | Premium | Unlimited |

Note: There is no middle tier. Map Smart -> Grundschutz and Best -> Premium, or rename to Smart/Best.

### Baustein Base Rates (Single, SB 150, monthly)

| Baustein | Smart | Best |
|----------|-------|------|
| Privat | 16.71 | 24.84 |
| Beruf (add-on) | +7.83 | +9.10 |
| Wohnen (add-on) | +1.31 | +1.83 |
| Verkehr (add-on) | +8.30 | +14.59 |
| All 4 total | 34.15 | 50.36 |

### Pricing Formula

    monthlyPremium = baustein_sum * familyMultiplier * sbDiscount * contractDiscount * youthDiscount

Where:
- baustein_sum = sum of selected Baustein prices for chosen tier
- familyMultiplier = 1.0 (Single/Alleinerziehend) or ~1.12 (Paar/Familie)
- sbDiscount = 1.0 (SB 150) / 0.911 (SB 250) / 0.779 (SB 500)
- contractDiscount = 1.0 (1yr) / 0.90 (3yr)
- youthDiscount = 0.90 (under 25) / 1.0 (25+)

### Age Curve

NONE. Pricing is flat regardless of age. Set: base=1.0, linear=0.0, quadratic=0.0

### Key Differences from Current Model

1. NO age-based pricing (our model has quadratic curve)
2. NO coverage amount slider (our model has 100K-1M range)
3. TWO tiers instead of THREE
4. ADDITIVE Bausteine (legal area modules) instead of fixed tier benefits
5. Family status affects pricing (~12% surcharge for Paar/Familie)
6. Multiple discount levers (SB, contract duration, youth, payment mode)
7. Vital variant for retirees (different base rates, no Beruf)

### Recommended Template

Template D (new): Flat Rate Additive Configurator -- does not fit existing Templates A/B/C.
