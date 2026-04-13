# Krankentagegeld - Structure Discovery

## Calculator Type
Single-page configurator (DKV pattern, like Pflegezusatz). NOT a multi-step wizard.

## Brand
ERGO product page, DKV-branded calculator. Product name: "KombiMed KTAG"
Footer shows both ERGO and DKV logos.

## Tiers / Products
- **Arbeitnehmer**: 2 columns shown:
  - Column 1: "für gesetzlich versicherte Arbeitnehmer"
  - Column 2: "für DKV-vollversicherte Arbeitnehmer"
  - These appear to be the SAME product with different target audiences, but share identical features
- **Selbständiger / Freiberufler**: 1 column only: "für Selbständige und Freiberufler"

Note: These are NOT tiers (no Smart/Best distinction). It's a single product with different configurations per Berufsstatus.

## Input Fields

### 1. Berufsstatus (3 radio buttons)
- Arbeitnehmer (default)
- Selbständiger
- Freiberufler

### 2. Geburtsjahr (dropdown)
- Range: 1946 - 2011
- Default: 1996 (age 30)

### 3. Tarifoption 1 (only for Arbeitnehmer)
- Gesetzlich pflichtversichert (default)
- Gesetzlich freiwillig versichert

### 4. Leistungsbeginn (dropdown) - varies by Berufsstatus
**Arbeitnehmer:**
43. Tag, 64. Tag, 85. Tag, 92. Tag, 106. Tag, 127. Tag, 169. Tag, 183. Tag, 274. Tag, 365. Tag
(Default: 43. Tag)

**Selbständiger / Freiberufler:**
4. Tag, 8. Tag, 15. Tag, 22. Tag, 29. Tag, 43. Tag, 92. Tag, 183. Tag
(Default: 29. Tag)

### 5. Tagegeldhöhe (dropdown, in 5€ steps)
**Arbeitnehmer:** 5€ - 35€ (default: 15€)
**Selbständiger:** 5€ - 300€ (default: 50€)
**Freiberufler:** 5€ - 520€ (default: 50€)

Note: Arbeitnehmer has MUCH lower max daily benefit (35€) vs Selbständiger (300€) / Freiberufler (520€).
This makes sense as Arbeitnehmer supplement GKV Krankengeld (gap insurance), while Selbständige need full income replacement.

## Coverage Details
- Max per day: 520€ (Arbeitnehmer/Freiberufler), 300€ (Selbständige)
- No Höchstleistungsdauer von 78 Wochen (unlike GKV)
- Step: 5€

## Initial Prices Observed
- Arbeitnehmer, 1996, gesetzlich pflicht, 43. Tag, 15€/day: 8.01€/mtl
- Column 2 (DKV-vollversichert): 5.37€/mtl (same settings)
- Selbständiger, 1996, 29. Tag, 50€/day: 33.60€/mtl
- Freiberufler, 1996, 29. Tag, 50€/day: 33.60€/mtl (same as Selbständiger!)
