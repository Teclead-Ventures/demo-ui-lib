# Insurance Product Knowledge Base

This file contains pre-built defaults for common German insurance products. Each entry provides everything needed to generate a complete tariff spec.

When the user names a product, find the matching entry and use it as the starting point. Adjust based on any user preferences.

---

## 1. Sterbegeldversicherung (Funeral Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | sterbegeld |
| **Category** | person |
| **Insured event** | death |
| **Age range** | 40–85 |
| **Coverage** | €1.000–€20.000, step €1.000, default €8.000 |
| **Coverage unit** | per €1.000 |
| **Risk class** | None (age only) |
| **Payment duration** | 85 − age |
| **Waiting period** | Grundschutz: 18 months, Komfort: 18 months, Premium: 3 months |

**Base rates** (per €1k/month): Grundschutz €3.68, Komfort €4.49, Premium €5.53
**Age curve**: base=0.65, linear=0.15, quadratic=0.55 (exponential growth after 60)
**Loading**: 25%
**Calibration**: 44yo, €8k, Komfort → ~€30/month ✓

**Tiers**:
- **Grundschutz**: Guaranteed death benefit, surplus participation ×1.32, 18-month waiting
- **Komfort**: Same + higher surplus ×1.50, Unfall-Sofortschutz ab Tag 1
- **Premium**: Same + surplus ×1.74, 3-month waiting, severe illness early payout, coverage >€15k

**Wizard steps**: Birth date → Insurance start → Coverage slider → Plan selection → Dynamic adjustment → Personal data → Summary

**Form fields**: birthDate, insuranceStart (3 radio options: 1st of next 3 months), coverageAmount (slider), plan (segmented), dynamicAdjustment, salutation, firstName, lastName, street, zip, city, birthPlace, nationality

---

## 2. Berufsunfähigkeitsversicherung (Disability / BU)

| Parameter | Value |
|-----------|-------|
| **ID** | berufsunfaehigkeit |
| **Category** | person |
| **Insured event** | disability (≥50% unable to work in current profession) |
| **Age range** | 18–55 |
| **Coverage** | €500–€5.000/month income replacement, step €100, default €2.000 |
| **Coverage unit** | per €100/month |
| **Risk class** | Occupation: Bürotätigkeit (1.0), Handwerk (1.4), Schwere körperliche Arbeit (1.8), Gefahrenberufe (2.2) |
| **Payment duration** | 67 − age (until retirement) |
| **Waiting period** | Grundschutz: 6 months, Komfort: 3 months, Premium: none |

**Base rates** (per €100 income/month): Grundschutz €2.08, Komfort €2.54, Premium €3.12
**Age curve**: base=0.70, linear=0.50, quadratic=−0.15 (bell curve, peaks ~45-50)
**Loading**: 28%
**Calibration**: 30yo desk worker, €2k/mo, Komfort → ~€55/month ✓

**Tiers**:
- **Grundschutz**: 50%+ BU definition, 6-month Karenzzeit, benefits until 67
- **Komfort**: Same + 3-month Karenz, Nachversicherungsgarantie, Infektionsklausel
- **Premium**: Same + no Karenz, Dienstunfähigkeitsklausel, Umorganisation verzicht, weltweiter Schutz

**Wizard steps**: Occupation → Birth date → Income/Coverage → Plan selection → Health questions (simplified) → Personal data → Summary

**Form fields**: occupation (select with risk classes), birthDate, monthlyIncome (number), coverageAmount (slider, max 75% of income), plan, smoker (inline-radio: Ja/Nein), preExistingConditions (inline-radio: Ja/Nein), salutation, firstName, lastName, street, zip, city

**Validation**: Age 18-55, coverage ≤ 75% of stated income, occupation required

---

## 3. Zahnzusatzversicherung (Dental Supplementary)

| Parameter | Value |
|-----------|-------|
| **ID** | zahnzusatz |
| **Category** | person |
| **Insured event** | dental treatment, dentures, orthodontics |
| **Age range** | 18–75 |
| **Coverage** | €500–€5.000/year dental budget, step €250, default €1.500 |
| **Coverage unit** | per €250/year |
| **Risk class** | None (age-based pricing only) |
| **Payment duration** | Ongoing (no end date, cancel anytime after minimum 2 years) |
| **Waiting period** | Grundschutz: 8 months, Komfort: 3 months, Premium: none |

**Base rates** (per €250/year): Grundschutz €2.70, Komfort €3.29, Premium €4.05
**Age curve**: base=0.80, linear=0.35, quadratic=0.10 (gentle linear increase)
**Loading**: 22%
**Calibration**: 35yo, €1.5k budget, Komfort → ~€22/month ✓

**Tiers**:
- **Grundschutz**: 60% Zahnbehandlung, 50% Zahnersatz, 8-month waiting
- **Komfort**: 80% Zahnbehandlung, 70% Zahnersatz, professionelle Zahnreinigung 1×/year, 3-month waiting
- **Premium**: 100% Zahnbehandlung, 90% Zahnersatz, Zahnreinigung 2×/year, Kieferorthopädie, Implantate, no waiting

**Wizard steps**: Birth date → Coverage budget → Dental status → Plan selection → Personal data → Summary

**Form fields**: birthDate, coverageAmount (slider), dentalStatus (select: Sehr gut / Gut / Befriedigend / Lückenhaft), missingTeeth (number, 0-10), plan, salutation, firstName, lastName, street, zip, city

**Validation**: Age 18-75, missingTeeth ≤ 10

---

## 4. Hausratversicherung (Household Contents)

| Parameter | Value |
|-----------|-------|
| **ID** | hausrat |
| **Category** | property |
| **Insured event** | damage/loss of household contents (fire, water, storm, theft) |
| **Age range** | 18–99 (age-independent pricing) |
| **Coverage** | €10.000–€150.000, step €5.000, default €50.000 |
| **Coverage unit** | per €5.000 |
| **Risk class** | Region: Zone 1 (0.85, rural), Zone 2 (1.0, suburban), Zone 3 (1.25, urban), Zone 4 (1.5, high-risk urban) |
| **Payment duration** | Annual renewal |
| **Waiting period** | None |

**Base rates** (per €5k/month): Grundschutz €0.44, Komfort €0.53, Premium €0.66
**Age curve**: base=1.0, linear=0.0, quadratic=0.0 (flat — age doesn't matter)
**Loading**: 20%
**Calibration**: €50k urban (Zone 3, 1.25×), Komfort → ~€8/month ✓

**Tiers**:
- **Grundschutz**: Fire, water, storm, basic theft. Selbstbeteiligung €500
- **Komfort**: Same + Elementarschäden (flooding), Fahrraddiebstahl bis €3.000, Selbstbeteiligung €250
- **Premium**: Same + Glasbruch, grobe Fahrlässigkeit, Überspannungsschäden, keine Selbstbeteiligung

**Wizard steps**: Address/Region → Living space → Coverage amount → Plan selection → Personal data → Summary

**Form fields**: zip (for region lookup), livingSpace (number, m²), buildingType (select: Mehrfamilienhaus/Einfamilienhaus/Reihenhaus), floor (select: EG/OG/DG), coverageAmount (slider), plan, salutation, firstName, lastName, street, city

---

## 5. Privathaftpflichtversicherung (Personal Liability)

| Parameter | Value |
|-----------|-------|
| **ID** | privathaftpflicht |
| **Category** | liability |
| **Insured event** | third-party damage (personal injury, property damage, financial loss) |
| **Age range** | 18–99 |
| **Coverage** | €1M–€50M, step €5M, default €10M |
| **Coverage unit** | flat rate (coverage amount affects payout cap, not premium much) |
| **Risk class** | Family status: Single (1.0), Familie (1.35), Single mit Kind (1.20) |
| **Payment duration** | Annual renewal |
| **Waiting period** | None |

**Base rates** (flat/month, coverageUnit=defaultCoverage so units=1): Grundschutz €4.10, Komfort €5.00, Premium €6.15
**Age curve**: base=1.0, linear=0.0, quadratic=0.0 (flat)
**Loading**: 20%
**Calibration**: Single, €10M, Komfort → ~€6/month ✓

**Tiers**:
- **Grundschutz**: €1M Deckung, Personenschäden, Sachschäden, Selbstbeteiligung €150
- **Komfort**: €10M Deckung, + Schlüsselverlust, Gefälligkeitsschäden, Mietsachschäden, SB €0
- **Premium**: €50M Deckung, + Internetschäden, Drohnen, Ehrenamt, weltweiter Schutz, Forderungsausfalldeckung

**Wizard steps**: Family status → Coverage sum → Plan selection → Personal data → Summary

**Form fields**: familyStatus (segmented: Single/Familie/Single mit Kind), coverageAmount (slider), plan, salutation, firstName, lastName, street, zip, city

---

## 6. Rechtsschutzversicherung (Legal Protection)

| Parameter | Value |
|-----------|-------|
| **ID** | rechtsschutz |
| **Category** | liability |
| **Insured event** | legal disputes (lawyer fees, court costs) |
| **Age range** | 18–75 |
| **Coverage** | €100.000–€1.000.000, step €100.000, default €300.000 |
| **Coverage unit** | flat rate (coverage determines max payout) |
| **Risk class** | None |
| **Payment duration** | Annual renewal |
| **Waiting period** | 3 months for all tiers |

**Base rates** (flat/month, coverageUnit=defaultCoverage so units=1): Grundschutz €12.50, Komfort €22.00, Premium €35.00
**Age curve**: base=0.90, linear=0.15, quadratic=0.05 (slight increase with age)
**Loading**: 23%

**Tiers**:
- **Grundschutz**: Privatrechtsschutz only, Selbstbeteiligung €250
- **Komfort**: + Berufsrechtsschutz, Verkehrsrechtsschutz, SB €150
- **Premium**: + Mietrechtsschutz, Steuerrechtsschutz, Mediation, SB €0, Anwaltshotline 24/7

**Wizard steps**: Legal areas (checkboxes) → Coverage sum → Plan selection → Personal data → Summary

**Form fields**: legalAreas (checkboxes: Privat/Beruf/Verkehr/Miete), coverageAmount (slider), plan, salutation, firstName, lastName, street, zip, city, occupation

---

## 7. Unfallversicherung (Accident Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | unfall |
| **Category** | person |
| **Insured event** | accident causing permanent disability |
| **Age range** | 1–75 (covers children too) |
| **Coverage** | €25.000–€500.000 Invaliditätssumme, step €25.000, default €100.000 |
| **Coverage unit** | per €25.000 |
| **Risk class** | Occupation: Büro (1.0), Handwerk (1.3), Risikobehaftet (1.7) |
| **Payment duration** | Annual renewal |
| **Waiting period** | None |

**Base rates** (per €25k/month): Grundschutz €1.80, Komfort €2.50, Premium €3.40
**Age curve**: base=0.85, linear=0.10, quadratic=0.15 (moderate increase)
**Loading**: 22%

**Tiers**:
- **Grundschutz**: Invaliditätsleistung mit Grundsumme, Todesfallleistung €10.000
- **Komfort**: + progressive Invaliditätsleistung (225%), Krankenhaustagegeld €25/Tag, Bergungskosten
- **Premium**: + Progression 350%, Krankenhaustagegeld €50/Tag, Kosmetische Operationen, Knochenbruch-Sofortleistung

**Wizard steps**: Birth date → Occupation → Coverage amount → Plan selection → Personal data → Summary

---

## 8. Risikolebensversicherung (Term Life)

| Parameter | Value |
|-----------|-------|
| **ID** | risikoleben |
| **Category** | person |
| **Insured event** | death during policy term |
| **Age range** | 18–65 |
| **Coverage** | €25.000–€1.000.000, step €25.000, default €200.000 |
| **Coverage unit** | per €25.000 |
| **Risk class** | Smoker: Nichtraucher (1.0), Raucher (1.80) |
| **Payment duration** | Fixed term: 10, 15, 20, 25, or 30 years |
| **Waiting period** | None (but health check for >€300k) |

**Base rates** (per €25k/month): Grundschutz €1.71, Komfort €2.08, Premium €2.56
**Age curve**: base=0.40, linear=0.20, quadratic=0.80 (exponential after 50)
**Loading**: 25%
**Calibration**: 35yo non-smoker, €200k, Komfort → ~€12/month ✓

**Tiers**:
- **Grundschutz**: Todesfallschutz, konstante Summe
- **Komfort**: + Nachversicherungsgarantie (bei Heirat, Geburt, Hauskauf), vorgezogene Leistung bei terminaler Krankheit
- **Premium**: + fallende + konstante Summe wählbar, Dynamik, Beitragsbefreiung bei BU, weltweiter Schutz

**Wizard steps**: Birth date → Smoker status → Coverage amount → Policy term → Plan selection → Personal data → Summary

**Form fields**: birthDate, smokerStatus (inline-radio: Nichtraucher/Gelegenheitsraucher/Raucher), coverageAmount (slider), policyTerm (segmented: 10/15/20/25/30 Jahre), plan, salutation, firstName, lastName, street, zip, city, beneficiary (text)

---

## 9. Pflegezusatzversicherung (Long-Term Care Supplementary)

| Parameter | Value |
|-----------|-------|
| **ID** | pflegezusatz |
| **Category** | person |
| **Insured event** | need for long-term care (Pflegegrad 1-5) |
| **Age range** | 20–65 |
| **Coverage** | €250–€3.000/month Pflegegeld, step €250, default €1.000 |
| **Coverage unit** | per €250/month |
| **Risk class** | None |
| **Payment duration** | 67 − age |
| **Waiting period** | Grundschutz: 5 years (!), Komfort: 3 years, Premium: 1 year |

**Base rates** (per €250/month): Grundschutz €4.50, Komfort €6.20, Premium €8.80
**Age curve**: base=0.50, linear=0.25, quadratic=0.65 (steep growth — care risk rises sharply)
**Loading**: 25%

**Tiers**:
- **Grundschutz**: Pflegegeld ab Pflegegrad 2, 5 years waiting, nur stationäre Pflege
- **Komfort**: Ab Pflegegrad 1, 3 years waiting, ambulant + stationär, Einmalzahlung bei Pflegegrad 4-5
- **Premium**: Ab Pflegegrad 1, 1 year waiting, ambulant + stationär + häuslich, Assistance-Leistungen, dynamische Anpassung

**Wizard steps**: Birth date → Health status → Coverage amount → Plan selection → Personal data → Summary

---

## 10. Tierkrankenversicherung (Pet Health)

| Parameter | Value |
|-----------|-------|
| **ID** | tierkranken |
| **Category** | animal |
| **Insured event** | veterinary treatment for illness/accident |
| **Age range** | 0–10 (pet age in years) |
| **Coverage** | €1.000–€20.000/year vet budget, step €1.000, default €5.000 |
| **Coverage unit** | per €1.000/year |
| **Risk class** | Species: Hund (1.0), Katze (0.75), Pferd (2.50) |
| **Payment duration** | Ongoing |
| **Waiting period** | Grundschutz: 3 months, Komfort: 1 month, Premium: none |

**Base rates** (per €1k/year): Grundschutz €6.62, Komfort €8.07, Premium €9.93
**Age curve**: base=0.60, linear=0.10, quadratic=0.90 (steep increase after age 7-8)
**Loading**: 22%
**Calibration**: Dog age 3, €5k budget, Komfort → ~€35/month ✓

**Tiers**:
- **Grundschutz**: OP-Schutz only, 3-month waiting, SB 20%, bis 2× GOT
- **Komfort**: Krankenvollschutz, 1-month waiting, SB 10%, bis 3× GOT, Impfungen
- **Premium**: Krankenvollschutz, no waiting, SB 0%, bis 4× GOT, Kastration, Zahnpflege, Auslandsschutz

**Wizard steps**: Animal type → Pet details (name, breed, age) → Coverage budget → Plan selection → Owner data → Summary

**Form fields**: animalType (segmented: Hund/Katze), petName (text), breed (select), petAge (number), chipNumber (text, optional), coverageAmount (slider), plan, salutation, firstName, lastName, street, zip, city

**Note**: Age range label is "Alter des Tieres", not "Eintrittsalter". Age validation: pet must be under 10 for new policies.

---

## 11. Reiseversicherung (Travel Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | reise |
| **Category** | travel |
| **Insured event** | trip cancellation, medical emergencies abroad, luggage loss |
| **Age range** | 0–85 |
| **Coverage** | €2.000–€30.000 trip cost, step €1.000, default €5.000 |
| **Coverage unit** | per €1.000 trip cost |
| **Risk class** | Destination: Europa (1.0), Weltweit (1.40) |
| **Payment duration** | Per trip or annual flat rate |
| **Waiting period** | None |

**Base rates** (per €1k trip cost): Grundschutz €1.50, Komfort €2.80, Premium €4.20
**Age curve**: base=0.75, linear=0.10, quadratic=0.30 (U-shape: young adventurers + elderly)
**Loading**: 20%

**Tiers**:
- **Grundschutz**: Reiserücktritt only, SB €100
- **Komfort**: + Reiseabbruch, Reisegepäck bis €2.000, SB €50
- **Premium**: + Auslandskranken, Mietwagenschutz, 24/7-Assistance, SB €0

**Wizard steps**: Destination → Trip details → Coverage → Plan selection → Traveler data → Summary

---

## 12. Wohngebäudeversicherung (Building Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | wohngebaeude |
| **Category** | property |
| **Insured event** | damage to the building structure (fire, storm, water, natural hazards) |
| **Age range** | 18–99 |
| **Coverage** | €100.000–€1.000.000 Gebäudewert, step €50.000, default €350.000 |
| **Coverage unit** | per €50.000 |
| **Risk class** | Building type: Massiv (0.85), Fertighaus (1.0), Holz/Fachwerk (1.35) |
| **Payment duration** | Annual renewal |
| **Waiting period** | None |

**Base rates** (per €50k/month): Grundschutz €1.20, Komfort €1.85, Premium €2.60
**Age curve**: base=1.0, linear=0.0, quadratic=0.0 (flat)
**Loading**: 22%

**Tiers**:
- **Grundschutz**: Feuer, Leitungswasser, Sturm/Hagel, SB €1.000
- **Komfort**: + Elementarschäden (Hochwasser, Erdbeben), Aufräumkosten, SB €500
- **Premium**: + Photovoltaik, Smarthome, grobe Fahrlässigkeit, Mietausfall 24 Monate, SB €0

**Wizard steps**: Property address → Building details → Coverage → Plan selection → Owner data → Summary

---

## 13. Kfz-Versicherung (Motor Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | kfz |
| **Category** | property |
| **Insured event** | vehicle damage, liability, theft |
| **Age range** | 18–99 |
| **Coverage** | Haftpflicht (mandatory) + Teilkasko/Vollkasko optional |
| **Coverage unit** | flat rate per vehicle class |
| **Risk class** | Typklasse (vehicle model group, 1-35) + Schadenfreiheitsklasse (SF 0-35) |
| **Payment duration** | Annual renewal |
| **Waiting period** | None |

**Base rates** (flat/month, coverageUnit=1 so units=1): Grundschutz €28.77, Komfort €35.08, Premium €43.15
**Age curve**: base=1.80, linear=−1.20, quadratic=0.50 (high for young drivers, drops, slight rise for elderly)
**Loading**: 18%
**Calibration**: 35yo, midsize, SF 10 (1.0×), Komfort → ~€65/month ✓

**Tiers**:
- **Grundschutz**: Kfz-Haftpflicht only (gesetzlich vorgeschrieben), €100M Deckung
- **Komfort**: + Teilkasko (Diebstahl, Glasbruch, Wildschaden, Hagel), SB €150
- **Premium**: + Vollkasko (Eigenschaden, Vandalismus), Schutzbrief, Neuwertentschädigung 24 Monate, SB €0

**Wizard steps**: Vehicle details → Driver info → SF-Klasse → Plan selection → Personal data → Summary

**Form fields**: licensePlate (text), vehicleType (select), yearBuilt (number), annualMileage (select: <5k/5-10k/10-20k/>20k km), sfClass (slider 0-35), birthDate, driverAge (auto-calculated), plan, salutation, firstName, lastName, street, zip, city

---

## 14. Cyberversicherung (Cyber Risk — for individuals)

| Parameter | Value |
|-----------|-------|
| **ID** | cyber |
| **Category** | liability |
| **Insured event** | identity theft, online fraud, data loss, cyberbullying |
| **Age range** | 18–75 |
| **Coverage** | €10.000–€100.000, step €10.000, default €25.000 |
| **Coverage unit** | per €10.000 |
| **Risk class** | None |
| **Payment duration** | Annual renewal |
| **Waiting period** | None |

**Base rates** (flat/month, coverageUnit=defaultCoverage so units=1): Grundschutz €1.50, Komfort €2.80, Premium €4.50
**Age curve**: base=1.0, linear=0.0, quadratic=0.0 (flat — cyber risk is age-independent)
**Loading**: 20%

**Tiers**:
- **Grundschutz**: Identitätsdiebstahl bis €10k, Phishing-Schutz, Datenrettung
- **Komfort**: + Onlinekauf-Schutz, Cybermobbing, Rechtsberatung digital, Kreditkartenschutz
- **Premium**: + Dark-Web-Monitoring, Reputationsschutz, psychologische Beratung, Lösegeldzahlung

**Wizard steps**: Digital profile → Coverage → Plan selection → Personal data → Summary

---

## 15. Krankentagegeldversicherung (Daily Sickness Allowance)

| Parameter | Value |
|-----------|-------|
| **ID** | krankentagegeld |
| **Category** | person |
| **Insured event** | income loss during illness (beyond employer continuation) |
| **Age range** | 18–60 |
| **Coverage** | €10–€200/day, step €10, default €75 |
| **Coverage unit** | per €10/day |
| **Risk class** | Employment: Angestellt (1.0), Selbstständig (1.30) |
| **Payment duration** | 67 − age |
| **Waiting period** | Angestellt: ab Tag 43 (after Lohnfortzahlung), Selbstständig: ab Tag 15 or 22 |

**Base rates** (per €10/day/month): Grundschutz €2.20, Komfort €3.10, Premium €4.30
**Age curve**: base=0.70, linear=0.35, quadratic=0.20 (steady increase)
**Loading**: 25%

**Tiers**:
- **Grundschutz**: Tagegeld ab 43. Tag, begrenzt auf 78 Wochen
- **Komfort**: Ab 43. Tag, unbegrenzt, Nachversicherungsgarantie
- **Premium**: Ab 22. Tag, unbegrenzt, Beitragsrückgewähr bei Leistungsfreiheit, Optionstarif

**Wizard steps**: Employment type → Income → Waiting period → Coverage/day → Plan selection → Personal data → Summary
