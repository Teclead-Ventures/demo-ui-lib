# ERGO Reiseversicherung - Pricing Analysis

## Calculator Summary

Domain: app.ergo-reiseversicherung.de (ERV subsidiary, completely separate from ergo.de)
Products: 3 product categories, each with single-trip AND annual variants
Key Dimensions: Trip cost, age band, destination, transport, deductible, travelers

## Product Structure

### Three Product Categories

1. Stornokostenschutz (Trip Cancellation + Interruption)
   - Jahres-RRV inkl. RAB (annual, 12 months min)
   - Jahres-RRV Sparfuchs (annual, 24 months min, 10% cheaper)
   - Einmal-RRV (single trip)

2. Rundumschutz (All-in-one Bundle)
   - RundumSorglos-Schutz (single trip)
   - RundumSorglos-Jahresschutz (annual, 12 months min)
   - Includes: Storno + Reiseabbruch + Reisekranken + Reisegepaeck

3. Krankenschutz (Travel Health only)
   - Reisekranken-Versicherung (single trip)
   - Jahres-Reisekranken-Versicherung (annual, 12 months min)

Each product has two deductible options: mit SB / ohne SB

## Pricing Model: Stornokostenschutz

### Single Trip (Einmal)
- Exactly 5% of trip cost (mit SB)
- Exactly 6% of trip cost (ohne SB)
- AGE-INDEPENDENT
- PER-BOOKING (not per person)
- Transport: Flug 5%, Auto 4.6%
- Region: NO effect

### Annual (Jahres)
- Best fit: price = -91 + 3.79 * sqrt(trip_cost) for base (<=40)
- Sparfuchs = 90% of Jahres
- Ohne SB = 119% of mit SB
- Age multipliers: <=40: 1.0, 41-64: 1.10, 65+: 2.09
- Pair/Family: 1.12x single
- Region: NO effect
- Transport: NO effect

## Pricing Model: Krankenschutz

### Age-based pricing (Europa, 7 days)
- <=40: Einmal 12.80 msb / 17.60 osb, Jahres 31 msb / 49 osb
- 41-64: Einmal 16.00 msb / 19.20 osb, Jahres 39 msb / 59 osb
- 65+: Einmal 34.40 msb / 57.60 osb, Jahres 105 msb / 155 osb

### Region effect (Krankenschutz only)
- Annual: NO region effect
- Single trip msb: Welt = 1.125x Europa
- Single trip osb: Welt = 2.05x Europa

## Key differences from our assumptions

Our assumptions were completely wrong on every dimension:
- No tiers (Grundschutz/Komfort/Premium) - instead 3 separate product categories
- No per-1k rate - instead 5% flat for single trip, sqrt-based for annual
- No U-shape age curve - instead 3 flat age bands with step multipliers
- Coverage is trip cost (1-20k), not 2k-30k fixed range
- Region has NO effect on cancellation insurance
- Transport mode matters (we missed this)
- Both annual AND per-trip options (we only had per-trip)
- Deductible toggle (we missed this)
