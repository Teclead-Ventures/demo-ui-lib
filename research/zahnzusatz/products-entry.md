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
**Age curve**: base=0.13, linear=3.08, quadratic=-0.52 (steep near-linear increase, but ERGO actually uses discrete age bands — see note)
**Loading**: 22%
**Calibration**: 35yo, Komfort → ~€21.70/month ✓

**Note — Age bands**: ERGO uses discrete age bands, not a smooth curve. The polynomial is an approximation. Actual ERGO band prices (DS90/Komfort):
- 0–20: €3.70, 21–25: €7.20, 26–30: €13.80, 31–40: €21.70, 41–50: €32.50, 51+: €44.40.
The polynomial fits band midpoints with R²=0.997 but deviates up to ±50% at band edges.

**Tiers**:
- **Grundschutz** (DS75): 75% Erstattung für Zahnersatz, Inlays, Implantate. Professionelle Zahnreinigung 1×/Jahr. Leistungsbegrenzung: max €1.000/Y1, €2.000/Y1-2, €3.000/Y1-3, €4.000/Y1-4
- **Komfort** (DS90): 90% Erstattung für Zahnersatz, Inlays, Implantate. Professionelle Zahnreinigung 1×/Jahr. Same Leistungsbegrenzungen. GOZ bis 3,5-fach
- **Premium** (DS100): 100% Erstattung für Zahnersatz, Inlays, Implantate, KFO für Kinder (bis €1.000). Professionelle Zahnreinigung. GOZ bis 5,0-fach. Fahrkostenpauschale €50 nach Narkose

**Special**: First 6 months at 50% premium (Startbeitrag). Optional add-on: "Dental-Vorsorge" (preventive dental) combined with DS tariff.

**Wizard steps**: Who to insure → Birth date → Start date (price shown) → Plan comparison → [Online-Abschluss]

**Form fields**: insurerType (radio: Ich / Ich und jemand anders / Nur jemand anders), birthDate (spinbutton: Tag/Monat/Jahr), insuranceStart (radio: 1st of next 3 months), plan (tabs: pre-selected by tariff URL, option for Dental-Vorsorge add-on)

**Validation**: Birth date required, no maximum age restriction observed in calculator

**Source**: ergo.de — researched 2026-04-12
**Evidence**: research/zahnzusatz/screenshots/, research/zahnzusatz/price-matrix.json
**Confidence**: HIGH
**Discrepancies from previous entry**:
- Coverage model changed from per-unit (€250/year) to flat rate
- Coverage slider removed (ERGO has no user-selectable coverage amount)
- Age range expanded from 18–75 to 0–75
- Base rates changed from per-unit to flat: Grundschutz €2.70→€14.26, Komfort €3.29→€17.79, Premium €4.05→€22.62
- Age curve changed from gentle (0.80/0.35/0.10) to steep (0.13/3.08/−0.52)
- Waiting period changed from 8mo/3mo/none to none/none/none
- dentalStatus and missingTeeth fields removed (not present in ERGO)
- Tiers renamed from benefit-differentiated to reimbursement %-differentiated (DS75/DS90/DS100)
- First 6 months half price feature added
