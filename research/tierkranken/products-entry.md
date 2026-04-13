# Tierkrankenversicherung — Revised Products Entry

## IMPORTANT: This entry is based on agent descriptions and third-party sources only.
## No online calculator exists. Pricing cannot be independently verified. Confidence: LOW.

## 10. Tierkrankenversicherung (Pet Health Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | tierkranken |
| **Category** | animal |
| **Insured event** | veterinary treatment for illness/accident |
| **Age range** | 0–10 (pet age in years) |
| **Coverage** | Fixed (no annual limit) — no coverage slider |
| **Coverage unit** | N/A (flat monthly premium) |
| **Risk class** | Species: Hund only (1.0) — Katze and Pferd NOT offered by ERGO |
| **Payment duration** | Ongoing |
| **Waiting period** | 30 days |

**Base rates** (monthly): GOT-1x ~20 EUR/month, GOT-2x ~30 EUR/month (UNVERIFIED)
**Age curve**: Flat rate ages 0-4, then +5%/year from age 5 birthday (exponential escalation)
**Loading**: Unknown
**Calibration**: Cannot verify — no online calculator

**Tiers** (REVISED — single tariff, not 3 tiers):
- **GOT-1x**: Erstattung nach 1-fachem GOT-Satz, 30 Tage Wartezeit
- **GOT-2x**: Erstattung nach 2-fachem GOT-Satz, 30 Tage Wartezeit

Both include:
- Ambulante + stationare Behandlung (unbegrenzt)
- Operationen inkl. Medikamente, Rontgen, Verbandsmaterial
- 100 EUR/Jahr Zuschuss fur Impfungen, Wurmkuren, Ektoparasiten, Zahnsteinentfernung
- Chipkosten bis 25 EUR
- Kastrationszuschuss
- Alternative Behandlungen (Homeopathie/Akupunktur)
- 6 Monate Auslandsschutz europaweit
- Freie Tierklinik/Tierarztwahl

**Wizard steps**: Animal type (Hund only) → Pet details (name, breed, age) → GOT level selection → Owner data → Summary

**Form fields**: petName (text), breed (select), petAge (number), chipNumber (text, optional), gotLevel (segmented: 1x/2x), salutation, firstName, lastName, street, zip, city

**Note**: This product has NO online calculator on ergo.de. It is sold exclusively through ERGO agents. Pricing data cannot be independently verified. The current entry is based on agent page descriptions and unverified third-party review sites.

## Source

| Attribute | Detail |
|-----------|--------|
| **Source type** | Agent pages + third-party review sites |
| **Calculator URL** | NONE — product not available online |
| **Confidence** | LOW |
| **Key discrepancy** | Our model assumed 3 tiers, coverage slider, Hund/Katze/Pferd, quadratic age curve. Reality: 1 tariff (2 GOT variants), no slider, Hund only, exponential escalation after age 5. |
| **Verified** | NO — no calculator to sample from |
