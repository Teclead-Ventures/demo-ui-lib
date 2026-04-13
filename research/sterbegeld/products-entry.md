### Sterbegeldversicherung

| Parameter | Value |
|-----------|-------|
| **ID** | sterbegeld |
| **Category** | person |
| **Age range** | 40-85 |
| **Coverage** | 1.000-20.000 EUR, step 500 EUR, default 7.000 EUR |
| **Coverage unit** | per 1.000 EUR |
| **Risk class** | None (age only) |
| **Payment duration** | 90 - age (min 5, max 46 years) |
| **Tiers** | Grundschutz, Komfort (default), Premium |

**Base rates** (per 1k/month at 8k reference coverage):

| Age | Grundschutz | Komfort | Premium |
|-----|-------------|---------|---------|
| 40 | 3.12 | 3.19 | 3.65 |
| 45 | 3.44 | 3.51 | 4.01 |
| 50 | 3.90 | 3.99 | 4.56 |
| 55 | 4.49 | 4.62 | 5.29 |
| 60 | 5.27 | 5.45 | 6.24 |
| 65 | 6.34 | 6.60 | 7.56 |
| 70 | 7.94 | 8.36 | 9.58 |
| 75 | 10.59 | 11.40 | 13.09 |
| 80 | 15.36 | 16.99 | 19.49 |
| 85 | N/A | 29.04 | 33.08 |

**Age curve** (cubic, t = (age - 40) / 45):

For Komfort: rate_per_1k = 2.40 + 21.28*t - 67.20*t^2 + 71.56*t^3 (R^2 = 0.990)

**Tier multipliers** (relative to Grundschutz, age-dependent):
- Komfort: 1.02 (age 40) to 1.11 (age 80)
- Premium: 1.17 (age 40) to 1.27 (age 80)

**Coverage scaling**: Linear with small fixed fee (~1.80 EUR/month)
- price = rate_per_1k * (coverage/1000) + 1.80

**Payment mode discounts**:
- Monthly: 0%
- Quarterly: 0.4%
- Semi-annual: 1.0%
- Annual: 3.4%

**Loading**: Built into rates (no separate loading factor needed)

**Calibration**: 44yo, 8k, Komfort = 27.45 EUR/month

#### Source

- **Calculator URL**: https://www.ergo.de/de/Produkte/Sterbegeldversicherungen/Sterbegeldversicherung/abschluss
- **Data collected**: 2026-04-13
- **Data points**: 160
- **Method**: Automated wizard navigation with Playwright
- **Ages sampled**: 40, 44, 45, 50, 55, 60, 65, 70, 75, 80, 85
- **Coverages sampled**: 3k, 5k, 8k, 10k, 15k EUR
- **Confidence**: HIGH (R^2 = 0.99 with cubic fit)
