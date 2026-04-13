# ERGO Kfz-Versicherung Calculator Structure

## Calculator URL
https://www.ergo.de/de/Produkte/KFZ-Versicherung/Autoversicherung/abschluss#/neu/

## Calculator Type
Multi-step wizard (4 main steps: Tarifdaten -> Beitrag -> Persoenliches -> Abschluss)
Actual flow: neu -> fahrzeugsuche -> fahrzeughalter -> fahrzeugnutzung -> tarifdaten (price display)

## Brand
ERGO (shown in header)

## Wizard Steps

### Step 1: Ihre Angaben (#/neu/)
Fields:
1. **Bitte waehlen** (radio): "Versicherer wechseln" [default], "Fahrzeug wechseln", "Erstvertrag"
2. **Geburtsdatum** (date): Tag, Monat, Jahr
3. **Berufsgruppe** (dropdown): Sonstige (Standard) [default], Finanzdienstleister Innendienst, Finanzdienstleister Aussendienst, Beamte/Richter/Pensionaere, Beschaeftigte im oeffentlichen Dienst/Berufssoldaten, Landwirte
4. **Versicherungsbeginn** (date): Tag, Monat, Jahr
5. **Saisonkennzeichen** (radio): Ja, Nein [default]

### Step 2: Fahrzeugsuche (#/fahrzeugsuche)
Fields:
1. **Pkw suchen** (radio): "ohne Kfz-Schein" [default], "mit Kfz-Schein" (HSN/TSN direct)
2. **Hersteller** (combobox/search): All manufacturers
3. **Modell** (combobox): Dependent on Hersteller
4. **Kraftstoff** (combobox): Benzin/Super, Diesel, Sonstige (LPG, Hybrid, Elektro, ...)
5. **Fahrzeugkategorie** (combobox): e.g. Kombi, Limousine
6. **Leistung** (combobox): Specific PS/KW values

After filtering, a table shows matching vehicles with: Modell, PS/KW, Baujahr, HSN/TSN
User selects a specific vehicle variant via radio button.

### Step 3: Fahrzeughalter (#/fahrzeughalter) - "Ihr Pkw"
Fields:
1. **Fahrzeughalter** (dropdown): Versicherungsnehmer [default], (Ehe-)Partner, Kind, Sonstige
2. **Postleitzahl des Halters** (textbox) - CRITICAL: determines Regionalklasse
3. **Ort** (auto-filled from PLZ)
4. **Erstzulassung** (date): Tag, Monat, Jahr - first registration
5. **Letzte Zulassung auf den Fahrzeughalter** (date) - with "Wie Erstzulassung" checkbox
6. **Fahrer des Pkws** (checkboxes): Versicherungsnehmer [default checked], (Ehe-)Partner, Familienmitglieder, Sonstige Fahrer (ab 18 Jahren)
7. **17-jaehriger begleiteter Fahrer** (radio): Ja, Nein [default]

### Step 4: Fahrzeugnutzung (#/fahrzeugnutzung)
Fields:
1. **Maximale jaehrliche Fahrleistung** (spinbutton): in thousands km - AFFECTS PRICE
2. **Nutzung des Fahrzeugs** (radio): Ueberwiegend privat (inkl. Arbeitsweg) [default], Ueberwiegend geschaeftlich
3. **Finanzierung** (radio): Nein [default], Kredit, Leasing

Section: Uebernahme der Schadenfreiheitsklasse
4. **Situation** (radio): SF aus Vorvertrag uebernehmen, SF von anderer Person uebernehmen

Section: Haftpflicht
5. **Schadenfreiheitsklasse HP (SF)** (dropdown): SF 0 (86%) through SF 50+ (15%) - 51 levels

Section: Kasko
6. **Versicherungsschutz** (dropdown): Haftpflicht & Vollkasko, Haftpflicht & Teilkasko, Haftpflicht ohne Kasko
7. **Schadenfreiheitsklasse VK (SF)** (dropdown): SF 0 (54%) through SF 50+ (15%) - appears only for Vollkasko
8. **Bereits Fahrzeug bei ERGO?** (radio): Ja, Nein [default]

Button: "Jetzt berechnen"

### Step 5: Tarifdaten / Price Display (#/tarifdaten)
Shows:
- Summary: Regionalklasse HP, Regionalklasse VK, Beitrag amounts, SF classes
- Can change: Versicherungsschutz, Kasko SF, Selbstbeteiligung, Zahlweise
- **Zahlweise** (dropdown): jaehrlich [default], halbjaehrlich, vierteljaehrlich, monatlich

Price Table:
- 2 tiers: **Smart** and **Best**
- Smart = "Staerkere Rueckstufung" (stronger SF downgrade on claims)
- Best = "mit normaler Rueckstufung im Schadenfall" (normal SF downgrade on claims)
- Breakdown: Kfz-Haftpflicht + Vollkasko (or Teilkasko)

**Selbstbeteiligung** options (Vollkasko):
- VK ohne / TK ohne
- VK 150 / TK 150
- VK 300 / TK 150
- VK 500 / TK 150 [default]
- VK 1000 / TK 150
- VK 150 / TK ohne
- VK 300 / TK ohne
- VK 500 / TK ohne
- VK 1000 / TK ohne
- VK 500 / TK 500
- VK 1000 / TK 1000

**Waehlbare Leistungsbausteine** (optional add-ons):
- Werkstattbonus
- Ersatzfahrzeug Plus (included in Best default)
- Wertschutz 24
- Wertschutz 36 (Best only, included)
- Schutzbrief (included in Best default)
- Rabattschutz (Best only)
- Safe Drive

## Key Structural Findings

1. **NO age curve**: Birth date does NOT affect premium. Tested ages 26, 36, 66 - all identical prices.
2. **2 tiers only**: Smart and Best (not 3 like we assumed)
3. **Separate SF tables**: Haftpflicht and Vollkasko have different SF percentage tables
4. **Regionalklasse**: PLZ determines Regionalklasse separately for HP and VK
5. **Mileage**: Annual mileage significantly affects price
6. **Vehicle-specific pricing**: HSN/TSN determines base rate (Typklasse)
7. **Price = HP component + Kasko component** (each independently SF-scaled)

## SF Percentage Tables

### Haftpflicht SF
| SF | % |
|----|---|
| 0 | 86 |
| 1/2 | 66 |
| 1 | 53 |
| 2 | 50 |
| 3 | 47 |
| 4 | 44 |
| 5 | 42 |
| 6 | 40 |
| 7 | 38 |
| 8 | 36 |
| 9 | 35 |
| 10 | 33 |
| 11 | 32 |
| 12 | 31 |
| 13 | 30 |
| 14 | 29 |
| 15 | 28 |
| 16 | 27 |
| 17 | 26 |
| 18 | 26 |
| 19 | 25 |
| 20 | 24 |
| 21 | 24 |
| 22 | 23 |
| 23 | 23 |
| 24 | 22 |
| 25 | 22 |
| 26 | 21 |
| 27 | 21 |
| 28 | 21 |
| 29 | 20 |
| 30 | 20 |
| 31 | 19 |
| 32 | 19 |
| 33 | 19 |
| 34 | 18 |
| 35 | 18 |
| 36 | 18 |
| 37 | 18 |
| 38 | 17 |
| 39 | 17 |
| 40 | 17 |
| 41 | 17 |
| 42 | 16 |
| 43 | 16 |
| 44 | 16 |
| 45 | 16 |
| 46 | 16 |
| 47 | 16 |
| 48 | 15 |
| 49 | 15 |
| 50+ | 15 |

### Vollkasko SF
| SF | % |
|----|---|
| 0 | 54 |
| 1/2 | 49 |
| 1 | 44 |
| 2 | 42 |
| 3 | 41 |
| 4 | 39 |
| 5 | 38 |
| 6 | 37 |
| 7 | 36 |
| 8 | 34 |
| 9 | 33 |
| 10 | 33 |
| 11 | 32 |
| 12 | 31 |
| 13 | 30 |
| 14 | 29 |
| 15 | 28 |
| 16 | 28 |
| 17 | 27 |
| 18 | 27 |
| 19 | 26 |
| 20 | 25 |
| 21 | 25 |
| 22 | 24 |
| 23 | 24 |
| 24 | 23 |
| 25 | 23 |
| 26 | 23 |
| 27 | 22 |
| 28 | 22 |
| 29 | 21 |
| 30 | 21 |
| 31 | 21 |
| 32 | 20 |
| 33 | 20 |
| 34 | 20 |
| 35 | 19 |
| 36 | 19 |
| 37 | 19 |
| 38 | 19 |
| 39 | 18 |
| 40 | 18 |
| 41 | 18 |
| 42 | 18 |
| 43 | 17 |
| 44 | 17 |
| 45 | 17 |
| 46 | 17 |
| 47 | 16 |
| 48 | 16 |
| 49 | 16 |
| 50+ | 15 |
