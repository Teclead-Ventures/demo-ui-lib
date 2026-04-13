# ERGO Tierkrankenversicherung — Structure Discovery

## Date: 2026-04-13

## Critical Finding: NO ONLINE CALCULATOR EXISTS

ERGO does **not** sell Tierkrankenversicherung as a direct online product. There is:
- **No product page** under ergo.de/de/Produkte/... for Tierkrankenversicherung
- **No online calculator** ("Beitrag berechnen" / "abschluss" URL)
- **No Beitragstabelle** on any page

### What ERGO does sell online (pet-related):
- **Hundehalterhaftpflichtversicherung** (dog liability) — has product page + calculator
- **Pferdehalterhaftpflichtversicherung** (horse liability) — has product page + calculator

### What ERGO does NOT sell online:
- **Tierkrankenversicherung** (pet health insurance) — agent-only product
- **Katzenkrankenversicherung** — not offered at all
- **Pferdekrankenversicherung** — not offered at all (agents refer to HanseMerkur/Uelzener/Helvetia)

## Evidence

### 1. Product page URLs — all return 404:
- https://www.ergo.de/de/Produkte/Tierversicherung → 404
- https://www.ergo.de/de/Produkte/Tierversicherung/Tierkrankenversicherung → 404
- https://www.ergo.de/de/Produkte/Tierversicherung/Hundekrankenversicherung → 404
- https://www.ergo.de/de/Produkte/Tierkrankenversicherung → 404
- https://www.ergo.de/de/Produkte/Krankenversicherung/Tierkrankenversicherung → 404
- https://www.ergo.de/de/Produkte/Tierversicherung/Tierkrankenversicherung/abschluss → 404
- https://www.ergodirekt.de/de/produkte/tierkrankenversicherung.html → redirects to ergo.de → 404

### 2. ERGO Produkte overview page (ergo.de/de/Produkte):
- Lists Hundehalterhaftpflicht and Pferdehalterhaftpflicht under "HAFTPFLICHTVERSICHERUNGEN"
- NO mention of any Tierkrankenversicherung product
- All "Krankenversicherungen" listed are for humans (DKV branded)

### 3. ERGO Ratgeber pages:
- ergo.de/de/Ratgeber/reise_und_freizeit/tierversicherung — informational only, no product links
- ergo.de/de/Ratgeber/familie/hundeversicherung — informational only, links only to Hundehalterhaftpflicht
- ergo.de/de/Ratgeber/familie/katzenversicherung — informational only

### 4. ERGO Agent pages confirm the product exists but is agent-only:
- Agent Anette Schuhmann describes "Hunde-Krankenversicherung" with specific features
- Agent Martin Gloeckner explicitly states he sells Tierkranken from **HanseMerkur, Uelzener, and Helvetia** — NOT from ERGO itself
- Agent Rainer Warns has a generic "Tierkrankenversicherung" page with no product details

### 5. Third-party review sites provide conflicting information:
- sicherheitsanker.de claims ERGO has "ErgoPremio" tariff and also shows 3 tiers (Basis/Komfort/Premium) — contradictory
- insurancy.de shows a comparison calculator iframe (not ERGO-specific) with age-band pricing examples
- tierversicherung-24.de confirms ERGO only has Tierhalterhaftpflicht (Basis/Premium tarife)

## Product Structure (from Agent Descriptions)

Based on agent page descriptions, ERGO's Hunde-Krankenversicherung appears to be:

### Single Tariff (one tier)
- Erstattung ohne Jahreslimit (no annual limit on reimbursement)
- Choice of 1x or 2x GOT reimbursement rate
- 100% Erstattung in jedem Hundealter
- Ambulante und stationare Behandlung, Vorbehandlung, Nachsorge (all unlimited)
- Operationen inkl. Medikamente, Rontgen, Verbandsmaterial
- Freie Tierklinik/Tierarztwahl
- 100 EUR/year Zuschuss for Impfungen, Wurmkuren, Ektoparasiten, Zahnsteinentfernung
- Chipkosten bis 25 EUR
- Kostenzuschuss bei Kastrationen
- Alternative Behandlungen (Homeopathie/Akupunktur)
- 6 Monate Auslandsschutz europaweit
- 30 Tage Wartezeit
- **5% jahrliche Beitragsanpassung ab dem 5. Geburtstag des Hundes**

### Key Differences from Our Model:
1. **Tiers**: Our model assumes 3 tiers (Grundschutz/Komfort/Premium). Reality: appears to be 1 tariff with GOT level choice (1x vs 2x)
2. **Coverage slider**: Our model has a EUR budget slider. Reality: no annual limit (or if limit exists, it's fixed per tariff)
3. **Species**: Our model has Hund/Katze/Pferd. Reality: only Hund. No Katze or Pferd Krankenversicherung from ERGO
4. **Age curve**: Our model uses quadratic. Reality: flat rate with 5% annual increase after age 5
5. **Online availability**: Our model assumes online calculator. Reality: agent-only product, no online purchase path

## Conclusion

**ERGO does not offer Tierkrankenversicherung through an online calculator.** The product exists as an agent-mediated product (likely underwritten by a partner like Uelzener), but there is no way to calculate or purchase it through ergo.de.

This means we CANNOT perform Phase B (price sampling) or Phase C (pricing analysis) as designed.

### Recommendation
The tierkranken entry in products.md should be flagged as:
- **Source**: Agent descriptions only (no calculator verification possible)
- **Confidence**: LOW
- **Note**: No online calculator exists; pricing cannot be independently verified
