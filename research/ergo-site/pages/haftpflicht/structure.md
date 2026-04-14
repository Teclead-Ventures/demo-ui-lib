# ERGO Haftpflicht — Structure Analysis

**URL**: https://www.ergo.de/de/Produkte/Haftpflichtversicherung
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Same                                             |
+----------------------------------------------------------+
| [HERO] .cmp-hero, shorter variant, title + subtitle       |
+----------------------------------------------------------+
| [PRODUCT GRID] Multiple PromoCards in 2-col grid          |
| (PHV, Haus & Grund, Bauherren, Gewässer, Jagd, etc.)     |
+----------------------------------------------------------+
| [CONTACT SECTION] TileCards (contact options)             |
+----------------------------------------------------------+
| [ACCORDION] Vorteile einer Haftpflichtversicherung        |
+----------------------------------------------------------+
| [COMPANY LOGOS] Partner logos                              |
+----------------------------------------------------------+
| [FOOTER] Same                                             |
+----------------------------------------------------------+
```

## NEW components: None
All components already cataloged. This page is a product category overview (like Products page) but for a single category.

## Key observation
Layout pattern is: Hero → Product grid (PromoCards) → Info sections → Accordion FAQ → Footer.
This is the same pattern as the full Products page but scoped to one category.

## Reused components
- HeroBanner (shorter variant), PromoCard (vertical, 2-col grid), PriceDisplay, CTAButton
- AccordionFAQ, CompanyLogos, TileCard, ErgoHeader, ErgoFooter
