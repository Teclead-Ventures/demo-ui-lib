# ERGO Risikolebensversicherung - Calculator Structure

## Source URL
https://www.ergo.de/de/Produkte/Lebensversicherung/Risikolebensversicherung/abschluss

## Calculator Type
Multi-step wizard (8 steps + price display page)

## Wizard Steps

### Step 1: Versicherte Person (`#versicherte-person`)
- **Heading**: "Wen möchten Sie versichern?"
- **Field**: Radio buttons
  - "Mich selbst" (default, selected)
  - "Jemand anders"

### Step 2: Geburtsdatum (`#geburtsdatum`)
- **Heading**: "Geben Sie Ihr Geburtsdatum an"
- **Fields**: 3 spinbuttons
  - Tag (day)
  - Monat (month)
  - Jahr (year)
- **Validation**: Inline, enables "weiter" button when valid

### Step 3: Absicherungsform (`#absicherungsbedarf`)
- **Heading**: "Wählen Sie Ihre Absicherungsform aus"
- **Field**: Radio buttons with icons
  - "Familien- / Partnerabsicherung" (constant sum, default)
  - "Kredit- / Darlehensabsicherung" (linearly falling sum)

### Step 4: Versicherungssumme (`#versicherungssumme`)
- **Heading**: "Legen Sie Ihre Versicherungssumme fest"
- **Field**: Combobox + slider
  - Range: 50,000 EUR to 500,000 EUR
  - Default: 150,000 EUR
  - Step: appears to be free-form (accepts any number in range)
- **Note**: For >500,000 EUR, user must contact advisor

### Step 5: Versicherungslaufzeit (`#versicherungslaufzeit`)
- **Heading**: "Für wie lange möchten Sie Ihre Hinterbliebenen absichern?"
- **Field**: Combobox + slider
  - Range: 1 to 50 years
  - Default: 20 years
  - Step: 1 year (continuous, NOT discrete options)

### Step 6: Berufliche Situation (`#stellung-beruf`)
- **Heading**: "Geben Sie Ihre berufliche Situation an"
- **Fields**:
  1. **Beschäftigungsverhältnis** (employment type) - Dropdown:
     - Arbeiter (nicht im öff. Dienst)
     - Angestellter (nicht im öff. Dienst)
     - Beamter / öff. Dienst
     - Selbstständiger Handwerker
     - Sonstige Selbstständige / Freiberufler
     - Gesellschafter / Vorstand
     - Auszubildende(r)
     - Sonstige
     - Arbeitslos
     - Versorgungsempfänger(in)
     - Student(in)
     - Rentner(in)
  2. **Ausgeübter Beruf** (occupation) - Autocomplete combobox

### Step 7: Raucherstatus (`#raucher`)
- **Heading**: "Geben Sie an, ob Sie rauchen."
- **Field**: 3 radio buttons (NOT 2 as our model assumed!)
  1. "Nichtraucher/-in" - "noch nie oder seit mind. 10 Jahren nicht mehr geraucht"
  2. "Nichtraucher/-in" - "seit mind. 1 Jahr nicht mehr geraucht"
  3. "Raucher/-in" - "innerhalb des letzten Jahres geraucht"

### Step 8: Versicherungsbeginn (`#versicherungsbeginn`)
- **Heading**: "Wann soll Ihre Versicherung beginnen?"
- **Field**: Radio buttons (3 upcoming 1st-of-month dates)
  - e.g., 01.05.2026, 01.06.2026, 01.07.2026
- **Button**: "Jetzt berechnen" (not "weiter")

### Price Display (`#vorlaufiger-beitrag`)
- **Heading**: "Wählen Sie Ihren Versicherungsschutz"
- **Adjustable on this page**:
  - Versicherungssumme (spinbutton)
  - Laufzeit (spinbutton)
- **Tier selection**: 3 radio buttons
  - Grundschutz: base price
  - Komfort: mid-tier (selected by default)
  - Premium: with "mit Waisenschutz" label
- **Additional options** (checkboxes):
  - Sofortleistung Dread Disease (critical illness benefit)
  - Sicherheit Plus (guaranteed level premiums)
  - Beitragsdynamik (dynamic 3% annual increase)
- **Zahlweise** (payment frequency) dropdown:
  - monatlich (monthly)
  - vierteljährlich (quarterly)
  - halbjährlich (semi-annual)
  - jährlich (annual)
- **Actions**: "Weiter" (proceed to application), "Angebot anfordern" (request quote), "zurück"

## Total Fields Summary
- 8 input fields across wizard
- 5 adjustable fields on price display
- 3 optional add-ons (checkboxes)

## Fields NOT in our current model
- **Beschäftigungsverhältnis** (employment type)
- **Ausgeübter Beruf** (occupation) - affects risk assessment
- **Absicherungsform** (constant vs. falling sum)
- **Third smoker class** (Nichtraucher 1+ year)
- **Dread Disease add-on**
- **Sicherheit Plus add-on**
- **Beitragsdynamik add-on**
- **Versicherungsbeginn** (start date)
