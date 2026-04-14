# Homepage Visual Comparison — Round 2 Diff Report

**Date**: 2026-04-14
**Focus**: Sections added in round 1 + remaining content issues

## Section: Services

- [CONTENT] Heading is wrong. Ours: "Wir sind für Sie da". ERGO: "Sparen Sie Zeit durch einfache Online-Services". Fix in `demo/ergo-site.tsx`.
- [CONTENT] Missing subtitle. ERGO has: "Informationen und Wissenswertes für ERGO Kunden und Interessierte". Fix: add `subtitle` prop to SectionHeader.
- [LAYOUT] Cards should be VERTICAL layout (large image top, content bottom), not horizontal. ERGO shows two tall side-by-side vertical cards with big images. Fix: change `layout="horizontal"` to `layout="vertical"` for both PromoCards.
- [CONTENT] Card 1 title: "Schaden melden" → "Schaden oder Leistungsfall melden"
- [CONTENT] Card 1 description: too short. ERGO: "Rechnungen einreichen, Schäden oder Leistungsfälle melden? Hier sind Sie richtig. Oder rufen Sie an."
- [CONTENT] Card 1 CTA: should be "Rechnung einreichen" with arrow variant (not "Jetzt melden" filled).
- [CONTENT] Card 2 title: "Kundenportal" → "Ihr ERGO Kundenportal"
- [CONTENT] Card 2 description: "Behalten Sie Ihre Versicherungen im Blick! Hier finden Sie viele Services, Ihr digitales Postfach und können bei Gewinnspielen mitmachen."
- [CONTENT] Card 2 badge: needs "Über 3 Mio." badge overlay. Use `badge` prop with URL: `https://assets.ergo.com/content/dam/ergo/grafiken/3-mio-kunden.dam.svg`
- [CONTENT] Card 2 CTA: should be "Zum Kundenportal" pill variant (not "Zum Portal" filled).
- [CONTENT] Bottom: needs "Alle Services ansehen" arrow CTA below the cards.

## Section: Wissenswertes

- [CONTENT] Heading wrong. Ours: "Gut zu wissen". ERGO: "Rundum gut informiert mit ERGO". Fix in demo.
- [CONTENT] Missing subtitle. ERGO: "Ihr Plus an Serviceleistungen".
- [CONTENT] Tile 1 (Kunden werben Kunden): needs PromoFlag "Aktion bis 31.12.2026" — add `flag` prop to the TileCard, but TileCard doesn't support `flag` yet. Alternative: wrap text in description mentioning the Geldprämie.
- [CONTENT] Tile 1 description: ERGO says "Für jeden neu geworbenen Kunden erhalten Sie eine Geldprämie von bis zu 150 € und sichern sich die Gewinnchance auf einen von 3 kleinen Goldbarren."
- [CONTENT] Tile 2 title: "Newsletter" → "Der ERGO Newsletter"
- [CONTENT] Tile 2 description: "Nichts mehr verpassen und immer top informiert."
- [CONTENT] Tile 3 title: "Geschäftskunden" → "Extra für Geschäftskunden"
- [CONTENT] Tile 3 description: "Eine passgenaue, breite Produktpalette für Gewerbe."
- [CONTENT] Tile CTA labels: should be "Gleich mitmachen", "Jetzt anmelden", "Zum Geschäftskundenbereich" (not generic "Mehr erfahren").

## Section: Warum ERGO Stats

- [LAYOUT] Stat tiles look correct — data mapping is right (stat=big text, title=label below). No changes needed.

## Section: Ratgeber

- [CONTENT] ERGO article teasers have a category label above the headline (e.g., "Schnarchschienen: Therapie und Hilfe bei Schnarchen") and a CTA "Mehr erfahren" (filled red). Our ArticleTeasers have the right structure but the content could be more accurate. Low priority — close enough.

---

## Summary of fixes (all in demo/ergo-site.tsx)

1. Services heading → "Sparen Sie Zeit durch einfache Online-Services"
2. Services subtitle → "Informationen und Wissenswertes für ERGO Kunden und Interessierte"
3. Services cards → `layout="vertical"` (not horizontal)
4. Services card content — match ERGO's exact titles, descriptions, CTAs
5. Services bottom → add "Alle Services ansehen" arrow CTA
6. Wissenswertes heading → "Rundum gut informiert mit ERGO"
7. Wissenswertes subtitle → "Ihr Plus an Serviceleistungen"
8. Wissenswertes tile content — match exact titles, descriptions, CTA labels
