# ERGO Hausratversicherung - Calculator Structure

## URL
https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Hausratversicherung/abschluss

## Calculator Type
Multi-step wizard (7 steps to reach price display)

## Tiers
- **Smart** - Leistungsstarke Absicherung (base tier)
- **Best** - Topschutz mit vielen Extras (premium tier, "Bestseller")

Note: Only 2 tiers, NOT the 3-tier model we assumed (Grundschutz/Komfort/Premium)

## Wizard Steps

### Step 1: Wie wohnen Sie? (Building type)
- URL hash: `#/living-place-type`
- Type: Radio button (2 options)
- Options:
  1. Wohnung in einem Mehrfamilienhaus (apartment in multi-family house)
  2. In einem Einfamilienhaus (single-family house)
- Default: None (must select)

### Step 2: In welchem Stockwerk liegt der Eingang zu Ihrer Wohnung? (Floor)
- URL hash: `#/home-location`
- Type: Radio button (5 options, MFH only)
- Options:
  1. Keller bzw. Souterrain
  2. Erdgeschoss bzw. Hochparterre
  3. 1. Obergeschoss
  4. 2. Obergeschoss
  5. 3. Obergeschoss oder darüber
- Default: None (must select)
- Note: This step is SKIPPED for Einfamilienhaus

### Step 3: Wie groß ist Ihre Wohnung? (Living space)
- URL hash: `#/home-square-meters`
- Type: Numeric text input
- Range: 10 to 384 qm
- Unit: Quadratmeter (m²)
- Note: Coverage is auto-calculated as 650 EUR × m²

### Step 4: Wo wohnen Sie? (Address)
- URL hash: `#/address`
- Fields:
  - Straße (Street) - text input, validated against database
  - Hausnummer (House number) - text input
  - Postleitzahl (ZIP code) - text input
  - Wohnort (City) - auto-populated from ZIP
- Note: Street names MUST be valid German street names (with umlauts)

### Step 5: Wann soll Ihre Versicherung beginnen? (Start date)
- URL hash: `#/insurance-start-date`
- Type: Radio button (3 options)
- Options:
  1. Morgen (Tomorrow) - pre-selected
  2. Nächsten Monat (Next month)
  3. Anderes Datum (Custom date)

### Step 6: Geben Sie Ihr Geburtsdatum ein. (Birth date)
- URL hash: `#/birth-date`
- Type: 3 spin buttons (Tag, Monat, Jahr)
- Note: Under 36 at insurance start → 13% Startbonus discount

### Step 7: Wählen Sie Ihren Versicherungsschutz. (Coverage selection)
- URL hash: `#/insurance-coverage`
- Type: Tabbed configurator

**Tier selection:**
- Tab: Smart / Best
- Default varies by configuration (usually Best)

**Included features (Best):**
- Grobe Fahrlässigkeit 100% (no deduction up to coverage sum)
- Einfacher Diebstahl inklusive (up to 10,000 EUR)

**Add-on modules (checkboxes):**
1. Diebstahl 10.000 EUR (Smart: optional, Best: included)
2. Haus- und Wohnungsschutzbrief
3. Glasversicherung
4. Weitere Naturgefahren (Elementar)
5. Unbenannte Gefahren (requires Weitere Naturgefahren)
6. Fahrrad- und E-Bike-Schutz (separate section)

**Dropdowns:**
- Selbstbeteiligung: 300 EUR (Flexi-SB) / 300 EUR / Keine Selbstbeteiligung
- Zahlungsweise: jährlich / halbjährlich / vierteljährlich / monatlich
- Vertragslaufzeit: 1 Jahr / 3 Jahre

**Coverage display:**
- Shows calculated Versicherungssumme (e.g., "52.000,00 EUR" for 80m²)
- Price shown in header throughout wizard (updates with each step)

## Key Differences from Our Model

1. **2 tiers, not 3** - Smart and Best, not Grundschutz/Komfort/Premium
2. **Coverage from m², not user-entered** - 650 EUR/m², range 10-384 m²
3. **ZIP-specific pricing**, not 4 zone model
4. **Floor affects price** - Keller/EG ~10% surcharge
5. **Building type affects price** - EFH ~6% surcharge vs MFH
6. **Age binary discount** - 13% off for under-36, not flat
7. **Add-on modules** are separate pricing (not base tier features)
8. **Contract duration** - 3-year default with 10% discount vs 1-year
9. **Deductible options** - 300 EUR options reduce premium ~7%
