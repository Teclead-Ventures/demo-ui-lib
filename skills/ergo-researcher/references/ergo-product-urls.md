# ERGO Product Calculator URLs

Known URLs for ERGO's online tariff calculators. Updated by the scout agent at the start of each research run.

**Last updated**: 2026-04-13 (Zahnzusatz, Sterbegeld, Risikoleben, Hausrat confirmed)

## Consumer portal (ergo.de)

| Product | Product page | Calculator URL | Status |
|---------|-------------|---------------|--------|
| Zahnzusatz | https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz | /abschluss_DS75, /abschluss_DS90, /abschluss_DS100 | CONFIRMED — 3 separate calculators. Beitragstabelle dialog on product page. Researched 2026-04-12. |
| Sterbegeld | https://www.ergo.de/de/Produkte/Sterbegeldversicherungen/Sterbegeldversicherung | /abschluss | CONFIRMED — 4-step wizard. No Beitragstabelle. 160 data points. Researched 2026-04-13. |
| Risikoleben | https://www.ergo.de/de/Produkte/Lebensversicherung/Risikolebensversicherung | /abschluss | CONFIRMED — 8-step wizard + price page. 3 smoker classes. Employment+occupation fields. 75 data points. Researched 2026-04-13. |
| Hausrat | https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Hausratversicherung | /abschluss | CONFIRMED — 7-step wizard. Only 2 tiers (Smart/Best). Per-m² model. 23 data points. Researched 2026-04-13. |
| Kfz (Auto) | https://www.ergo.de/de/Produkte/KFZ-Versicherung/Autoversicherung | likely /abschluss | Unconfirmed — full Tarifrechner expected |
| Haftpflicht | https://www.ergo.de/de/Produkte/Haftpflichtversicherung | likely /abschluss | Unconfirmed |
| Rechtsschutz | https://www.ergo.de/de/Produkte/Rechtsschutzversicherung | likely /abschluss | Unconfirmed |
| BU | https://www.ergo.de/de/Produkte/Berufsunfaehigkeitsversicherung | unknown | Unconfirmed — possibly broker-only |
| Unfall | https://www.ergo.de/de/Produkte/Unfallversicherung | Likely |
| Reise | https://www.ergo.de/de/Produkte/Reiseversicherung | Likely |
| Wohngebäude | https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung | Possibly combined with Hausrat |
| Pflege | https://www.ergo.de/de/Produkte/Pflegeversicherung | Possibly |
| Motorrad | https://www.ergo.de/de/Produkte/KFZ-Versicherung/Motorradversicherung | Yes |

## Broker portal (makler.ergo.de)

Some products have more detailed calculators on the broker portal. These may or may not require login.

| Product | Broker URL | Auth required? |
|---------|-----------|---------------|
| Sterbegeld | https://makler.ergo.de/tarifrechner-new/leben/sterbevorsorge | Unknown |
| Sterbegeld (alt) | https://makler.ergo.de/calculators/stg-calculator/quote | Unknown |
| BU | https://makler.ergo.de/calculators/sbu/quote | Unknown |
| BU (alt) | https://makler.ergo.de/calculators/makler/sbu/quote | Unknown |
| Leben (bAV) | https://makler.ergo.de/tarifrechner-new/leben/bav | Likely login required |

## Notes

- The scout agent should update this file with actual findings
- Mark each URL as: CONFIRMED (calculator found) | NO_CALCULATOR (product page only) | AUTH_REQUIRED (needs login) | NOT_FOUND (404/redirect)
- Record the exact "Beitrag berechnen" button URL for each confirmed calculator
