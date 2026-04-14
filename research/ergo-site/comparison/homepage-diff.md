# Homepage Visual Comparison — Diff Report

**Date**: 2026-04-14
**ERGO URL**: https://www.ergo.de
**Demo URL**: http://localhost:5174/ergo-site.html
**Viewport**: 1440x900

## Section 1: Hero Banner

- [LAYOUT] **CRITICAL**: Hero text overlay is on the LEFT in our demo but on the RIGHT on ERGO. ERGO's layout: image fills the left ~60%, text content sits on the right ~40% with a white background. Fix: In `ErgoHeroBanner.css`, swap the grid — teaser should be `grid-column: 2` or put image first, text second. The `.ergo-hero__teaser` needs to be right-aligned.
- [CONTENT] Title "ERGO STERBEVORSORGE" is uppercase in our demo. On ERGO it's regular case "ERGO Sterbevorsorge". Fix: Remove `text-transform: uppercase` from `.ergo-hero__title` in `ErgoHeroBanner.css`.
- [LAYOUT] On ERGO the hero headline "Entlasten Sie Ihre Lieben" is rendered in a large serif font (Fedra Serif / our Source Serif 4). Our demo shows it correctly in serif. Font looks good.
- [COLOR] On ERGO, the "Beitrag berechnen" CTA is a filled red button with white text. Our demo renders it as filled too — this looks correct.

## Section 2: Bestseller Product Cards

- [COLOR] **CRITICAL**: On ERGO, the "Jetzt informieren" CTA buttons on product cards are FILLED RED (solid bg #8e0038, white text, fully rounded). In our demo, they appear as outline pills (transparent bg, red border). Fix: In `demo/ergo-site.tsx`, change the CTA variant from `"pill"` to `"filled"` for the bestseller card CTAs.
- [CONTENT] ERGO cards show badge overlays (Stiftung Warentest seal, Nebenkostencheck badge, ekomi badge) on the card images. Our demo passes no `badge` prop. Fix: Add `badge` prop with ERGO CDN URLs to each PromoCard in the demo.
- [LAYOUT] ERGO card images are taller relative to the content area. Our cards use `aspect-ratio: 16/10`. ERGO looks more like `16/9` or taller. Fix: Adjust `.ergo-promo--vertical .ergo-promo__image-container` aspect-ratio to `3/2`.

## Section 3: Aktuelles (blue bg)

- [COLOR] On ERGO, the tile cards in the Aktuelles section have the SAME blue background as the section (`#ccebed`), making them blend in seamlessly. Our demo also uses blue bg for tiles — this looks correct.
- [LAYOUT] ERGO shows 6 tiles in a 3×2 grid. Our demo shows 3 tiles in a single row carousel. Fix: Add 3 more tiles (Unfallversicherung, Krankenhauszusatz, Basis-Rente) to the demo and change carousel columns to `{ mobile: 1, tablet: 2, desktop: 3 }` with 6 items.

## Section 4: MISSING — Services Section

- [MISSING] **CRITICAL**: ERGO has a "SERVICES" section between Aktuelles and Kundenbewertungen with horizontal PromoCards (Schaden melden, Kundenportal). Our demo skips this entirely. Fix: Add a Services section in `demo/ergo-site.tsx` after Aktuelles, with 2 horizontal PromoCards.

## Section 5: Kundenbewertungen (green bg)

- [LAYOUT] Our demo looks close. The review quote, star rating 4.6/5, and review count are all present. On ERGO the stars are gold/yellow — ours are too. Looks good.
- [CONTENT] Minor: ERGO shows "Ermittelt aus **387.143** Bewertungen" — verify our count matches.

## Section 6: Kontakt

- [LAYOUT] ERGO has 4 contact tiles in a row (E-Mail, Chat, Berater, Telefon) + a bottom link "Alle Kontaktmöglichkeiten ansehen". Our demo has the 4 tiles but is missing the bottom CTA link. Fix: Add a centered "Alle Kontaktmöglichkeiten ansehen" arrow CTA below the tiles.
- [COLOR] ERGO's contact tiles have white backgrounds. Our demo also uses white for `variant="contact"`. Looks correct.

## Section 7: MISSING — Wissenswertes Section

- [MISSING] ERGO has a "WISSENSWERTES" section with yellow background (`#fef6d2`) containing 3 icon tiles (Kunden werben Kunden, Newsletter, Geschäftskunden). Our demo skips this. Fix: Add a Wissenswertes section with yellow bg and 3 TileCards.

## Section 8: MISSING — Seasonal Promo

- [MISSING] ERGO has a seasonal promo card ("Frühlings-Check") between Wissenswertes and Ratgeber — a horizontal PromoCard with image. Our demo skips this. Fix: Add a seasonal promo PromoCard (horizontal layout).

## Section 9: Ratgeber (magenta bg)

- [LAYOUT] Our demo shows ArticleTeasers correctly in a carousel on magenta background. Looks close to ERGO.
- [CONTENT] ERGO shows article cards with small circular images. Our ArticleTeaser component has no image — it's text-only. Fix: Add an optional `image` prop to ErgoArticleTeaser for the circular thumbnail.

## Section 10: Warum ERGO

- [LAYOUT] ERGO shows 3 stat tiles (Weltweit, 31 Mio., 100+ Jahre) with icons. Our demo has these. Looks correct.
- [CONTENT] On ERGO the stat number is the big text and the label is below. Our TileCard `stat` variant has `title` as the big text and `stat` as the label. The data mapping may be swapped — verify: "Weltweit" should be the title, "in über 20 Ländern" the stat.

## Section 11: EXTRA — FAQ Accordion

- [MISSING] Our demo has an FAQ Accordion section at the bottom. This does NOT exist on the ERGO homepage. Fix: Remove the FAQ section from the homepage demo. (Accordion is used on product detail pages, not the homepage.)

## Section 12: Footer

- [LAYOUT] ERGO footer has multiple columns of links, legal text, social icons. Our demo has a simplified version. Close enough for now — footer is lower priority.

---

## Summary of fixes needed

### Priority 1 (Critical — wrong layout/missing sections)
1. **Hero layout reversed** — text should be RIGHT, not LEFT
2. **3 missing sections** — Services, Wissenswertes, Seasonal Promo
3. **Remove FAQ accordion** — doesn't belong on homepage
4. **Card CTAs wrong variant** — should be `filled`, not `pill`

### Priority 2 (Content/color)
5. Hero title should not be uppercase
6. Add badge overlays to bestseller cards
7. Add 3 more Aktuelles tiles (6 total)
8. Add "Alle Kontaktmöglichkeiten ansehen" link below Kontakt
9. Card image aspect ratio adjustment (3/2 instead of 16/10)

### Priority 3 (Nice to have)
10. ArticleTeaser needs optional circular image
11. Verify stat tile data mapping (title vs stat)
