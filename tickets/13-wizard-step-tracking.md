# Ticket 13: Wizard Step Tracking — Zahnzusatzversicherung

## Priority: Optional (post-launch)

## Problem

No visibility into where users drop off in the 6-step wizard.

## Objective

Track step transitions in `TariffContext.tsx` so analytics events can be fired on each `goTo()` / `nextStep()` call.

## Implementation

### In `TariffContext.tsx`

Add an optional `onStepChange` callback to the context:

```typescript
// Called whenever step changes — wire up to analytics if needed
const handleStepChange = (from: number, to: number) => {
  if (typeof window !== "undefined" && (window as any).gtag) {
    (window as any).gtag("event", "wizard_step", {
      event_category: "zahnzusatz_wizard",
      event_label: `step_${to}`,
      value: to,
    });
  }
};
```

Call `handleStepChange(currentStep, newStep)` inside `nextStep()` and `goTo()` before updating state.

### Step Labels

| Step | Label |
|------|-------|
| 1 | versicherte_person |
| 2 | geburtsdatum |
| 3 | versicherungsbeginn |
| 4 | tarifauswahl |
| 5 | persoenliche_daten |
| 6 | zusammenfassung |

### Drop-off Signal

Track `wizard_abandoned` event when user navigates away from `/wizard` without completing step 6.
Use `beforeunload` or Next.js `useRouter` navigation events — only if analytics are configured.

## Demo Mode

In demo mode (`isDemo=true`), suppress analytics events to avoid polluting real data.

## Dependencies

- No external analytics package needed — hooks into existing `gtag` if present
- If no analytics configured: function is a no-op
- Add `NEXT_PUBLIC_GA_ID` to `.env.local` if Google Analytics is used
