# ERGO Motorradversicherung Pricing Analysis

## Data Collection Summary
- Date: 2026-04-13
- Data points: ~22
- Vehicle: Honda CBF 500, 54 PS (40 kW), 499 ccm, HSN 4124 / TSN 133
- PLZ: 80331 Muenchen (Regionalklasse 5)
- Mileage: 6,000 km/year
- Selbstbeteiligung: VK 150 / TK 150

## Model Type

Template E-variant: Kfz-like additive structure (HP + VK/TK components), with SF lookup tables AND a U-shaped age curve. This extends Kfz Template E by adding age-dependent pricing.

## Pricing Formula

    monthly = HP_base * age_factor(age) * SF_HP_pct / 100
            + VK_base * age_factor(age) * SF_VK_pct / 100   (if Vollkasko)
            + TK_flat                                          (if Teilkasko)
            + best_addon                                       (if Best tier)

## Components (age 36)

### HP Base Rates (at SF 0 = 100%)
| Tier | HP Base | Ratio |
|------|---------|-------|
| Smart | 22.16 | 1.000 |
| Best | 26.99 | 1.218 |

### VK Base Rates (at SF 0 = 100%, SB VK 150/TK 150)
| Tier | VK Base | Ratio |
|------|---------|-------|
| Smart | 78.49 | 1.000 |
| Best | 106.45 | 1.356 |

### TK Rates (flat, no SF scaling)
| Tier | TK Flat |
|------|---------|
| Smart | 7.09 |
| Best | 11.23 |

### Best Add-on
Fixed 1.30 EUR/month (Ersatzfahrzeug Plus + Schutzbrief).

## SF-Klasse Tables (22 levels each)

### Haftpflicht
SF 0=100, 0.5=74, 1=54, 2=48, 3=44, 4=40, 5=38, 6=36, 7=34, 8=32,
9=31, 10=30, 11=29, 12=28, 13=28, 14=27, 15=27, 16=26, 17=26, 18=25,
19=25, 20+=24

### Vollkasko
SF 0=100, 0.5=76, 1=55, 2=49, 3=46, 4=43, 5=40, 6=38, 7=36, 8=35,
9=34, 10=33, 11=32, 12=31, 13=30, 14=30, 15=29, 16=28, 17=28, 18=28,
19=27, 20+=27

## Age Effect

U-shaped curve, minimum around age 47.

| Age | Smart HP SF 10 | Factor (vs 36) |
|-----|----------------|----------------|
| 26 | 8.93 | 1.343 |
| 30 | 6.97 | 1.048 |
| 36 | 6.65 | 1.000 |
| 46 | 6.51 | 0.979 |
| 55 | 6.78 | 1.020 |
| 66 | 8.03 | 1.208 |

Quadratic fit: factor(age) = 2.566 - 0.0698*age + 0.000750*age^2
Minimum at age ~47, factor ~0.94.

## Formula Verification

### HP (Smart, age 36)
| SF | Expected | Actual | Error |
|----|----------|--------|-------|
| 0 (100%) | 22.16 | 22.16 | 0.00 |
| 3 (44%) | 9.75 | 9.75 | 0.00 |
| 10 (30%) | 6.65 | 6.65 | 0.00 |
| 20+ (24%) | 5.32 | 5.32 | 0.00 |

### VK (Smart, age 36)
| VK SF | Expected | Actual | Error |
|-------|----------|--------|-------|
| 0 (100%) | 78.49 | 78.49 | 0.00 |
| 5 (40%) | 31.40 | 31.39 | 0.01 |
| 10 (33%) | 25.90 | 25.91 | 0.01 |

### TK (flat verification)
Smart: 7.09 at SF 0 = 7.09 at SF 10. FLAT.
Best: 11.23 at SF 0 = 11.23 at SF 10. FLAT.

## Confidence

- HP/SF formula: HIGH (zero error at fixed age)
- SF tables: HIGH (from dropdown labels)
- TK flat: HIGH (verified at 2 SF levels)
- Age curve: MEDIUM (6 points, clear U-shape, ~10% max residual)
- VK formula: MEDIUM (Best VK has ~0.8 EUR unexplained surplus)
- Single vehicle and PLZ tested
