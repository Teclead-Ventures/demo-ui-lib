## Privathaftpflichtversicherung (haftpflicht)

**Template**: D (flat-rate configurator with additive Bausteine)
**Brand**: ERGO
**Tiers**: Smart (10 Mio. EUR) / Best (50 Mio. EUR)
**Coverage**: Fixed by tier, no slider

### Base rates (monatlich, 3 Jahre, ohne SB, age >= 36)

| Family Status | Smart | Best |
|---|---|---|
| Single | 6.05 | 10.58 |
| Paar / Alleinerziehend | 7.56 | 12.09 |
| Familie | 9.07 | 13.60 |

### Age model
- Binary band: age < 36 at start = 13% Startbonus (x0.87), age >= 36 = flat
- No continuous age curve

### Risk classes (family status)
- Single: 1.0
- Paar / Alleinerziehend: Smart x1.25, Best x1.14
- Familie: Smart x1.50, Best x1.29
- Note: multipliers are tier-dependent (not a simple uniform multiplier)

### Bausteine (additive modules, monthly prices for Single/Smart)
- Schlüsselverlust: +1.21 (Best: included, Smart: optional)
- Neuwertentschädigung: +1.21 (Best: included, Smart: optional)
- Forderungsausfall: +1.21 (Best: included, Smart: optional)
- Amts- und Diensthaftpflicht: +1.93 (optional both tiers)
- Alleinstehende Familienangehörige: +0.00 (free, optional both tiers)

### Selbstbeteiligung
- ohne (default)
- 150 EUR: Smart -20%, Best -13.1%

### Vertragslaufzeit
- 3 Jahre (default, base rate)
- 1 Jahr: +11.1% surcharge

### Zahlungsweise surcharges (vs annual base)
- jährlich: 0%
- halbjährlich: +3%
- vierteljährlich: +5%
- monatlich: +6%

### Calibration check
- Single, Best, 3J, ohne SB, monatlich, age 36 = 10.58 EUR/month (ERGO actual)
- Single, Smart, 3J, ohne SB, monatlich, age < 36 = 5.26 EUR/month (advertised "ab" price)

**Source**: ergo.de -- researched 2026-04-13
**Evidence**: research/haftpflicht/screenshots/, research/haftpflicht/price-matrix.json
**Confidence**: HIGH
**Discrepancies from previous entry**:
- Tiers: was 3 (Grundschutz/Komfort/Premium), actually 2 (Smart/Best)
- Base rates: was 4.10/5.00/6.15, actually Smart 6.05 / Best 10.58
- Age curve: was flat (correct in spirit), but actually has binary Startbonus <36
- Risk class: was Single(1.0)/Familie(1.35)/Single-mit-Kind(1.20), actually Single(1.0)/Paar-Allein(1.25)/Familie(1.50) for Smart, different for Best
- Coverage: was 1M-50M slider, actually fixed by tier (10M/50M)
- Loading: was 20%, N/A for Template D
- Template: was implicitly A (polynomial), actually D (flat-rate configurator)
