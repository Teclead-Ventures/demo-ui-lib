Analysiere eine Website und baue ihre UI-Komponenten als React-Bibliothek nach.

## Ablauf

### 1. Design analysieren
- Fetch die Zielseite und extrahiere CSS-Custom-Properties, Hex-Farben, Schriften, Border-Radius, Abstände
- Wenn CSS nicht direkt zugänglich, nach dem Brand-Kit suchen (z. B. schemecolor.com, brandfetch.com)
- Primär- und Sekundärfarbe identifizieren
- Screenshots der Referenzseite mit `npm run screenshots -- --ref` erstellen

### 2. Komponenten bestimmen
Typischer Satz für Formulare/Antragsstrecken:
- Button (primary / secondary / ghost, fullWidth)
- Link
- TextInput, Textarea, Select, DateInput
- Checkbox, RadioButton (Karten-Style wenn vorhanden), Toggle
- Slider (falls vorhanden)
- Stepper (für mehrstufige Flows)
- Tooltip, Modal, Toast

### 3. Theming-System aufsetzen
- `src/theme/theme.css` mit CSS Custom Properties als Defaults anlegen
- `src/theme/index.ts` mit `initTheme({ primary, secondary })` — injiziert `<style>`-Tag in `document.head`
- Alle Komponenten nutzen `var(--color-primary)` etc.
- Hover/Active-States mit `color-mix(in srgb, var(--color-primary) 82%, #000000)`

### 4. Jede Komponente anlegen
Struktur pro Komponente:
```
src/components/{Name}/
  {Name}.tsx      ← React-Komponente, importiert CSS
  {Name}.css      ← Styles via .classname + data-Attribute für Varianten
  index.ts        ← Re-export
```
Alle neuen Komponenten in `src/index.ts` exportieren.

### 5. Build-Setup prüfen
- `rollup.config.js` braucht `rollup-plugin-postcss` mit `extract: "index.css"`
- Consumer importiert: `import "demo-ui-lib/dist/index.css"`

### 6. Demo-App aktualisieren
- `demo/main.tsx` — alle Komponenten mit realistischen Beispielen zeigen
- Theme-Switcher oben (Color-Picker + `initTheme()`)
- `npm run demo` starten

### 7. Screenshots erstellen
```bash
npm run screenshots          # Demo + Referenzseite
npm run screenshots -- --demo  # nur Demo
npm run screenshots -- --ref   # nur Referenzseite
```
Screenshots landen in `screenshots/demo/` und `screenshots/reference/`.

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
