# Ticket 11: Dashboard Styling Overhaul

## Priority: Phase 3 (after page integration, before deploy)

## Problem

The current dashboard is functional but visually plain — basic Tailwind utility classes with no visual hierarchy, poor spacing, and no polish. It doesn't match the quality level of the wizard pages which use the ERGO design system.

## Objective

Restyle the dashboard at `src/app/dashboard/page.tsx` to look professional and polished while remaining a server component with Tailwind CSS (no UI library components needed).

## Current State

The dashboard has:
- 3 stat cards (Anträge, Ø Deckung, Beliebtester Tarif) — plain gray boxes
- Plan distribution bars — basic colored divs
- Submissions table — minimal border styling

## Visual Improvements

### Header Area
- Add a subtle gradient or branded header bar with the ERGO primary color (#8e0038)
- Larger heading with better typography hierarchy
- Subtitle with timestamp ("Stand: 11.04.2026, 16:05 Uhr")

### Stat Cards
- Add subtle box shadows (`var(--box-shadow-small)` from theme)
- Use the primary color (#8e0038) for the big number text
- Add a colored top-border accent (4px solid var(--color-primary))
- Better padding and spacing (p-8 instead of p-6)
- Responsive: stack to 1 column on mobile

### Plan Distribution
- Make the bars taller (h-8 instead of h-5) with rounded corners
- Add the percentage number INSIDE the bar (white text) when bar is wide enough
- Add subtle gradient to the bars (primary → secondary)
- Label the plan names more prominently

### Submissions Table
- Add zebra striping (alternating row backgrounds)
- Better header styling (primary color background, white text)
- Status/Tarif column: render as colored badges/chips (Grundschutz=gray, Komfort=blue, Premium=gold)
- Add hover highlight effect on rows
- Better date formatting: "11. Apr. 2026" instead of "11.4.2026"
- Coverage column: right-aligned with monospace font for numbers

### Empty State
- When no submissions: show an illustration or icon (SVG) with "Noch keine Anträge" message
- Better visual hierarchy than the current plain text

### General
- Max-width 1024px (match wizard shell)
- Add a "Zurück zum Wizard" link at top-right
- Consistent use of CSS custom properties from theme.css where possible

## Styling Approach

Continue using Tailwind CSS for the dashboard (it's a server component, separate context from the wizard). But reference the theme CSS variables for brand colors:

```css
/* Available from theme.css: */
var(--color-primary)      /* #8e0038 */
var(--color-secondary)    /* #bf1528 */
var(--color-text)         /* #333333 */
var(--color-text-muted)   /* #737373 */
var(--color-border)       /* #d9d9d9 */
var(--box-shadow-small)
var(--box-shadow-medium)
var(--border-radius-large) /* 8px */
```

## Files to Modify

- `src/app/dashboard/page.tsx` — restyle the entire page

## Agent Execution

This is a Phase 3 task. The dashboard agent (Agent H) should apply these styles during page development, or the orchestrator applies them during integration.

### Reviewer Focus
- Visual hierarchy: big numbers prominent, labels secondary
- Brand colors used consistently (primary for accents, not random Tailwind colors)
- Responsive: works on narrow and wide viewports
- Empty state handled gracefully
- Table is scannable — key data (Name, Tarif, Summe) stands out

### Tester: Page-Specific Checks
```
[CHECK] Stat cards have colored top-border accent
[CHECK] Plan distribution bars have percentage labels
[CHECK] Table headers use brand color
[CHECK] Tarif column shows colored badges
[CHECK] Empty state shows icon + message (not just text)
[CHECK] Page has "Zurück zum Wizard" link
```
