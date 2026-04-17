# ERGO Product Calculator URLs

Known URLs for ERGO's online tariff calculators. Updated by the scout agent at the start of each research run.

**Last updated**: 2026-04-13 (13 products confirmed: Zahnzusatz, Sterbegeld, Risikoleben, Hausrat, Rechtsschutz, Unfall, Pflegezusatz, Haftpflicht, Kfz, Wohngebäude, Motorrad, Krankentagegeld, Reise. 3 products NO calculator: Tierkranken, BU, Cyber)

## Consumer portal (ergo.de)

| Product | Product page | Calculator URL | Status |
|---------|-------------|---------------|--------|
| Zahnzusatz | https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz | /abschluss_DS75, /abschluss_DS90, /abschluss_DS100 | CONFIRMED — 3 separate calculators. Beitragstabelle dialog on product page. Researched 2026-04-12. |
| Sterbegeld | https://www.ergo.de/de/Produkte/Sterbegeldversicherungen/Sterbegeldversicherung | /abschluss | CONFIRMED — 4-step wizard. No Beitragstabelle. 160 data points. Researched 2026-04-13. |
| Risikoleben | https://www.ergo.de/de/Produkte/Lebensversicherung/Risikolebensversicherung | /abschluss | CONFIRMED — 8-step wizard + price page. 3 smoker classes. Employment+occupation fields. 75 data points. Researched 2026-04-13. |
| Hausrat | https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Hausratversicherung | /abschluss | CONFIRMED — 7-step wizard. Only 2 tiers (Smart/Best). Per-m² model. 23 data points. Researched 2026-04-13. |
| Kfz (Auto) | https://www.ergo.de/de/Produkte/KFZ-Versicherung/Autoversicherung | /abschluss#/neu/ | CONFIRMED — 5-step wizard. 2 tiers (Smart/Best). Additive HP+VK components. SF-Klasse 0-50+ with 51 levels. NO age curve. Vehicle via HSN/TSN cascading dropdowns. 28 data points. Researched 2026-04-13. |
| Rechtsschutz | https://www.ergo.de/de/Produkte/Rechtsschutzversicherung | /abschluss | CONFIRMED — 4 intake steps + configurator page. Only 2 tiers (Smart/Best). Additive Bausteine (Privat/Beruf/Wohnen/Verkehr). NO age pricing. 42 data points. Researched 2026-04-13. |
| Unfall | https://www.ergo.de/de/Produkte/Unfallversicherung | /abschluss | CONFIRMED — 6-step wizard. 3 tiers (Basic/Smart/Best). Step-function age (1.0×/<65, 2.0×/≥65). Occupation autocomplete. 16 data points. Researched 2026-04-13. |
| Pflegezusatz | https://www.ergo.de/de/Produkte/Pflegeversicherung/Pflegezusatzversicherung | /abschluss-tagegeld | CONFIRMED — DKV-branded single-page configurator. 3 separate products (PTG/PZU/KFP). PTG exponential age curve. 82 data points. Researched 2026-04-13. |
| Haftpflicht | https://www.ergo.de/de/Produkte/Haftpflichtversicherung/Privathaftpflichtversicherung | /abschluss | CONFIRMED — 3 intake steps + configurator page. 2 tiers (Smart/Best). Template D (additive Bausteine). Binary age (<36 Startbonus). 32 data points. Researched 2026-04-13. |
| BU | https://www.ergo.de/de/Produkte/Berufsunfaehigkeitsversicherung | NONE | NO_CALCULATOR — Page exists but advisor-only ("Angebot anfordern"). No self-service calculator. Confirmed 2026-04-13. |
| Reise (Rücktritt) | https://www.ergo.de/de/Produkte/Reiseversicherung/Reiseruecktrittsversicherung | app.ergo-reiseversicherung.de/ba4/landingPage.html | CONFIRMED — External ERV domain. 3 product categories (Storno/Rundum/Kranken). Trip-cost-based pricing. Age bands. Template F. 20+ data points. Researched 2026-04-13. |
| Wohngebäude | https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Wohngebaeudeversicherung | wohngebaeudeversicherung.ergo.de | CONFIRMED — External subdomain. 2 tiers (Smart/Best). Per-m² pricing. Construction year bands. Address-specific (ZÜRS). Template C variant. 15 data points. Researched 2026-04-13. |
| Tierkranken | https://www.ergo.de/de/Produkte/Tierversicherung | NONE | NO_CALCULATOR — Agent-only product. No product page on ergo.de (all URLs return 404). ERGO agents sell third-party products (HanseMerkur, Uelzener, Helvetia). Only Hundehalterhaftpflicht and Pferdehalterhaftpflicht exist online. Researched 2026-04-13. |
| Motorrad | https://www.ergo.de/de/Produkte/KFZ-Versicherung/Motorradversicherung | /abschluss | CONFIRMED — ~13-step wizard. 2 tiers (Smart/Best). Template E variant with U-shaped age curve. 22 SF levels. ~22 data points. Researched 2026-04-13. |
| Cyber | N/A | NONE | NOT_FOUND — No product page exists (404). Confirmed 2026-04-13. |
| Krankentagegeld | https://www.ergo.de/de/Produkte/Krankenversicherung/Krankentagegeld | /abschluss | CONFIRMED — DKV-branded single-page configurator. Single product (KombiMed KTAG). Separate AN/SE tariff tables. No tiers. ~146 data points. Researched 2026-04-13. |

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
