# ERGO Homepage — Component & Design Token Reference

**Extracted**: 2026-04-13 from https://www.ergo.de at 1440px viewport

## Design Tokens (from CSS :root custom properties)

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| `--theme-primary` | `#8e0038` | Brand primary (dark red/burgundy) |
| `--theme-secondary` | `#bf1528` | Brand secondary (red) |
| `--theme-tertiary` | `#71022e` | Brand dark |
| `--theme-brand-color` | `#8e0038` | Same as primary |
| `--theme-brand-color-dark` | `#71022e` | Darker brand |
| `--theme-white` | `#fff` | White |
| `--theme-lightest-gray` | `#f2f2f2` | Lightest gray bg |
| `--theme-lighter-gray` | `#e1e1e1` | Lighter gray |
| `--theme-light-gray` | `#d9d9d9` | Light gray / borders |
| `--theme-medium-gray` | `#c8c8c8` | Medium gray |
| `--theme-dark-gray` | `#aeaeae` | Dark gray |
| `--theme-darker-gray` | `#737373` | Darker gray |
| `--theme-darkest-gray` | `#333` | Body text color |
| `--theme-black` | `#000` | Black |
| `--theme-error-color` | `#e80c26` | Error red |
| `--theme-success-color` | `#5de38e` | Success green |
| `--theme-additional-1` | `#b31767` | Magenta |
| `--theme-additional-2` | `#009284` | Teal |
| `--theme-additional-3` | `#0f94a7` | Cyan |
| `--theme-additional-4` | `#f6cb00` | Yellow |
| `--theme-additional-5` | `#e87a16` | Orange |
| `--theme-additional-6` | `#545241` | Olive |

### Section background tints (computed)
| Class | RGB | Hex (approx) | Used for |
|-------|-----|------|----------|
| `bg-blue` | `rgb(204,236,239)` | `#ccebed` | Aktuelles |
| `bg-green` | `rgb(211,235,229)` | `#d3ebe5` | Kundenbewertungen |
| `bg-yellow` | `rgb(254,246,210)` | `#fef6d2` | Wissenswertes, promo banner |
| `bg-magenta` | `rgb(245,225,235)` | `#f5e1eb` | Ratgeber, seasonal |
| `bg-orange` | transparent | — | Hero (uses image bg) |

### Typography
| Token | Value |
|-------|-------|
| `--font-family-fedra` | `Fedra Serif, Georgia, Times New Roman, serif` |
| `--font-family-fsme` | `FS Me, Arial, Helvetica, sans-serif` |
| `--base--font-family` | `FS Me, Arial, Helvetica, sans-serif` (body) |
| `--base--heading--font-family` | `Fedra Serif, Georgia, Times New Roman, serif` |
| `--base--font-size` | `14px` (small), `16px` (large screen) |
| `--base--line-height` | `1.5` |
| `--font-weight-normal` | `400` |
| `--font-weight-bold` | `700` |

#### Heading sizes (large screen)
| Level | Size | Use on ERGO |
|-------|------|-------------|
| `--text-base--large-screen__claim__font-size` | `40px` | Main claims |
| `--text-base--large-screen__h2__font-size` | `28px` | Section headings |
| `--text-base--large-screen__h3__font-size` | `24px` | Sub-headings |
| `--text-base--large-screen__h4__font-size` | `20px` | Card titles |
| `--text-base--large-screen__teaser__font-size` | `18px` | Teaser/label text |
| `--text-base--large-screen__paragraph__font-size` | `16px` | Body text |
| `--text-base--large-screen__caption__font-size` | `14px` | Captions |

#### Heading sizes (small screen)
| Level | Size |
|-------|------|
| `--text-base--small-screen__claim__font-size` | `28px` |
| `--text-base--small-screen__h2__font-size` | `24px` |
| `--text-base--small-screen__h3__font-size` | `20px` |
| `--text-base--small-screen__teaser__font-size` | `16px` |
| `--text-base--small-screen__paragraph__font-size` | `14px` |

### Spacing
| Token | Value |
|-------|-------|
| `--spacing` | `8px` (base unit) |
| `--gap--xxs` | `4px` |
| `--gap--xs` | `12px` |
| `--gap--s` | `16px` |
| `--gap` | `24px` |
| `--gap--m` | `32px` |
| `--gap--l` | `48px` |
| `--gap--xl` | `64px` |
| `--gap--xxl` | `96px` |
| `--column-gap` | `24px` |

### Border radius
| Token | Value |
|-------|-------|
| `--base--border-radius--small` | `4px` |
| `--base--border-radius--large` | `8px` |

### Shadows
| Token | Value |
|-------|-------|
| `--base--box-shadow--smallest` | `none` |
| `--base--box-shadow--small` | `0 4px 5px 0 rgba(0,0,0,.14), 0 1px 10px 0 rgba(0,0,0,.12), 0 2px 4px -1px rgba(0,0,0,.2)` |
| `--base--box-shadow--medium` | `0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12)` |
| `--base--box-shadow--large` | `0 6px 6px -3px rgba(0,0,0,.2), 0 10px 14px 1px rgba(0,0,0,.14), 0 4px 18px 3px rgba(0,0,0,.12)` |

### Breakpoints
| Token | Value |
|-------|-------|
| `--breakpoint-xxl` | `1440px` |
| `--breakpoint-xl` | `1152px` |
| `--breakpoint-l` | `912px` |
| `--breakpoint-m` | `768px` |
| `--breakpoint-s` | `480px` |
| `--breakpoint-xs` | `320px` |

### Header
| Token | Value |
|-------|-------|
| `--header-height` | `73px` (CSS var, actual computed: 97px) |
| `--header-border-color` | `#d9d9d9` |
| `--header-button-size` | `48px` |
| `--header-button-icon-size` | `24px` |
| `--header-button-border-radius` | `8px` |
| `--header-button-background-color-hover` | `#fbf4f4` |
| `--header-button-color-hover` | `#8e0038` |

---

## Fonts

ERGO uses two custom web fonts:
1. **FS Me** — Sans-serif, used for body text, labels, buttons, navigation
2. **Fedra Serif** — Serif, used for section headings (h2, h3)

**Builder note**: These are commercial fonts. For the clone:
- FS Me → Use `"FS Me", Arial, Helvetica, sans-serif` (fallback chain)
- Fedra Serif → Use `"Fedra Serif", Georgia, "Times New Roman", serif` (fallback chain)
- Consider loading from ERGO's CDN or using close Google Fonts alternatives (DM Sans / Source Serif Pro)

---

## Component Style Reference

### SectionHeader
Pattern used in every content section:
```
Label: FS Me 18px bold, uppercase, centered, color #333
H2:    Fedra Serif 28px bold, centered, color #333, line-height 1.3
Sub:   FS Me 18px/16px, centered, color #333 (optional)
```

### CTAButton variants
```
Primary (pill):
  border-radius: 100px
  border: 2px solid #8e0038
  color: #8e0038
  background: transparent
  padding: 1px 20px
  font: FS Me 16px bold

Arrow link:
  border-radius: 8px
  border: none
  color: #333
  padding-right: 32px (space for arrow icon)
  font: FS Me 16px bold
```

### PromoCard (.cmp-promo)
```
background: white
border-radius: 8px
border: 1px solid #c9c5c7
display: grid
overflow: hidden
padding: 0

Image: full-width top section, overflow hidden
Flag badge: bg #c34a89, white, padding 6px 12px, bottom-rounded (0 0 8px 8px)
Content: padded section below image
```

### TileCard (.cmp-tile)
```
background: varies by section (blue/green/yellow)
border-radius: 8px
padding: 48px 32px
display: flex
flex-direction: column
text-align: center
border: none

Icon: height 48px, centered
Title: FS Me 18px bold, #333
Text: FS Me 16px, #333
```

### PriceDisplay (.cmp-price)
```
display: flex
align-items: center

Prefix (.cmp-price__prefix): regular weight
Value (.cmp-price__value): FS Me 40px bold (hero) / smaller in cards
Currency (.cmp-price__currency): smaller
Suffix (.cmp-price__suffix): regular weight, "monatlich"
```

### HeroBanner (.cmp-hero)
```
display: grid
height: ~469px
max-width: 1440px

Image: .cmp-hero__image — full background
Teaser: .cmp-hero__teaser — padding 64px 48px, width 720px (50%)
Title: .cmp-hero__teaser-title
Headline: .cmp-hero__teaser-headline
Text: .cmp-hero__teaser-text
```

### ArticleTeaser (.cmp-articleTeaser)
```
background: #f5e1eb (magenta section)
border-radius: 8px
padding: 48px 32px
display: flex

Headline: Fedra Serif 24px bold, color #8e0038
Subhead: .cmp-articleTeaser__subhead
Text: .cmp-articleTeaser__text
CTA: .cmp-articleTeaser__cta
```

### CarouselContainer
```
Column variants (responsive):
  has-2-cols-m has-3-cols-l → 2 cols tablet, 3 cols desktop
  has-2-cols-m has-2-cols-l → 2 cols all
  has-2-cols-m has-4-cols-l → 2 cols tablet, 4 cols desktop
  has-3-cols-m has-3-cols-l → 3 cols all

Modifier: is-homogeneous → equal height cards
Navigation: .cmp-carousel__navigation (hidden at desktop when all items visible)
```

### PromoFlag (.cmp-promo__flag)
```
background: #c34a89
color: white
border-radius: 0 0 8px 8px
padding: 6px 12px
font-size: 16px
position: absolute top-right of card
```

---

## Icon library

ERGO uses inline SVG icons from their CMS:
```
Base path: /etc.clientlibs/ergoone/clientlibs/publish/assets/resources/icons/
```

Icons found on homepage:
- RiskIcon.svg (Risikoleben)
- DentalOrthodonticsIcon.svg (Kieferorthopädie)
- HobbyIcon.svg (BU)
- BrokenArmIcon.svg (Unfall)
- HospitalIcon.svg (Krankenhaus)
- HandsMoneyIcon.svg (Basis-Rente)
- MailIcon.svg (E-Mail)
- ChatIcon.svg (Chat)
- LocationIcon.svg (Berater)
- PhoneIcon.svg (Telefon)
- MegaphoneIcon.svg (Kunden werben)
- BusinessCardIcon.svg (Newsletter)
- StoreIcon.svg (Geschäftskunden)
- GlobeIcon.svg (Weltweit)
- GroupIcon.svg (Kunden)
- HandshakeIcon.svg (Erfahrung)

**Builder note**: Reference these via ERGO's CDN URL, don't download.

---

## ERGO Logo

- SVG URL: `https://www.ergo.de/content/dam/ergo/grafiken/logos/ERGO-Logo-ohne-Claim.svg`
- Used in header with tagline "Einfach, weil's wichtig ist." beneath
- Tagline styling: italic, brand color (#8e0038)
