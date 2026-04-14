# ERGO Rechtsschutz — Structure Analysis

**URL**: https://www.ergo.de/de/Produkte/Rechtsschutzversicherung
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Same                                             |
+----------------------------------------------------------+
| [HERO] .cmp-hero, with .cmp-hero__storer badge overlay    |
+----------------------------------------------------------+
| [TRUST BAR] TileCards with feature icons                  |
+----------------------------------------------------------+
| [CONTENT SECTIONS] Text + image blocks                    |
+----------------------------------------------------------+
| [VIDEO EMBED] .cmp-embed (YouTube video)                  |
+----------------------------------------------------------+
| [PROMO CARDS] Product variant cards in carousel           |
+----------------------------------------------------------+
| [CAROUSEL] Splide-based carousel with visible controls    |
+----------------------------------------------------------+
| [ACCORDION] FAQ sections                                  |
+----------------------------------------------------------+
| [STICKY FOOTER] Product name + CTA                       |
+----------------------------------------------------------+
| [EXPANSION PANELS] Additional expandable content          |
+----------------------------------------------------------+
| [DOWNLOAD] Document downloads                             |
+----------------------------------------------------------+
| [PROMO CARDS] Related products                            |
+----------------------------------------------------------+
| [FOOTER] Same                                             |
+----------------------------------------------------------+
```

## NEW components

### 1. FilledButton (.cmp-button)
- Different from CTAButton (.cmp-cta__link)
- **Filled variant**: bg #8e0038, white text, border-radius 16px, padding 8px 16px
- Used for consent/action buttons (e.g., "Youtube akzeptieren")
- TagName: `<a>`, display: inline-flex

### 2. VideoEmbed (.cmp-embed)
- YouTube video embed
- Dimensions: 864x486px (16:9)
- Sub-components: `__content`, `__player`, `__template`
- Requires consent button before loading

### 3. HeroStorer (.cmp-hero__storer)
- Badge/seal overlay on hero image
- Position: absolute, top: 24px, right: 24px
- Size: 96x96px
- Used for award seals (e.g., Nebenkostencheck badge)

## Key discovery: Carousel uses Splide
The carousel controls have class `splide__arrows`, confirming ERGO uses the [Splide](https://splidejs.com/) carousel library.
For our clone: can use Splide or Embla Carousel per user preference for existing libraries.

## Reused components
- HeroBanner, StickyFooter, AccordionFAQ, ExpansionPanel, DownloadLink
- PromoCard, PriceDisplay, CTAButton, TileCard, CompanyLogos
- ErgoHeader, ErgoFooter
