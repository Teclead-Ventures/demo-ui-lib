# Kfz-Versicherung -- Updated Products Entry

## Product: kfz

| Parameter | Value |
|-----------|-------|
| **ID** | kfz |
| **Category** | motor |
| **Age range** | 18+ (age does NOT affect pricing) |
| **Coverage** | Haftpflicht (mandatory), Teilkasko, Vollkasko |
| **Coverage unit** | N/A (vehicle-specific, not user-selectable amount) |
| **Risk class** | SF-Klasse (0-50+) for both HP and VK separately |
| **Payment duration** | 1 year renewable |

### Tiers (2 only, not 3)

| ERGO Name | Our Mapping | Key Difference |
|-----------|-------------|----------------|
| Smart | Grundschutz | Staerkere Rueckstufung (harsher claim downgrade) |
| Best | Premium | Normale Rueckstufung + Ersatzfahrzeug Plus + Schutzbrief + Wertschutz 36 |

Note: There is no middle tier. Map Smart -> Grundschutz and Best -> Premium.

### Coverage Types (act as primary product selector)

| Coverage | HP | TK | VK |
|----------|----|----|-----|
| Haftpflicht ohne Kasko | Yes | No | No |
| Haftpflicht & Teilkasko | Yes | Yes | No |
| Haftpflicht & Vollkasko | Yes | No | Yes |

### Base Rates (VW Golf VIII, Muenchen, 12k km, SB VK500/TK150, monthly at 100% SF)

| Component | Smart | Best |
|-----------|-------|------|
| HP base | 82.48 | 91.85 |
| VK base | 156.82 | 208.15 |
| TK (at SF 10) | 24.50 | 34.87 |
| Tier addon | 0 | 1.73 |

### Pricing Formula

    monthlyPremium = hp_base * hp_sf_pct/100 + vk_base * vk_sf_pct/100 + tier_addon

Where:
- hp_sf_pct: Haftpflicht SF lookup table (SF 0 = 86%, SF 10 = 33%, SF 50+ = 15%)
- vk_sf_pct: Vollkasko SF lookup table (SF 0 = 54%, SF 10 = 33%, SF 50+ = 15%)
- tier_addon: 0 (Smart) or ~1.73 EUR/month (Best)
- Teilkasko has no SF-Klasse (fixed rate per vehicle/region)

### Age Curve

NONE. Pricing is flat regardless of age.
Set: base=1.0, linear=0.0, quadratic=0.0

### SF Lookup Tables

#### Haftpflicht SF (percentage applied to HP base)
SF 0=86, 0.5=66, 1=53, 2=50, 3=47, 4=44, 5=42, 6=40, 7=38, 8=36, 9=35,
10=33, 11=32, 12=31, 13=30, 14=29, 15=28, 16=27, 17=26, 18=26, 19=25,
20=24, 21=24, 22=23, 23=23, 24=22, 25=22, 26=21, 27=21, 28=21, 29=20,
30=20, 31=19, 32=19, 33=19, 34=18, 35=18, 36=18, 37=18, 38=17, 39=17,
40=17, 41=17, 42=16, 43=16, 44=16, 45=16, 46=16, 47=16, 48=15, 49=15, 50+=15

#### Vollkasko SF (percentage applied to VK base)
SF 0=54, 0.5=49, 1=44, 2=42, 3=41, 4=39, 5=38, 6=37, 7=36, 8=34, 9=33,
10=33, 11=32, 12=31, 13=30, 14=29, 15=28, 16=28, 17=27, 18=27, 19=26,
20=25, 21=25, 22=24, 23=24, 24=23, 25=23, 26=23, 27=22, 28=22, 29=21,
30=21, 31=21, 32=20, 33=20, 34=20, 35=19, 36=19, 37=19, 38=19, 39=18,
40=18, 41=18, 42=18, 43=17, 44=17, 45=17, 46=17, 47=16, 48=16, 49=16, 50+=15

### Key Differences from Current Model

1. NO age-based pricing (our model has U-curve with base=1.80, linear=-1.20, quadratic=0.50)
2. Only TWO tiers (Smart, Best) instead of THREE (Grundschutz, Komfort, Premium)
3. NOT flat per month -- price depends heavily on SF-Klasse (factor 5.7x between SF 0 and SF 50+)
4. ADDITIVE structure (HP + VK components, not multiplicative tiers)
5. SF lookup table (not a polynomial curve)
6. Separate SF tables for Haftpflicht and Vollkasko
7. Coverage type (HP only / TK / VK) is the primary coverage selector
8. Vehicle-specific pricing via HSN/TSN (determines Typklasse)
9. Region via PLZ determines Regionalklasse
10. Mileage is a significant price driver
11. Our assumed prices (28.77/35.08/43.15 monthly) are wrong for any SF level

### Recommended Template

Template E (Kfz-specific, new) -- does not fit existing Templates A/B/C/D.

### Source

- Calculator: https://www.ergo.de/de/Produkte/KFZ-Versicherung/Autoversicherung/abschluss
- Confidence: MEDIUM-HIGH
- Vehicle tested: VW Golf VIII 1.5 TSI OPF (0603/CKM)
- PLZs tested: 80331 (Muenchen), 50667 (Koeln), 10117 (Berlin)
- 28 data points collected, SF model verified exactly
- Discrepancies: 5 VK data points affected by add-on checkbox state during collection
