# ERGO Zahnzusatzversicherung — Form Structure

**Source**: https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz
**Calculator URLs**:
- DS75: https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz/abschluss_DS75
- DS90: https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz/abschluss_DS90
- DS100: https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz/abschluss_DS100
**Researched**: 2026-04-12
**Total steps**: 4 (calculator) + application steps (not researched)

## Key Structural Difference from Our Model

ERGO's Zahnzusatz is NOT a coverage-budget product. There is NO coverage slider.
- The tariff (DS75/DS90/DS100) determines the Erstattungssatz (reimbursement percentage)
- DS75 = 75% reimbursement, DS90 = 90%, DS100 = 100%
- Pricing is a flat rate per age band per tariff — NOT per coverage unit
- There is no user-selectable coverage amount; the tariff name IS the coverage level

## Pricing Structure

ERGO uses **discrete age bands** with fixed monthly prices per band:

| Age Band | DS75 (€/month) | DS90 (€/month) | DS100 (€/month) |
|----------|----------------|----------------|-----------------|
| 0–20     | 2.90           | 3.70           | 4.80            |
| 21–25    | 5.70           | 7.20           | 9.20            |
| 26–30    | 10.90          | 13.80          | 17.50           |
| 31–40    | 17.40          | 21.70          | 27.60           |
| 41–50    | 25.90          | 32.50          | 41.30           |
| 51+      | 34.80          | 44.40          | 57.80           |

**Special**: First 6 months at 50% (Startbeitrag).

## Step 1: Initial Selection (#/initial-selection)

**Heading**: "Wer soll versichert werden?"
**Subtext**: "Bei ERGO bekommen Sie online den passenden Versicherungsschutz für ein strahlendes Lächeln."

- Field: Who to insure — Type: radio — Options: "Ich" / "Ich und jemand anders" / "Nur jemand anders" — Required: yes
- "weiter" button (disabled until selection made)

## Step 2: Birth Date (#/myself)

**Heading**: "Bitte geben Sie Ihr Geburtsdatum an."
**Subtext**: "Ihr Alter ist notwendig, um Ihren Beitrag zu berechnen."

- Field: Tag — Type: spinbutton — Required: yes
- Field: Monat — Type: spinbutton — Required: yes
- Field: Jahr — Type: spinbutton — Required: yes
- "Mehr Informationen anzeigen" button (info about age calculation)
- "weiter" button (disabled until valid date), "zurück" button

## Step 3: Start Date (still #/myself, rendered after entering birth date)

**Heading**: "Wann soll Ihre Versicherung beginnen?"

- **Price display**: Shows calculated price prominently at top
  - Format: "XX,XX € monatlich*" (first 6 months, half price)
  - Below: "Ab dem 7. Monat je XX,XX €*" (full price)
- Field: Start date — Type: radio — Options: 1st of next 3 months (e.g., 01.05.2026 / 01.06.2026 / 01.07.2026) — Required: yes, default: first option
- "weiter" button, "zurück" button

## Step 4: Plan Comparison (#/contribution)

**Heading**: "Wählen Sie Ihren Versicherungsschutz"

- Tabs: "Dental-Schutz [X]" (selected) | "Dental-Vorsorge + Dental-Schutz [X]" (combined tariff with preventive add-on)
- Plan benefits display:
  - DS100: 100% for implants, bridges/crowns/prosthetics, inlays/onlays
  - Leistungsbegrenzungen: max 1000€ Y1, 2000€ Y1-2, 3000€ Y1-3, 4000€ Y1-4
  - KFO for children: up to 1000€ total
  - GOZ-Satz: up to 3.5x (Zahnerhalt) / 5.0x (Zahnersatz)
- "Alle Leistungen im Vergleich" button → comparison overlay
- Price shown at top (same as step 3)
- Actions: "Weiter zum Online-Abschluss" / "Angebot anfordern" / "zurück"

## Additional Product Info

- The "Dental-Vorsorge" (DVB/DVE) is a separate preventive dental product that can be combined
- Each DS tariff page also has a "Beitragstabelle" dialog with all 3 tariffs' prices by age band
- First 6 months are half price (Startbeitrag) for all DS tariffs
- No Gesundheitsprüfung (health questionnaire) — stated explicitly
- No Wartezeit (waiting period) — stated explicitly on the comparison page
- Missing/unreplaced teeth at contract start are excluded from coverage
- Treatment must not have started before contract start

## Fields NOT Present (vs Our Model)

- ❌ NO coverage amount slider (our model assumes €500–€5,000 budget)
- ❌ NO dental status selection (our model has Sehr gut / Gut / Befriedigend / Lückenhaft)
- ❌ NO missing teeth count (our model has missingTeeth 0-10)
- ❌ NO risk class
- ✅ Birth date
- ✅ Insurance start date
- ✅ Plan selection (but pre-selected by URL, not in-wizard)
