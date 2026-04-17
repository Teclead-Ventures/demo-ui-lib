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
| **Payment duration** | 90 − age (min 5 years; at age 40 = 50 years, at age 85 = 5 years) |
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

**Pricing model: Lookup table** (Template B — age-dependent tier multipliers make polynomial insufficient)
**Age curve approximation** (for reference only, do NOT use for TypeScript): base=1.0, linear=−1.62, quadratic=5.47 (R²=0.978). Cubic R²=0.997. Use the lookup table above for implementation.
**Coverage scaling**: Linear with fixed fee (~€1.80/month) — price = rate_per_1k × (coverage/1000) + 1.80
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

**Note — Age bands**: ERGO uses discrete age bands, not a smooth curve. Actual ERGO band prices (Komfort/DS90): 0–20: €3.70, 21–25: €7.20, 26–30: €13.80, 31–40: €21.70, 41–50: €32.50, 51+: €44.40. First 6 months at 50% premium (Startbeitrag). Note: last band is open-ended ("51+") — upper age limit of 75 is approximate and needs confirmation in a future research run.

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
| **Age range** | 18+ (binary: under-36 gets 13% Startbonus) |
| **Coverage** | Fixed by tier: Smart = €10M, Best = €50M. No user-selectable coverage. |
| **Coverage unit** | flat rate (no user-selectable coverage; Smart=€10M cap, Best=€50M) |
| **Risk class** | None (family status affects base rate directly, not as uniform multiplier) |
| **Payment duration** | 1 year or 3 years (3yr = ~10% discount) |
| **Waiting period** | None |

**Note — Only 2 tiers**: ERGO Haftpflicht has 2 tiers (Smart/Best), NOT 3.

**Pricing model: Template D** (flat-rate additive configurator — no age curve, no coverage slider, additive Baustein modules)

**Base rates** (monthly, 3yr contract, ohne SB, age ≥36):

| Family Status | Smart | Best |
|---------------|-------|------|
| Single | €6.05 | €10.58 |
| Paar / Alleinerziehend | €7.56 | €12.09 |
| Familie | €9.07 | €13.60 |

**Family status multipliers** (tier-dependent, NOT uniform):
- Single: 1.0 (both tiers)
- Paar/Alleinerziehend: Smart ×1.25, Best ×1.14
- Familie: Smart ×1.50, Best ×1.29

**Baustein base rates** (additive, monthly, Single/Smart reference):

| Baustein | Smart | Best | Default |
|----------|-------|------|---------|
| Schlüsselverlust | +€1.21 | included | Best: on, Smart: off |
| Neuwertentschädigung | +€1.21 | included | Best: on, Smart: off |
| Forderungsausfall | +€1.21 | included | Best: on, Smart: off |
| Amts- und Diensthaftpflicht | +€1.93 | +€1.94 | off |
| Alleinstehende Familienangehörige | +€0.00 | +€0.00 | off (free) |

**Age curve**: NONE. Binary band: under 36 = ×0.87 (13% Startbonus), 36+ = ×1.0
**SB discount**: ohne = ×1.0, €150 SB = Smart ×0.80 / Best ×0.869
**Contract duration**: 3yr = ×1.0 (base), 1yr = ×1.111 (+11.1%)
**Payment mode**: jährlich = ×1.0, halbjährlich = ×1.03, vierteljährlich = ×1.05, monatlich = ×1.06
**Loading**: Built into base rates
**Calibration**: Single, Smart, 3yr, ohne SB, monatlich, age ≥36 → €6.05/month ✓
**Calibration**: Single, Best, 3yr, ohne SB, monatlich, age <36 → Startbonus advertised "ab €5.26" ✓

**Tiers** (ERGO names: Smart / Best):
- **Smart** (→ grundschutz): Versicherungssumme €10M, Personenschäden, Sachschäden, Vermögensschäden, Mietsachschäden, stärkere Rückstufung im Schadenfall
- **Best** (→ komfort): Versicherungssumme €50M, + Schlüsselverlust, Neuwertentschädigung, Forderungsausfalldeckung inkl., normale Rückstufung, Internetschäden, Drohnen, Ehrenamt, weltweiter Schutz

**Wizard steps**: Lebenssituation (Single/Alleinerziehend/Paar/Familie) → Versicherungsbeginn → Geburtsdatum → Beitrag/Configurator (tier tabs, Bausteine toggles, SB, Laufzeit, Zahlweise)

**Form fields**: familyStatus (radio tiles: Single/Alleinerziehend/Paar/Familie), insuranceStart (radio: Morgen/Nächsten Monat/Anderes Datum), birthDate (spinbutton: Tag/Monat/Jahr), plan (tabs: Smart/Best), bausteine (checkboxes: Schlüsselverlust/Neuwertentschädigung/Forderungsausfall/Amts-Diensthaftpflicht/Alleinstehende Familienangehörige), selbstbeteiligung (dropdown: ohne/€150), vertragslaufzeit (dropdown: 1/3 Jahre), zahlweise (dropdown: monatlich/vierteljährlich/halbjährlich/jährlich)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/haftpflicht/screenshots/, research/haftpflicht/price-matrix.json
**Confidence**: HIGH (32 data points, Baustein additivity verified <€0.02 error)
**Discrepancies from previous entry**: Only 2 tiers (was 3). Coverage fixed by tier (was €1M-€50M slider). Template D not A. Family multipliers tier-dependent (was uniform 1.0/1.35/1.20). Binary age band <36 (was flat). 5 additive Bausteine (not modeled before). SB and contract duration factors discovered.

---

## 6. Rechtsschutzversicherung (Legal Protection)

| Parameter | Value |
|-----------|-------|
| **ID** | rechtsschutz |
| **Category** | liability |
| **Insured event** | legal disputes (lawyer fees, court costs) |
| **Age range** | 18+ (no upper limit; under-25 gets 10% Startbonus) |
| **Coverage** | Fixed by tier: Smart = €2M, Best = unlimited. No user-selectable coverage. |
| **Coverage unit** | flat rate (no user-selectable coverage; Smart=€2M cap, Best=unlimited) |
| **Risk class** | None |
| **Payment duration** | 1 year or 3 years (3yr = 10% Dauernachlass) |
| **Waiting period** | None |

**Note — Only 2 tiers**: ERGO Rechtsschutz has 2 tiers (Smart/Best), NOT 3.

**Note — Additive Bausteine**: Pricing is based on toggling legal area modules (Bausteine), NOT a coverage amount. Each Baustein has its own price and they sum additively (verified with 0.00 error). For the demo, simplify by including legal areas in the tier description rather than exposing individual toggles.

**Pricing model: Template D** (flat-rate additive configurator — no age curve, no coverage slider)

**Baustein base rates** (Single, SB €150, monthly):

| Baustein | Smart | Best |
|----------|-------|------|
| Privat | €16.71 | €24.84 |
| Beruf (add-on) | +€7.83 | +€9.10 |
| Wohnen (add-on) | +€1.31 | +€1.83 |
| Verkehr (add-on) | +€8.30 | +€14.59 |
| **All 4 Bausteine** | **€34.15** | **€50.36** |

**Pricing formula**: `monthlyPremium = bausteinSum × familyMult × sbDiscount × contractDiscount × youthDiscount`
- familyMultiplier: Single/Alleinerziehend = 1.0, Paar/Familie = ~1.12
- sbDiscount: SB €150 = 1.0, SB €250 = 0.911, SB €500 = 0.779
- contractDiscount: 1yr = 1.0, 3yr = 0.90
- youthDiscount: under 25 = 0.90, 25+ = 1.0

**Age curve**: NONE. Flat rate. base=1.0, linear=0.0, quadratic=0.0
**Loading**: Built into base rates
**Calibration**: Single, all 4 Bausteine, Smart, SB €150, monthly → €34.15 ✓

**Tiers** (ERGO names: Smart / Best):
- **Smart** (→ grundschutz): Deckungssumme €2M, SB-Optionen €150/€250/€500, Privat-Baustein Pflicht
- **Best** (→ komfort): Deckungssumme unbegrenzt, SB-Optionen €150/€250/€500, Privat-Baustein Pflicht, erweiterte Leistungen

**Wizard steps**: Family status → Birth date → Employment status → Employment type → Baustein/tier selection (configurator page with toggles, SB, contract duration, payment mode) → Personal data → Summary

**Form fields**: familyStatus (radio: Single/Alleinerziehend/Paar/Familie), birthDate (spinbutton: Tag/Monat/Jahr), isEmployed (radio: Ja/Nein), employmentType (dropdown, if employed), plan (tabs: Smart/Best), bausteine (toggles: Privat/Beruf/Wohnen/Verkehr), selbstbeteiligung (dropdown: €150/€250/€500), vertragslaufzeit (dropdown: 1/3 Jahre), zahlweise (dropdown), salutation, firstName, lastName, street, zip, city

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/rechtsschutz/screenshots/, research/rechtsschutz/price-matrix.json
**Confidence**: HIGH (42 data points, Baustein additivity verified with 0.00 error)
**Discrepancies from previous entry**: No age-based pricing (was quadratic). No coverage slider (was €100k-€1M). Only 2 tiers (was 3). Additive Baustein model (was fixed tier pricing). No waiting period (was 3 months). Family status and SB affect pricing (not modeled before).

---

## 7. Unfallversicherung (Accident Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | unfall |
| **Category** | person |
| **Insured event** | accident causing permanent disability |
| **Age range** | 18–75 |
| **Coverage** | €10.000–€300.000 Invaliditätssumme, step €5.000, default €50.000 |
| **Coverage unit** | per €10.000 |
| **Risk class** | Occupation (autocomplete): Gruppe A/Büro (1.0), Gruppe B/Handwerk (1.55), Gruppe C/Erhöhtes Risiko (3.10) |
| **Payment duration** | Annual renewal (1-4 year contracts; Smart/Best get discounts for 3+ years) |
| **Waiting period** | None |

**Note — ERGO tier names**: Basic / Smart / Best (not Grundschutz/Komfort/Premium). Keep ERGO's names.

**Base rates** (per €10k/month, Gruppe A, under-65): Basic €0.754, Smart €1.524, Best €1.954
**Age curve**: Step function — NOT polynomial. 2 discrete bands:
- Age 18-64: multiplier = 1.0
- Age 65-75: multiplier = 2.0 (exact doubling)

**Coverage scaling**: Perfectly linear (R²=1.0, no fixed fee)
**Tier ratios**: Smart = 2.02× Basic, Best = 2.54× Basic (constant across ages)
**Occupation multipliers**: Gruppe A = 1.0, Gruppe B = 1.55, Gruppe C = 3.10 (constant across ages, verified)
**Loading**: Built into base rates
**Calibration**: 36yo, Bürokaufmann (A), €50k, Smart → €7.62/month ✓ (1.524 × 5 × 1.0 × 1.0)

**Pricing formula**: `price = baseRate × (coverage/10000) × ageBandMult × occupationMult`

**Tiers** (ERGO names: Basic / Smart / Best):
- **Basic**: Invaliditätsleistung mit Progression 300%, nur 1-Jahres-Vertrag
- **Smart**: Progression 300%, erweiterter Schutz, 1-4 Jahre Vertrag (Rabatt ab 3 Jahre)
- **Best**: Progression 600%, Topschutz, 1-4 Jahre Vertrag (Rabatt ab 3 Jahre)

**Optional add-ons** (separate pricing): Unfall-Rente, Unfall-Hilfe, Verletzungsgeld, Krankenhaus-Tagegeld, Todesfallleistung, Unfall-Pflege, Gliedertaxe Plus

**Wizard steps**: Who to insure (Ich/Jemand anders) → Birth date → Occupation (autocomplete) → Self-employed? (Ja/Nein) → Coverage slider → Tier selection (Basic/Smart/Best with add-ons, contract duration on same page)

**Form fields**: versichertePerson (radio: Mich selbst/Jemand anders), birthDate (spinbutton: Tag/Monat/Jahr), occupation (autocomplete combobox), selfEmployed (radio: Ja/Nein), coverageAmount (slider, €10k-€300k), plan (tabs: Basic/Smart/Best), addOns (checkboxes), vertragslaufzeit (dropdown: 1-4 Jahre), zahlweise (dropdown)

**Validation**: Age 18-75, coverage €10k-€300k step €5k, occupation required (autocomplete accepts specific job titles only — some trigger follow-up questions e.g. Polizist)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/unfall/screenshots/, research/unfall/price-matrix.json
**Confidence**: HIGH (16 data points, coverage linearity R²=1.0, occupation multipliers verified constant)
**Discrepancies from previous entry**: Coverage range €10k-€300k (was €25k-€500k). Tier names Basic/Smart/Best (was Grundschutz/Komfort/Premium). Step-function age model with 2.0× at 65 (was quadratic polynomial). Risk multipliers 1.0/1.55/3.10 (was 1.0/1.3/1.7). Tier ratios 1.0/2.02/2.54 (was ~1.0/1.39/1.89). Occupation is autocomplete with specific job titles (was generic dropdown).

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

**Note — ERGO tier names**: ERGO's calculator labels these as Grundschutz/Komfort/Premium (verified in batch 2 research screenshots). Unlike Unfall (Basic/Smart/Best) and Hausrat (Smart/Best), Risikoleben uses standard tier names.

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
| **Age range** | 0–99 (age bands: 0-15, 16-19 flat; 20-99 per-year) |
| **Coverage** | €5–€160/day Pflegetagegeld, step €5, default €10 |
| **Coverage unit** | per €1/day (perfectly linear: price = ageRate × dailyBenefit) |
| **Risk class** | None |
| **Payment duration** | Not specified in calculator |
| **Waiting period** | None |

**Note — Not 3 tiers**: ERGO offers 3 **separate products**, not 3 tiers of one product:
- **PTG** (Pflege Tagegeld) — age-dependent, "Bestseller", primary product for our demo
- **PZU** (Pflege-Zuschuss 50%/100%) — fixed price €29.70/€59.40/month, no age dependency
- **KFP** (KombiMed Förder-Pflege) — fixed price €25.72/month, state-subsidized (€5/month Zulage)

**Note — DKV brand**: Calculator is DKV-branded (ERGO Group subsidiary), not ERGO-branded.

**Pricing model: Template B** (lookup table — exponential age curve, quadratic R²=0.956 inadequate, exponential R²=0.999)

**PTG rate table** (EUR/month per €1/day benefit):

| Age | Rate | Age | Rate | Age | Rate | Age | Rate |
|-----|------|-----|------|-----|------|-----|------|
| 0-15 | 0.451 | 30 | 0.903 | 50 | 2.136 | 70 | 5.786 |
| 16-19 | 0.462 | 35 | 1.117 | 55 | 2.694 | 75 | 7.884 |
| 20 | 0.591 | 40 | 1.381 | 60 | 3.448 | 80 | 11.085 |
| 25 | 0.731 | 45 | 1.711 | 65 | 4.332 | 90 | 22.230 |

Full per-year rates for ages 20-99 available in research/pflegezusatz/products-entry.md.

**Growth rate**: ~5.4%/year (exponential). Age 65 anomaly: only 1.48% growth (likely regulatory adjustment).

**Fixed-price products**:

| Product | Monthly price | Description |
|---------|--------------|-------------|
| PZU 50% | €29.70 | 50% Aufstockung der gesetzlichen Pflegeleistungen |
| PZU 100% | €59.40 | Verdopplung der gesetzlichen Pflegeleistungen |
| KFP | €25.72 | Staatlich gefördert (€5/Monat Zulage), keine Gesundheitsfragen |

**Loading**: Built into rates
**Calibration**: PTG, age 30, €10/day → €9.03/month ✓ (0.903 × 10)

**Optional features**: Inflationsschutz (auto-increase every 3 years), Erhöhungsoption (increase on life events without health check), Pflege Schutz Paket (24h Versorgungsgarantie, €1.000 Einmalzahlung ab PG2)

**Wizard steps**: N/A (single-page configurator — no wizard steps. Just Geburtsjahr dropdown + Tagegeldhöhe dropdown → instant price display.)

**Form fields**: birthYear (dropdown), dailyBenefit (dropdown: €5-€160 in €5 steps)

**Validation**: birthYear range 1925–2026, dailyBenefit €5–€160 in €5 steps only

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/pflegezusatz/screenshots/, research/pflegezusatz/price-matrix.json
**Confidence**: HIGH (82 data points ages 0-99, coverage linearity verified at 3 ages, exponential R²=0.999)
**Discrepancies from previous entry**: Not 3 tiers — 3 separate products (PTG/PZU/KFP). Age range 0-99 (was 20-65). Coverage in EUR/day (was EUR/month). No waiting period (was 5y/3y/1y). No tiers to select — single product (PTG) with coverage amount. PZU and KFP are fixed-price alternatives. Exponential age curve needs Template B. DKV-branded calculator. Single-page configurator, not wizard.

---

## 10. Tierkrankenversicherung (Pet Health)

| Parameter | Value |
|-----------|-------|
| **ID** | tierkranken |
| **Category** | animal |
| **Insured event** | veterinary treatment for illness/accident |
| **Age range** | 0–10 (pet age in years) |
| **Coverage** | Fixed (no annual limit) — no coverage slider |
| **Coverage unit** | N/A (flat monthly premium) |
| **Risk class** | Species: Hund only (Katze and Pferd NOT offered by ERGO) |
| **Payment duration** | Ongoing |
| **Waiting period** | 30 days (all variants) |

**⚠ NO ONLINE CALCULATOR**: ERGO does not sell Tierkrankenversicherung online. No product page exists on ergo.de. This is an agent-only product, and ERGO agents may sell third-party products (HanseMerkur, Uelzener, Helvetia) rather than an ERGO-underwritten product. **All pricing data below is UNVERIFIED.**

**Note — Single tariff, not 3 tiers**: ERGO's Hunde-Krankenversicherung appears to be a single tariff with a GOT reimbursement level choice (1× or 2× GOT-Satz), not 3 tiers.

**Base rates** (monthly, UNVERIFIED): GOT-1× ~€20/month, GOT-2× ~€30/month
**Age curve**: Flat rate ages 0-4, then +5%/year exponential escalation from age 5 birthday
**Loading**: Unknown
**Calibration**: Cannot verify — no online calculator

**Tariff variants** (not tiers):
- **GOT-1×**: Erstattung nach 1-fachem GOT-Satz, 30 Tage Wartezeit
- **GOT-2×**: Erstattung nach 2-fachem GOT-Satz, 30 Tage Wartezeit

Both include: Ambulante + stationäre Behandlung (unbegrenzt), Operationen inkl. Medikamente/Röntgen/Verbandsmaterial, €100/Jahr Zuschuss für Impfungen/Wurmkuren/Ektoparasiten/Zahnsteinentfernung, Chipkosten bis €25, Kastrationszuschuss, Alternative Behandlungen (Homöopathie/Akupunktur), 6 Monate Auslandsschutz europaweit, Freie Tierklinik/Tierarztwahl

**Wizard steps**: N/A — no online calculator. Agent-only product.

**Form fields**: N/A

**Note for demo**: The existing demo (tierkranken-v1) uses a fabricated 3-tier model with coverage slider and species multipliers. This works as a generic pet insurance demo but does NOT reflect ERGO's actual product. Consider flagging this in the demo UI or replacing with a generic-market model disclaimer.

**Source**: Agent page descriptions + third-party review sites (NO calculator verification possible)
**Evidence**: research/tierkranken/screenshots/ergo-produkte-overview.png
**Confidence**: LOW (no online calculator, pricing unverified, product may not be ERGO-underwritten)
**Discrepancies from previous entry**: Not 3 tiers — single tariff with GOT choice. No coverage slider (was €1k-€20k). Hund only (was Hund/Katze/Pferd). No online calculator (was assumed to exist). Exponential age escalation from age 5 (was quadratic). 30-day waiting (was 3mo/1mo/none by tier).

---

## 11. Reiseversicherung (Travel Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | reise |
| **Category** | travel |
| **Insured event** | trip cancellation, medical emergencies abroad, luggage loss |
| **Age range** | Age bands: ≤40, 41–64, 65+ (not exact age) |
| **Coverage** | Trip cost €1–€20.000 (for Storno/Rundum); flat rates for Krankenschutz |
| **Coverage unit** | Percentage of trip cost (Storno: 5-6%) or flat age-band rates (Kranken) |
| **Risk class** | None |
| **Payment duration** | Per trip or annual |
| **Waiting period** | None |

**Note — Not tiers**: ERGO offers 3 **separate product categories**, not tiers:
- **Stornokostenschutz** — Trip cancellation + interruption
- **Rundumschutz** — Bundle: Storno + Kranken + Gepäck
- **Krankenschutz** — Medical coverage abroad only

Each has single-trip (Einmal) and annual (Jahres) variants, each with/without Selbstbeteiligung.

**Note — External domain**: Calculator is on `app.ergo-reiseversicherung.de` (ERV subsidiary), NOT ergo.de. Completely different UX from other ERGO calculators.

**Pricing model: Template F** (travel-specific — trip-cost-based, does not fit templates A-E)

**Stornokostenschutz Einmal** (single trip):
- mit SB: exactly 5% of trip cost (age-independent, per-booking)
- ohne SB: exactly 6% of trip cost
- Auto transport: ×0.92 discount vs Flug
- Region has ZERO effect

**Stornokostenschutz Jahres** (annual):
- Formula: `price = (-91 + 3.79 × √trip_cost) × ageMult × groupMult × sbMult`
- Sparfuchs variant = ×0.90
- Age multipliers: ≤40 = 1.0, 41-64 = 1.10, 65+ = 2.09
- Group: Single = 1.0, Paar/Familie = 1.12 (children free with 2 adults)
- ohne SB: ×1.19

**Krankenschutz Einmal** (Europa, mit SB): ≤40 = €12.80, 41-64 = €16.00, 65+ = €34.40
- Welt multiplier (mit SB): ×1.125; (ohne SB): ×2.05
**Krankenschutz Jahres** (region-independent, mit SB): ≤40 = €31, 41-64 = €39, 65+ = €105

**Loading**: Built into rates
**Calibration**: Storno Einmal, 1 adult ≤40, €5k trip, Flug, mit SB → €250 (5% × 5000) ✓

**Wizard steps**: N/A — single-page configurator. Select product category → Enter travelers (age bands) → Trip details (dates, cost, destination, transport) → Instant price display for all variants.

**Form fields**: productCategory (tabs: Stornokostenschutz/Rundumschutz/Krankenschutz), travelers (age-band counters: ≤40/41-64/65+/kids), tripCost (number), destination (radio: Europa/Welt), transport (radio: Flugzeug-Schiff/Auto-Zug), travelDates (date range), bookingDate (date), deductible (checkbox: mit/ohne SB)

**Source**: app.ergo-reiseversicherung.de — researched 2026-04-13
**Evidence**: research/reise/screenshots/, research/reise/price-matrix.json
**Confidence**: MEDIUM-HIGH (20+ data points, Storno 5% rule exact, Jahres sqrt fit, age bands verified)
**Discrepancies from previous entry**: Not 3 tiers — 3 separate product categories. Trip-cost-based (5% for cancellation, not per-€1k rate). Age bands not continuous curve. External ERV domain. No risk classes. Template F (new).

---

## 12. Wohngebäudeversicherung (Building Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | wohngebaeude |
| **Category** | property |
| **Insured event** | damage to the building structure (fire, storm, water, natural hazards) |
| **Age range** | N/A (no customer age field — construction year replaces age) |
| **Coverage** | Derived from Wohnfläche: 60–180 m² (>180 requires advisor) |
| **Coverage unit** | per m² (linear: price = slope × m² + intercept) |
| **Risk class** | Address-specific (PLZ + street + house number, ZÜRS zones) |
| **Payment duration** | 3 years (stated in calculator) |
| **Waiting period** | None |

**Note — Only 2 tiers**: ERGO Wohngebäude has 2 tiers (Smart/Best), NOT 3.

**Note — External calculator**: Calculator is on `wohngebaeudeversicherung.ergo.de` (external subdomain), not the standard ergo.de/abschluss pattern.

**Pricing model: Template C variant** (linear per-m² with multiplicative factors, like Hausrat)

**Pricing formula** (annual, Smart, München reference):
```
annual_price = (4.854 × m² + 87.93) × regionMult × yearMult × sbMult × tierMult
```

**Tier multipliers**: Smart = 1.000, Best = 1.0953 (constant across all data points)

**Deductible factors**: ohne SB = 1.000, €500 = 0.850, €1000 = 0.800

**Construction year factors** (discrete bands):

| Construction year | Factor |
|-------------------|--------|
| Pre-2000 (1960, 1980) | 1.068 |
| 2000 | 1.000 (reference) |
| 2010 | 0.830 |
| 2020 | 0.660 |

**Regional multipliers** (address-specific, München=reference):

| City | PLZ | Multiplier |
|------|-----|-----------|
| Berlin | 10117 | 0.875 |
| Trier | 54290 | 0.996 |
| München | 80331 | 1.000 |
| Köln | 50667 | 1.170 |

**Age curve**: NONE — no customer age field in calculator. Construction year is the age-like factor.

**Building configuration** (measured but factors NOT yet quantified):
- House type: Einfamilienhaus / Zweifamilienhaus / Mehrfamilienhaus
- Roof: Ausgebautes Dach / Nicht ausgebautes Dach / Flachdach
- Floors: 0–3 Vollgeschosse
- Basement: mehr/weniger als Hälfte unterkellert / kein Keller
- Garage: 0–4
- Open fireplace: Ja/Nein (>5000 Watt)

**Perils**: Feuer + Leitungswasser included. Sturm/Hagel and Elementargefahren toggleable. Add-ons: Leitungswasser Plus, Allgemeine Haustechnik, Heizungs- und Energietechnik.

**Loading**: Built into rates
**Calibration**: EFH, 120m², München, Baujahr 2000, SB €500, Smart → annual price from formula (4.854×120+87.93)×1.0×1.0×0.85×1.0 = €570.18/year ≈ €47.51/month

**Tiers** (ERGO names: Smart / Best):
- **Smart** (→ grundschutz): Basis-Gebäudeschutz, Feuer + Leitungswasser
- **Best** (→ komfort): + erweiterte Leistungen, höhere Deckungssummen

**Wizard steps**: Hausdaten (Haustyp/Dach/Geschosse/Keller/Garage/Kamin) → Wohnfläche (m²) → Baujahr → Adresse (PLZ+Straße+Hausnummer, validiert) → Versicherungsschutz (Gefahren toggles) → Tarifergebnis (Smart/Best, SB, Zahlweise)

**Form fields**: haustyp (radio: EFH/ZFH/MFH), dach (radio: 3 options), vollgeschosse (dropdown: 0-3), keller (radio: 3 options), garagen (dropdown: 0-4), kamin (radio: Ja/Nein), wohnflaeche (number: 60-180 m²), baujahr (dropdown), plz (text), strasse (text, validated), hausnummer (text), gefahren (toggles: Sturm/Hagel/Elementar), addOns (toggles), plan (tabs: Smart/Best), selbstbeteiligung (dropdown: ohne/€500/€1000), zahlweise (dropdown)

**Source**: wohngebaeudeversicherung.ergo.de — researched 2026-04-13
**Evidence**: research/wohngebaeude/screenshots/, research/wohngebaeude/price-matrix.json
**Confidence**: MEDIUM-HIGH (15 data points, m² linearity R²=0.997, tier ratio constant. Building config factors and add-on pricing not yet measured due to API 502 errors.)
**Discrepancies from previous entry**: Only 2 tiers (was 3). Per-m² pricing (was per-€50k). No age field (was 18-99). Construction year bands replace age. Address-specific regional (was building type risk classes). External subdomain calculator. Template C variant not A.

---

## 13. Kfz-Versicherung (Motor Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | kfz |
| **Category** | motor |
| **Insured event** | vehicle damage, liability, theft |
| **Age range** | 18+ (age does NOT affect pricing — collected for contract purposes only) |
| **Coverage** | Haftpflicht (mandatory) + Teilkasko or Vollkasko (optional, mutually exclusive) |
| **Coverage unit** | N/A (vehicle-specific, not user-selectable amount) |
| **Risk class** | SF-Klasse (0–50+, 51 levels) — SEPARATE tables for Haftpflicht and Vollkasko |
| **Payment duration** | 1 year renewable |
| **Waiting period** | None |

**Note — Only 2 tiers**: ERGO Kfz has 2 tiers (Smart/Best), NOT 3. Smart = stärkere Rückstufung (harsher claim downgrade, lower price). Best = normale Rückstufung + add-ons.

**Pricing model: Template E** (Kfz-specific additive component model — does NOT fit templates A-D)

**Pricing formula**: `monthlyPremium = HP_base × HP_SF_pct/100 + VK_base × VK_SF_pct/100 + tierAddon`

**Base rates** (monthly at 100% SF, VW Golf VIII, München, 12k km, SB VK500/TK150):

| Component | Smart | Best |
|-----------|-------|------|
| HP base | €82.48 | €91.85 |
| VK base | €156.82 | €208.15 |
| TK (at SF10) | €24.50 | €34.87 |
| Tier addon | €0 | €1.73 |

**Coverage types** (primary product selector, not tiers):

| Coverage | HP | TK | VK | Smart /mo | Best /mo |
|----------|----|----|-----|-----------|----------|
| Haftpflicht ohne Kasko | Yes | No | No | €27.22 | €32.04 |
| Haftpflicht & Teilkasko | Yes | Yes | No | €51.72 | €66.91 |
| Haftpflicht & Vollkasko | Yes | No | Yes | €78.97 | €100.73 |

(All prices: SF 10, München, 12k km, VK500/TK150, monthly)

**SF-Klasse lookup tables** (51 levels, percentages applied to base):

HP SF: 0=86%, ½=66%, 1=53%, 2=50%, 3=47%, 4=44%, 5=42%, 6=40%, 7=38%, 8=36%, 9=35%, 10=33%, 11=32%, 12=31%, 13=30%, 14=29%, 15=28%, 16=27%, 17=26%, 18=26%, 19=25%, 20=24%, 21=24%, 22=23%, 23=23%, 24=22%, 25=22%, 26=21%, 27=21%, 28=21%, 29=20%, 30=20%, 31=19%, 32=19%, 33=19%, 34=18%, 35=18%, 36=18%, 37=18%, 38=17%, 39=17%, 40=17%, 41=17%, 42=16%, 43=16%, 44=16%, 45=16%, 46=16%, 47=16%, 48=15%, 49=15%, 50+=15%

VK SF: 0=54%, ½=49%, 1=44%, 2=42%, 3=41%, 4=39%, 5=38%, 6=37%, 7=36%, 8=34%, 9=33%, 10=33%, 11=32%, 12=31%, 13=30%, 14=29%, 15=28%, 16=28%, 17=27%, 18=27%, 19=26%, 20=25%, 21=25%, 22=24%, 23=24%, 24=23%, 25=23%, 26=23%, 27=22%, 28=22%, 29=21%, 30=21%, 31=21%, 32=20%, 33=20%, 34=20%, 35=19%, 36=19%, 37=19%, 38=19%, 39=18%, 40=18%, 41=18%, 42=18%, 43=17%, 44=17%, 45=17%, 46=17%, 47=16%, 48=16%, 49=16%, 50+=15%

**Age curve**: NONE. Zero effect on pricing (verified at ages 26, 36, 66 — identical prices).

**Mileage impact** (relative to 12k km base, München, SF 10, Best):
- 6k km: HP ×0.886, VK ×0.807
- 12k km: ×1.0 (reference)
- 20k km: HP ×1.140, VK ×1.337

**Regional impact** (Regionalklasse determined by PLZ, separate for HP and VK):

| City | PLZ | RK HP | RK VK | HP Best SF10 | VK Best SF10 |
|------|-----|-------|-------|-------------|-------------|
| München | 80331 | 10 | 7 | €30.31 | €68.69 |
| Köln | 50667 | 10 | 7 | €30.75 | €70.11 |
| Berlin | 10117 | 12 | 9 | €35.90 | €83.93 |

**SB impact** (VK component, Best, SF10, monthly):

| Selbstbeteiligung | VK Best | vs VK500 |
|-------------------|---------|----------|
| VK ohne / TK ohne | €113.62 | ×1.654 |
| VK 300 / TK 150 | €73.51 | ×1.070 |
| VK 500 / TK 150 | €68.69 | ×1.000 |
| VK 1000 / TK 150 | €59.30 | ×0.863 |

**Payment mode**: monatlich = base, jährlich = ×0.932 (7.2% monthly surcharge)
**Loading**: Built into base rates
**Calibration**: VW Golf VIII, München, 12k km, SF 10, VK500/TK150, Best, monthly → HP €30.31 + VK €68.69 + addon €1.73 = €100.73/month ✓

**Tiers** (ERGO names: Smart / Best):
- **Smart** (→ grundschutz): Stärkere Rückstufung im Schadenfall (lower price, harsher claim penalty)
- **Best** (→ komfort): Normale Rückstufung, + Ersatzfahrzeug Plus, Wertschutz 36 Monate, Schutzbrief, Rabattschutz (optional), Mallorca-Police

**Optional add-ons**: Werkstattbonus, Ersatzfahrzeug Plus (Best: included), Wertschutz 24/36 (Best: 36 included), Schutzbrief (Best: included), Rabattschutz (Best only), Safe Drive

**Wizard steps**: Angaben (Vertragsart/Geburtsdatum/Berufsgruppe/Versicherungsbeginn) → Fahrzeugsuche (Hersteller/Modell/Kraftstoff/Kategorie/Leistung → HSN/TSN selection) → Fahrzeughalter (Halter/PLZ/Erstzulassung/Fahrer) → Fahrzeugnutzung (Fahrleistung/Nutzung/SF-Klasse HP+VK/Versicherungsschutz) → Tarifdaten (tier selection Smart/Best, SB, Zahlweise, add-ons)

**Form fields**: vertragsart (radio: Versicherer wechseln/Fahrzeug wechseln/Erstvertrag), birthDate (spinbutton), berufsgruppe (dropdown: 6 options), versicherungsbeginn (date), hersteller (combobox), modell (combobox), kraftstoff (combobox), fahrzeugkategorie (combobox), leistung (combobox), fahrzeugVariante (radio table: specific HSN/TSN), fahrzeughalter (dropdown), plz (text), erstzulassung (date), letzteZulassung (date), fahrer (checkboxes: VN/Partner/Familie/Sonstige), fahrleistung (spinbutton: km/year), nutzung (radio: privat/geschäftlich), sfKlasseHP (dropdown: SF 0-50+), sfKlasseVK (dropdown: SF 0-50+), versicherungsschutz (dropdown: HP only/HP+TK/HP+VK), plan (tabs: Smart/Best), selbstbeteiligung (dropdown: 11 VK/TK combinations), zahlweise (dropdown), addOns (checkboxes)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/kfz/screenshots/, research/kfz/price-matrix.json
**Confidence**: MEDIUM-HIGH (28 data points, SF model verified to sub-cent accuracy, only 1 vehicle tested)
**Discrepancies from previous entry**: NO age curve (was U-curve 1.80/-1.20/0.50). Only 2 tiers (was 3). Additive HP+VK components (was flat rate per tier). SF-Klasse 0-50+ with 51 levels (was 0-35). Separate SF tables for HP and VK. Category "motor" not "property". Base rates completely different. Mileage and region are significant factors (not modeled before). Template E (new) not A.

---

## 14. Motorradversicherung (Motorcycle Insurance)

| Parameter | Value |
|-----------|-------|
| **ID** | motorrad |
| **Category** | motor |
| **Insured event** | motorcycle damage, liability, theft |
| **Age range** | 18+ (age AFFECTS pricing — U-shaped curve, unlike Kfz) |
| **Coverage** | Haftpflicht (mandatory) + Teilkasko or Vollkasko (optional) |
| **Coverage unit** | N/A (vehicle-specific) |
| **Risk class** | SF-Klasse (0–20+, 22 levels) — SEPARATE tables for HP and VK |
| **Payment duration** | 1 year renewable |
| **Waiting period** | None |

**Note — Only 2 tiers**: Smart / Best (same as Kfz).

**Pricing model: Template E variant** (like Kfz but WITH age curve)

**Pricing formula**: `monthlyPremium = (HP_base × ageFactor × HP_SF%/100) + (VK_base × ageFactor × VK_SF%/100) + TK_flat + tierAddon`

**Base rates** (monthly at 100% SF, Honda CBF 500, München, 6k km, SB VK150/TK150, age 36):

| Component | Smart | Best |
|-----------|-------|------|
| HP base | €22.16 | €26.99 |
| VK base | €78.49 | €106.45 |
| TK (flat, no SF) | €7.09 | €11.23 |
| Tier addon | €0 | €1.30 |

**Age curve** (U-shaped quadratic, minimum at ~47):
`ageFactor(age) = 2.566 - 0.0698 × age + 0.000750 × age²`
- Age 26: 1.26, Age 36: 1.03, Age 46: 0.94, Age 66: 1.23

**SF-Klasse lookup tables** (22 levels):
HP SF: 0=100%, ½=74%, 1=54%, 2=48%, 3=44%, 4=40%, 5=38%, 6=36%, 7=34%, 8=32%, 9=31%, 10=30%, 11=29%, 12=28%, 13=28%, 14=27%, 15=27%, 16=26%, 17=26%, 18=25%, 19=25%, 20+=24%

VK SF: 0=100%, ½=76%, 1=55%, 2=49%, 3=46%, 4=43%, 5=40%, 6=38%, 7=36%, 8=35%, 9=34%, 10=33%, 11=32%, 12=31%, 13=30%, 14=30%, 15=29%, 16=28%, 17=28%, 18=28%, 19=27%, 20+=27%

**Key differences from Kfz**: Age curve EXISTS (Kfz had none). Only 22 SF levels (Kfz: 51). HP SF 0=100% (Kfz: 86%). Motorcycle-specific add-on: Motorradbekleidung Plus. Saisonkennzeichen option.

**Loading**: Built into base rates
**Calibration**: Honda CBF 500, München, 6k km, SF 10, VK150, Smart, age 36 → HP (22.16×1.03×0.30) + VK (78.49×1.03×0.33) + addon 0 ≈ €33.53/month

**Tiers** (ERGO names: Smart / Best):
- **Smart** (→ grundschutz): Stärkere Rückstufung
- **Best** (→ komfort): Normale Rückstufung + Ersatzfahrzeug Plus + Schutzbrief + Motorradbekleidung Plus

**Wizard steps**: ~13 steps: Angaben (Vertragsart/Geburtsdatum/Berufsgruppe/Beginn/Saisonkennzeichen) → Fahrzeugsuche (Hersteller/Modell/Hubraum → HSN/TSN) → Fahrzeughalter (Halter/PLZ/Erstzulassung/Fahrer) → Fahrzeugnutzung (km/Nutzung/SF HP+VK/Versicherungsschutz) → Tarifdaten (Smart/Best, SB, Zahlweise, add-ons)

**Form fields**: Similar to Kfz but with motorcycle-specific fields (Hubraum, Saisonkennzeichen)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/motorrad/screenshots/, research/motorrad/price-matrix.json
**Confidence**: MEDIUM-HIGH (~22 data points, HP SF model verified with zero error, age curve verified at 6 ages, only 1 motorcycle tested)

---

## 15. Cyberversicherung (Cyber Risk — for individuals)

**⚠ NO ONLINE CALCULATOR**: ERGO does not have a Cyberversicherung product page (404). All pricing data below is UNVERIFIED market estimates.

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

**Base rates** (flat/month, UNVERIFIED): Grundschutz €1.50, Komfort €2.80, Premium €4.50
**Age curve**: base=1.0, linear=0.0, quadratic=0.0 (flat — assumed)
**Loading**: 20%

**Tiers** (UNVERIFIED):
- **Grundschutz**: Identitätsdiebstahl bis €10k, Phishing-Schutz, Datenrettung
- **Komfort**: + Onlinekauf-Schutz, Cybermobbing, Rechtsberatung digital, Kreditkartenschutz
- **Premium**: + Dark-Web-Monitoring, Reputationsschutz, psychologische Beratung, Lösegeldzahlung

**Wizard steps**: N/A — no online calculator

**Source**: Generic market estimates (NO calculator verification possible)
**Confidence**: LOW (product page returns 404, pricing unverified)

---

## 15. Krankentagegeldversicherung (Daily Sickness Allowance)

| Parameter | Value |
|-----------|-------|
| **ID** | krankentagegeld |
| **Category** | person |
| **Insured event** | income loss during illness (Krankentagegeld supplement for employees; full income replacement for self-employed) |
| **Age range** | 15–80 (birth year 1946–2011; quadratic age curve with plateau at 67+) |
| **Coverage** | €5–€520/day, step €5, default €15 (AN) / €50 (SE) |
| **Coverage unit** | per €1/day (perfectly linear: price = rate × dailyBenefit) |
| **Risk class** | Berufsstatus: separate tariff tables for Arbeitnehmer vs Selbständiger/Freiberufler |
| **Payment duration** | Unlimited (keine Höchstleistungsdauer) |
| **Waiting period** | Leistungsbeginn: AN 43–365 Tag (10 options), SE 4–183 Tag (8 options) |

**Note — Not tiers**: ERGO does NOT offer tiers. Single product (KombiMed KTAG) with configuration via Berufsstatus, Leistungsbeginn, and Tagegeldhöhe.

**Note — Two tariff tables**: Arbeitnehmer and Selbständiger/Freiberufler use completely separate rate tables. Freiberufler = Selbständiger pricing (only max coverage differs: €520 vs €300/day).

**Note — DKV brand**: Calculator is DKV-branded (ERGO Group subsidiary).

**Pricing model: Template B variant** (quadratic age curve with plateau, separate tariff tables)

**Pricing formula**: `price = ageRate(age, berufsstatus) × dailyBenefit × lbFactor(tag, berufsstatus)`

**Arbeitnehmer age rates** (EUR/month per €1/day, Leistungsbeginn 43.Tag):

| Age | Rate | Age | Rate | Age | Rate |
|-----|------|-----|------|-----|------|
| 25 | 0.454 | 40 | 0.734 | 55 | 1.178 |
| 30 | 0.534 | 45 | 0.864 | 60 | 1.316 |
| 35 | 0.626 | 50 | 1.016 | 67+ | 1.412 (plateau) |

**Selbständiger age rates** (EUR/month per €1/day, Leistungsbeginn 29.Tag):

| Age | Rate | Age | Rate | Age | Rate |
|-----|------|-----|------|-----|------|
| 25 | 0.598 | 40 | 0.860 | 55 | 1.246 |
| 30 | 0.672 | 45 | 0.974 | 60 | 1.406 |
| 35 | 0.760 | 50 | 1.102 | 67+ | 1.532 (plateau) |

**Leistungsbeginn factors — AN** (normalized to 43.Tag = 1.0):
43=1.000, 64=0.712, 85=0.577, 92=0.502, 106=0.438, 127=0.375, 169=0.273, 183=0.243, 274=0.116, 365=0.064

**Leistungsbeginn factors — SE** (normalized to 29.Tag = 1.0):
4=3.432, 8=3.116, 15=1.905, 22=1.283, 29=1.000, 43=0.810, 92=0.354, 183=0.107

**Coverage limits by Berufsstatus**: AN pflichtversichert = €5-35/day, AN freiwillig = €5-520/day, Selbständiger = €5-300/day, Freiberufler = €5-520/day. Versicherungsstatus has NO effect on pricing — only changes max coverage.

**Loading**: Built into rates
**Calibration**: AN, age 30, 43.Tag, €15/day → €8.01/month (0.534×15) ✓
**Calibration**: SE, age 30, 29.Tag, €50/day → €33.60/month (0.672×50) ✓

**Wizard steps**: N/A (single-page configurator — Berufsstatus → Geburtsjahr → [Versicherungsstatus] → Leistungsbeginn → Tagegeldhöhe → instant price)

**Form fields**: berufsstatus (radio: Arbeitnehmer/Selbständiger/Freiberufler), versicherungsstatus (radio, AN only: pflichtversichert/freiwillig), birthYear (dropdown 1946-2011), leistungsbeginn (dropdown, options vary by status), dailyBenefit (dropdown: €5-€520 in €5 steps)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/krankentagegeld/screenshots/, research/krankentagegeld/price-matrix.json
**Confidence**: HIGH (~146 data points, coverage linearity verified, quadratic MAPE<1%, Leistungsbeginn factors verified at 3 ages)
**Discrepancies from previous entry**: Not 3 tiers — single product. Separate AN/SE tariff tables (not simple multiplier). Coverage step €5 (was €10). Age range 15-80 (was 18-60). Leistungsbeginn is key pricing variable with 10/8 options. Single-page configurator. DKV-branded.
