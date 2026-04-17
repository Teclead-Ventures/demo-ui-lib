# Ticket 09: Integration & End-to-End Testing

## Priority: FINAL — Execute after all page tickets (02-08) are merged

## Objective

Verify the complete wizard flow end-to-end using playwright-cli. Two test profiles (localhost + production). Confirm Supabase submissions appear on dashboard.

---

## Test Profile 1 — Integration (localhost)

**Scenario**: 35-year-old software developer, Bürotätigkeit, Komfort plan

| Field | Value |
|-------|-------|
| Beruf | Bürotätigkeit / kaufmännisch |
| Geburtsdatum | 15.03.1990 |
| Einkommen | 3.500 € |
| BU-Rente | 2.000 €/Monat |
| Plan | Komfort |
| Raucher | Nein |
| Vorerkrankungen | Nein |
| Anrede | Herr |
| Vorname | Markus |
| Nachname | Weber |
| Straße | Friedrichstraße 22 |
| PLZ | 10117 |
| Stadt | Berlin |
| **Erw. Preis** | **~58,37 €/Monat** |
| **Laufzeit** | **32 Jahre** |

```bash
playwright-cli open http://localhost:3000/wizard --headed

# Step 1: Occupation
# Select "Bürotätigkeit / kaufmännisch" → click "weiter"

# Step 2: Birth Date
# Enter Tag=15, Monat=03, Jahr=1990 → click "weiter"

# Step 3: Coverage
# Set income to 3500, slider to 2000 → click "weiter"

# Step 4: Plan Selection
# Verify "Komfort" pre-selected, price ~58,37 € → click "weiter zum Online-Antrag"

# Step 5: Health Questions
# Both "Nein" selected → click "weiter"

# Step 6: Personal Data
# Fill: Herr / Markus / Weber / Friedrichstraße 22 / 10117 / Berlin → click "weiter"

# Step 7: Summary
# Verify all 4 sections show correct data
# Check both checkboxes
# Click "Jetzt verbindlich abschließen"
# [CHECK] Success toast appears

playwright-cli open http://localhost:3000/dashboard --headed
# [CHECK] New submission from Markus Weber appears in table
```

---

## Test Profile 2 — Production (Vercel)

**Scenario**: 47-year-old electrician (Handwerk), Premium plan, higher risk

| Field | Value |
|-------|-------|
| Beruf | Handwerk / Techniker |
| Geburtsdatum | 22.07.1978 |
| Einkommen | 2.800 € |
| BU-Rente | 1.800 €/Monat |
| Plan | Premium |
| Raucher | Nein |
| Vorerkrankungen | Nein |
| Anrede | Frau |
| Vorname | Sandra |
| Nachname | Hoffmann |
| Straße | Karlsplatz 7 |
| PLZ | 80335 |
| Stadt | München |
| **Erw. Preis** | **~100,63 €/Monat** |
| **Laufzeit** | **20 Jahre** |

```bash
playwright-cli open https://[project].vercel.app/wizard --headed
# Complete full walkthrough with above data
# [CHECK] Success toast appears
# [CHECK] Dashboard shows both submissions (Test 1 + Test 2)
```

---

## Demo Mode Test

```bash
playwright-cli open http://localhost:3000/wizard?demo=true --headed
# All fields pre-filled with Markus Weber data
# Click "weiter" through all 7 steps without typing
# [CHECK] Summary shows pre-filled data
# [CHECK] Submit works
```

---

## Price Verification

Verify pricing formula at runtime (Console or test):

```
Set 1: age=35, coverage=2000, plan=komfort, occupation=buero
  t = (35-18)/(55-18) = 0.459
  ageFactor = 0.70 + 0.50×0.459 - 0.15×0.459² = 0.898
  netPremium = 2.54 × 20 × 0.898 × 1.0 = 45.63
  gross = 45.63 × 1.28 = 58.41 → ~58,37-58,41 €/Monat ✓

Set 2: age=47, coverage=1800, plan=premium, occupation=handwerk
  t = (47-18)/(55-18) = 0.784
  ageFactor = 0.70 + 0.50×0.784 - 0.15×0.784² = 0.998
  netPremium = 3.12 × 18 × 0.998 × 1.4 = 78.62
  gross = 78.62 × 1.28 = 100.63 → ~100,63 €/Monat ✓
```
