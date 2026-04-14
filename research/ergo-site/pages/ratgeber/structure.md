# ERGO Ratgeber — Structure Analysis

**URL**: https://www.ergo.de/de/Ratgeber
**Analyzed**: 2026-04-13

## Layout overview

```
+----------------------------------------------------------+
| [HEADER] Same                                             |
+----------------------------------------------------------+
| [HERO] .cmp-hero with image, title, subtitle              |
+----------------------------------------------------------+
| [FEATURED ARTICLE] Large article card with image + text   |
+----------------------------------------------------------+
| [ARTICLE GRID] PromoCards in 2-col layout                 |
| Topic sections: Rechtsportal, Haftpflicht, etc.           |
+----------------------------------------------------------+
| [SECTION HEADERS] Topic category labels                   |
+----------------------------------------------------------+
| [ARTICLE CARDS] Mix of PromoCard + ArticleTeaser          |
+----------------------------------------------------------+
| [TIPPS DER REDAKTION] ArticleTeaser carousel              |
+----------------------------------------------------------+
| [FOOTER] Same                                             |
+----------------------------------------------------------+
```

## NEW components

### 1. ArticleHeader (.cmp-article-header)
- Page-level header component for the Ratgeber section
- Contains hero image + title + subtitle
- Essentially a HeroBanner variant with article context

## Key observation
The Ratgeber page is primarily a content index — it reuses PromoCards (for article entries with images) and ArticleTeasers (for text-only article cards). No fundamentally new card patterns.

Layout is organized by topic categories (Rechtsportal, Haftpflichtversicherung articles, etc.) using the SectionHeader pattern.

## Reused components
- HeroBanner, PromoCard (vertical), ArticleTeaser, SectionHeader
- CarouselContainer, TileCard, CTAButton
- ErgoHeader, ErgoFooter
