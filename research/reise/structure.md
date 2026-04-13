# ERGO Reiseversicherung - Calculator Structure

## Brand & Platform
- **Brand**: ERGO Reiseversicherung (subsidiary: ERGO Reiseversicherung AG / ERV)
- **Domain**: app.ergo-reiseversicherung.de (EXTERNAL domain, not ergo.de)
- **URL**: https://app.ergo-reiseversicherung.de/ba4/landingPage.html?agency=028413000000&ba=standard

## Calculator Flow (Steps)

### Step 0: Product Selection
- "Welchen Versicherungsschutz wuenschen Sie?"
- Three product categories:
  1. **Stornokostenschutz** - Reiseruecktritt inkl. Reiseabbruch
  2. **Rundumschutz** - Reiseruecktritt inkl. Reiseabbruch, Reisekranken, Reisegepaeck
  3. **Krankenschutz** - Reisekranken only

### Step 1: Who's Traveling ("Wer verreist?")
- Four age band counters (0-9 per band):
  - Erwachsene(r) bis 40 Jahre
  - Erwachsene(r) 41 bis 64 Jahre
  - Erwachsene(r) ab 65 Jahre
  - Mitreisende(s) Kind(er) bis 25 Jahre
- Max 9 adults total
- 2 adults = Paar/Familien-Tarif
- Family = max 2 adults + children (no shared residence required)

### Step 2: Trip Cost ("Wie hoch ist Ihr Gesamtreisepreis?")
- **Only for Stornokostenschutz and Rundumschutz** (SKIPPED for Krankenschutz)
- Free text input in EUR
- Max 20,000 EUR online (higher requires phone)
- Total trip cost for ALL travelers combined

### Step 3: Destination ("In welche Region verreisen Sie?")
- Two options:
  - **Europa** inkl. Mittelmeer-Anliegerstaaten (incl. Morocco, Egypt, Canary Islands, Azores, Madeira, Spitzbergen)
  - **Welt** (worldwide)

### Step 4: Transportation ("Wie verreisen Sie?")
- **Only for Stornokostenschutz and Rundumschutz** (SKIPPED for Krankenschutz)
- Two options:
  - **Flugzeug, Schiff** (plane, ship/cruise)
  - **Auto, Zug, Sonstige** (car, train, other)

### Step 5: Travel Dates ("Wann reisen Sie?")
- Date range picker: start date + end date
- Determines trip duration

### Step 6: Booking Date ("Wann haben Sie Ihre Reise gebucht?")
- Single date picker
- Affects eligibility (30-day rule for cancellation insurance)

### Step 7: Results ("Waehlen Sie Ihre Absicherung")
- Checkbox: "Ohne Selbstbeteiligung" (without deductible) toggles between mit/ohne SB
- Shows available tariff variants:

#### For Stornokostenschutz:
- Jahres-Reiseruecktritts-Versicherung inkl. RAB (12 months min)
- Jahres-Reiseruecktritts-Versicherung Sparfuchs (24 months min) [RECOMMENDED]
- Reiseruecktritts-Versicherung (inkl. RAB) - single trip

#### For Rundumschutz:
- RundumSorglos-Schutz - single trip
- RundumSorglos-Jahresschutz (12 months min) [RECOMMENDED]

#### For Krankenschutz:
- Reisekranken-Versicherung - single trip
- Jahres-Reisekranken-Versicherung (12 months min) [RECOMMENDED]

## Key Pricing Dimensions
1. **Product category**: Storno / Rundum / Kranken
2. **Trip cost**: EUR amount (only for Storno & Rundum)
3. **Age band**: <=40 / 41-64 / 65+ / child <=25
4. **Number of travelers**: affects family/pair tariff
5. **Destination**: Europa / Welt
6. **Transportation**: Flugzeug-Schiff / Auto-Zug (only for Storno & Rundum)
7. **Trip duration**: derived from date range
8. **Deductible**: mit SB / ohne SB
9. **Contract type**: Einmal (per-trip) / Jahres (annual)

## Critical Differences from Main ERGO Calculators
- Completely different domain and UI system
- No weiter-weiter multi-page wizard like ergo.de
- No #ppzApp selector
- Cookie consent is domain-specific (comes back on each session)
- Age is band-based (not exact age input)
- Trip cost is the primary pricing driver (not personal attributes)
- Both per-trip and annual options shown on same results page
- Transportation mode is a pricing factor (unique to travel insurance)
