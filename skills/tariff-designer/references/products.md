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
| **Coverage** | €1.000–€20.000, step €500, default €7.000 |
| **Coverage unit** | per €1.000 |
| **Risk class** | None (age only) |
| **Payment duration** | 90 − age (min 5, max 46 years) |
| **Waiting period** | Grundschutz: 36 months (Aufbauzeit), Komfort: 18 months, Premium: 18 months |

**Base rates** (per €1k/month, age-dependent — see lookup table):

| Age | Grundschutz | Komfort | Premium |
|-----|-------------|---------|---------|
| 40 | €3.12 | €3.19 | €3.65 |
| 45 | €3.44 | €3.51 | €4.01 |
| 50 | €3.90 | €3.99 | €4.56 |
| 55 | €4.49 | €4.62 | €5.29 |
| 60 | €5.27 | €5.45 | €6.24 |
| 65 | €6.34 | €6.60 | €7.56 |
| 70 | €7.94 | €8.36 | €9.58 |
| 75 | €10.59 | €11.40 | €13.09 |
| 80 | €15.36 | €16.99 | €19.49 |
| 85 | N/A | €29.04 | €33.08 |

**Age curve** (cubic, better fit than quadratic): base=1.0, linear=−1.62, quadratic=5.47 (quadratic R²=0.978, cubic R²=0.997 for Grundschutz)
**Coverage scaling**: Linear with small fixed fee (~€1.80/month) — price = rate_per_1k × (coverage/1000) + 1.80
**Loading**: Built into base rates (no separate loading factor needed)
**Calibration**: 44yo, €8k, Komfort → €27.45/month ✓

**Note — Age-dependent tier multipliers**: Tier ratios are NOT constant. Komfort/Grundschutz ranges from 1.02× (age 40) to 1.11× (age 80). Premium/Grundschutz ranges from 1.17× (age 40) to 1.27× (age 80). For demo purposes, using the lookup table above is more accurate than applying fixed multipliers.

**Payment mode discounts**: Monthly 0%, Quarterly 0.4%, Semi-annual 1.0%, Annual 3.4%

**Tiers**:
- **Grundschutz**: Guaranteed death benefit, Aufbauzeit 36 Monate, surplus participation, Flex-Option nachträglich wählbar
- **Komfort**: Same + Aufbauzeit 18 Monate, Doppelte Leistung bei Unfalltod, Vorsorge-Ordner, kostenlose Rechtsberatung
- **Premium**: Same + Aufbauzeit 18 Monate, vorgezogene Leistung bei schwerer Krankheit, Leistung bei Pflegebedürftigkeit, Best Doctors, Bestattungspakete bis 20% günstiger, digitaler Nachlass-Verwalter, coverage >€15k

**Wizard steps**: Birth date → Insurance start → Coverage slider → Plan selection (with payment mode, coverage, and payment duration adjustable on same page) → Personal data → Summary

**Form fields**: birthDate (spinbutton: Tag/Monat/Jahr), insuranceStart (3 radio options: 1st of next 3 months), coverageAmount (slider+textbox, €1k-€20k, step €500), plan (tabs: Grundschutz/Komfort/Premium), zahlweise (dropdown: monatlich/vierteljährlich/halbjährlich/jährlich), beitragszahlungsdauer (dropdown: 5 to 90−age years), salutation, firstName, lastName, street, zip, city

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/sterbegeld/screenshots/, research/sterbegeld/price-matrix.json
**Confidence**: HIGH (160 data points, cubic R²=0.990-0.997)
**Discrepancies from previous entry**: Payment duration 90−age (was 85−age). Coverage step €500 (was €1.000), default €7.000 (was €8.000). Aufbauzeit differs by tier (36mo Grund vs 18mo Komfort/Premium, was 18/18/3). Base rates are age-dependent lookup table (was single rate). Calibration €27.45 (was ~€30). Fixed fee component ~€1.80/month discovered.

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
| **Age range** | 0–75 |
| **Coverage** | Reimbursement percentage: 75% / 90% / 100% (determined by tariff, not user-selectable) |
| **Coverage unit** | flat rate (coverageUnit=defaultCoverage so units=1) |
| **Risk class** | None (age-band pricing only) |
| **Payment duration** | Ongoing (no end date, cancel anytime) |
| **Waiting period** | None (all tariffs) |

**Base rates** (flat/month, coverageUnit=defaultCoverage so units=1): Grundschutz €14.26, Komfort €17.79, Premium €22.62
**Age curve**: base=0.13, linear=3.08, quadratic=-0.52 (steep near-linear increase; ERGO uses discrete age bands — see note)
**Loading**: 22%
**Calibration**: 35yo, Komfort → ~€21.70/month ✓

**Note — Age bands**: ERGO uses discrete age bands, not a smooth curve. Actual ERGO band prices (Komfort/DS90): 0–20: €3.70, 21–25: €7.20, 26–30: €13.80, 31–40: €21.70, 41–50: €32.50, 51+: €44.40. First 6 months at 50% premium (Startbeitrag).

**Tiers**:
- **Grundschutz** (Dental-Schutz 75): 75% Erstattung für Zahnersatz, Inlays, Implantate. Professionelle Zahnreinigung 1×/Jahr. Leistungsbegrenzung Y1-4. GOZ bis 3,5-fach
- **Komfort** (Dental-Schutz 90): 90% Erstattung für Zahnersatz, Inlays, Implantate. Professionelle Zahnreinigung 1×/Jahr. Leistungsbegrenzung Y1-4. GOZ bis 3,5-fach
- **Premium** (Dental-Schutz 100): 100% Erstattung für Zahnersatz, Inlays, Implantate, KFO für Kinder (bis €1.000). Professionelle Zahnreinigung. GOZ bis 5,0-fach. Fahrkostenpauschale €50 nach Narkose

**Wizard steps**: Who to insure → Birth date → Start date (price shown) → Plan comparison → Personal data → Summary

**Form fields**: insurerType (radio: Ich / Ich und jemand anders / Nur jemand anders), birthDate (spinbutton: Tag/Monat/Jahr), insuranceStart (radio: 1st of next 3 months), plan (tabs: Dental-Schutz [X] / Dental-Vorsorge + Dental-Schutz [X]), salutation, firstName, lastName, street, zip, city

**Validation**: Birth date required

**Source**: ergo.de — researched 2026-04-12
**Evidence**: research/zahnzusatz/screenshots/, research/zahnzusatz/price-matrix.json
**Confidence**: HIGH
**Discrepancies from previous entry**: Coverage model changed from per-unit to flat rate. Coverage slider removed. Age range 0–75. Base rates changed. Age curve now steep (0.13/3.08/−0.52). No waiting period. dentalStatus/missingTeeth fields removed. Tiers are reimbursement %-based (DS75/DS90/DS100).

---

## 4. Hausratversicherung (Household Contents)

| Parameter | Value |
|-----------|-------|
| **ID** | hausrat |
| **Category** | property |
| **Insured event** | damage/loss of household contents (fire, water, storm, theft) |
| **Age range** | 18–99 (binary: under-36 gets 13% Startbonus) |
| **Coverage** | Derived from m²: 650 EUR/m², range 10–384 m² (€6.500–€249.600) |
| **Coverage unit** | per m² (NOT per €5k) |
| **Risk class** | ZIP-code specific (not zone-based). Sampled range: 0.77× (Trier) to 1.37× (Hamburg/Berlin) |
| **Payment duration** | 1 year or 3 years (3yr = ~10% discount) |
| **Waiting period** | None |

**Note — Only 2 tiers**: ERGO Hausrat has 2 tiers (Smart/Best), NOT 3. No Premium equivalent exists.

**Pricing model: Linear per-m² with ADDITIVE tier difference** (NOT multiplicative):
```
Smart_monthly = (0.1114 × m² + 0.254) × regionMult × floorMult × buildingMult × ageFactor
Best_monthly  = (0.1114 × m² + 3.642) × regionMult × floorMult × buildingMult × ageFactor
```

Tier difference is a fixed ~€3.39/month (additive), not a percentage multiplier.

**Regional multipliers** (sampled, München=reference):

| City | ZIP | Multiplier |
|------|-----|-----------|
| Trier | 54290 | 0.77× |
| Nürnberg | 90402 | 0.79× |
| Dresden | 01067 | 0.97× |
| München | 80331 | 1.00× |
| Kiel | 24103 | 1.08× |
| Köln | 50667 | 1.31× |
| Hamburg | 20095 | 1.37× |
| Berlin | 10117 | 1.37× |

**Floor factor** (MFH only): Keller/EG = 1.10×, 1.OG+ = 1.00×
**Building type**: EFH = 1.06×, MFH = 1.00×
**Age factor**: Under 36 = 0.87× (13% Startbonus), 36+ = 1.00×
**Deductible**: None = 1.00×, €300 = 0.93×
**Contract duration**: 1yr = 1.11×, 3yr = 1.00×
**Payment mode**: Monthly = 1.00×, Annual = 0.94×

**Calibration**: 80m², München, MFH 2.OG, age 36+, no SB, 3yr, monthly → Smart €9.01, Best €12.40 ✓

**Tiers** (ERGO names: Smart / Best):
- **Smart** (→ grundschutz): Leistungsstarke Absicherung, Feuer/Wasser/Sturm/Einbruch, optional Diebstahl €10k
- **Best** (→ komfort): Topschutz, grobe Fahrlässigkeit 100%, einfacher Diebstahl €10k inkl., Bestseller

**Add-on modules** (separate pricing, not included in base tiers):
- Haus- und Wohnungsschutzbrief (~€1.71/month)
- Glasversicherung (~€2.52/month for 48m²)
- Weitere Naturgefahren/Elementar (~€1.12/month for 48m²)
- Unbenannte Gefahren (~€5.82/month, requires Naturgefahren)
- Fahrrad- und E-Bike-Schutz (from €1.85/month)

**Wizard steps**: Building type (MFH/EFH) → Floor (MFH only, 5 options) → Living space (m²) → Address (street+nr+ZIP+city, validated) → Insurance start → Birth date → Plan selection (Smart/Best, with add-ons, SB, payment mode, contract duration on same page)

**Form fields**: buildingType (radio: Wohnung in MFH/In einem EFH), floor (radio: Keller/EG/1.OG/2.OG/3.OG+, MFH only), livingSpace (number, m²), street (text, validated), houseNumber (text), zip (text), city (auto-populated), insuranceStart (radio: Morgen/Nächsten Monat/Anderes Datum), birthDate (spinbutton: Tag/Monat/Jahr), plan (tabs: Smart/Best), selbstbeteiligung (dropdown: Keine/€300/€300 Flexi-SB), zahlweise (dropdown), vertragslaufzeit (dropdown: 1/3 Jahre), addOns (checkboxes: Glasversicherung/Naturgefahren/Unbenannte Gefahren/Fahrradschutz/Wohnungsschutzbrief)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/hausrat/screenshots/, research/hausrat/price-matrix.json
**Confidence**: HIGH (23 data points, coverage linearity R²=0.998)
**Discrepancies from previous entry**: Only 2 tiers (was 3). Coverage from m² (was user-entered €10k-€150k). Tier model additive (was multiplicative). ZIP-specific pricing (was 4 broad zones). Age is binary under-36 discount (was flat). Floor and building type affect pricing (not modeled before). Deductible, contract duration, and add-on modules discovered. Street-level address validation required.

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
| **Coverage** | €50.000–€500.000, free-form with slider, default €150.000 |
| **Coverage unit** | per €1.000 (near-linear with small fixed base fee ~€0.91) |
| **Risk class** | Smoker: Nichtraucher 10+ (1.0), Nichtraucher 1+ (~1.17), Raucher (1.87–3.92×, age-dependent) |
| **Payment duration** | 1–50 years continuous slider, default 20 |
| **Waiting period** | None |

**Pricing model: Lookup table** (age curve too steep for polynomial — quadratic R²=0.958, cubic R²=0.995)

**Reference prices (€200k, 20yr, Nichtraucher 10+, monthly):**

| Age | Grundschutz | Komfort | Premium |
|-----|-------------|---------|---------|
| 25 | €3.94 | €4.97 | €7.50 |
| 30 | €5.15 | €6.51 | €9.54 |
| 35 | €7.54 | €9.54 | €13.54 |
| 40 | €12.16 | €15.42 | €21.30 |
| 45 | €20.32 | €25.82 | €35.02 |
| 50 | €34.34 | €43.65 | €58.53 |
| 55 | €60.94 | €77.48 | €103.11 |
| 60 | €121.61 | €154.68 | €204.46 |

**Smoker multipliers** (age-dependent, applied to Nichtraucher 10+ base):

| Age | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|-----|----|----|----|----|----|----|----|----|
| Raucher/NS10+ | 1.87× | 2.23× | 2.65× | 3.02× | 3.46× | 3.92× | 3.83× | 3.19× |

**Nichtraucher 1+ multiplier**: ~1.17× (slightly age-dependent, 1.13-1.24)

**Tier ratios** (stable across ages): Komfort/Grundschutz ~1.27×, Premium/Grundschutz ~1.70-1.90× (decreases with age)

**Term scaling** (relative to 20yr at age 35, Komfort): 10yr=0.63×, 15yr=0.77×, 20yr=1.00×, 25yr=1.38×, 30yr=1.95×

**Coverage scaling**: Near-linear. price ≈ fixedFee + rate × coverage. Simpler: scale linearly from 200k reference, accept ~5% error.

**Loading**: Built into base rates
**Calibration**: 35yo Nichtraucher 10+, €200k, 20yr, Komfort → €9.54/month ✓

**Tiers**:
- **Grundschutz**: Todesfallschutz, konstante Summe, vorläufiger Versicherungsschutz, Nachversicherungsgarantie (basic)
- **Komfort**: + erweiterte Nachversicherungsgarantie, vorübergehende Erhöhung, Soforthilfe bei Tod (default selection)
- **Premium**: + Waisenschutz (€250/Monat pro Kind), Pflegebonus, Verlängerungsoption

**Optional add-ons**: Dread Disease (critical illness benefit), Sicherheit Plus (guaranteed level premiums), Beitragsdynamik (3% annual dynamic increase)

**Wizard steps**: Versicherte Person (Ich/Jemand anders) → Birth date → Absicherungsform (konstant/fallend) → Coverage amount → Policy term → Berufliche Situation (employment+occupation) → Smoker status (3 options) → Insurance start → Plan selection (with adjustable coverage/term on same page) → Personal data → Summary

**Form fields**: versichertePerson (radio: Mich selbst/Jemand anders), birthDate (spinbutton: Tag/Monat/Jahr), absicherungsform (radio: Familien-Partnerabsicherung/Kredit-Darlehensabsicherung), coverageAmount (combobox+slider, €50k-€500k), policyTerm (combobox+slider, 1-50 years), beschaeftigungsverhaeltnis (dropdown: 12 options), ausgeuebterBeruf (autocomplete combobox), smokerStatus (radio: Nichtraucher 10+/Nichtraucher 1+/Raucher), insuranceStart (radio: 3 dates), plan (radio: Grundschutz/Komfort/Premium), dreadDisease (checkbox), sicherheitPlus (checkbox), beitragsdynamik (checkbox), zahlweise (dropdown), salutation, firstName, lastName, street, zip, city

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/risikoleben/screenshots/, research/risikoleben/price-matrix.json
**Confidence**: HIGH (75 data points, verified against ERGO website examples)
**Discrepancies from previous entry**: Coverage €50k-€500k (was €25k-€1M). Term 1-50 continuous (was fixed 10/15/20/25/30). 3 smoker classes (was 2). Smoker multiplier age-dependent 1.87-3.92× (was fixed 1.80×). Calibration €9.54 (was ~€12, off by 20%). Age curve exponential (quadratic inadequate). Employment type + occupation fields added. Absicherungsform (constant/falling) added. Add-ons (Dread Disease, Sicherheit Plus, Beitragsdynamik) discovered.

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
