# ERGO Motorradversicherung (Zweiradversicherung) Calculator Structure

## Calculator URL
https://www.ergo.de/de/Produkte/KFZ-Versicherung/Motorradversicherung/abschluss

## Calculator Type
Multi-step wizard (13+ steps), branded as "Zweiradversicherung"

## Brand
ERGO (shown in header)

## Wizard Steps

### Step 1: Fahrzeugsuche (#/)
Heading: "Wählen Sie Ihr Fahrzeug."

Two tabs:
1. **ohne Fahrzeugschein** (without registration document):
   - Hersteller (dropdown): HONDA, BMW, YAMAHA, KAWASAKI, SUZUKI, HARLEY-DAVIDSON, etc.
   - Modell (autocomplete text input): dependent on Hersteller
   - Leistung (dropdown): dependent on Modell
   - Hubraum (dropdown): dependent on Modell
   - Results table with radio buttons to select specific variant

2. **mit Fahrzeugschein** (with registration document) [default selected]:
   - HSN (Hersteller-Schlüsselnummer): 4-stellig
   - TSN (Typ-Schlüsselnummer): 3-stellig
   - Erstzulassung (date, TT.MM.JJJJ)

### Step 2: Fahrzeugwert (#/fahrzeugwert)
Heading: "Liegt der geschätzte Neuwert Ihrer [MARKE] unter 30.000 Euro?"
- Radio: Ja / Nein

If Ja, second question appears:
- "Liegt der Wert des mitversicherten Zubehörs unter 30.000 Euro?"
- Radio: Ja / Nein

### Step 3: Versicherungssituation (#/versicherungssituation)
Heading: "Wie ist Ihre Situation?"
- **Versicherer wechseln** [default]: "Bestehendes oder neues Fahrzeug"
- **Fahrzeug wechseln**: "gebraucht oder neu"
- **Erstvertrag**: "Sie möchten das Fahrzeug zum ersten Mal bei ERGO versichern"

### Step 4: Anfangsdatum (#/anfangsdatum)
Heading: "Wann soll die Versicherung beginnen?"
- **Morgen** [default]: shows next day date
- **Zum nächsten Monat**: shows first of next month
- **Anderes Datum**: custom date picker

### Step 5: Saisonkennzeichen (#/saisonkennzeichen)
Heading: "Wollen Sie ein Saisonkennzeichen?"
- **Ja**
- **Nein** [default]

Note: motorcycle-specific field (seasonal plates common for motorcycles)

### Step 6: Fahrzeughalter (#/fahrzeughalter)
Heading: "Wer ist der Fahrzeughalter?"
- **Versicherungsnehmer** [default]
- **(Ehe-)Partner**
- **Kind**
- **Sonstige**

Plus:
- **PLZ** (5-stellig): determines Regionalklasse
- **Ort** (auto-filled from PLZ)

### Step 7: Geburtsdatum (#/geburtsdatum)
Heading: "Fragen zum Versicherungsnehmer"
- **Geburtsdatum** (TT.MM.JJJJ): AFFECTS PRICE (U-shaped curve)
- **Berufsgruppe** (dropdown):
  - Sonstige (Standard) [default]
  - Finanzdienstleister Innendienst
  - Finanzdienstleister Außendienst
  - Beamte, Richter und Pensionäre
  - Beschäftigte im öffentlichen Dienst und Berufssoldaten

### Step 8: Fahrer (#/wer-ist-der-benutzer)
Heading: "Wer fährt Ihre [MARKE]?"
- Versicherungsnehmer [default checked]
- (Ehe-)Partner
- Familienmitglieder
- Sonstige Fahrer

### Step 9: Fahrzeugnutzung (#/fahrzeug-genutzt)
Heading: "Wie wird Ihre [MARKE] genutzt?"
- **Überwiegend privat** (inkl. Arbeitsweg) [default]
- **Überwiegend geschäftlich**
- **Maximale jährliche Fahrleistung**: numeric input (in .000 km), maxlength=3

### Step 10: Fahrzeugfinanzierung (#/fahrzeugfinanzierung)
Heading: "Ist Ihre [MARKE] finanziert?"
- **Nein** [default]
- **Kredit**
- **Leasing**

### Step 11: Rabatt-Quelle (#/rabatt-quelle)
Heading: "Ermittlung der Schadenfreiheitsklasse (SF-Klasse)."
- **aus dem Vorvertrag**: from previous contract
- **von einer anderen Person**: from another person

### Step 12: Bereits versichert (#/bereits-versichert)
Heading: "Ist bereits ein Fahrzeug bei ERGO versichert?"
- **Ja**: "von mir oder meinem (Ehe-)Partner"
- **Nein** [default]

### Step 13: Versicherungsprodukte (#/versicherungsprodukte)
Heading: "Wie soll Ihre [MARKE] abgesichert werden?"

Coverage types:
1. **Haftpflicht ohne Kasko** [default]
2. **Haftpflicht mit Teilkasko**
3. **Haftpflicht mit Vollkasko**

SF-Klasse:
- **Haftpflicht SF-Klasse (SF)**: 22 levels (0 through 20+)
- **Vollkasko SF-Klasse (SF)**: 22 levels (0 through 20+, only visible for Vollkasko)

Button: **Jetzt berechnen**

### Step 14: Beitrag / Price Display (#/beitrag)
Shows:
- Total monthly price
- Breakdown: Kfz-Haftpflicht (with Regionalklasse, SF) + Teilkasko/Vollkasko (with SF)
- Two tiers: **Smart** and **Best**
- Versicherungsbeginn date
- Fahrzeug details

**Selbstbeteiligung** options (only for VK/TK):
- VK 150 / TK ohne
- VK 150 / TK 150 [default]
- VK 300 / TK ohne
- VK 300 / TK 150
- VK 500 / TK ohne
- VK 500 / TK 150
- VK 500 / TK 500
- VK 1000 / TK ohne
- VK 1000 / TK 150
- VK 1000 / TK 1000

**Zahlweise**:
- monatlich [default]
- vierteljährlich
- halbjährlich
- jährlich

**Wählbare Bausteine** (add-ons):
- Motorradbekleidung Plus (motorcycle clothing coverage - MOTORCYCLE-SPECIFIC)
- Schutzbrief (breakdown coverage)
- Ersatzfahrzeug Plus (replacement vehicle)
- Wertschutz 24 (value protection 24 months)
- Wertschutz 36 (value protection 36 months)
- Rabattschutz (SF protection, Best only)

## Key Structural Findings

1. **AGE AFFECTS PRICING**: U-shaped curve. Minimum around age 45-50, higher for young (26) and old (66). This is DIFFERENT from Kfz which had zero age effect.
2. **2 tiers**: Smart and Best (same as Kfz)
3. **22 SF levels** (0 through 20+): Much fewer than Kfz's 51 levels (0 through 50+)
4. **Separate SF tables**: HP and VK have different percentage tables
5. **Teilkasko is FLAT**: No SF scaling for TK (same as Kfz)
6. **Additive structure**: Price = HP_component + VK/TK_component + add-ons
7. **Vehicle-specific pricing**: via HSN/TSN
8. **Region**: PLZ determines Regionalklasse
9. **Mileage**: Annual mileage affects price
10. **Seasonal plates**: Optional Saisonkennzeichen (motorcycle-specific)
11. **Motorcycle-specific add-on**: Motorradbekleidung Plus (clothing protection)

## SF Percentage Tables

### Haftpflicht SF (22 levels)
| SF | % |
|----|---|
| 0 | 100 |
| 1/2 | 74 |
| 1 | 54 |
| 2 | 48 |
| 3 | 44 |
| 4 | 40 |
| 5 | 38 |
| 6 | 36 |
| 7 | 34 |
| 8 | 32 |
| 9 | 31 |
| 10 | 30 |
| 11 | 29 |
| 12 | 28 |
| 13 | 28 |
| 14 | 27 |
| 15 | 27 |
| 16 | 26 |
| 17 | 26 |
| 18 | 25 |
| 19 | 25 |
| 20+ | 24 |

### Vollkasko SF (22 levels)
| SF | % |
|----|---|
| 0 | 100 |
| 1/2 | 76 |
| 1 | 55 |
| 2 | 49 |
| 3 | 46 |
| 4 | 43 |
| 5 | 40 |
| 6 | 38 |
| 7 | 36 |
| 8 | 35 |
| 9 | 34 |
| 10 | 33 |
| 11 | 32 |
| 12 | 31 |
| 13 | 30 |
| 14 | 30 |
| 15 | 29 |
| 16 | 28 |
| 17 | 28 |
| 18 | 28 |
| 19 | 27 |
| 20+ | 27 |

## Differences from Kfz

| Feature | Kfz | Motorrad |
|---------|-----|----------|
| Age effect | NONE | U-shaped curve |
| SF levels | 51 (0-50+) | 22 (0-20+) |
| HP SF 0 | 86% | 100% |
| HP SF max | 15% (SF 50+) | 24% (SF 20+) |
| Seasonal plates | Optional | Optional (more common) |
| Motorcycle clothing add-on | N/A | Motorradbekleidung Plus |
| Vehicle value question | N/A | Under 30k EUR check |
| Wizard steps | ~5 | ~13 (more granular) |
