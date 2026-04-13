# Sterbegeldversicherung - Calculator Structure

## URL
https://www.ergo.de/de/Produkte/Sterbegeldversicherungen/Sterbegeldversicherung/abschluss

## Calculator Type
Multi-step wizard (4 steps) within ERGO's React SPA

## Steps

### Step 1: Tarifdaten - Geburtsdatum
- **Heading**: "Geben Sie Ihr Geburtsdatum ein"
- **Fields**:
  - Tag (spinbutton, type=number, placeholder="TT")
  - Monat (spinbutton, type=number, placeholder="MM")
  - Jahr (spinbutton, type=number, placeholder="JJJJ")
- **Validation**: "Die versicherte Person muss zwischen 40 und 85 Jahre alt sein. Das Alter berechnet sich so: Jahr des gewünschten Versicherungsbeginns (z. B. 2026) - Geburtsjahr."
- **Button**: "weiter" (disabled until valid date entered)

### Step 2: Tarifdaten - Versicherungsbeginn
- **Heading**: "Wann soll die Versicherung beginnen?"
- **Fields**:
  - Radio buttons with 3 date options (next 3 months, 1st of month)
  - Default: first available date (e.g., 01.05.2026)
- **Button**: "weiter", "Zurueck"

### Step 3: Tarifdaten - Versicherungssumme
- **Heading**: "Wie viel Geld soll fuer die Beerdigung verfuegbar sein?"
- **Fields**:
  - Slider + textbox: 1.000 EUR to 20.000 EUR
  - Default: 7.000 EUR
  - Step: 500 EUR (based on dropdown options on next page)
- **Info texts**:
  - "Diese Summe steht fuer die Bestattung zur Verfuegung."
  - "Nur bei Premium: Bei einer schweren Krankheit bekommt die versicherte Person das Geld auf Wunsch direkt."
  - "Nur bei Premium: Versicherungssummen auch ueber 15.000 EUR moeglich."
- **Button**: "weiter", "Zurueck"

### Step 4: Beitrag - Tarifauswahl (Price Display Page)
- **Heading**: "Waehlen Sie Ihren passenden Schutz"
- **Shows**: "Garantierte Versicherungssumme: X.XXX EUR"
- **Sub-info**: "bei [zahlweise] Beitragszahlung und einer Beitragszahlungsdauer von XX Jahren"

#### Tier Selection (Tabs)
- **Grundschutz** | **Komfort** (default) | **Premium**
- Each shows:
  - "Sie zahlen XX,XX EUR monatlich"
  - Garantierte Todesfallleistung: X.XXX,XX EUR
  - Gesamtleistung inkl. Ueberschussbeteiligung: X.XXX,XX EUR
  - Aufbauzeit ab Vertragsbeginn: X Monate

#### Configuration Dropdowns (on same page)
1. **Zahlweise**: monatlich, vierteljaehrlich, halbjaehrlich, jaehrlich
2. **Todesfallleistung**: 1.000 EUR to 20.000 EUR in 500 EUR steps
3. **Beitragszahlungsdauer**: 5 to (90-age) Jahre

#### Additional Info
- "Sie zahlen Beitraege bis [date]. Danach sind Sie lebenslang versichert."
- "Alle Leistungen anzeigen" button opens comparison overlay

- **Buttons**: "weiter zum Online-Antrag", "Zurueck"

## Tier Feature Comparison

| Feature | Grundschutz | Komfort | Premium |
|---------|-------------|---------|---------|
| Aufbauzeit | 36 Monate | 18 Monate | 18 Monate |
| Doppelte Leistung bei Unfalltod | - | YES | YES |
| Leistung bei Pflegebeduerftigkeit | - | - | YES |
| Vorgezogene Leistung bei schwerer Krankheit | - | - | YES |
| Flex-Option | nachtraeglich waehlbar | nachtraeglich waehlbar | nachtraeglich waehlbar |
| Beitragsdynamik | waehlbar | waehlbar | waehlbar |
| Bestattungspakete | - | - | waehlbar, bis zu 20% guenstiger |
| Vorsorge-Ordner und Beratungstelefon | - | YES | YES |
| Kostenlose Rechtsberatung | - | YES | YES |
| Best Doctors | - | - | YES |
| Telefonische Pflegeberatung | - | - | YES |
| Psychologische Betreuung fuer Angehoerige | - | - | YES |
| Rueckholung bei Tod im Ausland | - | - | YES |
| Haushaltsnahe Dienstleistungen | - | - | YES |
| Haustierbetreuung | - | - | YES |
| Digitaler Nachlass-Verwalter | - | - | YES |

## Key Observations
- No Beitragstabelle found on product page
- No risk class selection (age only)
- Payment duration default = 90 - entry_age (NOT 85 - age as assumed)
- Coverage in 500 EUR steps (not 1000 as assumed)
- Default coverage is 7000 (not 8000 as assumed)
- Grundschutz unavailable at age 85 with 5-year payment
- Prices update dynamically when changing tier/coverage/payment on step 4
