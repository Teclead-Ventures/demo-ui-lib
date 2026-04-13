# ERGO Rechtsschutzversicherung -- Form Structure

**Source**: https://www.ergo.de/de/Produkte/Rechtsschutzversicherung
**Calculator URL**: https://www.ergo.de/de/Produkte/Rechtsschutzversicherung/abschluss
**Researched**: 2026-04-13
**Total steps**: 10 (steps 1-4 are intake, step 5 is single-page configurator with pricing, steps 6-10 are application/purchase)

## Key Structural Differences from Our Model

1. **NO age-based pricing curve** -- Price is flat regardless of age (verified at ages 20, 35, 60, 70). Only exception: under-25 gets 10% Startbonus.
2. **NO coverage amount selection** -- No slider for coverage. Coverage is determined by tier (Smart = 2M EUR, Best = unlimited).
3. **Bausteine (legal areas) are additive toggles**, not tiers. The user selects which legal areas to insure.
4. **Two tiers only**: Smart and Best (NOT Grundschutz/Komfort/Premium).
5. **Family status creates TWO pricing groups**: Single (includes Alleinerziehend) and Familie (includes Paar).
6. **Vital variant** for retirees: different base rates, no Beruf Baustein.

## Wizard Structure

### Step 1: Lebenssituation (#/)
**Heading**: "Wahlen Sie Ihre Lebenssituation aus."
- Field: Family status -- Type: radio -- Options: Single / Alleinerziehend / Paar / Familie
- "weiter" button

### Step 2: Geburtsdatum (#/geburtsdatum)
**Heading**: "Geben Sie Ihr Geburtsdatum ein."
**Subtext**: "Ihr Alter ist wichtig fur die Berechnung Ihres Beitrags."
- Field: Geburtsdatum -- Type: text (TT.MM.JJJJ format) -- Required: yes
- Note: Age does NOT affect pricing (except under-25 Startbonus). Birthdate is used for contract eligibility.
- "weiter" / "zuruck" buttons

### Step 3: Beschaftigungssituation (#/beschaftigungssituation)
**Heading**: "Sind Sie berufstatig?"
- Field: Employed -- Type: radio -- Options: Ja / Nein
- If "Nein": skips to different step 4 (retirement status)
- "weiter" / "zuruck" buttons

### Step 4a: Berufliche Situation (if Ja) (#/beschaftigt)
**Heading**: "Wahlen Sie Ihre berufliche Situation aus."
- Field: Employment type -- Type: radio -- Options: Arbeitnehmer / Beamter bzw. im offentlichen Dienst tatig / Selbststandig bzw. Freiberufler
- Note: Employment type does NOT affect pricing. Only affects default Baustein selection and Beruf coverage details.
- "weiter" / "zuruck" buttons

### Step 4b: Unbeschaftigt Situation (if Nein) (#/unbeschaftigt)
**Heading**: "Wahlen Sie Ihre Situation aus."
- Field: Status -- Type: radio -- Options: (Vor-)Ruhestand oder dauerhaft nicht mehr erwerbstatig / Beamter im (Vor-)Ruhestand / Ohne berufliche Tatigkeit
- Note: Ruhestand selections trigger "Vital" variant with different pricing.
- "weiter" / "zuruck" buttons

### Step 5: Versicherungsschutz / Configurator (#/versicherungsschutz)
**This is the main pricing page -- single-page configurator with live price updates.**

**Header shows**:
- Tier + family label (e.g., "Best Single", "Smart Familie fur Paare", "Best Vital Single")
- Monthly price (updates live on changes)
- Summary: Gewahlte Lebensbereiche, Selbstbeteiligung, Versicherungsbeginn, Vertragsdauer

**Tier selection**:
- Smart: Versicherungssumme 2 Mio. EUR, Cyber-Rechtsschutz
- Best: Versicherungssumme unbegrenzt, Cyber-/Urheber-Rechtsschutz, Phishing, Vorsorgeverfugungen/Testament, Spezial-Straf-Rechtsschutz, Kapitalanlagestreitigkeiten

**Bausteine (toggle switches)**:
- Privat: Private legal protection (can be standalone)
- Beruf: Employment legal protection (requires Privat; not available for Vital)
- Wohnen: Housing/rental legal protection (requires Privat)
- Verkehr: Traffic legal protection (can be standalone)

**Dropdowns**:
- Zahlungsweise: Monatlich / Vierteljahrlich / Halbjahrlich / Jahrlich
- Selbstbeteiligung: 150 EUR (default) / 250 EUR / 500 EUR
- Vertragsdauer: 1 Jahr (default) / 3 Jahre (10% Dauernachlass)

**Date field**:
- Versicherungsbeginn: default = tomorrow's date

**Buttons**: "Online beantragen" (continue to application), "zuruck"

### Steps 6-10: Application (not researched)
Steps 6-10 are personal data entry for the actual application (name, address, payment, etc.). Not relevant for pricing research.

## Product Variants

| Family Status | Label | Pricing Group | Beruf Available |
|---|---|---|---|
| Single | "Best/Smart Single" | Single | Yes |
| Alleinerziehend | "Best/Smart Single fur Alleinerziehende" | Single | Yes |
| Paar | "Best/Smart Familie fur Paare" | Familie | Yes |
| Familie | "Best/Smart Familie" | Familie | Yes |
| Ruhestand | "Best/Smart Vital Single" | Vital | No |

## Fields NOT Present (vs Our Model)

- NO coverage amount slider (our model assumes 100K-1M EUR)
- NO risk class
- NO continuous age curve (our model assumes quadratic age factor)
- NO waiting period field (no Wartezeit for this product)
- YES: tier selection (Smart/Best)
- YES: birth date (for under-25 bonus and eligibility)
- YES: family status (affects pricing group)
- YES: employment status (affects available Bausteine)
