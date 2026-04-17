# ERGO Pages to Research

Curated list of pages that cover all unique component patterns. Ordered by priority.

## Tier 1: Core pages (research first)

| # | Page | URL | Why | Expected components |
|---|------|-----|-----|-------------------|
| 1 | Homepage | https://www.ergo.de | Main layout, hero, product overview | ErgoHeader, HeroBanner, ProductGrid, TrustBadges, ErgoFooter |
| 2 | All Products | https://www.ergo.de/de/Produkte | Product catalog | CategoryNav, ProductCard, FilterBar |
| 3 | Zahnzusatz (product page) | https://www.ergo.de/de/Produkte/Zahnzusatzversicherung | Product detail pattern | ProductHero, BenefitList, ComparisonTable, CTASection, FAQ |
| 4 | Kfz (product page) | https://www.ergo.de/de/Produkte/KFZ-Versicherung/Autoversicherung | Complex product detail | Same pattern but with calculator embed |

## Tier 2: Variant pages (research second)

| # | Page | URL | Why | Expected components |
|---|------|-----|-----|-------------------|
| 5 | Sterbegeld | https://www.ergo.de/de/Produkte/Sterbegeldversicherungen/Sterbegeldversicherung | Life insurance product pattern | May have unique calculator CTA |
| 6 | Haftpflicht | https://www.ergo.de/de/Produkte/Haftpflichtversicherung | Liability product — simpler | Possibly different CTAs |
| 7 | Rechtsschutz | https://www.ergo.de/de/Produkte/Rechtsschutzversicherung | Legal protection | Module/Baustein selection UI? |
| 8 | Ratgeber (advice) | https://www.ergo.de/de/Ratgeber | Content/blog pattern | ArticleCard, ContentGrid, Sidebar |

## Tier 3: Supporting pages (if budget allows)

| # | Page | URL | Why |
|---|------|-----|-----|
| 9 | Service overview | https://www.ergo.de/de/Service | Different layout pattern |
| 10 | Contact | https://www.ergo.de/de/Service/Kontakt | Form components, contact cards |
| 11 | About/Karriere | https://www.ergo.de/de/Karriere | Corporate page pattern |

## Depth strategy

- **Depth 0**: Homepage (1 page)
- **Depth 1**: Main sections linked from homepage (~5-6 pages)
- **Depth 2**: Individual product pages + ratgeber articles (~6-8 pages)
- **Total**: ~15 pages, well within Firecrawl free tier

## Expected component yield

Based on similar insurance sites, we'll likely find ~15-25 unique components:
- 3-4 layout (header, footer, section container, grid)
- 5-8 content (hero, product card, benefit list, comparison table, CTA, testimonial, trust badge, FAQ accordion)
- 2-3 navigation (main nav, breadcrumb, footer nav)
- 2-3 interactive (accordion, tabs, carousel)
- 2-3 typography (heading block, body block, label/badge)

Many will be variants of the same base pattern (e.g., ProductCard with different content).
