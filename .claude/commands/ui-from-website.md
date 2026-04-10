Analysiere die Website **$ARGUMENTS** und baue ihre UI-Komponenten als React-Bibliothek nach.

## Ablauf

### 1. Referenz-Screenshots erstellen
Starte als erstes den Demo-Server falls noch nicht aktiv (`npm run demo`) und nimm dann Screenshots der Zielseite:
```bash
npm run screenshots -- --url=$ARGUMENTS
```
Screenshots landen in `screenshots/reference/`. Analysiere die erzeugten Bilder um Farben, Formen und Komponenten zu verstehen.

**Wenn der Screenshot "Access Denied" oder leer ist** (viele Sites blockieren Headless-Browser per CDN/Bot-Schutz):

Teile dem User mit, dass die Seite automatisierte Screenshots blockiert, und bitte ihn um manuelle Screenshots:

> Die Website blockiert automatisierte Screenshots. Für ein genaues Ergebnis brauche ich echte Bilder der Seite.
> Bitte mache in deinem Browser Screenshots von:
> 1. **Startseite** (Hero-Bereich mit Navigation)
> 2. **Einem Button-Paar** (primärer + sekundärer CTA, z. B. "Order Now" / "Learn More")
> 3. **Einem Formular oder Konfigurator-Schritt** (falls vorhanden)
> 4. **Farbakzenten** — z. B. hover-States, aktive Links, Checkboxen
>
> Ziehe die Screenshots einfach in den Chat. Du kannst diesen Schritt auch überspringen — dann basiert das Theme nur auf öffentlichen Brand-Quellen und kann von der echten UI abweichen.

- Wenn der User Screenshots liefert: analysiere sie sorgfältig (Farben per Augenschein, Schriftschnitt, Abstände, Eckenradien, Schatten) bevor du mit Schritt 2 weitermachst.
- Wenn der User überspringt: fahre mit Schritt 2 fort, weise aber am Ende der Arbeit darauf hin, dass ein manueller Abgleich mit der echten Site empfohlen wird.

**Wichtig — so nah wie möglich an der Referenz bleiben:**
Baue Komponenten pixel-genau nach dem was in den Screenshots sichtbar ist. Wenn z. B. ein RadioButton auf der Referenzseite keinen sichtbaren Radio-Kreis hat, dann lass ihn weg. Wenn ein Card-Element einen Subtitle-Text zeigt, füge eine `description`-Prop ein. Erfinde keine Elemente die in der Referenz nicht vorkommen, und lasse keine weg die sichtbar sind. Im Zweifelsfall: Referenz schlägt Konvention.

### 2. Design analysieren
- Fetch `$ARGUMENTS` und extrahiere CSS-Custom-Properties, Hex-Farben, Schriften, Border-Radius, Abstände
- Wenn CSS nicht direkt zugänglich, Brand-Kit suchen (schemecolor.com, brandfetch.com, WebSearch)
- Primär- und Sekundärfarbe identifizieren — **niemals raten**, immer verifizieren
- Typografie, Abstände, Eckenradien, Schatteneffekte notieren

### 3. Komponenten bestimmen
Typischer Satz für Formulare/Antragsstrecken — nur bauen was tatsächlich auf der Seite vorkommt:
- Button (primary / secondary / ghost, fullWidth)
- Link
- TextInput, Textarea, Select, DateInput
- Checkbox, RadioButton (Karten-Style wenn vorhanden), Toggle
- Slider (falls vorhanden)
- Stepper (für mehrstufige Flows)
- Tooltip, Modal, Toast

### 4. Theming-System aufsetzen
- `src/theme/theme.css` mit CSS Custom Properties als Defaults anlegen
- `src/theme/index.ts` mit `initTheme({ primary, secondary })` — injiziert `<style>`-Tag in `document.head`
- Alle Komponenten nutzen `var(--color-primary)` etc.
- Hover/Active-States mit `color-mix(in srgb, var(--color-primary) 82%, #000000)`

### 5. Jede Komponente anlegen
Struktur pro Komponente:
```
src/components/{Name}/
  {Name}.tsx      ← React-Komponente, importiert CSS
  {Name}.css      ← Styles via .classname + data-Attribute für Varianten
  index.ts        ← Re-export
```
Alle neuen Komponenten in `src/index.ts` exportieren.

### 6. Build-Setup prüfen
- `rollup.config.js` braucht `rollup-plugin-postcss` mit `extract: "index.css"`
- Consumer importiert: `import "demo-ui-lib/dist/index.css"`

### 7. Demo-App aktualisieren
- `demo/main.tsx` — alle Komponenten mit realistischen Beispielen zeigen
- Theme-Switcher oben (Color-Picker + `initTheme()`)
- `npm run demo` starten und Demo-Screenshots erstellen:
```bash
npm run screenshots -- --demo
```

### 8. README generieren
Dokumentation mit: Installation, CSS-Import, `initTheme()`-Aufruf, `ToastProvider`, Props-Tabellen für alle Komponenten, Entwicklungs-Commands.

## Wichtige Konventionen dieses Projekts
- Styling über CSS-Dateien (keine CSS-in-JS, keine Tailwind)
- Varianten über `data-variant`, `data-size` etc. als HTML-Attribute → CSS-Selektoren `[data-variant="primary"]`
- Multi-Element-Komponenten (Checkbox, Radio, Toggle) nutzen BEM-Klassen: `.checkbox__input`, `.checkbox__control`, `.checkbox__label`
- Kein `React.forwardRef` für einfache Wrapper — native Attribute per `...props` durchreichen
- `useId()` für automatisch generierte IDs bei Label-Input-Verknüpfungen
- Toast über Context: `<ToastProvider>` wrapping + `useToast()` Hook
- Modal und Toast rendern per `createPortal` auf `document.body`
