# Ticket 12: Form Validations — Berufsunfähigkeitsversicherung

## Overview

Validation rules for the BU wizard. Each page handles its own validation locally.

---

## Page 1b — BirthDatePage (Step 2)

**Field**: `birthDate`

| Rule | Logic | Error message |
|------|-------|---------------|
| required | All 3 parts (day/month/year) must be non-empty | "Bitte geben Sie Ihr vollständiges Geburtsdatum an." |
| age-range | `calculateAge(birthDate)` must be 18–55 | "Wir versichern Personen zwischen 18 und 55 Jahren." |

Implementation: validate on "weiter" click, show error inline below DateInput.

---

## Page 1c — CoveragePage (Step 3)

**Field**: `coverageAmount`

| Rule | Logic | Error message |
|------|-------|---------------|
| max-75-pct | `coverageAmount ≤ floor(monthlyIncome × 0.75 / 100) × 100` | Enforced by slider max — no explicit error needed |

The slider max is dynamically computed from income, so users cannot exceed 75% via the UI. No explicit error message required.

---

## Page 4 — PersonalDataPage (Step 6)

| Field | Rule | Error message |
|-------|------|---------------|
| salutation | required (non-empty string) | "Bitte wählen Sie eine Anrede." |
| firstName | min-length 2 | "Bitte geben Sie Ihren Vornamen ein." |
| lastName | min-length 2 | "Bitte geben Sie Ihren Nachnamen ein." |
| street | required (non-empty) | "Bitte geben Sie Ihre Straße und Hausnummer ein." |
| zip | pattern `/^\d{5}$/` | "Bitte geben Sie eine gültige Postleitzahl ein." |
| city | required (non-empty) | "Bitte geben Sie Ihren Ort ein." |

Implementation: validate all on "weiter" click, show per-field errors below each input. Clear individual error when user modifies that field.

---

## Pages without validation

These pages have no blocking validation:
- **OccupationPage (Step 1)**: Always has a value (defaulted to "buero")
- **PlanSelectionPage (Step 4)**: Always has a value (defaulted to "komfort")
- **HealthQuestionsPage (Step 5)**: Always has values (both default to "nein"), "Ja" shows notice but doesn't block
- **SummaryPage (Step 7)**: Submit button disabled until both checkboxes checked (UI-level, not form validation)

---

## Validation utilities

No shared validation file needed. Each page validates its own fields inline. Example pattern:

```typescript
const validate = (): Record<string, string> => {
  const errors: Record<string, string> = {};
  if (!data.salutation) errors.salutation = "Bitte wählen Sie eine Anrede.";
  if (data.firstName.trim().length < 2) errors.firstName = "Bitte geben Sie Ihren Vornamen ein.";
  // ...
  return errors;
};
```
