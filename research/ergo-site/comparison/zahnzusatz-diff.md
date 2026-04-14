# Zahnzusatz Page Visual Comparison — Diff Report

**Date**: 2026-04-14
**ERGO URL**: https://www.ergo.de/de/Produkte/Zahnzusatzversicherung
**Demo URL**: http://localhost:5174/ergo-zahnzusatz.html
**Viewport**: 1440x900

## Fixes applied during comparison

### Round 1 (initial build → fix pass)
1. **Hero image position** — image spanned full width, hiding bgColor → CSS fix: `.ergo-hero--text-left .ergo-hero__image { grid-column: 2 }` and transparent teaser bg
2. **Hero headline style** — not italic on ERGO product pages → CSS fix: `.ergo-hero--text-left .ergo-hero__headline { font-style: italic; color: var(--color-primary) }`
3. **Section headings** — were left-aligned, ERGO centers them → added `textAlign: "center"` to h2Style
4. **Body text** — was left-aligned, ERGO centers it → added `textAlign: "center"` and `margin: "16px auto 0"` to bodyStyle

## Sections verified

| Section | Status | Notes |
|---------|--------|-------|
| Hero (orange bg) | OK | Text left, image right, bgColor #ffe0cb visible |
| "Why" section | OK | Centered H2 + body text |
| Product overview (3 PromoCards) | OK | Yellow/pink/white bg, flag, prices, CTAs |
| TestSiegel (blue bg) | OK | 3 test seal images + ekomi rating 4.6/5 |
| Sub-products (Zahnerhalt) | OK | 1 tile card with "zum Produkt" |
| Sub-products (Zahnersatz) | OK | 3 tile cards |
| Sub-products (Sofortleistung) | OK | 2 tile cards |
| DKV cross-sell | OK | Green bg PromoCard |
| QuickLinks (9 tiles) | OK | 3-col grid, colored backgrounds, ERGO icons |
| Contact (3 tiles) | OK | Phone, Berater, Chat |
| Download link | OK | PDF brochure card |
| FAQ accordion (18 items) | OK | Centered heading, expandable items |
| Disclaimer | OK | Small print + Beitragstabelle button |
| StickyFooter | OK | Shows on scroll, "Beitrag berechnen" CTA |
| Footer | OK | Standard 4-column layout |

## Remaining minor differences

1. [CONTENT] Review section shows empty quotes ("") since we pass empty string. ERGO has no visible quote on this page. Acceptable.
2. [STYLE] ERGO's PromoCard CTAs on zahnzusatz are filled red buttons ("Mehr erfahren"), our demo uses arrow variant. Minor visual difference.
3. [LAYOUT] ERGO's QuickLink tiles have slight padding/icon positioning differences. Acceptable for demo.

## Overall assessment

All major page sections render correctly with accurate content, colors, and layout. The page closely matches the ERGO Zahnzusatzversicherung product detail page. Ready for commit.
