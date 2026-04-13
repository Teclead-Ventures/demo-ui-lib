# ERGO Kfz-Versicherung - Pricing Analysis

## Data Collection Summary
- Date: 2026-04-13
- Data points: 28
- Vehicle: VW Golf VIII 1.5 TSI OPF 131 PS (0603/CKM)
- Dimensions tested: VK SF (12 values), HP SF (4 values), Age (3 values), PLZ (3 values), Mileage (3 values), SB (4 values), Coverage (3 types)

## Pricing Formula (Verified)

    Monthly_Premium = HP_component + VK_component + tier_addon
    HP_component = HP_base(vehicle, region, mileage) * HP_SF_pct / 100
    VK_component = VK_base(vehicle, region, mileage, SB) * VK_SF_pct / 100
    tier_addon = 0 (Smart) or ~1.73 EUR/month (Best)

## SF Verification (HP)

HP_base_Best = 91.85 EUR/month (at 100% SF, Muenchen, 12k km)

| HP SF | SF % | Predicted | Actual | Error |
|-------|------|-----------|--------|-------|
| 0     | 86%  | 78.99     | 78.97  | 0.02  |
| 10    | 33%  | 30.31     | 30.31  | 0.00  |
| 20    | 24%  | 22.04     | 22.04  | 0.00  |
| 35    | 18%  | 16.53     | 16.53  | 0.00  |

Model: price = base * SF_pct -- EXACT match

## Age Test

| Birth Year | Age | HP Best | VK Best | Total Best |
|------------|-----|---------|---------|------------|
| 1960       | 66  | 30.31   | 68.69   | 100.73     |
| 1990       | 36  | 30.31   | 68.69   | 100.73     |
| 2000       | 26  | 30.31   | 68.69   | 100.73     |

Result: ZERO age effect

## Mileage Impact (Muenchen, SF 10, Best tier, monthly)

| Mileage (k) | HP Best | VK Best | HP base(100%) | VK base(100%) |
|-------------|---------|---------|---------------|---------------|
| 6           | 26.85   | 55.42   | 81.36         | 167.94        |
| 12          | 30.31   | 68.69   | 91.85         | 208.15        |
| 20          | 34.55   | 91.86   | 104.70        | 278.36        |

Linear fits:
- HP: 23.62 + 0.549 * km_thousands
- VK: 38.82 + 2.619 * km_thousands

## Regional Impact (SF 10, 12k km, Best tier, monthly)

| Region      | RK HP | RK VK | HP Best | VK Best | HP base | VK base |
|-------------|-------|-------|---------|---------|---------|---------|
| Muenchen    | 10    | 7     | 30.31   | 68.69   | 91.85   | 208.15  |
| Koeln       | 10    | 7     | 30.75   | 70.11   | 93.18   | 212.45  |
| Berlin      | 12    | 9     | 35.90   | 83.93   | 108.79  | 254.33  |

## Tier Ratios

| Component | Smart | Best | Smart/Best |
|-----------|-------|------|------------|
| HP base   | 82.48 | 91.85| 0.898      |
| VK base   | 156.82| 208.15| 0.753     |

Best has fixed addon: ~1.73 EUR/month (Mallorca-Police etc.)

## SB Impact on VK (monthly, Best tier, Muenchen, SF 10)

| Selbstbeteiligung  | VK Best | vs VK500 |
|--------------------|---------|----------|
| VK ohne / TK ohne  | 113.62  | 1.654    |
| VK 300 / TK 150    | 73.51   | 1.070    |
| VK 500 / TK 150    | 68.69   | 1.000    |
| VK 1000 / TK 150   | 59.30   | 0.863    |

## Coverage Types (Muenchen, SF 10, 12k km, monthly)

| Coverage         | Smart  | Best   |
|------------------|--------|--------|
| HP only          | 27.22  | 32.04  |
| HP + Teilkasko   | 51.72  | 66.91  |
| HP + Vollkasko   | 78.97  | 100.73 |

## SF Lookup Tables (from calculator dropdown)

### Haftpflicht
SF 0=86, 0.5=66, 1=53, 2=50, 3=47, 4=44, 5=42, 6=40, 7=38, 8=36, 9=35,
10=33, 11=32, 12=31, 13=30, 14=29, 15=28, 16=27, 17=26, 18=26, 19=25,
20=24, 21=24, 22=23, 23=23, 24=22, 25=22, 26=21, 27=21, 28=21, 29=20,
30=20, 31=19, 32=19, 33=19, 34=18, 35=18, 36=18, 37=18, 38=17, 39=17,
40=17, 41=17, 42=16, 43=16, 44=16, 45=16, 46=16, 47=16, 48=15, 49=15, 50+=15

### Vollkasko
SF 0=54, 0.5=49, 1=44, 2=42, 3=41, 4=39, 5=38, 6=37, 7=36, 8=34, 9=33,
10=33, 11=32, 12=31, 13=30, 14=29, 15=28, 16=28, 17=27, 18=27, 19=26,
20=25, 21=25, 22=24, 23=24, 24=23, 25=23, 26=23, 27=22, 28=22, 29=21,
30=21, 31=21, 32=20, 33=20, 34=20, 35=19, 36=19, 37=19, 38=19, 39=18,
40=18, 41=18, 42=18, 43=17, 44=17, 45=17, 46=17, 47=16, 48=16, 49=16, 50+=15

## Template Recommendation

Template E (Kfz-specific, new). Does not fit templates A-D because:
- No age curve
- Additive components (HP + VK)
- Separate SF lookup tables
- Coverage type changes structure
- Multiple dimensions: vehicle, region, mileage, SF, SB

## Confidence: MEDIUM-HIGH

- SF model: HIGH (exact verification)
- No age: HIGH (3 ages tested)
- Structure: HIGH (2 tiers, additive components)
- Base prices: LOW (only 1 vehicle, 3 PLZs)
