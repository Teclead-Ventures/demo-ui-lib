# Krankentagegeld Pricing Analysis

## Calculator Structure

Single-page configurator (DKV pattern). Not a multi-step wizard.
Brand: ERGO product page, DKV-branded calculator (KombiMed KTAG).

## Product Structure

Single product with 2 distinct tariff tables based on employment type:
1. Arbeitnehmer (employees) — supplementing GKV Krankengeld gap
2. Selbstaendiger / Freiberufler (identical pricing, different max coverage)

No tiers (no Grundschutz/Komfort/Premium).

## Pricing Formula

Price = rate_per_eur_day(age, berufsstatus) x tagesgelhoehe x leistungsbeginn_factor(tag, berufsstatus)

- Coverage scaling: PERFECTLY LINEAR
- Age curve: Quadratic with plateau at age 67+
- Leistungsbeginn factors interact with age (not purely multiplicative, ~2-3% spread)

## Quadratic Age Curve Coefficients (rate per EUR/day)

Selbstaendiger (29.Tag): 0.000223 * age^2 + 0.00364 * age + 0.365 (MAPE=0.75%)
Arbeitnehmer (43.Tag): 0.000112 * age^2 + 0.01485 * age - 0.0138 (MAPE=2.28%)

Plateau: price stops at age 67 for both.

## Leistungsbeginn Factors

AN (normalized to 43.Tag=1.0): 43:1.00, 64:0.71, 85:0.58, 92:0.50, 106:0.44, 127:0.37, 169:0.27, 183:0.24, 274:0.12, 365:0.06
SE (normalized to 29.Tag=1.0): 4:3.43, 8:3.12, 15:1.90, 22:1.28, 29:1.00, 43:0.81, 92:0.35, 183:0.11

## Key Differences from Previous Entry

1. No tiers - single product
2. Two separate tariff tables (AN/SE), not a simple multiplier
3. Leistungsbeginn is a key pricing variable with many options
4. Coverage step is 5 EUR, not 10 EUR
5. Age range extends to 80 (birth year 1946)
6. Age plateau at 67
7. Versicherungsstatus (pflicht/freiwillig) affects max coverage only, not price
8. Single-page configurator, not wizard
