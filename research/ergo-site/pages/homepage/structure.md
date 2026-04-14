# ERGO Homepage — Structure Analysis

**URL**: https://www.ergo.de
**Viewport**: 1440x900
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Fixed, z-1000, 97px height                      |
| Logo | Nav (Versicherungen, Service, Kontakt) | Utils     |
+----------------------------------------------------------+
| [PROMO BANNER] Thin yellow bar, full-width link           |
| "100%-Flatrate für professionelle Zahnreinigungen"        |
+----------------------------------------------------------+
| [HERO] .cmp-hero, grid layout, 469px height, maxW 1440   |
| Left: Image (50%) | Right: Text overlay with             |
| title, headline, description, price, 2x CTA              |
+----------------------------------------------------------+
| [SECTION: BESTSELLER] bg-white, centered heading          |
| Label: "BESTSELLER" + H2: "Die beliebtesten Produkte"    |
| 3-col carousel of .cmp-promo cards (image+text+price+CTA)|
+----------------------------------------------------------+
| [SECTION: AKTUELLES] bg-blue (#ccebed)                    |
| Label: "AKTUELLES" + H2: "Aktionen und Produktangebote"  |
| 3x2 grid of .cmp-tile (icon+title+desc+link)             |
+----------------------------------------------------------+
| [SECTION: SERVICES] bg-white                              |
| Label: "SERVICES" + H2: "Sparen Sie Zeit..."             |
| 2-col carousel of .cmp-promo cards (larger, with images)  |
+----------------------------------------------------------+
| [SECTION: KUNDENBEWERTUNGEN] bg-green (#d3ebe5)           |
| Label + H2, blockquote, 4.6/5 rating, 387k reviews       |
+----------------------------------------------------------+
| [SECTION: KONTAKT] bg-white                               |
| Label + H2, 4-col grid of .cmp-tile (icon cards)          |
| Email | Chat | Berater | Telefon                          |
+----------------------------------------------------------+
| [SECTION: WISSENSWERTES] bg-yellow (#fef6d2)              |
| Label + H2, 3-col .cmp-tile cards                         |
| Kunden werben Kunden | Newsletter | Geschäftskunden       |
+----------------------------------------------------------+
| [SEASONAL PROMO] bg-magenta (#f5e1eb)                     |
| Image left + text right, "Frühlings-Check"                |
+----------------------------------------------------------+
| [SECTION: RATGEBER] bg-magenta (#f5e1eb)                  |
| Label + H2, horizontal carousel of articleTeaser cards     |
+----------------------------------------------------------+
| [SECTION: WARUM ERGO] bg-white                            |
| Label + H2 + tagline, 3-col .cmp-tile (icon stats)        |
| Weltweit | 31 Mio. Kunden | 100+ Jahre Erfahrung          |
+----------------------------------------------------------+
| [FOOTER] Multi-section                                    |
| Links grid | Legal | Social | Eye-Able accessibility      |
+----------------------------------------------------------+
```

## Section pattern

Every section follows the same structure:
1. **Section label** — uppercase, FS Me 18px bold, centered (e.g., "BESTSELLER")
2. **Section heading** — Fedra Serif 28px bold, centered (e.g., "Die beliebtesten Produkte")
3. **Section subtitle** — FS Me 16px normal, centered (optional)
4. **Content grid/carousel** — cards in 2-4 column layouts
5. **Section CTA** — optional "Alle X ansehen" link at bottom

## Background color alternation

Sections alternate between white and tinted backgrounds:
- `bg-blue`: `#ccebed` (rgb 204,236,239) — Aktuelles
- `bg-green`: `#d3ebe5` (rgb 211,235,229) — Kundenbewertungen  
- `bg-yellow`: `#fef6d2` (rgb 254,246,210) — Wissenswertes, Promo banner
- `bg-magenta`: `#f5e1eb` (rgb 245,225,235) — Ratgeber, Seasonal promo

## Content containers

- Max width: 1440px (--breakpoint-xxl)
- Container class: `esc_container esc_container--xxl`
- Grid system: AEM Grid with 12-column layout (`aem-Grid--12`)
- Section padding classes: `padding-s`, `padding-m`, `padding-l`, `padding-xl`

## Components identified

### 1. ErgoHeader
- **Location**: Top of page, fixed position
- **Type**: Layout / Global
- **CSS class**: `headerNavigation navigation-main`
- **Content**: 
  - ERGO logo (SVG: `content/dam/ergo/grafiken/logos/ERGO-Logo-ohne-Claim.svg`)
  - Tagline: "Einfach, weil's wichtig ist." (italic, red)
  - Main nav: 3 buttons (Versicherungen & Finanzen, Service, Kontakt)
  - Utility bar: Suche, Berater, Log-in, Phone (0800 / 3746 095)
- **Styling**:
  - Height: 97px, fixed, z-index: 1000
  - Background: white
  - Nav items: FS Me 16px, padding 12px 16px
  - Utility buttons: 48px, border-radius 8px, hover bg #fbf4f4, hover color #8e0038
- **Screenshot**: pages/homepage/full-page-1440.png (top section)
- **Reuses existing ui/ component?**: No — new ergo/ component needed
- **Responsive**: At mobile (375px) → hamburger menu, phone number hidden

### 2. MegaMenu
- **Location**: Expands below header on nav click
- **Type**: Navigation / Interactive
- **CSS class**: Part of header navigation
- **Content**: 
  - Left: Category list (Zahn, Risikoleben, Gesundheit, Hausrat, Haftpflicht, Kfz, Reise, Rechtsschutz, Vorsorge, Finanzen, Unfall)
  - Middle: Sub-category links (appears on category click, e.g., Zahn → Zahnzusatzversicherungen, Zahnzusatzversicherung mit Sofortschutz, etc.)
  - Right: Promotional card + help card
- **Styling**: Full-width overlay, white bg, left border highlight on active category (red)
- **Screenshot**: pages/homepage/screenshots/mega-menu-versicherungen.png, mega-menu-zahn.png
- **Reuses existing ui/ component?**: No — new ergo/ component needed

### 3. PromoBanner
- **Location**: Below header, above hero
- **Type**: Content / Promotional
- **CSS class**: `cta padding-top-bottom padding-s bg-yellow`
- **Content**: Single full-width link with text + arrow
- **Styling**: bg-yellow (#fef6d2), centered text, link with arrow icon
- **Reuses existing ui/ component?**: No — simple new ergo/ component

### 4. HeroBanner
- **Location**: Main hero area, below promo banner
- **Type**: Content / Landing
- **CSS class**: `cmp-hero full-width`
- **Content**:
  - Background image (full-width photo)
  - Text overlay: title ("ERGO Sterbevorsorge"), headline ("Entlasten Sie Ihre Lieben"), description, price component, 2 CTAs
- **Styling**:
  - Display: grid, height: ~469px, maxWidth: 1440px
  - Teaser overlay: padding 64px 48px, width 720px (50%)
  - Title: FS Me 16px
  - Price: FS Me 40px bold for value
- **Screenshot**: pages/homepage/full-page-1440.png (hero section)
- **Reuses existing ui/ component?**: No — new ergo/ component needed
- **Responsive**: At mobile → stacks vertically, image on top, text below

### 5. SectionHeader
- **Location**: Top of every content section
- **Type**: Typography / Layout
- **Content**: Label (uppercase) + Heading (serif) + optional subtitle
- **Styling**:
  - Label: FS Me 18px bold, uppercase, centered, #333
  - Heading: Fedra Serif 28px bold, centered, #333, line-height 1.3
  - Subtitle: FS Me 16px normal, centered
- **Reuses existing ui/ component?**: No — new ergo/ component (simple)

### 6. PromoCard
- **Location**: Bestseller section, Services section
- **Type**: Content / Product
- **CSS class**: `cmp-promo`
- **Content**: Image, optional badge/seal overlay, headline, description, price, CTA link
- **Variants**: 
  - Product card (3-col): image top, text bottom, compact
  - Service card (2-col): side-by-side or larger layout
- **Styling**:
  - Background: white, border-radius: 8px, border: 1px solid #c9c5c7
  - Display: grid, overflow: hidden
  - Headline: FS Me 16px, color: black
  - Optional flag: bg #c34a89, white text, border-radius 0 0 8px 8px, padding 6px 12px
- **Screenshot**: pages/homepage/full-page-1440.png (bestseller section)
- **Reuses existing ui/ component?**: Could extend Card but significantly different — new ergo/ component

### 7. PriceDisplay
- **Location**: Inside HeroBanner and PromoCards
- **Type**: Content / Data
- **CSS class**: `cmp-price`
- **Content**: Prefix ("Z. B." or "Ab"), value (e.g., "27,02"), currency ("EUR"), suffix ("monatlich")
- **Styling**:
  - Display: flex, align-items: center
  - Value: FS Me 40px bold (hero), or smaller in cards
  - Variants: `--size-auto`, `--size-medium`, `--color-regular`
- **Reuses existing ui/ component?**: No — new ergo/ component

### 8. CTAButton
- **Location**: Throughout page
- **Type**: Interactive / Navigation
- **CSS class**: `cmp-cta__link`
- **Variants**:
  - **Primary (pill)**: border-radius 100px, border 2px solid #8e0038, color #8e0038, transparent bg, padding 1px 20px, 16px bold
  - **Arrow link**: border-radius 8px, no border, padding-right 32px (arrow icon), color #333, 16px bold
- **Reuses existing ui/ component?**: Could extend Button with new variants — recommend new ergo/ component wrapping ui/Button

### 9. TileCard
- **Location**: Aktuelles, Kontakt, Wissenswertes, Warum ERGO sections
- **Type**: Content / Navigation
- **CSS class**: `cmp-tile`
- **Content**: Icon (SVG, 48px), title, description text, optional CTA link
- **Variants**: 
  - Icon + title + desc + link (Aktuelles — bg-blue cards)
  - Icon + label + stat (Warum ERGO — e.g., "Weltweit / in über 20 Ländern")
  - Icon + title + desc + link (Kontakt — smaller cards)
- **Styling**:
  - Background: varies by section (blue, green, yellow, etc.)
  - Border-radius: 8px, padding: 48px 32px
  - Display: flex, flex-direction: column, text-align: center
  - Title: FS Me 18px bold
  - Icon: height 48px
- **Count**: 16 total across page
- **Reuses existing ui/ component?**: No — new ergo/ component needed

### 10. ReviewSection (Ekomi)
- **Location**: Kundenbewertungen section
- **Type**: Content / Social proof
- **CSS class**: `cmp-ekomi__rating-container`
- **Content**: Blockquote with customer review, rating (4.6/5), review count (387,143), company name
- **Styling**: bg-green section, centered layout
- **Reuses existing ui/ component?**: No — new ergo/ component

### 11. ArticleTeaser
- **Location**: Ratgeber section
- **Type**: Content / Blog
- **CSS class**: `cmp-articleTeaser`
- **Content**: Headline (serif), subhead, description text, CTA link
- **Styling**:
  - Background: #f5e1eb (magenta), border-radius: 8px, padding: 48px 32px
  - Display: flex
  - Headline: Fedra Serif 24px bold, color #8e0038
- **In carousel**: `cmp-articleTeaserCarousel`, horizontal scroll with navigation
- **Reuses existing ui/ component?**: No — new ergo/ component

### 12. CarouselContainer
- **Location**: Wraps Bestseller cards, Services cards, Ratgeber articles
- **Type**: Interactive / Layout
- **CSS class**: `cmp-carousel__container`
- **Content**: Child cards in horizontal scroll with prev/next navigation
- **Variants by columns**:
  - `has-2-cols-m has-3-cols-l` (Bestseller)
  - `has-2-cols-m has-2-cols-l` (Services)
  - `has-2-cols-m has-4-cols-l` (some sections)
  - `has-3-cols-m has-3-cols-l` (some sections)
- **Modifier**: `is-homogeneous` (equal height cards)
- **Reuses existing ui/ component?**: No — new ergo/ component

### 13. ErgoFooter
- **Location**: Bottom of page
- **Type**: Layout / Global
- **Content**: Link grid (45 links), legal section, social media, Eye-Able accessibility widget
- **Styling**: Container `esc_container--xxl`, text color #333, links no text-decoration, font 16px
- **Reuses existing ui/ component?**: No — new ergo/ component needed

## Responsive behavior summary

### Desktop (1440px)
- Header: Full nav visible with all utility items
- Hero: Side-by-side (image + text overlay)
- Card grids: 3-column (Bestseller, Aktuelles), 2-column (Services)
- Contact: 4-column grid

### Tablet (768px)
- Header: Nav still visible but compressed
- Hero: Image and text still side-by-side but narrower
- Card grids: 2-column throughout
- Contact: 2x2 grid
- Carousel navigation becomes visible

### Mobile (375px)
- Header: Hamburger menu, phone number hidden
- Hero: Stacked vertically — image top, text below
- Card grids: Single column
- CTAs: Full width
- All carousels show one card at a time with swipe
