# ERGO Design System — Component Catalog

**Compiled**: 2026-04-13
**Pages analyzed**: 8 (Homepage, Products, Zahnzusatz, Kfz, Sterbegeld, Haftpflicht, Rechtsschutz, Ratgeber)
**Firecrawl scrapes used**: 8 of 500

## Summary

- **Total unique components**: 23
- **Can reuse from existing ui/**: 0 (existing components are form/wizard-focused)
- **Need to create in ergo/**: 23
- **Can leverage existing libraries**: Embla Carousel (or Splide), Radix Accordion

## Design Tokens (global)

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#8e0038` | Brand burgundy — CTAs, links, headings, logo |
| Secondary | `#bf1528` | Red accent |
| Tertiary | `#71022e` | Dark brand |
| Text | `#333333` | Body text |
| Text light | `#737373` | Secondary text |
| Border | `#c9c5c7` / `#e1e1e1` | Card borders, dividers |
| Background white | `#ffffff` | Main background |
| bg-blue | `#ccebed` | Section tint |
| bg-green | `#d3ebe5` | Section tint |
| bg-yellow | `#fef6d2` | Section tint, promo banner |
| bg-magenta | `#f5e1eb` | Section tint |
| Error | `#e80c26` | Error state |
| Success | `#5de38e` | Success state |
| Flag/badge bg | `#c34a89` | PromoCard flag |

### Typography
| Role | Font | Size (desktop) | Weight | Line-height |
|------|------|----------------|--------|-------------|
| Body | DM Sans* | 16px | 400 | 1.5 |
| Section label | DM Sans* | 18px | 700 | 1.3 |
| Section heading | Source Serif Pro* | 28px | 700 | 1.3 |
| Sub-heading | Source Serif Pro* | 24px | 700 | 1.3 |
| Card title | DM Sans* | 18px | 700 | 1.3 |
| Price value | DM Sans* | 40px | 700 | 1.2 |
| Button | DM Sans* | 16px | 700 | — |
| Caption | DM Sans* | 14px | 400 | 1.5 |

*Google Fonts alternatives for ERGO's FS Me (→ DM Sans) and Fedra Serif (→ Source Serif Pro)

### Spacing scale
| Token | Value |
|-------|-------|
| xxs | 4px |
| xs | 12px |
| s | 16px |
| base | 24px |
| m | 32px |
| l | 48px |
| xl | 64px |
| xxl | 96px |

### Border radius
| Size | Value |
|------|-------|
| small | 4px |
| large | 8px |
| pill | 100px (CTA buttons) |
| button | 16px (filled buttons) |

### Shadows
| Level | Value |
|-------|-------|
| none | none |
| small | `0 4px 5px 0 rgba(0,0,0,.14), 0 1px 10px 0 rgba(0,0,0,.12), 0 2px 4px -1px rgba(0,0,0,.2)` |
| medium | `0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12)` |

### Breakpoints
| Name | Value |
|------|-------|
| xs | 320px |
| s | 480px |
| m (tablet) | 768px |
| l | 912px |
| xl | 1152px |
| xxl (desktop) | 1440px |

---

## Components

### 1. ErgoHeader
- **Type**: Layout / Global
- **Pages**: All
- **ERGO class**: `headerNavigation navigation-main`
- **Description**: Fixed header with logo, tagline, main nav (3 items), utility bar (search, berater, login, phone)
- **Variants**: Default, Scrolled (compact — not confirmed)
- **Props**: `currentPage`, `onSearch`, `onMenuToggle`
- **Key styles**: height 97px, fixed, z-1000, white bg
- **Responsive**: Mobile → hamburger menu, utility items hidden
- **Reuses**: None

### 2. MegaMenu
- **Type**: Navigation / Interactive
- **Pages**: All (part of header)
- **Description**: 3-column dropdown — categories left, sub-categories middle, promo cards right
- **Props**: `categories[]`, `activeCategory`, `promoCard`
- **Key styles**: Full-width overlay, white bg, red left-border on active category
- **Responsive**: Mobile → full-screen slide-in menu

### 3. HeroBanner
- **Type**: Content / Landing
- **ERGO class**: `cmp-hero full-width`
- **Pages**: All pages (different content per page)
- **Variants**:
  - **Full** (homepage): 469px, image + text overlay + price + 2 CTAs
  - **Short** (products/category): 360px, image + title + subtitle only
  - **With storer**: badge overlay (96x96px) at top-right
- **Props**: `image`, `title`, `headline`, `description`, `price?`, `ctas?`, `storerImage?`
- **Key styles**: display: grid, maxWidth: 1440px, teaser width 720px (50%), padding 64px 48px
- **Responsive**: Mobile → stacked, image top, text below

### 4. SectionHeader
- **Type**: Typography / Layout
- **Pages**: Homepage, Products
- **Description**: Centered section label + serif heading + optional subtitle
- **Props**: `label`, `heading`, `subtitle?`
- **Key styles**: label: DM Sans 18px bold uppercase centered, heading: Source Serif Pro 28px bold centered
- **Reuses**: None — standalone component

### 5. PromoCard
- **Type**: Content / Product
- **ERGO class**: `cmp-promo`
- **Pages**: All
- **Variants**:
  - **Vertical** (homepage bestsellers): image top, content bottom
  - **Horizontal** (products page): image left 40%, content right 60% (gridTemplateColumns: ~493px ~739px)
- **Props**: `image`, `badge?`, `flag?`, `headline`, `description`, `price?`, `ctas[]`, `layout: "vertical" | "horizontal"`
- **Key styles**: bg white, border-radius 8px, border 1px solid #c9c5c7, display: grid, overflow: hidden
- **Responsive**: Horizontal → vertical at tablet

### 6. PriceDisplay
- **Type**: Content / Data
- **ERGO class**: `cmp-price`
- **Pages**: Homepage, Products, Product detail
- **Props**: `prefix`, `value`, `currency`, `suffix`, `size: "auto" | "medium"`
- **Key styles**: display flex, value: DM Sans 40px bold (hero) / smaller in cards
- **Reuses**: None

### 7. CTAButton
- **Type**: Interactive / Navigation
- **ERGO class**: `cmp-cta__link`
- **Pages**: All
- **Variants**:
  - **Pill outline**: border-radius 100px, border 2px solid #8e0038, color #8e0038, transparent bg
  - **Arrow link**: no border, padding-right 32px for arrow, color #333
- **Props**: `href`, `label`, `variant: "pill" | "arrow"`, `icon?`
- **Key styles**: 16px bold, DM Sans

### 8. FilledButton
- **Type**: Interactive / Action
- **ERGO class**: `cmp-button`
- **Pages**: Rechtsschutz (consent), possibly others
- **Description**: Solid filled button — different from CTAButton outline
- **Props**: `href`, `label`
- **Key styles**: bg #8e0038, color white, border-radius 16px, padding 8px 16px, 16px bold
- **Note**: May be combined with CTAButton as a `variant: "filled"` option

### 9. TileCard
- **Type**: Content / Navigation
- **ERGO class**: `cmp-tile`
- **Pages**: Homepage (Aktuelles, Kontakt, Wissenswertes, Warum ERGO), Product pages (trust bar)
- **Variants**:
  - **Icon card**: icon + title + text + CTA (Aktuelles section)
  - **Stat card**: icon + number + label (Warum ERGO section)
  - **Contact card**: icon + title + description (Kontakt)
  - **Link item**: title + arrow CTA (Products page sub-product links)
- **Props**: `icon?`, `title`, `text?`, `cta?`, `stat?`, `variant`
- **Key styles**: bg varies, border-radius 8px, padding 48px 32px, flex column, text-align center
- **Responsive**: Grid collapses to fewer columns

### 10. CarouselContainer
- **Type**: Interactive / Layout
- **ERGO class**: `cmp-carousel__container`
- **Pages**: Homepage, Products, Product detail
- **Description**: Responsive carousel with column variants
- **Props**: `columns: { mobile: number, tablet: number, desktop: number }`, `homogeneous: boolean`
- **Key styles**: Splide-based carousel; variants: 2-col/3-col/4-col at different breakpoints
- **Library**: ERGO uses Splide; we'll use Embla Carousel per user preference
- **Column patterns**: `has-2-cols-m has-3-cols-l`, `has-2-cols-m has-4-cols-l`, etc.

### 11. ArticleTeaser
- **Type**: Content / Blog
- **ERGO class**: `cmp-articleTeaser`
- **Pages**: Homepage (Ratgeber section), Ratgeber page
- **Props**: `headline`, `subhead`, `text`, `cta`
- **Key styles**: bg #f5e1eb, border-radius 8px, padding 48px 32px, headline: Source Serif Pro 24px bold #8e0038

### 12. ReviewSection
- **Type**: Content / Social proof
- **ERGO class**: `cmp-ekomi__rating-container`
- **Pages**: Homepage, some product pages
- **Props**: `quote`, `rating`, `reviewCount`, `companyName`
- **Key styles**: bg-green section, centered layout

### 13. AccordionFAQ
- **Type**: Interactive / Content
- **ERGO class**: `cmp-accordion`
- **Pages**: Product detail pages (Sterbegeld: 29 items, Rechtsschutz, Kfz, etc.)
- **Props**: `items: { title: string, content: ReactNode }[]`
- **Key styles**: items separated by border-bottom 1px solid #e1e1e1, title: 16px bold, expandable panel
- **Library**: Can use Radix Accordion

### 14. ExpansionPanel
- **Type**: Interactive / Content
- **ERGO class**: `cmp-expansionPanel`
- **Pages**: Sterbegeld, Rechtsschutz, product detail pages
- **Description**: Expandable info section — similar to Accordion but for larger content blocks
- **Props**: `buttonText`, `children`
- **Key styles**: Button 13px, toggle icon, expandable panel

### 15. StickyFooter
- **Type**: Layout / Interactive
- **ERGO class**: `cmp-stickyFooter`
- **Pages**: Product detail pages
- **Description**: Fixed bottom bar with product name + CTA, appears on scroll past hero
- **Props**: `productName`, `tariffName?`, `ctaHref`, `ctaLabel`
- **Key styles**: position: fixed, bottom: 0, z-index: 90, white bg, display: none → shows on scroll

### 16. PromoBanner
- **Type**: Content / Promotional
- **Pages**: Homepage (top)
- **Description**: Thin full-width CTA bar below header
- **Props**: `text`, `href`
- **Key styles**: bg-yellow, centered text link with arrow

### 17. CompanyLogos
- **Type**: Content / Trust
- **ERGO class**: `cmp-companyLogos`
- **Pages**: Product detail pages
- **Props**: `logos: { src: string, alt: string }[]`
- **Key styles**: Simple flex/grid layout for logo images

### 18. DownloadLink
- **Type**: Content / Document
- **ERGO class**: `cmp-download`
- **Pages**: Product detail pages
- **Props**: `title`, `href`, `fileSize?`, `fileType?`
- **Key styles**: Block link with title + file properties

### 19. VideoEmbed
- **Type**: Content / Media
- **ERGO class**: `cmp-embed`
- **Pages**: Rechtsschutz
- **Description**: YouTube video embed with consent gate
- **Props**: `videoId`, `width?`, `height?`
- **Key styles**: 16:9 aspect ratio, 864x486px, consent button before loading

### 20. PromoFlag
- **Type**: Content / Badge
- **ERGO class**: `cmp-promo__flag`
- **Pages**: Homepage, Products, Product detail
- **Description**: Badge overlay on PromoCards (e.g., "Aktion bis 31.12.2026")
- **Props**: `text`, `variant?`
- **Key styles**: bg #c34a89, white text, border-radius 0 0 8px 8px, padding 6px 12px
- **Note**: Can be part of PromoCard rather than standalone

### 21. Tooltip
- **Type**: Interactive / UI
- **ERGO class**: `cmp-tooltip`
- **Pages**: Product detail pages
- **Props**: `triggerLabel`, `content`
- **Key styles**: Button trigger + dialog popup
- **Library**: Can use Radix Tooltip

### 22. BenefitsCard
- **Type**: Content / Feature highlights
- **ERGO class**: `.benefits__container` (custom React component, not AEM core)
- **Pages**: Kfz product page
- **Description**: Feature highlight card with flag label ("Highlights") and icon+title+text items
- **Props**: `flagLabel`, `flagColor`, `items: { icon: string, title: string, text: string }[]`
- **Key styles**: Flag: 14px/700, white on teal #428071; items with 48px SVG icons
- **Note**: Unlike other components, this is a standalone React component with its own CSS bundle, separate from ERGO's AEM CMS components

### 23. ErgoFooter
- **Type**: Layout / Global
- **Pages**: All
- **Description**: Multi-section footer — link grid (45+ links), legal, social, Eye-Able
- **Sub-components**: `cmp-footerLinks`, `cmp-footerSitemap`, `cmp-footerCookies`, `cmp-socialLinks`
- **Key styles**: Text #333, links no decoration, 16px (content), 14px (legal)
- **Responsive**: Columns collapse to stacked on mobile

---

## Component dependency graph

```
ErgoHeader
├── MegaMenu
│   └── PromoCard (mini variant for promo slot)
│
HeroBanner
├── PriceDisplay
├── CTAButton
└── PromoFlag (storer variant)
│
SectionHeader (standalone)
│
PromoCard
├── PriceDisplay
├── CTAButton
├── PromoFlag
│
TileCard (standalone, multiple variants)
│
CarouselContainer
├── PromoCard[]
├── TileCard[]
├── ArticleTeaser[]
│
AccordionFAQ (standalone, use Radix)
ExpansionPanel (standalone)
StickyFooter
├── CTAButton
│
ErgoFooter (standalone)
```

## Icon library

16+ SVG icons referenced from ERGO's CDN:
```
https://www.ergo.de/etc.clientlibs/ergoone/clientlibs/publish/assets/resources/icons/
```
Icons: RiskIcon, DentalOrthodonticsIcon, HobbyIcon, BrokenArmIcon, HospitalIcon, HandsMoneyIcon, MailIcon, ChatIcon, LocationIcon, PhoneIcon, MegaphoneIcon, BusinessCardIcon, StoreIcon, GlobeIcon, GroupIcon, HandshakeIcon

**Strategy**: Reference ERGO CDN URLs directly, don't download.

## ERGO Logo

SVG: `https://www.ergo.de/content/dam/ergo/grafiken/logos/ERGO-Logo-ohne-Claim.svg`
Tagline: "Einfach, weil's wichtig ist." (italic, brand color)
