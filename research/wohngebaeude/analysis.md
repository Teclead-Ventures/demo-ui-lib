# ERGO Wohngebaudeversicherung -- Pricing Analysis

## Summary

The ERGO Wohngebaudeversicherung calculator is hosted on an external subdomain (wohngebaeudeversicherung.ergo.de), built as an Angular SPA with product code WOHN25 (API uses WOHN24). It uses a Template C-WG pricing model: m2-based with linear formula, 2 tiers (Smart/Best), address-specific regional multipliers, construction year bands, and deductible factors.

## Key Findings vs. Our Assumptions

| Assumption | Reality | Status |
|---|---|---|
| 3 tiers (Grundschutz/Komfort/Premium) | 2 tiers (Smart/Best) | WRONG |
| Per-50k coverage | Per-m2 (Wohnflaeche) with linear formula | WRONG |
| Flat age curve | No age field at all - construction year matters instead | WRONG |
| Building type: Massiv/Fertighaus/Holz | Not asked - uses roof type, floors, basement instead | WRONG |
| Coverage 100k-1M step 50k | 60-180 m2 Wohnflaeche (>180 requires advisor) | WRONG |
| Risk class by building type | Address-specific (ZIP+street+house#) + construction year | WRONG |
| Loading 22% | Unknown, cannot determine from external prices | N/A |

ALL assumptions were wrong. This is a completely different model.

## Pricing Model

### Formula

price = (4.854 * sqm + 87.93) * region_factor * year_factor * sb_factor * tier_factor

Where the base formula gives the Smart tier price with 500 EUR SB for Muenchen, year 2000.

### Tier Factors

| Tier | Factor | Notes |
|------|--------|-------|
| Smart | 1.0000 | Base tier |
| Best | 1.0953 | Constant ~9.5% uplift across all parameters |

The tier ratio is remarkably constant (std = 0.000019) - pure multiplicative factor.

### Deductible (Selbstbeteiligung) Factors

| Deductible | Factor | Discount |
|-----------|--------|----------|
| ohne (0 EUR) | 1.000 | 0% |
| 500 EUR | 0.850 | 15% |
| 1.000 EUR | 0.800 | 20% |

Default is 500 EUR.

### m2 Pricing

Linear relationship: price = 4.854 * sqm + 87.93 (Smart, 500 EUR SB, Muenchen, year 2000)
- R2 = 0.997 (linear), 0.9999 (quadratic)
- Valid range: 60-180 m2 (>180 requires ERGO Berater)
- Slight concavity suggests minor quadratic component

### Regional Factors (address-specific)

| Location | Factor |
|----------|--------|
| Berlin (10117) | 0.875 |
| Trier (54290) | 0.996 |
| Muenchen (80331) | 1.000 |
| Koeln (50667) | 1.170 |

Pricing is truly address-specific (down to street + house number), likely using ZUERS flood risk zones.

### Construction Year Factors

| Year | Factor |
|------|--------|
| 1960 | 1.068 |
| 1980 | 1.068 |
| 2000 | 1.000 |
| 2010 | 0.830 |
| 2020 | 0.660 |

1960 and 1980 produce IDENTICAL prices - pre-2000 band grouping. Newer buildings dramatically cheaper (~34% less for 2020 vs 2000).

## Structure Details

### Wizard Steps
1. Building type (EFH/ZFH/MFH) + self-occupied + construction year
2. Address (PLZ + city + street + house number)
3. Building details (roof, floors, basement, m2)
4. Additional details (fireplace, garage, start date)
5. Pricing page with tier selection + add-ons

### Coverage Options
- Core perils: Feuer, Leitungswasser (always included)
- Toggleable: Sturm/Hagel, Elementargefahren
- Add-ons: Leitungswasser Plus, Allgemeine Haustechnik, Heizungs-/Energietechnik
- Not available online: Glasversicherung, Haus-/Wohnungsschutzbrief (requires Berater)

### Building Configuration Fields
- Roof: Ausgebautes Dach, Nicht ausgebautes Dach, Flachdach
- Upper floors: 0-3
- Basement: >50% basement, <50% basement, no basement
- Garage: 0-4 spaces
- Fireplace >5000 EUR: Ja/Nein

## Template Classification

Template C-WG (Wohngebaeude variant of Template C)

Similar to Hausrat (Template C) in using m2-based pricing, 2 tiers, and address-specific regional multipliers. Different in using construction year (not customer age), building characteristics, and a linear formula with intercept (not pure per-m2).

## Confidence

- Tier ratio: Very high (14 data points, std < 0.001%)
- SB factors: High (3 data points, exact match)
- m2 relationship: High (5 data points, R2 = 0.997)
- Regional factors: Medium (only 4 locations, Berlin partially failed)
- Year factors: Medium-High (5 data points, clear pattern)
- Building config factors: Not tested (roof, floors, basement variations not collected due to API instability)
- Add-on pricing: Not tested

## Data Collection

- 15 data points collected
- 1 partially failed (Berlin Best price - API 502)
- API intermittently unavailable during collection
- All prices captured with SB=500 EUR (default) unless specifically testing SB variation
- All prices are annual (jaehrlich)
