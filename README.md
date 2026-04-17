# demo-ui-lib

Theming-fähige React UI component library. Alle Komponenten nutzen CSS Custom Properties und lassen sich per `initTheme()` auf jedes Brand anpassen.

**Design-Tokens (ERGO-Default):** `#8e0038` Primär (Weinrot) · `#bf1528` Sekundär · `#333333` Text · `4px` Border-Radius · DM Sans / Arial

---

## Integration in ein externes Projekt

Es gibt zwei Wege die Library zu nutzen: **npm-Paket** (empfohlen für fertige Projekte) oder **Dateikopie** (empfohlen für Demos und Prototypen).

### Variante A: npm-Paket

```bash
npm install demo-ui-lib
```

**Voraussetzungen:**
- React ≥ 18 + React DOM ≥ 18 (Peer Dependencies)
- TypeScript ≥ 5.0 (empfohlen, nicht zwingend)

**1. CSS importieren**

Einmalig im App-Einstiegspunkt (z.B. `layout.tsx`, `main.tsx`, `index.tsx`):

```ts
import "demo-ui-lib/dist/index.css";
```

Ohne diesen Import haben die Komponenten **kein Styling**. Der Import lädt alle CSS Custom Properties (`--color-primary`, `--color-border`, etc.) und die Komponenten-Styles.

**2. Theme konfigurieren (optional)**

```ts
import { initTheme } from "demo-ui-lib";

// Eigene Markenfarben setzen — überschreibt die ERGO-Defaults
initTheme({
  primary: "#003366",   // z.B. Allianz-Blau
  secondary: "#0066cc",
});
```

Ohne `initTheme()` gelten die ERGO-Defaults (`#8e0038` / `#bf1528`). `initTheme()` kann jederzeit aufgerufen werden um Farben zur Laufzeit zu wechseln.

**3. Komponenten importieren**

```tsx
import { Button, TextInput, Select, Stepper } from "demo-ui-lib";
```

---

### Variante B: Dateikopie (für Demos)

Wenn das Projekt nicht als npm-Paket installiert werden soll (z.B. bei autonomen Demo-Builds), werden die Quelldateien direkt kopiert.

**Voraussetzungen:**
- Next.js ≥ 14 oder Vite + React ≥ 18
- TypeScript ≥ 5.0

**1. Dateien kopieren**

```bash
# UI-Komponenten
mkdir -p src/components/ui
cp -r <path-to-demo-ui-lib>/src/components/* src/components/ui/

# Theme (CSS Custom Properties + initTheme-Helper)
mkdir -p src/lib/theme
cp -r <path-to-demo-ui-lib>/src/theme/* src/lib/theme/
```

**2. Theme CSS importieren**

In `src/app/globals.css` (Next.js) oder im App-Root:

```css
@import "../lib/theme/theme.css";
```

Oder als TypeScript-Import im App-Layout/Root:

```ts
import "@/lib/theme/theme.css";
```

Ohne diesen Import fehlen die CSS Custom Properties und alle Komponenten sind unstyled.

**3. Komponenten importieren**

```tsx
import { Button } from "@/components/ui/Button/Button";
import { TextInput } from "@/components/ui/TextInput/TextInput";
import { Stepper } from "@/components/ui/Stepper/Stepper";
```

**4. Farben anpassen (optional)**

Entweder per `initTheme()`:

```ts
import { initTheme } from "@/lib/theme";
initTheme({ primary: "#003366", secondary: "#0066cc" });
```

Oder direkt in `globals.css` die CSS Custom Properties überschreiben:

```css
:root {
  --color-primary: #003366;
  --color-secondary: #0066cc;
}
```

---

### Automatisierter Setup mit `setup-demo.sh`

Für Demo-Projekte gibt es ein Setup-Script das alles automatisch macht:

```bash
cd <path-to-demo-ui-lib>
./setup-demo.sh my-demo-project
```

Das Script:
1. Kopiert das Base-Template (`next-demo-base/`) in ein neues Verzeichnis
2. Setzt den Supabase Table-Prefix in `.env.local`
3. Kopiert alle UI-Komponenten nach `src/components/ui/`
4. Kopiert das Theme nach `src/lib/theme/`
5. Kopiert die Ticket-Files nach `tickets/`
6. Führt `npm install` aus
7. Initialisiert ein Git-Repository

Voraussetzung: `.env.local` muss im Base-Template existieren (mit Supabase-Credentials).

---

## Vollständige CSS Custom Properties

Die `theme.css` definiert alle Design-Tokens. Externe Projekte können jede Variable in ihrem eigenen CSS überschreiben:

```css
:root {
  /* Farben */
  --color-primary: #8e0038;        /* Buttons, aktive States, Links */
  --color-secondary: #bf1528;      /* Sekundäre Akzente */
  --color-tertiary: #71022e;       /* Tertiärfarbe (Hover-States) */
  --color-text: #333333;           /* Standard-Textfarbe */
  --color-text-muted: #737373;     /* Hinweistexte, Labels */
  --color-border: #d9d9d9;         /* Input-Borders */
  --color-border-card: #c9c5c7;    /* Card-Borders */
  --color-bg-disabled: #f2f2f2;    /* Deaktivierte Elemente */
  --color-text-disabled: #aeaeae;  /* Deaktivierter Text */
  --color-focus: #326ec8;          /* Fokus-Ring */

  /* Hintergrundfarben (für Sektionen) */
  --color-bg-blue: #ccebed;
  --color-bg-green: #d3ebe5;
  --color-bg-yellow: #fef6d2;
  --color-bg-magenta: #f5e1eb;

  /* Border-Radien */
  --border-radius: 4px;            /* Standard (Inputs, Cards) */
  --border-radius-large: 8px;      /* Größere Container */
  --border-radius-pill: 100px;     /* Pill-Shapes (Badges) */
  --border-radius-button: 16px;    /* Buttons */

  /* Typografie */
  --font-family: "DM Sans", Arial, Helvetica, sans-serif;
  --font-family-heading: "Fedra Serif", Georgia, "Times New Roman", serif;

  /* Spacing (8px Grid) */
  --space-xxs: 4px;
  --space-xs: 12px;
  --space-s: 16px;
  --space-base: 24px;
  --space-m: 32px;
  --space-l: 48px;
  --space-xl: 64px;
  --space-xxl: 96px;

  /* Layout */
  --max-width: 1440px;
}
```

### Mindest-Override für eigenes Branding

Wer nur die Markenfarben ändern will, braucht nur 2 Variablen:

```css
:root {
  --color-primary: #003366;
  --color-secondary: #0066cc;
}
```

Alles andere (Borders, Hover-States, Fokus-Ringe) leitet sich automatisch ab oder nutzt neutrale Farben.

### Toast Provider

Wenn die `Toast`-Komponente verwendet wird, muss `ToastProvider` die App umschließen:

```tsx
import { ToastProvider } from "demo-ui-lib"; // oder "@/components/ui/Toast/Toast"

export default function Layout({ children }) {
  return (
    <ToastProvider>
      {children}
    </ToastProvider>
  );
}
```

---

## Komponenten

### Button

```tsx
<Button variant="primary" size="md" fullWidth={false} onClick={...}>
  Beitrag berechnen
</Button>
```

| Prop | Typ | Default |
|---|---|---|
| `variant` | `"primary" \| "secondary" \| "ghost"` | `"primary"` |
| `size` | `"sm" \| "md" \| "lg"` | `"md"` |
| `fullWidth` | `boolean` | `false` |

Alle nativen `<button>`-Attribute werden weitergereicht.

---

### Link

```tsx
<Link href="/datenschutz" variant="muted">Datenschutzhinweise</Link>
```

| Prop | Typ | Default |
|---|---|---|
| `variant` | `"default" \| "muted"` | `"default"` |

Alle nativen `<a>`-Attribute werden weitergereicht.

---

### TextInput

```tsx
<TextInput
  label="Vorname"
  placeholder="Max"
  hint="Wie auf dem Personalausweis."
  error="Bitte geben Sie einen gültigen Wert ein."
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` |
| `hint` | `string` |
| `error` | `string` |

Alle nativen `<input>`-Attribute werden weitergereicht.

---

### Textarea

```tsx
<Textarea
  label="Anmerkungen"
  placeholder="Haben Sie weitere Hinweise?"
  rows={4}
  error="Dieses Feld ist erforderlich."
/>
```

| Prop | Typ | Default |
|---|---|---|
| `label` | `string` | — |
| `hint` | `string` | — |
| `error` | `string` | — |
| `rows` | `number` | `4` |

---

### Select

```tsx
<Select
  label="Versicherungsart"
  placeholder="Bitte wählen"
  options={[
    { value: "risikoleben", label: "Risikolebensversicherung" },
    { value: "hausrat", label: "Hausratversicherung" },
  ]}
  error="Bitte treffen Sie eine Auswahl."
/>
```

| Prop | Typ |
|---|---|
| `options` | `{ value: string; label: string }[]` |
| `label` | `string` |
| `placeholder` | `string` |
| `hint` | `string` |
| `error` | `string` |

---

### Checkbox

```tsx
<Checkbox
  label="Ich stimme den Allgemeinen Versicherungsbedingungen zu."
  checked={checked}
  onChange={(e) => setChecked(e.target.checked)}
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` (required) |

Alle nativen `<input type="checkbox">`-Attribute werden weitergereicht.

---

### RadioButton

Rendert als auswählbare Karte mit Rand. Gleichen `name` für gruppierte Optionen verwenden.

```tsx
<RadioButton
  name="startdatum"
  value="01.06.2026"
  label="01.06.2026"
  description="In ca. 4 Wochen"
  checked={selected === "01.06.2026"}
  onChange={() => setSelected("01.06.2026")}
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` (required) |
| `description` | `string` |

Alle nativen `<input type="radio">`-Attribute werden weitergereicht.

---

### InlineRadio

Horizontale Radio-Gruppe für kurze Optionen wie Anrede oder Ja/Nein.

```tsx
<InlineRadio
  label="Anrede"
  value={anrede}
  onChange={setAnrede}
  options={[
    { value: "herr", label: "Herr" },
    { value: "frau", label: "Frau" },
    { value: "divers", label: "Divers" },
  ]}
/>
```

| Prop | Typ | Default |
|---|---|---|
| `label` | `string` | — |
| `options` | `{ value: string; label: string }[]` | — |
| `value` | `string` | — |
| `onChange` | `(value: string) => void` | — |
| `disabled` | `boolean` | `false` |

---

### Toggle

```tsx
<Toggle
  label="Dynamikerhöhung aktivieren"
  checked={enabled}
  onChange={(e) => setEnabled(e.target.checked)}
/>
```

| Prop | Typ |
|---|---|
| `label` | `string` (required) |

Alle nativen `<input type="checkbox">`-Attribute werden weitergereicht.

---

### SegmentedControl

Horizontaler Tab-Wechsler für exklusiv auswählbare Optionen.

```tsx
<SegmentedControl
  value={tarif}
  onChange={setTarif}
  options={[
    { value: "basis", label: "Basis" },
    { value: "komfort", label: "Komfort" },
    { value: "premium", label: "Premium" },
  ]}
/>
```

| Prop | Typ |
|---|---|
| `options` | `{ value: string; label: string }[]` |
| `value` | `string` |
| `onChange` | `(value: string) => void` |

---

### Slider

```tsx
<Slider
  min={50000}
  max={1000000}
  step={50000}
  value={value}
  onChange={setValue}
  label="Gewünschte Versicherungssumme"
  unit="€"
  formatLabel={(v) => `${v.toLocaleString("de-DE")} €`}
/>
```

| Prop | Typ | Default |
|---|---|---|
| `min` | `number` | — |
| `max` | `number` | — |
| `step` | `number` | `1` |
| `value` | `number` | — |
| `onChange` | `(value: number) => void` | — |
| `label` | `string` | — |
| `unit` | `string` | — |
| `formatLabel` | `(value: number) => string` | `toLocaleString` |

---

### DateInput

Drei separate Felder für Tag, Monat und Jahr.

```tsx
const [date, setDate] = useState({ day: "", month: "", year: "" });

<DateInput
  label="Geburtsdatum"
  value={date}
  onChange={setDate}
  hint="Die versicherte Person muss zwischen 18 und 69 Jahren alt sein."
  error="Bitte geben Sie ein gültiges Datum ein."
/>
```

| Prop | Typ |
|---|---|
| `value` | `{ day: string; month: string; year: string }` |
| `onChange` | `(value: DateValue) => void` |
| `label` | `string` |
| `hint` | `string` |
| `error` | `string` |

---

### Stepper

```tsx
<Stepper
  steps={[
    { label: "Tarifdaten" },
    { label: "Beitrag" },
    { label: "Persönliches" },
    { label: "Zusammenfassung" },
  ]}
  currentStep={2}
/>
```

| Prop | Typ |
|---|---|
| `steps` | `{ label: string }[]` |
| `currentStep` | `number` (1-basiert) |

---

### Tooltip

```tsx
<Tooltip
  content="Die Versicherungssumme bestimmt die Auszahlung im Leistungsfall."
  position="top"
>
  <button>Versicherungssumme</button>
</Tooltip>
```

| Prop | Typ | Default |
|---|---|---|
| `content` | `string` | — |
| `position` | `"top" \| "bottom" \| "left" \| "right"` | `"top"` |

---

### Card

Inhaltskarte mit optionalem CTA-Link.

```tsx
<Card
  title="Risikolebensversicherung"
  cta="Mehr erfahren"
  onCta={() => navigate("/risikoleben")}
>
  Schützen Sie Ihre Familie finanziell — auch wenn Sie nicht mehr da sind.
</Card>
```

| Prop | Typ |
|---|---|
| `title` | `string` |
| `cta` | `string` |
| `onCta` | `() => void` |
| `className` | `string` |

---

### Alert

Hinweisbox mit vier Varianten.

```tsx
<Alert variant="info">
  Ihre Sitzung läuft in 10 Minuten ab.
</Alert>
```

| Prop | Typ | Default |
|---|---|---|
| `variant` | `"info" \| "success" \| "warning" \| "error"` | `"info"` |

---

### Modal

```tsx
<Modal
  open={open}
  onClose={() => setOpen(false)}
  title="Einstellungen zum Datenschutz"
  footer={
    <>
      <Button variant="secondary" onClick={() => setOpen(false)}>Ablehnen</Button>
      <Button onClick={() => setOpen(false)}>Alle akzeptieren</Button>
    </>
  }
>
  <p>Modalinhalt...</p>
</Modal>
```

| Prop | Typ |
|---|---|
| `open` | `boolean` |
| `onClose` | `() => void` |
| `title` | `string` |
| `footer` | `React.ReactNode` |

Schließt per ESC-Taste und Klick auf den Hintergrund. Verhindert Hintergrundscrollen während des Öffnens.

---

### Toast

```tsx
import { useToast } from "demo-ui-lib";

function MeineKomponente() {
  const { show } = useToast();

  return (
    <button onClick={() => show("Änderungen gespeichert.", "success")}>
      Speichern
    </button>
  );
}
```

`show(message, variant?)` — Varianten: `"success"` `"error"` `"warning"` `"info"` (Default: `"info"`)

Toasts verschwinden automatisch nach 4 Sekunden und können manuell geschlossen werden.

---

## Entwicklung

```bash
npm run build                          # Library bauen (dist/)
npm run demo                           # Demo-App starten (http://localhost:5173)
npm run demo:ergo                      # ERGO-Demo starten (http://localhost:5174)
npm run screenshots -- --demo          # Demo-Screenshots erstellen
npm run screenshots -- --url=example.com  # Referenz-Screenshots einer Website erstellen
npm run test                           # Tests ausführen
npm run lint                           # Linting
```
