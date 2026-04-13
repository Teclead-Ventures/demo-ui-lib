# ERGO Wohngebäudeversicherung — Calculator Structure

**URL**: https://wohngebaeudeversicherung.ergo.de?intcid=9000961
**Redirects to**: https://wohngebaeudeversicherung.ergo.de/public/web-app/checkout/WOHN25/0
**Brand**: ERGO (external subdomain, Angular-based SPA)
**Product code**: WOHN25

## Wizard Steps

### Step 0: Was möchten Sie versichern?
- **Haustyp** (radio): Einfamilienhaus | Zweifamilienhaus | Mehrfamilienhaus
- **Wohnen Sie selbst im Haus?** (dropdown): Ja | Nein
- **Wann wurde Ihr Haus gebaut?** (text): free-form year (e.g. 2012)

### Step 1: Wo befindet sich Ihr Haus?
- **Postleitzahl** (text): e.g. 80331
- **Ort** (dropdown, auto-populated from PLZ): e.g. München
- **Straße** (autocomplete combobox): lists all streets in the PLZ
- **Hausnummer** (autocomplete combobox): lists specific house numbers for the street

NOTE: Address is HIGHLY specific — down to individual house numbers. This is ZÜRS-zone based pricing (flood/natural hazard risk zones).

### Step 2: Wie ist Ihr Haus aufgebaut?
- **Dachgeschoss** (dropdown): Ausgebautes Dach | Nicht ausgebautes Dach | Flachdach
- **Obergeschosse** (dropdown): 0 | 1 | 2 | 3
- **Keller** (dropdown): mehr als die Hälfte unterkellert | weniger als die Hälfte unterkellert | kein Keller
- **Wohnfläche** (text, m²): e.g. 120 m²

KEY FINDING: Coverage is based on m² (Wohnfläche), NOT on a user-entered Gebäudewert. The system derives the insured value from the building characteristics (m², floors, roof, basement, etc.) using the "Wert 1914" formula.

### Step 3: Details zu Ihrem Haus
- **Kamin/Kachelofen >5.000€** (dropdown): Ja | Nein
- **Garagenstellplätze** (dropdown): 0 | 1 | 2 | 3 | 4
- **Versicherungsbeginn** (dropdown): 2026 | 2027

### Step 4: Pricing & Configuration Page
#### Tiers (2 tiers)
- **Smart** — base tier
- **Best** — premium tier (default, preselected)

#### Included Perils (always included)
- Feuer (Fire)
- Leitungswasser (Water damage from pipes)

#### Toggleable Perils (Versicherbare Gefahren)
- **Sturm und Hagel** (Storm & Hail) — toggle, appears ON by default
- **Elementargefahren** (Natural disasters) — toggle, state TBD

#### Add-on Modules (Sinnvolle Zusatzleistungen)
- **Leitungswasser Plus** — e.g. external pipe damage
- **Allgemeine Haustechnik** — e.g. wallboxes, charging stations
- **Heizungs- und Energietechnik** — e.g. PV systems, heat pumps

#### Configuration Options
- **Selbstbeteiligung** (deductible): ohne SB | 500€ (default) | 1.000€
- **Zahlweise** (payment frequency): monatlich | jährlich (default)

#### Assumptions stated
- "Gebäude mit max. 5 Nebengebäuden mit jeweils max. 30 qm"
- "keine Schäden in den letzten 3 Jahren"
- "harte Bedachung"
- "3 Jahre Vertragsdauer"

## Key Observations

1. **NO age field** — no customer birth date or age asked anywhere
2. **NO building type (Massiv/Fertighaus/Holz)** — our assumption was wrong! Instead uses construction year, roof type, floors, basement
3. **m²-based pricing** — like Hausrat, NOT per-€50k coverage value
4. **Address-specific** — uses exact street + house number, not just ZIP zone
5. **2 tiers** (Smart/Best), not 3 as we assumed
6. **Deductible strongly affects price** — consistent 15% discount for 500€ SB, 20% for 1000€ SB
7. **External subdomain calculator** — completely different UX from main ergo.de

## Deductible Factors (from first data point, München 120m²)
| SB | Smart | Best | Factor (vs ohne SB) |
|----|-------|------|---------------------|
| ohne | 801.69 | 878.12 | 1.000 |
| 500€ | 681.44 | 746.40 | 0.850 |
| 1000€ | 641.36 | 702.49 | 0.800 |

Tier ratio (Best/Smart): 878.12/801.69 = 1.0953 (~9.5% uplift)
