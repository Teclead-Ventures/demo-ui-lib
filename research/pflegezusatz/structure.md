# ERGO Pflegezusatzversicherung — Calculator Structure

## Product Overview

ERGO's Pflegezusatzversicherung is actually **three separate products** (not three tiers of one product):

| Product | Tariff Code | Calculator URL | Age-Dependent? |
|---------|-------------|---------------|----------------|
| Pflege Tagegeld | PTG | /abschluss-tagegeld | YES |
| Pflege-Zuschuss | PZU (50/100) | /abschluss-zuschuss | NO (fixed) |
| KombiMed Förder-Pflege | KFP | /abschluss-foerderpflege | NO (fixed) |

All are under the DKV brand (ERGO's health insurance subsidiary).

## Calculator Type: Single-Page Configurator

Each product variant has its own single-page calculator. No wizard, no multi-step process.

### PTG (Pflege Tagegeld) — "Bestseller"

**URL**: https://www.ergo.de/de/Produkte/Pflegeversicherung/Pflegezusatzversicherung/abschluss-tagegeld

**Fields**:
1. **Geburtsjahr** (birth year) — Dropdown, 1927-2026 (age 0-99)
2. **Tagegeldhöhe** (daily benefit) — Dropdown, 5-160 EUR/day in steps of 5 EUR

**Output**:
- Pflege Tagegeld: X.XX EUR/month
- Gesamtbeitrag: X.XX EUR/month (same as above, single product)

**Features**:
- No health questionnaire in the calculator
- No waiting period
- Inflationsschutz (inflation protection) every 3 years
- Anlassbezogene Erhöhungsoption (event-based increase option)
- Kostenloses Pflegetelefon

### PZU (Pflege-Zuschuss)

**URL**: https://www.ergo.de/de/Produkte/Pflegeversicherung/Pflegezusatzversicherung/abschluss-zuschuss

**Fields**:
1. **Geburtsjahr** — Dropdown (but price does NOT change)
2. **Tarif selection** — PZU50 (50% supplement) or PZU100 (100% supplement)

**Fixed prices** (all ages):
- PZU50: 29.70 EUR/month
- PZU100: 59.40 EUR/month

### KFP (KombiMed Förder-Pflege)

**URL**: https://www.ergo.de/de/Produkte/Pflegeversicherung/Pflegezusatzversicherung/abschluss-foerderpflege

**Fields**:
1. **Geburtsjahr** — Dropdown (but price does NOT change)

**Fixed price**: 25.72 EUR/month (after 5 EUR/month state subsidy deduction)
- No health questions
- Mindestleistung 600 EUR/month in Pflegegrad 5
- Erhöhte Leistung nach 15 Versicherungsjahren

## Pflege Schutz Paket (PSP) — Optional Add-On

**URL**: https://www.ergo.de/de/Produkte/Pflegeversicherung/pflegeschutzpaket/abschluss

Combinable with all tariffs or standalone:
- 24-Stunden-Versorgungsgarantie
- Beratungsleistungen
- Vermittlung von Serviceleistungen
- 1.000 EUR Einmalzahlung (ab Pflegegrad 2)
- Ohne Gesundheitsprüfung

## Comparison Table Summary

| Feature | PTG | PZU | KFP |
|---------|-----|-----|-----|
| Ambulante Pflege | ✓ | ✓ | ✓ |
| Stationäre Pflege | ✓ | ✓ | ✓ |
| Sofortiger Schutz (keine Wartezeit) | ✓ | ✓ | ✗ |
| Inflationsschutz | ✓ | ✓ | ✗ |
| Rückwirkende Leistungen | ✓ | ✓ | ✓ |
| Pflegetelefon | ✓ | ✓ | ✗ |
| Gesetzliche Leistungen als Basis | ✗ | ✓ | ✗ |
| Erhöhungsoption | ✓ | ✗ | ✗ |
