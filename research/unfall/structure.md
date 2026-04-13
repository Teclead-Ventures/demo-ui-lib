# ERGO Unfallversicherung — Calculator Structure

**URL**: https://www.ergo.de/de/Produkte/Unfallversicherung/abschluss
**Type**: Multi-step wizard (React SPA)
**Date**: 2026-04-13

## Wizard Steps

### Step 1: Wen möchten Sie versichern? (#/wer-zu-versichern)
- Radio selection:
  - **Mich selbst** (pre-selected)
  - Mich und weitere Personen
  - Nur andere Personen

### Step 2: Geburtsdatum (#/geburtstag)
- Three spin buttons: Tag, Monat, Jahr
- Date determines age band (<65 or >=65)

### Step 3: Beruf (#/beruf)
- Autocomplete combobox with thousands of specific job titles
- NO generic risk class selection (unlike our assumptions)
- Some occupations trigger follow-up questions:
  - "Polizist" → "Sind Sie ausschließlich kaufmännisch/verwaltend tätig?" (Ja/Nein)
- Internal mapping to at least 3 risk groups (see price analysis)

### Step 4: Arbeitsverhältnis (#/arbeitsverhaltnis)
- "Sind Sie hauptberuflich selbstständig tätig?" (Ja/Nein)
- Pre-selected: Nein
- NOTE: This step is sometimes SKIPPED (e.g., for Dachdecker it went straight to coverage)

### Step 5: Kapitaleinlage (#/kapitaleinlage)
- "Versicherungssumme für die Kapitalleistung bei Invalidität"
- Slider + combobox input
- **Range**: 10.000 € to 300.000 € (NOT 25k-500k as assumed!)
- **Default**: 50.000 €
- Step size appears to be 5.000 € or 10.000 €

### Step 6: Tarifauswahl (#/tarifauswahl)
- Main configuration page where all pricing is visible
- **Tier selection** (radio buttons):
  - Basic mit Progression 300%
  - Smart mit Progression 300%
  - Best mit Progression 600%
- **Price display**: updates live when switching tiers
- **Coverage editable**: text field allows changing coverage, price updates on blur/Tab
- **Optional add-ons** (checkboxes):
  - Unfall-Rente
  - Unfall-Hilfe
  - Verletzungsgeld
  - Krankenhaus-Tagegeld
  - Todesfallleistung
  - Unfall-Pflege
- **Vertragslaufzeit** (contract duration):
  - Basic: locked to 1 Jahr
  - Smart/Best: 1, 2, 3, or 4 Jahre
  - Note: "Durch Laufzeiten ab 3 Jahren kann sich bei Smart oder Best ein besseres Preis-Leistungs-Verhältnis ergeben"

## Key Structural Differences from Our Assumptions

1. **Tier names**: Basic/Smart/Best (NOT Grundschutz/Komfort/Premium)
2. **Coverage range**: 10k-300k (NOT 25k-500k)
3. **Default coverage**: 50k (NOT 100k)
4. **No generic risk class selection**: Uses specific job titles, internally mapped to risk groups
5. **Progression is tier-dependent**: Basic/Smart = 300%, Best = 600%
6. **Optional add-ons** not in our model: Rente, Hilfe, Verletzungsgeld, KH-Tagegeld, Todesfallleistung, Pflege
7. **Contract duration affects Smart/Best pricing** (multi-year discounts)
8. **Age band system**: Only 2 bands (<65 and >=65), NOT continuous curve
