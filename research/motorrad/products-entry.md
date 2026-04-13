# Motorradversicherung -- Products Entry

## Product: motorrad

| Parameter | Value |
|-----------|-------|
| **ID** | motorrad |
| **Category** | motor |
| **Age range** | 18+ (age AFFECTS pricing, U-shaped curve) |
| **Coverage** | Haftpflicht (mandatory), Teilkasko, Vollkasko |
| **Coverage unit** | N/A (vehicle-specific, not user-selectable amount) |
| **Risk class** | SF-Klasse (0-20+) for both HP and VK separately |
| **Payment duration** | 1 year renewable |

### Tiers (2 only)

| ERGO Name | Our Mapping | Key Difference |
|-----------|-------------|----------------|
| Smart | Grundschutz | Staerkere Rueckstufung (harsher claim downgrade) |
| Best | Premium | Normale Rueckstufung + Ersatzfahrzeug Plus + Schutzbrief + Motorradbekleidung Plus |

### Coverage Types

| Coverage | HP | TK | VK |
|----------|----|----|-----|
| Haftpflicht ohne Kasko | Yes | No | No |
| Haftpflicht & Teilkasko | Yes | Yes | No |
| Haftpflicht & Vollkasko | Yes | No | Yes |

### Base Rates (Honda CBF 500, Muenchen, 6k km, SB VK150/TK150, monthly at 100% SF, age 36)

| Component | Smart | Best |
|-----------|-------|------|
| HP base | 22.16 | 26.99 |
| VK base | 78.49 | 106.45 |
| TK (flat) | 7.09 | 11.23 |
| Tier addon | 0 | 1.30 |

### Pricing Formula

    monthlyPremium = hp_base * age_factor(age) * hp_sf_pct/100
                   + vk_base * age_factor(age) * vk_sf_pct/100  (if VK)
                   + tk_flat                                      (if TK)
                   + tier_addon                                   (if Best)

### Age Curve

U-shaped quadratic: factor(age) = 2.566 - 0.0698*age + 0.000750*age^2
- Minimum at age ~47
- Set: base=2.566, linear=-0.0698, quadratic=0.000750

Age factor examples:
- Age 26: 1.26
- Age 36: 1.03
- Age 46: 0.94
- Age 66: 1.23

### SF Lookup Tables (22 levels each)

#### Haftpflicht SF
SF 0=100, 0.5=74, 1=54, 2=48, 3=44, 4=40, 5=38, 6=36, 7=34, 8=32,
9=31, 10=30, 11=29, 12=28, 13=28, 14=27, 15=27, 16=26, 17=26, 18=25,
19=25, 20+=24

#### Vollkasko SF
SF 0=100, 0.5=76, 1=55, 2=49, 3=46, 4=43, 5=40, 6=38, 7=36, 8=35,
9=34, 10=33, 11=32, 12=31, 13=30, 14=30, 15=29, 16=28, 17=28, 18=28,
19=27, 20+=27

### Key Differences from Kfz

1. AGE CURVE EXISTS (Kfz had none) -- U-shaped, min at ~47
2. Only 22 SF levels (Kfz had 51)
3. HP SF 0 = 100% (Kfz was 86%)
4. HP SF 20+ = 24% (Kfz had SF 50+ = 15%)
5. Motorcycle-specific: Motorradbekleidung Plus add-on
6. Saisonkennzeichen option (seasonal plates)
7. Vehicle value check (under 30k EUR)
8. Wizard has ~13 steps vs Kfz's ~5

### Recommended Template

Template E-variant (extends Kfz Template E with age curve).
Must support:
- Additive HP + VK/TK components
- Separate SF lookup tables for HP and VK (22 levels, not 51)
- U-shaped age curve (quadratic)
- Flat TK rate (no SF scaling)
- 2 tiers with flat add-on

### Source

- Calculator: https://www.ergo.de/de/Produkte/KFZ-Versicherung/Motorradversicherung/abschluss
- Confidence: MEDIUM-HIGH
- Vehicle tested: Honda CBF 500 (4124/133)
- PLZ tested: 80331 (Muenchen)
- ~22 data points collected
- Age effect verified at 6 ages (26, 30, 36, 46, 55, 66)
- SF formula verified at 4 levels with zero error (HP Smart)
