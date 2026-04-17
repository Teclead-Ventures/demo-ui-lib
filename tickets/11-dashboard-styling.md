# Ticket 11: Dashboard Styling — Zahnzusatzversicherung

## Priority: Phase 3 (after pages integrated)

## Note

This ticket is a styling review/polish pass after the initial dashboard (ticket 08) is live.
Full visual spec is in `10-dashboard.md`. This ticket focuses on polish items to check after first render.

## Polish Checklist

After dashboard renders:

- [ ] Stat card values are `#8e0038` (Weinrot), not default black
- [ ] Plan distribution bar fill is `#8e0038`, track is `#f0f0f0`
- [ ] Table header row background `#f8f8f8`, no Tailwind interference
- [ ] Font is DM Sans (inherits from root) — no system fallback visible
- [ ] Mobile: stat cards collapse to 1 column at < 600px
- [ ] Mobile: table scrolls horizontally, no overflow clipping
- [ ] "Noch keine Anträge" empty state is centered, color `#737373`
- [ ] Border radius 8px on all cards and table wrapper
- [ ] No console errors on page load

## Common Issues

| Symptom | Fix |
|---------|-----|
| Stat values show in black | Check `color: "#8e0038"` on the `<p>` inside stat card |
| Font looks like Arial | Ensure `font-family: var(--font-family, 'DM Sans', Arial, sans-serif)` on root div |
| Table overflows on narrow screen | Add `overflowX: "auto"` to table wrapper div |
| Bar fill doesn't show at 0% | `width: "0%"` still renders — check `minWidth` not set to anything unexpected |
