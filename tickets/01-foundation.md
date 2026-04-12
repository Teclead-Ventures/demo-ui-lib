# Ticket 01: Foundation — Wizard Shell, State & Navigation

## Priority: BLOCKING — Must complete before all other tickets

## Objective

Create the multi-step wizard infrastructure: shared form state context, wizard shell with step navigation, page routing, and the updated demo entry point. This replaces the current component showcase with the tariff wizard.

## Reference

The stepper bar visible in all reference screenshots (`screenshots/reference/`):
- 4 steps: **Tarifdaten** → **Beitrag** → **Persönliches** → **Zusammenfassung**
- Steps have sub-pages (Step 1 has 3, Step 2 has 2, Steps 3-4 have 1 each)
- Navigation: "weiter" (forward) button + "Zurück" (back) link
- Stepper component already exists in `src/components/Stepper/`

## Files to Create

### `demo/context/TariffContext.tsx`
Shared form state using React Context + useReducer:

```typescript
interface TariffState {
  // Step 1a: Birth date
  birthDate: { day: string; month: string; year: string };
  // Step 1b: Insurance start
  insuranceStart: string; // e.g. "01.06.2026"
  // Step 1c: Coverage
  coverageAmount: number; // 1000–20000, default 8000
  // Step 2a: Plan
  plan: "grundschutz" | "komfort" | "premium";
  // Step 2b: Dynamic
  dynamicAdjustment: "none" | "standard";
  // Step 3: Personal
  salutation: string;
  firstName: string;
  lastName: string;
  street: string;
  zipCity: string;
  birthPlace: string;
  nationality: string;
}

// Navigation state
interface WizardNav {
  step: number;      // 1-4 (maps to stepper)
  subStep: number;   // 1-based within each step
}
```

Provide `TariffProvider`, `useTariff()` for state, and `useWizardNav()` for navigation.

### `demo/TariffWizard.tsx`
Main wizard shell:
- Renders `<Stepper>` at top with 4 steps
- Conditionally renders the active page component based on step/subStep
- Centered layout (max-width ~560px, centered, padding 48px 24px)
- Font: "FS Me", Arial, Helvetica, sans-serif
- Page components are lazy-placeholders initially (just showing "Page X" text) — each ticket fills them in

### `demo/pages/index.ts`
Barrel export for all page components. Initially exports placeholder components.

### `demo/main.tsx` (MODIFY)
Replace the component showcase App with the TariffWizard wrapped in providers:
```tsx
import { TariffProvider } from "./context/TariffContext";
import { TariffWizard } from "./TariffWizard";
import { ToastProvider } from "../src/components/Toast";

initTheme({ primary: "#8e0038", secondary: "#bf1528" });

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ToastProvider>
    <TariffProvider>
      <TariffWizard />
    </TariffProvider>
  </ToastProvider>
);
```

## Layout Specifications (from reference screenshots)

- Stepper bar: full width at top, with subtle bottom border
- Content area: centered, max-width ~560px
- Heading: bold, large, centered
- "weiter" button: full-width, primary, ~max-width 360px, centered
- "Zurück" link: centered below button, ghost style
- Consistent vertical spacing: 32px between sections

## Sub-step Map

```
Step 1 (Tarifdaten):    subStep 1 = BirthDate, 2 = StartDate, 3 = CoverageAmount
Step 2 (Beitrag):       subStep 1 = PlanSelection, 2 = DynamicAdjustment
Step 3 (Persönliches):  subStep 1 = PersonalData
Step 4 (Zusammenfassung): subStep 1 = Summary
```

---

## Agent Sub-Team Instructions

### Developer Agent
1. Read the existing `demo/main.tsx` to understand current structure
2. Read `src/components/Stepper/Stepper.tsx` for the Stepper API
3. Create `demo/context/TariffContext.tsx` with full state management
4. Create `demo/TariffWizard.tsx` with wizard shell
5. Create `demo/pages/index.ts` with placeholder page components
6. Modify `demo/main.tsx` to use the wizard
7. Run `npx tsc --noEmit` to verify TypeScript compiles
8. Run `npm run demo` briefly to verify it starts

### Reviewer Agent
Review the developer's code for:
- [ ] Context state shape covers all form fields from all tickets
- [ ] Navigation logic handles forward/back correctly, including sub-step transitions
- [ ] Stepper `currentStep` maps correctly (sub-steps within step 1 all show step 1 active)
- [ ] No TypeScript errors
- [ ] Layout matches the centered, clean style from reference screenshots
- [ ] Placeholder pages are properly exported and renderable
- [ ] Provider wrapping order is correct (ToastProvider > TariffProvider > Wizard)

### Tester Agent
```bash
# 1. Verify TypeScript compiles
npx tsc --noEmit

# 2. Start dev server and take screenshot
# Start the vite dev server, navigate to localhost, verify:
#   - Stepper is visible with 4 steps
#   - "Tarifdaten" is highlighted as active
#   - A placeholder page is shown
#   - No console errors

# 3. Playwright smoke test (create e2e/foundation.spec.ts):
npx playwright test e2e/foundation.spec.ts
```

Write a Playwright test that:
- Loads the page
- Verifies the stepper is visible with 4 step labels
- Verifies "Tarifdaten" step is active
- Verifies a placeholder page renders
