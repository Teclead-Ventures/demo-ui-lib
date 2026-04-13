# ERGO Privathaftpflichtversicherung — Calculator Structure

## Calculator URL
https://www.ergo.de/de/Produkte/Haftpflichtversicherung/Privathaftpflichtversicherung/abschluss

## Calculator Type
Multi-step wizard (3 intake steps) → single configurator page with live price updates

## Brand
ERGO (not subsidiary)

## Wizard Steps

### Step 1: Lebenssituation (#/marital-status)
- Field: "Wählen Sie Ihre Lebenssituation aus"
- Type: Radio tile group
- Options: Single, Alleinerziehend, Paar, Familie
- Default: None (must select)

### Step 2: Versicherungsbeginn (#/insurance-start)
- Field: "Wann soll die Versicherung beginnen?"
- Type: Radio group
- Options: Morgen (tomorrow), Nächsten Monat (first of next month), Anderes Datum
- Default: Morgen

### Step 3: Geburtsdatum (#/birthdate)
- Field: "Geben Sie Ihr Geburtsdatum ein"
- Type: Three spinbuttons (Tag, Monat, Jahr)
- Note: "Wenn Sie bei Versicherungsbeginn jünger sind als 36 Jahre, erhalten Sie einen Startbonus von 13%."

### Step 4: Contribution/Configurator (#/contribution)
- This is the main configuration and pricing page
- Price updates live as options change

#### Tier Selection
- Type: Radio group
- Options: Smart (10 Mio. EUR Versicherungssumme), Best (50 Mio. EUR Versicherungssumme)
- Default: Best
- Coverage is FIXED by tier — no coverage slider

#### Wählbare Leistungsbausteine (Toggleable Modules)
All are checkboxes. For Best, first 3 are checked by default; for Smart, all unchecked.

1. **Schlüsselverlust** — Best: included, Smart: optional
2. **Neuwertentschädigung** — Best: included, Smart: optional
3. **Forderungsausfall** — Best: included, Smart: optional
4. **Amts- und Diensthaftpflicht** — optional for both tiers
5. **Alleinstehende Familienangehörige** — optional for both (free add-on, 0 EUR)

#### Selbstbeteiligung (Deductible)
- Type: Dropdown
- Options: ohne Selbstbeteiligung, 150 EUR Selbstbeteiligung
- Default: ohne

#### Vertragslaufzeit (Contract Duration)
- Type: Dropdown
- Options: 1 Jahr, 3 Jahre
- Default: 3 Jahre

#### Zahlungsweise (Payment Frequency)
- Type: Dropdown
- Options: monatlich, vierteljährlich, halbjährlich, jährlich
- Default: monatlich

## Discovery Answers

1. **How many tiers?** 2 (Smart and Best) — NOT 3 as assumed
2. **Tiers of one product?** Yes, same product with two tier levels
3. **Coverage slider?** No — coverage is fixed by tier (Smart=10M, Best=50M)
4. **Coverage unit?** EUR (Versicherungssumme)
5. **Toggleable Bausteine?** Yes — 5 modules, additive pricing
6. **Age input?** Yes, but no continuous age curve. Binary: <36 gets 13% Startbonus, >=36 flat rate
7. **Brand?** ERGO (direct)

## Beitragstabelle
None found on product page (as expected for non-health products).
