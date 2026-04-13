# ERGO Risikolebensversicherung - Pricing Analysis

## Data Collection Summary
- Date: 2026-04-13
- Data points: 75
- Ages sampled: 25, 30, 35, 40, 45, 50, 55, 60

## Age Curve (NS10+, 200k, 20yr, monthly EUR)
| Age | Grundschutz | Komfort | Premium |
|-----|------------|---------|---------|
| 25  | 3.94       | 4.97    | 7.50    |
| 30  | 5.15       | 6.51    | 9.54    |
| 35  | 7.54       | 9.54    | 13.54   |
| 40  | 12.16      | 15.42   | 21.30   |
| 45  | 20.32      | 25.82   | 35.02   |
| 50  | 34.34      | 43.65   | 58.53   |
| 55  | 60.94      | 77.48   | 103.11  |
| 60  | 121.61     | 154.68  | 204.46  |

## Curve Fitting
- Quadratic: R2=0.958 (poor), Exponential: R2=0.956 (poor), Cubic: R2=0.995 (good)
- Recommendation: Lookup table with interpolation

## Smoker Multipliers (age-dependent, NOT constant)
| Age | Raucher/NS10+ | NS1+/NS10+ |
|-----|---------------|-------------|
| 25  | 1.87x         | n/a         |
| 30  | 2.23x         | 1.13x       |
| 35  | 2.65x         | n/a         |
| 40  | 3.02x         | 1.17x       |
| 45  | 3.46x         | n/a         |
| 50  | 3.92x         | 1.24x       |
| 55  | 3.83x         | n/a         |
| 60  | 3.19x         | n/a         |

## Coverage: Near-linear with fixed base fee
price = 0.91 + 0.0000432 * coverage

## Term Effect (age 35, NS10+, 200k, Komfort)
10yr: 6.00, 15yr: 7.38, 20yr: 9.54, 25yr: 13.13, 30yr: 18.55

## Tier Ratios: K/G ~1.27x (stable), P/G ~1.68-1.90x (age-dependent)
## Base rates per 25k at 35: G=0.94, K=1.19, P=1.69
