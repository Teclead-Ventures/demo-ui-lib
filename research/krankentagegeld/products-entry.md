## 15. Krankentagegeldversicherung (Daily Sickness Allowance)

| Parameter | Value |
|-----------|-------|
| **ID** | krankentagegeld |
| **Category** | person |
| **Insured event** | income loss during illness (Krankentagegeld supplement for employees; full income replacement for self-employed) |
| **Age range** | 15–80 (birth year 1946–2011; quadratic age curve with plateau at age 67+) |
| **Coverage** | €5–€520/day, step €5, default €15 (AN) / €50 (SE) |
| **Coverage unit** | per €1/day (perfectly linear: price = rate × dailyBenefit) |
| **Risk class** | Berufsstatus: separate tariff tables for Arbeitnehmer vs. Selbständiger/Freiberufler |
| **Payment duration** | Unlimited (keine Höchstleistungsdauer von 78 Wochen wie in GKV) |
| **Waiting period** | Leistungsbeginn: AN 43–365 Tag (10 options), SE 4–183 Tag (8 options) |

**Note — Not tiers**: ERGO does NOT offer tiers (Grundschutz/Komfort/Premium). It is a **single product** (KombiMed KTAG) with configuration via Berufsstatus, Leistungsbeginn, and Tagegeldhöhe.

**Note — Two tariff tables**: Arbeitnehmer and Selbständiger/Freiberufler use completely separate rate tables. Freiberufler pricing is identical to Selbständiger (only max coverage differs: 520€ vs 300€/day).

**Note — DKV brand**: Calculator is DKV-branded (ERGO Group subsidiary).

**Pricing model: Template B variant** (quadratic age curve with plateau, MAPE=0.75%)

**Pricing formula**: `price = ageRate(age, berufsstatus) × dailyBenefit × lbFactor(tag, berufsstatus)`

**Arbeitnehmer age rate table** (EUR/month per €1/day, Leistungsbeginn 43.Tag):

| Age | Rate | Age | Rate | Age | Rate | Age | Rate |
|-----|------|-----|------|-----|------|-----|------|
| 25 | 0.454 | 35 | 0.626 | 45 | 0.864 | 55 | 1.178 |
| 27 | 0.484 | 38 | 0.688 | 48 | 0.954 | 58 | 1.264 |
| 30 | 0.534 | 40 | 0.734 | 50 | 1.016 | 60 | 1.316 |
| 33 | 0.588 | 43 | 0.810 | 53 | 1.114 | 65 | 1.396 |
| 67+ | 1.412 (plateau) | | | | | | |

**Selbständiger/Freiberufler age rate table** (EUR/month per €1/day, Leistungsbeginn 29.Tag):

| Age | Rate | Age | Rate | Age | Rate | Age | Rate |
|-----|------|-----|------|-----|------|-----|------|
| 20 | 0.534 | 34 | 0.742 | 45 | 0.974 | 57 | 1.310 |
| 23 | 0.570 | 35 | 0.760 | 47 | 1.022 | 59 | 1.374 |
| 25 | 0.598 | 37 | 0.800 | 49 | 1.074 | 60 | 1.406 |
| 26 | 0.612 | 39 | 0.840 | 50 | 1.102 | 61 | 1.436 |
| 28 | 0.642 | 40 | 0.860 | 52 | 1.158 | 63 | 1.488 |
| 30 | 0.672 | 42 | 0.904 | 54 | 1.216 | 65 | 1.524 |
| 31 | 0.690 | 44 | 0.950 | 55 | 1.246 | 66 | 1.530 |
| 67+ | 1.532 (plateau) | | | | | | |

**Quadratic fit** (rate per €1/day, for ages up to 66):
- AN (43.Tag): rate = 0.000112 × age² + 0.01485 × age - 0.0138
- SE (29.Tag): rate = 0.000223 × age² + 0.00364 × age + 0.365

**Leistungsbeginn factors — Arbeitnehmer** (normalized to 43.Tag = 1.0):

| Tag | Factor | Tag | Factor | Tag | Factor |
|-----|--------|-----|--------|-----|--------|
| 43 | 1.0000 | 92 | 0.5019 | 183 | 0.2434 |
| 64 | 0.7116 | 106 | 0.4382 | 274 | 0.1161 |
| 85 | 0.5768 | 127 | 0.3745 | 365 | 0.0637 |
| | | 169 | 0.2734 | | |

**Leistungsbeginn factors — Selbständiger/Freiberufler** (normalized to 29.Tag = 1.0):

| Tag | Factor | Tag | Factor |
|-----|--------|-----|--------|
| 4 | 3.4315 | 29 | 1.0000 |
| 8 | 3.1161 | 43 | 0.8095 |
| 15 | 1.9048 | 92 | 0.3542 |
| 22 | 1.2827 | 183 | 0.1071 |

**Note**: Leistungsbeginn factors have ~2-3% age interaction (not purely multiplicative), acceptable for demo.

**Coverage limits by Berufsstatus**:

| Berufsstatus | Versicherungsstatus | Tagegeldhöhe |
|-------------|---------------------|--------------|
| Arbeitnehmer | Gesetzlich pflichtversichert | 5–35 €/day |
| Arbeitnehmer | Gesetzlich freiwillig versichert | 5–520 €/day |
| Selbständiger | N/A | 5–300 €/day |
| Freiberufler | N/A | 5–520 €/day |

**Versicherungsstatus** (pflicht/freiwillig) has NO effect on pricing — only changes max Tagegeldhöhe.

**Loading**: Built into rates

**Calibration**:
- AN, age 30, 43.Tag, 15€/day → 8.01€/month (0.534 × 15 = 8.01) ✓
- SE, age 30, 29.Tag, 50€/day → 33.60€/month (0.672 × 50 = 33.60) ✓
- AN, age 50, 43.Tag, 15€/day → 15.24€/month (1.016 × 15 = 15.24) ✓
- SE, age 40, 4.Tag, 50€/day → 126.70€/month (0.860 × 50 × 2.9465 ≈ 126.7) ✓

**Form fields**: berufsstatus (radio: Arbeitnehmer/Selbständiger/Freiberufler), versicherungsstatus (radio, AN only: pflichtversichert/freiwillig), birthYear (dropdown 1946-2011), leistungsbeginn (dropdown, options vary by berufsstatus), dailyBenefit (dropdown: €5-€520 in €5 steps, max varies by status)

**Validation**: birthYear 1946–2011, dailyBenefit step €5, leistungsbeginn from fixed option lists

**Wizard steps**: N/A (single-page configurator — no wizard. Berufsstatus → Geburtsjahr → [Versicherungsstatus] → Leistungsbeginn → Tagegeldhöhe → instant price.)

**Source**: ergo.de — researched 2026-04-13
**Evidence**: research/krankentagegeld/screenshots/, research/krankentagegeld/price-matrix.json
**Confidence**: HIGH (~146 data points, coverage linearity verified, quadratic age fit MAPE<1%, Leistungsbeginn factors verified at 3 ages, Freiberufler=Selbständiger confirmed)
**Discrepancies from previous entry**: Not 3 tiers — single product (no Grundschutz/Komfort/Premium). Not a simple employment multiplier — completely separate tariff tables for AN vs SE. Coverage step €5 (was €10). Age range 15–80 (was 18–60). Leistungsbeginn is a key pricing variable with 10 (AN) / 8 (SE) options. Single-page configurator, not wizard. DKV-branded. Versicherungsstatus only affects max coverage, not price.
