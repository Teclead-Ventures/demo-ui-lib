# Reiseversicherung (reise) - Products Entry

## Corrected products.md entry

```yaml
reise:
  name: Reiseversicherung
  brand: ERGO Reiseversicherung (ERV)
  calculator_url: https://app.ergo-reiseversicherung.de/ba4/landingPage.html?agency=028413000000&ba=standard
  external_domain: true  # NOT on ergo.de
  
  # This product is fundamentally different from all other ERGO products.
  # It has 3 product categories, each with single-trip and annual variants.
  # The pricing model is trip-cost-based, not person-based.
  
  template: travel_insurance  # NEW template - does not fit existing templates
  
  products:
    stornokostenschutz:
      name: Stornokostenschutz
      description: Reiseruecktritt inkl. Reiseabbruch
      
      einmal:  # Single trip
        pricing_model: percentage_of_trip_cost
        rate_mit_sb: 0.05  # 5% of trip cost
        rate_ohne_sb: 0.06  # 6% of trip cost
        transport_discount_auto: 0.92  # Auto = 92% of Flug price
        age_independent: true
        per_booking: true  # Not per person
        
      jahres:  # Annual
        pricing_model: sqrt_fit
        formula: "price = -91 + 3.79 * sqrt(trip_cost)"
        sparfuchs_ratio: 0.90  # Sparfuchs = 90% of Jahres
        ohne_sb_ratio: 1.19
        age_multipliers:
          u40: 1.00
          m41_64: 1.10
          o65: 2.09
        group_multipliers:
          single: 1.00
          pair_family: 1.12
        region_independent: true
        transport_independent: true
    
    rundumschutz:
      name: Rundumschutz
      description: Storno + Reiseabbruch + Reisekranken + Reisegepaeck
      # Bundle product - priced as package, not sum of parts
      # Reference prices (1 adult <=40, EUR 5000, Europa, Flug):
      #   Einmal msb: 450, osb: 650
      #   Jahres msb: 184, osb: 201
    
    krankenschutz:
      name: Krankenschutz
      description: Reisekranken only
      
      einmal:
        base_prices_europa_msb:  # Per-trip, 7 days
          u40: 12.80
          m41_64: 16.00
          o65: 34.40
        base_prices_europa_osb:
          u40: 17.60
          m41_64: 19.20
          o65: 57.60
        region_multiplier_welt_msb: 1.125
        region_multiplier_welt_osb: 2.05
      
      jahres:
        prices_msb:  # Region-independent
          u40: 31
          m41_64: 39
          o65: 105
        prices_osb:
          u40: 49
          m41_64: 59
          o65: 155
        region_independent: true
  
  input_fields:
    - product_category: [stornokostenschutz, rundumschutz, krankenschutz]
    - travelers:
        age_bands: [u40, m41_64, o65, kids_u25]
        max_adults: 9
        pair_threshold: 2  # 2 adults = pair tariff
    - trip_cost:  # Only for storno and rundum
        min: 1
        max: 20000
        unit: EUR
    - region: [europa, welt]
    - transport: [flugzeug_schiff, auto_zug]  # Only for storno and rundum
    - travel_dates: date_range
    - booking_date: single_date
    - deductible: [mit_sb, ohne_sb]
  
  output:
    - multiple tariff options shown simultaneously
    - both single-trip and annual on same page
    - checkbox to toggle deductible
```

## Key Implementation Notes

1. This is a COMPLETELY DIFFERENT system from the main ERGO calculators
2. No #ppzApp selector, no weiter-weiter wizard
3. Custom ERV domain with its own cookie consent
4. Age is band-based (not exact), only 3 adult bands + children
5. Trip cost is the primary pricing driver for Storno
6. Single trip pricing is trivially simple: 5% of trip cost
7. Annual pricing follows sqrt curve with age/group multipliers
8. Region only matters for Krankenschutz single trip
