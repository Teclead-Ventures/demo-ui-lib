# Ticket 13: Wizard Step Tracking

## Priority: Phase 1 (Foundation) — build BEFORE wizard pages

Tracking is not optional. Without it, the dashboard has no funnel data and the demo
loses half its value. Every wizard must track step transitions to Supabase so the
dashboard can show where users drop off.

## Implementation

### 1. Create `src/app/(app)/api/track/route.ts` (shared, created once per project)

```typescript
import { NextResponse } from "next/server";
import { supabase, isSupabaseConfigured, tableName } from "@/lib/supabase";

export async function POST(request: Request) {
  if (!isSupabaseConfigured) {
    return NextResponse.json({ ok: true }); // silent no-op when Supabase not configured
  }
  try {
    const body = await request.json();
    await supabase.from(tableName(`${body.product}_tracking`)).insert([{
      session_id: body.sessionId,
      product: body.product,
      step: body.step,
      step_label: body.stepLabel,
      timestamp: new Date().toISOString(),
    }]);
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ ok: true }); // tracking failures must not block the wizard
  }
}
```

### 2. Add tracking call in each wizard wrapper

In each product's main wizard component (e.g., `PrivathaftpflichtWizard.tsx`), track step changes:

```typescript
import { useEffect, useRef } from "react";

// Generate a session ID once per wizard mount
const sessionId = useRef(crypto.randomUUID());

// Track step changes
useEffect(() => {
  fetch("/api/track", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      sessionId: sessionId.current,
      product: PRODUCT_ID, // e.g., "privathaftpflicht"
      step: state.step,
      stepLabel: STEP_LABELS[state.step - 1]?.label ?? `step_${state.step}`,
    }),
  }).catch(() => {}); // never block on tracking
}, [state.step]);
```

### 3. Supabase table schema

Create `{TABLE_PREFIX}_{PRODUCT_ID}_tracking` with:

```sql
create table {TABLE_PREFIX}_{PRODUCT_ID}_tracking (
  id uuid default gen_random_uuid() primary key,
  session_id text not null,
  product text not null,
  step integer not null,
  step_label text,
  timestamp timestamptz,
  created_at timestamptz default now()
);
alter table {TABLE_PREFIX}_{PRODUCT_ID}_tracking enable row level security;
create policy "Allow anonymous inserts" on {TABLE_PREFIX}_{PRODUCT_ID}_tracking
  for insert with check (true);
create policy "Allow anonymous reads" on {TABLE_PREFIX}_{PRODUCT_ID}_tracking
  for select using (true);
```

### 4. Dashboard funnel section

The product dashboard MUST read from the tracking table and render a funnel:

```typescript
// Count distinct sessions that reached each step
const { data: funnelData } = await supabase
  .from(tableName(`${productId}_tracking`))
  .select("session_id, step, step_label");

// Group: for each step, count distinct session_ids
// Display as horizontal bars with conversion percentages
```

## Verification checklist

- [ ] `/api/track` POST returns 200
- [ ] Tracking table has rows after stepping through the wizard
- [ ] Dashboard shows funnel with per-step counts and conversion rates
- [ ] Tracking failures never block the wizard UX
