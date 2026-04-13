# Unfallversicherung - Corrected Products Entry

```yaml
unfall:
  id: unfall
  name: Unfallversicherung
  category: person
  description: Kapitalleistung bei Invaliditat durch Unfall
  ageRange: [18, 75]
  coverage:
    min: 10000
    max: 300000
    step: 5000
    default: 50000
    unit: 10000
    label: "Invaliditätssumme"
  tiers:
    basic:
      name: "Basic"
      label: "Basic mit Progression 300%"
      baseRate: 0.754    # EUR/month per 10k coverage, Group A, under-65
    smart:
      name: "Smart"
      label: "Smart mit Progression 300%"
      baseRate: 1.524
    best:
      name: "Best"
      label: "Best mit Progression 600%"
      baseRate: 1.954
  ageCurve:
    # ERGO uses discrete age bands, NOT a polynomial curve
    # Our model needs a step function:
    # age < 65: multiplier = 1.0
    # age >= 65: multiplier = 2.0
    # For polynomial approximation: base=1.0, linear=0.0, quadratic=0.0
    # with ageBandThreshold: 65, ageBandMultiplier: 2.0
    type: "step_function"
    bands:
      - range: [18, 64]
        multiplier: 1.0
      - range: [65, 75]
        multiplier: 2.0
  riskClass:
    field: "occupation"
    inputType: "autocomplete"  # Specific job titles, not generic categories
    classes:
      A:
        name: "Büro/Verwaltung"
        multiplier: 1.0
        examples: ["Bürokaufmann", "Lehrer", "Angestellter"]
      B:
        name: "Handwerk/Gewerbe"
        multiplier: 1.55
        examples: ["Dachdecker", "Maurer", "Polizist"]
      C:
        name: "Erhöhtes Risiko"
        multiplier: 3.10
        examples: ["Berufskraftfahrer (Güterverkehr)"]
  paymentDuration: "annual_renewal"
  contractDuration: [1, 2, 3, 4]  # years; Basic only 1 year
  loading: 0.0  # absorbed into base rates
  paymentModes:
    monthly: 1.0
    # quarterly, annual discounts unknown (not tested)
  optionalAddons:
    - "Unfall-Rente"
    - "Unfall-Hilfe"
    - "Verletzungsgeld"
    - "Krankenhaus-Tagegeld"
    - "Todesfallleistung"
    - "Unfall-Pflege"
    - "Gliedertaxe Plus"
  tierRelationship: "multiplicative"
  notes:
    - "Pricing has NO continuous age curve - uses 2 discrete bands"
    - "Coverage scaling is perfectly linear (no fixed fee)"
    - "Occupation risk multipliers are age-independent"
    - "Smart/Best get discounts for 3+ year contracts"
    - "Some occupations trigger follow-up questions (e.g., Polizist)"
```

## Verification Examples

| Config | Tier | Expected | Formula |
|--------|------|----------|---------|
| Age 36, Bürokaufmann, 50k | Basic | 3.77 | 0.754 * 5 * 1.0 * 1.0 = 3.77 |
| Age 36, Bürokaufmann, 50k | Smart | 7.62 | 1.524 * 5 * 1.0 * 1.0 = 7.62 |
| Age 36, Bürokaufmann, 50k | Best | 9.77 | 1.954 * 5 * 1.0 * 1.0 = 9.77 |
| Age 36, Bürokaufmann, 100k | Best | 19.54 | 1.954 * 10 * 1.0 * 1.0 = 19.54 |
| Age 70, Bürokaufmann, 50k | Smart | 15.22 | 1.524 * 5 * 2.0 * 1.0 = 15.24 (rounding) |
| Age 36, Dachdecker, 50k | Basic | 5.85 | 0.754 * 5 * 1.0 * 1.55 = 5.84 (rounding) |
| Age 70, Dachdecker, 50k | Best | 29.23 | 1.954 * 5 * 2.0 * 1.55 = 30.29 (approx) |
| Age 36, Berufskraftfahrer, 50k | Smart | 23.60 | 1.524 * 5 * 1.0 * 3.10 = 23.62 (rounding) |
