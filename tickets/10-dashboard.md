# Ticket 10: Dashboard — Berufsunfähigkeitsversicherung

## Priority: Phase 2 (parallel with wizard pages)

## Objective

Build an analytics dashboard at `/dashboard` that reads all BU applications from Supabase and displays stats + submissions table.

## Visual Specification

```
┌─────────────────────────────────────────────────┐
│  BU-Versicherung — Antrags-Dashboard            │  ← page title
│                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐│
│  │ Gesamt   │ │ Ø Rente  │ │ Beliebtester     ││
│  │    12    │ │ 1.850 €  │ │ Tarif: Komfort   ││
│  └──────────┘ └──────────┘ └──────────────────┘│
│                                                  │
│  Tarifverteilung                                 │
│  Grundschutz ████░░░░░░░░  25 %                 │
│  Komfort     ████████░░░░  58 %                 │
│  Premium     ████░░░░░░░░  17 %                 │
│                                                  │
│  Letzte Anträge                                  │
│  # │ Name           │ Tarif   │ BU-Rente │ Datum│
│  1 │ Weber, Markus  │ Komfort │ 2.000 €  │ ...  │
│  2 │ Hoffmann, Sand.│ Premium │ 1.800 €  │ ...  │
└─────────────────────────────────────────────────┘
```

## Files to Create

### `src/app/dashboard/page.tsx`

```tsx
import { supabase, tableName, isSupabaseConfigured } from "@/lib/supabase";

export const dynamic = "force-dynamic";

interface BUApplication {
  id: string;
  created_at: string;
  occupation: string;
  birth_date: string;
  monthly_income: string;
  coverage_amount: string;
  plan: string;
  monthly_price: string;
  payment_duration_years: number;
  smoker: string;
  pre_existing_conditions: string;
  salutation: string;
  first_name: string;
  last_name: string;
  zip: string;
  city: string;
}

const PLAN_LABELS: Record<string, string> = {
  grundschutz: "Grundschutz",
  komfort: "Komfort",
  premium: "Premium",
};

export default async function DashboardPage() {
  let rows: BUApplication[] = [];

  if (isSupabaseConfigured()) {
    const { data } = await supabase
      .from(tableName("bu_applications"))
      .select("*")
      .order("created_at", { ascending: false });
    rows = (data as BUApplication[]) ?? [];
  }

  const total = rows.length;
  const avgCoverage = total > 0
    ? Math.round(rows.reduce((s, r) => s + parseInt(r.coverage_amount), 0) / total)
    : 0;

  const planCounts = rows.reduce((acc, r) => {
    acc[r.plan] = (acc[r.plan] ?? 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const topPlan = Object.entries(planCounts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "–";

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "48px 24px", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, color: "#333", marginBottom: 32 }}>
        BU-Versicherung — Antrags-Dashboard
      </h1>

      {/* Stat cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 32 }}>
        {[
          { label: "Gesamte Anträge", value: String(total) },
          { label: "Ø BU-Rente", value: total > 0 ? `${avgCoverage.toLocaleString("de-DE")} €/Mo.` : "–" },
          { label: "Beliebtester Tarif", value: PLAN_LABELS[topPlan] ?? topPlan },
        ].map((s) => (
          <div key={s.label} style={{ backgroundColor: "#fff", border: "1px solid #e5e5e5", borderRadius: 8, padding: 20, textAlign: "center" }}>
            <p style={{ fontSize: 32, fontWeight: 700, color: "#8e0038", margin: "0 0 4px" }}>{s.value}</p>
            <p style={{ fontSize: 14, color: "#737373", margin: 0 }}>{s.label}</p>
          </div>
        ))}
      </div>

      {/* Plan distribution */}
      <div style={{ backgroundColor: "#fff", border: "1px solid #e5e5e5", borderRadius: 8, padding: 24, marginBottom: 32 }}>
        <h2 style={{ fontSize: 18, fontWeight: 700, color: "#333", marginBottom: 16 }}>Tarifverteilung</h2>
        {["grundschutz", "komfort", "premium"].map((plan) => {
          const count = planCounts[plan] ?? 0;
          const pct = total > 0 ? Math.round((count / total) * 100) : 0;
          return (
            <div key={plan} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
              <span style={{ width: 120, fontSize: 14, color: "#333" }}>{PLAN_LABELS[plan]}</span>
              <div style={{ flex: 1, backgroundColor: "#f0f0f0", borderRadius: 4, height: 12 }}>
                <div style={{ width: `${pct}%`, backgroundColor: "#8e0038", borderRadius: 4, height: "100%" }} />
              </div>
              <span style={{ width: 40, fontSize: 14, color: "#737373", textAlign: "right" }}>{pct}%</span>
            </div>
          );
        })}
      </div>

      {/* Submissions table */}
      <div style={{ backgroundColor: "#fff", border: "1px solid #e5e5e5", borderRadius: 8, overflow: "hidden" }}>
        <div style={{ padding: "16px 24px", borderBottom: "1px solid #e5e5e5" }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: "#333", margin: 0 }}>Letzte Anträge</h2>
        </div>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f8f8f8" }}>
              {["#","Name","Tarif","BU-Rente","Datum"].map((h) => (
                <th key={h} style={{ padding: "12px 16px", textAlign: "left", fontSize: 12, fontWeight: 600, color: "#737373", borderBottom: "1px solid #e5e5e5" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={row.id} style={{ borderBottom: "1px solid #f0f0f0" }}>
                <td style={{ padding: "12px 16px", fontSize: 14, color: "#737373" }}>{i + 1}</td>
                <td style={{ padding: "12px 16px", fontSize: 14, color: "#333" }}>{row.last_name}, {row.first_name}</td>
                <td style={{ padding: "12px 16px", fontSize: 14, color: "#333" }}>{PLAN_LABELS[row.plan] ?? row.plan}</td>
                <td style={{ padding: "12px 16px", fontSize: 14, color: "#333" }}>{parseInt(row.coverage_amount).toLocaleString("de-DE")} €/Mo.</td>
                <td style={{ padding: "12px 16px", fontSize: 14, color: "#737373" }}>{new Date(row.created_at).toLocaleDateString("de-DE")}</td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr><td colSpan={5} style={{ padding: "24px 16px", textAlign: "center", color: "#737373", fontSize: 14 }}>Noch keine Anträge vorhanden.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}
```

## Gate

```bash
npm run dev
# http://localhost:3000/dashboard → renders without crash
# After submitting via wizard → new row appears in table
```
