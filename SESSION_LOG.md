<!-- cSpell:locale de,en -->
# Session Log – 2026-04-23

Dokumentation aller Schritte, Konsolenbefehle und Prompts dieser Session.

---

## Prompts an Claude

| # | Prompt (Zusammenfassung) |
|---|--------------------------|
| 1 | Erstelle ein MD zur Session-Dokumentation – alle Befehle und Prompts festhalten |
| 2 | Erkläre kurz was der Skill `demo-factory` macht und was er braucht |
| 3 | `/demo-factory` mit Projektname Kevin-Test, 3 Produkte: Zahnzusatz, BU, Vollkasko |
| 4 | Feedback zum Ergebnis: ~30 Min Gesamtdauer, ~50k Tokens, Qualität gut, kleinere visuelle Overflow-Issues bei langen Wörtern in schmalen Containern, Supabase hat nicht funktioniert (nebensächlich) |
| 5 | Wizard-Container maxWidth von 560px auf 720px ändern |
| 6 | Bestätigung: Dev-Server läuft bereits, Änderungen sehen gut aus |
| 7 | Tarif-Karten Layout umbauen: Titel oben, Empfohlen-Tag darunter, Benefits mittig, Preis unten |
| 8 | Bestätigung: Karten sehen wie gewünscht aus ✓ |
| 9 | ERGO-Site Kontakt-Karten: farbige Hintergründe → weiß mit Rand |
| 10 | Bestätigung: Kontakt-Karten sehen viel besser aus ✓ |
| 11 | ERGO-Site Ratgeber + Warum ERGO Karten: bunte bgColors → weiß mit Rand |
| 12 | Bestätigung: Ratgeber + Warum ERGO korrekt umgesetzt ✓ |
| 13 | Ratgeber: Revert — Section-Hintergrund weiß, Cards wieder bunt (magenta/blau/grün) |
| 14 | Bestätigung: Ratgeber wie erwartet ✓ |
| 15 | ERGO Produktseite: Neuer Abschnitt "Flugzeugversicherungen" zwischen Pflege und Kfz |
| 16 | ERGO Produktseite: "Beitrag berechnen" bleibt filled, aber border-radius auf pill (rund) geändert |
| 17 | Bestätigung: Buttons genau wie gewünscht ✓ |
| 18 | cSpell-Locale auf de,en gesetzt für SESSION_LOG.md |
| 19 | Supabase Tracking-Fehler (500) gemeldet — API Key ungültig |
| 20 | Korrekten Supabase anon Key bereitgestellt (eyJ…) |
| 21 | Korrekte Supabase URL bereitgestellt (ecppykudtuileosvskie) |
| 22 | Tabellen noch nicht angelegt — SQL für 6 Tabellen (3× tracking + 3× applications) generiert |
| 23 | Ist im demo-factory Skill ein Vercel Deployment vorgesehen? → Ja |
| 24 | Vercel Deployment bitte durchführen |
| 25 | Session Log Dokumentation wieder aktivieren |
| 26 | Telefonservice: Erreichbarkeit 8–12 Uhr, 4,99 €/Min. aus dem Festnetz |
| 27 | Telefonservice-Änderung auf allen Seiten und Produkten durchziehen (5 Dateien) |
| 28 | Vercel Deployment manuell auslösen |

## Konsolenbefehle

| # | Befehl | Notizen |
|---|--------|---------|
| 1 | `git clone <repo> ~/coding/next-demo-base` | Base-Template geklont |
| 2 | Supabase Publishable Key bereitgestellt | `.env.local` im Template erstellt |
| 3 | Supabase URL + Key in `.env.local` korrigiert | URL: `ecppykudtuileosvskie`, Key: JWT anon Key |
| 4 | Submit-API camelCase→snake_case Konvertierung | `Kevin-Test/src/app/api/submit/route.ts` angepasst |
| 5 | `npm i -g vercel@latest` | CLI-Upgrade von 44.6.3 auf 51.6.1 (alte Version inkompatibel) |
| 6 | `vercel deploy --yes --prod` | Projekt `kevin-test` deployed, Scope: `kevinpandura-teclead-vents-projects` |
| 7 | `vercel env add` ×3 | SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, TABLE_PREFIX für Production gesetzt |
| 8 | `vercel deploy --yes --prod` | Redeploy mit Env-Vars |

## Sonstige Aktionen

- `SESSION_LOG.md` erstellt
- Demo Factory gestartet → **Blocker**: `next-demo-base` Template fehlt unter `/Users/kevinpandura/coding/`
- Blocker gelöst: `next-demo-base` geklont nach `/Users/kevinpandura/coding/next-demo-base`
- `setup-demo.sh Kevin-Test` ausgeführt → Table prefix: `run_20260423_1358`
- Multi-Produkt-Infrastruktur erstellt (Registry, Dynamic Routes, Tracking API, Tarife-Seite)
- **Zahnzusatz Pass 1** gebaut (Agent): Wizard, Pricing, Dashboard, 6 Wizard-Seiten
- Pass 1 Review: Theme-CSS fehlte → gefixt (`theme.css` Import + ToastProvider)
- Zahnzusatz Pass 2 (gezielter Fix, kein Rebuild) → committet
- **BU Pass 1** gebaut (Agent): 7 Wizard-Seiten, Pricing mit Berufsgruppen-Risikoklassen
- BU Pass 1 Review: Wizard und Homepage sehen gut aus
- **Kfz Pass 1** gebaut (Agent): 5 Wizard-Seiten, Template E Pricing mit SF-Klassen (51 Stufen)
- Kfz Pass 1 Review: Stepper-Labels passen, Wizard sieht sauber aus
- **Alle 3 Produkte fertig gebaut** ✓
- Visuelle Anpassungen: Wizard maxWidth 720px, Tarif-Karten Layout, ERGO-Site Cards, Flugzeug-Section, Button border-radius
- cSpell-Locale auf `de,en` gesetzt
- Supabase `.env.local` korrigiert (URL + anon Key)
- Submit-API: camelCase→snake_case Konvertierung hinzugefügt
- Vercel CLI aktualisiert (44.6.3 → 51.6.1)
- **Vercel Deployment** erfolgreich: `kevin-test-xi.vercel.app`
- Env-Vars auf Vercel gepusht (Supabase URL, Key, Table Prefix)
- Supabase-Tabellen: SQL für 6 Tabellen generiert (noch nicht ausgeführt)

## Ergebnis

| # | Produkt | Wizard-Seiten | Pricing-Modell | Status |
|---|---------|---------------|----------------|--------|
| 1 | Zahnzusatz | 6 | Template A (Alter-Polynomial) | ✓ |
| 2 | Berufsunfähigkeit | 7 | Template A (Alter + Berufsgruppe) | ✓ |
| 3 | Kfz/Vollkasko | 5 | Template E (HP+VK, SF-Klassen) | ✓ |

**Projekt**: `/Users/kevinpandura/coding/Kevin-Test/`
**Table prefix**: `run_20260423_1358`
**Vercel URL**: https://kevin-test-xi.vercel.app
**Noch offen**: GitHub Repo (gh CLI nicht installiert), Supabase Tabellen (SQL generiert, muss im Dashboard ausgeführt werden)

## User-Feedback

- **Gesamtdauer**: ~30 Minuten (inkl. User-Eingaben)
- **Token-Verbrauch**: ~50k Tokens
- **Qualität**: Gut
- **Bekannte Issues**:
  - Lange Wörter ragen bei schmalen Containern über den Rand hinaus (CSS overflow)
  - Supabase-Anbindung hat nicht funktioniert (nicht im Scope der Aufgabe)
  - Stepper-Labels werden bei 6+ Steps abgeschnitten (ellipsis)
