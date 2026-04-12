# Ticket 13: Generic Wizard Step Tracking & Analytics

## Priority: Phase 1 (foundation) + Phase 3 (integration)

## Problem

There is no visibility into where users drop off in the wizard funnel. We don't know:
- How many users start vs. complete the wizard
- Which step has the highest abandonment rate
- How long users spend on each step
- Whether users go back to edit previous steps

## Objective

Build a **generic, reusable** tracking system that works for any multi-step wizard, not just the tariff wizard. Records step progression events to Supabase for funnel analytics.

## Architecture

### Overview

```
User navigates wizard
        ↓
WizardTrackingProvider (useEffect on step/subStep changes)
        ↓
Fire-and-forget POST to /api/track
        ↓
Supabase: wizard_tracking_events table
```

### Components

1. **`WizardTrackingProvider`** — React component that wraps inside WizardProvider. Observes step changes, computes dwell time and field completion, fires tracking events. Zero re-renders (all state in useRef).

2. **`/api/track` route** — POST handler that inserts events into Supabase. Returns 200 even when Supabase is not configured (tracking is non-critical).

3. **Supabase table** — `{TABLE_PREFIX}_wizard_tracking_events` with indexes for session and wizard type queries.

## Tracked Events

| Event Type | When | Data Captured |
|-----------|------|---------------|
| `wizard_start` | Provider mounts | session_id, wizard_name, timestamp |
| `step_enter` | User arrives at a step | step, subStep, direction (forward/backward/jump) |
| `step_leave` | User leaves a step | step, subStep, direction, **dwell_time_ms**, **fields_filled**, **fields_total** |
| `wizard_complete` | User reaches final step | same as step_enter |

## Files to Create

### `src/lib/wizard/WizardTrackingProvider.tsx` (CREATE)

```typescript
"use client";

import { useEffect, useRef } from "react";
import { useWizard, type StepMap, type WizardFormData } from "./WizardContext";

// -- Types --

export type TrackingEventType =
  | "wizard_start"
  | "step_enter"
  | "step_leave"
  | "wizard_complete";

export type NavigationDirection = "forward" | "backward" | "jump";

export interface TrackingEvent {
  session_id: string;
  wizard_name: string;
  event_type: TrackingEventType;
  step: number;
  sub_step: number;
  direction: NavigationDirection | null;
  dwell_time_ms: number | null;
  fields_filled: number | null;
  fields_total: number | null;
  timestamp: string; // ISO 8601
  metadata: Record<string, unknown> | null;
}

// -- Props --

interface WizardTrackingProviderProps {
  wizardName: string;        // e.g. "tariff", "onboarding"
  stepMap: StepMap;          // from WizardContext
  children: React.ReactNode;
  enabled?: boolean;         // default true, disable in tests
  metadata?: Record<string, unknown> | null;
}
```

**Internal mechanics:**
- `sessionIdRef` — `crypto.randomUUID()` on mount
- `prevStepRef` — tracks previous step/subStep for direction computation
- `entryTimestampRef` — `Date.now()` when step was entered, for dwell time
- Single `useEffect` watching `[state.step, state.subStep]`
- `beforeunload` handler captures step_leave when user closes tab

**Direction computation:**
```typescript
function computeDirection(
  prev: { step: number; subStep: number },
  curr: { step: number; subStep: number }
): NavigationDirection {
  const prevLinear = prev.step * 1000 + prev.subStep;
  const currLinear = curr.step * 1000 + curr.subStep;
  if (Math.abs(curr.step - prev.step) > 1) return "jump"; // goTo from summary
  if (currLinear > prevLinear) return "forward";
  if (currLinear < prevLinear) return "backward";
  return "forward";
}
```

**Field counting:**
```typescript
function countFilledFields(formData: Record<string, unknown>): {
  filled: number;
  total: number;
} {
  const keys = Object.keys(formData);
  let filled = 0;
  for (const key of keys) {
    const val = formData[key];
    if (val === null || val === undefined || val === "") continue;
    if (typeof val === "object" && !Array.isArray(val)) {
      // Nested (e.g., birthDate: { day, month, year })
      const children = Object.values(val as Record<string, unknown>);
      if (children.some((v) => v !== null && v !== undefined && v !== "")) filled++;
      continue;
    }
    filled++;
  }
  return { filled, total: keys.length };
}
```

**Fire-and-forget:**
```typescript
function sendTrackingEvent(event: TrackingEvent): void {
  try {
    fetch("/api/track", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(event),
      keepalive: true, // survives page navigation/close
    }).catch(() => {}); // silently ignore
  } catch {
    // silently ignore
  }
}
```

**Renders:** `{children}` unchanged. Zero visual output.

### `src/app/api/track/route.ts` (CREATE)

```typescript
import { supabase, isSupabaseConfigured, tableName } from "@/lib/supabase";

export async function POST(request: Request) {
  if (!isSupabaseConfigured) {
    return Response.json({ ok: true, stored: false });
  }

  try {
    const body = await request.json();
    if (!body.session_id || !body.event_type || !body.wizard_name) {
      return Response.json({ error: "Missing required fields" }, { status: 400 });
    }

    const { error } = await supabase
      .from(tableName("wizard_tracking_events"))
      .insert([{
        session_id: body.session_id,
        wizard_name: body.wizard_name,
        event_type: body.event_type,
        step: body.step,
        sub_step: body.sub_step,
        direction: body.direction,
        dwell_time_ms: body.dwell_time_ms,
        fields_filled: body.fields_filled,
        fields_total: body.fields_total,
        timestamp: body.timestamp,
        metadata: body.metadata,
        created_at: new Date().toISOString(),
      }]);

    if (error) {
      console.error("Tracking insert error:", error);
      return Response.json({ error: error.message }, { status: 500 });
    }

    return Response.json({ ok: true, stored: true });
  } catch (err) {
    console.error("Track error:", err);
    return Response.json({ error: "Invalid request" }, { status: 400 });
  }
}
```

### Supabase Table Schema

Add to Phase 0 (setup), after creating the insurance_applications table:

```sql
CREATE TABLE IF NOT EXISTS {TABLE_PREFIX}_wizard_tracking_events (
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  session_id    UUID NOT NULL,
  wizard_name   TEXT NOT NULL,
  event_type    TEXT NOT NULL CHECK (event_type IN ('wizard_start', 'step_enter', 'step_leave', 'wizard_complete')),
  step          INTEGER NOT NULL,
  sub_step      INTEGER NOT NULL,
  direction     TEXT CHECK (direction IN ('forward', 'backward', 'jump') OR direction IS NULL),
  dwell_time_ms INTEGER,
  fields_filled INTEGER,
  fields_total  INTEGER,
  timestamp     TIMESTAMPTZ NOT NULL,
  metadata      JSONB,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_wte_session ON {TABLE_PREFIX}_wizard_tracking_events (session_id);
CREATE INDEX idx_wte_wizard_event ON {TABLE_PREFIX}_wizard_tracking_events (wizard_name, event_type);

ALTER TABLE {TABLE_PREFIX}_wizard_tracking_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public insert" ON {TABLE_PREFIX}_wizard_tracking_events FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read" ON {TABLE_PREFIX}_wizard_tracking_events FOR SELECT USING (true);
```

## Files to Modify

### `src/lib/wizard/TariffContext.tsx` (MODIFY)
Export the step map so it can be passed to the tracking provider:
```typescript
// Change line 39 from:
const TARIFF_STEP_MAP: StepMap = { 1: 3, 2: 2, 3: 1, 4: 1 };
// To:
export const TARIFF_STEP_MAP: StepMap = { 1: 3, 2: 2, 3: 1, 4: 1 };
```

### `src/lib/wizard/index.ts` (MODIFY)
Add exports:
```typescript
export { WizardTrackingProvider } from "./WizardTrackingProvider";
export type { TrackingEvent, TrackingEventType, NavigationDirection } from "./WizardTrackingProvider";
```

### `src/app/wizard/page.tsx` (MODIFY)
Wrap WizardShell inside the tracking provider:
```tsx
import { WizardTrackingProvider } from "@/lib/wizard/WizardTrackingProvider";
import { TARIFF_STEP_MAP } from "@/lib/wizard/TariffContext";

// Nesting order:
// ToastProvider > TariffProvider > WizardTrackingProvider > WizardShell
<TariffProvider>
  <WizardTrackingProvider wizardName="tariff" stepMap={TARIFF_STEP_MAP}>
    <WizardShell ... />
  </WizardTrackingProvider>
</TariffProvider>
```

### `tickets/EXECUTE.md` (MODIFY)
Add to Phase 0 Step 4: create the tracking table alongside insurance_applications.
Add to Phase 1: create WizardTrackingProvider.tsx and /api/track route.
Add to Phase 3 integration: verify tracking events appear in Supabase after walkthrough.

## Reusability

To add tracking to a **different** wizard (e.g., "onboarding"):

```tsx
<OnboardingProvider>
  <WizardTrackingProvider wizardName="onboarding" stepMap={ONBOARDING_STEP_MAP}>
    <WizardShell ... />
  </WizardTrackingProvider>
</OnboardingProvider>
```

That's it. The `/api/track` route and Supabase table are shared. The `wizard_name` column distinguishes sources in queries.

## Example Analytics Queries

```sql
-- Funnel: how many sessions reached each step?
SELECT step, sub_step, COUNT(DISTINCT session_id) as sessions
FROM {TABLE_PREFIX}_wizard_tracking_events
WHERE wizard_name = 'tariff' AND event_type = 'step_enter'
GROUP BY step, sub_step ORDER BY step, sub_step;

-- Drop-off: sessions that started but never completed
SELECT COUNT(DISTINCT session_id) as abandoned
FROM {TABLE_PREFIX}_wizard_tracking_events
WHERE wizard_name = 'tariff' AND event_type = 'wizard_start'
  AND session_id NOT IN (
    SELECT session_id FROM {TABLE_PREFIX}_wizard_tracking_events
    WHERE event_type = 'wizard_complete'
  );

-- Average dwell time per step
SELECT step, sub_step, AVG(dwell_time_ms) / 1000.0 as avg_seconds
FROM {TABLE_PREFIX}_wizard_tracking_events
WHERE event_type = 'step_leave' AND wizard_name = 'tariff'
GROUP BY step, sub_step ORDER BY step, sub_step;

-- Field completion at drop-off points
SELECT step, sub_step, AVG(fields_filled::float / NULLIF(fields_total, 0)) as avg_completion
FROM {TABLE_PREFIX}_wizard_tracking_events
WHERE event_type = 'step_leave' AND wizard_name = 'tariff'
GROUP BY step, sub_step ORDER BY step, sub_step;
```

## Dashboard: Funnel Analytics Section

**IMPORTANT**: The dashboard (ticket 10/11) must include a "Wizard-Funnel" section that visualizes the tracking data. This was missed in previous runs where the tracking infrastructure was built but never surfaced in the UI.

### What to add to `src/app/dashboard/page.tsx`

Query the `wizard_tracking_events` table alongside `insurance_applications` (use `Promise.all` for parallel queries). Compute and display:

#### 1. Funnel Summary Cards (3-column grid)
- **Sessions gestartet** — count of distinct `session_id` where `event_type = 'wizard_start'` (accent: green `#4CAF50`)
- **Abgeschlossen** — count of distinct `session_id` where `event_type = 'wizard_complete'` (accent: blue `#2196F3`)
- **Abschlussrate** — `completed / started * 100` as percentage (accent: primary color)

#### 2. Step-by-step Funnel Bars
For each wizard step (1.1 through 4.1), show:
- Step number badge (primary color circle) + German label
- Horizontal bar showing percentage of sessions that reached this step (relative to total started)
- Average dwell time badge: "Ø Xs" from `step_leave` events' `dwell_time_ms`
- Drop-off badge: "−N Abbruch" showing sessions lost between this step and the previous one
- Final step (4.1 Zusammenfassung) bar in green instead of primary color

#### Step label map:
```typescript
const STEP_LABELS: Record<string, string> = {
  "1.1": "Geburtsdatum",
  "1.2": "Versicherungsbeginn",
  "1.3": "Versicherungssumme",
  "2.1": "Tarifauswahl",
  "2.2": "Beitragsdynamik",
  "3.1": "Persönliche Daten",
  "4.1": "Zusammenfassung",
};
```

#### 3. Placement
Insert the funnel section between "Tarif-Verteilung" and "Letzte Anträge". Only render when `totalSessions > 0`.

### Dashboard Agent Instructions

The **Dashboard agent (Agent H)** must implement this funnel section as part of building `src/app/dashboard/page.tsx`. It is NOT a separate agent — it's part of the same dashboard page.

The agent should:
1. Add a `TrackingEvent` interface for the query result
2. Query `tableName("wizard_tracking_events")` with `Promise.all` alongside the submissions query
3. Implement a `computeFunnel()` function that groups events by step and computes session counts, dwell times, and drop-offs
4. Render the funnel section with the summary cards and step bars

## Agent Execution

### Phase 0: Supabase table creation
Add the tracking table SQL to the setup alongside the insurance_applications table.

### Phase 1: Foundation
Create `WizardTrackingProvider.tsx` and `/api/track/route.ts`. Export from barrel. This is done by the orchestrator directly, not a parallel agent (it's shared infrastructure).

### Phase 2: Dashboard agent
Agent H must include the funnel analytics section when building the dashboard page. See "Dashboard: Funnel Analytics Section" above.

### Phase 3: Integration
- Modify `page.tsx` to wrap with WizardTrackingProvider
- During the playwright-cli walkthrough, check the browser Network tab for `/api/track` POST requests
- After walkthrough, query Supabase to verify tracking events exist
- Verify the dashboard funnel section renders with data after the walkthrough

### Tester: Integration Checks
```
[CHECK] Network tab shows POST /api/track requests on each step navigation
[CHECK] All requests return 200 with { ok: true, stored: true }
[CHECK] Supabase table contains wizard_start event
[CHECK] Supabase table contains step_enter and step_leave pairs
[CHECK] step_leave events have non-null dwell_time_ms
[CHECK] step_leave events have non-null fields_filled and fields_total
[CHECK] wizard_complete event exists after reaching final step
[CHECK] Dashboard shows "Wizard-Funnel" heading
[CHECK] Dashboard shows 3 funnel summary cards (Sessions, Abgeschlossen, Abschlussrate)
[CHECK] Dashboard shows step-by-step funnel bars with dwell times
[CHECK] Removing Supabase env vars → wizard still works, /api/track returns { ok: true, stored: false }
```
