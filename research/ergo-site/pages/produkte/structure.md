# ERGO Products Page — Structure Analysis

**URL**: https://www.ergo.de/de/Produkte
**Viewport**: 1440x900
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Same as homepage — fixed, 97px                   |
+----------------------------------------------------------+
| [PAGE HERO] .cmp-hero, 360px (shorter than homepage 469px)|
| Image bg + "Alle ERGO Produkte" title + subtitle          |
+----------------------------------------------------------+
| [CATEGORY SECTION] ×12 — repeating pattern:               |
|                                                           |
|   H2: "ZAHNZUSATZVERSICHERUNGEN" (uppercase, FS Me 18px) |
|   Description paragraph (FS Me 16px)                      |
|                                                           |
|   +--PromoCard (horizontal)---------------------------+   |
|   | Image (40%)  |  Content: headline, desc, price,   |   |
|   |              |  badge, 2 CTAs                      |   |
|   +--------------------------------------------------+   |
|                                                           |
|   Sub-product links (carousel, 2-4 cols):                 |
|   [Title + "mehr lesen"] [Title + "mehr lesen"] ...       |
+----------------------------------------------------------+
| ... repeats for 12 categories ...                         |
+----------------------------------------------------------+
| [FOOTER] Same as homepage                                 |
+----------------------------------------------------------+
```

## Product categories (12 total)

| # | Category | Featured product | Sub-products |
|---|----------|-----------------|-------------|
| 1 | Zahnzusatzversicherungen | Individueller Zahnschutz (24,70€) | 7 links |
| 2 | Lebensversicherungen | Risikolebensversicherung (1,97€) | 2 links |
| 3 | Rechtsschutzversicherungen | Rechtsschutzversicherung (12,17€) | 2 links |
| 4 | Rentenversicherungen | Private Rentenversicherung (25€) | 4 links |
| 5 | Krankenversicherungen | DKV Krankenhauszusatz (6,40€) | 6 links |
| 6 | Haftpflichtversicherungen | Private Haftpflicht (5,26€) | 7 links |
| 7 | Unfall-/BU-/Grundfähigkeit | Unfallversicherung (1,89€) | 2 links |
| 8 | Pflegeversicherungen | Pflegezusatzversicherung | 2 links |
| 9 | Kfz-Versicherungen | Autoversicherung (27,46€) | 6 links |
| 10 | Hausrat- & Gebäudeversicherungen | Hausratversicherung (3,90€) | 6 links |
| 11 | Reiseversicherungen | Auslandskranken (9,90€/Jahr) | 9 links |
| 12 | Bausparen & Finanzprodukte | ERGO Kidspolicen | 5 links |

## Key differences from homepage

1. **PromoCard layout**: HORIZONTAL (image left 40%, content right 60%) vs homepage VERTICAL (image top, content bottom)
   - Grid: `gridTemplateColumns: 492.797px 739.188px`
   - Same `.cmp-promo` component, different variant
2. **Page hero**: Shorter (360px vs 469px), no price/CTAs — just title + subtitle
3. **No section labels**: Categories use H2 headings directly (not the label+heading pattern)
4. **Sub-product link lists**: New pattern — `.cmp-tile` items in carousel containers with "mehr lesen" arrow links
5. **No alternating backgrounds**: Page is mostly white with `bg-gray` (transparent) — simpler than homepage

## Components identified

### NEW components (not seen on homepage)

#### 1. ProductCategorySection
- **Type**: Layout / Content
- **Content**: Category heading + description + featured PromoCard + sub-product links
- **Repeats**: 12 times on this page
- **Styling**: White background, standard content padding
- **Note**: This is the main structural component for the products page. Could be a wrapper that composes existing components.

#### 2. SubProductLinkList
- **Type**: Navigation / Content
- **CSS class**: `.cmp-carousel__container` wrapping `.cmp-tile` items
- **Content**: Product name + "mehr lesen" arrow link, per item
- **Styling**: `.cmp-tile__cta-wrapper`, padding-top: 32px, display: contents
- **Layout**: 2-4 column carousel container
- **Count**: 12 list containers, varying item counts (2-9 per category)
- **Note**: Uses the same `.cmp-tile` as homepage TileCard but in a simpler variant (no icon, just title+link)

### REUSED components (same as homepage)

| Component | Variant/Notes |
|-----------|--------------|
| ErgoHeader | Identical |
| HeroBanner (.cmp-hero) | **Shorter variant** — 360px height, title-only (no price/CTA) |
| PromoCard (.cmp-promo) | **Horizontal variant** — image left, content right (vs homepage vertical) |
| PriceDisplay (.cmp-price) | Same |
| CTAButton | Same pill + arrow variants |
| PromoFlag (.cmp-promo__flag) | Same badge overlay |
| ErgoFooter | Identical |

### PromoCard horizontal variant details
```
.cmp-promo (horizontal):
  display: grid
  gridTemplateColumns: ~493px ~739px  (≈40% image, 60% content)
  
  .cmp-promo__image-container: order 0 (left)
  .cmp-promo__content: order 0 (right)
  
Same internal structure: headline, description, price, CTAs, optional badge
```

## Responsive behavior

### Desktop (1440px)
- PromoCards: horizontal layout (image left, content right)
- Sub-product links: 2-4 column grid
- Full page hero visible

### Tablet (768px)
- PromoCards: Stack vertically (image top, content bottom) — same as homepage cards
- Sub-product links: 2-column grid
- Hero: Narrower but same layout

### Mobile (375px)
- PromoCards: Full-width stacked
- Sub-product links: Single column
- Hero: Fully stacked
- CTAs: Full-width
