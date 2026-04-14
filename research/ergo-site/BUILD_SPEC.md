# ERGO Site — Build Specification

**Generated**: 2026-04-13
**Source**: 8 pages analyzed via Firecrawl + Playwright
**Component catalog**: `research/ergo-site/components/CATALOG.md`

## Project structure

All new files go in the ergo-tarife Next.js project:

```
src/
├── components/
│   ├── ergo/                    # NEW — ERGO website components
│   │   ├── ErgoHeader.tsx
│   │   ├── MegaMenu.tsx
│   │   ├── HeroBanner.tsx
│   │   ├── SectionHeader.tsx
│   │   ├── PromoCard.tsx
│   │   ├── PriceDisplay.tsx
│   │   ├── CTAButton.tsx
│   │   ├── TileCard.tsx
│   │   ├── CarouselContainer.tsx
│   │   ├── ArticleTeaser.tsx
│   │   ├── ReviewSection.tsx
│   │   ├── AccordionFAQ.tsx
│   │   ├── ExpansionPanel.tsx
│   │   ├── StickyFooter.tsx
│   │   ├── PromoBanner.tsx
│   │   ├── CompanyLogos.tsx
│   │   ├── DownloadLink.tsx
│   │   ├── VideoEmbed.tsx
│   │   ├── PromoFlag.tsx
│   │   ├── Tooltip.tsx
│   │   ├── ErgoFooter.tsx
│   │   └── ProductCategorySection.tsx
│   └── ui/                      # EXISTING — tariff wizard components (untouched)
├── app/
│   ├── (site)/                  # NEW — content pages (route group)
│   │   ├── page.tsx             # Homepage (ERGO clone)
│   │   ├── layout.tsx           # ErgoHeader + ErgoFooter shell
│   │   ├── produkte/
│   │   │   ├── page.tsx         # All Products overview
│   │   │   └── [product]/
│   │   │       └── page.tsx     # Product detail pages
│   │   └── ratgeber/
│   │       └── page.tsx         # Ratgeber index
│   └── wizard/[product]/        # EXISTING — tariff wizards (untouched)
├── styles/
│   └── ergo-theme.css           # NEW — ERGO design tokens as CSS variables
└── lib/
    └── ergo-data.ts             # NEW — page content data (from Firecrawl dumps)
```

## Component build order

Build bottom-up — primitives first, compositions last.

### Phase 1: Design tokens + primitives
1. **ergo-theme.css** — CSS custom properties (colors, fonts, spacing, shadows, breakpoints)
2. **Google Fonts** — Add DM Sans + Source Serif Pro to the project
3. **CTAButton** — pill outline + arrow link + filled variants
4. **PriceDisplay** — prefix + value + currency + suffix
5. **PromoFlag** — badge overlay component
6. **SectionHeader** — label + heading + subtitle
7. **Tooltip** — use Radix Tooltip

### Phase 2: Content components
8. **TileCard** — icon card with 4 variants (icon, stat, contact, link)
9. **PromoCard** — vertical + horizontal layouts, composing PriceDisplay + CTAButton + PromoFlag
10. **ArticleTeaser** — serif headline card for blog content
11. **AccordionFAQ** — use Radix Accordion, style to match ERGO
12. **ExpansionPanel** — expandable content block
13. **DownloadLink** — document download link
14. **VideoEmbed** — YouTube embed with consent gate
15. **ReviewSection** — ekomi rating display
16. **CompanyLogos** — logo strip
17. **BenefitsCard** — feature highlights with flag label + icon items

### Phase 3: Layout components
17. **CarouselContainer** — use Embla Carousel, responsive column config
18. **HeroBanner** — full/short/storer variants
19. **PromoBanner** — thin CTA bar
20. **StickyFooter** — fixed bottom CTA bar with scroll trigger
21. **ProductCategorySection** — wrapper composing SectionHeader + PromoCard + TileCard links

### Phase 4: Global components
22. **ErgoHeader** — fixed header with logo, nav, utility bar
23. **MegaMenu** — 3-column dropdown navigation
24. **ErgoFooter** — multi-section footer

### Phase 5: Page assembly
25. **(site)/layout.tsx** — ErgoHeader + ErgoFooter shell
26. **(site)/page.tsx** — Homepage assembly
27. **(site)/produkte/page.tsx** — Products overview
28. **(site)/produkte/[product]/page.tsx** — Product detail template
29. **(site)/ratgeber/page.tsx** — Ratgeber index

## Per-component build instructions

### ergo-theme.css
```css
:root {
  /* Colors */
  --ergo-primary: #8e0038;
  --ergo-secondary: #bf1528;
  --ergo-tertiary: #71022e;
  --ergo-text: #333333;
  --ergo-text-light: #737373;
  --ergo-border: #c9c5c7;
  --ergo-border-light: #e1e1e1;
  --ergo-white: #ffffff;
  --ergo-bg-blue: #ccebed;
  --ergo-bg-green: #d3ebe5;
  --ergo-bg-yellow: #fef6d2;
  --ergo-bg-magenta: #f5e1eb;
  --ergo-flag-bg: #c34a89;
  --ergo-error: #e80c26;
  --ergo-success: #5de38e;

  /* Typography */
  --ergo-font-body: 'DM Sans', Arial, Helvetica, sans-serif;
  --ergo-font-heading: 'Source Serif Pro', Georgia, 'Times New Roman', serif;

  /* Spacing */
  --ergo-space-xxs: 4px;
  --ergo-space-xs: 12px;
  --ergo-space-s: 16px;
  --ergo-space-base: 24px;
  --ergo-space-m: 32px;
  --ergo-space-l: 48px;
  --ergo-space-xl: 64px;
  --ergo-space-xxl: 96px;

  /* Border radius */
  --ergo-radius-sm: 4px;
  --ergo-radius-lg: 8px;
  --ergo-radius-pill: 100px;
  --ergo-radius-button: 16px;

  /* Shadows */
  --ergo-shadow-sm: 0 4px 5px 0 rgba(0,0,0,.14), 0 1px 10px 0 rgba(0,0,0,.12), 0 2px 4px -1px rgba(0,0,0,.2);
  --ergo-shadow-md: 0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12);

  /* Layout */
  --ergo-max-width: 1440px;
  --ergo-header-height: 97px;
}
```

### CTAButton
- **Pill variant**: `border: 2px solid var(--ergo-primary)`, `color: var(--ergo-primary)`, `border-radius: var(--ergo-radius-pill)`, `padding: 1px 20px`, `font: 700 16px var(--ergo-font-body)`
- **Arrow variant**: no border, `padding-right: 32px`, arrow icon SVG, `color: var(--ergo-text)`, `font: 700 16px`
- **Filled variant**: `bg: var(--ergo-primary)`, `color: white`, `border-radius: var(--ergo-radius-button)`, `padding: 8px 16px`
- Hover states: pill → filled; arrow → underline; filled → darker bg

### PromoCard
- Two grid layouts controlled by `layout` prop
- Vertical: single column `grid-template-rows: auto 1fr`
- Horizontal: `grid-template-columns: 40% 60%`
- Image section: `overflow: hidden`, image covers container
- Content section: padding, contains headline + description + PriceDisplay + CTAButton(s)
- Optional PromoFlag positioned at top-right of image

### HeroBanner
- `display: grid`, `max-width: var(--ergo-max-width)`
- Full variant: `height: ~469px`, image bg, teaser overlay `width: 50%`, `padding: 64px 48px`
- Short variant: `height: ~360px`, title only
- Storer: absolute positioned badge `top: 24px, right: 24px, 96x96px`

### AccordionFAQ
- Use Radix `@radix-ui/react-accordion`
- Items separated by `border-bottom: 1px solid var(--ergo-border-light)`
- Trigger: FS Me 16px bold, expand/collapse chevron icon
- Content: padding when expanded

### StickyFooter
- `position: fixed`, `bottom: 0`, `z-index: 90`
- Hidden by default, show on scroll past hero (use IntersectionObserver)
- Left: product name + tariff name
- Right: CTA button (pill variant)
- White background, box-shadow for separation

## Per-page assembly instructions

### Homepage (`(site)/page.tsx`)
1. PromoBanner (Zahnreinigung promo)
2. HeroBanner (full variant, Sterbevorsorge)
3. SectionHeader (BESTSELLER) + CarouselContainer(3-col) of PromoCards(vertical)
4. SectionHeader (AKTUELLES) + CarouselContainer(3x2) of TileCards(icon) — bg-blue
5. SectionHeader (SERVICES) + CarouselContainer(2-col) of PromoCards(horizontal)
6. SectionHeader (KUNDENBEWERTUNGEN) + ReviewSection — bg-green
7. SectionHeader (KONTAKT) + 4-col TileCards(contact)
8. SectionHeader (WISSENSWERTES) + 3-col TileCards + seasonal promo — bg-yellow
9. SectionHeader (RATGEBER) + ArticleTeaser carousel — bg-magenta
10. SectionHeader (WARUM ERGO) + 3-col TileCards(stat)

### Products (`(site)/produkte/page.tsx`)
1. HeroBanner (short variant, "Alle ERGO Produkte")
2. ProductCategorySection × 12 (each: heading + description + PromoCard(horizontal) + sub-product links)

### Product detail (`(site)/produkte/[product]/page.tsx`)
Template page that renders based on `product` param:
1. HeroBanner (full variant with product content)
2. TileCard trust bar (3-col icons)
3. Content sections (text + images)
4. PromoCard(s) for sub-products
5. AccordionFAQ
6. CompanyLogos
7. DownloadLink(s)
8. Related PromoCards
9. StickyFooter (product-specific CTA)

### Ratgeber (`(site)/ratgeber/page.tsx`)
1. HeroBanner (short, "Ratgeber und Rechtsportal")
2. Featured PromoCard(horizontal)
3. Topic sections with SectionHeader + PromoCard grids
4. ArticleTeaser carousel (Tipps der Redaktion)

## Per-component responsive behavior

### Desktop → Tablet → Mobile

| Component | Desktop (1440px) | Tablet (768px) | Mobile (375px) |
|-----------|-----------------|----------------|----------------|
| ErgoHeader | Full nav + utils | Compressed nav | Hamburger menu |
| HeroBanner | Side-by-side | Side-by-side narrower | Stacked vertical |
| PromoCard (horiz) | Image left, content right | Stacked vertical | Stacked, full-width |
| PromoCard (vert) | Fixed width in grid | Fixed width | Full-width |
| TileCard grid | 3-4 columns | 2 columns | 1 column |
| CarouselContainer | Show all items | 2-col + nav | 1-col + swipe |
| AccordionFAQ | Full width | Full width | Full width |
| StickyFooter | Product name + CTA | Smaller text + CTA | CTA only |
| ErgoFooter | Multi-column links | 2-col links | Stacked |

## Interaction states

### CTAButton
- **Hover (pill)**: bg fills with primary color, text turns white
- **Hover (arrow)**: text underline appears
- **Hover (filled)**: darker bg (tertiary color)
- **Focus**: outline ring 2px offset

### PromoCard
- **Hover**: subtle shadow elevation (shadow-sm → shadow-md)

### TileCard
- **Hover**: background slightly darker

### AccordionFAQ
- **Hover trigger**: background tint
- **Open**: chevron rotates 180°, panel slides down

### MegaMenu
- **Active category**: red left border indicator
- **Item hover**: text color → primary

## Image strategy

- Reference ERGO's CDN URLs for `<img>` tags — all images are at `https://assets.ergo.com/content/dam/ergo/...`
- For CSS background images: use the CDN URL
- For SVG icons: reference `https://www.ergo.de/etc.clientlibs/ergoone/clientlibs/publish/assets/resources/icons/{IconName}.svg`
- Logo: use text "ERGO" styled to match, or reference the SVG at `https://www.ergo.de/content/dam/ergo/grafiken/logos/ERGO-Logo-ohne-Claim.svg`

## Link mapping

| ERGO URL pattern | Our URL | Notes |
|-----------------|---------|-------|
| `/de` | `/(site)` | Homepage |
| `/de/Produkte` | `/(site)/produkte` | Products overview |
| `/de/Produkte/<category>` | `/(site)/produkte/<category>` | Category page |
| `/de/Produkte/<category>/<product>` | `/(site)/produkte/<product>` | Product detail |
| `/de/Produkte/<product>/abschluss` | `/wizard/<product>` | Tariff wizard (existing) |
| `/de/Ratgeber` | `/(site)/ratgeber` | Ratgeber index |
| `/de/Ratgeber/*` | External → ergo.de | Not recreating articles |
| `/de/Service/*` | External → ergo.de | Not recreating |

## Dependencies to install

```bash
npm install embla-carousel-react          # Carousel
npm install @radix-ui/react-accordion     # Accordion
npm install @radix-ui/react-tooltip       # Tooltip
# Google Fonts loaded via next/font or <link> tag
```

## Validation checklist

For each rebuilt page:
1. Screenshot at 1440px, 768px, 375px
2. Compare against ERGO screenshots in `research/ergo-site/pages/<page>/`
3. Match layout exactly (per user feedback — no "improvements")
4. All links work (product cards → wizard links especially)
5. Interactive elements work (menu, accordion, carousel)
6. Fonts render correctly (DM Sans body, Source Serif Pro headings)
7. Colors match design tokens
8. StickyFooter appears on scroll (product pages only)
