# Hausratversicherung - Updated products.md Entry

## Product: hausrat

| Parameter | Value |
|-----------|-------|
| **ID** | hausrat |
| **Category** | property |
| **Age range** | 18-99 (binary: under-36 gets 13% Startbonus) |
| **Coverage** | Derived from m2: 650 EUR/m2, range 10-384 m2 (6,500-249,600 EUR) |
| **Coverage unit** | per m2 (NOT per 5k EUR) |
| **Risk class** | ZIP-code specific (not zone-based) |
| **Payment duration** | 1 year or 3 years (3yr = 10% discount) |

### Tiers (ERGO uses 2, not 3)

| ERGO Tier | Our Mapping | Description |
|-----------|-------------|-------------|
| Smart | grundschutz | Leistungsstarke Absicherung |
| Best | komfort | Topschutz mit vielen Extras |

Note: No "Premium" tier equivalent exists in ERGO's Hausrat product.

### Pricing Model

ERGO uses a **linear + fixed base** model (NOT purely multiplicative):

```
Smart_monthly = (0.1114 * m2 + 0.254) * regionMult * floorMult * buildingMult * ageFactor
Best_monthly  = (0.1114 * m2 + 3.642) * regionMult * floorMult * buildingMult * ageFactor
```

Where the tier difference is ADDITIVE (~3.39 EUR/month fixed), not multiplicative.

### Base Rates (Muenchen reference)

| Parameter | Smart | Best |
|-----------|-------|------|
| Rate per m2/month | 0.1114 | 0.1114 |
| Fixed base/month | 0.25 | 3.64 |

### Regional Multipliers (sampled)

| City | ZIP | Multiplier |
|------|-----|-----------|
| Trier | 54290 | 0.768 |
| Nuernberg | 90402 | 0.788 |
| Dresden | 01067 | 0.966 |
| Muenchen | 80331 | 1.000 (reference) |
| Kiel | 24103 | 1.078 |
| Koeln | 50667 | 1.312 |
| Hamburg | 20095 | 1.365 |
| Berlin | 10117 | 1.365 |

### Age Factor

| Condition | Factor |
|-----------|--------|
| Under 36 | 0.870 (13% Startbonus) |
| 36+ | 1.000 |

### Floor Factor (MFH only)

| Floor | Factor |
|-------|--------|
| Keller/Souterrain | 1.104 |
| Erdgeschoss | 1.104 |
| 1. OG+ | 1.000 |

### Building Type Factor

| Type | Factor |
|------|--------|
| Mehrfamilienhaus | 1.000 |
| Einfamilienhaus | 1.060 |

### Additional Modifiers

| Modifier | Factor |
|----------|--------|
| 1-year contract (vs 3yr) | 1.111 |
| 300 EUR deductible | 0.927 |
| Annual payment | 0.943 |

### Add-On Modules (separate pricing)

- Diebstahl 10.000 EUR (included in Best, optional in Smart)
- Haus- und Wohnungsschutzbrief (~1.71 EUR/month)
- Glasversicherung (~2.52 EUR/month for 48m2)
- Weitere Naturgefahren (~1.12 EUR/month for 48m2)
- Unbenannte Gefahren (~5.82 EUR/month)
- Fahrrad- und E-Bike-Schutz (from 1.85 EUR/month)

### Calibration Check

80m2, Muenchen (80331), MFH 2.OG, age 36+, no deductible, 3yr, monthly:
- Smart: 9.01 EUR/month
- Best: 12.40 EUR/month

Formula check (Smart): 0.1114 * 80 + 0.254 = 9.17 (actual 9.01, delta -1.7%)
Formula check (Best): 0.1114 * 80 + 3.642 = 12.55 (actual 12.40, delta -1.2%)
