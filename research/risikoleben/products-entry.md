## Risikolebensversicherung (risikoleben)

| Parameter | Value |
|-----------|-------|
| **ID** | risikoleben |
| **Category** | person |
| **Age range** | 18-65 (wizard accepts exact birth date) |
| **Coverage** | 50.000-500.000 EUR, free-form entry with slider, default 150.000 |
| **Coverage unit** | per 1.000 EUR (near-linear with small fixed base fee) |
| **Risk class** | 3 classes: Nichtraucher 10+ (1.0), Nichtraucher 1+ (~1.17), Raucher (1.87-3.92x, age-dependent) |
| **Payment duration** | 1-50 years, continuous slider, default 20 |
| **Beruf** | Employment type + occupation (required, affects risk) |
| **Absicherungsform** | Constant sum (default) or linearly falling |

### Tiers
- **Grundschutz**: Basic death benefit + provisional cover + nachversicherung
- **Komfort**: + extended nachversicherung + temporary increase + Soforthilfe (default selection)
- **Premium**: + Waisenschutz (250 EUR/month per child) + Pflegebonus + Verlaengerungsoption

### Optional Add-ons
- Dread Disease (critical illness benefit)
- Sicherheit Plus (guaranteed level premiums)
- Beitragsdynamik (3% annual dynamic increase)

### Payment Frequency
monatlich, vierteljaehrlich, halbjaehrlich, jaehrlich

### Pricing Model: Lookup Table (NOT formula)

The age curve is too steep/exponential for a simple quadratic. Use lookup table with interpolation.

**Reference prices (200k, 20yr, Nichtraucher 10+, monthly):**

```json
{
  "grundschutz": {"25": 3.94, "30": 5.15, "35": 7.54, "40": 12.16, "45": 20.32, "50": 34.34, "55": 60.94, "60": 121.61},
  "komfort":     {"25": 4.97, "30": 6.51, "35": 9.54, "40": 15.42, "45": 25.82, "50": 43.65, "55": 77.48, "60": 154.68},
  "premium":     {"25": 7.50, "30": 9.54, "35": 13.54, "40": 21.30, "45": 35.02, "50": 58.53, "55": 103.11, "60": 204.46}
}
```

**Smoker multipliers (age-dependent, applied to NS10+ base):**
```json
{"25": 1.87, "30": 2.23, "35": 2.65, "40": 3.02, "45": 3.46, "50": 3.92, "55": 3.83, "60": 3.19}
```

**Nichtraucher 1+ multiplier:** ~1.17x (slightly age-dependent, 1.13-1.24)

**Coverage scaling:** price = fixedFee + rate * coverage
- fixedFee ~0.91 EUR, rate ~0.0000432 EUR per EUR coverage (for Komfort at 35)
- Simpler approximation: scale linearly from 200k reference, accept ~5% error

**Term scaling (relative to 20yr at age 35, Komfort):**
```json
{"10": 0.629, "15": 0.774, "20": 1.000, "25": 1.376, "30": 1.945}
```

**Tier ratios (stable across ages):**
- Komfort / Grundschutz: ~1.27x
- Premium / Grundschutz: ~1.70-1.90x (decreases with age)

### Calibration Check
- 35yo non-smoker(10+), 200k, Komfort, 20yr -> 9.54 EUR/month (our assumption was ~12 EUR, off by -20%)
- Andrea example (35, 200k, 20yr, Premium): website says 13.54, we got 13.54 - EXACT MATCH
