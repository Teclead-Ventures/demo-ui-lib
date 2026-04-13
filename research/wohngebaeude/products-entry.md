# Wohngebaudeversicherung products.md Entry

## Recommended Entry

```yaml
wohngebaeude:
  name: "Wohngebaudeversicherung"
  template: "C-WG"
  brand: "ERGO"
  calculator_url: "https://wohngebaeudeversicherung.ergo.de?intcid=9000961"
  
  tiers:
    - id: "smart"
      name: "Smart"
      factor: 1.0000
    - id: "best"
      name: "Best"
      factor: 1.0953
  
  pricing:
    model: "linear_sqm"
    formula: "(slope * sqm + intercept) * region * year * sb * tier"
    slope: 4.854          # EUR per m2 per year (Smart, SB=500, Muenchen, year 2000)
    intercept: 87.93      # EUR base charge per year
    unit: "m2"
    min: 60
    max: 180
    step: 1
    default: 120
  
  deductible:
    options: [0, 500, 1000]
    default: 500
    factors:
      0: 1.000
      500: 0.850
      1000: 0.800
  
  construction_year:
    type: "band"
    factors:
      "pre_2000": 1.068
      "2000": 1.000
      "2010": 0.830
      "2020": 0.660
    default: 2000
    note: "1960 and 1980 give identical prices. Discrete bands, not continuous."
  
  regional:
    type: "address_specific"
    sample_factors:
      "10117": 0.875   # Berlin
      "54290": 0.996   # Trier
      "80331": 1.000   # Muenchen (reference)
      "50667": 1.170   # Koeln
    default: 1.000
    note: "True address-specific pricing (PLZ + street + house number). ZUERS zones."
  
  age_curve:
    type: "none"
    note: "No customer age field in calculator. Construction year replaces age."
  
  building_config:
    house_type:
      options: ["Einfamilienhaus", "Zweifamilienhaus", "Mehrfamilienhaus"]
      default: "Einfamilienhaus"
    roof:
      options: ["Ausgebautes Dach", "Nicht ausgebautes Dach", "Flachdach"]
      default: "Ausgebautes Dach"
    floors:
      options: [0, 1, 2, 3]
      default: 1
    basement:
      options: ["mehr als die Haelfte unterkellert", "weniger als die Haelfte unterkellert", "kein Keller"]
      default: "mehr als die Haelfte unterkellert"
    garage:
      options: [0, 1, 2, 3, 4]
      default: 1
    fireplace_over_5000:
      options: [true, false]
      default: false
    note: "Building config factors NOT yet measured. Only m2 measured so far."
  
  perils:
    included: ["Feuer", "Leitungswasser"]
    toggleable: ["Sturm und Hagel", "Elementargefahren"]
    addons: ["Leitungswasser Plus", "Allgemeine Haustechnik", "Heizungs- und Energietechnik"]
  
  payment:
    options: ["monatlich", "jaehrlich"]
    default: "jaehrlich"
  
  contract:
    duration: "3 Jahre"
    note: "Stated in calculator assumptions"
  
  loading: null  # Cannot determine from external prices

  source:
    date: "2026-04-13"
    data_points: 15
    confidence: "medium-high"
    discrepancies:
      - "ALL original assumptions were wrong (tiers, pricing model, age curve, building type)"
      - "Building config factors (roof, floors, basement) not measured due to API instability"
      - "Only 4 regional data points collected"
      - "Berlin Best price failed (API 502) - estimated from tier ratio"
      - "Construction year bands not fully mapped (only 5 years tested)"
      - "Add-on/peril toggle pricing not measured"
      - "API was intermittently returning 502 errors during collection"
```

## Key Differences from Current products.md

1. Template: Not "A" or "C" but "C-WG" (new variant)
2. Tiers: 2 (Smart/Best), not 3 (Grundschutz/Komfort/Premium)
3. Pricing unit: m2 Wohnflaeche, not EUR coverage value
4. No age curve at all - replaced by construction year
5. No Massiv/Fertighaus/Holz building type - uses roof/floors/basement instead
6. Address-specific regional pricing (ZUERS zones)
7. Deductible options: 0/500/1000 EUR (not part of original assumptions)
