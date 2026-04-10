# demo-ui-lib

Theming-fähige React UI component library. Alle Komponenten nutzen CSS Custom Properties und lassen sich per `initTheme()` auf jedes Brand anpassen.

**Design-Tokens (ERGO-Default):** `#8e0038` Primär (Weinrot) · `#bf1528` Sekundär · `#333333` Text · `4px` Border-Radius · FS Me / Arial

## Installation

```bash
npm install demo-ui-lib
```

React ≥ 18 ist als Peer Dependency erforderlich.

## Setup

### 1. CSS importieren

Einmalig im App-Einstiegspunkt (`main.tsx` / `index.tsx`):

```ts
import "demo-ui-lib/dist/index.css";
```

### 2. Theme konfigurieren

```ts
import { initTheme } from "demo-ui-lib";

initTheme({
  primary: "#8e0038",   // Primärfarbe (Buttons, aktive States)
  secondary: "#bf1528", // Sekundärfarbe
});
```

Beide Parameter sind optional — ohne Aufruf gelten die Defaults. `initTheme()` kann jederzeit aufgerufen werden um das Theme zur Laufzeit zu wechseln.

### 3. Toast Provider (nur bei Nutzung von Toast)

`ToastProvider` muss einmalig die App umschließen:

```tsx
import { ToastProvider } from "demo-ui-lib";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <ToastProvider>
    <App />
  </ToastProvider>
);
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
  <button>ⓘ Versicherungssumme</button>
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
npm run screenshots -- --demo          # Demo-Screenshots erstellen
npm run screenshots -- --url=example.com  # Referenz-Screenshots einer Website erstellen
npm run test                           # Tests ausführen
npm run lint                           # Linting
```
