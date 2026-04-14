# ERGO Kfz/Autoversicherung — Structure Analysis

**URL**: https://www.ergo.de/de/Produkte/KFZ-Versicherung/Autoversicherung
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Same ErgoHeader                                  |
+----------------------------------------------------------+
| [HERO] .cmp-hero, bg-blue, with PriceDisplay + CTA       |
|   Image left, H1 "Kfz-Versicherung" + H2 subtitle        |
|   Price "ab 27,46 EUR monatlich" + "Beitrag berechnen"    |
+----------------------------------------------------------+
| [BENEFITS LIST] .cmp-text, bullet list of Vorteile        |
+----------------------------------------------------------+
| [CTA] Beitrag berechnen (centered, pill button)           |
+----------------------------------------------------------+
| [TEXT BLOCK] Smart vs Best comparison explanation          |
+----------------------------------------------------------+
| [IMAGE] Infographic: Smart/Best tariff diagram            |
+----------------------------------------------------------+
| [CTA] Beitrag berechnen                                   |
+----------------------------------------------------------+
| [ACCORDION x3] Bausteine sections:                        |
|   Group 1: Werkstattbonus, Wertschutz 24,                |
|            Kfz-Schutzbrief, Ersatzfahrzeug Plus (4 items) |
|   Group 2: Wertschutz 36, Rabattschutz (2 items, Best)   |
|   Group 3: GAP, Safe Drive (2 items, Flexible)            |
+----------------------------------------------------------+
| [BENEFITS CARD] "Besondere Leistungen" with Highlights    |
|   flag + icon items (3 cards with SVG icons)              |
+----------------------------------------------------------+
| [CTA BUTTON] "Alle Leistungen vergleichen" (modal opener) |
+----------------------------------------------------------+
| [TESTSIEGEL] Awards section, bg-blue, heading centered    |
|   Carousel with seal/badge images                         |
+----------------------------------------------------------+
| [PROMO] CO2-Praemie card with image + text + CTA          |
+----------------------------------------------------------+
| [SCROLL TO TOP] "Nach oben" link                          |
+----------------------------------------------------------+
| [CTA] Beitrag berechnen                                   |
+----------------------------------------------------------+
| [DOWNLOAD LIST] 3 PDF downloads in bordered cards         |
+----------------------------------------------------------+
| [CTA] Beitrag berechnen                                   |
+----------------------------------------------------------+
| [PROMO x2] Baustein use-case stories (image + text)       |
|   Werkstattbonus story, Ersatzfahrzeug Plus story         |
+----------------------------------------------------------+
| [CTA] Beitrag berechnen                                   |
+----------------------------------------------------------+
| [CLAIM SECTION] bg-magenta, "Schaden melden" + tile       |
+----------------------------------------------------------+
| [CROSS-SELL PROMOS] "Das koennte Sie auch interessieren"  |
|   Schutzbrief + Verkehrsrechtsschutz (with prices)        |
+----------------------------------------------------------+
| [ICON TILE CAROUSEL] "Rundum sicher unterwegs"            |
|   9 icon-tiles in splide carousel, pastel backgrounds     |
+----------------------------------------------------------+
| [CONTACT SECTION] "Nicht sicher, was Sie benoetigen?"     |
|   3 contact tiles: Phone, Berater, Chat                   |
+----------------------------------------------------------+
| [SCROLL TO TOP]                                           |
+----------------------------------------------------------+
| [FAQ ACCORDION] 23 items, all collapsed by default        |
+----------------------------------------------------------+
| [LEGAL DISCLAIMER] Price calculation basis + date         |
+----------------------------------------------------------+
| [SCROLL TO TOP]                                           |
+----------------------------------------------------------+
| [STICKY FOOTER] Fixed bottom bar with price + CTA         |
+----------------------------------------------------------+
| [FOOTER] Same ErgoFooter                                  |
+----------------------------------------------------------+
```

## AEM component types found

All `cmp-*` classes on this page:
`cmp-accordion`, `cmp-application-embed`, `cmp-carouselContainer`, `cmp-companyLogos`, `cmp-container`, `cmp-cta`, `cmp-download`, `cmp-footerCookies`, `cmp-footerLinks`, `cmp-footerSitemap`, `cmp-hero`, `cmp-image`, `cmp-price`, `cmp-promo`, `cmp-scrollToTop`, `cmp-search`, `cmp-socialLinks`, `cmp-stickyFooter`, `cmp-text`, `cmp-tile`

## NEW components

### 1. AccordionPanel (.cmp-accordion)

Used in two contexts: Bausteine sections (3 groups) and FAQ section (1 group with 23 items).

**Structure:**
- `.cmp-accordion` > `.cmp-accordion__item` (repeated)
  - `.cmp-accordion__button` with `.cmp-accordion__title` + `.cmp-accordion__icon`
  - `.cmp-accordion__panel` (expanded content)

**Styles:**
- Button: FS Me 18px/700, color #333, padding 16px, cursor pointer
- Item separator: border-bottom 1px solid #e1e1e1
- Icon: 16x16px chevron
- Panel (expanded): padding 16px, content 16px/24px FS Me regular
- Items can default to expanded via `data-cmp-expanded` attribute

**Bausteine groups:**
- Group 1: "Welche Bausteine kann ich waehlen?" — 4 items (Werkstattbonus, Wertschutz 24, Kfz-Schutzbrief, Ersatzfahrzeug Plus)
- Group 2: "Zusaetzliche Bausteine im Top-Tarif Best" — 2 items (Wertschutz 36, Rabattschutz)
- Group 3: "Flexible Bausteine" — 2 items (GAP, Safe Drive — Safe Drive default-expanded)

**FAQ group:** 23 items covering Haftpflicht, Teilkasko, Vollkasko, SF-Klassen, eVB, costs, etc.

### 2. BenefitsCard (.benefits__container)

Custom React component (not AEM core), loaded via separate CSS/JS. Shows product highlights with icon tiles.

**Structure:**
- `.benefits` (wrapper section)
  - `.benefits__container.is-frame.has-flag` with CSS variable `--benefit-container-color: #428071`
    - `.benefits__flag` — floating label ("Highlights")
    - `.benefits__items-wrapper`
      - `.benefits__item` > `.benefits__item-container.has-icon`
        - `.benefits__item-icon` (SVG image)
        - `.benefits__item-title`
        - `.benefits__item-text`

**Styles:**
- Flag: 14px/700, white text on #428071 (teal green), padding 4px 8px, positioned right
- Item container: padding-left 56px (icon offset)
- Item title: 16px/700, FS Me, #333
- Item text: 16px/400, #333, line-height 24px
- Icons: SVG from `/etc.clientlibs/ergoone/.../icons/` (LightningIcon, GroupIcon, ParentsIcon)

**Content on this page:** 3 items — Schutz vor Folgeschaeden, Einschluss weiterer Fahrer, Begleitetes Fahren

### 3. DownloadLink (.cmp-download)

PDF/document download card with title, filename, format, and file size.

**Structure:**
- `.cmp-download` > `a` (flex container)
  - `.cmp-download__title` — document name
  - `.cmp-download__property` (dl/dd pairs) — filename, format (pdf), size

**Styles:**
- Link: display flex, padding 16px 88px 16px 24px, border 1px solid #d9d9d9
- Title: 14px/700, #333
- No border-radius, stacked vertically (3 download cards)
- Color: #333, text-decoration none

**Files on this page:**
1. Allgemeine-Bedingungen-Kfz.pdf (971 KB)
2. kfz-leistungstabelle.pdf (36 KB)
3. broschuere-kfz-versicherung.pdf (3 MB)

### 4. StickyFooter (.cmp-stickyFooter)

Fixed bottom bar showing product name, price, and CTA. Appears on scroll past hero.

**Structure:**
- `.cmp-stickyFooter` (position: fixed, bottom: 0, z-index: 90)
  - `.cmp-stickyFooter__container` (display: grid, padding: 12px)
    - `.cmp-stickyFooter__left`
      - `.cmp-stickyFooter__product-name` — "Autoversicherung" (18px/700)
      - `.cmp-stickyFooter__tariff-details-link` — "Alle Leistungen vergleichen" (modal opener)
    - `.cmp-stickyFooter__right`
      - `.cmp-price` — "Beitrag ab 27,46 EUR monatlich"
      - `.cmp-cta__link` — "Beitrag berechnen"

**Styles:**
- Container: white bg, grid layout, padding 12px
- CTA button: bg #8e0038, white text, border-radius 100px, padding 1px 25px, 14px/700

### 5. ScrollToTop (.cmp-scrollToTop)

Simple link to scroll back to page top, used between major sections.

**Styles:**
- Display: flex
- Link: 16px/700, color #8e0038 (ERGO magenta), no text-decoration
- Text: "Nach oben"
- Appears 3 times on the page between sections

### 6. ApplicationEmbed (.cmp-application-embed)

Empty embed container (height: 0px) for "beratungsweiche-2.0" — an advisory routing widget. Not visually rendered on page load; likely activates via user interaction or JS event.

### 7. CompanyLogos (.cmp-companyLogos)

Footer-area component showing ERGO + DKV logos. Already seen on other pages — reconfirmed here.
- Images: ERGO-Logo-ohne-Claim.svg, DKV-Logo.svg

## Reused components (already cataloged)

| Component | Usage on this page |
|---|---|
| ErgoHeader | Standard fixed header, 97px |
| HeroBanner (.cmp-hero) | bg-blue (#cceced), grid layout, image+text+price+CTA |
| PriceDisplay (.cmp-price) | In hero, sticky footer, cross-sell promos |
| CTAButton (.cmp-cta__link) | Pill variant (border-radius 100px), bg #8e0038, used 7+ times |
| PromoCard (.cmp-promo) | Vertical variant only; CO2 card, Baustein stories, cross-sell cards (5 total) |
| TileCard (.cmp-tile) | Icon tiles in carousel (21 duplicated for infinite loop), contact tiles (3), claim tile (1) |
| CarouselContainer (.cmp-carouselContainer) | 4 instances: testsiegel, empty, icon-tiles (Splide), contact tiles |
| ErgoFooter | Standard footer |

## Color palette (page-specific)

| Element | Color | RGB |
|---|---|---|
| Hero bg / Testsiegel bg | bg-blue | rgb(204, 236, 239) |
| Claim section bg | bg-magenta | rgb(245, 225, 235) |
| Benefits flag | teal | rgb(66, 128, 113) / #428071 |
| CTA buttons | ERGO magenta | rgb(142, 0, 56) / #8e0038 |
| Accordion separator | light gray | rgb(225, 225, 225) / #e1e1e1 |
| Download border | lighter gray | rgb(217, 217, 217) / #d9d9d9 |
| Contact tile border | warm gray | rgb(201, 197, 199) / #c9c5c7 |

**Icon tile carousel pastel backgrounds** (rotating palette):
- rgb(245, 225, 235) — light magenta
- rgb(254, 246, 210) — light yellow
- rgb(255, 224, 203) — light peach/orange
- rgb(204, 236, 239) — light cyan
- rgb(211, 235, 229) — light green/mint

## Key style differences from other product pages

1. **No Breadcrumb** — This product page does not have a breadcrumb trail
2. **No ComparisonTable** — Tariff comparison is done via an infographic image + accordion groups, not a structured HTML table
3. **Multiple accordion groups** — Three separate accordion instances for Bausteine categories (Smart, Best, Flexible) instead of a single FAQ
4. **BenefitsCard is React-based** — Uses custom React component with separate CSS bundle, not AEM core component
5. **Heavy CTA repetition** — "Beitrag berechnen" CTA appears 7 times throughout the page
6. **StickyFooter** — Persistent bottom bar not seen on category/overview pages; specific to product detail pages

## Responsive behavior

Note: Due to headed browser session constraints, 768px and 375px screenshots rendered at the browser's minimum width (~1200px). Based on viewport meta tag and CSS breakpoint classes observed:

- The page uses `.aem-Grid--default--12` grid system
- Sections use padding utility classes: `padding-s` (12px), `padding-m` (24px), `padding-l` (48px)
- Hero converts from side-by-side (image + text) to stacked layout at mobile breakpoints
- Accordion items remain full-width at all breakpoints
- Icon tile carousel shows fewer visible tiles and pagination dots on mobile
- Contact tiles stack vertically on mobile
- Sticky footer simplifies (product name may hide, CTA remains prominent)

## Screenshot references

- `full-page-1440.png` — Desktop full-page (actual viewport ~1200px)
- `full-page-768.png` — Tablet attempt (browser minimum width applied)
- `full-page-375.png` — Mobile attempt (browser minimum width applied)
