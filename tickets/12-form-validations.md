# Ticket 12: Form Validations

## Priority: Phase 1 (foundation) + Phase 2 (per-page)

## Problem

The wizard currently has zero validation. Users can:
- Enter a birth year that makes them 20 years old (policy requires 40-85)
- Leave all personal data fields empty and still submit
- Submit without filling required fields on any step

This is unrealistic for a demo and makes the wizard feel broken.

## Objective

Add validation at two levels:
1. **Per-step validation**: Prevent advancing ("weiter") until the current step's required fields are valid
2. **Field-level validation**: Show inline error messages on individual fields

## Validation Rules by Page

### Page 1a: Birth Date
- All three fields (day, month, year) must be filled
- Day: 1-31, Month: 1-12, Year: 4 digits
- **Age validation**: Calculate age as `insuranceStartYear - birthYear`. Must be 40-85 inclusive.
- Error message: "Die versicherte Person muss zwischen 40 und 85 Jahre alt sein."
- "weiter" disabled until valid

### Page 1b: Insurance Start Date
- One option must be selected (default is middle, so this is always valid)
- No additional validation needed

### Page 1c: Coverage Amount
- Slider enforces range (1000-20000), so always valid
- No additional validation needed

### Page 2a: Plan Selection
- A plan must be selected (default is "komfort", so always valid)
- No additional validation needed

### Page 2b: Dynamic Adjustment
- User must click one of the two options (button or link), so always valid
- No additional validation needed

### Page 3: Personal Data
- **Required fields**: firstName, lastName (minimum)
- **Recommended fields**: street, zip, city, birthPlace, nationality
- Show errors on blur (not on every keystroke) for required fields
- Error message: "Dieses Feld ist erforderlich."
- ZIP validation: exactly 5 digits → "Bitte geben Sie eine gültige PLZ ein."
- "weiter" disabled until at least firstName and lastName are filled

### Page 4: Summary
- Both consent checkboxes must be checked (already implemented)
- Submit button already disabled until both checked (already works)

## Implementation Approach

### Foundation (Phase 1)

Create a generic validation utility at `src/lib/wizard/validation.ts`:

```typescript
export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: unknown, formData: Record<string, unknown>) => string | null;
}

export interface FieldValidation {
  field: string;
  rules: ValidationRule;
  errorMessage?: string; // override default messages
}

export interface StepValidationConfig {
  fields: FieldValidation[];
}

// Returns a map of field → error message (or empty map if all valid)
export function validateStep(
  config: StepValidationConfig,
  formData: Record<string, unknown>
): Record<string, string> {
  // ... validate each field against its rules
}

// Returns true if no errors
export function isStepValid(
  config: StepValidationConfig,
  formData: Record<string, unknown>
): boolean {
  return Object.keys(validateStep(config, formData)).length === 0;
}
```

### Per-Page (Phase 2)

Each page agent uses the validation utility:

```typescript
// Example: BirthDatePage
const VALIDATION: StepValidationConfig = {
  fields: [
    {
      field: "birthDate",
      rules: {
        custom: (val, formData) => {
          const bd = val as { day: string; month: string; year: string };
          if (!bd.day || !bd.month || !bd.year) return "Bitte geben Sie Ihr Geburtsdatum ein.";
          const startYear = parseInt(formData.insuranceStart?.toString().split(".")[2] || "2026");
          const age = startYear - parseInt(bd.year);
          if (age < 40 || age > 85) return "Die versicherte Person muss zwischen 40 und 85 Jahre alt sein.";
          return null;
        },
      },
    },
  ],
};
```

Each page:
1. Calls `validateStep(config, state.formData)` to get current errors
2. Passes error strings to UI components via their `error` prop (TextInput, DateInput, Select all support it)
3. Shows errors on blur or on "weiter" click attempt
4. Disables "weiter" button when `!isStepValid(config, state.formData)`

### UI Component Support

The existing UI components already have `error` props:
- `TextInput`: `error?: string` → renders `<span className="text-input__error">`
- `DateInput`: `error?: string` → renders `<span className="date-input__error">`
- `Select`: `error?: string` → renders `<span className="select__error">`

No UI component changes needed.

## Files to Create/Modify

### Foundation (Phase 1)
- `src/lib/wizard/validation.ts` — **CREATE** — generic validation utility

### Per-Page (Phase 2)
- `src/app/wizard/pages/BirthDatePage.tsx` — **MODIFY** — add age validation
- `src/app/wizard/pages/PersonalDataPage.tsx` — **MODIFY** — add required field validation
- Other pages: no changes needed (their inputs are always valid by design)

## Agent Execution

### Phase 1: Create `validation.ts` in foundation
The orchestrator creates this file alongside TariffContext and planData so all worktree agents inherit it.

### Phase 2: Page agents apply validation
- Agent A (BirthDatePage): Import validation, add age check, disable "weiter" when invalid
- Agent F (PersonalDataPage): Import validation, add required checks for firstName/lastName, show errors on blur

### Reviewer Focus
- Error messages in German
- Errors shown AFTER user interaction (blur or submit attempt), not on initial render
- "weiter" button disabled when validation fails (use `disabled` prop on Button)
- Age calculation uses the correct formula: insuranceStartYear - birthYear

### Tester: Page-Specific Checks
```
[CHECK] BirthDatePage: Enter birth year 2000 → error about age range shown
[CHECK] BirthDatePage: Enter birth year 1982 → no error, weiter enabled
[CHECK] BirthDatePage: Leave all fields empty → weiter disabled
[CHECK] PersonalDataPage: Leave firstName empty, click weiter → error shown
[CHECK] PersonalDataPage: Fill firstName + lastName → weiter enabled
[CHECK] PersonalDataPage: Enter 3-digit ZIP → error about PLZ format
```
