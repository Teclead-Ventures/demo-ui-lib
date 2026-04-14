# ERGO Zahnzusatzversicherung — Structure Analysis

**URL**: https://www.ergo.de/de/Produkte/Zahnzusatzversicherung
**Viewport**: 1440x900
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] ErgoHeader (reused) — fixed, 97px               |
| Logo | Nav (Versicherungen, Service, Kontakt) | Utils     |
+----------------------------------------------------------+
| [HERO] .cmp-hero, grid, bg-orange (#ffe0cb), 360px h     |
| Left: Text (H1 + subtitle + description)                 |
| Right: Family photo                                       |
| grid-template-columns: 0 720px 720px 0                   |
+----------------------------------------------------------+
| [SECTION: WHY] bg-white, text block                       |
| H2: "Warum ist eine Zahnzusatzversicherung sinnvoll?"    |
| Body paragraph                                            |
+----------------------------------------------------------+
| [SECTION: PRODUCT OVERVIEW] bg-white                      |
| H2: "Die Zahnzusatzversicherungen der ERGO im Überblick"|
| 3x PromoCard (.cmp-promo) — horizontal layout             |
|   1. Individueller Zahnschutz (bg-yellow, with badge)     |
|   2. Sofortschutz (bg-pink)                               |
|   3. Kieferorthopaedie (bg-white, border)                 |
+----------------------------------------------------------+
| [SECTION: TESTSIEGEL] bg-blue (#ccecef)                   |
| H2: "Die ERGO Zahnzusatzversicherungen – immer wieder    |
| ausgezeichnet"                                            |
| Carousel: TestSiegel images + ekomi 4.6/5 rating          |
| Splide carousel, 2-col layout, pagination dots            |
+----------------------------------------------------------+
| [SECTION: ZAHNERHALT] bg-white                            |
| H3: "Zahnversicherungen für Zahnerhalt"                  |
| SubProductCard carousel (1 item): Dental-Vorsorge         |
+----------------------------------------------------------+
| [SECTION: ZAHNERSATZ] bg-white                            |
| H3: "Zahnversicherungen für Zahnersatz"                  |
| SubProductCard carousel (3 items):                        |
|   - Verdoppelter Festzuschuss                             |
|   - Dental-Schutz                                         |
|   - Zahnersatz mit Implantaten                            |
+----------------------------------------------------------+
| [SECTION: SOFORTLEISTUNG] bg-white                        |
| H3: "Zahnzusatzversicherungen mit Sofortleistung"        |
| SubProductCard carousel (2 items):                        |
|   - Zahnzusatzversicherung mit Sofortschutz               |
|   - Kieferorthopädie Sofort                               |
+----------------------------------------------------------+
| [SECTION: DKV CROSS-SELL] bg-white                        |
| H2: "Die Zahnzusatzversicherungen der DKV"               |
| PromoCard (.cmp-promo) — horizontal, bg-green (#d3ebe5)  |
+----------------------------------------------------------+
| [SECTION: QUICK LINKS] bg-white                           |
| H2: "Ihr Lächeln ist uns wichtig!"                       |
| QuickLinkTile carousel (9 items, 3-col, Splide)           |
| Icon tiles with colored backgrounds                       |
+----------------------------------------------------------+
| [SECTION: CONTACT] bg-white                               |
| H2: "Nicht sicher, was Sie benötigen?"                   |
| ContactTile carousel (3 items, 3-col):                    |
|   - Telefon | Berater | Chat                              |
+----------------------------------------------------------+
| [SECTION: BERATER FORM] applicationembed                  |
| Address input form for finding ERGO Berater               |
+----------------------------------------------------------+
| [SECTION: DOWNLOAD] bg-white                              |
| H2: "Wissenswertes für Sie zum Download"                 |
| DownloadLink (.cmp-download) — PDF link card              |
+----------------------------------------------------------+
| [SECTION: FAQ] bg-white                                   |
| H2: "FAQs - Häufige gestellte Fragen..."                |
| Accordion (.cmp-accordion) — 18 FAQ items                 |
+----------------------------------------------------------+
| [SECTION: DISCLAIMER] bg-white                            |
| Small print + "Zur Beitragstabelle" button                |
+----------------------------------------------------------+
| [FOOTER] ErgoFooter (reused)                              |
+----------------------------------------------------------+
```

## All components identified

### REUSED from homepage/products page

| Component | CSS Class | Notes |
|---|---|---|
| ErgoHeader | `.esc_container .new-navigation` | Fixed, 97px, identical |
| HeroBanner | `.cmp-hero.full-width` | Same grid layout, different bg color (orange #ffe0cb vs blue) |
| PromoCard | `.cmp-promo` | Horizontal grid variant (image left, content right). 4 instances with different bg colors |
| PriceDisplay | `.cmp-price` | Inside PromoCards for products with pricing |
| CTAButton | `.cmp-cta__link` | Arrow variant for "Mehr erfahren" and "zum Produkt" |
| TileCard | `.cmp-tile` | Used in QuickLinks and Contact sections |
| CarouselContainer | `.cmp-carousel__container` | 6 instances, Splide.js, various column configs |
| ReviewSection | ekomi rating | Inside TestSiegel carousel, 4.6/5 stars |
| ErgoFooter | `contentinfo` | Identical 4-column layout |

### NEW components

| Component | CSS Class | Status |
|---|---|---|
| **FAQ Accordion** | `.cmp-accordion` | NEW |
| **SubProductCard** | `.cmp-tile` (in carousel) | NEW variant of TileCard |
| **TestSiegel Carousel** | `.cmp-carousel__container` (with award images) | NEW content pattern |
| **DownloadLink** | `.cmp-download` | NEW |
| **QuickLinkTile** | `.cmp-tile` (icon + label + colored bg) | NEW variant of TileCard |
| **ContactTile** | `.cmp-tile` (icon + title + desc + CTA) | NEW variant of TileCard |
| **DisclaimerSection** | `.experienceFragment` (with Beitragstabelle btn) | NEW |
| **ScrollToTop** | `.scrollToTop` | NEW (simple anchor link) |

## NEW component details

### 1. FAQ Accordion (`.cmp-accordion`)

**Container**: `.accordion.panelcontainer`
```
CSS class:    .cmp-accordion
Items:        18 FAQ questions
Border:       none on container
```

**Each Item**: `.cmp-accordion__item`
```
border-bottom:  1px solid rgb(225, 225, 225)  (#e1e1e1)
padding:        0
```

**Button**: `.cmp-accordion__button`
```
display:          flex
justify-content:  space-between
align-items:      center
padding:          16px
font-size:        16px (button) / 18px (title inside, bold)
font-weight:      400 (button) / 700 (title)
font-family:      "FS Me", Arial, Helvetica, sans-serif
color:            rgb(51, 51, 51)  (#333)
background:       transparent
border:           none
cursor:           default (changes on hover)
```

**Title**: `.cmp-accordion__title.txt.txt--headline.txt__h1`
```
font-size:    18px
font-weight:  700
```

**Icon**: `.cmp-accordion__icon`
```
width:        16px
height:       16px
display:      block
mask-image:   url("...ChevronDownIcon.svg")
transform:    matrix(1,0,0,1,0,0) — rotates 180deg when expanded
transition:   transform 0.2s ease-in-out
```

**Content structure**:
```
.cmp-accordion
  .cmp-accordion__item
    h3.cmp-accordion__header
      button.cmp-accordion__button
        span.cmp-accordion__title   (question text, bold)
        span.cmp-accordion__icon    (chevron, mask-image SVG)
    div.cmp-accordion__panel        (answer content, hidden by default)
```

### 2. SubProductCard (`.cmp-tile` in sub-product carousels)

Used for linking to specific product sub-pages (Zahnerhalt, Zahnersatz, Sofortleistung).

```
Container:      .cmp-carousel__container.has-2-cols-m.has-2-cols-l.is-homogeneous
Items per row:  2 at desktop (non-initialized Splide, rendered as grid)
```

**Tile**: `.cmp-tile`
```
display:        flex
flex-direction: column
padding:        24px 80px 24px 32px
background:     rgb(255, 255, 255)  (#fff)
border:         1px solid rgb(201, 197, 199)  (#c9c5c7)
border-radius:  8px
box-shadow:     none
```

**Internal structure**:
```
div.tile.cta
  div.cmp-tile
    p.cmp-tile__title        (18px, bold, #333)
    div.cmp-tile__text       (16px, regular, #333)
    div.cmp-tile__cta-wrapper
      div.cmp-cta
        a.cmp-cta__link      ("zum Produkt", arrow variant, 16px, #333)
```

### 3. TestSiegel Carousel

Awards section on tinted blue background (#ccecef).

```
Container:     .cmp-carousel__container.has-2-cols-m.has-2-cols-l.is-initialized
Layout:        Splide carousel, 2-col per view
Background:    rgb(204, 236, 239)  (#ccecef) — applied to parent .bg-blue
Padding:       48px 12px (from parent)
```

**Slide types**:
- `image.splide__slide` — Stiftung Warentest seals (PNG images)
- `experienceFragment.splide__slide` — ekomi rating widget (star icon + "4,6/5" + "387.143 Bewertungen")

**Siegel image URLs**:
- `assets.ergo.com/.../dentaltarif-ds75-ds90-ds100-dvb-dve-25nt40.dam.png`
- `assets.ergo.com/.../dentalschutz-ds75-ds90-ds100-25zx67.dam.png`
- `assets.ergo.com/.../dentalschutz-ds75-24ty61.dam.png`

**Pagination**: 2 pages, dot indicators + prev/next buttons

### 4. QuickLinkTile (`.cmp-tile` with icon + colored bg)

"Ihr Lächeln ist uns wichtig!" section — icon action tiles.

```
Container:     .cmp-carousel__container.has-2-cols-m.has-3-cols-l.is-homogeneous.is-initialized
Layout:        Splide carousel, 3-col per view at desktop
Pagination:    3 pages, dot indicators
```

**Tile**: `.cmp-tile`
```
display:          flex
flex-direction:   column
align-items:      stretch
justify-content:  center
padding:          24px 80px 24px 104px
min-height:       96px
border:           none
border-radius:    8px
box-shadow:       none
```

**Colored backgrounds** (vary per tile):
- `rgb(245, 225, 235)` — pink (#f5e1eb) — "Zahnrechnung einreichen"
- `rgb(254, 246, 210)` — yellow (#fef6d2) — "Schon in Behandlung?"
- `rgb(255, 224, 203)` — orange (#ffe0cb) — "Prof. Zahnreinigung"

**Icon**: 48x48px SVG from ERGO CDN
**Title**: 18px, bold, #333
**Link**: wraps entire tile

**Icon URLs** (ERGO CDN path pattern):
```
/etc.clientlibs/ergoone/clientlibs/publish/assets/resources/icons/{Name}Icon.svg
```
Icons: DocumentIcon, DentalRepairIcon, DentalToothCleaningIcon, DentalImplantIcon,
ChecklistIcon, ShieldIcon, ToothIcon, MoneyIcon, HeartIcon

### 5. ContactTile (`.cmp-tile` in contact carousel)

"Nicht sicher, was Sie benötigen?" section.

```
Container:     .cmp-carousel__container.has-2-cols-m.has-3-cols-l.is-homogeneous
Layout:        3 items (not scrollable at desktop)
```

**Tile**: `.cmp-tile`
```
display:        flex
padding:        48px 32px
background:     rgb(255, 255, 255)  (#fff)
border-radius:  8px
```

**Items**:
1. **Telefon**: PhoneIcon + "7-24 Uhr" + "Rufen Sie an!" + phone link (0800/3746420)
2. **Berater**: ManIcon + "Ihr ERGO Berater" + "Gleich Termin vereinbaren!" + button
3. **Chat**: ChatIcon + "Per Chat" + "Ein Klick und los gehts!" + button

**CTA link/button**: 
```
color:          rgb(142, 0, 56)  (#8e0038) — ERGO brand magenta
border-radius:  100px (pill)
padding:        1px 20px
background:     transparent
```

### 6. DownloadLink (`.cmp-download`)

```
display:      block
```

**Link wrapper**: `a`
```
display:        flex
padding:        16px 88px 16px 24px
background:     rgb(255, 255, 255)  (#fff)
border:         1px solid rgb(217, 217, 217)  (#d9d9d9)
border-radius:  8px
text-decoration: none
color:          rgb(51, 51, 51)  (#333)
```

**Internal structure**:
```
.cmp-download
  a (href to .pdf)
    h3.cmp-download__title     (14px, bold)
    dl.cmp-download__properties (display: contents)
      dt + dd (filename)
      dt + dd (format: pdf)
      dt + dd (size: |712 KB)
```

### 7. DisclaimerSection

Small print text + link button at bottom of page.

```
Container:    .experienceFragment.experiencefragment
Background:   transparent
```

**Paragraph**: 14px, #333, legal disclaimer text
**Button**: "Zur Beitragstabelle"
```
display:        flex
background:     transparent
color:          rgb(142, 0, 56)  (#8e0038)
border:         none
border-radius:  100px
padding:        1px 0px
font-size:      14px
```

## Key style differences from homepage

| Aspect | Homepage | Zahnzusatz |
|---|---|---|
| Hero bg color | Blue tones | Orange (#ffe0cb) |
| Hero height | 469px | 360px |
| Hero grid | 4-column with named areas | Same pattern, grid-rows: 360px |
| Section labels | "BESTSELLER", "AKTUELLES" etc. | No section labels — direct H2/H3 headings |
| Background sections | Blue, green, yellow alternating | Only blue (#ccecef) for TestSiegel |
| PromoCard count | 3+ in carousel | 4 standalone (stacked vertically) |
| PromoCard bg colors | Varies | Yellow, pink, white, green |
| Has FAQ accordion | No | Yes (18 items) |
| Has download link | No | Yes (PDF brochure) |
| Has sub-product lists | No | Yes (3 categorized link groups) |
| Has quick-link tiles | No | Yes (9 icon action tiles) |
| Has TestSiegel | No | Yes (Stiftung Warentest badges carousel) |

## Heading typography

| Level | Font Size | Weight | Font Family | Line Height |
|---|---|---|---|---|
| H1 | 18px | 700 | FS Me, Arial | 23.4px |
| H2 | 28px | 700 | FS Me, Arial | 36.4px |
| H3 (section) | 24px | 700 | FS Me, Arial | 31.2px |
| H3 (accordion) | 18px | 700 | FS Me, Arial | - |

Note: H1 is smaller than H2 on this page (18px vs 28px). The H1 serves as a label-like element inside the hero, while H2s are the actual section headings.

## Color palette (page-specific)

| Usage | Color | Hex |
|---|---|---|
| Hero background | rgb(255, 224, 203) | #ffe0cb |
| TestSiegel section bg | rgb(204, 236, 239) | #ccecef |
| PromoCard 1 bg (yellow) | rgb(254, 246, 210) | #fef6d2 |
| PromoCard 2 bg (pink) | rgb(245, 225, 235) | #f5e1eb |
| PromoCard 4 bg (green) | rgb(211, 235, 229) | #d3ebe5 |
| Accordion divider | rgb(225, 225, 225) | #e1e1e1 |
| Tile border | rgb(201, 197, 199) | #c9c5c7 |
| Brand magenta (CTAs) | rgb(142, 0, 56) | #8e0038 |
| Body text | rgb(51, 51, 51) | #333333 |
| Download border | rgb(217, 217, 217) | #d9d9d9 |

## AEM grid structure

The page uses Adobe Experience Manager's responsive grid:
```
main.esc_container.new-navigation
  section.esc_container.esc_container--xxl
    div.root.responsivegrid
      div.aem-Grid.aem-Grid--12
        [28 grid children, each spanning full 12 columns]
```

Each child uses classes like `aem-GridColumn--default--12` (full-width) combined with:
- Component type: `hero`, `text`, `promo`, `carouselContainer`, `accordion`, `download`, etc.
- Padding: `padding-m` (24px 12px), `padding-l` (48px 12px), `padding-s` (12px)
- Padding position: `padding-top`, `padding-bottom`, `padding-top-bottom`
- Background: `bg-blue`, `bg-orange`, `bg-no-color`

## Responsive behavior

### 768px (tablet)
- Hero: Image stacks above text (single column)
- PromoCards: Image stacks above content (single column)
- TestSiegel carousel: Still 2-col, Splide active
- Sub-product cards: Stack vertically
- QuickLink tiles: 2-col carousel
- Contact tiles: Stack vertically
- FAQ accordion: Full-width, unchanged
- Footer: 2-column grid

### 375px (mobile)
- Header: Hamburger menu replaces nav
- Hero: Full-width stacked, image on top
- PromoCards: Full-width stacked, image on top
- TestSiegel: 1-col carousel
- All tile carousels: 1-col, swipeable
- Sub-product cards: Full-width stacked
- Contact tiles: Full-width stacked
- FAQ accordion: Full-width, slightly smaller padding
- Download link: Full-width
- Footer: Single column

## Splide.js carousel configuration

All carousels use Splide.js library with these observed configurations:

| Carousel | Desktop cols | Tablet cols | Mobile cols | Loop | Initialized |
|---|---|---|---|---|---|
| TestSiegel | 2 | 2 | 1 | Yes | Yes |
| Zahnerhalt | 2 | 2 | 1 | No | No (1 item) |
| Zahnersatz | 2 | 2 | 1 | No | No (3 items) |
| Sofortleistung | 2 | 2 | 1 | No | No (2 items) |
| QuickLinks | 3 | 2 | 1 | Yes | Yes |
| Contact | 3 | 2 | 1 | No | No (3 items) |

Non-initialized carousels render their items in a simple grid/flex layout instead.

## Screenshots

- `full-page-1440.png` — Desktop (1440px)
- `full-page-768.png` — Tablet (768px)
- `full-page-375.png` — Mobile (375px)
