# ERGO Sterbegeld — Structure Analysis

**URL**: https://www.ergo.de/de/Produkte/Sterbegeldversicherungen/Sterbegeldversicherung
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Same                                             |
+----------------------------------------------------------+
| [HERO] .cmp-hero, image + text overlay, price, 2 CTAs    |
+----------------------------------------------------------+
| [TRUST BAR] 3-col TileCards (icons: trust features)       |
+----------------------------------------------------------+
| [CONTENT] Text sections with headings                     |
+----------------------------------------------------------+
| [PRICING TABLE] Comparison/pricing section                |
+----------------------------------------------------------+
| [ACCORDION] FAQ / expandable Q&A sections (29 items!)     |
+----------------------------------------------------------+
| [EXPANSION PANEL] Expandable info panels                  |
+----------------------------------------------------------+
| [DOWNLOAD] Downloadable documents section                 |
+----------------------------------------------------------+
| [COMPANY LOGOS] Trust/partner logos (2 logos)              |
+----------------------------------------------------------+
| [PROMO CARDS] Related product cards                       |
+----------------------------------------------------------+
| [STICKY FOOTER] Fixed bottom bar with product + CTA      |
| (display:none by default, shows on scroll)                |
+----------------------------------------------------------+
| [FOOTER] Same                                             |
+----------------------------------------------------------+
```

## NEW components (first seen here)

### 1. AccordionFAQ (.cmp-accordion)
- 29 accordion items on this page
- Structure: `.cmp-accordion__item` → `.cmp-accordion__header` + `.cmp-accordion__panel`
- Item separator: `border-bottom: 1px solid #e1e1e1`
- Title: FS Me 16px bold, #333
- Expand/collapse icon: `.cmp-accordion__icon`
- Panel: hidden until expanded

### 2. StickyFooter (.cmp-stickyFooter)
- Fixed bottom bar, position: fixed, bottom: 0, z-index: 90
- White background, contains product name + CTA button
- `display: none` by default — appears on scroll past hero
- Sub-components: `__container`, `__left`, `__right`, `__product`, `__tariff`

### 3. ExpansionPanel (.cmp-expansionPanel)
- Similar to accordion but different styling
- Button text: e.g., "Aufbauzeit ab Vertragsbeginn"
- Expandable content panel

### 4. CompanyLogos (.cmp-companyLogos)
- Logo strip with partner/trust logos
- 2 logo items on this page
- Simple grid/flex layout

### 5. DownloadLink (.cmp-download)
- Downloadable document link
- Title + file properties (size, type)
- Example: "Informationen Bestattungspakete"

### 6. Tooltip (.cmp-tooltip)
- Info tooltip on hover/click
- Button trigger + dialog popup

## Reused components
- HeroBanner, PromoCard, PriceDisplay, CTAButton, TileCard, ErgoHeader, ErgoFooter
