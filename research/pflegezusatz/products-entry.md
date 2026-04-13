## pflegezusatz

```yaml
pflegezusatz:
  id: pflegezusatz
  name: Pflegezusatzversicherung
  brand: DKV (ERGO Group)
  category: person
  calculatorUrl: https://www.ergo.de/de/Produkte/Pflegeversicherung/Pflegezusatzversicherung/abschluss-tagegeld
  calculatorType: single-page configurator

  # NOTE: ERGO offers 3 separate products, not 3 tiers.
  # Our demo models PTG (Pflege Tagegeld) as the primary product.
  # PZU and KFP are fundamentally different (fixed-price, no age dependency).

  ageRange: [0, 99]
  # Age bands: 0-15 = flat rate, 16-19 = flat rate, 20+ = individual per year

  coverage:
    unit: EUR/Tag (EUR per day)
    min: 5
    max: 160
    step: 5
    default: 10
    linear: true  # price = rate(age) * dailyBenefit — perfectly linear

  riskClass: none

  # Template B required — exponential age curve over 80-year range
  template: B

  # Lookup table for PTG monthly premium at 1 EUR/day benefit
  # Multiply by dailyBenefit to get actual price
  ageBands:
    - { ageMin: 0, ageMax: 15, ratePerEurDay: 0.451 }
    - { ageMin: 16, ageMax: 19, ratePerEurDay: 0.462 }

  # Per-year rates for ages 20-99 (EUR/month per 1 EUR/day benefit)
  ageRates:
    20: 0.591
    21: 0.617
    22: 0.644
    23: 0.672
    24: 0.701
    25: 0.731
    26: 0.762
    27: 0.795
    28: 0.829
    29: 0.865
    30: 0.903
    31: 0.942
    32: 0.983
    33: 1.026
    34: 1.071
    35: 1.117
    36: 1.166
    37: 1.216
    38: 1.269
    39: 1.324
    40: 1.381
    41: 1.441
    42: 1.504
    43: 1.570
    44: 1.639
    45: 1.711
    46: 1.788
    47: 1.868
    48: 1.953
    49: 2.042
    50: 2.136
    51: 2.235
    52: 2.341
    53: 2.452
    54: 2.569
    55: 2.694
    56: 2.826
    57: 2.967
    58: 3.117
    59: 3.277
    60: 3.448
    61: 3.632
    62: 3.830
    63: 4.041
    64: 4.269
    65: 4.332
    66: 4.583
    67: 4.853
    68: 5.143
    69: 5.453
    70: 5.786
    71: 6.143
    72: 6.527
    73: 6.942
    74: 7.393
    75: 7.884
    76: 8.420
    77: 9.004
    78: 9.640
    79: 10.333
    80: 11.085
    81: 11.899
    82: 12.777
    83: 13.720
    84: 14.726
    85: 15.791
    86: 16.955
    87: 18.184
    88: 19.477
    89: 20.827
    90: 22.230
    91: 23.681
    92: 25.180
    93: 26.731
    94: 28.343
    95: 30.025
    96: 31.779
    97: 33.595
    98: 35.461
    99: 37.348

  # Additional fixed-price products (not modeled with age curve)
  additionalProducts:
    PZU50:
      name: Pflege-Zuschuss 50%
      fixedMonthlyPrice: 29.70
      description: 50% Aufstockung der gesetzlichen Pflegeleistungen
    PZU100:
      name: Pflege-Zuschuss 100%
      fixedMonthlyPrice: 59.40
      description: Verdopplung der gesetzlichen Pflegeleistungen
    KFP:
      name: KombiMed Foerder-Pflege
      fixedMonthlyPrice: 25.72
      description: Staatlich gefoerdert (5 EUR/Monat Zulage abgezogen), keine Gesundheitsfragen
    PSP:
      name: Pflege Schutz Paket
      description: Optional add-on with 24h Versorgungsgarantie, 1000 EUR Einmalzahlung ab PG2

  tiers: null  # No tiers — single product (PTG) with coverage amount selection
  waitingPeriod: none  # PTG has no waiting period
  paymentDuration: null  # Not specified in calculator

  notes:
    - "PTG is the 'Bestseller' and primary product"
    - "Coverage is per day (Pflegetagegeld), not per month"
    - "Perfectly linear pricing: price = ageRate * dailyBenefit"
    - "Age 65 shows anomalous low growth (1.48% vs ~5% average) — likely regulatory"
    - "Inflationsschutz: benefits increase every 3 years without new health check"
    - "Erhöhungsoption: can increase coverage on life events without health check"
    - "PZU and KFP are separate products with fixed pricing, no age dependency"
```
