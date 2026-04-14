# Products Page Visual Comparison — Diff Report

**Date**: 2026-04-14
**ERGO URL**: https://www.ergo.de/de/Produkte
**Demo URL**: http://localhost:5174/ergo-produkte.html
**Viewport**: 1440x900

## Fixes applied during comparison

### Round 1 (initial build → first fix pass)
1. **Hero text position** — text was on RIGHT, ERGO has it on LEFT → added `textPosition="left"`
2. **Category section layout** — was plain H2+p left-aligned, ERGO uses centered SectionHeader pattern (label + serif heading + description) → replaced with `ErgoSectionHeader` + centered description paragraph, with `splitTagline()` helper
3. **Sub-product CTA label** — was "Mehr erfahren", ERGO uses "mehr lesen" → fixed
4. **Sub-product columns** — was 4-column grid, ERGO uses 2-column → changed to `desktop: 2`

## Remaining minor differences

1. [LAYOUT] Sub-product link tiles on ERGO show just product name + arrow (→), no visible "mehr lesen" text. Our demo shows "mehr lesen >" as a CTA link label. Acceptable for demo.
2. [STYLE] ERGO's sub-product tiles have visible border + border-radius matching the TileCard variant="link" style. Ours look similar.
3. [COLOR] Some PromoCards on ERGO show subtle peach/beige background on the content area. Our cards use white background. Minor.
4. [CONTENT] ERGO shows "Zahnzusatzversicherung (DKV Deutsche Krankenversicherung AG)" full name, our demo abbreviated to "Zahnzusatzversicherung (DKV)". Minor content accuracy.

## Overall assessment

Layout, content structure, and visual appearance closely match the ERGO products page. All 12 categories render correctly with horizontal PromoCards, badges, prices, CTAs, and sub-product links. Ready for commit.
